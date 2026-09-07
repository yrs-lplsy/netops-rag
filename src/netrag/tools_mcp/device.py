"""netmiko/ncclient 设备封装层：只读命令、配置下发、快照/回滚状态机。

与任务书的**实测偏差**（lab 真机 netops/frr-ssh:10.4.3 验证，见
tests/integration/test_lab_smoke.py）：
  1. FRR 节点 root 登录 shell 即 vtysh（prompt ``acc1#``），show 命令**直接下发**，
     不用 ``vtysh -c "..."`` 包装——该包装在真机上返回 ``% Unknown command``。
  2. 本 FRR 构建仅含 mgmtd/zebra/ospfd/watchfrr/staticd，且不支持管道：
     Cisco 风格命令（show vlan / show ip interface brief / show ip arp）不存在，
     按各工具的 fallback 链回退到 FRR 原生等价命令（见 server.py 命令表）。

**commit confirmed 偏差**：FRR 无原生 ``commit confirmed``。ConfigTransaction
手写等价物：快照 running → 下发 → threading.Timer(默认 60s) 到期自动回滚
（negation + 快照整份回放 + write memory），``confirm()`` 在窗口内取消定时器并
持久化。回滚 negation 为逐行 ``no <line>`` 上下文重放（``description`` 特例为
``no description``，本 FRR 构建不接受带参 no 形式），尽力而为非字节级精确还原。
"""

from __future__ import annotations

import difflib
import logging
import re
import threading
import time
import uuid
from dataclasses import dataclass
from pathlib import Path

import netmiko
import yaml
from ncclient import manager

log = logging.getLogger(__name__)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_INVENTORY = REPO_ROOT / "deploy" / "containerlab" / "inventory.yaml"
DEFAULT_SNAPSHOT_DIR = REPO_ROOT / "data" / "snapshots"
CONNECT_TIMEOUT = 15  # 秒；netmiko/ncclient 共用

# 下发序列中"打开配置上下文"的行（回滚时对它们原样重放以恢复上下文）
_CONTEXT_OPENER = re.compile(
    r"^(interface\s+\S+|router\s+\S+|route-map\s+\S+|vrf\s+\S+|key chain\s+\S+"
    r"|(ip|ipv6)\s+access-list\s+(standard\s+|extended\s+)?\S+|bfd profile\s+\S+"
    r"|template\s+\S+|policy-map\s+\S+|class-map\s+\S+|address-family\b|line\s+\S+)"
)
_META_LINE = re.compile(r"^(Building configuration|Current configuration|end)\b")

# ping 目标白名单字符（IP/主机名）：注入串在建连前即拒
_PING_TARGET_RE = re.compile(r"^[A-Za-z0-9](?:[A-Za-z0-9.-]*[A-Za-z0-9])?$")


class DeviceError(RuntimeError):
    """设备操作失败（不可达/未知主机/状态非法）。``host`` 属性便于上层归因。"""

    def __init__(self, host: str, message: str):
        self.host = host
        super().__init__(f"[{host}] {message}")


@dataclass(frozen=True)
class NodeSpec:
    name: str
    host: str
    port: int
    username: str
    password: str
    device_type: str = "linux"
    kind: str = "cli"  # cli（netmiko）| netconf（ncclient）


def load_inventory(path: Path | str | None = None) -> dict[str, NodeSpec]:
    """读 deploy/containerlab/inventory.yaml，组字段作为节点缺省值合并。"""
    path = Path(path) if path else DEFAULT_INVENTORY
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    groups = raw.get("groups", {}) or {}
    nodes: dict[str, NodeSpec] = {}
    for name, n in (raw.get("nodes", {}) or {}).items():
        g = groups.get(n.get("group", ""), {}) or {}
        nodes[name] = NodeSpec(
            name=name,
            host=str(n["host"]),
            port=int(n["port"]),
            username=str(n.get("username", g.get("username", ""))),
            password=str(n.get("password", g.get("password", ""))),
            device_type=str(n.get("netmiko_device_type", g.get("netmiko_device_type", "linux"))),
            kind=str(n.get("kind", g.get("kind", "cli"))),
        )
    return nodes


def _new_snapshot_ts() -> str:
    return time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()) + "-" + uuid.uuid4().hex[:6]


