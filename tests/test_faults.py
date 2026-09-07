"""faults.py 纯函数单测（零 IO）：基线解析/规范比对、故障命令构造、重置命令构造。

真机语义依据（2026-09-07 FRR 10.4.3 实测探针，详见 task-14 报告）：
  - ``shutdown`` / ``no shutdown``：接口 down、OSPF 邻居掉、恢复后 ~5s 重收敛
  - ``ip ospf cost 65535`` 的 no 形式带值（``no ip ospf cost 65535``）被接受
  - 内核态 VLAN 子接口（NETOPS_VLANS 启动建的 eth1.100/eth2.100）``no interface``
    删不掉（zebra 从内核重导入），故障形态改为摘 IP（``no ip address``）
  - FRR-only 子接口（eth1.200 等内核不存在的标签）``interface + ip address`` 可进
    running，``no interface`` 可整体删除 —— access_vlan_wrong 的 retag 通道
"""

import pathlib

import pytest

from netrag.tools_mcp.faults import (
    FaultError,
    build_fault_commands,
    build_reset_commands,
    canonical_entries,
    diff_config,
    find_vlan_subif,
    parse_baseline,
    verify_fault_in_running,
)

ROOT = pathlib.Path(__file__).resolve().parents[1]
CONFIGS = ROOT / "deploy/containerlab/configs"

# 真机 acc2 `show running-config` 原文（干净态，2026-09-07 抓取）——
# 与 baseline frr.conf 的渲染差异（passive-interface↔ip ospf passive、boilerplate、
# 注释行）全部体现在这里，是重置机制"干净节点零操作"的回归锚。
ACC2_RUNNING_CLEAN = """Building configuration...

Current configuration:
!
frr version 10.4.3_git
frr defaults traditional
hostname acc2
domainname localdomain
log syslog informational
!
interface eth1
 description P2P:acc2-core1
 ip address 10.0.102.2/30
 ip ospf network point-to-point
exit
!
interface eth2
 description P2P:acc2-core2
 ip address 10.0.202.2/30
 ip ospf network point-to-point
exit
!
interface lo
 ip address 10.255.0.4/32
 ip ospf passive
exit
!
router ospf
 ospf router-id 10.255.0.4
 network 10.0.102.0/30 area 0
 network 10.0.202.0/30 area 0
exit
!
end"""

# acc1 干净态（与真机探针一致，接口面 = eth1/eth1.100/eth2/lo）
ACC1_RUNNING_CLEAN = """Building configuration...

Current configuration:
!
frr version 10.4.3_git
frr defaults traditional
hostname acc1
domainname localdomain
log syslog informational
!
interface eth1
 description P2P:acc1-core1
 ip address 10.0.101.2/30
 ip ospf network point-to-point
exit
!
interface eth1.100
 description VLAN100-dot1q-example
 ip address 10.100.0.2/24
 ip ospf passive
exit
!
interface eth2
 description P2P:acc1-core2
 ip address 10.0.201.2/30
 ip ospf network point-to-point
exit
!
interface lo
 ip address 10.255.0.3/32
 ip ospf passive
exit
!
router ospf
 ospf router-id 10.255.0.3
 network 10.0.101.0/30 area 0
 network 10.0.201.0/30 area 0
exit
!
end"""

# no_vlan 后的 acc1：eth1.100 只剩 description + ip ospf passive（IP 被摘）
ACC1_NOVLAN = ACC1_RUNNING_CLEAN.replace(
    "interface eth1.100\n description VLAN100-dot1q-example\n ip address 10.100.0.2/24",
    "interface eth1.100\n description VLAN100-dot1q-example")
# access_vlan_wrong retag 后的 acc1：IP 迁到 eth1.200（FRR-only 标签），
# eth1.100 保留 description + ip ospf passive（与真实注入形态一致）
ACC1_RETAG = ACC1_RUNNING_CLEAN.replace(
    "interface eth1.100\n description VLAN100-dot1q-example\n ip address 10.100.0.2/24",
    "interface eth1.100\n description VLAN100-dot1q-example\n ip ospf passive\nexit\n!\n"
    "interface eth1.200\n description VLAN100-dot1q-example\n ip address 10.100.0.2/24")


def _base(host):
    return parse_baseline(host, baseline_dir=CONFIGS)


