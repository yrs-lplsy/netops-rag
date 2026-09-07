"""run_e2e.py 纯函数单测：任务装载、判分解析、判分提示词、记录组装（零 IO/LLM）。"""

import pathlib
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import pytest

import run_e2e as R

ROOT = pathlib.Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# 任务装载
# ---------------------------------------------------------------------------

def test_load_tasks_all_and_subset():
    all_tasks = R.load_tasks(ROOT / "data/tasks/e2e_30.yaml", None)
    assert len(all_tasks) == 30
    subset = R.load_tasks(ROOT / "data/tasks/e2e_30.yaml", ["t02", "t17", "t30"])
    assert [t["task_id"] for t in subset] == ["t02", "t17", "t30"]


def test_load_tasks_unknown_id_raises():
    with pytest.raises(R.TaskListError):
        R.load_tasks(ROOT / "data/tasks/e2e_30.yaml", ["t02", "nope"])


# ---------------------------------------------------------------------------
# 判分输出解析（鲁棒：取首个含两键的 JSON 对象）
# ---------------------------------------------------------------------------

def test_judge_parse_clean():
    v = R.judge_parse('{"conclusion_correct": true, "tools_reasonable": false, "reason": "x"}')
    assert v == {"conclusion_correct": True, "tools_reasonable": False, "reason": "x"}


def test_judge_parse_wrapped_in_prose_and_code_fence():
    v = R.judge_parse('前置说明\n```json\n{"conclusion_correct": "true", '
                      '"tools_reasonable": "yes", "reason": "答出了 eth1.100 丢 IP"}\n```')
    assert v["conclusion_correct"] is True
    assert v["tools_reasonable"] is True


def test_judge_parse_garbage_falls_back_conservative():
    v = R.judge_parse("模型只输出了散文，没有 JSON")
    assert v == {"conclusion_correct": False, "tools_reasonable": False,
                 "reason": "judge 输出不可解析"}


# ---------------------------------------------------------------------------
# 判分提示词 / 记录组装
# ---------------------------------------------------------------------------

def test_judge_prompt_contains_all_inputs():
    msgs = R.judge_messages("acc1 eth1.100 丢失 IP 10.100.0.2/24",
                            "经查看配置，acc1 的 eth1.100 上没有 IP 地址……",
                            [{"tool": "get_running_config", "args": {"host": "acc1"},
                              "output": "..."}],
                            expected_tools=["get_running_config"])
    blob = "\n".join(m["content"] for m in msgs)
    assert "10.100.0.2/24" in blob and "eth1.100" in blob
    assert "get_running_config" in blob
    assert msgs[0]["role"] == "system" and msgs[-1]["role"] == "user"


class _CountInner:
    """chat 计数替身：正常返回固定 JSON 判分。"""

    def __init__(self, reply='{"conclusion_correct": true, "tools_reasonable": true}'):
        self.reply = reply

    def chat(self, messages, temperature=0.2, max_tokens=2048):
        return self.reply


def test_counting_llm_counts_calls_even_on_exception():
    c = R.CountingLLM(_CountInner())
    c.chat([{"role": "user", "content": "x"}])
    assert c.calls == 1

    class _Boom:
        def chat(self, *a, **k):
            raise RuntimeError("402 insufficient balance")

    c2 = R.CountingLLM(_Boom())
    with pytest.raises(RuntimeError):
        c2.chat([])
    assert c2.calls == 1  # 异常/402 的已消耗调用同样入账（评审 Minor 2）


# ---------------------------------------------------------------------------
# 批量跑容错（评审 Important：reset 裸调用不得中断整批/丢失记录）
# ---------------------------------------------------------------------------

