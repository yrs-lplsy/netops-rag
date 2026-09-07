"""LangGraph Corrective RAG（CRAG）状态机：检索 → 打分 → 高分生成 / 低分改写重检 / 拒答转人工。

流程（Corrective RAG 简化版，评分为一次 LLM 通读全部片段的 1-10 整数）：

    retrieve → grade ─┬─ grade ≥ threshold → [diagnose →] generate（answer_with_citations）
                      ├─ retries < max_rewrite → rewrite → retrieve（重检一轮）
                      └─ 否则 → fallback（拒答 + handoff=True，转人工）

tools=True 时在高分路径上（重检后的高分同样算）插一个 diagnose 节点：把问题中
的设备实况类查询（启发式分类，见 is_device_state_query）经 ToolsGateway 调
只读 MCP 工具（show_ospf_neighbor 等），输出以「【设备实况】{host}」伪片段
追加进生成上下文，引用列表相应追加设备实况条目。实况问题在 grade 条件边上
**绕过打分门**直达 diagnose（人工决策 2026-09-07：手册打分对实况问题无意义，
低分也诊断，先导 t17 失败模式）；非实况问题仅在 grade 高分时经过 diagnose
（其内启发式不命中即空过），低分纠错路径不变；工具异常 fail-open 记入
tool_calls 不阻断生成。默认 tools=False，图结构与行为和 T7-T9 完全一致。

设计决策：
- 打分不是逐片 yes/no（那是 RAGAS/CRAG 论文的 token 密集做法），而是一次调用让模型
  对整组片段输出 {"score": 1-10}：省调用（每次打分 1 个 LLM call），解析用
  「取第一个落在 1-10 的整数」做鲁棒降级，垃圾输出按 0.0 记低分走纠错路径。
- 空检索结果不浪费打分调用，直接 0.0。
- 改写提示词强制原样保留设备型号/软件版本实体——语料按 model 标量字段索引，
  改写丢实体等于检索丢过滤键。
- Tracer 可选注入（默认 get_tracer 按配置自动选 Langfuse/JSONL）。一次 invoke
  恰好一条 trace：首个节点懒打开、终态节点（generate/fallback）关闭，句柄按
  thread_id 挂在 build 期登记簿上——langgraph 传给各节点的 config 不是同一对象，
  不能靠 configurable 传句柄（实测验证）。
- MemorySaver 检查点：同 thread_id 完成后再 invoke 会走断点续跑语义而不重跑
  （langgraph 原生行为），调用方应一个问题一个新 thread_id。
"""

from __future__ import annotations

import re
from typing import Any, TypedDict

from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph

from netrag.agent.condense import condense_question
from netrag.agent.query_router import hydep_expand, route_query
from netrag.generation.answer import answer_with_citations
from netrag.observability.tracer import Tracer, get_tracer
from netrag.retrieval.base import RetrievedChunk

FALLBACK_ANSWER = "手册中未找到相关内容，建议转人工工程师。"

DIRECT_ANSWER = "该问题与网络设备运维知识库无关，请提出网络设备配置、故障排查等相关问题。"

GRADE_SYSTEM = (
    "你是检索质量评审员。判断给定网络设备手册片段是否包含回答问题所需的信息。"
    '只输出一个 JSON 对象：{"score": <1到10的整数>}，'
    "10 表示片段足以回答问题，1 表示完全无关。不要输出任何其他文字。"
)

REWRITE_SYSTEM = (
    "你是网络手册检索查询改写器。把用户问题改写成更适合检索的查询："
    "补充同义词、展开缩写（如 OSPF 开放最短路径优先、STP 生成树）。"
    "必须原样保留设备型号与软件版本实体（如 Catalyst 9300、V600R025、S5700），不得改写或删除。"
    "只输出改写后的查询本身，不要任何解释。"
)

_INT_RE = re.compile(r"\d+")

# ---------------------------------------------------------------------------
# 诊断路由（tools=True）：设备实况问题启发式 —— 确定性、零 LLM、可单测。
# 刻意不复用 T9 的 route_query（那是检索路由，且多花一次 LLM 调用）；关键词
# 查询一次只读调用为代价，不改变检索/生成主链路。
# ---------------------------------------------------------------------------
_STATE_KEYWORDS: tuple[str, ...] = (
    "状态", "邻居", "邻接", "日志", "接口", "查看", "看下", "查一下",
    "检查", "当前", "实况", "show", "display", "neighbor", "up/down",
    # 人工决策（2026-09-07）新增只读工具的触发词：绕路/cost → 路由表，不通 → ping
    "不通", "绕路", "绕远", "路径", "ping",
)

