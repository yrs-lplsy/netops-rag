"""FastMCP("netops-devices")：12 只读 + 2 写工具，审批门 + 幂等 + 快照回滚。

安全模型：
  - 只读工具开放调用；写工具（push_config / restore_snapshot）在触碰设备**之前**
    必须通过 approval.consume_token 校验一次性 token（先 request_approval 登记
    变更计划 → 人工 approve 发 token → 携 token 调用）。
  - FRR 无原生 commit confirmed：push 后进入回滚窗口（默认 60s，threading.Timer
    到期自动回滚到快照）；窗口内再次调用 push_config(confirm_transaction=True,
    snapshot_ts=...) 即确认（同一变更的已批准动作，无需新 token）。

命令映射按 lab 实测（FRR 10.4.3，无 vlan/arp 插件、不支持管道），每工具带
fallback 链；``vtysh -c`` 包装在真机不可用，show 命令直接下发（见 device.py 模块注释）。

运行：``python -m netrag.tools_mcp.server``（stdio transport，供 MCP client 挂载）。
"""

from __future__ import annotations

from .approval import DEFAULT_PATH as _DEFAULT_APPROVALS_PATH
from .approval import consume_token, verify_token
from .device import DEFAULT_SNAPSHOT_DIR, DeviceConnection
from fastmcp import FastMCP

SNAPSHOT_ROOT = DEFAULT_SNAPSHOT_DIR

# 只读命令表：FRR 10.4.3 实测可用的 fallback 链（% 错误自动尝试下一条）
SHOW_COMMANDS: dict[str, list[str]] = {
    "show_interface_status": ["show interface status", "show interface brief"],
    "show_ip_interface_brief": ["show ip interface brief", "show interface brief"],
    "show_vlan": ["show vlan", "show vlan brief", "show interface brief"],
    "show_ospf_neighbor": ["show ip ospf neighbor"],
    "show_logging": ["show logging"],
    "show_version": ["show version"],
    "get_arp_table": ["show ip arp", "show ip nht"],
    "show_ip_route": ["show ip route"],
}


