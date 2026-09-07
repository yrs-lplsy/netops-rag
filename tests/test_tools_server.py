"""FastMCP server 单测：fastmcp 内存 Client 直连，device 层全 mock。

覆盖：14 工具注册、只读工具透传、写工具审批门（无/错/重复 token 拒绝、
合法 token 走事务、confirm_transaction 路径）、approved_by 必填。
"""

import asyncio
import json
from pathlib import Path

import pytest
from fastmcp import Client
from fastmcp.exceptions import ToolError

from netrag.tools_mcp import approval
from netrag.tools_mcp.device import DeviceError
from netrag.tools_mcp.server import build_server

EXPECTED_TOOLS = {
    "get_running_config", "show_interface_status", "show_ip_interface_brief",
    "show_vlan", "show_ospf_neighbor", "show_logging", "show_version",
    "get_arp_table", "diff_config", "netconf_get", "push_config", "restore_snapshot",
    # 人工决策（2026-09-07）：+show_ip_route（cost/绕路实况）、+ping（不通探测）
    "show_ip_route", "ping",
}

LOG_OUTPUT = "\n".join(f"log line {i}" for i in range(100))


class FakeDevice:
    def __init__(self):
        self.push_calls = []
        self.confirm_calls = []
        self.restore_calls = []
        self.ping_calls = []
        self._tx_approval_id = ""  # 最近一次 push 登记的 approval_id
        self.push_result = {
            "host": "acc1", "status": "awaiting_confirm",
            "already_applied": [], "applied": ["interface eth0", "description X"],
            "snapshot_ts": "20260101T000000Z-abc123", "snapshot_path": "/tmp/x.cfg",
            "rollback_seconds": 60,
        }

    def get_running_config(self, host):
        return f"hostname {host}\n!"

    def show_with_fallback(self, host, commands):
        if commands == ["show logging"]:
            return LOG_OUTPUT
        if commands == ["show ip route"]:
            return "O>* 10.0.12.0/30 [110/65535] via 10.0.12.2"
        return "fake output"

    def ping(self, host, target, seconds=5):
        self.ping_calls.append((host, target, seconds))
        return f"--- {target} ping statistics ---\n0% packet loss"

    def netconf_get(self, host, filter_xml):
        return f"<data from={host}>{filter_xml}</data>"

    def diff_with_snapshot(self, host, ts):
        return f"--- snapshot:{ts}\n+++ {host}:running"

    def push(self, host, cli_lines, *, rollback_seconds=60, approval_id=""):
        self.push_calls.append((host, list(cli_lines), rollback_seconds, approval_id))
        self._tx_approval_id = approval_id  # 模拟事务登记 approval_id
        return dict(self.push_result, rollback_seconds=rollback_seconds,
                    approval_id=approval_id or None)

    def confirm_commit(self, host, snapshot_ts, approval_id=""):
        # 模拟真实现：事务登记的 approval_id 不匹配即拒绝（评审 Finding 1）
        if approval_id and self._tx_approval_id and approval_id != self._tx_approval_id:
            raise DeviceError(host, f"approval_id 与事务不匹配（事务登记为 {self._tx_approval_id}）")
        self.confirm_calls.append((host, snapshot_ts, approval_id))
        return {"host": host, "snapshot_ts": snapshot_ts, "status": "confirmed",
                "persist": {"ok": True, "output": "[OK]"}}

    def restore_snapshot(self, host, ts):
        self.restore_calls.append((host, ts))
        return {"host": host, "snapshot_ts": ts, "status": "restored", "removed": []}


@pytest.fixture()
def fake_dev():
    return FakeDevice()


@pytest.fixture()
def approvals(tmp_path):
    return tmp_path / "approvals.jsonl"


@pytest.fixture()
def server(fake_dev, approvals):
    return build_server(device=fake_dev, approvals_path=str(approvals))


def call(server, tool, args):
    async def _run():
        async with Client(server) as client:
            return await client.call_tool(tool, args)

    return asyncio.run(_run())


def list_names(server):
    async def _run():
        async with Client(server) as client:
            return {t.name for t in await client.list_tools()}

    return asyncio.run(_run())


def test_registers_exactly_14_tools(server):
    """12 只读 + 2 写；+show_ip_route/ping 为人工决策（2026-09-07），写面不变。"""
    names = list_names(server)
    assert names == EXPECTED_TOOLS
    assert len(names) == 14


def test_read_tool_returns_mocked_output(server, fake_dev):
    result = call(server, "get_running_config", {"host": "acc1"})
    assert "hostname acc1" in result.content[0].text


def test_show_logging_tails_server_side(server, fake_dev):
    result = call(server, "show_logging", {"host": "core1", "tail": 5})
    lines = result.content[0].text.splitlines()
    assert lines == [f"log line {i}" for i in range(95, 100)]


