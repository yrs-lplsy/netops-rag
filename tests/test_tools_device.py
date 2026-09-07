"""设备层单测（全 mock，不碰真机）：
netmiko/ncclient 连接参数、fallback、幂等、快照、定时回滚状态机、restore。
"""

import threading
import time
from unittest.mock import MagicMock, patch

import pytest

from netrag.tools_mcp.device import (
    ConfigTransaction,
    DeviceConnection,
    DeviceError,
    _negate_pushed_lines,
    load_inventory,
)

RUNNING_V1 = """Building configuration...

Current configuration:
!
frr version 10.4.3
hostname acc1
!
interface eth0
exit
!
interface eth1
 description P2P
 ip address 10.0.101.2/30
exit
!
router ospf
 network 10.0.101.0/30 area 0
exit
!
end
"""

RUNNING_WITH_DESC = RUNNING_V1.replace(" description P2P\n", " description P2P\n description TOC-test\n")


class FakeNetmikoConn:
    """假 netmiko 连接：按命令表回包，记录全部收到的命令。"""

    def __init__(self, show_outputs: dict[str, str], config_outputs: dict[str, str] | None = None,
                 ping_chunks: list[str] | None = None):
        self.show_outputs = show_outputs
        self.config_outputs = config_outputs or {}
        self.ping_chunks = ping_chunks or []
        self.sent_timing: list[str] = []
        self.sent_show: list[str] = []
        self.written: list[str] = []
        self.disconnected = False

    def send_command(self, cmd, **kw):
        self.sent_show.append(cmd)
        if cmd not in self.show_outputs:
            raise AssertionError(f"unexpected show cmd: {cmd}")
        return self.show_outputs[cmd]

    def send_command_timing(self, cmd, **kw):
        self.sent_timing.append(cmd)
        return self.config_outputs.get(cmd, "")

    def write_channel(self, s: str):
        self.written.append(s)

    def read_channel(self) -> str:
        return self.ping_chunks.pop(0) if self.ping_chunks else ""

    def disconnect(self):
        self.disconnected = True


@pytest.fixture()
def inv_path(tmp_path):
    p = tmp_path / "inventory.yaml"
    p.write_text(
        """
groups:
  frr: {netmiko_device_type: linux, username: root, password: root}
  netconf: {kind: netconf, username: root, password: netconf}
nodes:
  core1: {host: 127.0.0.1, port: 22022, group: frr}
  nc1: {host: 127.0.0.1, port: 21830, group: netconf}
""",
        encoding="utf-8",
    )
    return p


def wait_until(fn, timeout=5.0, step=0.02):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if fn():
            return True
        time.sleep(step)
    return False


# ---------------------------------------------------------------------------
# inventory 与连接
# ---------------------------------------------------------------------------

def test_load_inventory_resolves_groups(inv_path):
    nodes = load_inventory(inv_path)
    assert nodes["core1"].device_type == "linux"
    assert nodes["core1"].username == "root"
    assert nodes["core1"].port == 22022
    assert nodes["core1"].kind == "cli"
    assert nodes["nc1"].kind == "netconf"
    assert nodes["nc1"].password == "netconf"


def test_run_show_connection_params_and_disconnect(inv_path):
    conn = DeviceConnection(inventory=load_inventory(inv_path))
    fake = FakeNetmikoConn({"show version": "FRRouting 10.4.3"})
    with patch("netrag.tools_mcp.device.netmiko.ConnectHandler", return_value=fake) as ch:
        out = conn.run_show("core1", "show version")
    assert out == "FRRouting 10.4.3"
    kwargs = ch.call_args.kwargs
    assert kwargs["device_type"] == "linux" and kwargs["port"] == 22022
    assert kwargs["username"] == "root" and kwargs["password"] == "root"
    assert kwargs["use_keys"] is False and kwargs["allow_agent"] is False  # 禁公钥协商
    assert kwargs["timeout"] > 0
    assert fake.disconnected


def test_unreachable_host_error_shape(inv_path):
    conn = DeviceConnection(inventory=load_inventory(inv_path))
    with patch(
        "netrag.tools_mcp.device.netmiko.ConnectHandler",
        side_effect=OSError("connection refused"),
    ):
        with pytest.raises(DeviceError) as ei:
            conn.run_show("core1", "show version")
    assert "core1" in str(ei.value) and "unreachable" in str(ei.value)
    assert ei.value.host == "core1"