class _FakeLab:
    """FaultLab 替身：reset 按调用序号可注入失败；其余走 happy path。"""

    HOSTS = ("core1", "core2", "acc1", "acc2")

    def __init__(self, fail_reset_calls=()):
        self.reset_calls = 0
        self.fail_on = set(fail_reset_calls)

    def reset(self, hosts=None):
        self.reset_calls += 1
        if self.reset_calls in self.fail_on:
            raise RuntimeError(f"netmiko boom #{self.reset_calls}")
        return {h: {"changed": False, "commands": [f"cmd-{h}"]} for h in self.HOSTS}

    def wait_healthy(self, timeout=90, expect_full=3, probe_host="core1"):
        return True

    def inject(self, host, kind, param):
        return {"host": host, "kind": kind, "param": dict(param), "commands": ["c1"],
                "verified": True, "verify_detail": "ok"}

    def diff_from_baseline(self, host):
        return ([], [])


class _FakeGraph:
    def invoke(self, state, config):
        return {"answer": f"诊断：{state['host']} 接口异常", "citations": [],
                "tool_calls": [{"tool": "show_ospf_neighbor",
                                "args": {"host": state["host"]}, "output": "..."}],
                "handoff": False, "trace_meta": {"grades": [8.0], "rewrites": []}}


def _task(tid):
    return {"task_id": tid, "difficulty": "easy",
            "fault": {"host": "core1", "kind": "shutdown_interface", "param": {"iface": "eth3"}},
            "question": "q?", "expected_conclusion": "core1 eth3 shutdown",
            "expected_tools": ["show_ospf_neighbor"]}


def test_reset_and_check_returns_error_instead_of_raising():
    lab = _FakeLab(fail_reset_calls={1})
    info = R._reset_and_check(lab, "core1")
    assert info["clean"] is False and "netmiko boom #1" in info["error"]
    assert info["changed"] == {} and info["commands"] == {}


def test_reset_and_check_success_contains_commands():
    info = R._reset_and_check(_FakeLab(), "core1")
    assert info["clean"] is True and info["error"] == ""
    assert info["commands"]["core1"] == ["cmd-core1"]
    assert info["changed"] == {h: False for h in _FakeLab.HOSTS}


def test_run_agent_step1_reset_failure_records_item_and_continues(tmp_path):
    lab = _FakeLab(fail_reset_calls={1})  # 第 1 条任务的预重置炸
    records = R.run_agent([_task("tA"), _task("tB")], 6.0, judge=False,
                          out_path=tmp_path / "out.jsonl",
                          lab=lab, graph_pair=(_FakeGraph(), R.CountingLLM(_CountInner())))
    assert [r["task_id"] for r in records] == ["tA", "tB"]  # 批继续
    assert "pre-reset" in records[0]["error"] and records[0]["llm_calls"] == 0
    assert records[1]["verdict"]["reason"] == "judge disabled"  # 第 2 条正常走完
    assert records[1]["reset_report"]["clean"] is True


def test_run_agent_step5_reset_failure_still_records_verdict(tmp_path):
    lab = _FakeLab(fail_reset_calls={2, 3})  # 收尾重置 + 一次重试都炸
    records = R.run_agent([_task("tA")], 6.0, judge=True,
                          out_path=tmp_path / "out.jsonl",
                          lab=lab, graph_pair=(_FakeGraph(), R.CountingLLM(_CountInner())))
    rec = records[0]
    assert "verdict" in rec and rec["verdict"]["conclusion_correct"] is True
    assert "netmiko boom" in rec["reset_report"]["error"]
    assert rec["reset_report"]["drift"] == {"added": [], "removed": []}  # 残留线索
    assert rec["llm_calls"] == 1  # 仅 judge 1 次（CountingLLM 精确入账）


def test_run_agent_step5_reset_recovered_after_retry(tmp_path):
    lab = _FakeLab(fail_reset_calls={2})  # 收尾重置炸、重试成功
    records = R.run_agent([_task("tA")], 6.0, judge=False,
                          out_path=tmp_path / "out.jsonl",
                          lab=lab, graph_pair=(_FakeGraph(), R.CountingLLM(_CountInner())))
    assert records[0]["reset_report"]["recovered_after_retry"] is True
    assert records[0]["reset_report"]["clean"] is True
    assert records[0]["reset_report"]["error"] == ""


