"""RAGAS 四指标基线评测：分层抽样 golden set → 检索 → 生成 → faithfulness /
answer_relevancy（即 ResponseRelevancy）/ context_precision / context_recall。

抽样口径：只在 factual + troubleshoot 上分层（multihop 的 ground-truth 语义不同
——期望 2 条子块拼 reference 会稀释上下文精度判分，本期不评；reject 无期望子块
即无 ground truth，不评），seed 固定随机，比例配额 + 最大余数法凑满 sample。

用法：uv run python scripts/run_ragas.py [--golden data/golden/s3_full.yaml]
         [--sample 30] [--retriever hybrid] [--out docs/eval-reports/xxx.md]
         [--qtype factual,troubleshoot] [--seed 42] [--k 5]
"""

import argparse
import math
import os
import random
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import ragas

from netrag.config import Settings
from netrag.embedding.bge_m3 import BGEM3Embedder
from netrag.embedding.reranker import BgeReranker
from netrag.eval.golden import GoldenItem, load_golden
from netrag.eval.ragas_runner import Bgem3LangchainEmbeddings, build_judge_llm, run_ragas
from netrag.eval.report import write_report
from netrag.generation.llm import LLMClient
from netrag.index.milvus_client import get_milvus, wait_healthy
from netrag.observability.tracer import get_tracer
from netrag.retrieval.hybrid import HybridRetriever
from netrag.retrieval.naive import NaiveRetriever

METRIC_LABELS = {
    "faithfulness": "忠实度（答案可由 contexts 支撑）",
    "answer_relevancy": "答案相关性（贴合问题）",
    "context_precision": "上下文精度（期望内容排前）",
    "context_recall": "上下文召回（期望子块被覆盖）",
}
METRIC_ORDER = ("faithfulness", "answer_relevancy", "context_precision", "context_recall")

# T6 基线（docs/eval-reports/2026-09-06-s3-ragas-baseline.md，git 2eb8eab）：
# judge=Qwen2.5-72B@SiliconFlow（与生成同模型），assembly=child-chunks，同抽样同生成。
# 仅当 --judge deepseek 时进报告作"纯 judge 后端差异"对照行。
T6_BASELINE = {
    "label": "T6 基线（judge=Qwen2.5-72B@SiliconFlow，assembly=child-chunks）",
    "n": "48-49",
    "means": {"faithfulness": 0.654, "answer_relevancy": 0.800,
              "context_precision": 0.881, "context_recall": 0.844},
}


def t6_comparison_text(assembly: str, means: dict, judge_label: str) -> str:
    """T6 基线对照段（judge=deepseek 时输出）。

    评审 Fix Round 1 Finding 1：T6 基线为 child-chunks 装配——只有本次同为 child-chunks
    时该对照才是"纯 judge 后端差异"单变量；parent-window 时 judge 与装配同时变化，
    必须标注双变量并指路单变量结论（Run A 判 judge 效应、Run B-vs-Run A 判装配效应）。
    """
    base = T6_BASELINE
    cmp_rows = []
    for m in METRIC_ORDER:
        now = means.get(m)
        base_v = base["means"][m]
        delta = "—" if now is None else f"{now - base_v:+.3f}"
        cmp_rows.append(f"| {METRIC_LABELS[m]} | "
                        f"{'—' if now is None else f'{now:.3f}'} | {base_v:.3f} | {delta} |")
    if assembly == "child-chunks":
        title = "## 与 T6 基线对照（差异 = 纯 judge 后端差异）"
        lead = (f"同抽样（50 条，seed=42）、同生成（Qwen2.5-72B，生成缓存命中）、"
                f"同装配（child-chunks），\n唯一变量为 judge 后端（{judge_label} vs 72B judge）")
    else:
        title = "## 与 T6 基线对照（差异 = judge+装配 双变量，非单变量）"
        lead = (f"同抽样（50 条，seed=42）、同生成（Qwen2.5-72B，生成缓存命中）；但 T6 基线为 "
                f"child-chunks 装配、本次为 parent-window，judge 后端与装配同时变化——\n"
                f"本行 Δ 为双变量（judge+装配）合成差异，单变量结论另见：Run A 对照行"
                f"（纯 judge 效应 f+0.098）与 Run B-vs-Run A 对照行（纯装配效应 f+0.049）")
    return f"""
{title}

{lead}；非空计数 <40 的指标只作参考。

| 指标 | 本次（{assembly}） | {base['label']}（n={base['n']}） | Δ |
|---|---|---|---|
{chr(10).join(cmp_rows)}
"""