def test_unknown_host_error(inv_path):
    conn = DeviceConnection(inventory=load_inventory(inv_path))
    with pytest.raises(DeviceError, match="unknown host"):
        conn.run_show("nope", "show version")


def test_show_with_fallback_skips_percent_errors(inv_path):
    conn = DeviceConnection(inventory=load_inventory(inv_path))
    fake = FakeNetmikoConn(
        {
            "show vlan": "% Unknown command: show vlan",
            "show interface brief": "eth0  up  default",
        }
    )
    with patch("netrag.tools_mcp.device.netmiko.ConnectHandler", return_value=fake):
        out = conn.show_with_fallback("core1", ["show vlan", "show interface brief"])
    assert out == "eth0  up  default"
    assert fake.disconnected


def test_show_with_fallback_all_fail_returns_primary_error(inv_path):
    conn = DeviceConnection(inventory=load_inventory(inv_path))
    fake = FakeNetmikoConn({"a": "% bad a", "b": "% bad b"})
    with patch("netrag.tools_mcp.device.netmiko.ConnectHandler", return_value=fake):
        out = conn.show_with_fallback("core1", ["a", "b"])
    assert out == "% bad a"  # 保留首命令原始错误，交由上层展示


def test_ping_sends_cmd_ctrl_c_and_returns_statistics(inv_path):
    """ping 探测（只读）：发 `ping <target>` → 限时收流 → ^C 截停 → 回收统计。

    本构建 vtysh 的 ping 不接受 count 参数且默认无限刷屏（会挂死读循环），
    故必须主动 Ctrl-C 触发 statistics 输出（真机实测，见 server.py 命令表）。
    """
    conn = DeviceConnection(inventory=load_inventory(inv_path))
    fake = FakeNetmikoConn({}, ping_chunks=[
        "ping 10.0.12.2\nPING 10.0.12.2 (10.0.12.2): 56 data bytes\n",
        "64 bytes from 10.0.12.2: seq=0 ttl=64\n^C\n",
        "--- statistics ---\n0% packet loss\ncore1# ",
    ])
    with patch("netrag.tools_mcp.device.netmiko.ConnectHandler", return_value=fake):
        out = conn.ping("core1", "10.0.12.2", seconds=1)
    assert fake.written == ["ping 10.0.12.2\n", "\x03"]  # 先发命令、限时后 ^C
    assert "0% packet loss" in out
    assert not out.lstrip().startswith("ping ")  # 命令回显剥离，只留探测输出
    assert "core1#" not in out  # vtysh 提示符剥离
    assert fake.disconnected


def test_ping_rejects_unsafe_target_before_connecting(inv_path):
    """目标串只允许 IP/主机名安全字符：注入串在建连前即拒（设备层零调用）。"""
    conn = DeviceConnection(inventory=load_inventory(inv_path))
    with patch("netrag.tools_mcp.device.netmiko.ConnectHandler",
               side_effect=AssertionError("非法目标不得建连")) as ch:
        with pytest.raises(DeviceError, match="ping 目标"):
            conn.ping("core1", "10.0.12.2; rm -rf /")
    assert not ch.called


def test_run_config_wraps_conf_t_and_end(inv_path):
    conn = DeviceConnection(inventory=load_inventory(inv_path))
    fake = FakeNetmikoConn({}, {"conf t": "", "interface eth0": "", "description X": "", "end": ""})
    with patch("netrag.tools_mcp.device.netmiko.ConnectHandler", return_value=fake):
        conn.run_config("core1", ["interface eth0", "description X"])
    assert fake.sent_timing[0] == "conf t"
    assert fake.sent_timing[-1] == "end"
    assert fake.sent_timing[1:-1] == ["interface eth0", "description X"]


def test_netconf_get_params_and_filter(inv_path):
    conn = DeviceConnection(inventory=load_inventory(inv_path))
    reply = MagicMock()
    reply.data_xml = b"<data>ietf-interfaces</data>"
    mgr = MagicMock()
    mgr.__enter__.return_value.get.return_value = reply
    with patch("netrag.tools_mcp.device.manager.connect", return_value=mgr) as mc:
        out = conn.netconf_get("nc1", "<modules-state/>")
    assert "ietf-interfaces" in out
    kwargs = mc.call_args.kwargs
    assert kwargs["hostkey_verify"] is False
    assert kwargs["look_for_keys"] is False and kwargs["allow_agent"] is False
    assert mgr.__enter__.return_value.get.call_args.kwargs["filter"] == (
        "subtree",
        "<modules-state/>",
    )


