"""T14 端到端排障评测运行器：重置 → 注入 → CRAG(tools=True) 排障 → LLM 判分 → 重置。

两种模式：
    --validate   零 LLM 基建自检：逐条任务 注入→running 核验→只读工具证据→重置→
                 基线收敛→OSPF 重收敛。用于 30 条故障的逐一可逆性验证（先导基建）。
    默认（agent） 真实排障：reset_lab → inject → build_crag_graph(tools=True) 以任务
                 问题 invoke（fresh thread_id，state["host"] 显式传入）→ 捕获
                 answer/citations/tool_calls → judge（同 Qwen，temp 0）输出
                 {conclusion_correct, tools_reasonable} → reset_lab 收敛。

用法：
    uv run python scripts/run_e2e.py --validate                       # 30 条全验
    uv run python scripts/run_e2e.py --ids t02,t17,t30                # 3 条先导
    uv run python scripts/run_e2e.py --ids t02 --no-judge             # 只跑图不判分

纪律：
  - LLM 预算：先导 3 条 ≈ 9-12 次（每条 grade+generate[+rewrite] + judge 1 次）；
    SiliconFlow 402 → BudgetExhausted 即刻停批，如实记录覆盖。
  - 注入/重置全程不 write memory（faults.py 契约）：bind-mount 基线与 git 不被触碰。
  - 逐条结果增量落 JSON（data/llm_cache/t14_results/，gitignored），可断点续读。

结构（TDD-lite）：纯函数（装载/判分解析/提示词/计数/记录）单测
tests/test_run_e2e_script.py；LLM/Milvus/netmiko 全部懒加载在函数内。
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, os.path.dirname(__file__))

RESULTS_DIR = "data/llm_cache/t14_results"

JUDGE_SYSTEM = (
    "你是网络排障评测的判分器。给定【期望结论】、【Agent 答案】与【工具调用序列】，"
    '只输出一个 JSON 对象：{"conclusion_correct": <bool>, "tools_reasonable": <bool>, '
    '"reason": "<一句话依据>"}，不要任何其他文字。\n'
    "判定标准：\n"
    "- conclusion_correct：Agent 答案是否明确指出了期望结论中的关键事实"
    "（具体接口号/地址/取值）；仅泛泛说『配置有问题』而未点中关键事实算 false；\n"
    "- tools_reasonable：实际调用的只读工具是否足以获得该结论（对照合理工具参考），"
    "调用了完全无关工具或明显不足的工具算 false。\n"
    "校准约定（人工决策 ③，修复轮 1 扩展）：\n"
    "- 当【合理工具参考】恰好只有 1 个工具、且实际调用序列恰好只调用了该工具时，"
    "tools_reasonable 恒为 true（由运行器直接判定，你无需裁量）；此时请只专注 "
    "conclusion_correct 的判定；\n"
    "- 当【合理工具参考】多于 1 个工具时，tools_reasonable 判据为：调用了至少一个"
    "预期工具且无越权工具即算 true（越权=与获取该结论完全无关的工具）；一个预期"
    "工具都没调用才判 false；调用了个别预期之外但与本次排障直接相关的只读工具"
    "不算越权。\n"
)


class TaskListError(RuntimeError):
    """任务清单/ID 非法。"""


class BudgetExhausted(RuntimeError):
    """SiliconFlow 402（余额不足）：即刻停止批次，如实记录覆盖。"""


# ---------------------------------------------------------------------------
# 纯函数（单测覆盖）
# ---------------------------------------------------------------------------

def load_tasks(path: Path | str, ids: list[str] | None) -> list[dict]:
    """装载任务 YAML；ids 非空时按序筛选，未知 ID 报错。"""
    import yaml

    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    tasks = raw.get("tasks") or []
    if not tasks:
        raise TaskListError(f"no tasks in {path}")
    if not ids:
        return tasks
    by_id = {t["task_id"]: t for t in tasks}
    missing = [i for i in ids if i not in by_id]
    if missing:
        raise TaskListError(f"unknown task ids: {missing}; 清单含 {sorted(by_id)}")
    return [by_id[i] for i in ids]


def _to_bool(v) -> bool:
    if isinstance(v, bool):
        return v
    return str(v).strip().lower() in ("true", "yes", "1", "是", "正确")


class CountingLLM:
    """LLMClient 薄代理：精确计数 chat 调用（先计数后委托——异常/402 的已消耗次数
    也如实入账）。替代按 trace_meta 估算：图异常中途退出时估算不可得，计数器可得。
    **单题计量**：run_agent 每条任务开始时 :meth:`reset`，记录存单题消耗而非批内累计
    （否则 summarize 求和超线性虚报、首条之后所有 item 的单题归因全错）。"""

    def __init__(self, inner):
        self._inner = inner
        self.calls = 0

    def reset(self) -> None:
        """单题边界：新 item 开始前清零。"""
        self.calls = 0

    def chat(self, messages, temperature: float = 0.2, max_tokens: int = 2048) -> str:
        self.calls += 1
        return self._inner.chat(messages, temperature=temperature,
                                max_tokens=max_tokens)


def judge_parse(text: str) -> dict:
    """judge 输出 → 判分 dict；解析失败保守给 (False, False)。"""
    for m in re.finditer(r"\{[^{}]*\}", text or "", re.S):
        try:
            obj = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        if "conclusion_correct" in obj and "tools_reasonable" in obj:
            return {"conclusion_correct": _to_bool(obj["conclusion_correct"]),
                    "tools_reasonable": _to_bool(obj["tools_reasonable"]),
                    "reason": str(obj.get("reason", ""))}
    return {"conclusion_correct": False, "tools_reasonable": False,
            "reason": "judge 输出不可解析"}


def tools_match_single_expected(expected_tools: list[str], tool_calls: list[dict]) -> bool:
    """判分校准（人工决策 ③）：期望工具恰 1 个且 Agent 恰只调用了该工具 → True。

    先导实测：唯一正确工具调用仍被判 tools_reasonable=False（判分器裁量在该
    场景只有噪声）。该场景无需裁量——运行器直接判 true，判分器只裁
    conclusion_correct；期望工具多于 1 个时仍归判分器裁量。
    """
    return (len(expected_tools) == 1
            and [c.get("tool") for c in (tool_calls or [])] == [expected_tools[0]])


def calibrated_tools_reasonable(expected_tools: list[str],
                                tool_calls: list[dict]) -> tuple[bool, str] | None:
    """判分校准（修复轮 1，t02 根因②）：可确定性判定时返回 (值, 审计标签)，否则 None。

    - len(expected_tools)==1：恰只调用了该工具 → (True, 单工具自动判定)（先导批准，
      与 tools_match_single_expected 同一规则）；其余 → None（判分器裁量）；
    - len(expected_tools)>1（判据「调用了至少一个预期工具且无越权工具」）：
      调用全部 ⊆ 预期（至少一个）→ (True, 多预期工具校准)；零调用 →
      (False, 多预期工具校准)；调用含预期外工具（是否越权需语境判断）或期望为空
      → None（判分器按 JUDGE_SYSTEM 校准判据裁量）。
    """
    called = [c.get("tool") for c in (tool_calls or [])]
    if len(expected_tools) == 1:
        return ((True, "单工具自动判定")
                if tools_match_single_expected(expected_tools, tool_calls) else None)
    if not expected_tools or not called:
        return None if not expected_tools else (False, "多预期工具校准")
    if set(called) <= set(expected_tools):
        return True, "多预期工具校准"
    return None


def judge_messages(expected_conclusion: str, answer: str, tool_calls: list[dict],
                   expected_tools: list[str]) -> list[dict]:
    """判分提示词：期望结论 + 答案 + 工具序列（输出截断防爆 token）。"""
    seq = "\n".join(
        f"{i + 1}. {c.get('tool')} args={c.get('args')} "
        f"output={(c.get('output') or '')[:400]!r}"
        for i, c in enumerate(tool_calls or [])) or "（无工具调用）"
    user = (f"【期望结论】{expected_conclusion}\n\n"
            f"【合理工具参考】{expected_tools}\n\n"
            f"【工具调用序列】\n{seq}\n\n"
            f"【Agent 答案】\n{answer or '（空）'}")
    return [{"role": "system", "content": JUDGE_SYSTEM},
            {"role": "user", "content": user}]


def verdict_record(task: dict, *, answer: str, citations: list[str],
                   tool_calls: list[dict], trace_meta: dict | None, handoff: bool,
                   verdict: dict, inject: dict | None, reset_report: dict | None,
                   wall_seconds: float, llm_calls: int, thread_id: str = "") -> dict:
    """单条任务结果记录（落盘/报告统一形）。"""
    meta = trace_meta or {}
    return {
        "task_id": task["task_id"],
        "fault": task["fault"],
        "difficulty": task.get("difficulty"),
        "question": task["question"],
        "expected_conclusion": task["expected_conclusion"],
        "expected_tools": task.get("expected_tools"),
        "answer": answer,
        "citations": citations,
        "tool_calls": tool_calls,
        "grades": list(meta.get("grades") or []),
        "rewrites": [r.get("to", "") for r in (meta.get("rewrites") or [])],
        "handoff": bool(handoff),
        "verdict": verdict,
        "inject": inject,
        "reset_report": reset_report,
        "wall_seconds": round(wall_seconds, 1),
        "llm_calls": llm_calls,
        "thread_id": thread_id,
        "ts": _dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),
    }


def _err(e: Exception) -> str:
    return f"{type(e).__name__}: {e}"


def _print_verbatim(rec: dict) -> None:
    """先导要求：逐字打印答案与工具输出。"""
    print(f"\n--- {rec['task_id']} verdict={rec['verdict']} "
          f"calls={rec['llm_calls']} wall={rec['wall_seconds']}s ---")
    print(f"[Q] {rec['question']}")
    for c in rec["tool_calls"]:
        print(f"[TOOL] {c['tool']} {c['args']}")
        print((c.get("output") or "")[:1200])
    print(f"[ANSWER]\n{rec['answer']}")
    for c in rec.get("citations") or []:
        print(f"  {c}")
    print(f"[EXPECT] {rec['expected_conclusion']}")


# ---------------------------------------------------------------------------
# validate 模式（零 LLM）
# ---------------------------------------------------------------------------

def run_validate(tasks: list[dict]) -> bool:
    from netrag.tools_mcp.device import DeviceConnection
    from netrag.tools_mcp.faults import FaultLab
    from netrag.tools_mcp.server import SHOW_COMMANDS

    lab = FaultLab(DeviceConnection())
    ok_all = True
    for t in tasks:
        tid, f = t["task_id"], t["fault"]
        try:
            t0 = time.monotonic()
            lab.reset()
            if not lab.wait_healthy():
                print(f"{tid} FAIL: 起跑前 OSPF 未收敛")
                ok_all = False
                continue
            inj = lab.inject(f["host"], f["kind"], f["param"])
            # 只读工具证据：首个 expected_tool 对应的 show（与 Agent 同一观测面）
            tool = (t.get("expected_tools") or ["show_ip_interface_brief"])[0]
            cmd = SHOW_COMMANDS.get(tool, ["show running-config" if tool == "get_running_config"
                                           else "show interface brief"])[0]
            evidence = ""
            try:
                evidence = lab.device.show_with_fallback(f["host"], [cmd])
            except Exception as e:  # noqa: BLE001
                evidence = f"<show failed: {_err(e)}>"
            rep = lab.reset([f["host"]])
            added, removed = lab.diff_from_baseline(f["host"])
            clean = not added and not removed
            healthy = lab.wait_healthy()
            ok = inj["verified"] and clean and healthy and rep[f["host"]]["changed"]
            ok_all &= ok
            print(f"{tid} {'PASS' if ok else 'FAIL'} ({time.monotonic() - t0:.0f}s) "
                  f"inject_verified={inj['verified']} reset_changed={rep[f['host']]['changed']} "
                  f"clean={clean} healthy={healthy} detail={inj['verify_detail']}")
            print(f"     evidence[{tool} → {cmd}]: {evidence.strip().splitlines()[0] if evidence.strip() else '∅'}"
                  f" | reset_cmds={len(rep[f['host']]['commands'])}")
        except Exception as e:  # noqa: BLE001 — 单条基建异常不中断 30 条自检
            ok_all = False
            print(f"{tid} FAIL: {_err(e)}")
            try:
                lab.reset()
                lab.wait_healthy()
            except Exception as e2:  # noqa: BLE001
                print(f"{tid} FAIL: 异常后清场重置也失败 {_err(e2)}（故障可能残留）")
            continue
    return ok_all


# ---------------------------------------------------------------------------
# agent 模式（真实排障 + 判分）
# ---------------------------------------------------------------------------

def build_graph(threshold: float):
    """检索器/LLM/图懒构建（Milvus+GPU embedder 只加载一次）；LLM 经 CountingLLM 包装。"""
    from netrag.agent.crag import build_crag_graph
    from netrag.config import Settings
    from netrag.embedding.bge_m3 import BGEM3Embedder
    from netrag.embedding.reranker import BgeReranker
    from netrag.generation.llm import LLMClient
    from netrag.index.milvus_client import get_milvus, wait_healthy
    from netrag.retrieval.hybrid import HybridRetriever

    settings = Settings.from_env()
    client = get_milvus()
    wait_healthy(client)
    embedder = BGEM3Embedder(settings.embed_model)
    retriever = HybridRetriever(client, embedder, BgeReranker(settings.rerank_model),
                                recall_n=48)
    llm = CountingLLM(LLMClient())
    graph = build_crag_graph(retriever, llm, settings=settings, threshold=threshold,
                             tools=True)
    return graph, llm


def _reset_and_check(lab, host: str) -> dict:
    """重置 + 基线收敛核验（不抛：任何异常收敛为 error 字段，含各节点已下发命令）。

    返回 {changed, clean, commands, error}；error 非空时由调用方决定重试/记录。
    """
    try:
        rep = lab.reset()
        added, removed = lab.diff_from_baseline(host)
        healthy = lab.wait_healthy()
        return {"changed": {h: r["changed"] for h, r in rep.items()},
                "clean": bool(not added and not removed and healthy),
                "commands": {h: r["commands"] for h, r in rep.items()},
                "error": ""}
    except Exception as e:  # noqa: BLE001 — 瞬时 netmiko 失败不得中断整批
        return {"changed": {}, "clean": False, "commands": {}, "error": _err(e)}


def _safe_drift(lab, host: str) -> dict:
    """尽力记录当前相对基线的漂移（reset 失败后的人工核对线索；失败不抛）。"""
    try:
        added, removed = lab.diff_from_baseline(host)
        return {"added": [[c, l] for c, l in added], "removed": [[c, l] for c, l in removed]}
    except Exception as e:  # noqa: BLE001
        return {"error": _err(e)}


def run_agent(tasks: list[dict], threshold: float, judge: bool, out_path: Path,
              lab=None, graph_pair=None) -> list[dict]:
    """逐任务：重置→注入→CRAG 排障→判分→重置。lab/graph_pair 可注入（单测 spy）。

    容错契约：任一步骤（预重置/注入/图/判分/收尾重置）异常都收敛为该 item 的
    error 记录并继续批，绝不中断整批；llm_calls 用 CountingLLM 精确入账（含异常路径）。
    """
    from netrag.tools_mcp.device import DeviceConnection
    from netrag.tools_mcp.faults import FaultLab

    if lab is None:
        lab = FaultLab(DeviceConnection())
    graph, llm = graph_pair if graph_pair is not None else build_graph(threshold)
    records: list[dict] = []
    out_path.parent.mkdir(parents=True, exist_ok=True)

    for t in tasks:
        tid, f = t["task_id"], t["fault"]
        llm.reset()  # 单题计量：记录存该题真实消耗（含后续异常路径），非批内累计
        print(f"\n===== {tid} [{t['difficulty']}] {f['host']} {f['kind']} {f['param']} =====",
              flush=True)
        t0 = time.monotonic()
        # 1) 干净起点（预重置异常 → 记录该 item 失败，批继续）
        try:
            lab.reset()
        except Exception as e:  # noqa: BLE001
            err = f"pre-reset: {_err(e)}"
            print(f"{tid} FAIL: {err}", flush=True)
            records.append({"task_id": tid, "error": err, "llm_calls": llm.calls})
            _append(out_path, records[-1])
            continue
        if not lab.wait_healthy():
            print(f"{tid} FAIL: 起跑前 OSPF 未收敛，跳过", flush=True)
            records.append({"task_id": tid, "error": "lab not healthy before inject",
                            "llm_calls": llm.calls})
            _append(out_path, records[-1])
            continue
        # 2) 注入
        try:
            inj = lab.inject(f["host"], f["kind"], f["param"])
        except Exception as e:  # noqa: BLE001
            print(f"{tid} FAIL: 注入异常 {_err(e)}", flush=True)
            try:
                lab.reset()
            except Exception as e2:  # noqa: BLE001 — 清场失败也只记录，不中断
                print(f"{tid} WARN: 注入后清场重置异常 {_err(e2)}", flush=True)
            records.append({"task_id": tid, "error": f"inject: {_err(e)}",
                            "llm_calls": llm.calls})
            _append(out_path, records[-1])
            continue
        if not inj["verified"]:
            print(f"{tid} WARN: 注入未核验到（{inj['verify_detail']}），仍继续排障", flush=True)
        time.sleep(2)  # 状态稳定（接口 down → OSPF 邻立即摘除，无需等 dead timer）
        # 3) Agent 排障（fresh thread；host 显式传入优先于问题内提取）
        thread_id = f"e2e-{tid}-{uuid.uuid4().hex[:6]}"
        try:
            final = graph.invoke({"question": t["question"], "host": f["host"]},
                                 config={"configurable": {"thread_id": thread_id}})
        except Exception as e:  # noqa: BLE001
            err = _err(e)
            print(f"{tid} 图执行异常：{err}", flush=True)
            try:
                lab.reset()
            except Exception as e2:  # noqa: BLE001
                print(f"{tid} WARN: 异常后清场重置失败 {_err(e2)}（故障可能残留）", flush=True)
            rec = {"task_id": tid, "error": err, "llm_calls": llm.calls}
            records.append(rec)
            _append(out_path, rec)
            if "402" in err:
                raise BudgetExhausted(err) from e
            continue
        meta = final.get("trace_meta") or {}
        tool_calls = list(final.get("tool_calls") or [])
        answer, citations = final.get("answer", ""), list(final.get("citations") or [])
        handoff = bool(final.get("handoff"))
        # 4) 判分（CountingLLM 已把 judge 调用计入 llm.calls）
        verdict = {"conclusion_correct": None, "tools_reasonable": None,
                   "reason": "judge disabled"}
        if judge:
            # 校准（人工决策 ③ + 修复轮 1）：可确定性判定的 tools_reasonable 由运行器
            # 直判（单工具精确命中 / 多预期子集 → true；多预期零调用 → false），
            # 判分器只裁 conclusion_correct 与裁量场景（覆盖在解析后、落盘前，可审计）
            calibration = calibrated_tools_reasonable(t.get("expected_tools") or [],
                                                      tool_calls)
            try:
                out = llm.chat(judge_messages(t["expected_conclusion"], answer,
                                              tool_calls, t.get("expected_tools") or []),
                               temperature=0.0, max_tokens=256)
                verdict = judge_parse(out)
                if calibration is not None and verdict["conclusion_correct"] is not None:
                    value, label = calibration
                    verdict = {**verdict, "tools_reasonable": value,
                               "reason": f"[{label}] {verdict.get('reason', '')}"}
            except Exception as e:  # noqa: BLE001
                err = _err(e)
                print(f"{tid} judge 异常：{err}", flush=True)
                verdict = {"conclusion_correct": None, "tools_reasonable": None,
                           "reason": f"judge error: {err}"}
                if "402" in err:
                    reset_info = _reset_and_check(lab, f["host"])
                    if reset_info["error"]:
                        print(f"{tid} WARN: 402 后清场重置失败 {reset_info['error']}"
                              f"（故障可能残留，drift={_safe_drift(lab, f['host'])}）",
                              flush=True)
                    raise BudgetExhausted(err) from e
        # 5) 重置 + 收敛核验（失败重试一次，仍失败则带命令/漂移详情记录，批继续——
        #    故障可能残留，下一条任务的预重置会再尝试收敛）
        reset_info = _reset_and_check(lab, f["host"])
        if reset_info["error"]:
            retry = _reset_and_check(lab, f["host"])
            if not retry["error"] and retry["clean"]:
                reset_info = {**retry, "recovered_after_retry": True}
            else:
                reset_info["drift"] = _safe_drift(lab, f["host"])
                print(f"{tid} WARN: 收尾重置失败 {reset_info['error']}（故障可能残留）",
                      flush=True)
        rec = verdict_record(
            t, answer=answer, citations=citations, tool_calls=tool_calls,
            trace_meta=meta, handoff=handoff, verdict=verdict, inject=inj,
            reset_report=reset_info,
            wall_seconds=time.monotonic() - t0, llm_calls=llm.calls, thread_id=thread_id)
        records.append(rec)
        _append(out_path, rec)
        _print_verbatim(rec)
        print(f"[RESET] clean={reset_info['clean']} error={reset_info['error'] or '∅'} "
              f"changed={reset_info['changed']}", flush=True)
    return records


def _append(out_path: Path, rec: dict) -> None:
    """增量落盘（断点可续读）。"""
    with out_path.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def summarize(records: list[dict]) -> dict:
    agent_recs = [r for r in records if "verdict" in r]
    n = len(agent_recs)
    return {
        "n_records": len(records), "n_agent": n,
        "conclusion_correct": sum(1 for r in agent_recs
                                  if r["verdict"].get("conclusion_correct") is True),
        "tools_reasonable": sum(1 for r in agent_recs
                                if r["verdict"].get("tools_reasonable") is True),
        "handoff": sum(1 for r in agent_recs if r["handoff"]),
        "llm_calls": sum(r.get("llm_calls", 0) for r in records if r.get("llm_calls", 0) > 0),
        "errors": [r["task_id"] for r in records if r.get("error")],
        "reset_all_clean": all((r.get("reset_report") or {}).get("clean", True)
                               for r in agent_recs),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--tasks", default="data/tasks/e2e_30.yaml")
    ap.add_argument("--ids", default=None,
                    help="逗号分隔 task_id（缺省=全部任务；先导 3 条可传 t02,t17,t30）")
    ap.add_argument("--validate", action="store_true",
                    help="零 LLM 基建自检：注入→核验→证据→重置→收敛")
    ap.add_argument("--dry-run", action="store_true", help="= --validate（别名）")
    ap.add_argument("--threshold", type=float, default=6.0)
    ap.add_argument("--no-judge", action="store_true", help="跳过判分 LLM 调用")
    ap.add_argument("--out", default=None, help="结果 JSONL 路径（缺省 t14_results/）")
    args = ap.parse_args()

    root = Path(__file__).resolve().parents[1]
    ids = [s.strip() for s in args.ids.split(",")] if args.ids else None
    tasks = load_tasks(root / args.tasks, ids)
    print(f"[run_e2e] mode={'validate' if (args.validate or args.dry_run) else 'agent'} "
          f"tasks={len(tasks)} ids={[t['task_id'] for t in tasks]}")

    if args.validate or args.dry_run:
        ok = run_validate(tasks)
        print(f"\n[validate] {'ALL PASS' if ok else 'FAILURES PRESENT'}")
        sys.exit(0 if ok else 1)

    # 收尾轮修复：--ids 缺省=全部任务（原缺省静默只跑先导 3 条，全量评测被截断）
    ts = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    out_path = root / (args.out or f"{RESULTS_DIR}/agent-{ts}.jsonl")
    try:
        records = run_agent(tasks, args.threshold, not args.no_judge, out_path)
    except BudgetExhausted as e:
        print(f"\n[BudgetExhausted] 402 余额不足，停止批次：{e}", flush=True)
        records = []
    summary = summarize(records)
    summary["out"] = str(out_path)
    print("\n[SUMMARY] " + json.dumps(summary, ensure_ascii=False))
    (out_path.parent / f"summary-{out_path.stem}.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