# ---------------------------------------------------------------------------
# 基线解析 / 规范化
# ---------------------------------------------------------------------------

def test_parse_baseline_core1_entries():
    entries = parse_baseline("core1", baseline_dir=CONFIGS)
    pairs = set(entries)
    assert (None, "router ospf") in pairs
    assert ("interface eth2", "ip address 10.0.101.1/30") in pairs
    assert ("interface eth2.100", "ip address 10.100.0.1/24") in pairs
    # passive-interface lo（router ospf 上下文）归一为接口侧写法
    assert ("interface lo", "ip ospf passive") in pairs
    assert ("interface eth2.100", "ip ospf passive") in pairs


def test_parse_baseline_strips_comments_and_boilerplate():
    entries = parse_baseline("core1", baseline_dir=CONFIGS)
    leaves = [l for _, l in entries]
    assert not any(l.startswith("!") for l in leaves)  # 中文注释行
    assert not any(l.startswith(("frr version", "frr defaults", "hostname",
                                 "domainname", "log ", "service ", "line vty"))
                   for l in leaves)
    assert "exit" not in leaves
    assert not any(l == "" for l in leaves)


def test_canonical_running_clean_diffs_empty():
    """真机干净 running ↔ baseline 规范比对：added/removed 全空（重置零操作的锚）。"""
    baseline = _base("acc2")
    assert len(canonical_entries(ACC2_RUNNING_CLEAN)) > 0
    added, removed = diff_config(ACC2_RUNNING_CLEAN, baseline)
    assert added == []
    assert removed == []
    added1, removed1 = diff_config(ACC1_RUNNING_CLEAN, _base("acc1"))
    assert added1 == [] and removed1 == []


# ---------------------------------------------------------------------------
# 故障命令构造
# ---------------------------------------------------------------------------

def test_build_shutdown_interface():
    assert build_fault_commands("core1", "shutdown_interface",
                                {"iface": "eth2"}, _base("core1")) == \
        ["interface eth2", "shutdown"]


def test_build_ospf_cost_skyhigh():
    assert build_fault_commands("core1", "ospf_cost_skyhigh",
                                {"iface": "eth3", "cost": 65535}, _base("core1")) == \
        ["interface eth3", "ip ospf cost 65535"]


def test_build_description_garbage():
    assert build_fault_commands("acc2", "description_garbage",
                                {"iface": "eth1", "text": "xJ48f-kz"}, _base("acc2")) == \
        ["interface eth1", "description xJ48f-kz"]


def test_build_no_vlan_uses_baseline_subif():
    # core1 的 VLAN100 子接口 = eth2.100 / 10.100.0.1/24（从基线解析，非硬编码）
    assert build_fault_commands("core1", "no_vlan", {"vlan": 100}, _base("core1")) == \
        ["interface eth2.100", "no ip address 10.100.0.1/24"]


def test_build_access_vlan_wrong_retag():
    cmds = build_fault_commands("acc1", "access_vlan_wrong",
                                {"mode": "retag", "vlan": 200}, _base("acc1"))
    assert cmds == [
        "interface eth1.100", "no ip address 10.100.0.2/24",
        "interface eth1.200", "description VLAN100-dot1q-example",
        "ip address 10.100.0.2/24",
    ]


def test_build_access_vlan_wrong_port():
    cmds = build_fault_commands("core1", "access_vlan_wrong",
                                {"mode": "wrong_port", "new_parent": "eth3"}, _base("core1"))
    assert cmds == [
        "interface eth2.100", "no ip address 10.100.0.1/24",
        "interface eth3.100", "description VLAN100-dot1q-example",
        "ip address 10.100.0.1/24",
    ]


def test_build_fault_commands_errors():
    with pytest.raises(FaultError):
        build_fault_commands("core1", "no_such_kind", {}, _base("core1"))
    with pytest.raises(FaultError):  # core2 基线无 VLAN 子接口
        build_fault_commands("core2", "no_vlan", {"vlan": 100}, _base("core2"))
    with pytest.raises(FaultError):  # retag 目标标签与原标签相同
        build_fault_commands("acc1", "access_vlan_wrong",
                             {"mode": "retag", "vlan": 100}, _base("acc1"))
    with pytest.raises(FaultError):  # wrong_port 新父口与原父口相同
        build_fault_commands("acc1", "access_vlan_wrong",
                             {"mode": "wrong_port", "new_parent": "eth1"}, _base("acc1"))
    with pytest.raises(FaultError):  # description 文本缺失
        build_fault_commands("acc2", "description_garbage", {"iface": "eth1"}, _base("acc2"))
    with pytest.raises(FaultError):  # shutdown 缺 iface
        build_fault_commands("acc2", "shutdown_interface", {}, _base("acc2"))


