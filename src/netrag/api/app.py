"""netrag API 层：FastAPI 收口（/ask、/diagnose、/approvals 审批工作流）。

设计（Task 13 Part B）：
- ``create_app(settings, graph, gateway, approvals_path)`` 依赖注入：测试传
  fake graph/gateway；生产不传则**首次用到图的请求**才懒构建真实图（Milvus +
  BGE-M3 + LLM，构建在请求线程完成，import/启动期零副作用、零网络）。
- ``POST /ask``：普通手册问答（tools=False 图）。每次请求一个新 thread_id
  （=响应里的 trace_id）——MemorySaver 检查点对同 thread_id 的二次 invoke 走
  断点续跑语义而不重跑，因此一问一 thread 是硬性要求。
- ``POST /diagnose``：诊断问答（tools=True 图，diagnose 节点经 ToolsGateway
  调只读 MCP 工具取设备实况）。**绝不执行写操作**：图内唯一可达的工具面是
  gateway.read 只读工具；若 LLM 认为需要变更，答案文本会给出「变更计划」提案，
  执行必须走人工流程——request_approval（Python 侧）登记计划 → 人工审批
  （``POST /approvals/{id}/approve`` 取一次性 token）→ 由运维/自动化携 token
  显式调用 MCP 写工具（push_config，token 与 host+变更计划强绑定）。写执行
  不暴露为任何 HTTP 端点（见 openapi 面测试）。
- ``GET /approvals/{id}`` / ``POST /approvals/{id}/approve``：审批单状态查询
  与人工批准（token 明文仅在 approve 响应出现一次，存储只有 sha256）。
  approve 设共享密钥门（评审 Finding 1）：配置 ``APPROVE_SECRET`` 后请求须携
  头 ``X-Approve-Secret``（常量时间比较，缺头/不匹配 403 且不烧 token）；
  未配置保持无鉴权旧行为，但 create_app 记启动警告。GET 状态查询不设门。
- 校验失败统一 400 ``{"error": "invalid_request", "detail": [...]}``；未知
  资源 404 ``{"error": "unknown_approval_id"}``。
- 端点均为同步 def（Starlette 线程池执行）——ToolsGateway 的 asyncio.run
  只能在无事件循环的线程里跑，async def 端点会破坏该前提。
"""

from __future__ import annotations

import hmac
import logging
import uuid
from typing import Any

from fastapi import FastAPI, Header, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from starlette.exceptions import HTTPException as StarletteHTTPException

from netrag.config import Settings
from netrag.tools_mcp import approval

__all__ = ["create_app"]

log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 请求/响应模型
# ---------------------------------------------------------------------------

class AskRequest(BaseModel):
    question: str = Field(min_length=1, pattern=r"\S")  # 拒绝纯空白
    history: list[tuple[str, str]] = Field(default_factory=list)
    top_k: int | None = Field(default=None, ge=1, le=20)


class DiagnoseRequest(BaseModel):
    question: str = Field(min_length=1, pattern=r"\S")
    host: str | None = Field(default=None, min_length=1, pattern=r"\S")
    top_k: int | None = Field(default=None, ge=1, le=20)


class ApproveRequest(BaseModel):
    approver: str = Field(min_length=1, pattern=r"\S")  # 审批人必填非空白


# ---------------------------------------------------------------------------
# 默认图懒构建（生产路径；测试 monkeypatch 本函数注入 fake）
# ---------------------------------------------------------------------------

def _build_default_retriever(settings: Settings) -> Any:
    from netrag.embedding.bge_m3 import BGEM3Embedder
    from netrag.embedding.reranker import BgeReranker
    from netrag.index.milvus_client import get_milvus, wait_healthy
    from netrag.retrieval.hybrid import HybridRetriever

    client = get_milvus()
    wait_healthy(client)
    embedder = BGEM3Embedder(settings.embed_model)
    return HybridRetriever(client, embedder, BgeReranker(settings.rerank_model),
                           recall_n=48)


def _build_default_graphs(settings: Settings, gateway: Any | None = None):
    """构建 (ask_graph, diagnose_graph)；共享检索器与 LLM，各构建一次。"""
    from netrag.agent.crag import build_crag_graph
    from netrag.generation.llm import LLMClient
    from netrag.tools_mcp.gateway import ToolsGateway

    llm = LLMClient(settings)
    retriever = _build_default_retriever(settings)
    ask = build_crag_graph(retriever, llm, settings=settings)
    diag = build_crag_graph(retriever, llm, settings=settings, tools=True,
                            gateway=gateway if gateway is not None
                            else ToolsGateway())
    return ask, diag


# ---------------------------------------------------------------------------
# app 工厂
# ---------------------------------------------------------------------------