def test_netconf_get_passthrough(server, fake_dev):
    result = call(server, "netconf_get", {"host": "nc1", "filter_xml": "<x/>"})
    assert "<data from=nc1><x/></data>" in result.content[0].text


def test_show_ip_route_passthrough(server, fake_dev):
    """路由表只读透传：cost/绕路类实况问题的诊断证据面（[110/cost] 直接可见）。"""
    result = call(server, "show_ip_route", {"host": "core1"})
    assert "[110/65535]" in result.content[0].text


def test_ping_passthrough_with_target(server, fake_dev):
    """ping 只读透传：target 必填参数原样下发，返回统计文本。"""
    result = call(server, "ping", {"host": "core1", "target": "10.0.12.2"})
    assert "0% packet loss" in result.content[0].text
    assert fake_dev.ping_calls == [("core1", "10.0.12.2", 5)]


def test_diff_config_passthrough(server, fake_dev):
    result = call(server, "diff_config", {"host": "acc1", "snapshot_ts": "ts1"})
    assert "snapshot:ts1" in result.content[0].text


def test_push_without_token_rejected_before_device(server, fake_dev, approvals):
    rid = approval.request_approval("acc1", ["description X"], path=approvals)
    with pytest.raises(ToolError, match="审批门拒绝"):
        call(server, "push_config", {
            "host": "acc1", "cli_lines": ["description X"], "approval_id": rid,
            "token": "forged", "approved_by": "ops",
        })
    assert fake_dev.push_calls == []  # 设备未被触碰


def test_push_with_valid_token_runs_transaction(server, fake_dev, approvals):
    rid = approval.request_approval("acc1", ["interface eth0", "description X"], path=approvals)
    token = approval.approve(rid, "ops-admin", path=approvals)
    result = call(server, "push_config", {
        "host": "acc1", "cli_lines": ["interface eth0", "description X"],
        "approval_id": rid, "token": token, "approved_by": "ops-admin",
        "rollback_seconds": 15,
    })
    assert fake_dev.push_calls == [("acc1", ["interface eth0", "description X"], 15, rid)]
    data = json.loads(result.content[0].text)
    assert data["status"] == "awaiting_confirm"
    assert data["snapshot_ts"] == "20260101T000000Z-abc123"
    assert data["approved_by"] == "ops-admin"
    assert "confirm_transaction=True" in data["message"]


def test_token_one_time_second_push_rejected(server, fake_dev, approvals):
    rid = approval.request_approval("acc1", ["description X"], path=approvals)
    token = approval.approve(rid, "ops", path=approvals)
    call(server, "push_config", {
        "host": "acc1", "cli_lines": ["description X"], "approval_id": rid,
        "token": token, "approved_by": "ops",
    })
    with pytest.raises(ToolError, match="审批门拒绝"):
        call(server, "push_config", {
            "host": "acc1", "cli_lines": ["description Y"], "approval_id": rid,
            "token": token, "approved_by": "ops",
        })
    assert len(fake_dev.push_calls) == 1


def test_push_confirm_transaction_path(server, fake_dev, approvals):
    rid = approval.request_approval("acc1", ["!"], path=approvals)
    token = approval.approve(rid, "ops", path=approvals)
    result = call(server, "push_config", {
        "host": "acc1", "cli_lines": ["!"], "approval_id": rid, "token": token,
        "approved_by": "ops", "confirm_transaction": True,
        "snapshot_ts": "20260101T000000Z-abc123",
    })
    data = json.loads(result.content[0].text)
    assert data["status"] == "confirmed"
    assert fake_dev.confirm_calls == [("acc1", "20260101T000000Z-abc123", rid)]
    assert fake_dev.push_calls == []  # 确认路径不下发新配置


def test_push_rejects_host_mismatch_binding(server, fake_dev, approvals):
    """acc1 的审批 token 拿去 core1 → 拒绝且设备未被触碰（评审 Finding 1）。"""
    rid = approval.request_approval("acc1", ["description benign"], path=approvals)
    token = approval.approve(rid, "ops", path=approvals)
    with pytest.raises(ToolError, match="审批门拒绝"):
        call(server, "push_config", {
            "host": "core1", "cli_lines": ["description benign"],
            "approval_id": rid, "token": token, "approved_by": "ops",
        })
    assert fake_dev.push_calls == []
    # token 未被误烧：对正确 host 仍可用
    result = call(server, "push_config", {
        "host": "acc1", "cli_lines": ["description benign"],
        "approval_id": rid, "token": token, "approved_by": "ops",
    })
    assert json.loads(result.content[0].text)["status"] == "awaiting_confirm"