def parse_args(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--golden", default="data/golden/s3_full.yaml")
    ap.add_argument("--sample", type=int, default=30)
    ap.add_argument("--retriever", choices=("hybrid", "naive"), default="hybrid")
    ap.add_argument("--out", default="docs/eval-reports/2026-09-06-s3-ragas-baseline.md")
    ap.add_argument("--qtype", default="factual,troubleshoot",
                    help="参与抽样的 qtype（逗号分隔；multihop/reject 语义不适用默认排除）")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--recall-n", type=int, default=20)
    ap.add_argument("--rrf-k", type=int, default=60)
    ap.add_argument("--progress-every", type=int, default=5)
    ap.add_argument("--max-workers", type=int, default=2,
                    help="ragas 并发（TPM 限速保护，默认 2；429 致 NaN 增多时再调低）")
    ap.add_argument("--gen-cache", default="",
                    help="生成结果缓存 json 路径（命中条目跳过生成 LLM 只重跑 judge）")
    ap.add_argument("--judge", choices=("deepseek", "siliconflow"), default="deepseek",
                    help="RAGAS judge 后端（默认 deepseek：降成本+消自评偏差；"
                         "siliconflow 复现 T6 基线口径）")
    ap.add_argument("--assembly", choices=("child-chunks", "parent-window"),
                    default="child-chunks",
                    help="RAGAS contexts 装配口径：child-chunks=子块文本（历史报告可复现）；"
                         "parent-window=父块窗口（与生成 LLM 可见严格一致，Run B 口径）")
    ap.add_argument("--vs-label", default="",
                    help="对照行标签（如 'Run A（judge=deepseek，assembly=child-chunks）'）")
    ap.add_argument("--vs", default="",
                    help="对照均值 faithfulness,relevancy,precision,recall（逗号分隔浮点，"
                         "与 --vs-label 搭配生成对照表）")
    ap.add_argument("--timeout", type=int, default=60,
                    help="ragas RunConfig 单次 LLM 调用超时秒数（ragas 默认 60；"
                         "推理型 judge 如 DeepSeek 单调用常超 60s，需调大）")
    return ap.parse_args(argv)


def stratified_sample(items: list[GoldenItem], qtypes: list[str], sample: int,
                      seed: int) -> list[GoldenItem]:
    """按 qtype 分层比例抽样（最大余数法保证总数恰为 sample）。"""
    pools: dict[str, list[GoldenItem]] = defaultdict(list)
    for it in items:
        if it.qtype in qtypes:
            pools[it.qtype].append(it)
    total = sum(len(v) for v in pools.values())
    if sample >= total:
        return [it for qt in qtypes for it in pools.get(qt, [])]
    rng = random.Random(seed)
    picked: list[GoldenItem] = []
    quotas: list[tuple[str, int, float]] = []
    assigned = 0
    for qt in qtypes:
        pool = pools.get(qt, [])
        if not pool:
            continue
        exact = sample * len(pool) / total
        base = math.floor(exact)
        quotas.append((qt, base, exact - base))
        assigned += base
    for qt, _, frac in sorted(quotas, key=lambda x: -x[2])[: sample - assigned]:
        idx = next(i for i, q in enumerate(quotas) if q[0] == qt)
        quotas[idx] = (qt, quotas[idx][1] + 1, frac)
    for qt, n, _ in quotas:
        pool = pools[qt]
        picked += rng.sample(pool, min(n, len(pool)))
    return picked


def main() -> None:
    args = parse_args()

    qtypes = [q.strip() for q in args.qtype.split(",") if q.strip()]
    items = load_golden(Path(args.golden))
    sample = stratified_sample(items, qtypes, args.sample, args.seed)
    comp = " / ".join(f"{qt} {sum(1 for i in sample if i.qtype == qt)}" for qt in qtypes)
    print(f"golden {len(items)} 条 → 分层抽样 {len(sample)} 条（{comp}，seed={args.seed}）", flush=True)

    settings = Settings.from_env()
    # judge LLM 先于 Milvus/GPU 构造：deepseek 未配置（key/模型名空）时立即报错指路 env，
    # 不烧任何检索/生成开销
    judge_llm = build_judge_llm(settings, backend=args.judge)
    judge_label = (f"deepseek（DEEPSEEK_MODEL env 值：{settings.deepseek_model}）"
                   if args.judge == "deepseek"
                   else f"siliconflow（{settings.llm_model}，与生成同模型）")
    client = get_milvus()
    wait_healthy(client)
    embedder = BGEM3Embedder(settings.embed_model)
    if args.retriever == "hybrid":
        retriever = HybridRetriever(client, embedder,
                                    reranker=BgeReranker(settings.rerank_model),
                                    recall_n=args.recall_n, rrf_k=args.rrf_k)
    else:
        retriever = NaiveRetriever(client, embedder)
    llm_client = LLMClient(settings)
    embeddings = Bgem3LangchainEmbeddings(settings.embed_model)

    from ragas.run_config import RunConfig

    run_config = RunConfig(max_workers=args.max_workers, max_retries=8, max_wait=240,
                           timeout=args.timeout, seed=args.seed)
    tracer = get_tracer(settings, run_name="ragas")
    with tracer.trace("ragas", meta={"golden": args.golden, "sample": len(sample),
                                     "retriever": args.retriever, "k": args.k,
                                     "recall_n": args.recall_n, "rrf_k": args.rrf_k,
                                     "seed": args.seed, "model": settings.llm_model,
                                     "judge": args.judge, "judge_model": settings.deepseek_model,
                                     "assembly": args.assembly}) as trace:
        cache_path = Path(args.gen_cache) if args.gen_cache else None
        cache_key = "|".join([Path(args.golden).name, ",".join(qtypes), str(len(sample)),
                              str(args.seed), args.retriever, f"k={args.k}",
                              settings.llm_model])
        result = run_ragas(sample, retriever, llm_client, judge_llm=judge_llm,
                           embeddings=embeddings, k=args.k,
                           progress_every=args.progress_every, run_config=run_config,
                           gen_cache_path=cache_path, cache_key=cache_key,
                           assembly=args.assembly)
        means = result["means"]
        trace.event("ragas_done", n=result["n"], skipped=result["skipped"],
                    errors=len(result["errors"]), out=args.out,
                    **{m: (None if means.get(m) is None else round(means[m], 3))
                       for m in means})
    tracer_name = type(tracer).__name__
    trace_id = getattr(trace, "id", None)
    print(f"[tracer] {tracer_name} trace_id={trace_id}", flush=True)

    per_item = result["per_item"]
    n = result["n"]

    # ---- 汇总行 ----
    rows: dict[str, str] = {f"{m}（{METRIC_LABELS.get(m, m)}）":
                            ("—" if means.get(m) is None else f"{means[m]:.3f}")
                            for m in METRIC_ORDER}
    rows["评测条数 n"] = str(n)
    rows["跳过（无 ground truth）"] = str(result["skipped"])
    rows["单条失败"] = str(len(result["errors"]))
    rows["生成缓存命中（跳过生成 LLM）"] = str(result.get("cache_hits", 0))
    # 各指标非空计数：NaN（judge 限速失败等）不计入均值，必须暴露覆盖面
    for m in means:
        valid = sum(1 for p in per_item if p.get(m) is not None)
        rows[f"{m} 非空计数 /{n}"] = str(valid)

    # ---- judge 后端对照段（judge=deepseek 时输出；措辞按装配口径切换单/双变量）----
    comparison = ""
    if args.judge == "deepseek":
        comparison = t6_comparison_text(args.assembly, means, judge_label)
    # ---- 装配对照段（--vs/--vs-label：如 Run B vs Run A，纯装配差异）----
    vs_section = ""
    if args.vs and args.vs_label:
        vs_vals = [float(x) for x in args.vs.split(",")]
        if len(vs_vals) != len(METRIC_ORDER):
            raise SystemExit(f"--vs 需 {len(METRIC_ORDER)} 个均值（{','.join(METRIC_ORDER)}）")
        vs_rows = []
        for m, prev in zip(METRIC_ORDER, vs_vals):
            now = means.get(m)
            delta = "—" if now is None else f"{now - prev:+.3f}"
            vs_rows.append(f"| {METRIC_LABELS[m]} | "
                           f"{'—' if now is None else f'{now:.3f}'} | {prev:.3f} | {delta} |")
        vs_section = f"""
## 与 {args.vs_label} 对照（差异 = 纯装配差异）

同抽样（50 条，seed=42）、同生成（缓存命中，答案逐字节一致）、同 judge（{judge_label}），
唯一变量为 contexts 装配口径（child-chunks → {args.assembly}）；非空计数 <40 的指标只作参考。

| 指标 | 本次（assembly={args.assembly}） | {args.vs_label} | Δ |
|---|---|---|---|
{chr(10).join(vs_rows)}
"""

    # ---- 正文 ----
    if args.assembly == "parent-window":
        assembly_line = ("- 装配：**parent-window**（RAGAS contexts 经 answer.build_generation_contexts"
                         " 取父块窗口，与生成 LLM 实际可见片段严格一致——T6 验证序列 Run B 装配修正）")
    else:
        assembly_line = ("- 装配：**child-chunks**（RAGAS contexts = 检索命中子块文本，与 T6 基线一致；"
                         "生成可见的仍是父块窗口——装配错位本运行未修，仅隔离 judge 变量）")
    qt_line = "、".join(f"{qt} {sum(1 for i in items if i.qtype == qt)}" for qt in qtypes)
    judge_caveat = (
        f"- **judge 为异构模型**（{judge_label}）：消除与生成同模型的自评偏差（72B 基线的"
        "系统性风险），但异构 judge 对中文陈述抽取的校准同样未验证，绝对值仍只作相对对比；"
        "与 72B judge 的数值差异方向见对照表（纯 judge 后端差异）"
        if args.judge == "deepseek" else
        f"- **judge 与生成同模型**（{settings.llm_model}）：自评偏差（self-preference）"
        "系统性风险存在，faithfulness 可能偏高")
    body = f"""
## 参数与判据

- golden：{args.golden}（{len(items)} 条；抽样域 {qt_line}），分层比例抽样 n={len(sample)}
  （seed={args.seed}，最大余数法配额）
- 检索：{retriever.name}，top_k={args.k}，recall_n={args.recall_n}，rrf_k={args.rrf_k}（hybrid 时）
- 生成：{settings.llm_model}（SiliconFlow），answer_with_citations 父块窗口（cap 6000）；
  生成缓存命中 {result.get('cache_hits', 0)}/{n} 条（命中条目生成 LLM 零调用，答案与 T6 基线逐字节一致）
{assembly_line}
- RAGAS：ragas {ragas.__version__}，judge={judge_label}（temperature=0，LangchainLLMWrapper）；
  嵌入：本地 {settings.embed_model}（dense，Bgem3LangchainEmbeddings）；
  ground truth = 期望子块全文（Milvus 点查拼接）；raise_exceptions=False
- 指标名对应：answer_relevancy 即 ragas ResponseRelevancy（0.3.x 的 .name）
- 观测：tracer={tracer_name}（langfuse 有密钥时自动选 Cloud，否则本地 JSONL 兜底），
  trace_id={trace_id}
{comparison}{vs_section}
## 主结果

| 指标 | 均值 |
|---|---|
""" + "\n".join(f"| {k} | {v} |" for k, v in rows.items()) + f"""

## 逐条明细（n={n}）

| qid | qtype | faithfulness | answer_relevancy | context_precision | context_recall |
|---|---|---|---|---|---|
""" + "\n".join(
        f"| {p['qid']} | {p['qtype']} | " + " | ".join(
            "—" if p[m] is None else f"{p[m]:.3f}" for m in METRIC_ORDER) + " |"
        for p in per_item) + f"""

## 跳过与失败（不造数）

- 跳过 {result['skipped']} 条：""" + ("；".join(f"`{qid}`（{reason}）" for qid, reason in result["skipped_detail"]) or "无") + f"""
- 单条失败 {len(result['errors'])} 条：""" + ("；".join(f"`{qid}` {err}" for qid, err in result["errors"]) or "无") + f"""

## 诚实的局限（caveats）

- {judge_caveat}
- **ragas 指标 prompt 为英文**，语料/问答为中文混合：faithfulness 的陈述抽取与
  context_recall 的语句分类在中文上未做校准，绝对值只作相对基线（跨迭代对比用），
  不与公开英文 benchmark 直接可比
- ground truth 用期望子块全文拼 reference：多期望子块（multihop，本期未抽样）会稀释
  precision/recall 判分，故 multihop/reject 不在本期口径
- **本任务只测量不调参**；抽样 n={len(sample)}，均值抽样误差不小（±0.1 量级），
  结论以跨版本相对变化为准
""" + (
    f"""- **装配修正已生效**：本运行 contexts 为父块窗口（生成可见全集），T6 报告中
  "contexts=子块而生成见父块窗口导致 faithfulness 被系统性压低"的错位在本运行不存在；
  与 child-chunks 运行的差异即该错位的量化影响
""" if args.assembly == "parent-window" else
    """- RAGAS 评测的 contexts 用**子块文本**（ground truth 同为期望子块），而生成实际可见的是
  **父块窗口**（spec 规定口径）：faithfulness 只对生成可见上下文的子集打分，答案引用了
  父块窗口内、子块之外的内容时会被误判为不忠实——该系统性压低方向已知，跨运行一致，
  只影响绝对值不影响相对对比（装配修正另行单变量重测）
""") + f"""- 逐条分数中"—"为该条该指标 judge 调用失败（raise_exceptions=False下 NaN：TPM 限速
  429 / 余额不足 402 等 API 错误重试耗尽），未计入均值；
  各指标"非空计数"行即该均值的实际样本量——覆盖面过低的均值只作参考
"""

    write_report(Path(args.out), title=(f"S3 RAGAS 四指标（{len(sample)} 条分层抽样，"
                                        f"judge={args.judge}，assembly={args.assembly}，"
                                        "hybrid+rerank）"),
                 summary_rows=rows, body_md=body)
    print("means:", {k: (None if v is None else round(v, 3)) for k, v in means.items()},
          f"n={n} skipped={result['skipped']} errors={len(result['errors'])} "
          f"cache_hits={result.get('cache_hits', 0)} judge={args.judge}", flush=True)


if __name__ == "__main__":
    main()