def test_build_fault_commands_idempotent():
    a = build_fault_commands("core1", "ospf_cost_skyhigh",
                             {"iface": "eth2", "cost": 65535}, _base("core1"))
    b = build_fault_commands("core1", "ospf_cost_skyhigh",
                             {"iface": "eth2", "cost": 65535}, _base("core1"))
    assert a == b  # 同参数重复注入下发同一命令序列（vtysh 覆盖语义 → 幂等收敛）


def test_find_vlan_subif():
    sub = find_vlan_subif(_base("acc1"), 100)
    assert sub == {"parent": "eth1", "ip": "10.100.0.2/24",
                   "description": "VLAN100-dot1q-example"}
    assert find_vlan_subif(_base("core2"), 100) is None


# ---------------------------------------------------------------------------
# 注入后状态核验（纯文本判定）
# ---------------------------------------------------------------------------

def test_verify_shutdown_present_absent():
    base = _base("acc2")
    injected = ACC2_RUNNING_CLEAN.replace(
        "interface eth1\n description P2P:acc2-core1",
        "interface eth1\n shutdown\n description P2P:acc2-core1")
    ok, detail = verify_fault_in_running(injected, "shutdown_interface",
                                         {"iface": "eth1"}, base)
    assert ok, detail
    ok2, _ = verify_fault_in_running(ACC2_RUNNING_CLEAN, "shutdown_interface",
                                     {"iface": "eth1"}, base)
    assert not ok2


def test_verify_description_and_cost():
    base = _base("acc2")
    injected = ACC2_RUNNING_CLEAN.replace(" description P2P:acc2-core1",
                                          " description xJ48f-kz-GARBAGE")
    ok, _ = verify_fault_in_running(injected, "description_garbage",
                                    {"iface": "eth1", "text": "xJ48f-kz-GARBAGE"}, base)
    assert ok
    ok2, _ = verify_fault_in_running(ACC2_RUNNING_CLEAN, "description_garbage",
                                     {"iface": "eth1", "text": "xJ48f-kz-GARBAGE"}, base)
    assert not ok2


def test_verify_no_vlan_and_avw():
    base = _base("acc1")
    ok, detail = verify_fault_in_running(ACC1_NOVLAN, "no_vlan", {"vlan": 100}, base)
    assert ok, detail
    ok2, _ = verify_fault_in_running(ACC1_RUNNING_CLEAN, "no_vlan", {"vlan": 100}, base)
    assert not ok2
    ok3, detail3 = verify_fault_in_running(ACC1_RETAG, "access_vlan_wrong",
                                           {"mode": "retag", "vlan": 200}, base)
    assert ok3, detail3
    ok4, _ = verify_fault_in_running(ACC1_RUNNING_CLEAN, "access_vlan_wrong",
                                     {"mode": "retag", "vlan": 200}, base)
    assert not ok4


# ---------------------------------------------------------------------------
# 重置命令构造
# ---------------------------------------------------------------------------

def test_build_reset_commands_noop_when_clean():
    assert build_reset_commands(ACC2_RUNNING_CLEAN, _base("acc2")) == []
    assert build_reset_commands(ACC1_RUNNING_CLEAN, _base("acc1")) == []


def test_build_reset_after_shutdown():
    injected = ACC2_RUNNING_CLEAN.replace(
        "interface eth1\n description P2P:acc2-core1",
        "interface eth1\n shutdown\n description P2P:acc2-core1")
    cmds = build_reset_commands(injected, _base("acc2"))
    assert cmds == ["interface eth1", "no shutdown", "exit"]


def test_build_reset_after_description():
    injected = ACC2_RUNNING_CLEAN.replace(" description P2P:acc2-core1",
                                          " description GARBAGE")
    cmds = build_reset_commands(injected, _base("acc2"))
    # negation（description 特例：no description）+ 基线重放（原描述）
    assert cmds == ["interface eth1", "no description", "exit",
                    "interface eth1", "description P2P:acc2-core1", "exit"]


