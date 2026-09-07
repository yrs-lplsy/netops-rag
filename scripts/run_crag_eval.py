"""CRAG 评测（对齐③）：troubleshoot 40 条子集上 CRAG 开/关对比 + 救回/损失配对。

口径（报告正文同文）：
- 自动解决（一条题在某配置下）= final answer 非 fallback 文本（handoff=False）
  且 citations 命中期望文档（任一 citation 的 doc_id ∈ expected_doc_ids）
- 转人工 = handoff=True
- 初次低置信 = 首次 grade < threshold（从 graph state 的 grades/retries 提取；
  CRAG-off 配置无此概念，记 —）
- crag_off 基线 = 同一 HybridRetriever top_k=5 → answer_with_citations 直接生成
  （无打分/改写/兜底；生成 prompt 为 Run C 收紧版，即当前系统）
- crag_on = build_crag_graph(retriever, llm, threshold=T, max_rewrite=M, route=False)
  （T9 路由不进本评测，其量化评测按计划推迟到 S4）

结构（TDD-lite）：纯函数（doc_id 提取/命中判定/三分类/配对转移/汇总）可单测
（tests/test_run_crag_eval_script.py）；LLM/Milvus 重依赖全部懒加载在函数内。
结果增量落 JSON store（data/llm_cache/crag_eval/raw.json，gitignored），调参轮次
按配置名追加，报告可从 store 全量重建（--report-only）。

用法：
    uv run python scripts/run_crag_eval.py --configs off,on            # 基线对
    uv run python scripts/run_crag_eval.py --configs on_t1 --threshold 5.0
    uv run python scripts/run_crag_eval.py --report-only --report PATH \
        --title ... --disposition-file ...
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

STORE_DEFAULT = "data/llm_cache/crag_eval/raw.json"
QTYPES = ("factual", "troubleshoot", "multihop", "reject")


class BudgetExhausted(RuntimeError):
    """SiliconFlow 402（余额不足）：即刻停止批次，如实记录覆盖。"""


# ---------------------------------------------------------------------------
# 纯函数（单测覆盖）
# ---------------------------------------------------------------------------

_CIT_DOC_RE = re.compile(r"（([^（）]+)）\s*$")


def doc_ids_from_citations(citations: list[str]) -> list[str]:
    """answer_with_citations 的引用格式 '[i] breadcrumb（doc_id）' → doc_id 列表。

    无尾全角括号/空串/None → ""（占位，不参与命中判定）。"""
    out = []
    for c in citations or []:
        m = _CIT_DOC_RE.search((c or "").strip())
        out.append(m.group(1) if m else "")
    return out


def citation_hit(citations: list[str], expected_doc_ids: list[str]) -> bool:
    """任一 citation 的 doc_id ∈ expected_doc_ids。"""
    return any(d in (expected_doc_ids or []) for d in doc_ids_from_citations(citations) if d)


def classify_outcome(handoff: bool, hit: bool) -> str:
    """逐题三分类：handoff=True → handoff；否则命中引用 → solved，未命中 → missed。"""
    if handoff:
        return "handoff"
    return "solved" if hit else "missed"


def first_grade_low(grades: list[float], threshold: float) -> bool:
    """初次低置信：首次 grade < threshold（grade == threshold 算高分，与图一致）。"""
    return bool(grades) and grades[0] < threshold


def paired_transitions(off: dict[str, str], on: dict[str, str]) -> dict[str, list[str]]:
    """同一题在 off/on 两配置间的结果转移（qid 有序列表）。

    rescued=off 未解决→on 解决（救回）；lost=off 解决→on 未解决（损失）；
    error 与 missed/handoff 同视为"未解决"。"""
    rescued = sorted(q for q in off if off[q] != "solved" and on.get(q, "missing") == "solved")
    lost = sorted(q for q in off if off[q] == "solved" and on.get(q, "missing") != "solved")
    stable_solved = sorted(q for q in off if off[q] == "solved" and on.get(q) == "solved")
    both_fail = sorted(q for q in off
                       if off[q] != "solved" and on.get(q, "missing") != "solved")
    return {"rescued": rescued, "lost": lost,
            "stable_solved": stable_solved, "both_fail": both_fail}


def summarize(records: list[dict]) -> dict:
    """单配置汇总：三分类计数与率 + CRAG-only 计数（初次低置信/改写触发）。"""
    n = len(records)
    solved = sum(1 for r in records if r["outcome"] == "solved")
    handoff = sum(1 for r in records if r["outcome"] == "handoff")
    missed = sum(1 for r in records if r["outcome"] == "missed")
    error = sum(1 for r in records if r["outcome"] == "error")
    low = sum(1 for r in records if r.get("low_first"))
    rewritten = sum(1 for r in records if r.get("rewritten"))
    calls = sum(r.get("calls") or 0 for r in records)
    d = max(1, n)
    return {"n": n, "solved": solved, "handoff": handoff, "missed": missed,
            "error": error, "low_first": low, "rewritten": rewritten,
            "llm_calls": calls,
            "solve_rate": solved / d, "handoff_rate": handoff / d,
            "missed_rate": missed / d, "error_rate": error / d,
            "low_first_rate": low / d, "rewrite_rate": rewritten / d}


# ---------------------------------------------------------------------------
# 运行器（LLM/Milvus 懒加载；逐题异常捕获，402 即停）
# ---------------------------------------------------------------------------

def _err(e: Exception) -> str:
    return f"{type(e).__name__}: {e}"


def run_off(retriever, llm, items, top_k: int) -> list[dict]:
    """crag_off 基线：检索 top_k → answer_with_citations 直接生成。"""
    from netrag.generation.answer import answer_with_citations

    records: list[dict] = []
    try:
        for i, it in enumerate(items, 1):
            rec: dict = {"qid": it.qid, "question": it.question}
            try:
                chunks = retriever.retrieve(it.question, top_k=top_k)
                res = answer_with_citations(it.question, chunks, llm)
                hit = citation_hit(res.citations, it.expected_doc_ids)
                rec.update(handoff=False, answer=res.text, citations=res.citations,
                           hit=hit, outcome=classify_outcome(False, hit),
                           calls=1, error="")
            except Exception as e:  # noqa: BLE001 — 单题失败不中断批次（402 除外）
                rec.update(handoff=False, answer="", citations=[], hit=False,
                           outcome="error", calls=0, error=_err(e))
                records.append(rec)
                if "402" in rec["error"]:
                    raise BudgetExhausted(rec["error"])
                print(f"  [off] {it.qid} 异常：{rec['error']}", flush=True)
                continue
            records.append(rec)
            if i % 5 == 0 or i == len(items):
                print(f"  [off] {i}/{len(items)} 完成", flush=True)
    except BudgetExhausted:
        raise
    return records


def run_on(retriever, llm, items, threshold: float, max_rewrite: int,
           top_k: int, label: str) -> list[dict]:
    """crag_on：build_crag_graph（route=False），fresh thread_id/题，逐题捕异常。"""
    from netrag.agent.crag import build_crag_graph

    graph = build_crag_graph(retriever, llm, threshold=threshold,
                             max_rewrite=max_rewrite, top_k=top_k, route=False)
    records: list[dict] = []
    for i, it in enumerate(items, 1):
        rec = {"qid": it.qid, "question": it.question}
        try:
            tid = f"crag-eval-{label}-{i:03d}-{uuid.uuid4().hex[:6]}"
            final = graph.invoke({"question": it.question},
                                 config={"configurable": {"thread_id": tid}})
            meta = final.get("trace_meta") or {}
            grades = list(meta.get("grades") or [])
            rewrites = [r.get("to", "") for r in meta.get("rewrites", [])]
            handoff = bool(final.get("handoff"))
            cits = list(final.get("citations") or [])
            hit = citation_hit(cits, it.expected_doc_ids)
            outcome = classify_outcome(handoff, hit)
            rec.update(handoff=handoff, answer=final.get("answer", ""),
                       citations=cits, hit=hit, outcome=outcome,
                       grades=grades, retries=final.get("retries", 0),
                       low_first=first_grade_low(grades, threshold),
                       rewritten=bool(rewrites), rewrites=rewrites,
                       calls=len(grades) + len(rewrites)
                       + (1 if outcome in ("solved", "missed") else 0),
                       error="")
        except Exception as e:  # noqa: BLE001 — 单题失败不中断批次（402 除外）
            rec.update(handoff=False, answer="", citations=[], hit=False,
                       outcome="error", grades=[], retries=0, low_first=False,
                       rewritten=False, rewrites=[], calls=0, error=_err(e))
            records.append(rec)
            if "402" in rec["error"]:
                raise BudgetExhausted(rec["error"])
            print(f"  [{label}] {it.qid} 异常：{rec['error']}", flush=True)
            continue
        records.append(rec)
        if i % 5 == 0 or i == len(items):
            print(f"  [{label}] {i}/{len(items)} 完成 "
                  f"(solved={sum(1 for r in records if r['outcome'] == 'solved')})",
                  flush=True)
    return records


# ---------------------------------------------------------------------------
# store（JSON 增量）与报告
# ---------------------------------------------------------------------------

def load_store(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text())
    return {"configs": {}}


def save_store(path: Path, store: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(store, ensure_ascii=False, indent=1))


def records_map(records: list[dict]) -> dict[str, str]:
    return {r["qid"]: r["outcome"] for r in records}


def _pct(x: float) -> str:
    return f"{x * 100:.1f}%"


def build_report(store: dict, title: str, disposition: str,
                 stop_note: str = "") -> tuple[dict, str]:
    """从 store 重建汇总表与报告正文（调参轮次按 configs 插入顺序即轮次序）。"""
    cfgs = store["configs"]
    off = cfgs.get("off")
    on_name = next((k for k in cfgs if k.startswith("on")), None)

    rows: dict[str, str] = {}
    body = ["## 口径", ""]
    body += [
        "- 子集：data/golden/s3_full.yaml 中 qtype=troubleshoot 的 "
        f"{summarize(off['records'])['n'] if off else 40} 条（现象→排查题，作"
        "\"模糊类\"代理）。原始方案的计数口径为 200 条其中模糊类 80 条，本 golden "
        "实际为 200 条其中 troubleshoot 40 条——**40≠80 是已知口径差异，数字按 "
        "40 条原样报告，不为对齐叙事而调整子集或阈值**。",
        "- 指标定义（逐题）：",
        "  - **自动解决**（一条题在某配置下）= final answer 非 fallback 文本"
        "（handoff=False）**且** citations 命中期望文档（任一 citation 的 doc_id ∈ "
        "expected_doc_ids）",
        "  - **转人工** = handoff=True",
        "  - **初次低置信** = 首次 grade < threshold（从 graph state 的 "
        "grades/retries 字段提取；CRAG-off 配置无此概念，记 —）",
        "  - **改写触发** = 该题 CRAG 图发生过 rewrite（trace_meta.rewrites 非空；"
        "CRAG-off 记 —）",
        "- 配置：**crag_off** = 同一 HybridRetriever top_k=5 检索后直接 "
        "answer_with_citations（无打分/改写/兜底；生成 prompt 为 Run C 收紧版，"
        "即被测系统现状）；**crag_on** = build_crag_graph(retriever, llm, "
        "threshold=T, max_rewrite=M, route=False)（**T9 路由不进本评测**——路由的"
        "量化评测按计划推迟到 S4，本任务只测 CRAG 核心回路 打分→改写→兜底）。",
        "- 检索：HybridRetriever(client, embedder, reranker=BgeReranker) top_k=5；"
        "golden troubleshoot 子集无 filters，两配置检索输入严格一致。",
        "- 逐题异常捕获记 error 不中断批次；SiliconFlow 402（余额不足）即刻停止并"
        "如实记录覆盖。评测为单次运行（MEASURE），未对子集做任何题目增删。",
        "",
    ]
    body += ["## 主结果", "",
             "| 配置 | threshold | max_rewrite | n | 自动解决 | 转人工 | 有答案未命中 | error | 初次低置信 | 改写触发 | LLM调用 |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for name, entry in cfgs.items():
        s = summarize(entry["records"])
        p = entry["params"]
        is_off = not name.startswith("on")
        if is_off:  # CRAG-off 无打分/改写概念，记 —
            low_cell = rewrite_cell = "—"
        else:
            low_cell = f"{s['low_first']}（{_pct(s['low_first_rate'])}）"
            rewrite_cell = f"{s['rewritten']}（{_pct(s['rewrite_rate'])}）"
        body.append(
            f"| {name} | {p.get('threshold', '—')} | {p.get('max_rewrite', '—')} "
            f"| {s['n']} | {s['solved']}（{_pct(s['solve_rate'])}） "
            f"| {s['handoff']}（{_pct(s['handoff_rate'])}） "
            f"| {s['missed']}（{_pct(s['missed_rate'])}） | {s['error']} "
            f"| {low_cell} | {rewrite_cell} | {s['llm_calls']} |")
        if name == "off":
            rows["crag_off 自动解决率"] = f"{_pct(s['solve_rate'])}（{s['solved']}/{s['n']}）"
            rows["crag_off 转人工"] = "0（无 handoff 机制，恒生成）"
        elif name == on_name:
            rows["crag_on(基线) 自动解决率"] = f"{_pct(s['solve_rate'])}（{s['solved']}/{s['n']}）"
            rows["crag_on(基线) 转人工率"] = f"{_pct(s['handoff_rate'])}（{s['handoff']}/{s['n']}）"
            rows["crag_on(基线) 初次低置信"] = f"{s['low_first']}/{s['n']}"
            rows["crag_on(基线) 改写触发"] = f"{s['rewritten']}/{s['n']}"
    body.append("")

    # 配对视角：off vs 每个 on 配置
    if off:
        off_map = records_map(off["records"])
        body += ["## 配对视角（同一题 off → on 的结果转移）", "",
                 "| 对比 | 保持解决 | 救回（off未解决→on解决） | 损失（off解决→on未解决） | 双败 |",
                 "|---|---|---|---|---|"]
        for name, entry in cfgs.items():
            if not name.startswith("on"):
                continue
            v = paired_transitions(off_map, records_map(entry["records"]))
            body.append(f"| off → {name} | {len(v['stable_solved'])} "
                        f"| {len(v['rescued'])} | {len(v['lost'])} "
                        f"| {len(v['both_fail'])} |")
            if name == on_name:
                rows[f"救回（off未解决→{name}解决）"] = str(len(v["rescued"]))
                rows[f"损失（off解决→{name}未解决）"] = str(len(v["lost"]))
        body.append("")
        for name, entry in cfgs.items():
            if not name.startswith("on"):
                continue
            v = paired_transitions(off_map, records_map(entry["records"]))
            body.append(f"### off → {name}")
            body.append("")
            for key, label in (("rescued", "救回"), ("lost", "损失"),
                               ("stable_solved", "保持解决"), ("both_fail", "双败")):
                qs = v[key]
                body.append(f"- **{label}（{len(qs)}）**：" +
                            ("；".join(f"`{q}`" for q in qs) if qs else "无"))
            body.append("")

    # 调参轮次：on_ 前缀且非基线的配置按插入序=轮次序
    tuned = [(k, e) for k, e in cfgs.items() if k.startswith("on") and k != on_name]
    if tuned:
        base = summarize(cfgs[on_name]["records"])["solve_rate"]
        body += ["## 调参轮次（spec §8：≤3 轮、每轮一个杠杆、无改善即停）", "",
                 "| 轮 | 配置 | 杠杆 | 自动解决率 | Δ vs 基线 on | 结论 |", "|---|---|---|---|---|---|"]
        for i, (name, entry) in enumerate(tuned, 1):
            s = summarize(entry["records"])
            delta = s["solve_rate"] - base
            p = entry["params"]
            lever = f"threshold={p.get('threshold')}, max_rewrite={p.get('max_rewrite')}"
            concl = "有效（提升）" if delta > 0 else "无改善"
            body.append(f"| {i} | {name} | {lever} | {_pct(s['solve_rate'])}（{s['solved']}/{s['n']}） "
                        f"| {delta:+.3f} | {concl} |")
        body.append("")
        if stop_note:
            body += [stop_note, ""]
    body += ["## 对齐③", "", disposition or "（待补充）", ""]
    rows["LLM 调用合计（估算）"] = str(
        sum(summarize(e["records"])["llm_calls"] for e in cfgs.values()))
    return rows, "\n".join(body)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--golden", default="data/golden/s3_full.yaml")
    ap.add_argument("--configs", default="off,on",
                    help="本次要运行的配置名（逗号分隔）：off=基线直答；"
                         "其余名字走 CRAG-on 路径，参数取 --threshold/--max-rewrite")
    ap.add_argument("--threshold", type=float, default=6.0)
    ap.add_argument("--max-rewrite", type=int, default=1)
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--limit", type=int, default=0, help="只跑前 N 条（冒烟用；0=全量 40 条）")
    ap.add_argument("--store", default=STORE_DEFAULT)
    ap.add_argument("--force", action="store_true", help="同名配置强制重跑（默认跳过）")
    ap.add_argument("--report", default=None, help="报告输出路径（写报告并退出）")
    ap.add_argument("--report-only", action="store_true", help="不跑评测，仅从 store 写报告")
    ap.add_argument("--title", default="CRAG 评测（对齐③）：troubleshoot 子集开/关对比")
    ap.add_argument("--disposition-file", default=None,
                    help="对齐③ 处置文本（markdown 片段）文件路径")
    ap.add_argument("--stop-note", default="",
                    help="调参轮次表后的停止说明（为何不再继续轮次）")
    return ap.parse_args(argv)


def main(argv=None) -> None:
    args = parse_args(argv)
    store_path = Path(args.store)
    store = load_store(store_path)

    if not args.report_only:
        from netrag.config import Settings
        from netrag.embedding.bge_m3 import BGEM3Embedder
        from netrag.embedding.reranker import BgeReranker
        from netrag.eval.golden import load_golden
        from netrag.generation.llm import LLMClient
        from netrag.index.milvus_client import get_milvus, wait_healthy
        from netrag.retrieval.hybrid import HybridRetriever

        all_items = load_golden(Path(args.golden))
        items = [it for it in all_items if it.qtype == "troubleshoot"]
        if args.limit:
            items = items[:args.limit]
        print(f"golden {len(all_items)} 条 → troubleshoot 子集 {len(items)} 条", flush=True)

        settings = Settings.from_env()
        client = get_milvus()
        wait_healthy(client)
        embedder = BGEM3Embedder(settings.embed_model)
        retriever = HybridRetriever(client, embedder, BgeReranker(settings.rerank_model))
        llm = LLMClient()

        for name in [c.strip() for c in args.configs.split(",") if c.strip()]:
            if name in store["configs"] and not args.force:
                print(f"== {name} 已在 store，跳过（--force 重跑） ==", flush=True)
                continue
            print(f"== {name}（threshold={args.threshold}, "
                  f"max_rewrite={args.max_rewrite}） ==", flush=True)
            if name == "off":
                records = run_off(retriever, llm, items, args.top_k)
                params = {"mode": "off", "top_k": args.top_k}
            else:
                records = run_on(retriever, llm, items, args.threshold,
                                 args.max_rewrite, args.top_k, name)
                params = {"mode": "on", "threshold": args.threshold,
                          "max_rewrite": args.max_rewrite, "top_k": args.top_k}
            store["configs"][name] = {"params": params, "records": records,
                                      "golden": args.golden}
            save_store(store_path, store)
            s = summarize(records)
            print(f"== {name} 汇总：solve={s['solved']}/{s['n']}"
                  f"（{_pct(s['solve_rate'])}）handoff={s['handoff']}"
                  f" low_first={s['low_first']} rewritten={s['rewritten']}",
                  flush=True)

    if args.report:
        disposition = ""
        if args.disposition_file and Path(args.disposition_file).exists():
            disposition = Path(args.disposition_file).read_text().strip()
        rows, body = build_report(store, args.title, disposition,
                                  stop_note=args.stop_note)
        from netrag.eval.report import write_report

        write_report(Path(args.report), title=args.title,
                     summary_rows=rows, body_md=body)


if __name__ == "__main__":
    main()