def test_netconf_get_rejects_cli_node(inv_path):
    conn = DeviceConnection(inventory=load_inventory(inv_path))
    with pytest.raises(DeviceError, match="not a netconf"):
        conn.netconf_get("core1", "<x/>")


# ---------------------------------------------------------------------------
# ConfigTransaction：幂等 / 快照 / 定时回滚 / 确认
# ---------------------------------------------------------------------------

class FakeDevice:
    """假 DeviceConnection：供 ConfigTransaction 驱动。"""

    def __init__(self, running: str, tmp_path):
        self.running = running
        self.snapshots_dir = tmp_path / "snapshots"
        self.config_calls: list[tuple[str, list[str]]] = []
        self.persisted = 0

    def get_running_config(self, host):
        return self.running

    def run_config(self, host, lines):
        self.config_calls.append((host, list(lines)))
        return "ok"

    def persist(self, host):
        self.persisted += 1
        return {"ok": True, "output": "[OK]"}


@pytest.fixture()
def fake_dev(tmp_path):
    return FakeDevice(RUNNING_V1, tmp_path)


def test_push_full_idempotent_noop(fake_dev):
    tx = ConfigTransaction(
        fake_dev, "acc1", ["interface eth1", "description P2P", "exit"], rollback_seconds=0
    )
    result = tx.execute()
    assert result["status"] == "noop"
    assert result["already_applied"] == ["interface eth1", "description P2P", "exit"]
    assert result["applied"] == []
    assert fake_dev.config_calls == []  # 零写操作
    assert not list(fake_dev.snapshots_dir.rglob("*.cfg"))  # 不产生快照
    assert tx.state == "noop"


def test_push_partial_idempotency_applies_new_with_full_context(fake_dev):
    lines = ["interface eth1", "description P2P", "description TOC-test", "exit"]
    tx = ConfigTransaction(fake_dev, "acc1", lines, rollback_seconds=0)
    result = tx.execute()
    assert result["status"] == "awaiting_confirm"
    assert result["already_applied"] == ["interface eth1", "description P2P", "exit"]
    assert result["applied"] == ["description TOC-test"]
    # vtysh 配置态有上下文：整段原样下发（跳行会把叶子落到错误上下文）
    assert fake_dev.config_calls[0][1] == lines
    # 快照已写入 data/snapshots/{host}/{ts}.cfg，内容为下发生成前的 running
    assert tx.snapshot_path and tx.snapshot_path.exists()
    assert tx.snapshot_path.parent.name == "acc1"
    assert "description TOC-test" not in tx.snapshot_path.read_text(encoding="utf-8")


def test_confirm_cancels_timer(fake_dev):
    tx = ConfigTransaction(fake_dev, "acc1", ["interface eth0", "description X", "exit"],
                           rollback_seconds=0.1)
    tx.execute()
    calls_before = len(fake_dev.config_calls)
    result = tx.confirm()
    assert result["status"] == "confirmed"
    assert wait_until(lambda: time.monotonic() > 0)
    time.sleep(0.3)
    assert tx.state == "confirmed"  # 定时器未触发
    assert len(fake_dev.config_calls) == calls_before  # 确认后无回滚下发
    assert fake_dev.persisted == 1  # write memory 持久化


def test_timer_fires_auto_rollback(fake_dev):
    tx = ConfigTransaction(fake_dev, "acc1", ["interface eth1", "description TOC-test", "exit"],
                           rollback_seconds=0.1)
    tx.execute()
    assert wait_until(lambda: tx.state == "rolled_back", timeout=5)
    rollback_host, rollback_lines = fake_dev.config_calls[-1]
    assert rollback_host == "acc1"
    assert rollback_lines[:3] == ["interface eth1", "no description", "exit"]
    assert any("description P2P" in l for l in rollback_lines[3:])  # 快照内容回放
    assert fake_dev.persisted >= 1  # 回滚后持久化到快照状态


def test_confirm_after_rollback_rejected(fake_dev):
    tx = ConfigTransaction(fake_dev, "acc1", ["interface eth0", "description X"],
                           rollback_seconds=0.05)
    tx.execute()
    assert wait_until(lambda: tx.state == "rolled_back", timeout=5)
    with pytest.raises(DeviceError, match="rolled_back"):
        tx.confirm()