# 关键词 → 只读 MCP 工具序列（顺序即优先级，首个命中生效；值为**有序工具元组**，
# diagnose 节点按序调用元组内全部工具，每个输出各成一条【设备实况】伪片段）。
# 人工决策（2026-09-07）：+绕路/路径 → show_ip_route（FRR 路由表证「绕路存在」，
# 先于「配置」命中）；+不通 → ping 次选（仅当问题无更具体的关键词时才命中）。
# 收尾轮（与 shutdown 类同构）：cost 类补 get_running_config——异常 cost 在路由表
# 不显式可见（直连网段仅 `C>* … is directly connected`），`ip ospf cost 65535`
# 配置行才能归因，证据链闭合。
# 修复轮 1（t02 根因①：单工具诊断证据链断裂）：
#   - shutdown/接口类 → (show_ip_interface_brief, show_ospf_neighbor)：接口摘要
#     含接口名与 up/down（eth3 相关输出在前），邻居表佐证邻接摘除——被 shutdown 的
#     接口在邻居表里只是"消失"，证据必须来自接口视图；
#   - 排序调整（确定性优先级，非架构变更）：vlan 先于 接口（「VLAN 子接口」类问题
#     不得被「子接口」关键词劫持），接口 先于 邻居（同时点名的 shutdown 类问题走
#     工具对；纯「OSPF 邻居状态」问题不含接口词仍命中单工具）。
# 修复轮 2（t02 闭合）：shutdown 类元组补第三工具 get_running_config——接口摘要
#   只能看到 down（管理性关闭与链路故障不可分），`shutdown` 配置行才能归因
#   「管理性关闭」，证据链闭合。
_STATE_TOOL_MAP: tuple[tuple[tuple[str, ...], tuple[str, ...]], ...] = (
    (("日志", "log"), ("show_logging",)),
    (("arp",), ("get_arp_table",)),
    # 修复（t23-t28 闭合，与 shutdown/cost 类同构）：vlan 类二元组——show_vlan 证
    # 子接口存在/失链，但对 down 子接口不显示地址列；running-config 的
    # `no ip address`+迁移命令序列才能归因「地址迁到哪个新标签」，证据链闭合
    (("vlan",), ("show_vlan", "get_running_config")),
    (("版本", "version"), ("show_version",)),
    (("绕路", "绕远", "路径", "路由", "route"),
     ("show_ip_route", "get_running_config")),
    # 修复轮 2（t02 闭合）：接口对扩三元组——brief 显示 down → 邻居表佐证邻接摘除
    # → running config 的 `shutdown` 行归因「管理性关闭」，证据链闭合
    (("接口", "interface", "up/down"),
     ("show_ip_interface_brief", "show_ospf_neighbor", "get_running_config")),
    (("邻居", "neighbor", "ospf", "邻接"), ("show_ospf_neighbor",)),
    (("配置", "config", "running"), ("get_running_config",)),
    (("不通", "ping"), ("ping",)),
)
_DEFAULT_STATE_TOOLS: tuple[str, ...] = ("show_ip_interface_brief",)

# 问题中的主机名：字母开头、含数字的短词（core1/acc2/sw-3）。"S5735" 这类
# 型号词会误中——已知局限，host 显式传入（API 层）优先于提取；未知主机只会
# 得到一条 fail-open 的工具错误记录，不影响生成。
_HOST_RE = re.compile(r"(?<![A-Za-z0-9_-])[A-Za-z][A-Za-z0-9-]*\d(?![A-Za-z0-9_-])")

# 问题中的 ping 目标：点分十进制 IPv4（ping 工具的必填 target 参数）。
_TARGET_RE = re.compile(r"(\d{1,3}(?:\.\d{1,3}){3})")

_TOOL_OUTPUT_CAP = 2000  # 设备实况进提示词的截断长度

_GRADE_TEMPERATURE = 0.0
_GRADE_MAX_TOKENS = 16
_REWRITE_MAX_TOKENS = 128
_CHUNK_EXCERPT = 800  # 打分提示词里每片段截断长度：评分只需判断相关性，不必全文