# ---------------------------------------------------------------------------
# 判分校准（人工决策 ③）：期望工具恰 1 个且恰调用该工具 → tools_reasonable 恒 true
# （先导实测：唯一正确工具调用被判 false，判分器裁量在该场景只有噪声）
# ---------------------------------------------------------------------------

def test_tools_match_single_expected_only_for_exact_single_call():
    assert R.tools_match_single_expected(
        ["get_running_config"], [{"tool": "get_running_config"}]) is True
    assert R.tools_match_single_expected(
        ["get_running_config"], [{"tool": "show_vlan"}]) is False  # 工具不对
    assert R.tools_match_single_expected(["get_running_config"], []) is False  # 没调用
    assert R.tools_match_single_expected(
        ["get_running_config", "show_vlan"],
        [{"tool": "get_running_config"}]) is False  # 多期望 → 仍归判分器裁量


def test_run_agent_single_expected_tool_overrides_judge_tools_reasonable(tmp_path):
    """判分器说 false 也不作数：单期望工具被恰好调用 → 运行器直接置 true。"""
    llm = R.CountingLLM(_CountInner(
        reply='{"conclusion_correct": true, "tools_reasonable": false, "reason": "j"}'))
    records = R.run_agent([_task("tA")], 6.0, judge=True,
                          out_path=tmp_path / "out.jsonl",
                          lab=_FakeLab(), graph_pair=(_FakeGraph(), llm))
    v = records[0]["verdict"]
    assert v["tools_reasonable"] is True
    assert v["conclusion_correct"] is True
    assert "单工具" in v["reason"]  # 覆盖来源可审计


def test_run_agent_multi_expected_tools_keeps_judge_discretion(tmp_path):
    """多期望但调用含越权工具（预期外）→ 判分器按校准判据裁量，false 保持 false。"""
    llm = R.CountingLLM(_CountInner(
        reply='{"conclusion_correct": true, "tools_reasonable": false, "reason": "j"}'))
    t = _task("tA")
    t["expected_tools"] = ["get_running_config", "show_vlan"]
    records = R.run_agent([t], 6.0, judge=True, out_path=tmp_path / "out.jsonl",
                          lab=_FakeLab(), graph_pair=(_FakeGraph(), llm))
    assert records[0]["verdict"]["tools_reasonable"] is False


# ---------------------------------------------------------------------------
# 判分校准扩展（修复轮 1，t02 根因②）：多预期工具的确定性判定
#   - 调用了至少一个预期工具且无越权（全部 ⊆ 预期）→ true
#   - 一个预期工具都没调（含零调用）→ false
#   - 含越权工具 / 期望为空 → 判分器按 JUDGE_SYSTEM 校准判据裁量
# ---------------------------------------------------------------------------

def test_calibrated_tools_reasonable_multi_expected():
    cal = R.calibrated_tools_reasonable
    # 单工具规则并存：恰调用该工具 → True；否则交判分器
    assert cal(["get_running_config"], [{"tool": "get_running_config"}]) == (
        True, "单工具自动判定")
    assert cal(["get_running_config"], [{"tool": "show_vlan"}]) is None
    # 多预期：调用其一且全部 ⊆ 预期 → True
    assert cal(["get_running_config", "show_vlan"],
               [{"tool": "show_vlan"}]) == (True, "多预期工具校准")
    assert cal(["show_ospf_neighbor", "show_ip_interface_brief", "get_running_config"],
               [{"tool": "show_ip_interface_brief"},
                {"tool": "show_ospf_neighbor"}]) == (True, "多预期工具校准")
    # 多预期：零调用 → False
    assert cal(["get_running_config", "show_vlan"], []) == (False, "多预期工具校准")
    # 多预期：调用含越权（预期外）工具 → 判分器裁量
    assert cal(["get_running_config", "show_vlan"],
               [{"tool": "show_ospf_neighbor"}]) is None
    # 期望为空 → 判分器裁量
    assert cal([], [{"tool": "show_vlan"}]) is None


