"""ToolsGateway 单测：fastmcp 内存 Client 直连（in-process，零子进程零网络）。

覆盖：read 返回工具文本、未知工具/工具内异常透传 ToolError、default_host 属性、
未注入 server 时懒构造真实 MCP server（仅列工具名，不触碰设备）。
"""

import pytest
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError

from netrag.tools_mcp.gateway import ToolsGateway


def _server() -> FastMCP:
    mcp = FastMCP("t")

    @mcp.tool
    def echo(host: str, tail: int = 5) -> str:
        """echo host（白名单外：仅供白名单拒绝测试用）"""
        return f"echo:{host}:{tail}"

    @mcp.tool
    def show_version(host: str) -> str:
        """白名单内工具：正常回文本"""
        return f"version:{host}"

    @mcp.tool
    def get_arp_table(host: str) -> str:
        """白名单内工具：始终失败"""
        raise RuntimeError("device down")

    return mcp


def test_read_returns_tool_text():
    gw = ToolsGateway(server=_server(), default_host="core1")
    assert gw.read("show_version", {"host": "acc1"}) == "version:acc1"


def test_read_unknown_tool_raises_tool_error():
    """白名单内但 server 未注册 → ToolError（透传语义不因白名单改变）。"""
    gw = ToolsGateway(server=_server())
    with pytest.raises(ToolError):
        gw.read("show_vlan", {})


def test_read_tool_failure_propagates_tool_error():
    gw = ToolsGateway(server=_server())
    with pytest.raises(ToolError, match="device down"):
        gw.read("get_arp_table", {"host": "x"})


def test_default_host_attribute_passthrough():
    assert ToolsGateway(server=_server(), default_host="core1").default_host == "core1"
    assert ToolsGateway(server=_server()).default_host is None


# ---------------------------------------------------------------------------
# 只读白名单（评审 Finding 2）：read 对白名单外工具名拒绝，且在建连前拒绝
# ---------------------------------------------------------------------------

def test_read_rejects_tool_outside_readonly_whitelist():
    """push_config 不在白名单 → ValueError（内存 server 上根本没有该工具：拿到
    ValueError 而非 ToolError，即证明白名单在建连之前就拒绝了）。"""
    gw = ToolsGateway(server=_server())
    with pytest.raises(ValueError, match="只读"):
        gw.read("push_config", {"host": "acc1", "cli_lines": ["description X"]})


def test_readonly_whitelist_exactly_twelve_read_tools():
    """12 只读工具：人工决策（2026-09-07）新增 show_ip_route（cost/绕路实况）
    与 ping（不通探测），与 server.py 注册一一对应；写工具仍永不入列。"""
    from netrag.tools_mcp.gateway import READONLY_TOOLS

    assert READONLY_TOOLS == frozenset({
        "get_running_config", "show_interface_status", "show_ip_interface_brief",
        "show_vlan", "show_ospf_neighbor", "show_logging", "show_version",
        "get_arp_table", "diff_config", "netconf_get",
        "show_ip_route", "ping"})
    assert "push_config" not in READONLY_TOOLS
    assert "restore_snapshot" not in READONLY_TOOLS


def test_whitelist_gates_real_write_tool_before_any_device_io():
    """真实 server 场景：restore_snapshot 是真实存在的写工具，白名单在建立
    连接前拒绝（拒绝发生在 Client 连接建立之前，设备层零调用）。"""
    gw = ToolsGateway()  # 懒构建真实 netops-devices server
    with pytest.raises(ValueError, match="restore_snapshot"):
        gw.read("restore_snapshot", {"host": "acc1", "ts": "x", "approval_id": "a",
                                     "token": "t", "approved_by": "b"})


def test_lazy_default_server_lists_real_device_tools():
    """未注入 server → 首次使用时才构建真实 MCP server（懒加载，不在 import 期）。"""
    gw = ToolsGateway()
    names = gw.list_tools()
    assert "show_ospf_neighbor" in names
    assert "push_config" in names  # 真实 server 12 工具可列（未触设备）