def normalize_lines(cli_lines: list[str]) -> list[str]:
    """配置行规范化：去首尾空白，丢弃空行与 '!' 注释行，保留顺序（可含重复上下文）。"""
    out = []
    for line in cli_lines:
        s = line.strip()
        if s and s != "!":
            out.append(s)
    return out


def config_lines_from_text(text: str) -> list[str]:
    """running-config 原文 → 可回放的配置行（去包头/注释/空行/end，去缩进）。"""
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s == "!" or _META_LINE.match(s):
            continue
        out.append(s)
    return out


def running_entries(text: str) -> list[tuple[str | None, str]]:
    """解析 running-config 为 (所属顶层上下文, 行) 列表（单层缩进语义，
    FRR integrated 格式：顶层行 = 上下文，缩进行 = 上下文内叶子）。"""
    entries: list[tuple[str | None, str]] = []
    header: str | None = None
    for line in text.splitlines():
        s = line.strip()
        if not s or s == "!" or _META_LINE.match(s):
            continue
        if line[:1].isspace():
            entries.append((header, s))
        else:
            entries.append((None, s))
            header = s
    return entries


def _negate_leaf(line: str) -> str:
    if line.startswith("description"):
        return "no description"  # 本 FRR 构建实测不接受 `no description <args>`
    return f"no {line}"


def _negate_pushed_lines(lines: list[str]) -> list[str]:
    """对下发过的行构造 negation 重放序列：叶子 → no 形式；上下文行原样重入，
    上下文切换处补 exit（用户推的 exit/end 忽略，由本函数自行配对）。"""
    out: list[str] = []
    in_ctx = False
    for s in normalize_lines(lines):
        if s in ("exit", "end"):
            continue  # 上下文切换由本函数自行配对，用户推的 exit/end 不参与 negation
        if _CONTEXT_OPENER.match(s):
            if in_ctx:
                out.append("exit")
            out.append(s)
            in_ctx = True
        else:
            out.append(_negate_leaf(s))
    if in_ctx:
        out.append("exit")
    return out


def _negate_diff_entries(added: list[tuple[str | None, str]]) -> list[str]:
    """对 restore 场景（running 与快照 diff 出的新增 (上下文, 叶子)）构造 negation。"""
    out: list[str] = []
    for header, leaf in added:
        if header is not None:
            out.extend([header, _negate_leaf(leaf), "exit"])
        else:
            out.append(_negate_leaf(leaf))
    return out


