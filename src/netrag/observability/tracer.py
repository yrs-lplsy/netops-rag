"""可插拔 Tracer：trace → span（可嵌套）→ event 三层观测。

- JsonlTracer：本地兜底。每条 trace/span/event 追加一行 JSON 到同一文件
  （iso 时间戳 + latency_ms + meta + trace/span 关联 id），便于离线 grep/jq 复盘。
  IO 失败一律吞掉只记 stderr——观测绝不拖垮主流程。
- LangfuseTracer：映射到 langfuse SDK（懒导入，缺 SDK/初始化失败在构造时抛出，
  由 get_tracer 降级到 JSONL）；trace 退出时 flush；SDK 运行期异常同样只记 stderr。
- get_tracer：Settings 里有 Langfuse 密钥 → LangfuseTracer，否则
  JsonlTracer(data/traces/<时间戳>-<run_name>.jsonl)。
"""

from __future__ import annotations

import datetime as _dt
import importlib
import json
import re
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Protocol

from netrag.config import Settings


def _now_iso() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="milliseconds")


def _note(msg: str) -> None:
    print(f"[tracer] {msg}", file=sys.stderr)


# ---------------------------------------------------------------------------
# 协议（结构化鸭子类型，供调用方做类型标注）
# ---------------------------------------------------------------------------

class Span(Protocol):
    """span 句柄：记录起止（latency）、meta 与嵌套事件。"""

    def event(self, name: str, **kv: Any) -> None: ...

    def __enter__(self) -> "Span": ...

    def __exit__(self, exc_type, exc, tb) -> None: ...


class Trace(Span, Protocol):
    """trace 句柄：本身是上下文管理器，可开嵌套 span 与直接打事件。"""

    def span(self, name: str, meta: dict | None = None) -> Span: ...


class Tracer(Protocol):
    """可插拔 Tracer 协议：Langfuse / JSONL（或其他后续实现）二选一。"""

    def trace(self, name: str, meta: dict | None = None) -> Trace: ...


# ---------------------------------------------------------------------------
# JSONL 实现
# ---------------------------------------------------------------------------

class _JsonlEmitter:
    """追加式 JSONL 写入器：一行一记录，任何 IO 失败吞掉只记 stderr。"""

    def __init__(self, path: Path):
        self._path = Path(path)

    @property
    def path(self) -> Path:
        return self._path

    def emit(self, record: dict) -> None:
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            with self._path.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        except Exception as exc:  # noqa: BLE001 — best-effort，观测不上抛
            _note(f"jsonl 写入失败（忽略）：{exc}")


class _JsonlNode:
    """trace/span 共用实现：进入返回自身，退出写一行（含 latency_ms）。"""

    kind = "span"

    def __init__(self, emitter: _JsonlEmitter, name: str, meta: dict | None,
                 trace_id: str, span_id: str | None, parent_id: str | None):
        self._emitter = emitter
        self.name = name
        self._meta = dict(meta or {})
        self._trace_id = trace_id
        self._parent_id = parent_id
        self.id = span_id if span_id else trace_id
        self._t0 = time.perf_counter()
        self._ts = _now_iso()

    def __enter__(self) -> "_JsonlNode":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self._emitter.emit({
            "kind": self.kind,
            "name": self.name,
            "ts": self._ts,
            "ts_end": _now_iso(),
            "latency_ms": round((time.perf_counter() - self._t0) * 1000, 1),
            "meta": self._meta,
            "trace_id": self._trace_id,
            "span_id": self.id if self.kind == "span" else None,
            "parent_id": self._parent_id,
        })

    def span(self, name: str, meta: dict | None = None) -> "_JsonlNode":
        return _JsonlNode(self._emitter, name, meta, trace_id=self._trace_id,
                          span_id=uuid.uuid4().hex[:8], parent_id=self.id)

    def event(self, name: str, **kv: Any) -> None:
        self._emitter.emit({
            "kind": "event",
            "name": name,
            "ts": _now_iso(),
            "latency_ms": None,
            "meta": dict(kv),
            "trace_id": self._trace_id,
            "span_id": self.id,
            "parent_id": None,
        })


class _JsonlTrace(_JsonlNode):
    """trace 节点：id 即 trace_id。"""

    kind = "trace"

    def __init__(self, emitter: _JsonlEmitter, name: str, meta: dict | None = None):
        super().__init__(emitter, name, meta, trace_id=uuid.uuid4().hex[:12],
                         span_id=None, parent_id=None)


class JsonlTracer:
    """本地 JSONL 兜底 Tracer：调用方指定输出路径（通常 data/traces/ 下一文件一次运行）。"""

    def __init__(self, path: Path):
        self._emitter = _JsonlEmitter(path)

    @property
    def path(self) -> Path:
        return self._emitter.path

    def trace(self, name: str, meta: dict | None = None) -> Trace:
        return _JsonlTrace(self._emitter, name, meta)


# ---------------------------------------------------------------------------
# Langfuse 实现
# ---------------------------------------------------------------------------

class _DeadObservation:
    """SDK 调用失败后的空实现：所有方法 no-op，保证主流程不受观测故障影响。"""

    def __enter__(self) -> "_DeadObservation":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        return None

    def __getattr__(self, name: str):
        def _noop(*args, **kwargs):
            return _DeadObservation()
        return _noop


