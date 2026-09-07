"""FastAPI 收口单测：httpx TestClient（ASGI 内存）+ fake graph/gateway，零网络零设备。

覆盖：/ask 与 /diagnose 全请求-响应环（fresh thread_id、history/top_k/host 透传、
tool_outputs 透传）、校验错误 400 形状、审批端点（tmp approvals 文件：GET 状态 /
approve 发一次性 token / 404 / approver 必填）、默认图懒构建（启动零副作用，首次
用到图的请求才构建）与「不暴露任何写端点」的 API 面约束。
"""

import logging

import pytest
from fastapi.testclient import TestClient

from netrag.api.app import create_app
from netrag.config import Settings
from netrag.tools_mcp import approval


# ---------------------------------------------------------------------------
# 假件
# ---------------------------------------------------------------------------

class FakeGraph:
    """记录 invoke 入参的假图：返回脚本化终态（可注入 tool_calls 等）。"""

    def __init__(self, final=None):
        self.final = final or {}
        self.invocations = []

    def invoke(self, state, config=None):
        self.invocations.append((state, config))
        base = {"answer": "答案", "citations": ["[1] 手册"], "handoff": False,
                "route": None, "tool_calls": []}
        return {**base, **self.final}


class FakeGateway:
    default_host = "core1"

    def __init__(self):
        self.calls = []

    def read(self, tool, args):
        self.calls.append((tool, dict(args)))
        return "fake live output"


def _diag_final():
    return {"tool_calls": [{"tool": "show_ospf_neighbor",
                            "args": {"host": "core1"},
                            "output": "10.0.0.2 1 FULL/DR"}]}


# ---------------------------------------------------------------------------
# 注入图/网关：全请求-响应环
# ---------------------------------------------------------------------------

@pytest.fixture()
def tmp_approvals(tmp_path):
    return tmp_path / "approvals.jsonl"


@pytest.fixture()
def app(tmp_approvals):
    # 显式 Settings()（approve_secret 为空）：测试密闭，不随开发者 .env 的
    # APPROVE_SECRET 漂移；密钥门行为由专用测试覆盖
    return create_app(settings=Settings(), graph=FakeGraph(final=_diag_final()),
                      gateway=FakeGateway(), approvals_path=tmp_approvals)


@pytest.fixture()
def client(app):
    return TestClient(app)


def test_ask_round_trip(client):
    r = client.post("/ask", json={"question": "如何在 Catalyst 9300 上配置 OSPF 存根区域",
                                  "history": [["上一问", "上一答"]], "top_k": 3})
    assert r.status_code == 200
    body = r.json()
    assert set(body) == {"answer", "citations", "handoff", "route", "trace_id"}
    assert body["answer"] == "答案"
    assert body["citations"] == ["[1] 手册"]
    assert body["handoff"] is False
    assert body["route"] is None
    assert body["trace_id"]


def test_ask_passes_question_history_top_k_with_fresh_thread(client):
    r1 = client.post("/ask", json={"question": "q1", "history": [["a", "b"]], "top_k": 3})
    r2 = client.post("/ask", json={"question": "q2"})
    graph = client.app.state.injected_graph
    (state1, cfg1), (state2, cfg2) = graph.invocations
    assert state1 == {"question": "q1", "history": [("a", "b")], "top_k": 3}
    assert state2 == {"question": "q2"}
    tid1, tid2 = cfg1["configurable"]["thread_id"], cfg2["configurable"]["thread_id"]
    assert tid1 and tid2 and tid1 != tid2  # 每请求新 thread_id（MemorySaver 语义）


def test_ask_validation_error_400_shape(client):
    for payload in ({"question": ""}, {}, {"question": "q", "top_k": 0},
                    {"question": "q", "top_k": 999}):
        r = client.post("/ask", json=payload)
        assert r.status_code == 400, payload
        body = r.json()
        assert body["error"] == "invalid_request"
        assert body["detail"]


def test_diagnose_round_trip_returns_tool_outputs(client):
    r = client.post("/diagnose", json={"question": "core1 的 OSPF 邻居状态怎么样",
                                       "host": "core1"})
    assert r.status_code == 200
    body = r.json()
    assert set(body) == {"answer", "citations", "tool_outputs", "handoff",
                         "route", "trace_id"}
    assert body["tool_outputs"] == [
        {"tool": "show_ospf_neighbor", "args": {"host": "core1"},
         "output": "10.0.0.2 1 FULL/DR"}]
    state, _ = client.app.state.injected_graph.invocations[-1]
    assert state["host"] == "core1"  # host 透传进图（诊断节点免提取）
    assert state["question"].startswith("core1")


def test_diagnose_without_host_omits_key(client):
    r = client.post("/diagnose", json={"question": "看看日志"})
    assert r.status_code == 200
    state, _ = client.app.state.injected_graph.invocations[-1]
    assert "host" not in state  # 留给诊断节点从问题提取/gateway 默认
    r2 = client.post("/diagnose", json={"question": ""})
    assert r2.status_code == 400


def test_api_surface_has_no_write_endpoints(client):
    """API 面只暴露只读能力：任何配置下发/回滚端点都不存在（审批外置）。"""
    paths = set(client.get("/openapi.json").json()["paths"])
    assert paths == {"/health", "/ask", "/diagnose",
                     "/approvals/{approval_id}", "/approvals/{approval_id}/approve"}


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


# ---------------------------------------------------------------------------
# 审批工作流（tmp approvals 文件）
# ---------------------------------------------------------------------------

