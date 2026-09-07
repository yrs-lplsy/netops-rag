"""CRAG 多轮指代消解集成测试：build_crag_graph(condense=True) 的最小改动验证。

- 带 history + 指代词 → condense 节点一次 LLM 改写，检索用改写后问题，
  原问题保留在 orig_question；
- 无 history → 零额外 LLM 调用，检索用原问题；
- 默认 condense=False 保持 T7 旧行为（state 里塞 history 也不触发）。
"""

from netrag.agent.crag import build_crag_graph
from netrag.retrieval.base import RetrievedChunk


class FakeLLM:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def chat(self, messages, temperature=0.2, max_tokens=2048):
        self.calls.append({"messages": messages})
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
    return RetrievedChunk(chunk_id="c1", text="S5735 生成树模式：STP/RSTP/MSTP。",
                          score=0.8, doc_id="d1", breadcrumb="S5735 > 生成树",
                          vendor="huawei", model="S5735", sw_version="V200R019",
                          parent_id=None, parent_text=None)


CFG = lambda tid: {"configurable": {"thread_id": tid}}  # noqa: E731
HISTORY = [("华为S5735支持多少VLAN？", "S5735支持最多32个VLAN。")]


def test_condense_rewrites_question_for_retrieval_and_keeps_original():
    llm = FakeLLM(["华为S5735交换机支持哪些生成树模式？",  # condense
                   '{"score": 8}', "答案【出处】[1] 生成树"])  # 打分+生成
    retr = FakeRetriever([_chunk()])
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), condense=True)
    out = graph.invoke({"question": "它的生成树模式有哪些？", "history": HISTORY},
                       config=CFG("c1"))
    assert retr.queries[0] == "华为S5735交换机支持哪些生成树模式？"  # 检索用改写问题
    assert out["question"] == "华为S5735交换机支持哪些生成树模式？"
    assert out["orig_question"] == "它的生成树模式有哪些？"  # 原问题保留供引用/调试
    assert out["handoff"] is False
    assert len(llm.calls) == 3  # condense+打分+生成，无多余调用


def test_condense_with_history_but_no_referent_skips_llm():
    llm = FakeLLM(['{"score": 8}', "答案"])
    retr = FakeRetriever([_chunk()])
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), condense=True)
    q = "如何在 Catalyst 9300 上配置 OSPF 存根区域"  # 无指代词
    out = graph.invoke({"question": q, "history": HISTORY}, config=CFG("c2"))
    assert retr.queries[0] == q  # 原问题直通检索
    assert out["orig_question"] == q
    assert len(llm.calls) == 2  # 只打分+生成，condense 零调用


def test_condense_no_history_zero_extra_calls():
    llm = FakeLLM(['{"score": 8}', "答案"])
    retr = FakeRetriever([_chunk()])
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), condense=True)
    out = graph.invoke({"question": "它的生成树模式有哪些？"}, config=CFG("c3"))
    assert retr.queries[0] == "它的生成树模式有哪些？"  # 无历史不改写
    assert out["orig_question"] == "它的生成树模式有哪些？"
    assert len(llm.calls) == 2  # 打分+生成，condense 零调用


def test_default_condense_off_keeps_t7_behavior():
    llm = FakeLLM(['{"score": 8}', "答案"])
    retr = FakeRetriever([_chunk()])
    graph = build_crag_graph(retr, llm, tracer=FakeTracer())  # 默认 condense=False
    out = graph.invoke({"question": "q", "history": HISTORY}, config=CFG("c4"))
    assert retr.queries[0] == "q"  # history 被忽略
    assert len(llm.calls) == 2  # 不触发 condense 调用
    assert "orig_question" not in out or out.get("orig_question") == "q"


def test_force_condense_flag_bypasses_heuristic_in_graph():
    llm = FakeLLM(["Catalyst 9300 OSPF stub area 配置", '{"score": 8}', "答案"])
    retr = FakeRetriever([_chunk()])
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), condense=True)
    q = "如何在 Catalyst 9300 上配置 OSPF 存根区域"  # 无指代词
    out = graph.invoke({"question": q, "history": HISTORY, "force_condense": True},
                       config=CFG("c5"))
    assert retr.queries[0] == "Catalyst 9300 OSPF stub area 配置"
    assert out["orig_question"] == q
    assert len(llm.calls) == 3


def test_condense_event_in_trace():
    tracer = FakeTracer()
    llm = FakeLLM(["华为S5735支持哪些生成树模式？", '{"score": 8}', "答案"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=tracer,
                             condense=True)
    graph.invoke({"question": "它的生成树模式有哪些？", "history": HISTORY},
                 config=CFG("c6"))
    assert len(tracer.traces) == 1  # 一次 invoke 仍恰好一条 trace
    names = [n for n, _ in tracer.traces[0].events]
    assert "condense" in names and "grade" in names