def _parse_grade(text: str) -> float:
    """从 LLM 输出提取第一个落在 1-10 的整数；找不到/全越界 → 0.0（记低分）。"""
    for m in _INT_RE.finditer(text or ""):
        v = int(m.group())
        if 1 <= v <= 10:
            return float(v)
    return 0.0


def is_device_state_query(question: str) -> bool:
    """启发式判断问题是否在问设备实况（子串匹配，小写归一；零 LLM 调用）。"""
    q = (question or "").lower()
    return any(k.lower() in q for k in _STATE_KEYWORDS)


def select_state_tools(question: str) -> tuple[str, ...]:
    """按关键词把实况问题映射到只读 MCP 工具**有序序列**（顺序优先，缺省接口摘要）。"""
    q = (question or "").lower()
    for keys, tools in _STATE_TOOL_MAP:
        if any(k.lower() in q for k in keys):
            return tools
    return _DEFAULT_STATE_TOOLS


def _extract_host(question: str) -> str:
    """从问题提取主机名（首个字母开头含数字的短词）；无 → 空串。"""
    m = _HOST_RE.search(question or "")
    return m.group(0) if m else ""


def _device_state_chunk(call: dict) -> RetrievedChunk | None:
    """一次工具调用 → 「【设备实况】{host}」伪片段（进生成上下文与引用）。"""
    out = (call.get("output") or "").strip()
    if not out:
        return None
    host = (call.get("args") or {}).get("host", "")
    return RetrievedChunk(
        chunk_id=f"tool:{call['tool']}:{host}", text=out, score=1.0,
        doc_id=f"mcp:{call['tool']}", breadcrumb=f"【设备实况】{host}",
        vendor="", model="", sw_version="", parent_id=None, parent_text=None)


def grade_chunks(question: str, chunks: list[RetrievedChunk], llm: Any) -> float:
    """一次 LLM 调用给整组片段打 1-10 相关分；解析失败/无片段 → 0.0。"""
    if not chunks:
        return 0.0
    ctx = "\n\n".join(
        f"[{i + 1}] {c.breadcrumb}\n{c.text[:_CHUNK_EXCERPT]}" for i, c in enumerate(chunks)
    )
    user = f"问题：{question}\n\n手册片段：\n{ctx}"
    out = llm.chat([{"role": "system", "content": GRADE_SYSTEM},
                    {"role": "user", "content": user}],
                   temperature=_GRADE_TEMPERATURE, max_tokens=_GRADE_MAX_TOKENS)
    return _parse_grade(out)


def rewrite_query(question: str, llm: Any) -> str:
    """一次 LLM 调用改写检索查询（补同义词/展开缩写，保留型号版本实体）。"""
    out = llm.chat([{"role": "system", "content": REWRITE_SYSTEM},
                    {"role": "user", "content": question}],
                   max_tokens=_REWRITE_MAX_TOKENS)
    rewritten = (out or "").strip().strip('"').strip()
    return rewritten or question


class CRAGState(TypedDict, total=False):
    question: str
    orig_question: str  # 仅 condense=True 且发生改写时与 question 不同（调试/引用）
    history: list  # [(user_q, assistant_a), ...] 多轮历史，condense 节点消费
    force_condense: bool  # 绕过指代词启发式，强制改写
    route: str  # 路由分类结果：exact | fuzzy | direct（仅 route=True 时产出）
    hyde: str  # HyDE 假设文档段（仅 fuzzy 路由且生成成功时非空）
    host: str  # 诊断目标主机（API 显式传入时优先于问题内提取）
    tool_calls: list  # diagnose 节点产出：[{tool, args, output}, ...]（仅 tools=True）
    top_k: int  # 本次 invoke 的检索条数覆盖（API /ask 透传；缺省用构建默认）
    rewritten: str
    chunks: list
    grade: float
    retries: int
    answer: str
    citations: list[str]
    handoff: bool
    trace_meta: dict


class _TraceBook:
    """build 期登记簿：thread_id → 已打开的 trace 句柄。

    首个节点懒打开一次 invoke 的 trace，终态节点关闭并移除——保证一次 invoke
    恰好一条 trace，重检回路（retrieve 跑两遍）不会重复开。Tracer 的实现自身
    吞异常（观测不上抛），这里不再包 try。
    """

    def __init__(self) -> None:
        self._open: dict[str, Any] = {}

    def open(self, tracer: Tracer | None, thread_id: str, meta: dict) -> Any:
        if tracer is None:
            return None
        if thread_id not in self._open:
            handle = tracer.trace("crag", meta=meta)
            handle.__enter__()
            self._open[thread_id] = handle
        return self._open[thread_id]

    def close(self, thread_id: str) -> None:
        handle = self._open.pop(thread_id, None)
        if handle is not None:
            handle.__exit__(None, None, None)


