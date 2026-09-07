"""T12 真机冒烟（marker: ``lab``，无 LLM）：FastMCP 14 工具 × containerlab 实设备。

覆盖：
  - 只读：get_running_config(core1)、show_ospf_neighbor(core1)（期望 3 个邻居）、
    netconf_get(nc1)（yang-library 含 ietf-interfaces）
  - 写：审批门全流程 on acc1（request → approve → push → 窗口内 confirm →
    write memory 持久化过窗口 → 幂等 no-op → restore_snapshot 清场）
  - 手写 commit-confirmed 的自动回滚真机验证（不确认 → 到期自动恢复）

写路径只在 acc1 eth1 上打 description 标记（eth0 无配置、不在 running 中），
测试自清理（restore/自动回滚），并把快照临时目录用后即清。

评审 Finding 2：confirm/restore/回滚的 write memory 持久化会重写 bind-mount
的基线 `deploy/containerlab/configs/acc1/frr.conf`（丢注释、owner 变 root 600），
模块 teardown fixture 自动 `git checkout` 还原（先 sudo 放权限供 git 写），
跑完 `git status` 保持干净；永久解法（persist 改 opt-in）记为 deferred。
"""

import json
import pathlib
import subprocess
import time

import pytest

from netrag.tools_mcp import approval
from netrag.tools_mcp.device import DeviceConnection
from netrag.tools_mcp.server import build_server

pytestmark = [pytest.mark.lab]

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASELINE_CONF = ROOT / "deploy" / "containerlab" / "configs" / "acc1" / "frr.conf"
EXPECT_NODES = {"core1", "core2", "acc1", "acc2", "nc1"}
WINDOW = 15  # 回滚窗口（秒）：确认后需等过窗口证明定时器被取消

YANG_LIBRARY_FILTER = (
    '<modules-state xmlns="urn:ietf:params:xml:ns:yang:ietf-yang-library"/>'
)
PUSH_LINES = ["interface eth1", "description TOC-test", "exit"]  # eth1 在 running 中有块（eth0 无配置不在 running）


@pytest.fixture(scope="module", autouse=True)
def _restore_frr_conf_baseline():
    """模块 teardown：自动还原被 write memory 重写的 bind-mount 基线文件。

    write memory 后文件 owner 变 root/600，git 无法读写，先 sudo 放权限再
    `git checkout HEAD --`（内容/权限按 git 基线恢复，设备 running 态不受影响）。
    """
    yield
    try:
        subprocess.run(["sudo", "-n", "chmod", "a+r,u+w", str(BASELINE_CONF)],
                       capture_output=True, timeout=30, check=False)
    except (OSError, subprocess.SubprocessError):
        pass
    subprocess.run(
        ["git", "checkout", "HEAD", "--", str(BASELINE_CONF.relative_to(ROOT))],
        cwd=ROOT, capture_output=True, timeout=60, check=False,
    )


