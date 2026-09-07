"""故障注入 + lab 重置（T14 端到端排障评测基建）。

位置抉择：放 ``src/netrag/tools_mcp/``（而非 scripts/）——与 device.py 共用同一
连接缝（inventory + netmiko），纯函数命令构造器可零 IO 单测，评测脚本与 lab
marked 测试都能 import。

**故障形态（5 类，全部只动 running-config、不 write memory —— bind-mount 的
基线 frr.conf 不被触碰，git 保持干净）**：

===========================  ========================  ==================================
kind                          param                     vtysh 语义（FRR 10.4.3 实测）
===========================  ========================  ==================================
shutdown_interface            {iface}                   interface + shutdown / no shutdown
ospf_cost_skyhigh             {iface, cost=65535}       ip ospf cost N（邻居保持 Full，
                                                        路由绕行——观测靠 running-config）
description_garbage           {iface, text}             description 覆盖语义
no_vlan                       {vlan}                    摘 VLAN 子接口三层 IP。**不能用
                                                        ``no interface``**：内核态子接口
                                                        （NETOPS_VLANS 启动建的 ethN.100）
                                                        会被 zebra 从内核重导入，删不掉；
                                                        摘 IP 即"VLAN100 三层不通"的诚实形态
access_vlan_wrong             {mode: retag|wrong_port,  VLAN100 的 IP 迁到错误标签/错误物理口
                              vlan | new_parent}        （FRR-only 子接口可整体 ``no
                                                        interface`` 删除——真机已验证）
===========================  ========================  ==================================

**重置机制（reset_lab）**：基线文件 diff 比对，非故障台账——对每个 FRR 节点取
running-config，与 ``deploy/containerlab/configs/<host>/frr.conf`` 做*规范化*
比对（渲染差异归一，见下），``no`` 掉多出的行、回放缺失的行，全程不持久化。
选此机制的理由：无需维护注入台账（任何来源的漂移——手改/上轮崩溃残留——都能
收敛回基线），且干净节点零操作。渲染差异归一（真机实测）：
  - 基线 ``router ospf`` 下的 ``passive-interface X`` ≡ running 接口块内的
    ``ip ospf passive``
  - 剔除两侧 boilerplate（frr version/defaults、hostname、domainname、log、
    service、line vty）、注释行、exit/end
  - FRR-only 新增上下文（如注入产生的 ``interface eth1.200``，不在基线）→ 整块
    ``no <context>`` 删除；基线已有上下文内的新增叶 → 逐叶 ``no <leaf>``
    （``description`` 特例 ``no description``，与 device.py 同款）
OSPF 重收敛由 :meth:`FaultLab.wait_healthy` 显式等待（shutdown 类恢复后 ~5-40s），
不混入 reset 本体（保持 reset 快速、可组合）。
"""

from __future__ import annotations

import time
from pathlib import Path

