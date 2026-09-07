"""data/tasks/e2e_30.yaml 任务清单 schema 与 QC 规则校验（纯文件，零 IO 设备）。

QC 规则（T14 Phase 1 数字纪律）：
  - 恰好 30 条、task_id 唯一且形如 tNN
  - fault 五元组合法（host/kind/param）；(host, kind, 规范化 param) 不重复
  - question 非空且含本任务 host 名（诊断启发式的 host 提取依赖）
  - expected_conclusion 非空且含具体取值（接口号/地址/取值之一）
  - expected_tools ⊆ 网关只读白名单；difficulty ∈ easy|medium|hard
  - 难度分布与 kind 分布锚定（防手滑改动）
"""

import pathlib

import pytest
import yaml

from netrag.tools_mcp.faults import FAULT_KINDS, build_fault_commands, parse_baseline
from netrag.tools_mcp.gateway import READONLY_TOOLS

ROOT = pathlib.Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "data" / "tasks" / "e2e_30.yaml"
DIFFICULTIES = {"easy", "medium", "hard"}


@pytest.fixture(scope="module")
def tasks():
    raw = yaml.safe_load(TASKS_PATH.read_text(encoding="utf-8"))
    assert isinstance(raw, dict) and "tasks" in raw
    return raw["tasks"]


def _param_key(param: dict) -> str:
    return "&".join(f"{k}={sorted(str(v))}" if isinstance(v, (list, set)) else f"{k}={v}"
                    for k, v in sorted((param or {}).items()))


def test_exactly_30_unique_ids(tasks):
    assert len(tasks) == 30
    ids = [t["task_id"] for t in tasks]
    assert len(set(ids)) == 30
    assert all(__import__("re").fullmatch(r"t\d{2}", i) for i in ids)


def test_fault_kinds_hosts_params_legal_and_buildable(tasks):
    hosts = {"core1", "core2", "acc1", "acc2"}
    for t in tasks:
        f = t["fault"]
        assert f["host"] in hosts, t["task_id"]
        assert f["kind"] in FAULT_KINDS, t["task_id"]
        baseline = parse_baseline(f["host"])
        cmds = build_fault_commands(f["host"], f["kind"], f["param"], baseline)
        assert cmds and all(isinstance(c, str) for c in cmds), t["task_id"]


def test_no_duplicate_host_kind_param(tasks):
    seen = set()
    for t in tasks:
        f = t["fault"]
        key = (f["host"], f["kind"], _param_key(f.get("param")))
        assert key not in seen, f"重复故障: {t['task_id']} {key}"
        seen.add(key)


def test_question_fields(tasks):
    for t in tasks:
        q = t["question"]
        assert q and len(q) >= 10, t["task_id"]
        assert t["fault"]["host"] in q, f"{t['task_id']} 问题未含主机名"
        c = t["expected_conclusion"]
        assert c and len(c) >= 10, t["task_id"]
        assert any(tok in c for tok in ("eth", "10.", "cost", "description")), \
            f"{t['task_id']} 结论缺具体取值: {c}"


def test_expected_tools_and_difficulty(tasks):
    for t in tasks:
        assert t["expected_tools"], t["task_id"]
        assert set(t["expected_tools"]) <= READONLY_TOOLS, t["task_id"]
        assert t["difficulty"] in DIFFICULTIES, t["task_id"]


def test_distribution_anchors(tasks):
    """分布锚：kind/难度计数改动须有意为之（改动本测试 = 校准决策）。"""
    from collections import Counter

    kinds = Counter(t["fault"]["kind"] for t in tasks)
    assert kinds == {"description_garbage": 9, "ospf_cost_skyhigh": 7,
                     "shutdown_interface": 6, "access_vlan_wrong": 6, "no_vlan": 2}
    diffs = Counter(t["difficulty"] for t in tasks)
    assert diffs == {"medium": 18, "easy": 7, "hard": 5}
    hosts = Counter(t["fault"]["host"] for t in tasks)
    assert set(hosts) == {"core1", "core2", "acc1", "acc2"}
    assert min(hosts.values()) >= 4  # acc2 物理下限（仅 2 条链路、无 VLAN 子接口）


def test_pilot_ids_are_easy(tasks):
    """先导 3 条必须为 easy（t02/t17/t30：shutdown/no_vlan/description 各一）。"""
    by_id = {t["task_id"]: t for t in tasks}
    for tid in ("t02", "t17", "t30"):
        assert by_id[tid]["difficulty"] == "easy", tid
    assert {by_id[i]["fault"]["kind"] for i in ("t02", "t17", "t30")} == \
        {"shutdown_interface", "no_vlan", "description_garbage"}
