"""审批门：写操作必须先 request → 人工 approve 发一次性 token → 工具 consume。

存储为 JSONL 追加式审计日志（data/approvals.jsonl，gitignore）：
每条记录一行，同一 approval_id 多条记录时"最后一条有效记录"为当前状态，
旧记录保留作审计链。token 只存 sha256 哈希，明文仅在 approve 返回值出现一次。

安全绑定：token 与登记时的 (host, planned_lines) 绑定——consume/verify 可选
传入 expected_host/expected_lines（规范化后比对），不匹配即拒绝，防止把
A 设备良性变更的 token 拿去 B 设备执行任意计划。读改写全程 fcntl.flock
互斥（跨线程/进程），并发双花不可能。仅支持 POSIX（fcntl）。"""

from __future__ import annotations

import contextlib
import fcntl
import hashlib
import json
import secrets
import uuid
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_PATH = REPO_ROOT / "data" / "approvals.jsonl"


def _resolve(path: Path | str | None) -> Path:
    return Path(path) if path else DEFAULT_PATH


def _normalize_lines(lines: list[str]) -> list[str]:
    """与 device.normalize_lines 语义一致（strip、去空行/!）；此处复制一份
    保持 approval 层不依赖 device 层（避免拖入 netmiko/ncclient）。"""
    out = []
    for line in lines or []:
        s = str(line).strip()
        if s and s != "!":
            out.append(s)
    return out


def _lines_match(record_lines: list, planned_lines: list[str] | None) -> bool:
    if planned_lines is None:
        return True
    return _normalize_lines(record_lines) == _normalize_lines(planned_lines)


@contextlib.contextmanager
def _exclusive(path: Path):
    """fcntl.flock 互斥：consume 的读-校验-写全程持锁（跨线程/进程串行化）。"""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)


def _append(record: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def _load(path: Path) -> dict[str, dict]:
    """读全部记录；坏行跳过（容错不修复，保留现场），同 id 后写覆盖先写。"""
    if not path.exists():
        return {}
    latest: dict[str, dict] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(rec, dict) and rec.get("approval_id"):
            latest[rec["approval_id"]] = rec
    return latest


def _now_ts() -> str:
    from datetime import datetime, timezone

    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def request_approval(
    host: str,
    planned_lines: list[str],
    *,
    requested_by: str = "agent",
    path: Path | str | None = None,
) -> str:
    """登记一条待审批变更计划，返回 approval_id（后续 approve/consume 用）。"""
    approval_id = uuid.uuid4().hex[:12]
    _append(
        {
            "approval_id": approval_id,
            "host": host,
            "planned_lines": list(planned_lines),
            "requested_by": requested_by,
            "status": "pending",
            "ts": _now_ts(),
        },
        _resolve(path),
    )
    return approval_id


def approve(approval_id: str, approver: str, *, path: Path | str | None = None) -> str:
    """人工批准：返回一次性明文 token（仅此一次；落盘只有 sha256 哈希）。

    重复 approve 会轮换 token（旧 token 随旧记录被覆盖而失效）。
    """
    p = _resolve(path)
    rec = _load(p).get(approval_id)
    if rec is None:
        raise ValueError(f"unknown approval_id: {approval_id}")
    token = secrets.token_urlsafe(24)
    _append(
        {
            **rec,
            "status": "approved",
            "approver": approver,
            "token_hash": hashlib.sha256(token.encode()).hexdigest(),
            "approved_ts": _now_ts(),
        },
        p,
    )
    return token


def consume_token(
    approval_id: str,
    token: str,
    *,
    path: Path | str | None = None,
    expected_host: str | None = None,
    expected_lines: list[str] | None = None,
) -> bool:
    """校验并消费一次性 token：仅 status=approved 且哈希匹配且未消费 → True。

    expected_host/expected_lines 给定时强绑定核对（规范化后比对 planned_lines），
    任一不匹配 → False 且**不消费**（token 仍可被正确请求使用）。
    读-校验-写全程 fcntl.flock 互斥，并发调用恰有一方成功。
    """
    p = _resolve(path)
    with _exclusive(p):
        rec = _load(p).get(approval_id)
        if rec is None or rec.get("status") != "approved":
            return False
        if hashlib.sha256(token.encode()).hexdigest() != rec.get("token_hash"):
            return False
        if expected_host is not None and rec.get("host") != expected_host:
            return False
        if not _lines_match(rec.get("planned_lines", []), expected_lines):
            return False
        _append({**rec, "status": "consumed", "consumed_ts": _now_ts()}, p)
        return True


def verify_token(
    approval_id: str,
    token: str,
    *,
    path: Path | str | None = None,
    expected_host: str | None = None,
    expected_lines: list[str] | None = None,
) -> bool:
    """只校验不消费：token 与已批准记录哈希匹配（approved/consumed 均可）→ True。

    供"同一已批准变更的后续动作"复用（如 push 后窗口内 confirm_transaction），
    避免确认被审批门误拒，也不产生双花。expected_host/expected_lines 同
    consume_token 的绑定核对。
    """
    p = _resolve(path)
    with _exclusive(p):
        rec = _load(p).get(approval_id)
        if rec is None or rec.get("status") not in ("approved", "consumed"):
            return False
        if hashlib.sha256(token.encode()).hexdigest() != rec.get("token_hash"):
            return False
        if expected_host is not None and rec.get("host") != expected_host:
            return False
        return _lines_match(rec.get("planned_lines", []), expected_lines)


def get(approval_id: str, *, path: Path | str | None = None) -> dict:
    rec = _load(_resolve(path)).get(approval_id)
    if rec is None:
        raise ValueError(f"unknown approval_id: {approval_id}")
    return rec
