"""CRAG 查询路由集成测试：build_crag_graph(route=True) 的最小改动验证。

- route=True 时 condense 后（或图入口）插 route 节点：exact→BM25 检索器、
  fuzzy→HyDE+拼接查询走 dense 检索器、direct→跳过检索直接 canned 回复；
- 垃圾分类 fail-safe 回 fuzzy；
- 默认 route=False 保持 T7/T8 行为（传 RoutedRetriever 也走默认路径）。
全 mock（FakeLLM/FakeRetriever/FakeTracer/RoutedRetriever 映射），零网络。
"""

import pytest

from netrag.agent.crag import CRAGState, build_crag_graph
from netrag.agent.query_router import RoutedRetriever
from netrag.retrieval.base import RetrievedChunk


class FakeLLM:
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

    def __init__(self, tag=""):
        self.tag = tag
        self.chunks = []
        self.queries = []

    def retrieve(self, query, top_k=5, filters=None):
        self.queries.append(query)
        return list(self.chunks)


class FakeTracer:
    def __init__(self):
        self.traces = []

    def trace(self, name, meta=None):
        span = _RecSpan(name, meta)
        self.traces.append(span)
        return span


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


def _chunk():
    return RetrievedChunk(chunk_id="c1", text="display interface brief 显示接口简要状态。",
                          score=0.8, doc_id="d1", breadcrumb="S5735 > 接口管理",
                          vendor="huawei", model="S5735", sw_version="V200R019",
                          parent_id=None, parent_text=None)


def _routed(exact=None, fuzzy=None, default=None):
    def seeded(tag):
        r = FakeRetriever(tag)
        r.chunks = [_chunk()]  # 有片段→正常打分路径（空片段会跳打分走改写）
        return r
    return RoutedRetriever({
        "exact": exact or seeded("bm25"),
        "fuzzy": fuzzy or seeded("dense"),
        "default": default or seeded("full"),
    })


CFG = lambda tid: {"configurable": {"thread_id": tid}}  # noqa: E731
Q = "display interface brief 的作用"
HYDE = "本节介绍display interface brief命令：用于查看接口简要状态，包括链路_up/down_与速率。"


# ---------------------------------------------------------------------------
# exact：BM25 检索器直查
# ---------------------------------------------------------------------------

def test_exact_route_uses_bm25_retriever_only():
    llm = FakeLLM(["exact", '{"score": 8}', "答案【出处】[1] 接口"])
    retr = _routed()
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), route=True)
    out = graph.invoke({"question": Q}, config=CFG("r1"))
    assert out["route"] == "exact"
    assert out["hyde"] == ""  # exact 不做 HyDE
    assert retr.for_route("exact").queries == [Q]  # BM25 检索器收到原问题
    assert retr.for_route("fuzzy").queries == []  # dense 未被使用
    assert retr.for_route("default").queries == []  # 通用三路未被使用
    assert out["handoff"] is False
    assert len(llm.calls) == 3  # 路由+打分+生成，无 HyDE 调用


def test_exact_route_retry_after_rewrite_still_bm25():
    llm = FakeLLM(["exact", '{"score": 2}', "display interface brief 命令详解",
                   '{"score": 8}', "答案"])
    retr = _routed()
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), route=True)
    out = graph.invoke({"question": Q}, config=CFG("r2"))
    bm25_q = retr.for_route("exact").queries
    assert bm25_q == [Q, "display interface brief 命令详解"]  # 重检仍走 BM25 检索器
    assert out["retries"] == 1


# ---------------------------------------------------------------------------
# fuzzy：HyDE + 拼接查询走 dense
# ---------------------------------------------------------------------------

def test_fuzzy_route_hyde_then_dense_with_concatenated_query():
    q = "交换机端口频繁up-down怎么排查"
    llm = FakeLLM(["fuzzy", HYDE, '{"score": 8}', "答案【出处】[1] 接口"])
    retr = _routed()
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), route=True)
    out = graph.invoke({"question": q}, config=CFG("r3"))
    assert out["route"] == "fuzzy"
    assert out["hyde"] == HYDE
    dense = retr.for_route("fuzzy")
    assert dense.queries == [f"{HYDE}\n{q}"]  # hyde 段落 + 原问题 拼接检索
    assert retr.for_route("exact").queries == []
    assert retr.for_route("default").queries == []
    assert len(llm.calls) == 4  # 路由+HyDE+打分+生成


def test_fuzzy_route_empty_hyde_falls_back_to_question():
    q = "网络很卡"
    llm = FakeLLM(["fuzzy", "", '{"score": 8}', "答案"])
    retr = _routed()
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), route=True)
    out = graph.invoke({"question": q}, config=CFG("r4"))
    assert out["route"] == "fuzzy" and out["hyde"] == ""
    assert retr.for_route("fuzzy").queries == [q]  # HyDE 垃圾 → 原问题直查


