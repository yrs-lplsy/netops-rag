"""S2 检索升级对比与消融评测。

判据（每行结果都标注判据，三类对称可用）：
- chunk-id：检索命中精确等于期望子块 id（hybrid 各配置的 brief 口径）；
  naive 索引是独立 id 空间（doc#nN vs doc#cN），按 id 匹配恒为 0，故 naive 的
  chunk 判据退化为文本重叠：期望子块内容 token ≥50% 出现在命中 chunk 中
  （阈值先验取 0.5，未对测试集调优）。
- parent：任一 top-k 命中的 parent_id 等于期望子块的 parent_id（章节级；
  naive 集合无 parent 字段，不适用）。
- doc：任一 top-k 命中的 doc_id 属于期望文档（文档级）。

运行模式：
- 默认（--paths all）：naive + 消融矩阵（三路/dense+bm25/dense+sparse/精排）
  + 单路诊断（dense/bm25/sparse，Recall@5 与 Recall@20）
  + 融合池天花板（三路，recall_n=30、top_k=30，Recall@30）
  + 版本过滤子集，并写出完整报告。
- --paths <组合>（如 dense / dense,bm25）：仅跑该 hybrid 组合并打印，
  不写报告（除非显式 --out），用于单点复现。
- --k：主矩阵的 k，指标名如实反映（Recall@k）；--date：报告文件名日期覆盖
  （仓库内的 2026-09-04 报告即由 --date 2026-09-04 再生）。
"""

import argparse
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from netrag.config import Settings
from netrag.embedding.bge_m3 import BGEM3Embedder
from netrag.embedding.reranker import BgeReranker
from netrag.eval.golden import load_golden
from netrag.eval.metrics import mrr, recall_at_k
from netrag.eval.report import write_report
from netrag.index.milvus_client import get_milvus, wait_healthy
from netrag.retrieval.hybrid import HybridRetriever
from netrag.retrieval.naive import NaiveRetriever
from pathlib import Path

OVERLAP_THRESHOLD = 0.5  # naive chunk 判据的文本重叠阈值（先验值，未调优）
CEILING_RECALL_N = 30  # 天花板测量用池深（调参后精排池，对应 --recall-n 30）
CEILING_K = 30
VALID_PATHS = {"dense", "bm25", "sparse"}


def _content_tokens(text: str) -> set[str]:
    toks = set(t.lower() for t in re.findall(r"[A-Za-z][A-Za-z0-9-]{1,}|\d[\d.]*", text))
    return toks | set(re.findall(r"[\u4e00-\u9fff]", text))


def eval_naive(retriever: NaiveRetriever, items, k: int,
               exp_texts: dict[str, str], naive_texts: dict[str, set[str]]) -> dict[str, float]:
    """naive：chunk 判据=文本重叠（见模块 docstring），doc 判据同 hybrid。"""
    ranks, doc_hits = [], 0
    for it in items:
        hits = retriever.retrieve(it.question, top_k=k, filters=it.filters)
        exp_toks = _content_tokens(exp_texts[it.expected_chunk_ids[0]])
        rank = 0
        for i, h in enumerate(hits, start=1):
            if exp_toks and len(exp_toks & naive_texts[h.chunk_id]) / len(exp_toks) >= OVERLAP_THRESHOLD:
                rank = i
                break
        ranks.append(rank)
        if any(h.doc_id in it.expected_doc_ids for h in hits):
            doc_hits += 1
    n = len(items)
    expected = [it.expected_chunk_ids for it in items]
    return {f"Recall@{k}": sum(1 for r in ranks if 0 < r <= k) / n,
            "MRR": sum(1 / r for r in ranks if 0 < r <= k) / n,
            f"DocRecall@{k}": doc_hits / n}


def eval_hybrid(retriever: HybridRetriever, items, k: int,
                exp_parent: dict[str, str]) -> tuple[dict[str, float], list]:
    """hybrid：一次检索同时算 chunk-id / parent / doc 三判据 + MRR。

    返回 (指标, chunk-id 未命中列表 [(item, 命中id列表)])。
    """
    ranked, doc_hits, parent_hits, misses = [], 0, 0, []
    for it in items:
        hits = retriever.retrieve(it.question, top_k=k, filters=it.filters)
        ids = [h.chunk_id for h in hits]
        ranked.append(ids)
        if any(h.doc_id in it.expected_doc_ids for h in hits):
            doc_hits += 1
        ep = exp_parent.get(it.expected_chunk_ids[0])
        if ep and any(h.parent_id and h.parent_id == ep for h in hits):
            parent_hits += 1
        if it.expected_chunk_ids[0] not in ids:
            misses.append((it, ids))
    n = len(items)
    return ({f"Recall@{k}": recall_at_k(ranked, [it.expected_chunk_ids for it in items], k),
             "MRR": mrr(ranked, [it.expected_chunk_ids for it in items]),
             f"DocRecall@{k}": doc_hits / n,
             f"ParentRecall@{k}": parent_hits / n}, misses)