from netrag.tools_mcp.device import (
    _CONTEXT_OPENER,  # 上下文声明行识别与 device.py 共用一源，避免双份漂移
    DeviceConnection,
    running_entries,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
BASELINE_DIR = REPO_ROOT / "deploy" / "containerlab" / "configs"

FAULT_KINDS = (
    "shutdown_interface",
    "ospf_cost_skyhigh",
    "description_garbage",
    "no_vlan",
    "access_vlan_wrong",
)

LAB_FRR_HOSTS = ("core1", "core2", "acc1", "acc2")

# 比对时剔除的 boilerplate（身份/渲染性配置，不参与 diff，永不 negate/重放）
_BOILERPLATE_PREFIXES = (
    "frr version", "frr defaults", "hostname", "domainname",
    "log ", "service ", "line vty",
    "Building configuration", "Current configuration",  # show running 包头
)

# 基线 passive-interface（router ospf 上下文）→ running 接口块内 ip ospf passive
_PASSIVE_RE_LENGTH = len("passive-interface ")


class FaultError(RuntimeError):
    """故障定义非法（未知 kind/参数缺失/基线不支持该形态）。"""


# ---------------------------------------------------------------------------
# 规范化解析（纯函数）
# ---------------------------------------------------------------------------

def canonical_entries(config_text: str) -> list[tuple[str | None, str]]:
    """running/baseline 配置文本 → 规范 (上下文, 叶) 序列（比对/重放的统一形）。

    剔除 boilerplate/注释/exit/end；``router ospf`` 上下文的
    ``passive-interface X`` 归一为 ``('interface X', 'ip ospf passive')``。
    """
    out: list[tuple[str | None, str]] = []
    header: str | None = None
    for line in (config_text or "").splitlines():
        s = line.strip()
        if not s or s == "!" or s in ("exit", "end") or s.startswith("!"):
            continue
        if s.startswith(_BOILERPLATE_PREFIXES):
            continue
        if line[:1].isspace():
            ctx_leaf = (header, s)
        else:
            header = s
            ctx_leaf = (None, s)
        # passive-interface 归一（基线在 router ospf 上下文，running 在接口上下文）
        if ctx_leaf[1].startswith("passive-interface ") and ctx_leaf[0] in (None, "router ospf"):
            out.append((f"interface {ctx_leaf[1][_PASSIVE_RE_LENGTH:].strip()}",
                        "ip ospf passive"))
            continue
        out.append(ctx_leaf)
    return out


def parse_baseline(host: str, baseline_dir: Path | str | None = None) -> list[tuple[str | None, str]]:
    """读 deploy/containerlab/configs/<host>/frr.conf 基线 → 规范序列。"""
    path = Path(baseline_dir) / host / "frr.conf" if baseline_dir else BASELINE_DIR / host / "frr.conf"
    if not path.exists():
        raise FaultError(f"baseline config not found: {path}")
    return canonical_entries(path.read_text(encoding="utf-8"))


def diff_config(
    running_text: str, baseline: list[tuple[str | None, str]],
) -> tuple[list[tuple[str | None, str]], list[tuple[str | None, str]]]:
    """running 与基线规范化比对 → (added, removed)，各为 (上下文, 叶) 列表。"""
    running = canonical_entries(running_text)
    base_set = set(baseline)
    run_set = set(running)
    added = [e for e in running if e not in base_set]
    removed = [e for e in baseline if e not in run_set]
    return added, removed


def find_vlan_subif(
    baseline: list[tuple[str | None, str]], vlan: int,
) -> dict | None:
    """基线中 vlan 子接口的定义 → {parent, ip, description}（无 → None）。"""
    want_ctx = f"interface *.{vlan}"
    leaves: dict[str, str] = {}
    parent = None
    for ctx, leaf in baseline:
        if ctx and ctx.startswith("interface ") and "." in ctx:
            tag = ctx.rsplit(".", 1)[1]
            if tag.isdigit() and int(tag) == vlan:
                want_ctx = ctx
                parent = ctx.split()[1].rsplit(".", 1)[0]
                if leaf.startswith("ip address "):
                    leaves["ip"] = leaf[len("ip address "):]
                elif leaf.startswith("description "):
                    leaves["description"] = leaf[len("description "):]
    if parent is None or "ip" not in leaves:
        return None
    return {"parent": parent, "ip": leaves["ip"],
            "description": leaves.get("description", "")}


# ---------------------------------------------------------------------------
# 故障/重置命令构造（纯函数）
# ---------------------------------------------------------------------------

def _need(param: dict, key: str, kind: str):
    v = (param or {}).get(key)
    if v is None or (isinstance(v, str) and not v.strip()):
        raise FaultError(f"kind={kind} 缺少必填参数 {key!r}（param={param}）")
    return v


def build_fault_commands(
    host: str, kind: str, param: dict,
    baseline: list[tuple[str | None, str]],
) -> list[str]:
    """故障 → conf t 内的 vtysh 命令序列（run_config 会自行包 conf t/end）。

    幂等安全：全部为覆盖/移除语义，重复下发收敛到同一状态。
    """
    if kind == "shutdown_interface":
        iface = _need(param, "iface", kind)
        return [f"interface {iface}", "shutdown"]
    if kind == "ospf_cost_skyhigh":
        iface = _need(param, "iface", kind)
        cost = int(_need(param, "cost", kind))
        if not (0 < cost <= 65535):
            raise FaultError(f"ospf cost 越界: {cost}")
        return [f"interface {iface}", f"ip ospf cost {cost}"]
    if kind == "description_garbage":
        iface = _need(param, "iface", kind)
        text = str(_need(param, "text", kind)).strip()
        if any(c in text for c in "\n\r!"):
            raise FaultError(f"description 非法字符: {text!r}")
        return [f"interface {iface}", f"description {text}"]
    if kind == "no_vlan":
        vlan = int(_need(param, "vlan", kind))
        sub = find_vlan_subif(baseline, vlan)
        if sub is None:
            raise FaultError(f"{host} 基线无 VLAN{vlan} 子接口，no_vlan 不可表达")
        return [f"interface {sub['parent']}.{vlan}", f"no ip address {sub['ip']}"]
    if kind == "access_vlan_wrong":
        mode = _need(param, "mode", kind)
        sub = find_vlan_subif(baseline, 100)  # 实验唯一业务 VLAN 固定 100
        if sub is None:
            raise FaultError(f"{host} 基线无 VLAN100 子接口，access_vlan_wrong 不可表达")
        parent = sub["parent"]
        if mode == "retag":
            tag = int(_need(param, "vlan", kind))
            if tag == 100:
                raise FaultError("retag 目标标签不能等于原标签 100")
            new_if = f"{parent}.{tag}"
        elif mode == "wrong_port":
            new_parent = str(_need(param, "new_parent", kind))
            if new_parent == parent:
                raise FaultError("wrong_port 新父口不能与原父口相同")
            new_if = f"{new_parent}.100"
        else:
            raise FaultError(f"未知 access_vlan_wrong mode: {mode!r}")
        # 前半摘原口 IP（内核子接口删不掉块），后半把 IP 挂到错误标签/端口
        # （FRR-only 接口，真机验证可进 running 且可 no interface 整删）
        return [f"interface {parent}.100", f"no ip address {sub['ip']}",
                f"interface {new_if}", f"description {sub['description']}",
                f"ip address {sub['ip']}"]
    raise FaultError(f"未知故障类型: {kind!r}（支持: {FAULT_KINDS}）")


def verify_fault_in_running(
    running_text: str, kind: str, param: dict,
    baseline: list[tuple[str | None, str]],
) -> tuple[bool, str]:
    """注入核验（纯文本）：running 的规范序列含/缺期望行 → (ok, 说明)。"""
    entries = set(canonical_entries(running_text))

    def has(ctx: str | None, leaf: str) -> bool:
        return (ctx, leaf) in entries

    if kind == "shutdown_interface":
        iface = _need(param, "iface", kind)
        ok = has(f"interface {iface}", "shutdown")
        return ok, f"({iface}, shutdown) {'存在' if ok else '缺失'}"
    if kind == "ospf_cost_skyhigh":
        iface = _need(param, "iface", kind)
        cost = int(_need(param, "cost", kind))
        ok = has(f"interface {iface}", f"ip ospf cost {cost}")
        return ok, f"({iface}, ip ospf cost {cost}) {'存在' if ok else '缺失'}"
    if kind == "description_garbage":
        iface = _need(param, "iface", kind)
        text = str(_need(param, "text", kind)).strip()
        ok = has(f"interface {iface}", f"description {text}")
        return ok, f"({iface}, description {text}) {'存在' if ok else '缺失'}"
    if kind == "no_vlan":
        vlan = int(_need(param, "vlan", kind))
        sub = find_vlan_subif(baseline, vlan)
        if sub is None:
            raise FaultError(f"{host} 基线无 VLAN{vlan} 子接口")
        ok = not has(f"interface {sub['parent']}.{vlan}", f"ip address {sub['ip']}")
        return ok, (f"({sub['parent']}.{vlan}, ip address {sub['ip']}) "
                    f"{'已摘除' if ok else '仍在'}")
    if kind == "access_vlan_wrong":
        mode = _need(param, "mode", kind)
        sub = find_vlan_subif(baseline, 100)
        if sub is None:
            raise FaultError(f"{host} 基线无 VLAN100 子接口")
        if mode == "retag":
            tag = int(_need(param, "vlan", kind))
            new_if = f"{sub['parent']}.{tag}"
        elif mode == "wrong_port":
            new_if = f"{_need(param, 'new_parent', kind)}.100"
        else:
            raise FaultError(f"未知 access_vlan_wrong mode: {mode!r}")
        moved = has(f"interface {new_if}", f"ip address {sub['ip']}")
        gone = not has(f"interface {sub['parent']}.100", f"ip address {sub['ip']}")
        return (moved and gone,
                f"IP@{new_if} {'存在' if moved else '缺失'} / "
                f"IP@{sub['parent']}.100 {'仍在' if not gone else '已摘'}")
    raise FaultError(f"未知故障类型: {kind!r}")


def build_reset_commands(
    running_text: str, baseline: list[tuple[str | None, str]],
) -> list[str]:
    """漂移 → 收敛回基线的 vtysh 命令序列（negation 多余 + 重放缺失，不持久化）。

    - 基线外的整块上下文（FRR-only，如注入的 eth1.200）→ ``no <context>`` 整删
    - 基线内上下文的多余叶 → 逐叶 ``no <leaf>``（``description`` → ``no description``）
    - 基线有而 running 缺的行 → 按上下文重放
    干净节点 → []（零下发）。
    """
    added, removed = diff_config(running_text, baseline)
    base_ctxs = {ctx for ctx, _ in baseline if ctx is not None}
    cmds: list[str] = []

    # 1) 基线外的整块上下文（FRR-only，如注入的 eth1.200）→ ``no <context>`` 整删。
    #    注意 canonical 序列里上下文声明行以 (None, 'interface X') 出现，须识别归入
    #    块删除，不得走叶 negation（否则重复 no 且块空后残留声明行）。
    block_ctxs: set[str] = set()
    leaf_added: list[tuple[str | None, str]] = []
    for ctx, leaf in added:
        if ctx is None and _CONTEXT_OPENER.match(leaf):
            block_ctxs.add(leaf)
        elif ctx is not None and ctx not in base_ctxs:
            block_ctxs.add(ctx)
        else:
            leaf_added.append((ctx, leaf))
    cmds.extend(f"no {ctx}" for ctx in sorted(block_ctxs))

    # 2) 基线内上下文的逐叶 negation（按上下文分组，上下文只进一次）
    by_ctx: dict[str | None, list[str]] = {}
    for ctx, leaf in leaf_added:
        by_ctx.setdefault(ctx, []).append(leaf)
    for ctx, leaves in by_ctx.items():
        neg = ["no description" if l.startswith("description") else f"no {l}"
               for l in leaves]
        if ctx is None:
            cmds.extend(neg)
        else:
            cmds.extend([ctx, *neg, "exit"])

    # 3) 基线缺失行按上下文重放
    replay: dict[str | None, list[str]] = {}
    for ctx, leaf in removed:
        replay.setdefault(ctx, []).append(leaf)
    for ctx, leaves in replay.items():
        if ctx is None:
            cmds.extend(leaves)
        else:
            cmds.extend([ctx, *leaves, "exit"])
    return cmds


# ---------------------------------------------------------------------------
# 真机执行层（netmiko 缝与 device.py 共用）
# ---------------------------------------------------------------------------

class FaultLab:
    """故障注入 / lab 重置门面。device 可注入（单测 spy），缺省真实 DeviceConnection。

    纪律：注入与重置**永不 write memory**（running-config 态即可满足评测，
    bind-mount 基线文件与 git 工作区保持干净）。
    """

    def __init__(
        self,
        device: DeviceConnection | None = None,
        baseline_dir: Path | str | None = None,
    ):
        self.device = device if device is not None else DeviceConnection()
        self.baseline_dir = Path(baseline_dir) if baseline_dir else BASELINE_DIR
        self._baselines: dict[str, list[tuple[str | None, str]]] = {}

    def baseline(self, host: str) -> list[tuple[str | None, str]]:
        if host not in self._baselines:
            self._baselines[host] = parse_baseline(host, baseline_dir=self.baseline_dir)
        return self._baselines[host]

    # -- 注入 ---------------------------------------------------------------

    def inject(self, host: str, kind: str, param: dict) -> dict:
        """下发故障命令并回读 running 核验。返回变更描述（含核验结果）。"""
        baseline = self.baseline(host)
        cmds = build_fault_commands(host, kind, param, baseline)
        self.device.run_config(host, cmds)
        running = self.device.get_running_config(host)
        ok, detail = verify_fault_in_running(running, kind, param, baseline)
        return {"host": host, "kind": kind, "param": dict(param or {}),
                "commands": cmds, "verified": ok, "verify_detail": detail}

    # -- 重置 ---------------------------------------------------------------

    def reset(self, hosts: list[str] | tuple[str, ...] | None = None) -> dict:
        """把（全部/指定）FRR 节点收敛回基线。返回每节点 {changed, commands}。"""
        hosts = hosts or LAB_FRR_HOSTS
        report: dict = {}
        for host in hosts:
            baseline = self.baseline(host)
            running = self.device.get_running_config(host)
            cmds = build_reset_commands(running, baseline)
            if cmds:
                self.device.run_config(host, cmds)
            report[host] = {"changed": bool(cmds), "commands": cmds}
        return report

    def diff_from_baseline(self, host: str) -> tuple[list, list]:
        """当前 running 相对基线的 (added, removed)——重置后应为 ([], [])。"""
        return diff_config(self.device.get_running_config(host), self.baseline(host))

    # -- 健康等待 ------------------------------------------------------------

    def wait_healthy(self, timeout: float = 90, expect_full: int = 3,
                     probe_host: str = "core1") -> bool:
        """轮询 probe_host 的 OSPF 邻居直到 expect_full 个 Full（重置后重收敛）。"""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            try:
                out = self.device.run_show(probe_host, "show ip ospf neighbor")
                if out.count("Full/") >= expect_full:
                    return True
            except Exception:  # noqa: BLE001 — 单次轮询失败（断连抖动）继续等
                pass
            time.sleep(3)
        return False
