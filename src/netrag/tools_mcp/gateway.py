"""ToolsGateway：Agent 侧 MCP 工具薄网关（read → fastmcp 内存 Client）。

设计（Task 13 Part A）：
- CRAG 的 diagnose 节点只依赖本网关的 ``read`` 接口（测试 mock 网关，绝不 mock
  fastmcp 内部）；真实实现用 fastmcp 内存传输 ``Client(server)`` 直连 server
  对象——零子进程、零端口，与 API 侧同进程构造。
- 只封装只读工具（``read``，白名单 READONLY_TOOLS 强制）；写工具（
  push_config/restore_snapshot）不经过本网关——写路径必须走审批门
  （approval.py + server 写工具），且 Task 13 的 Agent 图只在 diagnose 节点
  消费实况，永不自动下发配置。
- 每次调用独立开合 Client 连接：内存传输开销可忽略，且规避事件循环亲和性
  （langgraph 节点/FastAPI 线程池 worker 各自 asyncio.run，无跨 loop 复用问题）。
  因此本类方法必须在**同步上下文**调用（langgraph 节点、FastAPI def 端点均满足）。
- 工具内异常透传为 fastmcp 的 ToolError，由调用方（diagnose 节点）兜底——
  网关不做吞异常的降级，保证测试里异常语义可断言。
"""

from __future__ import annotations

import asyncio
from typing import Any

# 只读白名单（评审 Finding 2）：网关是 Agent 可编程面，裸透传意味着任何上游
# 逻辑失误都能经它下发 push_config/restore_snapshot。写工具永不经过网关——
# 写路径唯一入口是审批门（approval.py）+ 显式携一次性 token 的 MCP 写工具调用，
# 由人工/运维侧执行。名单与 server.py 的 12 个只读工具一一对应（人工决策
# 2026-09-07：+show_ip_route/ping，服务 cost/绕路与不通类实况问题的诊断映射）。
READONLY_TOOLS = frozenset({
    "get_running_config", "show_interface_status", "show_ip_interface_brief",
    "show_vlan", "show_ospf_neighbor", "show_logging", "show_version",
    "get_arp_table", "diff_config", "netconf_get", "show_ip_route", "ping",
})


class ToolsGateway:
    """``gateway.read(tool_name, args_dict) -> str``：只读工具的唯一入口。

    server=None 时**懒**构建真实 MCP server（首次使用才 import netmiko 栈并
    读 inventory），保证 import 期零副作用；测试注入内存 FastMCP 即可。
    default_host：问题里提取不到主机名时诊断调用的缺省节点（可为 None）。
    """

    def __init__(self, server: Any | None = None, default_host: str | None = None):
        self._server = server
        self.default_host = default_host

    def _server_obj(self) -> Any:
        if self._server is None:
            from netrag.tools_mcp.server import build_server

            self._server = build_server()
        return self._server

    def read(self, tool_name: str, args: dict | None = None) -> str:
        """同步调用只读 MCP 工具并返回首个文本 content（无 content → 空串）。

        白名单校验先于建立任何连接（写工具名直接 ValueError，设备层零调用）。
        """
        if tool_name not in READONLY_TOOLS:
            raise ValueError(
                f"拒绝调用 {tool_name!r}：网关只读白名单外（写操作必须走审批门 + "
                f"携一次性 token 显式调用 MCP 写工具，不经网关）；白名单："
                f"{sorted(READONLY_TOOLS)}")

        async def _run() -> str:
            from fastmcp import Client

            async with Client(self._server_obj()) as client:
                result = await client.call_tool(tool_name, args or {})
                if not result.content:
                    return ""
                return result.content[0].text

        return asyncio.run(_run())

    def list_tools(self) -> list[str]:
        """列出 server 已注册工具名（诊断/自检用，不触设备）。"""

        async def _run() -> list[str]:
            from fastmcp import Client

            async with Client(self._server_obj()) as client:
                tools = await client.list_tools()
                return sorted(t.name for t in tools)

        return asyncio.run(_run())