class _SingleToolGraph:
    """只调用指定工具的图替身（tool_calls 可控）。"""

    def __init__(self, tools):
        self.tools = tools

    def invoke(self, state, config):
        return {"answer": "诊断", "citations": [],
                "tool_calls": [{"tool": t, "args": {"host": state["host"]},
                                "output": "..."} for t in self.tools],
                "handoff": False, "trace_meta": {"grades": [8.0], "rewrites": []}}


def test_run_agent_multi_expected_called_subset_overrides_true(tmp_path):
    """多预期 + 调用其一（全部 ⊆ 预期）→ 运行器直判 true（judge 说 false 也不算）。"""
    llm = R.CountingLLM(_CountInner(
        reply='{"conclusion_correct": true, "tools_reasonable": false, "reason": "j"}'))
    t = _task("tA")
    t["expected_tools"] = ["show_ospf_neighbor", "show_ip_interface_brief"]
    graph = _SingleToolGraph(["show_ip_interface_brief"])
    records = R.run_agent([t], 6.0, judge=True, out_path=tmp_path / "out.jsonl",
                          lab=_FakeLab(), graph_pair=(graph, llm))
    v = records[0]["verdict"]
    assert v["tools_reasonable"] is True
    assert "多预期工具校准" in v["reason"]


def test_run_agent_multi_expected_zero_calls_overrides_false(tmp_path):
    """多预期 + 一个预期工具都没调（零调用）→ 运行器直判 false（judge 说 true 也不算）。"""
    llm = R.CountingLLM(_CountInner(
        reply='{"conclusion_correct": true, "tools_reasonable": true, "reason": "j"}'))
    t = _task("tA")
    t["expected_tools"] = ["show_ospf_neighbor", "show_ip_interface_brief"]
    records = R.run_agent([t], 6.0, judge=True, out_path=tmp_path / "out.jsonl",
                          lab=_FakeLab(), graph_pair=(_SingleToolGraph([]), llm))
    v = records[0]["verdict"]
    assert v["tools_reasonable"] is False
    assert "多预期工具校准" in v["reason"]


def test_judge_prompt_documents_single_tool_calibration():
    """校准约定写进判分提示词：单工具场景运行器直判、无需裁量；多预期场景判据
    为「至少一个预期工具且无越权」。"""
    assert "tools_reasonable" in R.JUDGE_SYSTEM
    assert "无需" in R.JUDGE_SYSTEM
    assert "至少一个预期工具" in R.JUDGE_SYSTEM
    assert "越权" in R.JUDGE_SYSTEM


# ---------------------------------------------------------------------------
# CLI 缺省契约（收尾轮修复）：agent 模式不带 --ids → 跑全部任务（原缺省只跑
# 先导 3 条，全量评测会被静默截断）
# ---------------------------------------------------------------------------

def _fake_run_agent_capture(captured):
    def fake_run_agent(tasks, threshold, judge, out_path, **kw):
        captured["tasks"] = [t["task_id"] for t in tasks]
        return [{"task_id": t["task_id"], "verdict": {"conclusion_correct": True,
                 "tools_reasonable": True, "reason": "ok"}, "handoff": False,
                 "llm_calls": 1, "reset_report": {"clean": True}} for t in tasks]
    return fake_run_agent


def test_main_agent_without_ids_defaults_to_all_tasks(tmp_path, monkeypatch):
    captured = {}
    monkeypatch.setattr(R, "run_agent", _fake_run_agent_capture(captured))
    monkeypatch.setattr(sys, "argv",
                        ["run_e2e.py", "--tasks", "data/tasks/e2e_30.yaml",
                         "--out", str(tmp_path / "out.jsonl")])
    R.main()
    assert len(captured["tasks"]) == 30  # 缺省=全部 30 条（不再静默截断为先导 3 条）


def test_main_agent_with_ids_selects_subset(tmp_path, monkeypatch):
    captured = {}
    monkeypatch.setattr(R, "run_agent", _fake_run_agent_capture(captured))
    monkeypatch.setattr(sys, "argv",
                        ["run_e2e.py", "--tasks", "data/tasks/e2e_30.yaml",
                         "--ids", "t02,t17,t30",
                         "--out", str(tmp_path / "out.jsonl")])
    R.main()
    assert captured["tasks"] == ["t02", "t17", "t30"]


