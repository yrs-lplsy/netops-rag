"""scripts/run_crag_eval.py 纯函数单测（零 API、零 Milvus、零 LLM）。

覆盖：引用 doc_id 提取、citation 命中判定、结果三分类（自动解决/转人工/未命中）、
初次低置信判定（grade 边界）、开/关配对转移（救回/损失/保持/双败）、汇总率计算。
"""

import importlib.util
import sys
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_crag_eval.py"


def _load_script():
    spec = importlib.util.spec_from_file_location("run_crag_eval_script", _SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


# ---------------------------------------------------------------------------
# doc_id 提取与 citation 命中
# ---------------------------------------------------------------------------

def test_doc_ids_from_citations_extracts_fullwidth_paren():
    mod = _load_script()
    cits = ["[1] IP路由 > BFD（hw-aaa-01-03）", "[2] 告警处理（hw-bbb-01-71）"]
    assert mod.doc_ids_from_citations(cits) == ["hw-aaa-01-03", "hw-bbb-01-71"]


def test_doc_ids_from_citations_robust_to_garbage():
    mod = _load_script()
    assert mod.doc_ids_from_citations(["没有括号", "", None, "工具:mcp（mcp:show）"]) == \
        ["", "", "", "mcp:show"]
    assert mod.doc_ids_from_citations([]) == []


def test_citation_hit_any_doc_in_expected():
    mod = _load_script()
    cits = ["[1] X（doc-a）", "[2] Y（doc-b）"]
    assert mod.citation_hit(cits, ["doc-b"]) is True
    assert mod.citation_hit(cits, ["doc-c"]) is False
    assert mod.citation_hit(cits, []) is False
    assert mod.citation_hit([], ["doc-a"]) is False


# ---------------------------------------------------------------------------
# 结果三分类
# ---------------------------------------------------------------------------

def test_classify_outcome_handoff_wins():
    mod = _load_script()
    assert mod.classify_outcome(handoff=True, hit=True) == "handoff"
    assert mod.classify_outcome(handoff=True, hit=False) == "handoff"


def test_classify_outcome_solved_requires_hit():
    mod = _load_script()
    assert mod.classify_outcome(handoff=False, hit=True) == "solved"
    assert mod.classify_outcome(handoff=False, hit=False) == "missed"


# ---------------------------------------------------------------------------
# 初次低置信（首次 grade < threshold；grade == threshold 算高分）
# ---------------------------------------------------------------------------

def test_first_grade_low_true_when_first_below_threshold():
    mod = _load_script()
    assert mod.first_grade_low([3.0, 7.0], 6.0) is True


def test_first_grade_low_false_when_first_at_or_above():
    mod = _load_script()
    assert mod.first_grade_low([6.0, 2.0], 6.0) is False  # ==threshold 算高分
    assert mod.first_grade_low([7.0], 6.0) is False


def test_first_grade_low_false_when_no_grades():
    mod = _load_script()
    assert mod.first_grade_low([], 6.0) is False


# ---------------------------------------------------------------------------
# 配对转移（救回/损失）
# ---------------------------------------------------------------------------

def test_paired_transitions_counts_and_qids():
    mod = _load_script()
    off = {"q1": "solved", "q2": "missed", "q3": "solved", "q4": "missed", "q5": "solved"}
    on = {"q1": "solved", "q2": "solved", "q3": "handoff", "q4": "handoff", "q5": "missed"}
    v = mod.paired_transitions(off, on)
    assert v["rescued"] == ["q2"]          # off 未解决 → on 解决
    assert v["lost"] == ["q3", "q5"]       # off 解决 → on 未解决
    assert v["stable_solved"] == ["q1"]
    assert v["both_fail"] == ["q4"]


def test_paired_transitions_error_counts_as_not_solved():
    mod = _load_script()
    v = mod.paired_transitions({"q1": "error"}, {"q1": "solved"})
    assert v["rescued"] == ["q1"]


# ---------------------------------------------------------------------------
# 汇总
# ---------------------------------------------------------------------------

def test_summarize_rates_and_crag_only_counters():
    mod = _load_script()
    recs = [
        {"qid": "q1", "outcome": "solved", "low_first": True, "rewritten": False, "calls": 2},
        {"qid": "q2", "outcome": "handoff", "low_first": True, "rewritten": True, "calls": 4},
        {"qid": "q3", "outcome": "missed", "low_first": False, "rewritten": True, "calls": 3},
        {"qid": "q4", "outcome": "error", "low_first": False, "rewritten": False, "calls": 0},
    ]
    s = mod.summarize(recs)
    assert s["n"] == 4
    assert s["solved"] == 1 and s["handoff"] == 1 and s["missed"] == 1 and s["error"] == 1
    assert abs(s["solve_rate"] - 0.25) < 1e-9
    assert abs(s["handoff_rate"] - 0.25) < 1e-9
    assert s["low_first"] == 2 and s["rewritten"] == 2
    assert abs(s["low_first_rate"] - 0.5) < 1e-9
    assert s["llm_calls"] == 9  # 求和（2+4+3+0），非"有调用记录条数"


def test_summarize_empty_guard():
    mod = _load_script()
    s = mod.summarize([])
    assert s["n"] == 0 and s["solve_rate"] == 0.0 and s["handoff_rate"] == 0.0
