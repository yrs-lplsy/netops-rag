"""CRAG 状态机单元测试：全 mock（FakeLLM/FakeRetriever/FakeTracer），零 API。

四条路径：
① 打分高 → 直接生成；② 打分低 → 改写重检 → 打分高 → 生成（retries+1）；
③ 打分低两次 → 拒答 handoff；④ 打分输出不可解析 → 视为低分走纠错。
外加：阈值边界（==threshold 算高）、JSON 解析鲁棒性、改写提示词保留型号实体、
一次 invoke 恰好一条 trace（含 grade/rewrite 事件）。
"""

import pytest

from netrag.agent.crag import (
    FALLBACK_ANSWER,
    CRAGState,
    _parse_grade,
    build_crag_graph,
    grade_chunks,
    rewrite_query,
)
from netrag.retrieval.base import RetrievedChunk


# ---------------------------------------------------------------------------
# 假件：脚本化 LLM、记录型检索器与 Tracer，零网络
# ---------------------------------------------------------------------------

class FakeLLM:
    """按脚本依次吐回复，并记录每次 chat 的入参供提示词断言。"""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def chat(self, messages, temperature=0.2, max_tokens=2048):
        self.calls.append({"messages": messages, "temperature": temperature,
                           "max_tokens": max_tokens})
        assert self.responses, "脚本回复耗尽：图发起了计划外的 LLM 调用"
        return self.responses.pop(0)


class FakeRetriever:
    name = "fake"

    def __init__(self, chunks):
        self.chunks = chunks
        self.queries = []

    def retrieve(self, query, top_k=5, filters=None):
        self.queries.append(query)
        return list(self.chunks)


class _RecSpan:
    def __init__(self, name, meta):
        self.name, self.meta, self.events = name, meta, []
        self.closed = False

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.closed = True
        return False

    def event(self, name, **kv):
        self.events.append((name, kv))


class FakeTracer:
    """记录 trace/span/event 的假 Tracer（替代 get_tracer 注入）。"""

    def __init__(self):
        self.traces = []

    def trace(self, name, meta=None):
        span = _RecSpan(name, meta)
        self.traces.append(span)
        return span


def _chunk(text="OSPF stub area 配置：router ospf 下执行 area 1 stub。"):
    return RetrievedChunk(chunk_id="c1", text=text, score=0.8, doc_id="d1",
                          breadcrumb="Catalyst 9300 > 路由配置 > OSPF",
                          vendor="cisco", model="Catalyst 9300", sw_version="17.6",
                          parent_id=None, parent_text=None)


def _graph(llm, retriever, tracer=None, threshold=6.0, max_rewrite=1):
    return build_crag_graph(retriever, llm, tracer=tracer,
                            threshold=threshold, max_rewrite=max_rewrite)


def _user_text(call):
    return "\n".join(m["content"] for m in call["messages"] if m["role"] == "user")


# ---------------------------------------------------------------------------
# 纯函数：打分解析与改写提示词
# ---------------------------------------------------------------------------

def test_parse_grade_variants():
    assert _parse_grade('{"score": 8}') == 8.0
    assert _parse_grade('```json\n{"score": 3}\n```') == 3.0
    assert _parse_grade("评分是 9 分") == 9.0
    assert _parse_grade("理由充分，给 10 分") == 10.0
    assert _parse_grade("完全无关，0 分") == 0.0  # 0 不在 1-10，视为解析失败
    assert _parse_grade("超出范围的 12 分") == 0.0  # 12 不在 1-10 → 0.0
    assert _parse_grade("我也不知道") == 0.0


def test_grade_chunks_one_call_and_score():
    llm = FakeLLM(['{"score": 7}'])
    q = "如何在 Catalyst 9300 上配置 OSPF 存根区域"
    assert grade_chunks(q, [_chunk()], llm) == 7.0
    assert len(llm.calls) == 1  # 恰好一次 LLM 调用
    assert q in _user_text(llm.calls[0])  # 问题进入提示词
    assert "OSPF" in _user_text(llm.calls[0])  # 片段文本进入提示词