def create_app(settings: Settings | None = None, graph: Any | None = None,
               gateway: Any | None = None,
               approvals_path: str | None = None) -> FastAPI:
    """组装 FastAPI：graph/gateway 可注入（fakes）；缺省懒构建真实组件。"""
    app = FastAPI(
        title="netops-rag",
        description=(
            "网络设备问答与诊断（Corrective RAG + MCP 设备工具）。"
            "写操作不经过本 API：/diagnose 至多给出变更计划提案，"
            "执行须经 request_approval → 人工 approve（本服务 "
            "/approvals/{id}/approve）→ 携一次性 token 显式调用 MCP 写工具。"
        ),
    )
    app.state.settings = settings or Settings.from_env()
    app.state.injected_graph = graph
    app.state.gateway = gateway
    app.state.approvals_path = str(approvals_path) if approvals_path \
        else str(approval.DEFAULT_PATH)
    app.state.approve_secret = app.state.settings.approve_secret
    if not app.state.approve_secret:
        # 评审 Finding 1：无共享密钥时 approve 端点对一切能触达 API 的人开放
        log.warning(
            "APPROVE_SECRET 未配置：POST /approvals/{id}/approve 无鉴权"
            "（能触达本服务即可自批拿写 token）。请在 .env 配置共享密钥；"
            "公网/跨网部署还应在网络层限制该端点可达范围。")
    app.state.resolved_graphs: tuple | None = None

    def _graphs() -> tuple:
        """首次用到才构建并缓存；注入图时两端点共用它（测试/定制场景）。"""
        if app.state.resolved_graphs is None:
            if app.state.injected_graph is not None:
                app.state.resolved_graphs = (app.state.injected_graph,) * 2
            else:
                app.state.resolved_graphs = _build_default_graphs(
                    app.state.settings, app.state.gateway)
        return app.state.resolved_graphs

    # -- 错误形状 ------------------------------------------------------------

    @app.exception_handler(RequestValidationError)
    async def _validation_handler(request: Request, exc: RequestValidationError):
        detail = [{"loc": list(e.get("loc", [])), "msg": e.get("msg", ""),
                   "type": e.get("type", "")} for e in exc.errors()]
        return JSONResponse(status_code=400,
                            content={"error": "invalid_request", "detail": detail})

    @app.exception_handler(StarletteHTTPException)
    async def _http_handler(request: Request, exc: StarletteHTTPException):
        key = "unknown_approval_id" if exc.status_code == 404 else str(exc.detail)
        return JSONResponse(status_code=exc.status_code, content={"error": key})

    def _trace_id() -> str:
        return uuid.uuid4().hex

    def _invoke(graph, state: dict, trace_id: str) -> dict:
        # fresh thread_id：MemorySaver 对同 thread_id 走断点续跑语义，一问一新
        thread_id = f"{trace_id}"
        return graph.invoke(state, config={"configurable": {"thread_id": thread_id}})

    def _clean_state(payload: dict, *, with_host: bool) -> dict:
        state: dict = {"question": payload["question"]}
        if payload.get("history"):
            state["history"] = [tuple(p) for p in payload["history"]]
        if payload.get("top_k"):
            state["top_k"] = payload["top_k"]
        if with_host and payload.get("host"):
            state["host"] = payload["host"]
        return state

    # -- 端点 ----------------------------------------------------------------

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.post("/ask")
    def ask(req: AskRequest) -> dict:
        ask_graph, _ = _graphs()
        trace_id = _trace_id()
        final = _invoke(ask_graph, _clean_state(req.model_dump(), with_host=False),
                        trace_id)
        return {"answer": final.get("answer", ""),
                "citations": final.get("citations", []),
                "handoff": bool(final.get("handoff", False)),
                "route": final.get("route") or None,
                "trace_id": trace_id}

    @app.post("/diagnose")
    def diagnose(req: DiagnoseRequest) -> dict:
        _, diag_graph = _graphs()  # tools=True：只读设备实况，永不执行写
        trace_id = _trace_id()
        final = _invoke(diag_graph, _clean_state(req.model_dump(), with_host=True),
                        trace_id)
        return {"answer": final.get("answer", ""),
                "citations": final.get("citations", []),
                "tool_outputs": final.get("tool_calls") or [],
                "handoff": bool(final.get("handoff", False)),
                "route": final.get("route") or None,
                "trace_id": trace_id}

    @app.get("/approvals/{approval_id}")
    def get_approval(approval_id: str) -> dict:
        try:
            return approval.get(approval_id, path=app.state.approvals_path)
        except ValueError:
            raise StarletteHTTPException(status_code=404, detail="unknown approval")

    @app.post("/approvals/{approval_id}/approve")
    def approve_approval(approval_id: str, req: ApproveRequest,
                         x_approve_secret: str | None = Header(
                             default=None, alias="X-Approve-Secret")) -> dict:
        # 共享密钥门（评审 Finding 1）：配置了 APPROVE_SECRET 时，缺头/不匹配
        # 一律 403 且不动审批单（token 不烧）。常量时间比较防时序侧信道。
        if app.state.approve_secret:
            supplied = x_approve_secret or ""
            if not hmac.compare_digest(supplied, app.state.approve_secret):
                raise StarletteHTTPException(status_code=403, detail="forbidden")
        try:
            token = approval.approve(approval_id, req.approver,
                                     path=app.state.approvals_path)
        except ValueError:
            raise StarletteHTTPException(status_code=404, detail="unknown approval")
        return {"approval_id": approval_id, "status": "approved",
                "approver": req.approver, "token": token}  # token 仅此一次

    return app
