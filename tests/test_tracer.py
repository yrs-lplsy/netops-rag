"""可插拔 Tracer 单测：JSONL 往返、fallback 选择、Langfuse 假 SDK 注入、IO 容错。

全部离线：Langfuse 用注入 sys.modules 的假 SDK，不发网络请求。
"""

import json
import sys
import time
import types
from datetime import datetime

from netrag.config import Settings
from netrag.observability.tracer import JsonlTracer, LangfuseTracer, get_tracer


def _read_lines(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


# ---------------------------------------------------------------------------
# JSONL 往返
# ---------------------------------------------------------------------------

def test_jsonl_roundtrip_trace_span_event(tmp_path):
    path = tmp_path / "nested" / "run.jsonl"
    tracer = JsonlTracer(path)
    with tracer.trace("run", meta={"question": "q"}) as trace:
        with trace.span("retrieve", meta={"top_k": 5}) as span:
            span.event("hits", chunk_ids=["c1", "c2"], scores=[0.9, 0.8])
        trace.event("done", ok=True)

    assert path.exists()  # 父目录自动创建
    records = _read_lines(path)
    assert [r["kind"] for r in records] == ["event", "span", "event", "trace"]

    trace_rec = records[-1]
    assert trace_rec["name"] == "run"
    assert trace_rec["meta"] == {"question": "q"}
    assert trace_rec["latency_ms"] >= 0
    assert trace_rec["trace_id"] == trace.id

    span_rec = records[1]
    assert span_rec["name"] == "retrieve"
    assert span_rec["meta"] == {"top_k": 5}
    assert span_rec["latency_ms"] >= 0
    assert span_rec["trace_id"] == trace.id

    hit = records[0]
    assert hit["name"] == "hits"
    assert hit["meta"] == {"chunk_ids": ["c1", "c2"], "scores": [0.9, 0.8]}
    assert hit["span_id"] == span.id  # 事件挂在所属 span 上
    assert hit["trace_id"] == trace.id

    # iso 时间戳可解析
    datetime.fromisoformat(trace_rec["ts"])
    datetime.fromisoformat(trace_rec["ts_end"])
    datetime.fromisoformat(span_rec["ts"])


def test_jsonl_latency_recorded(tmp_path):
    tracer = JsonlTracer(tmp_path / "t.jsonl")
    with tracer.trace("slow") as trace:
        with trace.span("wait"):
            time.sleep(0.05)
    records = _read_lines(tmp_path / "t.jsonl")
    spans = [r for r in records if r["kind"] == "span"]
    assert spans and spans[0]["latency_ms"] >= 40.0
    assert trace.id


def test_jsonl_nested_span_linkage(tmp_path):
    tracer = JsonlTracer(tmp_path / "t.jsonl")
    with tracer.trace("run") as trace:
        with trace.span("outer") as outer:
            with outer.span("inner") as inner:
                inner.event("leaf", k="v")
    records = _read_lines(tmp_path / "t.jsonl")
    by_name = {r["name"]: r for r in records if r["kind"] == "span"}
    assert by_name["inner"]["parent_id"] == outer.id
    assert by_name["outer"]["parent_id"] == trace.id
    leaf = next(r for r in records if r["name"] == "leaf")
    assert leaf["span_id"] == inner.id


def test_jsonl_io_failure_is_best_effort(tmp_path, capsys):
    # 父路径被同名文件占用 → mkdir/append 必失败，但绝不上抛
    blocker = tmp_path / "blocker"
    blocker.write_text("x")
    tracer = JsonlTracer(blocker / "traces" / "run.jsonl")
    with tracer.trace("run") as trace:
        trace.event("e", k=1)  # 不应抛异常
    assert "tracer" in capsys.readouterr().err.lower()


# ---------------------------------------------------------------------------
# get_tracer 选择逻辑
# ---------------------------------------------------------------------------

def test_get_tracer_falls_back_to_jsonl_without_keys(tmp_path):
    settings = Settings(data_dir=tmp_path)  # langfuse 密钥缺省为空
    tracer = get_tracer(settings, run_name="ask")
    assert isinstance(tracer, JsonlTracer)
    assert tracer.path.parent == tmp_path / "traces"
    assert tracer.path.suffix == ".jsonl"
    assert "ask" in tracer.path.name


def test_get_tracer_uses_langfuse_when_keys_present(monkeypatch, tmp_path):
    mod, instances = _fake_langfuse_module()
    monkeypatch.setitem(sys.modules, "langfuse", mod)
    settings = Settings(data_dir=tmp_path, langfuse_public_key="pk-test",
                        langfuse_secret_key="sk-test", langfuse_host="http://lf.local")
    tracer = get_tracer(settings, run_name="ask")
    assert isinstance(tracer, LangfuseTracer)
    assert instances[0]["kwargs"] == {"public_key": "pk-test", "secret_key": "sk-test",
                                      "host": "http://lf.local"}

    client = instances[0]["client"]
    with tracer.trace("ask", meta={"question": "q"}) as trace:
        with trace.span("retrieve"):
            pass
    assert client.flushed == 1  # trace 退出即 flush
    root = client.roots[0]
    assert root.name == "ask" and root.metadata == {"question": "q"}
    assert root.ended  # trace 结束被标记
    assert any(o.name == "retrieve" for o in root.children)


def test_get_tracer_falls_back_when_langfuse_init_fails(monkeypatch, tmp_path, capsys):
    mod = types.ModuleType("langfuse")

    class Boom:
        def __init__(self, **kwargs):
            raise RuntimeError("no network")

    mod.Langfuse = Boom
    monkeypatch.setitem(sys.modules, "langfuse", mod)
    settings = Settings(data_dir=tmp_path, langfuse_public_key="pk",
                        langfuse_secret_key="sk")
    tracer = get_tracer(settings)
    assert isinstance(tracer, JsonlTracer)  # 初始化失败 → 本地兜底
    assert "langfuse" in capsys.readouterr().err.lower()


def test_langfuse_tracer_raises_when_sdk_missing(monkeypatch):
    monkeypatch.setitem(sys.modules, "langfuse", None)  # import 即 ImportError
    import pytest

    with pytest.raises(RuntimeError):
        LangfuseTracer("pk", "sk", "http://x")


def test_langfuse_tracer_maps_spans_and_events(monkeypatch):
    mod, instances = _fake_langfuse_module()
    monkeypatch.setitem(sys.modules, "langfuse", mod)
    tracer = LangfuseTracer("pk", "sk", "http://lf.local")
    client = instances[0]["client"]
    with tracer.trace("t", meta={"a": 1}) as trace:
        with trace.span("s", meta={"b": 2}) as span:
            span.event("e", c=3)
    root = client.roots[0]
    assert root.name == "t" and root.metadata == {"a": 1} and root.ended
    spans = [o for o in root.children if o.name == "s"]
    assert spans and spans[0].metadata == {"b": 2} and spans[0].ended
    events = [o for o in spans[0].children if o.name == "e"]
    assert events and events[0].metadata == {"c": 3}
    assert events[0].as_type == "event"


# ---------------------------------------------------------------------------
# Settings 新字段
# ---------------------------------------------------------------------------

def test_settings_langfuse_fields(monkeypatch, tmp_path):
    for k in ("LANGFUSE_PUBLIC_KEY", "LANGFUSE_SECRET_KEY", "LANGFUSE_HOST"):
        monkeypatch.delenv(k, raising=False)
    s = Settings.from_env(env_file=tmp_path / "absent.env")
    assert s.langfuse_public_key == ""
    assert s.langfuse_secret_key == ""
    assert s.langfuse_host == "https://cloud.langfuse.com"

    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-env")
    monkeypatch.setenv("LANGFUSE_HOST", "http://self-hosted:3000")
    s2 = Settings.from_env(env_file=tmp_path / "absent.env")
    assert s2.langfuse_public_key == "pk-env"
    assert s2.langfuse_host == "http://self-hosted:3000"


# ---------------------------------------------------------------------------
# 假 langfuse SDK（记录调用，不发网络请求）
# ---------------------------------------------------------------------------

def _fake_langfuse_module():
    """构造可注入 sys.modules 的假 langfuse 模块（对齐 SDK v4 API：start_observation /
    create_event / end / flush），记录调用树，不发网络请求。"""
    mod = types.ModuleType("langfuse")
    instances: list[dict] = []

    class FakeObservation:
        def __init__(self, store, name, metadata, as_type="span"):
            self.name = name
            self.metadata = metadata
            self.as_type = as_type
            self.ended = False
            self.children: list[FakeObservation] = []
            self.id = f"obs-{id(store) % 10000}-{len(store)}"
            self.trace_id = "trace-fake"
            store.append(self)

        def start_observation(self, name=None, as_type="span", metadata=None):
            return FakeObservation(self.children, name, metadata, as_type)

        def create_event(self, name=None, metadata=None):
            return FakeObservation(self.children, name, metadata, as_type="event")

        def end(self):
            self.ended = True

    class FakeLangfuse:
        def __init__(self, public_key=None, secret_key=None, host=None):
            self.public_key = public_key
            self.secret_key = secret_key
            self.host = host
            self.roots: list[FakeObservation] = []
            self.flushed = 0
            instances.append({"kwargs": {"public_key": public_key, "secret_key": secret_key,
                                         "host": host}, "client": self})

        def start_observation(self, name=None, as_type="span", metadata=None):
            return FakeObservation(self.roots, name, metadata, as_type)

        def flush(self):
            self.flushed += 1

    mod.Langfuse = FakeLangfuse
    return mod, instances