def test_grade_chunks_empty_chunks_no_llm_call():
    llm = FakeLLM([])
    assert grade_chunks("q", [], llm) == 0.0
    assert llm.calls == []


def test_rewrite_prompt_keeps_model_entity():
    llm = FakeLLM(["Catalyst 9300 OSPF stub area 配置命令"])
    q = "如何在 Catalyst 9300 上配置 OSPF 存根区域"
    out = rewrite_query(q, llm)
    assert out == "Catalyst 9300 OSPF stub area 配置命令"
    assert len(llm.calls) == 1
    sent = _user_text(llm.calls[0])
    assert "Catalyst 9300" in sent  # 型号实体原样进入改写提示词
    assert "OSPF" in sent  # 原问题完整嵌入提示词
    assert "型号" in llm.calls[0]["messages"][0]["content"]  # system 明确要求保留型号/版本


def test_rewrite_query_falls_back_on_empty_output():
    llm = FakeLLM(["  "])
    assert rewrite_query("原始问题", llm) == "原始问题"


# ---------------------------------------------------------------------------
# 图：四条路径
# ---------------------------------------------------------------------------

CFG = lambda tid: {"configurable": {"thread_id": tid}}  # noqa: E731


def test_path1_high_grade_goes_straight_to_generate():
    llm = FakeLLM(['{"score": 8}', "答案：在 OSPF 下执行 area 1 stub。【出处】[1] OSPF"])
    retr = FakeRetriever([_chunk()])
    graph = _graph(llm, retr, FakeTracer())
    out = graph.invoke({"question": "如何在 Catalyst 9300 上配置 OSPF 存根区域"},
                       config=CFG("p1"))
    assert out["grade"] == 8.0
    assert out["answer"].startswith("答案：")
    assert out["citations"] == ["[1] Catalyst 9300 > 路由配置 > OSPF（d1）"]
    assert out["handoff"] is False
    assert out["retries"] == 0
    assert len(retr.queries) == 1  # 未改写，只检索一次
    assert len(llm.calls) == 2  # 1 次打分 + 1 次生成


def test_path2_low_grade_rewrites_then_generates():
    llm = FakeLLM([
        '{"score": 2}',  # 第一次打分：低
        "Catalyst 9300 OSPF stub area 配置命令",  # 改写
        '{"score": 7}',  # 重检打分：高
        "答案文本【出处】[1] OSPF",  # 生成
    ])
    retr = FakeRetriever([_chunk()])
    graph = _graph(llm, retr, FakeTracer())
    out = graph.invoke({"question": "Catalyst 9300 怎么配 OSPF 存根区域"},
                       config=CFG("p2"))
    assert out["retries"] == 1
    assert out["rewritten"] == "Catalyst 9300 OSPF stub area 配置命令"
    assert out["grade"] == 7.0
    assert out["handoff"] is False
    assert out["answer"].startswith("答案文本")
    assert retr.queries[0] == "Catalyst 9300 怎么配 OSPF 存根区域"  # 首检原问题
    assert retr.queries[1] == out["rewritten"]  # 重检用改写查询
    assert len(llm.calls) == 4  # 打分+改写+重检打分+生成


def test_path3_low_grade_twice_falls_back_to_handoff():
    llm = FakeLLM(['{"score": 3}', "改写后的问题", '{"score": 4}'])
    retr = FakeRetriever([_chunk("无关片段：交换机外观描述")])
    graph = _graph(llm, retr, FakeTracer())
    out = graph.invoke({"question": "如何配置 Kubernetes 网络插件"}, config=CFG("p3"))
    assert out["handoff"] is True
    assert out["answer"] == FALLBACK_ANSWER
    assert "手册中未找到相关内容" in out["answer"]
    assert "转人工" in out["answer"]
    assert out["citations"] == []
    assert out["retries"] == 1
    assert out["grade"] == 4.0
    assert len(llm.calls) == 3  # 打分+改写+重检打分，生成从未被调用