def build_server(
    device: DeviceConnection | None = None,
    approvals_path: str | None = None,
) -> FastMCP:
    """组装 MCP server；device/approvals 可注入（测试 mock / Task 13 Agent 复用）。"""
    device = device or DeviceConnection()
    approvals_file = approvals_path or str(_DEFAULT_APPROVALS_PATH)
    mcp = FastMCP(
        "netops-devices",
        instructions=(
            "containerlab 网络设备工具链（FRR×4 + netopeer2×1）。"
            "只读工具可直接调用；写工具（push_config/restore_snapshot）受审批门保护："
            "必须先把变更计划经 request_approval（Python 侧/审批系统）登记，人工 approve "
            "取得一次性 token 后方可调用。push 后有回滚窗口，确认需在窗口内 "
            "confirm_transaction=True。"
        ),
    )

    # ------------------------------------------------------------------
    # 只读 ×12（人工决策 2026-09-07：+show_ip_route/+ping）
    # ------------------------------------------------------------------

    @mcp.tool
    def get_running_config(host: str) -> str:
        """获取设备当前 running-config 原文（FRR `show running-config`）。

        Args:
            host: inventory 中的节点名（core1/core2/acc1/acc2/nc1 中的 CLI 节点）。

        只读安全。返回 integrated 配置全文；改动设备前请先用它做 diff 依据。
        """
        return device.get_running_config(host)

    @mcp.tool
    def show_interface_status(host: str) -> str:
        """查看接口层状态表（接口/状态/VRF/地址）。

        Args:
            host: CLI 节点名。

        只读安全。FRR 构建无 `show interface status` 时自动回退
        `show interface brief`（含 up/down 与 IP 地址列）。
        """
        return device.show_with_fallback(host, SHOW_COMMANDS["show_interface_status"])

    @mcp.tool
    def show_ip_interface_brief(host: str) -> str:
        """查看三层接口摘要（IP 地址与接口 up/down 状态）。

        Args:
            host: CLI 节点名。

        只读安全。Cisco 风格命令不存在时回退 `show interface brief`。
        """
        return device.show_with_fallback(host, SHOW_COMMANDS["show_ip_interface_brief"])

    @mcp.tool
    def show_vlan(host: str) -> str:
        """查看 VLAN 信息。

        Args:
            host: CLI 节点名。

        只读安全。本 FRR 构建无 vlan 插件，`show vlan` 不存在时回退
        `show interface brief`——VLAN 以 dot1q 子接口呈现（如 eth1.100）。
        """
        return device.show_with_fallback(host, SHOW_COMMANDS["show_vlan"])

    @mcp.tool
    def show_ospf_neighbor(host: str) -> str:
        """查看 OSPF 邻居表（`show ip ospf neighbor`），排障首查。

        Args:
            host: 运行 ospfd 的 CLI 节点（core1/core2/acc1/acc2）。

        只读安全。正常拓扑每节点应有 2-3 个 Full 状态邻居；State 列非 Full
        说明邻接故障。对未运行 OSPF 的节点返回错误文本。
        """
        return device.show_with_fallback(host, SHOW_COMMANDS["show_ospf_neighbor"])

    @mcp.tool
    def show_logging(host: str, tail: int = 50) -> str:
        """查看设备日志（`show logging` 输出，取最后 tail 行）。

        Args:
            host: CLI 节点名。
            tail: 返回末尾行数，默认 50。FRR vtysh 不支持管道，尾部截取在服务端完成。

        只读安全。输出以日志配置为主，含最近日志事件（视节点日志目标而定）。
        """
        out = device.show_with_fallback(host, SHOW_COMMANDS["show_logging"])
        lines = out.splitlines()
        return "\n".join(lines[-tail:]) if tail > 0 else out

    @mcp.tool
    def show_version(host: str) -> str:
        """查看设备版本信息（FRR 版本/编译项/主机名/内核）。

        Args:
            host: CLI 节点名。

        只读安全。用于确认镜像版本与运行时长。
        """
        return device.show_with_fallback(host, SHOW_COMMANDS["show_version"])

    @mcp.tool
    def get_arp_table(host: str) -> str:
        """查看 ARP/下一跳解析表。

        Args:
            host: CLI 节点名。

        只读安全。FRR 无 `show ip arp` 时回退 `show ip nht`（zebra 下一跳表，
        含各前缀的解析 nexthop），用于判断三层可达性。
        """
        return device.show_with_fallback(host, SHOW_COMMANDS["get_arp_table"])

    @mcp.tool
    def show_ip_route(host: str) -> str:
        """查看 IPv4 路由表（`show ip route`），流量绕路/开销异常排障首查。

        Args:
            host: CLI 节点名。

        只读安全。每条路由带 [管理距离/度量]（OSPF 为 [110/cost]）：某前缀度量
        异常抬高（如 65535）或下一跳绕开直连链路，即为流量绕路的直接证据；
        结合 ping 可区分「无路由」与「有路由但不通」。
        """
        return device.show_with_fallback(host, SHOW_COMMANDS["show_ip_route"])

    @mcp.tool
    def ping(host: str, target: str, seconds: int = 5) -> str:
        """从设备向目标发 ICMP 探测（vtysh `ping <target>`），判断三层可达性。

        Args:
            host: CLI 节点名。
            target: 目标地址（点分十进制 IPv4 或主机名，只允许安全字符）。
            seconds: 探测窗口秒数，默认 5（本构建 vtysh ping 不支持 count 参数，
                服务端限时后 ^C 截停并回收统计，避免无限 ping 挂起会话）。

        只读安全。返回逐包回显与末尾 statistics（丢包率/往返时延）；全超时说明
        源到目标三层不通，结合 show_ip_route 可定位是「无路由」还是「有路由不通」。
        """
        return device.ping(host, target, seconds=seconds)

    @mcp.tool
    def diff_config(host: str, snapshot_ts: str) -> str:
        """对比指定历史快照与当前 running-config 的 unified diff。

        Args:
            host: CLI 节点名。
            snapshot_ts: 快照时间戳（data/snapshots/{host}/{ts}.cfg，来自
                push_config 返回值或目录列表）。

        只读安全。无差异返回 "no differences"；回滚评估时先用它预览影响面。
        """
        return device.diff_with_snapshot(host, snapshot_ts)

    @mcp.tool
    def netconf_get(host: str, filter_xml: str) -> str:
        """NETCONF `<get>` 查询（ncclient，仅 netconf 节点 nc1）。

        Args:
            host: 必须为 netconf 节点 nc1（端口 830）。
            filter_xml: subtree 过滤器 XML，例如
                '<modules-state xmlns="urn:ietf:params:xml:ns:yang:ietf-yang-library"/>'
                或 '<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces"/>'。

        只读安全。返回 reply.data_xml 原文；非 netconf 节点报错。
        """
        return device.netconf_get(host, filter_xml)

    # ------------------------------------------------------------------
    # 写 ×2（审批门）
    # ------------------------------------------------------------------

    @mcp.tool
    def push_config(
        host: str,
        cli_lines: list[str],
        approval_id: str,
        token: str,
        approved_by: str,
        rollback_seconds: int = 60,
        confirm_transaction: bool = False,
        snapshot_ts: str = "",
    ) -> dict:
        """向设备下发配置变更（写操作，需审批 token；FRR 版 commit-confirmed 流程）。

        ⚠️ 调用前必须完成审批：request_approval(host, cli_lines) 登记计划 →
        人工 approve 取得一次性 token。token 与登记的 (host, 变更计划) 强绑定，
        host 或 cli_lines 与审批单不一致即拒绝；无有效 token 本工具拒绝执行
        （token 校验先于任何设备操作）。

        正常变更流程（confirm_transaction=False）：
          1. 幂等检查：cli_lines 规范化后逐行与 running 比对，全部已存在 → no-op
             （零下发）；部分存在 → 整段原样下发并报告 already_applied/applied。
          2. 快照 running 到 data/snapshots/{host}/{ts}.cfg。
          3. conf t 下发 cli_lines（vtysh 配置态，含上下文行请一并给出，如
             ["interface eth0", "description X", "exit"]）→ end。
          4. 进入回滚窗口 rollback_seconds（默认 60s）：到期自动回滚到快照。
          5. 验证无误后在窗口内**再次调用本工具**：
             confirm_transaction=True, snapshot_ts=<返回值>, 其余审批参数同前
             （确认属于同一已批准变更，不消耗新 token）→ write memory 持久化。

        Args:
            host: CLI 节点名。
            cli_lines: FRR vtysh 配置行（含上下文行，按序）。
            approval_id: 审批单 ID。
            token: 一次性审批 token（明文仅在 approve 返回值出现一次）。
            approved_by: 审批人标识，审计用，必填非空。
            rollback_seconds: 回滚窗口秒数，默认 60；0 表示不自动回滚（慎用）。
            confirm_transaction: True 时仅执行窗口确认（需 snapshot_ts）。
            snapshot_ts: confirm_transaction=True 时指定要确认的事务。

        Returns:
            dict：status（noop/awaiting_confirm/confirmed）、already_applied、
            applied、snapshot_ts、snapshot_path、rollback_seconds、persist 等。
        """
        if not approved_by or not approved_by.strip():
            raise ValueError("approved_by 必填：写操作必须记录审批人")
        if confirm_transaction:
            # 确认属于同一已批准变更：token/host 绑定核对通过即可（不重复消费）；
            # (approval_id ↔ 事务) 的匹配由 device.confirm_commit 核对
            if not verify_token(approval_id, token, path=approvals_file, expected_host=host):
                raise PermissionError(
                    f"审批门拒绝：approval_id={approval_id} 与 token 不匹配、"
                    f"未批准或非 host={host} 的审批单"
                )
            return device.confirm_commit(host, snapshot_ts, approval_id)
        # token 与登记的 (host, planned_lines) 强绑定：A 设备的审批单不能用于
        # B 设备，登记计划与实际下发行不一致即拒绝（核对先于任何设备操作）
        if not consume_token(approval_id, token, path=approvals_file,
                             expected_host=host, expected_lines=cli_lines):
            raise PermissionError(
                f"审批门拒绝：approval_id={approval_id} 的 token 无效、已消费，"
                "或与该审批单登记的 host/变更计划不一致；写操作需先 "
                "request_approval(host, cli_lines) → 人工 approve 获取一次性 token"
            )
        result = device.push(host, cli_lines, rollback_seconds=rollback_seconds,
                             approval_id=approval_id)
        result["approved_by"] = approved_by
        result["approval_id"] = approval_id
        if result.get("status") == "awaiting_confirm":
            result["message"] = (
                f"变更已下发，{rollback_seconds}s 后自动回滚；确认请再次调用本工具："
                f"confirm_transaction=True, snapshot_ts={result['snapshot_ts']}"
            )
        return result

    @mcp.tool
    def restore_snapshot(
        host: str, ts: str, approval_id: str, token: str, approved_by: str
    ) -> dict:
        """把设备回滚到历史快照状态（写操作，需审批 token）。

        语义：diff 当前 running 与快照，negation 掉新增行（含上下文重放）后整份
        回放快照，并 write memory——尽力恢复到快照时刻状态（行级 negation，
        非字节级精确还原）。快照来自 data/snapshots/{host}/{ts}.cfg。

        ⚠️ 需审批：request_approval(host, ["restore snapshot " + ts]) → approve →
        携 token 调用。建议先调用 diff_config 预览差异。

        Args:
            host: CLI 节点名。
            ts: 快照时间戳（push_config 返回值或快照目录名）。
            approval_id: 审批单 ID。
            token: 一次性审批 token。
            approved_by: 审批人标识，必填非空。

        Returns:
            dict：status=restored、removed（被 negation 的行）、persist、output。
        """
        if not approved_by or not approved_by.strip():
            raise ValueError("approved_by 必填：写操作必须记录审批人")
        # 审批绑定核对：token 必须属于该 host 的审批单（先于任何设备操作）
        if not consume_token(approval_id, token, path=approvals_file, expected_host=host):
            raise PermissionError(
                f"审批门拒绝：approval_id={approval_id} 的 token 无效、已消费，"
                f"或非 host={host} 的审批单"
            )
        return device.restore_snapshot(host, ts)

    return mcp


mcp = build_server()

if __name__ == "__main__":
    mcp.run(transport="stdio")