def build_crag_graph(retriever, llm, settings=None, threshold: float = 6.0,
                     max_rewrite: int = 1, *, top_k: int = 5,
                     tracer: Tracer | None = None, condense: bool = False,
                     route: bool = False, tools: bool = False,
                     gateway: Any | None = None):
    """组装 CRAG 图并编译（MemorySaver 检查点，invoke 需带 thread_id）。

    condense=True 时在 retrieve 前插一个 condense 节点做多轮指代消解：读
    state["history"]（[(user_q, assistant_a), ...]），按指代词启发式决定是否花
    一次 LLM 改写（force_condense=True 可强制），改写结果写入 state["question"]，
    原问题保留在 state["orig_question"]。默认 False，图结构与 T7 完全一致。
    route=True 时在 condense 后（或图入口）插一个 route 节点做查询类型路由
    （retriever 须为 RoutedRetriever）：
        exact  → BM25 单路检索器直查（命令/参数/报错码，字面匹配最准）；
        fuzzy  → hydep_expand 生成假设文档段，与原问题拼接为单一查询走 dense
                 检索器（hyde 丰富语义向量、原问题锚定意图；刻意不做两次检索
                 再合并——避免第二套融合权重）；hyde 为空则原问题直查；
        direct → 跳过检索与打分，直接 canned 回复（不转人工，超纲≠系统故障）。
    垃圾分类 fail-safe 按 fuzzy 兜底。默认 False，检索行为与 T7/T8 一致。
    tools=True 时在 grade 后插 diagnose 节点：实况问题（is_device_state_query）
    绕过打分门直达诊断，其余问题仅在 grade 高分路径经过；经 gateway.read 按映射
    的**有序工具序列**逐个调用只读 MCP 工具（host 取 state["host"] > 问题内提取 >
    gateway.default_host），每个输出以「【设备实况】{host}」伪片段注入生成并追加
    引用条目；工具异常 fail-open（单工具失败记入 tool_calls、继续其余）。
    gateway=None 时懒构建真实 ToolsGateway（测试注入假网关）。默认 False，
    图结构与行为和 T7-T9 完全一致（gateway 完全不被触碰）。
    tracer=None 时按 Settings 自动选（Langfuse 密钥 → Cloud，否则 JSONL 兜底）；
    测试注入假 Tracer 保持零网络。
    """
    if tools and gateway is None:
        from netrag.tools_mcp.gateway import ToolsGateway

        gateway = ToolsGateway()
    if tracer is None:
        tracer = get_tracer(settings, run_name="crag")
    book = _TraceBook()

    def _tid(config) -> str:
        return str((config or {}).get("configurable", {}).get("thread_id", ""))

    def condense_node(state: CRAGState, config=None) -> dict:
        question = state["question"]
        trace = book.open(tracer, _tid(config),
                          {"question": question, "threshold": threshold,
                           "max_rewrite": max_rewrite})
        history = state.get("history") or []
        if not history:  # 单轮：零 LLM，仅落 orig_question 便于统一取用
            return {"orig_question": question}
        condensed = condense_question(history, question, llm,
                                      force=bool(state.get("force_condense", False)))
        if trace is not None:
            trace.event("condense", old=question, new=condensed,
                        n_turns=len(history))
        return {"question": condensed, "orig_question": question}

    def route_node(state: CRAGState, config=None) -> dict:
        question = state["question"]
        trace = book.open(tracer, _tid(config),
                          {"question": question, "threshold": threshold,
                           "max_rewrite": max_rewrite})
        r = route_query(question, llm)
        hyde = hydep_expand(question, llm) if r == "fuzzy" else ""
        if trace is not None:
            trace.event("route", route=r, hyde_len=len(hyde))
        return {"route": r, "hyde": hyde}

    def retrieve_node(state: CRAGState, config=None) -> dict:
        trace = book.open(tracer, _tid(config),
                          {"question": state["question"], "threshold": threshold,
                           "max_rewrite": max_rewrite})
        query = state.get("rewritten") or state["question"]
        retr_query = query
        eff_top_k = state.get("top_k") or top_k  # invoke 级覆盖（API top_k 透传）
        if route:
            rname = state.get("route") or "default"
            # HyDE 拼接只在首检（查询仍为原问题）时生效；改写后的查询本身就是
            # 检索增强，再拼 HyDE 属于双重增强，无测试/证据支撑，不做。
            if (rname == "fuzzy" and state.get("hyde")
                    and not state.get("rewritten")):
                retr_query = f"{state['hyde']}\n{query}"
            chunks = retriever.retrieve(retr_query, top_k=eff_top_k, route=rname)
        else:
            chunks = retriever.retrieve(retr_query, top_k=eff_top_k)
        if trace is not None:
            trace.event("retrieve", query=retr_query, n_chunks=len(chunks),
                        top_k=eff_top_k)
        return {  # 首检顺带补齐默认值，保证终态字段齐全（重检不覆盖已有值）
            "chunks": chunks,
            "rewritten": state.get("rewritten", ""),
            "retries": state.get("retries", 0),
            "answer": state.get("answer", ""),
            "citations": state.get("citations", []),
            "handoff": state.get("handoff", False),
            "grade": state.get("grade", 0.0),
            "trace_meta": state.get("trace_meta",
                                    {"grades": [], "rewrites": [], "handoff": False}),
        }

    def grade_node(state: CRAGState, config=None) -> dict:
        trace = book.open(tracer, _tid(config),
                          {"question": state["question"], "threshold": threshold,
                           "max_rewrite": max_rewrite})
        query = state.get("rewritten") or state["question"]
        grade = grade_chunks(query, state.get("chunks", []), llm)
        meta = state.get("trace_meta") or {"grades": [], "rewrites": [], "handoff": False}
        meta = {**meta, "grades": [*meta.get("grades", []), grade]}
        if trace is not None:
            trace.event("grade", score=grade, threshold=threshold,
                        retries=state.get("retries", 0))
        return {"grade": grade, "trace_meta": meta}

    def rewrite_node(state: CRAGState, config=None) -> dict:
        rewritten = rewrite_query(state["question"], llm)
        meta = state.get("trace_meta") or {"grades": [], "rewrites": [], "handoff": False}
        meta = {**meta, "rewrites": [*meta.get("rewrites", []),
                                     {"from": state["question"], "to": rewritten}]}
        trace = book.open(tracer, _tid(config),
                          {"question": state["question"], "threshold": threshold,
                           "max_rewrite": max_rewrite})
        if trace is not None:
            trace.event("rewrite", old=state["question"], new=rewritten,
                        retries=state.get("retries", 0) + 1)
        return {"rewritten": rewritten, "retries": state.get("retries", 0) + 1,
                "trace_meta": meta}

    def diagnose_node(state: CRAGState, config=None) -> dict:
        """设备实况采集：实况问题（含打分门绕过直达的）调只读工具取实况。

        修复轮 1（t02 根因①）：按 select_state_tools 的**有序工具序列**逐个调用
        （如 shutdown/接口类 → 接口摘要 + 邻居表），每个输出各成一条【设备实况】
        伪片段进生成上下文与引用；单工具输出的证据缺口（被 shutdown 的接口在邻居
        表里只是"消失"）由接口视图补全。ping 需目标参数：从问题提取点分十进制
        IP，无可 ping 目标则该工具确定性退回接口摘要，不发必失败的废调用。
        非实况问题空过（不触 gateway）；fail-open：单个工具异常收敛为 tool_calls
        里的错误记录、继续其余工具，绝不阻断生成（lab 不可达时问答主链路照常）。
        """
        trace = book.open(tracer, _tid(config),
                          {"question": state["question"], "threshold": threshold,
                           "max_rewrite": max_rewrite})
        q = state.get("rewritten") or state["question"]
        if not is_device_state_query(q):
            return {"tool_calls": []}
        host = (state.get("host") or _extract_host(q)
                or getattr(gateway, "default_host", None))
        if not host:
            return {"tool_calls": []}
        calls: list[dict] = []
        for tool in select_state_tools(q):
            args: dict = {"host": host}
            if tool == "ping":
                m = _TARGET_RE.search(q)
                if m:
                    args["target"] = m.group(1)
                else:
                    tool = _DEFAULT_STATE_TOOLS[0]  # 无目标可 ping → 接口摘要
            try:
                out = gateway.read(tool, args)
            except Exception as e:  # noqa: BLE001 — 任何工具失败都不阻断问答
                out = f"[工具错误] {type(e).__name__}: {e}"
            calls.append({"tool": tool, "args": args,
                          "output": (out or "")[:_TOOL_OUTPUT_CAP]})
        if trace is not None:
            trace.event("diagnose", tool=calls[0]["tool"] if calls else "",
                        tools=[c["tool"] for c in calls], host=host,
                        output_len=sum(len(c["output"]) for c in calls))
        return {"tool_calls": calls}

    def generate_node(state: CRAGState, config=None) -> dict:
        question = state.get("rewritten") or state["question"]
        chunks = list(state.get("chunks", []))
        # 诊断实况以伪片段追加在手册片段之后：生成提示词与引用列表自然多一条
        # 「【设备实况】{host}」条目（tools=False 时 tool_calls 恒空，零影响）
        for tc in state.get("tool_calls") or []:
            pseudo = _device_state_chunk(tc)
            if pseudo is not None:
                chunks.append(pseudo)
        result = answer_with_citations(question, chunks, llm)
        book.close(_tid(config))
        return {"answer": result.text, "citations": result.citations,
                "handoff": False,
                "trace_meta": {**(state.get("trace_meta") or {}), "handoff": False}}

    def direct_answer_node(state: CRAGState, config=None) -> dict:
        """direct 路由终态：跳过检索/打分/生成，canned 回复且不转人工。"""
        book.close(_tid(config))
        meta = state.get("trace_meta") or {"grades": [], "rewrites": [], "handoff": False}
        return {"grade": 0.0, "chunks": [], "retries": state.get("retries", 0),
                "answer": DIRECT_ANSWER, "citations": [], "handoff": False,
                "trace_meta": {**meta, "handoff": False, "route": "direct"}}

    def fallback_node(state: CRAGState, config=None) -> dict:
        book.close(_tid(config))
        return {"answer": FALLBACK_ANSWER, "citations": [], "handoff": True,
                "trace_meta": {**(state.get("trace_meta") or {}), "handoff": True}}

    def grade_branch(state: CRAGState) -> str:
        """grade 后的条件边（原内部函数 route，为给 build 参数 route 让名而改名）。

        设备实况问题绕过打分门直达 diagnose（人工决策 2026-09-07，t17 失败模式）：
        实况问题的答案在设备上而非手册里，按手册片段打分必然低分，旧逻辑走
        改写→重检→fallback，diagnose 永不执行——手册打分对这类问题无意义，故
        tools=True 时 Regardless of grade 直达诊断（检索已在前序节点完成，诊断
        所需 chunks 齐备）；非实况问题保持原打分纠错路径不变。
        """
        if tools and is_device_state_query(state.get("rewritten") or state["question"]):
            return "diagnose"
        if state["grade"] >= threshold:
            return "diagnose" if tools else "generate"
        if state.get("retries", 0) < max_rewrite:
            return "rewrite"
        return "fallback"

    sg = StateGraph(CRAGState)
    sg.add_node("retrieve", retrieve_node)
    sg.add_node("grade", grade_node)
    sg.add_node("rewrite", rewrite_node)
    sg.add_node("generate", generate_node)
    sg.add_node("fallback", fallback_node)
    first = "retrieve"
    if route:
        sg.add_node("route", route_node)
        sg.add_node("direct_answer", direct_answer_node)
        first = "route"
    if tools:
        sg.add_node("diagnose", diagnose_node)
    if condense:
        sg.add_node("condense", condense_node)
        sg.set_entry_point("condense")
        sg.add_edge("condense", first)
    else:
        sg.set_entry_point(first)
    if route:
        sg.add_conditional_edges("route",
                                 lambda s: "direct" if s.get("route") == "direct"
                                 else "retrieve",
                                 {"retrieve": "retrieve", "direct": "direct_answer"})
    sg.add_edge("retrieve", "grade")
    grade_targets = {"generate": "generate", "rewrite": "rewrite",
                     "fallback": "fallback"}
    if tools:
        grade_targets["diagnose"] = "diagnose"
        sg.add_edge("diagnose", "generate")
    sg.add_conditional_edges("grade", grade_branch, grade_targets)
    sg.add_edge("rewrite", "retrieve")
    sg.add_edge("generate", END)
    sg.add_edge("fallback", END)
    return sg.compile(checkpointer=MemorySaver())