def _lab_deployed() -> bool:
    try:
        proc = subprocess.run(
            ["docker", "ps", "--filter", "name=clab-netops-", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    if proc.returncode != 0:
        return False
    names = {n.strip() for n in proc.stdout.splitlines() if n.strip()}
    return {f"clab-netops-{n}" for n in EXPECT_NODES} <= names


@pytest.fixture(scope="module")
def lab_env(tmp_path_factory):
    if not _lab_deployed():
        pytest.skip("lab not deployed")
    device = DeviceConnection()  # 真实 inventory/netmiko/ncclient
    approvals = tmp_path_factory.mktemp("approvals") / "approvals.jsonl"
    server = build_server(device=device, approvals_path=str(approvals))
    return server, approvals, device


@pytest.fixture(scope="module")
def mcp_server(lab_env):
    return lab_env[0]


def call(server, tool, args):
    import asyncio
    from fastmcp import Client

    async def _run():
        async with Client(server) as client:
            return await client.call_tool(tool, args)

    return asyncio.run(_run())


def _text(result):
    return result.content[0].text


def _data(result):
    return json.loads(_text(result))


def _approve(approvals_path, host, planned_lines):
    """审批两步：request → approve。返回 (approval_id, token)。"""
    rid = approval.request_approval(host, planned_lines, path=approvals_path)
    return rid, approval.approve(rid, "lab-tester", path=approvals_path)


# ---------------------------------------------------------------------------
# 只读
# ---------------------------------------------------------------------------

def test_get_running_config_core1(mcp_server):
    out = _text(call(mcp_server, "get_running_config", {"host": "core1"}))
    assert "hostname core1" in out
    assert "router ospf" in out


def test_show_ospf_neighbor_core1_three_full(mcp_server):
    out = _text(call(mcp_server, "show_ospf_neighbor", {"host": "core1"}))
    full = [l for l in out.splitlines() if "Full/" in l]
    assert len(full) == 3, f"期望 3 个 Full 邻居，实际 {len(full)}: {out}"


def test_netconf_get_nc1_yang_library(mcp_server):
    out = _text(call(mcp_server, "netconf_get",
                     {"host": "nc1", "filter_xml": YANG_LIBRARY_FILTER}))
    assert "ietf-interfaces" in out


def test_show_version_core1(mcp_server):
    out = _text(call(mcp_server, "show_version", {"host": "core1"}))
    assert "FRR" in out


# ---------------------------------------------------------------------------
# 写路径：审批门 + 幂等 + 快照回滚（acc1 eth0，自清理）
# ---------------------------------------------------------------------------

def _running_contains(mcp_server, needle):
    out = _text(call(mcp_server, "get_running_config", {"host": "acc1"}))
    return needle in out, out


ORIG_ETH1_DESC = "description P2P:acc1-core1"


def _force_cleanup_acc1():
    """写测试护栏：无条件把 acc1 收敛回原始态（防上轮崩溃残留的 TOC-test /
    eth1 描述被覆盖）。FRR description 为覆盖语义、空块自动消失，故收敛序列
    幂等：eth0 去 description（块消失）+ eth1 恢复原描述 + write memory。"""
    import netmiko

    c = netmiko.ConnectHandler(device_type="linux", host="127.0.0.1", port=22023,
                               username="root", password="root", timeout=15,
                               use_keys=False, allow_agent=False)
    try:
        for cmd in ["conf t", "interface eth0", "no description", "end",
                    "conf t", "interface eth1", ORIG_ETH1_DESC, "end", "write memory"]:
            c.send_command_timing(cmd, read_timeout=30)
    finally:
        c.disconnect()


def test_write_flow_approve_push_confirm_persist_noop_restore(lab_env):
    mcp_server, approvals, _device = lab_env
    _force_cleanup_acc1()

    # 1) 无 token 直接拒绝（设备未被触碰）
    from fastmcp.exceptions import ToolError
    with pytest.raises(ToolError, match="审批门拒绝"):
        call(mcp_server, "push_config", {
            "host": "acc1", "cli_lines": PUSH_LINES, "approval_id": "fake",
            "token": "fake", "approved_by": "nobody",
        })
    assert not _running_contains(mcp_server, "TOC-test")[0]

    # 2) 审批 → push（15s 回滚窗口）
    rid, token = _approve(approvals, "acc1", PUSH_LINES)
    result = _data(call(mcp_server, "push_config", {
        "host": "acc1", "cli_lines": PUSH_LINES, "approval_id": rid,
        "token": token, "approved_by": "lab-tester", "rollback_seconds": WINDOW,
    }))
    assert result["status"] == "awaiting_confirm"
    assert result["already_applied"] == ["interface eth1", "exit"]  # 部分幂等报告
    assert result["applied"] == ["description TOC-test"]
    snap = pathlib.Path(result["snapshot_path"])
    assert snap.exists() and "TOC-test" not in snap.read_text(encoding="utf-8")
    ok, running = _running_contains(mcp_server, "description TOC-test")
    assert ok, running

    # 3) 窗口内 confirm（同一已批准变更，复用同一 token）→ 过窗口仍存活
    ts = result["snapshot_ts"]
    confirmed = _data(call(mcp_server, "push_config", {
        "host": "acc1", "cli_lines": PUSH_LINES, "approval_id": rid,
        "token": token, "approved_by": "lab-tester",
        "confirm_transaction": True, "snapshot_ts": ts,
    }))
    assert confirmed["status"] == "confirmed"
    assert confirmed["persist"]["ok"], confirmed["persist"]
    time.sleep(WINDOW + 3)
    assert _running_contains(mcp_server, "description TOC-test")[0], "确认后不应被自动回滚"

    # 4) 幂等：同样行再次 push（新审批单）→ no-op 零下发
    rid2, token2 = _approve(approvals, "acc1", PUSH_LINES)
    noop = _data(call(mcp_server, "push_config", {
        "host": "acc1", "cli_lines": PUSH_LINES, "approval_id": rid2,
        "token": token2, "approved_by": "lab-tester", "rollback_seconds": WINDOW,
    }))
    assert noop["status"] == "noop"
    assert noop["applied"] == [] and len(noop["already_applied"]) == 3

    # 5) restore_snapshot 清场 → description 移除且持久化
    rid3, token3 = _approve(approvals, "acc1", [f"restore snapshot {ts}"])
    restored = _data(call(mcp_server, "restore_snapshot", {
        "host": "acc1", "ts": ts, "approval_id": rid3,
        "token": token3, "approved_by": "lab-tester",
    }))
    assert restored["status"] == "restored"
    assert "description TOC-test" in restored["removed"]
    gone, running = _running_contains(mcp_server, "description TOC-test")
    assert not gone, f"restore 后仍在: {running}"
    # 快照回放同时恢复了 eth1 原描述（覆盖语义下被 push 替换的 P2P）
    assert ORIG_ETH1_DESC in running, f"原描述未恢复: {running}"


def test_write_flow_unconfirmed_auto_rollback(lab_env):
    # 不确认：窗口（5s）到期自动回滚到快照（手写 commit-confirmed 的真机证明）
    mcp_server, approvals, device = lab_env
    _force_cleanup_acc1()
    rid, token = _approve(approvals, "acc1", PUSH_LINES)
    result = _data(call(mcp_server, "push_config", {
        "host": "acc1", "cli_lines": PUSH_LINES, "approval_id": rid,
        "token": token, "approved_by": "lab-tester", "rollback_seconds": 5,
    }))
    assert result["status"] == "awaiting_confirm"
    ts = result["snapshot_ts"]
    assert _running_contains(mcp_server, "description TOC-test")[0]
    # 等"事务完成"信号（negation+整份快照回放是约 30 条命令的慢设备 IO，
    # 以注册表移除为准，避免轮询到回滚中途的中间态），再断言最终态
    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        if ("acc1", ts) not in device.open_transactions:
            break
        time.sleep(1)
    assert ("acc1", ts) not in device.open_transactions, "120s 内事务未终结（自动回滚未完成）"
    running = _running_contains(mcp_server, "")[1]
    assert "description TOC-test" not in running, f"到期未自动回滚: {running}"
    assert ORIG_ETH1_DESC in running, f"原描述未随回滚恢复: {running}"
    assert pathlib.Path(result["snapshot_path"]).exists()