def test_push_rejects_planned_lines_mismatch(server, fake_dev, approvals):
    """登记良性计划、实际下发危险计划 → 拒绝且设备未被触碰（评审 Finding 1）。"""
    rid = approval.request_approval("acc1", ["description benign"], path=approvals)
    token = approval.approve(rid, "ops", path=approvals)
    with pytest.raises(ToolError, match="审批门拒绝"):
        call(server, "push_config", {
            "host": "acc1", "cli_lines": ["no router ospf"],
            "approval_id": rid, "token": token, "approved_by": "ops",
        })
    assert fake_dev.push_calls == []
    assert approval.get(rid, path=approvals)["status"] == "approved"  # 未被消费


def test_confirm_with_unregistered_approval_id_rejected(server, fake_dev, approvals):
    """confirm 的 (approval_id, token) 必须与事务登记一致（评审 Finding 1）。"""
    rid = approval.request_approval("acc1", ["!"], path=approvals)
    token = approval.approve(rid, "ops", path=approvals)
    call(server, "push_config", {
        "host": "acc1", "cli_lines": ["!"], "approval_id": rid, "token": token,
        "approved_by": "ops",
    })
    # 用另一张审批单（哪怕合法）确认该事务 → 拒绝
    rid2 = approval.request_approval("acc1", ["!"], path=approvals)
    token2 = approval.approve(rid2, "ops", path=approvals)
    with pytest.raises(ToolError, match="审批门拒绝|approval_id 与事务不匹配"):
        call(server, "push_config", {
            "host": "acc1", "cli_lines": ["!"], "approval_id": rid2, "token": token2,
            "approved_by": "ops", "confirm_transaction": True,
            "snapshot_ts": "20260101T000000Z-abc123",
        })
    assert fake_dev.confirm_calls == []
    # 换回事务登记的 approval_id（token 已消费仍可 verify）→ 通过
    result = call(server, "push_config", {
        "host": "acc1", "cli_lines": ["!"], "approval_id": rid, "token": token,
        "approved_by": "ops", "confirm_transaction": True,
        "snapshot_ts": "20260101T000000Z-abc123",
    })
    assert json.loads(result.content[0].text)["status"] == "confirmed"


def test_confirm_reuses_same_consumed_token(server, fake_dev, approvals):
    """同一变更：push 消费 token 后，窗口内 confirm 复用同一 token 通过（不双花）。"""
    rid = approval.request_approval("acc1", ["!"], path=approvals)
    token = approval.approve(rid, "ops", path=approvals)
    call(server, "push_config", {
        "host": "acc1", "cli_lines": ["!"], "approval_id": rid, "token": token,
        "approved_by": "ops",
    })
    assert len(fake_dev.push_calls) == 1  # token 已被 push 消费
    result = call(server, "push_config", {
        "host": "acc1", "cli_lines": ["!"], "approval_id": rid, "token": token,
        "approved_by": "ops", "confirm_transaction": True,
        "snapshot_ts": "20260101T000000Z-abc123",
    })
    assert json.loads(result.content[0].text)["status"] == "confirmed"
    # 但同一 token 无法再次走 push（一次性语义不破）
    with pytest.raises(ToolError, match="审批门拒绝"):
        call(server, "push_config", {
            "host": "acc1", "cli_lines": ["!"], "approval_id": rid, "token": token,
            "approved_by": "ops",
        })


def test_approved_by_required(server, fake_dev, approvals):
    rid = approval.request_approval("acc1", ["!"], path=approvals)
    token = approval.approve(rid, "ops", path=approvals)
    with pytest.raises(ToolError, match="approved_by"):
        call(server, "push_config", {
            "host": "acc1", "cli_lines": ["!"], "approval_id": rid,
            "token": token, "approved_by": "  ",
        })
    assert fake_dev.push_calls == []


def test_restore_snapshot_requires_token(server, fake_dev, approvals):
    with pytest.raises(ToolError, match="审批门拒绝"):
        call(server, "restore_snapshot", {
            "host": "acc1", "ts": "ts1", "approval_id": "x",
            "token": "y", "approved_by": "ops",
        })
    assert fake_dev.restore_calls == []
    rid = approval.request_approval("acc1", ["restore snapshot ts1"], path=approvals)
    token = approval.approve(rid, "ops", path=approvals)
    result = call(server, "restore_snapshot", {
        "host": "acc1", "ts": "ts1", "approval_id": rid,
        "token": token, "approved_by": "ops",
    })
    assert fake_dev.restore_calls == [("acc1", "ts1")]
    data = json.loads(result.content[0].text)
    assert data["status"] == "restored"


def test_device_error_surfaces_host(server, fake_dev, approvals):
    def boom(host, ts):
        raise DeviceError(host, "snapshot not found: /x")
    fake_dev.diff_with_snapshot = boom
    with pytest.raises(ToolError, match=r"\[acc1\]"):
        call(server, "diff_config", {"host": "acc1", "snapshot_ts": "ts1"})