def test_path4_unparseable_grade_treated_low():
    llm = FakeLLM(["我不知道怎么评分", "改写后的查询", '{"score": 9}', "答案内容"])
    retr = FakeRetriever([_chunk()])
    graph = _graph(llm, retr, FakeTracer())
    out = graph.invoke({"question": "q1"}, config=CFG("p4"))
    assert out["trace_meta"]["grades"][0] == 0.0  # 垃圾输出 → 0.0 记为低分走纠错
    assert out["grade"] == 9.0  # 终态打分为重检后的高分
    assert out["handoff"] is False  # 改写重检后高分 → 正常生成
    assert out["retries"] == 1


def test_threshold_boundary_grade_equals_threshold_is_high():
    llm = FakeLLM(['{"score": 6}', "边界答案"])
    graph = _graph(llm, FakeRetriever([_chunk()]), FakeTracer(), threshold=6.0)
    out = graph.invoke({"question": "q"}, config=CFG("b1"))
    assert out["grade"] == 6.0
    assert out["handoff"] is False  # == threshold 算高，直接生成
    assert out["retries"] == 0


def test_threshold_boundary_just_below_goes_rewrite():
    llm = FakeLLM(['{"score": 5}', "改写", '{"score": 8}', "答案"])
    graph = _graph(llm, FakeRetriever([_chunk()]), FakeTracer(), threshold=6.0)
    out = graph.invoke({"question": "q"}, config=CFG("b2"))
    assert out["grade"] == 8.0
    assert out["retries"] == 1


def test_max_rewrite_zero_goes_straight_fallback():
    llm = FakeLLM(['{"score": 2}'])
    graph = _graph(llm, FakeRetriever([_chunk()]), FakeTracer(), max_rewrite=0)
    out = graph.invoke({"question": "q"}, config=CFG("m0"))
    assert out["handoff"] is True
    assert out["retries"] == 0
    assert len(llm.calls) == 1  # 只打分一次，无改写


# ---------------------------------------------------------------------------
# 观测与检查点
# ---------------------------------------------------------------------------

def test_one_trace_per_invocation_with_grade_and_rewrite_events():
    tracer = FakeTracer()
    llm = FakeLLM(['{"score": 2}', "改写", '{"score": 8}', "答案"])
    graph = _graph(llm, FakeRetriever([_chunk()]), tracer)
    graph.invoke({"question": "q"}, config=CFG("t1"))
    assert len(tracer.traces) == 1  # 一次 invoke 恰好一条 trace
    span = tracer.traces[0]
    assert span.name == "crag"
    assert span.closed is True  # 终态节点关闭 trace
    names = [n for n, _ in span.events]
    assert "grade" in names and "rewrite" in names
    grade_ev = [kv for n, kv in span.events if n == "grade"][0]
    assert grade_ev["score"] == 2.0
    assert grade_ev["threshold"] == 6.0


def test_trace_meta_records_grades_and_rewrite():
    llm = FakeLLM(['{"score": 2}', "改写", '{"score": 8}', "答案"])
    graph = _graph(llm, FakeRetriever([_chunk()]), FakeTracer())
    out = graph.invoke({"question": "q"}, config=CFG("t2"))
    assert out["trace_meta"]["grades"] == [2.0, 8.0]
    assert out["trace_meta"]["rewrites"] == [
        {"from": "q", "to": "改写"}]
    assert out["trace_meta"]["handoff"] is False


def test_state_has_all_spec_fields_after_run():
    llm = FakeLLM(['{"score": 8}', "答案"])
    graph = _graph(llm, FakeRetriever([_chunk()]), FakeTracer())
    out = graph.invoke({"question": "q"}, config=CFG("s1"))
    for key in ("question", "rewritten", "chunks", "grade", "retries",
                "answer", "citations", "handoff", "trace_meta"):
        assert key in out
        assert key in CRAGState.__annotations__  # TypedDict 形状固定
    assert isinstance(out["chunks"], list) and out["chunks"]


def test_memory_checkpointer_with_thread_id():
    graph = _graph(FakeLLM(['{"score": 8}', "答案"]), FakeRetriever([_chunk()]),
                   FakeTracer())
    assert graph.checkpointer is not None  # MemorySaver 已挂
    out = graph.invoke({"question": "q"}, config=CFG("ck1"))
    assert out["answer"] == "答案"