def test_build_reset_after_cost():
    injected = ACC2_RUNNING_CLEAN.replace(
        "interface eth1\n description P2P:acc2-core1",
        "interface eth1\n ip ospf cost 65535\n description P2P:acc2-core1")
    cmds = build_reset_commands(injected, _base("acc2"))
    assert cmds == ["interface eth1", "no ip ospf cost 65535", "exit"]


def test_build_reset_after_retag():
    """retag 重置 = FRR-only 块整体删除（真机验证过 no interface 可删）+ 基线 IP 回填。"""
    cmds = build_reset_commands(ACC1_RETAG, _base("acc1"))
    assert cmds == ["no interface eth1.200",
                    "interface eth1.100", "ip address 10.100.0.2/24", "exit"]


def test_build_reset_after_no_vlan_replays_baseline_ip():
    cmds = build_reset_commands(ACC1_NOVLAN, _base("acc1"))
    assert cmds == ["interface eth1.100", "ip address 10.100.0.2/24", "exit"]


# ---------------------------------------------------------------------------
# FaultLab 执行层（spy DeviceConnection：绝不 write memory）
# ---------------------------------------------------------------------------

class _SpyDevice:
    """记录调用的 DeviceConnection 替身（只实现 FaultLab 用到的三个方法）。"""

    def __init__(self, running_text: str):
        self.running_text = running_text
        self.config_calls: list[tuple[str, list[str]]] = []
        self.persist_calls = 0

    def run_config(self, host, cli_lines):
        self.config_calls.append((host, list(cli_lines)))
        return "ok"

    def get_running_config(self, host):
        return self.running_text

    def run_show(self, host, command):
        # 3 个 Full 邻居的极简形（wait_healthy 只数 Full/ 出现次数）
        return ("Neighbor ID Pri State\n"
                "10.255.0.2 1 Full/- eth1\n10.255.0.3 1 Full/- eth2\n"
                "10.255.0.4 1 Full/- eth3\n")

    def persist(self, host):  # pragma: no cover — FaultLab 契约禁止走到这里
        self.persist_calls += 1
        raise AssertionError("FaultLab 不允许 write memory/persist")


def test_faultlab_inject_uses_run_config_never_persist():
    from netrag.tools_mcp.faults import FaultLab

    dev = _SpyDevice(ACC2_RUNNING_CLEAN.replace(
        " description P2P:acc2-core1", " description xJ48f-kz_GARBAGE"))
    lab = FaultLab(device=dev)
    rep = lab.inject("acc2", "description_garbage",
                     {"iface": "eth1", "text": "xJ48f-kz_GARBAGE"})
    assert rep["verified"] is True
    assert dev.config_calls == [("acc2", ["interface eth1", "description xJ48f-kz_GARBAGE"])]
    assert dev.persist_calls == 0


def test_faultlab_reset_clean_node_zero_io():
    from netrag.tools_mcp.faults import FaultLab

    dev = _SpyDevice(ACC2_RUNNING_CLEAN)
    lab = FaultLab(device=dev)
    rep = lab.reset(["acc2"])
    assert rep["acc2"] == {"changed": False, "commands": []}
    assert dev.config_calls == []
    assert dev.persist_calls == 0


def test_faultlab_reset_dirty_node_converges():
    from netrag.tools_mcp.faults import FaultLab

    dirty = ACC1_NOVLAN
    dev = _SpyDevice(dirty)
    lab = FaultLab(device=dev)
    rep = lab.reset(["acc1"])
    assert rep["acc1"]["changed"] is True
    assert dev.config_calls == [("acc1", ["interface eth1.100",
                                          "ip address 10.100.0.2/24", "exit"])]
    assert dev.persist_calls == 0
    # 重置后 diff 应为干净（回读文本换成干净态模拟收敛）
    dev.running_text = ACC1_RUNNING_CLEAN
    assert lab.diff_from_baseline("acc1") == ([], [])


def test_faultlab_wait_healthy_parses_full():
    from netrag.tools_mcp.faults import FaultLab

    dev = _SpyDevice("")
    lab = FaultLab(device=dev)
    assert lab.wait_healthy(timeout=1) is True