class _LangfuseObservation:
    """span/event 句柄：包装 langfuse observation，SDK 异常只记 stderr 不上抛。

    兼容 langfuse v4（start_observation/create_event，命令式）与 v2/3（span()/event()）。
    """

    def __init__(self, raw: Any):
        self._raw = raw

    def __enter__(self) -> "_LangfuseObservation":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self._call("end")

    def _call(self, method: str, **kwargs: Any) -> Any:
        fn = getattr(self._raw, method, None)
        if not callable(fn):
            return None
        try:
            return fn(**kwargs)
        except Exception as exc:  # noqa: BLE001 — 观测不上抛
            _note(f"langfuse {method} 失败（忽略）：{exc}")
            return None

    @property
    def id(self) -> str | None:
        return getattr(self._raw, "id", None)

    def span(self, name: str, meta: dict | None = None) -> "_LangfuseObservation":
        raw = None
        if callable(getattr(self._raw, "start_observation", None)):  # v4
            raw = self._call("start_observation", name=name, as_type="span",
                             metadata=dict(meta or {}))
        elif callable(getattr(self._raw, "span", None)):  # v2/3
            raw = self._call("span", name=name, metadata=dict(meta or {}))
        return _LangfuseObservation(raw if raw is not None else _DeadObservation())

    def event(self, name: str, **kv: Any) -> None:
        if callable(getattr(self._raw, "create_event", None)):  # v4
            self._call("create_event", name=name, metadata=dict(kv))
        elif callable(getattr(self._raw, "event", None)):  # v2/3
            self._call("event", name=name, metadata=dict(kv))
        else:  # 更旧的 SDK 无 event 观测类型 → 用瞬时观测表达
            raw = (self._call("start_observation", name=name, as_type="event",
                              metadata=dict(kv))
                   or self._call("span", name=name, metadata=dict(kv)))
            if raw is not None:
                end = getattr(raw, "end", None)
                if callable(end):
                    try:
                        end()
                    except Exception:  # noqa: BLE001
                        pass


class _LangfuseTrace(_LangfuseObservation):
    """trace 句柄（v4 下即根观测）：退出时 end + flush。"""

    def __init__(self, client: Any, raw: Any):
        super().__init__(raw)
        self._client = client

    @property
    def id(self) -> str | None:
        tid = getattr(self._raw, "trace_id", None)
        return tid if tid else getattr(self._raw, "id", None)

    def __exit__(self, exc_type, exc, tb) -> None:
        super().__exit__(exc_type, exc, tb)
        fn = getattr(self._client, "flush", None)
        if callable(fn):
            try:
                fn()
            except Exception as exc:  # noqa: BLE001
                _note(f"langfuse flush 失败（忽略）：{exc}")


class LangfuseTracer:
    """Langfuse Cloud Tracer：懒导入 SDK；导入/初始化失败在构造时抛 RuntimeError。"""

    def __init__(self, public_key: str, secret_key: str, host: str):
        try:
            sdk = importlib.import_module("langfuse")
        except Exception as exc:  # noqa: BLE001 — 统一转 RuntimeError 供 get_tracer 降级
            raise RuntimeError(f"langfuse SDK 导入失败（uv add langfuse）：{exc}") from exc
        try:
            self._client = sdk.Langfuse(public_key=public_key, secret_key=secret_key,
                                        host=host)
        except Exception as exc:  # noqa: BLE001
            raise RuntimeError(f"langfuse 初始化失败：{exc}") from exc

    def trace(self, name: str, meta: dict | None = None) -> Trace:
        raw = None
        try:
            if callable(getattr(self._client, "start_observation", None)):  # v4：根观测即 trace
                raw = self._client.start_observation(name=name, as_type="span",
                                                     metadata=dict(meta or {}))
            else:  # v2/3：显式 trace 对象
                raw = self._client.trace(name=name, metadata=dict(meta or {}))
        except Exception as exc:  # noqa: BLE001
            _note(f"langfuse trace 创建失败（忽略）：{exc}")
        return _LangfuseTrace(self._client, raw if raw is not None else _DeadObservation())


# ---------------------------------------------------------------------------
# 选择逻辑
# ---------------------------------------------------------------------------

def get_tracer(settings: Settings | None = None, run_name: str = "run") -> Tracer:
    """按配置选择 Tracer：有 Langfuse 密钥 → Cloud，否则本地 JSONL 兜底。

    Langfuse 构造失败（缺 SDK / 密钥无效）时降级 JSONL 并记 stderr，绝不阻断主流程。
    """
    settings = settings or Settings.from_env()
    if settings.langfuse_public_key and settings.langfuse_secret_key:
        try:
            return LangfuseTracer(settings.langfuse_public_key,
                                  settings.langfuse_secret_key, settings.langfuse_host)
        except Exception as exc:  # noqa: BLE001
            _note(f"Langfuse 不可用，降级本地 JSONL：{exc}")
    stamp = _dt.datetime.now().strftime("%Y%m%d-%H%M%S")
    safe = re.sub(r"[^0-9A-Za-z_-]+", "-", run_name).strip("-") or "run"
    path = settings.data_dir / "traces" / f"{stamp}-{safe}.jsonl"
    return JsonlTracer(path)