def test_negate_pushed_lines_context_aware():
    pushed = [
        "interface eth1", "description TOC-test", "exit",
        "router ospf", "network 10.9.0.0/30 area 0",
    ]
    negated = _negate_pushed_lines(pushed)
    # 用户推的 exit 被忽略，上下文切换处的 exit 由本函数自行配对
    assert negated == [
        "interface eth1", "no description",       # description 特例：FRR 不接受 no description <args>
        "exit", "router ospf", "no network 10.9.0.0/30 area 0", "exit",
    ]
    assert _negate_pushed_lines(["!", "", "end", "exit"]) == []


def test_push_registers_and_confirm_commit_via_connection(fake_dev):
    conn = DeviceConnection.__new__(DeviceConnection)  # 只测注册表逻辑，绕过真实 inventory
    conn.snapshots_dir = fake_dev.snapshots_dir
    conn.inventory = {"acc1": MagicMock()}
    conn.open_transactions = {}
    conn._lock = threading.Lock()
    conn.get_running_config = fake_dev.get_running_config
    conn.run_config = fake_dev.run_config
    conn.persist = fake_dev.persist

    result = conn.push("acc1", ["interface eth0", "description X", "exit"],
                       rollback_seconds=0, approval_id="req-1")
    assert result["status"] == "awaiting_confirm"
    assert result["approval_id"] == "req-1"
    ts = result["snapshot_ts"]
    assert ("acc1", ts) in conn.open_transactions
    # confirm 绑定核对：approval_id 与事务登记不一致 → 拒绝（评审 Finding 1）
    with pytest.raises(DeviceError, match="approval_id 与事务不匹配"):
        conn.confirm_commit("acc1", ts, approval_id="req-2")
    confirmed = conn.confirm_commit("acc1", ts, approval_id="req-1")
    assert confirmed["status"] == "confirmed"
    assert ("acc1", ts) not in conn.open_transactions
    with pytest.raises(DeviceError, match="no open transaction"):
        conn.confirm_commit("acc1", ts, approval_id="req-1")


def test_rollback_exception_sets_error_and_cleans_registry(fake_dev):
    """回滚设备 IO 异常兜底：状态置 error + 注册表清理，不留悬挂事务（Minor 4）。"""
    conn = DeviceConnection.__new__(DeviceConnection)
    conn.snapshots_dir = fake_dev.snapshots_dir
    conn.inventory = {"acc1": MagicMock()}
    conn.open_transactions = {}
    conn._lock = threading.Lock()
    conn.get_running_config = fake_dev.get_running_config
    conn.run_config = fake_dev.run_config
    conn.persist = fake_dev.persist

    result = conn.push("acc1", ["interface eth0", "description X"], rollback_seconds=0)
    ts = result["snapshot_ts"]

    def _boom(host, lines):
        raise OSError("ssh died")

    conn.run_config = _boom  # 回滚设备 IO 失败
    tx = conn.open_transactions[("acc1", ts)]
    rolled = tx.rollback()
    assert rolled["status"] == "error" and "ssh died" in rolled["error"]
    assert tx.state == "error"
    assert ("acc1", ts) not in conn.open_transactions  # finally 清理，无悬挂


def test_restore_snapshot_negates_added_leaves_and_reapplies(fake_dev, tmp_path):
    snap_dir = fake_dev.snapshots_dir / "acc1"
    snap_dir.mkdir(parents=True)
    (snap_dir / "20260101T000000Z-abc.cfg").write_text(RUNNING_V1, encoding="utf-8")
    fake_dev.running = RUNNING_WITH_DESC  # 当前 running 比快照多了 description TOC-test

    result = conn_restore(fake_dev, "acc1", "20260101T000000Z-abc")
    assert result["status"] == "restored"
    assert result["removed"] == ["description TOC-test"]
    host, lines = fake_dev.config_calls[-1]
    assert lines[:3] == ["interface eth1", "no description", "exit"]
    assert "description P2P" in "".join(lines[3:])  # 快照整份回放
    assert fake_dev.persisted == 1


def test_restore_snapshot_missing_file(fake_dev):
    with pytest.raises(DeviceError, match="snapshot not found"):
        conn_restore(fake_dev, "acc1", "no-such-ts")


def conn_restore(fake_dev, host, ts):
    conn = DeviceConnection.__new__(DeviceConnection)
    conn.snapshots_dir = fake_dev.snapshots_dir
    conn.inventory = {host: MagicMock()}
    conn.get_running_config = fake_dev.get_running_config
    conn.run_config = fake_dev.run_config
    conn.persist = fake_dev.persist
    return conn.restore_snapshot(host, ts)