def test_garbage_route_falls_back_to_fuzzy_path():
    q = "随便问一句奇怪的话"
    llm = FakeLLM([" blah blah ", HYDE, '{"score": 8}', "答案"])
    retr = _routed()
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), route=True)
    out = graph.invoke({"question": q}, config=CFG("r5"))
    assert out["route"] == "fuzzy"  # 垃圾分类 fail-safe → fuzzy
    assert retr.for_route("fuzzy").queries == [f"{HYDE}\n{q}"]
    assert len(llm.calls) == 4  # 路由+HyDE（fuzzy 路径补 HyDE）+打分+生成


# ---------------------------------------------------------------------------
# direct：跳过检索，canned 回复不转人工
# ---------------------------------------------------------------------------

def test_direct_route_skips_retrieval_answers_canned():
    llm = FakeLLM(["direct"])
    retr = _routed()
    tracer = FakeTracer()
    graph = build_crag_graph(retr, llm, tracer=tracer, route=True)
    out = graph.invoke({"question": "今天天气怎么样"}, config=CFG("r6"))
    assert out["route"] == "direct"
    assert out["chunks"] == [] and out["citations"] == []
    assert out["grade"] == 0.0
    assert out["handoff"] is False  # 超纲不是系统故障，不转人工
    assert "网络设备运维" in out["answer"]  # canned 回复说明知识库范围
    assert len(llm.calls) == 1  # 只有路由一次调用
    for r in (retr.for_route("exact"), retr.for_route("fuzzy"), retr.for_route("default")):
        assert r.queries == []  # 三路检索器全部未被使用
    assert tracer.traces[0].closed is True  # direct_answer 是终态节点，关闭 trace


def test_direct_route_state_fields_present():
    from netrag.agent.crag import DIRECT_ANSWER
    llm = FakeLLM(["direct"])
    graph = build_crag_graph(_routed(), llm, tracer=FakeTracer(), route=True)
    out = graph.invoke({"question": "你好"}, config=CFG("r7"))
    assert out["answer"] == DIRECT_ANSWER
    for key in ("route", "hyde", "question", "chunks", "grade", "answer",
                "citations", "handoff", "trace_meta"):
        assert key in out
        assert key in CRAGState.__annotations__


# ---------------------------------------------------------------------------
# 组合与默认关闭
# ---------------------------------------------------------------------------

def test_route_with_condense_ordering():
    q = "它的生成树模式有哪些？"
    llm = FakeLLM(["华为S5735支持哪些生成树模式？",  # condense
                   "exact",  # route
                   '{"score": 8}', "答案"])
    retr = _routed()
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), condense=True, route=True)
    out = graph.invoke({"question": q, "history": [("华为S5735支持多少VLAN？", "32个。")]},
                       config=CFG("r8"))
    assert retr.for_route("exact").queries == ["华为S5735支持哪些生成树模式？"]  # condense 结果进路由后的检索
    assert out["orig_question"] == q
    assert out["route"] == "exact"
    assert len(llm.calls) == 4  # condense+路由+打分+生成


def test_route_event_recorded_in_trace():
    tracer = FakeTracer()
    llm = FakeLLM(["exact", '{"score": 8}', "答案"])
    graph = build_crag_graph(_routed(), llm, tracer=tracer, route=True)
    graph.invoke({"question": Q}, config=CFG("r9"))
    assert len(tracer.traces) == 1  # 一次 invoke 仍恰好一条 trace
    events = [n for n, _ in tracer.traces[0].events]
    assert "route" in events and "retrieve" in events and "grade" in events


def test_default_route_off_keeps_t7_behavior_even_with_routed_retriever():
    llm = FakeLLM(['{"score": 8}', "答案"])
    retr = _routed()
    graph = build_crag_graph(retr, llm, tracer=FakeTracer())  # 默认 route=False
    out = graph.invoke({"question": Q}, config=CFG("r10"))
    assert retr.for_route("default").queries == [Q]  # 不分类，走 default 检索器自身逻辑
    assert retr.for_route("exact").queries == []
    assert "route" not in out or out.get("route") in ("", None)
    assert len(llm.calls) == 2  # 打分+生成，无路由调用


def test_route_node_reclassifies_over_preexisting_state_route():
    # state 里已带 route（检查点续跑/手工 invoke）→ route 节点重新分类并覆盖；
    # retrieve 侧对未知 route 名也回 default，双保险
    llm = FakeLLM(["exact", '{"score": 8}', "答案"])
    retr = _routed()
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), route=True)
    out = graph.invoke({"question": Q, "route": "unknown-x"}, config=CFG("r11"))
    assert out["route"] == "exact"  # 重新分类覆盖外部传入值
    assert retr.for_route("exact").queries == [Q]
    assert out["handoff"] is False


@pytest.mark.parametrize("route_flag", [False], ids=["explicit-off"])
def test_route_param_explicit_off(route_flag):
    llm = FakeLLM(['{"score": 8}', "答案"])
    retr = _routed()
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), route=route_flag)
    out = graph.invoke({"question": Q}, config=CFG("r12"))
    assert retr.for_route("default").queries == [Q]
    assert len(llm.calls) == 2