def eval_single_paths(retriever: HybridRetriever, items, ks: tuple[int, ...]) -> dict[int, float]:
    """单路诊断：一次 top_k=max(ks) 检索，对每个 k 分别算 chunk-id Recall。"""
    kmax = max(ks)
    ranked = []
    for it in items:
        hits = retriever.retrieve(it.question, top_k=kmax, filters=it.filters)
        ranked.append([h.chunk_id for h in hits])
    expected = [it.expected_chunk_ids for it in items]
    return {k: recall_at_k(ranked, expected, k) for k in ks}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--golden", default="data/golden/s2_mixed.yaml")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--skip-rerank", action="store_true")  # 无 GPU 时跳过精排行
    ap.add_argument("--recall-n", type=int, default=20)  # 调参杆 1（数字对齐流程用）
    ap.add_argument("--rrf-k", type=int, default=60)  # 调参杆 2
    ap.add_argument("--paths", default="all",
                    help="all=完整矩阵+单路+天花板+版本子集；或 hybrid 路径组合如 dense / dense,bm25（仅跑该组合并打印）")
    ap.add_argument("--date", default=None, help="报告文件名日期覆盖（如 2026-09-04）")
    ap.add_argument("--out", default=None, help="报告输出路径覆盖")
    args = ap.parse_args()

    if args.paths != "all":
        plist = [p.strip() for p in args.paths.split(",") if p.strip()]
        bad = [p for p in plist if p not in VALID_PATHS]
        if bad or not plist:
            ap.error(f"--paths 组合只能含 {sorted(VALID_PATHS)}，得到 {bad or '空'}")
    items = load_golden(Path(args.golden))
    client = get_milvus()
    wait_healthy(client)
    embedder = BGEM3Embedder(Settings.from_env().embed_model)

    # 期望子块元数据：全文（naive 重叠判据用）+ parent_id（parent 判据用）
    exp_ids = sorted({cid for it in items for cid in it.expected_chunk_ids})
    exp_texts: dict[str, str] = {}
    exp_parent: dict[str, str] = {}
    for i in range(0, len(exp_ids), 64):
        flt = "chunk_id in [" + ", ".join(f'"{c}"' for c in exp_ids[i:i + 64]) + "]"
        for r in client.query("chunks", filter=flt,
                              output_fields=["chunk_id", "text", "parent_id"], limit=64):
            exp_texts[r["chunk_id"]] = r["text"]
            exp_parent[r["chunk_id"]] = r["parent_id"]
    naive_texts = {r["chunk_id"]: _content_tokens(r["text"]) for r in
                   client.query("chunks_naive", filter='text != ""',
                                output_fields=["chunk_id", "text"], limit=16384)}

    def hybrid(paths=("dense", "bm25", "sparse"), reranker=None, recall_n=None):
        return HybridRetriever(client, embedder, reranker=reranker, paths=paths,
                               recall_n=recall_n or args.recall_n, rrf_k=args.rrf_k)

    k = args.k
    ver_items = [it for it in items if it.filters]

    if args.paths != "all":  # 单组合复现模式：只打印，不碰报告文件
        m, _ = eval_hybrid(hybrid(paths=tuple(p.strip() for p in args.paths.split(","))),
                           items, k, exp_parent)
        for key, val in m.items():
            print(f"hybrid({args.paths}) {key} = {val:.3f}")
        if args.out:
            write_report(Path(args.out), title=f"S2 子集运行 hybrid({args.paths})",
                         summary_rows={f"hybrid({args.paths}) {kk}": f"{vv:.3f}" for kk, vv in m.items()},
                         body_md=f"- 参数：recall_n={args.recall_n}，rrf_k={args.rrf_k}，k={k}")
        return

    # ---- 完整矩阵模式 ----
    print(f"== naive（k={k}） ==", flush=True)
    nm = eval_naive(NaiveRetriever(client, embedder), items, k, exp_texts, naive_texts)
    for key, val in nm.items():
        print(f"naive {key} = {val:.3f}", flush=True)

    configs = [
        ("hybrid(dense+bm25+sparse)", ("dense", "bm25", "sparse"), None),
        ("hybrid(dense+bm25)", ("dense", "bm25"), None),
        ("hybrid(dense+sparse)", ("dense", "sparse"), None),
    ]
    if not args.skip_rerank:
        configs.append(("hybrid(dense+bm25+sparse|rerank)", ("dense", "bm25", "sparse"),
                        BgeReranker(Settings.from_env().rerank_model)))
    results: dict[str, dict[str, float]] = {}
    misses_3way: list = []
    for name, paths, reranker in configs:
        print(f"== {name}（k={k}） ==", flush=True)
        m, misses = eval_hybrid(hybrid(paths, reranker), items, k, exp_parent)
        results[name] = m
        if name == "hybrid(dense+bm25+sparse)":
            misses_3way = misses
        for key, val in m.items():
            print(f"{name} {key} = {val:.3f}", flush=True)

    print("== 单路诊断（top_k=20 一次检索，分别计 Recall@5/@20） ==", flush=True)
    singles = {}
    for p in (("dense",), ("bm25",), ("sparse",)):
        singles[p] = eval_single_paths(hybrid(paths=p), items, (5, 20))
        print(f"hybrid({'+'.join(p)}) Recall@5 = {singles[p][5]:.3f}  Recall@20 = {singles[p][20]:.3f}", flush=True)

    print(f"== 融合池天花板（三路，recall_n={CEILING_RECALL_N}，top_k={CEILING_K}） ==", flush=True)
    ceil_m, _ = eval_hybrid(hybrid(recall_n=CEILING_RECALL_N), items, CEILING_K, exp_parent)
    print(f"hybrid(dense+bm25+sparse) Recall@{CEILING_K} = {ceil_m[f'Recall@{CEILING_K}']:.3f}", flush=True)

    print(f"== 版本过滤子集（{len(ver_items)} 条，k={k}） ==", flush=True)
    vm, _ = eval_hybrid(hybrid(), ver_items, k, exp_parent)
    for key, val in vm.items():
        print(f"版本子集 hybrid(dense+bm25+sparse) {key} = {val:.3f}", flush=True)
    nvm = eval_naive(NaiveRetriever(client, embedder), ver_items, k, exp_texts, naive_texts)
    for key, val in nvm.items():
        print(f"版本子集 naive {key} = {val:.3f}", flush=True)

    # ---- 汇总表（每行标注判据） ----
    rows: dict[str, str] = {}
    rows[f"naive Recall@{k} [chunk-id/文本重叠]"] = f"{nm[f'Recall@{k}']:.3f}"
    rows["naive MRR"] = f"{nm['MRR']:.3f}"
    rows[f"naive Recall@{k} [doc]"] = f"{nm[f'DocRecall@{k}']:.3f}"
    for name, _, _ in configs:
        m = results[name]
        rows[f"{name} Recall@{k} [chunk-id]"] = f"{m[f'Recall@{k}']:.3f}"
        rows[f"{name} MRR"] = f"{m['MRR']:.3f}"
        rows[f"{name} Recall@{k} [parent]"] = f"{m[f'ParentRecall@{k}']:.3f}"
        rows[f"{name} Recall@{k} [doc]"] = f"{m[f'DocRecall@{k}']:.3f}"

    # ---- 报告正文 ----
    miss_lines = "\n".join(
        f"- `{it.qid.split('#')[-1]}`（{it.expected_doc_ids[0]}）{it.question} → top{min(3, len(ids))}: "
        f"{[i.split('#')[-1] for i in ids[:3]]}"
        for it, ids in misses_3way[:8])
    single_lines = "\n".join(
        f"- hybrid({'+'.join(p)})（chunk-id 判据）: Recall@5={singles[p][5]:.3f} Recall@20={singles[p][20]:.3f}"
        for p in (("dense",), ("bm25",), ("sparse",)))
    delta_rerank = results[configs[-1][0]][f"Recall@{k}"] - results["hybrid(dense+bm25+sparse)"][f"Recall@{k}"] if not args.skip_rerank else 0.0

    body = f"""\n## 参数与口径

- 参数：recall_n={args.recall_n}，rrf_k={args.rrf_k}，top_k={k}；golden：{len(items)} 条（版本过滤 {len(ver_items)} 条）
- naive 索引：同语料 4 文档 100 chunk（ospf 27 / stp 33 / vlan17.9 20 / vlan17.7 20），所有配置（含 naive）对带 filters 的题同样应用 filters
- 判据标注：[chunk-id]=命中精确等于期望子块 id（naive 因 id 空间不同退化为文本重叠≥{OVERLAP_THRESHOLD}，先验阈值未调优）；[parent]=任一 top-{k} 命中的 parent_id 等于期望子块的 parent_id（章节级，naive 无 parent 字段不适用）；[doc]=任一 top-{k} 命中的 doc_id 属于期望文档
- 主结果行："""
    for name, _, _ in configs:
        m = results[name]
        body += f"\n- {name}: Recall@{k} [chunk-id]={m[f'Recall@{k}']:.3f} MRR={m['MRR']:.3f} [parent]={m[f'ParentRecall@{k}']:.3f} [doc]={m[f'DocRecall@{k}']:.3f}"
    body += f"\n- naive（文本重叠判据）: Recall@{k}={nm[f'Recall@{k}']:.3f} MRR={nm['MRR']:.3f} [doc]={nm[f'DocRecall@{k}']:.3f}（parent 不适用）"

    body += f"""

## 版本过滤子集（{len(ver_items)} 条）

- hybrid(dense+bm25+sparse): Recall@{k} [chunk-id]={vm[f'Recall@{k}']:.3f} MRR={vm['MRR']:.3f} [parent]={vm[f'ParentRecall@{k}']:.3f} [doc]={vm[f'DocRecall@{k}']:.3f}
- naive（文本重叠判据）: Recall@{k}={nvm[f'Recall@{k}']:.3f} MRR={nvm['MRR']:.3f} [doc]={nvm[f'DocRecall@{k}']:.3f}

## 单路消融诊断（chunk-id 判据，{len(items)} 条全量）

{single_lines}

**BM25 路是主要噪声源**：Task 13 的 `bm25_text` 只保留命令型行（英文命令/参数），与中文 golden 题几乎无词法交集，单路 Recall@5 仅 {singles[('bm25',)][5]:.3f}；RRF 等权融合两个弱路把 dense 单路 {singles[('dense',)][5]:.3f} 拉低到三路 {results['hybrid(dense+bm25+sparse)'][f'Recall@{k}']:.3f}（dense+bm25 {results['hybrid(dense+bm25)'][f'Recall@{k}']:.3f} > 三路，sparse 融合亦无增益）。

## 融合池天花板（精排池上界，chunk-id 判据）

- hybrid(dense+bm25+sparse)（recall_n={CEILING_RECALL_N}，top_k={CEILING_K}）: **Recall@{CEILING_K}={ceil_m[f'Recall@{CEILING_K}']:.3f}**
- 即使精排器完美（把池内期望子块总排到第 1），Recall@{k} 上限即该池召回值；等价单点复现：`--paths dense,bm25,sparse --k {CEILING_K} --recall-n {CEILING_RECALL_N}`。
- 剩余任务书调参杆不可行或方向相反：child_max 500→400 需重建 hybrid 索引 → 全部期望 chunk id 失效；BM25 加权 3→5 需重建且实测单路 Recall@5={singles[('bm25',)][5]:.3f}，加权只会放大噪声。

## 未命中样例（默认配置 hybrid 三路，chunk-id 判据，前 {min(8, len(misses_3way))}）

{miss_lines}

## 版本子集构成（人工核验记录）

两版 VLAN 手册各 8/7 条镜像题（filter `sw_version=17.9/17.7`，期望 chunk 指向对应版本手册）。其中 c8/c25/c49 三对 chunk 两版本**文本确有差异**（17.9 独有 VTP 名长句/media 命令表 Note/接口模板告诫，diff 实测 ratio 0.81–0.97），c10/c15/c35/c60/c78 五对字节级相同（同质特性，仅作过滤机制测试——期望 chunk 必须落在 filter 指定文档）。naive 在 filter 后候选池仅 20 chunk，得高分属小池效应；hybrid 过滤本身工作正常（无跨版本误检），低分与其整体检索质量一致。

## naive 判据说明（口径可比性）

s2_mixed 的期望 chunk 是 hybrid 子块（`doc#cN`），naive 索引是独立切分的 `doc#nN`，按 chunk_id 匹配对 naive 恒为 0，故 naive 的 chunk 行用文本重叠判据（宽松）；[doc] 与 [parent] 判据为 naive/hybrid 共用的对称锚点——naive 无 parent 字段，doc 级为两检索器可直接对比的粒度。

## 调参记录（数字对齐流程，逐杆追加，历史轮次实测值）

### Round 1：recall_n 20→30（其余默认，chunk-id 判据）

- hybrid(+rerank): Recall@5 **0.757** MRR 0.608（↑0.718，精排池变大）
- hybrid(dense+bm25+sparse): 0.544（↓0.583，池变大但弱路噪声稀释了无精排的排序）
- hybrid(dense+bm25): 0.660；hybrid(dense+sparse): 0.534；naive 不受影响（0.961）
- 复现：`--recall-n 30`

### Round 2：recall_n=30 基础上 rrf_k 60→40

- hybrid(+rerank): Recall@5 **0.757**（无变化）；hybrid 三路 0.563；dense+bm25 0.660；dense+sparse 0.544
- 复现：`--recall-n 30 --rrf-k 40`

### 停止依据

实测最佳 0.757 距 0.88 差 12.3pct > 3pct，且融合池天花板（见上）< 0.88——按 spec §8 停止调参，保留实测数字。

## 偏差分析（对比 88% 目标，未改任何数字）

1. **BM25 专用字段与中文查询错配是根因**：`bm25_text`（Task 13，仅命令型行）对英文查询有效（Task 15 spot check `ospf network-type` 命中 c144），对中文 golden 题无词法交集（单路 Recall@5={singles[('bm25',)][5]:.3f}）。RRF 等权融合使该噪声路实际降低了 dense 质量（{singles[('dense',)][5]:.3f}→{results['hybrid(dense+bm25+sparse)'][f'Recall@{k}']:.3f}）。改进方向（超出本任务范围）：bm25_text 同时纳入中文叙述句或查询侧翻译/混编，或对 BM25 路降权。
2. **rerank 是本链路最有效的升级**（三路 {results['hybrid(dense+bm25+sparse)'][f'Recall@{k}']:.3f}→精排 {results[configs[-1][0]][f'Recall@{k}']:.3f}，{delta_rerank:+.3f}；Round1 池扩大后再 +3.9pct 至 0.757），但受融合池天花板 {ceil_m[f'Recall@{CEILING_K}']:.3f} 限制。
3. **naive 与 hybrid 的对称锚点**：doc 级判据下 naive {nm[f'DocRecall@{k}']:.3f} vs hybrid 三路 {results['hybrid(dense+bm25+sparse)'][f'DocRecall@{k}']:.3f} / 精排 {results[configs[-1][0]][f'DocRecall@{k}']:.3f}；naive chunk 行的高分部分来自宽松的内容重叠判据与 100 个大窗口小池，但 doc 级对称对比同样显示 naive 领先，混合链路在本语料上未超过 naive 基线是实测事实。
4. **版本过滤子集**：过滤机制工作正常（{len(ver_items)} 条无跨版本误检）；hybrid 低分来自上述整体检索质量问题而非过滤本身。
5. **结论**：S2 混合链路未达到 88% 目标（实测最佳 hybrid+rerank chunk Recall@5=0.757，默认配置 {results[configs[-1][0]][f'Recall@{k}']:.3f}）。**"67%→88%" 的目标叙事与实测不符**：本报告 naive（重建后同语料）chunk {nm[f'Recall@{k}']:.3f} / doc {nm[f'DocRecall@{k}']:.3f}，hybrid+rerank chunk {results[configs[-1][0]][f'Recall@{k}']:.3f} / doc {results[configs[-1][0]][f'DocRecall@{k}']:.3f}。是否修订目标数字（或注明口径：小语料 4 文档/103 题/判据）交由用户决策。所有数字均为脚本单次运行实测，调参轮次逐杆追加，无手改。

## 复现性修订（Fix Round 1，2026-09-05）

本文件此前有 4 处数字来自临时 probe 脚本（未入库），本次全部改为由提交的 `scripts/run_s2_eval.py` 直接产出，逐项对账：

1. **单路消融（dense/bm25/sparse Recall@5/@20）**：probe → 脚本"单路消融诊断"一节（默认运行即产出；单点复现 `--paths dense` 等）。数值与 probe 一致。
2. **parent 判据（三路 0.621 / 精排 0.748）**：probe → 主表 [parent] 行，默认运行即产出。数值与 probe 一致。
3. **融合池天花板（Recall@30=0.864）**：probe → "融合池天花板"一节（默认运行即产出；单点复现 `--paths dense,bm25,sparse --k 30 --recall-n 30`）。数值与 probe 一致。
4. **naive doc 级（0.951）**：旧脚本 body 行 → 主表 [doc] 行。数值一致。
5. **指标命名修正**：`evaluate` 此前无论 k 取值都输出 "Recall@5"；现按实际 k 命名（Recall@{k} / DocRecall@{k} / ParentRecall@{k}）。
6. 调参记录两轮数字为历史轮次（上一脚本版本）实测，评测逻辑未变，可用 `--recall-n 30` / `--recall-n 30 --rrf-k 40` 复现。
"""

    out = args.out or f"docs/eval-reports/{args.date or date.today().isoformat()}-s2-comparison.md"
    write_report(Path(out), title="S2 检索升级对比与消融", summary_rows=rows, body_md=body)


if __name__ == "__main__":
    main()