class ConfigTransaction:
    """一次配置变更的事务状态机：new → ready → awaiting_confirm → confirmed/rolled_back。

    幂等：规范化后逐行与 running 比对，全部已存在 → no-op（零下发、零快照）；
    部分存在时整段**原样**下发（vtysh 配置态有上下文，跳行会把叶子落进错误上下文），
    already_applied 仅作报告字段。
    """

    def __init__(
        self,
        conn: "DeviceConnection",
        host: str,
        cli_lines: list[str],
        *,
        rollback_seconds: float = 60,
        snapshots_dir: Path | str | None = None,
        approval_id: str = "",
    ):
        self.conn = conn
        self.host = host
        self.lines = normalize_lines(cli_lines)
        self.rollback_seconds = float(rollback_seconds)
        self.snapshots_dir = Path(snapshots_dir) if snapshots_dir else conn.snapshots_dir
        self.approval_id = approval_id  # 审批绑定：confirm 时核对 (host, 事务) ↔ approval_id
        self.state = "new"
        self.snapshot_ts: str = ""
        self.snapshot_path: Path | None = None
        self.snapshot_text: str = ""
        self.applied: list[str] = []
        self.already_applied: list[str] = []
        self.output = ""
        self._timer: threading.Timer | None = None
        self._lock = threading.Lock()

    # -- 流程 ---------------------------------------------------------------

    def prepare(self) -> dict:
        running_text = self.conn.get_running_config(self.host)
        running_lines = set(config_lines_from_text(running_text))
        self.already_applied = [l for l in self.lines if l in running_lines]
        self.applied = [l for l in self.lines if l not in running_lines]
        if self.applied:
            self.snapshot_text = running_text
            self.snapshot_ts = _new_snapshot_ts()
            path = self.snapshots_dir / self.host / f"{self.snapshot_ts}.cfg"
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(running_text, encoding="utf-8")
            self.snapshot_path = path
            self.state = "ready"
        return self.report()

    def execute(self) -> dict:
        report = self.prepare()
        if not self.applied:
            self.state = "noop"
            return report | {"status": "noop",
                             "message": "全部行已存在于 running-config，no-op 未下发任何命令"}
        self.output = self.conn.run_config(self.host, self.lines)
        self.state = "awaiting_confirm"
        self._start_timer()
        return self.report() | {"status": "awaiting_confirm"}

    def confirm(self) -> dict:
        with self._lock:
            if self.state == "rolling_back":
                raise DeviceError(self.host, "回滚已在进行，无法确认")
            if self.state != "awaiting_confirm":
                raise DeviceError(self.host, f"cannot confirm in state {self.state}")
            if self._timer is not None:
                self._timer.cancel()
            self.state = "confirmed"
        persist = self.conn.persist(self.host)
        self._finish()
        return {"host": self.host, "snapshot_ts": self.snapshot_ts,
                "status": "confirmed", "persist": persist}

    # -- 定时回滚 ------------------------------------------------------------

    def _start_timer(self):
        if self.rollback_seconds <= 0:
            return  # 0 = 不设自动回滚（仅测试/显式 restore 用）
        timer = threading.Timer(self.rollback_seconds, self._on_timeout)
        timer.daemon = True
        self._timer = timer
        timer.start()

    def _on_timeout(self):
        with self._lock:
            if self.state != "awaiting_confirm":
                return
            self.state = "rolling_back"
        self.rollback()

    def rollback(self) -> dict:
        """negation 重放 + 快照整份回放 + write memory（尽力恢复到快照态）。

        设备 IO 全程兜底：异常时状态置 error、注册表照常清理（finally），
        不留悬挂事务；异常经日志记录后收敛为 error 结果返回。
        """
        try:
            negation = _negate_pushed_lines(self.lines)
            lines = negation + config_lines_from_text(self.snapshot_text)
            output = self.conn.run_config(self.host, lines)
            persist = self.conn.persist(self.host)
            with self._lock:
                if self.state != "confirmed":
                    self.state = "rolled_back"
            return {"host": self.host, "snapshot_ts": self.snapshot_ts,
                    "status": "rolled_back", "persist": persist, "output": output}
        except Exception as e:  # 回滚失败也要终结事务，不让注册表悬挂
            with self._lock:
                self.state = "error"
            log.exception("auto-rollback failed (host=%s snapshot_ts=%s)",
                          self.host, self.snapshot_ts)
            return {"host": self.host, "snapshot_ts": self.snapshot_ts,
                    "status": "error", "error": f"{type(e).__name__}: {e}"}
        finally:
            self._finish()

    def _finish(self):
        discard = getattr(self.conn, "discard_transaction", None)
        if discard is not None:
            discard(self)

    def report(self) -> dict:
        return {
            "host": self.host,
            "approval_id": self.approval_id or None,
            "already_applied": list(self.already_applied),
            "applied": list(self.applied),
            "snapshot_ts": self.snapshot_ts or None,
            "snapshot_path": str(self.snapshot_path) if self.snapshot_path else None,
            "rollback_seconds": self.rollback_seconds,
        }