def test_approval_get_status_round_trip(client, tmp_approvals):
    rid = approval.request_approval("acc1", ["description X"], path=tmp_approvals)
    r = client.get(f"/approvals/{rid}")
    assert r.status_code == 200
    body = r.json()
    assert body["approval_id"] == rid
    assert body["status"] == "pending"
    assert body["host"] == "acc1"
    assert body["planned_lines"] == ["description X"]


def test_approval_approve_returns_one_time_token(client, tmp_approvals):
    rid = approval.request_approval("acc1", ["description X"], path=tmp_approvals)
    r = client.post(f"/approvals/{rid}/approve", json={"approver": "ops-admin"})
    assert r.status_code == 200
    body = r.json()
    assert body["approval_id"] == rid
    assert body["status"] == "approved"
    assert body["token"]  # 明文 token 仅此一次
    rec = client.get(f"/approvals/{rid}").json()
    assert rec["status"] == "approved" and rec["approver"] == "ops-admin"
    assert "token" not in rec  # 落盘只有哈希，状态接口不回明文


def test_approval_unknown_id_404_shape(client, tmp_approvals):
    r = client.get("/approvals/nope")
    assert r.status_code == 404
    assert r.json()["error"] == "unknown_approval_id"
    r2 = client.post("/approvals/nope/approve", json={"approver": "ops"})
    assert r2.status_code == 404
    assert r2.json()["error"] == "unknown_approval_id"


def test_approval_approve_requires_nonempty_approver(client, tmp_approvals):
    rid = approval.request_approval("acc1", ["description X"], path=tmp_approvals)
    r = client.post(f"/approvals/{rid}/approve", json={"approver": "  "})
    assert r.status_code == 400
    assert r.json()["error"] == "invalid_request"


# ---------------------------------------------------------------------------
# approve 共享密钥门（评审 Finding 1）：配置 APPROVE_SECRET 后必须携
# X-Approve-Secret 头才能批；未配置保持旧行为但记启动警告
# ---------------------------------------------------------------------------

def test_approve_secret_gate_when_configured(tmp_approvals):
    app = create_app(settings=Settings(approve_secret="s3cr3t"),
                     graph=FakeGraph(), approvals_path=tmp_approvals)
    client = TestClient(app)
    rid = approval.request_approval("acc1", ["description X"], path=tmp_approvals)
    # 状态查询（GET）不设门——只读，无提权面
    assert client.get(f"/approvals/{rid}").status_code == 200
    # 无头 → 403；错头 → 403；token 未被烧
    for headers in ({}, {"X-Approve-Secret": "wrong"}):
        r = client.post(f"/approvals/{rid}/approve", json={"approver": "ops"},
                        headers=headers)
        assert r.status_code == 403, headers
        assert r.json() == {"error": "forbidden"}
    assert approval.get(rid, path=tmp_approvals)["status"] == "pending"
    # 正头 → 200 + 一次性 token，状态推进
    r = client.post(f"/approvals/{rid}/approve", json={"approver": "ops"},
                    headers={"X-Approve-Secret": "s3cr3t"})
    assert r.status_code == 200 and r.json()["token"]
    assert approval.get(rid, path=tmp_approvals)["status"] == "approved"


def test_approve_open_when_secret_unconfigured_with_startup_warning(
        tmp_approvals, caplog):
    app = create_app(settings=Settings(), graph=FakeGraph(),
                     approvals_path=tmp_approvals)
    client = TestClient(app)
    rid = approval.request_approval("acc1", ["description X"], path=tmp_approvals)
    with caplog.at_level(logging.WARNING, logger="netrag.api.app"):
        create_app(settings=Settings(), graph=FakeGraph(),
                   approvals_path=tmp_approvals)  # 再次构建以捕获启动警告
    assert any("APPROVE_SECRET" in rec.message for rec in caplog.records)
    r = client.post(f"/approvals/{rid}/approve", json={"approver": "ops"})
    assert r.status_code == 200 and r.json()["token"]  # 旧行为：无头可批


# ---------------------------------------------------------------------------
# 默认图懒构建：注入图缺席时首次请求才构建（且 /ask 与 /diagnose 各用其图）
# ---------------------------------------------------------------------------

def test_default_graphs_built_lazily_per_endpoint(monkeypatch, tmp_approvals):
    ask, diag = FakeGraph(), FakeGraph(final=_diag_final())
    calls = []
    import netrag.api.app as app_mod

    def fake_build(settings, gateway=None):
        calls.append(settings)
        return ask, diag

    monkeypatch.setattr(app_mod, "_build_default_graphs", fake_build)
    app = create_app(approvals_path=tmp_approvals)
    client = TestClient(app)
    assert calls == []  # 启动/注册期零构建
    client.get("/health")
    assert calls == []  # 健康检查不触图
    client.get("/approvals/x")  # 404，同样不触图
    assert calls == []
    r = client.post("/ask", json={"question": "q"})
    assert r.status_code == 200 and ask.invocations and not diag.invocations
    r = client.post("/diagnose", json={"question": "q"})
    assert r.status_code == 200 and diag.invocations
    assert len(calls) == 1  # 构建恰好一次，两图共享


def test_injected_graph_used_for_both_endpoints(tmp_approvals):
    g = FakeGraph()
    app = create_app(graph=g, approvals_path=tmp_approvals)
    client = TestClient(app)
    assert client.post("/ask", json={"question": "q"}).status_code == 200
    assert client.post("/diagnose", json={"question": "q"}).status_code == 200
    assert len(g.invocations) == 2  # 注入图同时服务两端点（测试/定制场景）