def test_verdict_record_shape():
    rec = R.verdict_record(
        {"task_id": "t02", "question": "q", "expected_conclusion": "c",
         "expected_tools": ["show_ospf_neighbor"], "difficulty": "easy",
         "fault": {"host": "core1", "kind": "shutdown_interface", "param": {"iface": "eth3"}}},
        answer="……", citations=["[1] x（doc）"], tool_calls=[{"tool": "show_ospf_neighbor"}],
        trace_meta={"grades": [7.0], "rewrites": []}, handoff=False,
        verdict={"conclusion_correct": True, "tools_reasonable": True, "reason": "ok"},
        inject=None, reset_report=None, wall_seconds=12.3, llm_calls=2)
    assert rec["task_id"] == "t02" and rec["verdict"]["conclusion_correct"] is True
    assert rec["llm_calls"] == 2 and rec["handoff"] is False
    assert rec["grades"] == [7.0]


def test_run_agent_graph_exception_records_consumed_llm_calls(tmp_path):
    class _GraphDiesAfterGrade:
        def __init__(self, llm):
            self.llm = llm

        def invoke(self, state, config):
            self.llm.chat([{"role": "user", "content": "grade 调用已消耗"}])
            raise RuntimeError("generation blew up")

    llm = R.CountingLLM(_CountInner())
    records = R.run_agent([_task("tA")], 6.0, judge=False,
                          out_path=tmp_path / "out.jsonl",
                          lab=_FakeLab(), graph_pair=(_GraphDiesAfterGrade(llm), llm))
    rec = records[0]
    assert "generation blew up" in rec["error"]
    assert rec["llm_calls"] == 1  # 异常路径已消耗的调用如实入账（评审 Minor 2）


# ---------------------------------------------------------------------------
# 单题计量（复审：CountingLLM 批内累计会虚报汇总、污染单题归因）
# ---------------------------------------------------------------------------

def test_counting_llm_reset():
    c = R.CountingLLM(_CountInner())
    c.chat([])
    c.chat([])
    c.reset()
    assert c.calls == 0


def test_run_agent_multi_item_llm_calls_are_per_item_not_cumulative(tmp_path):
    """3 题全判分：每条 llm_calls 应为该题真实消耗（1 次 judge），汇总=各题之和。"""
    records = R.run_agent([_task("tA"), _task("tB"), _task("tC")], 6.0, judge=True,
                          out_path=tmp_path / "out.jsonl",
                          lab=_FakeLab(), graph_pair=(_FakeGraph(), R.CountingLLM(_CountInner())))
    assert [r["llm_calls"] for r in records] == [1, 1, 1]  # 累计回归会是 1/2/3
    summary = R.summarize(records)
    assert summary["llm_calls"] == 3
    assert summary["llm_calls"] == sum(r["llm_calls"] for r in records)


def test_run_agent_multi_item_graph_exception_per_item_accounting(tmp_path):
    """混合批：第 1 题图消耗 1 次后炸，第 2 题正常判分——两条都记单题值。"""

    class _DiesOnce:
        def __init__(self, llm):
            self.llm = llm
            self.invocations = 0

        def invoke(self, state, config):
            self.invocations += 1
            if self.invocations == 1:
                self.llm.chat([{"role": "user", "content": "grade 调用已消耗"}])
                raise RuntimeError("boom after grade")
            return _FakeGraph().invoke(state, config)

    llm = R.CountingLLM(_CountInner())
    records = R.run_agent([_task("tA"), _task("tB")], 6.0, judge=True,
                          out_path=tmp_path / "out.jsonl",
                          lab=_FakeLab(), graph_pair=(_DiesOnce(llm), llm))
    assert "boom after grade" in records[0]["error"] and records[0]["llm_calls"] == 1
    assert records[1]["verdict"]["conclusion_correct"] is True and records[1]["llm_calls"] == 1
    summary = R.summarize(records)
    assert summary["llm_calls"] == 2 == sum(r["llm_calls"] for r in records)