class DeviceConnection:
    """设备连接门面：inventory 驱动，netmiko（cli）/ ncclient（netconf）。"""

    def __init__(
        self,
        inventory: dict[str, NodeSpec] | None = None,
        snapshots_dir: Path | str | None = None,
    ):
        self.inventory = inventory if inventory is not None else load_inventory()
        self.snapshots_dir = Path(snapshots_dir) if snapshots_dir else DEFAULT_SNAPSHOT_DIR
        self.open_transactions: dict[tuple[str, str], ConfigTransaction] = {}
        self._lock = threading.Lock()

    # -- 基础 ---------------------------------------------------------------

    def _node(self, host: str) -> NodeSpec:
        try:
            return self.inventory[host]
        except KeyError:
            raise DeviceError(host, f"unknown host; inventory has: {sorted(self.inventory)}") from None

    def _connect(self, host: str):
        node = self._node(host)
        try:
            # netmiko 无 look_for_keys 参数：use_keys=False + allow_agent=False
            # 即 paramiko look_for_keys=False 的等价禁用（禁公钥协商，纯口令）
            return netmiko.ConnectHandler(
                device_type=node.device_type,
                host=node.host,
                port=node.port,
                username=node.username,
                password=node.password,
                timeout=CONNECT_TIMEOUT,
                use_keys=False,
                allow_agent=False,
            )
        except Exception as e:  # netmiko 异常族未稳定，统一收敛
            raise DeviceError(host, f"unreachable ({type(e).__name__}: {e})") from e

    # -- 只读 ---------------------------------------------------------------

    def run_show(self, host: str, command: str) -> str:
        conn = self._connect(host)
        try:
            return conn.send_command(command, read_timeout=CONNECT_TIMEOUT * 2)
        except DeviceError:
            raise
        except Exception as e:
            raise DeviceError(host, f"show '{command}' failed ({type(e).__name__}: {e})") from e
        finally:
            conn.disconnect()

    def show_with_fallback(self, host: str, commands: list[str]) -> str:
        """依序尝试命令链，返回首个非 '%' 错误输出；全失败时返回首命令的错误原文。"""
        first_error = ""
        for cmd in commands:
            out = self.run_show(host, cmd)
            if out.lstrip().startswith("%"):
                first_error = first_error or out
                continue
            return out
        return first_error or ""

    def get_running_config(self, host: str) -> str:
        return self.run_show(host, "show running-config")

    def ping(self, host: str, target: str, seconds: int = 5) -> str:
        """vtysh ping 探测（只读）：限时收流后 ^C 截停，回收探测输出与统计。

        本构建 vtysh 的 ping 只接受 `ping <target>`，不接受 count 类参数
        （实测 `ping X -c 3` / `ping X count 3` → % Unknown command），且默认
        无限刷屏会挂死 netmiko 读循环——须主动写 Ctrl-C 触发 statistics 输出，
        读到 vtysh 提示符为止。剥掉命令回显首行与尾部提示符后返回。
        """
        t = (target or "").strip()
        if not _PING_TARGET_RE.match(t):
            raise DeviceError(host, f"非法 ping 目标: {target!r}（仅允许 IP/主机名）")
        conn = self._connect(host)
        try:
            conn.write_channel(f"ping {t}\n")
            time.sleep(max(1, min(int(seconds), 30)))  # 限时收流（探测窗口）
            conn.write_channel("\x03")  # Ctrl-C：截停无限 ping 并触发统计输出
            out = ""
            deadline = time.monotonic() + CONNECT_TIMEOUT
            while time.monotonic() < deadline:
                out += conn.read_channel()
                if out.rstrip().endswith("#"):
                    break
                time.sleep(0.2)
            out = re.sub(r"^\s*ping [^\n]*\n", "", out)  # 命令回显首行
            out = re.sub(r"\n?\S+#\s*$", "", out)  # 尾部 vtysh 提示符
            return out.strip()
        except DeviceError:
            raise
        except Exception as e:
            raise DeviceError(host, f"ping '{t}' failed ({type(e).__name__}: {e})") from e
        finally:
            conn.disconnect()

    def netconf_get(self, host: str, filter_xml: str) -> str:
        node = self._node(host)
        if node.kind != "netconf":
            raise DeviceError(host, f"not a netconf node (kind={node.kind})")
        try:
            with manager.connect(
                host=node.host,
                port=node.port,
                username=node.username,
                password=node.password,
                hostkey_verify=False,
                allow_agent=False,
                look_for_keys=False,
                timeout=CONNECT_TIMEOUT,
            ) as m:
                reply = m.get(filter=("subtree", filter_xml))
                data = reply.data_xml
                return data.decode() if isinstance(data, bytes) else str(data)
        except DeviceError:
            raise
        except Exception as e:
            raise DeviceError(host, f"netconf get failed ({type(e).__name__}: {e})") from e

    # -- 配置写路径 -----------------------------------------------------------

    def run_config(self, host: str, cli_lines: list[str]) -> str:
        """配置态下发：conf t → 逐行 → end（vtysh 登录 shell 即 CLI，直接发命令）。"""
        lines = normalize_lines(cli_lines)
        conn = self._connect(host)
        try:
            outs = [conn.send_command_timing("conf t", read_timeout=CONNECT_TIMEOUT * 2)]
            for line in lines:
                outs.append(conn.send_command_timing(line, read_timeout=CONNECT_TIMEOUT * 2))
            outs.append(conn.send_command_timing("end", read_timeout=CONNECT_TIMEOUT * 2))
            return "\n".join(o for o in outs if o and o.strip())
        except DeviceError:
            raise
        except Exception as e:
            raise DeviceError(host, f"config push failed ({type(e).__name__}: {e})") from e
        finally:
            conn.disconnect()

    def persist(self, host: str) -> dict:
        """write memory 持久化（尽力而为：失败不阻断事务，只回报 warning）。"""
        try:
            conn = self._connect(host)
        except DeviceError as e:
            return {"ok": False, "output": str(e)}
        try:
            out = conn.send_command_timing("write memory", read_timeout=CONNECT_TIMEOUT * 4)
            return {"ok": "[OK]" in out, "output": out}
        except Exception as e:
            return {"ok": False, "output": f"{type(e).__name__}: {e}"}
        finally:
            conn.disconnect()

    # -- 事务注册表 -----------------------------------------------------------

    def push(self, host: str, cli_lines: list[str], *, rollback_seconds: float = 60,
             approval_id: str = "") -> dict:
        tx = ConfigTransaction(self, host, cli_lines, rollback_seconds=rollback_seconds,
                               approval_id=approval_id)
        result = tx.execute()
        if result["status"] == "awaiting_confirm":
            with self._lock:
                self.open_transactions[(host, tx.snapshot_ts)] = tx
        return result | {"snapshot_ts": tx.snapshot_ts or None,
                         "snapshot_path": str(tx.snapshot_path) if tx.snapshot_path else None,
                         "approval_id": approval_id or None}

    def confirm_commit(self, host: str, snapshot_ts: str, approval_id: str = "") -> dict:
        tx = self.open_transactions.get((host, snapshot_ts))
        if tx is None:
            raise DeviceError(host, f"no open transaction for snapshot {snapshot_ts!r}")
        if approval_id and tx.approval_id != approval_id:
            raise DeviceError(
                host,
                f"approval_id 与事务不匹配（事务登记为 {tx.approval_id or '无'}，"
                f"请求为 {approval_id}）",
            )
        return tx.confirm()

    def discard_transaction(self, tx: ConfigTransaction):
        with self._lock:
            self.open_transactions.pop((tx.host, tx.snapshot_ts), None)

    def restore_snapshot(self, host: str, ts: str) -> dict:
        """回滚到历史快照：diff 当前 running 与快照，negation 新增叶 + 快照整份回放。"""
        path = self.snapshots_dir / host / f"{ts}.cfg"
        if not path.exists():
            raise DeviceError(host, f"snapshot not found: {path}")
        snapshot_text = path.read_text(encoding="utf-8")
        snapshot_lines = set(config_lines_from_text(snapshot_text))
        running_text = self.get_running_config(host)
        added = [(h, l) for h, l in running_entries(running_text)
                 if l not in snapshot_lines and not _CONTEXT_OPENER.match(l)
                 and not l.startswith(("frr version", "frr defaults", "hostname"))]
        negation = _negate_diff_entries(added)
        output = self.conn_run(negation + config_lines_from_text(snapshot_text), host)
        persist = self.persist(host)
        return {"host": host, "snapshot_ts": ts, "status": "restored",
                "removed": [l for _, l in added], "persist": persist, "output": output}

    def conn_run(self, lines, host):
        return self.run_config(host, lines)

    def diff_with_snapshot(self, host: str, ts: str) -> str:
        path = self.snapshots_dir / host / f"{ts}.cfg"
        if not path.exists():
            raise DeviceError(host, f"snapshot not found: {path}")
        running = config_lines_from_text(self.get_running_config(host))
        snapshot = config_lines_from_text(path.read_text(encoding="utf-8"))
        diff = "\n".join(difflib.unified_diff(
            snapshot, running,
            fromfile=f"snapshot:{ts}", tofile=f"{host}:running", lineterm="",
        ))
        return diff if diff else "no differences"
