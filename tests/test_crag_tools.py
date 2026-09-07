"""CRAG 诊断路由（tools=True）单测：mock Gateway + mock LLM，零网络零设备。

覆盖：
- 设备实况问题启发式分类（is_device_state_query）与工具映射（select_state_tools，
  值为有序工具元组：diagnose 按序调用全部）、问题中 host 提取；
- diagnose 节点在实况问题上绕过打分门直达（手册打分对实况问题无意义，t17 失败
  模式），非实况问题保持原打分纠错路径且不触 gateway；经
  gateway.read(tool, {"host": ...}) 取设备实况；
- 工具输出以「【设备实况】{host}」伪片段注入生成上下文，引用列表追加设备实况条目；
- 工具异常 fail-open（记入 tool_calls，不阻断问答主链路）；
- 默认 tools=False 与 T7-T9 行为完全一致（gateway 不被触碰）。
"""

import pytest

from netrag.agent.crag import (
    CRAGState,
    _extract_host,
    build_crag_graph,
    is_device_state_query,
    select_state_tools,
)
from netrag.retrieval.base import RetrievedChunk


# ---------------------------------------------------------------------------
# 假件：mock Gateway / LLM / Retriever / Tracer（与 T7-T9 测试同构）
# ---------------------------------------------------------------------------

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

    def __init__(self, chunks):
        self.chunks = chunks
        self.queries = []
        self.top_ks = []

    def retrieve(self, query, top_k=5, filters=None):
        self.queries.append(query)
        self.top_ks.append(top_k)
        return list(self.chunks)


class FakeGateway:
    """记录 read 调用的假网关：按工具名回放脚本输出，可注入异常。"""

    default_host = None

    def __init__(self, outputs=None, error=None, default_host=None):
        self.calls = []
        self.outputs = outputs or {}
        self.error = error
        if default_host is not None:
            self.default_host = default_host

    def read(self, tool, args):
        self.calls.append((tool, dict(args)))
        if self.error is not None:
            raise self.error
        return self.outputs.get(tool, f"{tool}@{args.get('host')} 输出")


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
    def __init__(self):
        self.traces = []

    def trace(self, name, meta=None):
        span = _RecSpan(name, meta)
        self.traces.append(span)
        return span


def _chunk(text="OSPF 邻居排障：show ip ospf neighbor 查看 Full 状态。"):
    return RetrievedChunk(chunk_id="c1", text=text, score=0.8, doc_id="d1",
                          breadcrumb="Catalyst 9300 > 路由配置 > OSPF",
                          vendor="cisco", model="Catalyst 9300", sw_version="17.6",
                          parent_id=None, parent_text=None)


CFG = lambda tid: {"configurable": {"thread_id": tid}}  # noqa: E731
Q = "core1 的 OSPF 邻居状态怎么样"


def _user_text(call):
    return "\n".join(m["content"] for m in call["messages"] if m["role"] == "user")


# ---------------------------------------------------------------------------
# 启发式：分类 / 工具映射 / host 提取
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("q", [
    "core1 的 OSPF 邻居状态怎么样",
    "acc1 当前日志有什么报错",
    "查看接口状态",
    "show ip ospf neighbor",
    "display interface brief",
    "接口 up/down 了怎么办",
])
def test_heuristic_true_on_device_state_questions(q):
    assert is_device_state_query(q) is True


@pytest.mark.parametrize("q", [
    "如何在 Catalyst 9300 上配置 OSPF 存根区域",
    "华为S5735支持多少VLAN",
    "生成树模式的配置命令有哪些",
    "今天天气怎么样",
])
def test_heuristic_false_on_manual_or_offtopic_questions(q):
    assert is_device_state_query(q) is False


@pytest.mark.parametrize("q,tools", [
    ("core1 的 OSPF 邻居状态怎么样", ("show_ospf_neighbor",)),
    ("acc1 的日志看看", ("show_logging",)),
    ("arp 表里有啥", ("get_arp_table",)),
    # 修复（t23-t28 闭合）：vlan 类二元组——show_vlan 证子接口存在/失链（down 子接口
    # 无地址列，brief 不显示地址），running-config 的 `no ip address`+迁移命令序列
    # 才能归因「地址迁到哪个新标签」，证据链闭合（与 shutdown/cost 类同构）
    ("vlan 信息查看", ("show_vlan", "get_running_config")),
    ("core2 版本是多少", ("show_version",)),
    # 修复轮 1（t02 根因）：shutdown/接口类 → 接口摘要在前（含接口名与 up/down）、
    # 邻居表佐证；修复轮 2（t02 闭合）：+get_running_config 补 `shutdown` 配置行，
    # 归因「管理性关闭」证据闭合。diagnose 按序调用元组内全部工具
    ("接口状态如何", ("show_ip_interface_brief", "show_ospf_neighbor",
                      "get_running_config")),
    ("当前 running 配置", ("get_running_config",)),
    # 人工决策（2026-09-07）：新增 show_ip_route/ping 两个只读工具的映射；
    # 收尾轮（与 shutdown 同构）：cost 类补 get_running_config——路由表证「绕路
    # 存在」（异常 cost 不显式可见），running-config 的 `ip ospf cost 65535` 行归因
    ("core1 到 core2 的流量绕路了，检查下配置",
     ("show_ip_route", "get_running_config")),
    ("流量路径好像绕远了", ("show_ip_route", "get_running_config")),
    ("10.100.0.2 好像不通了", ("ping",)),  # 无更具体关键词的「不通」问题 → ping（次选）
])
def test_select_state_tools_mapping(q, tools):
    assert select_state_tools(q) == tools


def test_select_state_tools_priority_pins_for_e2e_questions():
    """优先级锚（修复轮 1 重排：vlan 先于 接口、接口 先于 邻居；修复轮 2 三元组）：
    - t01/t02（含 接口+邻居）→ 接口三元组（证据链闭合：down → 邻居消失 → shutdown 行）；
    - t30（VLAN 子接口）→ 仍命中 vlan 二元组（「子接口」不得劫持 VLAN 类问题）；
    - t17（检查/配置）→ get_running_config。"""
    triple = ("show_ip_interface_brief", "show_ospf_neighbor", "get_running_config")
    assert select_state_tools(
        "core1 与 acc1 之间的 OSPF 邻居关系突然断了，这条链路好像不通了，帮我看看接口状态"
    ) == triple  # t01
    assert select_state_tools(
        "core1 的 eth3 接口好像有问题，OSPF 邻居关系断了，业务也中断了，帮我看看"
    ) == triple  # t02
    assert select_state_tools(
        "acc1 的 VLAN100 子接口的 IP 好像没了，帮我确认一下配置"
    ) == ("show_vlan", "get_running_config")  # t30 不回归
    assert select_state_tools(
        "core2 的 eth1 端口描述好像被人改过，帮我检查下当前的配置"
    ) == ("get_running_config",)  # t17 不回归
    # t07（cost 类）→ 绕路先于 配置 命中二元组；绕路问题不被 配置 单工具截胡
    assert select_state_tools(
        "core1 到 core2 的流量这两天绕路了，延迟明显变大，帮我检查下配置有没有被动过"
    ) == ("show_ip_route", "get_running_config")


def test_select_state_tools_default_for_unmapped_state_query():
    assert select_state_tools("查看设备信息") == ("show_ip_interface_brief",)


def test_extract_host_from_question():
    assert _extract_host(Q) == "core1"
    assert _extract_host("acc2 的日志") == "acc2"
    assert _extract_host("OSPF 邻居状态怎么样") == ""  # 无主机名 → 空串


# ---------------------------------------------------------------------------
# diagnose 节点：高分路径经 gateway 取设备实况
# ---------------------------------------------------------------------------

def test_diagnose_calls_gateway_with_expected_tool_and_host():
    gw = FakeGateway({"show_ospf_neighbor": "Neighbor 10.0.0.2 Full"})
    llm = FakeLLM(['{"score": 8}', "邻居全 Full。"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw)
    out = graph.invoke({"question": Q}, config=CFG("d1"))
    assert gw.calls == [("show_ospf_neighbor", {"host": "core1"})]
    assert out["tool_calls"] == [
        {"tool": "show_ospf_neighbor", "args": {"host": "core1"},
         "output": "Neighbor 10.0.0.2 Full"}]


def test_host_param_overrides_question_extraction():
    gw = FakeGateway(default_host="core1")
    llm = FakeLLM(['{"score": 8}', "答案"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw)
    out = graph.invoke({"question": "OSPF 邻居状态怎么样", "host": "acc2"},
                       config=CFG("d2"))
    assert gw.calls == [("show_ospf_neighbor", {"host": "acc2"})]
    assert out["tool_calls"][0]["args"] == {"host": "acc2"}


def test_gateway_default_host_used_when_no_host_anywhere():
    gw = FakeGateway(default_host="core1")
    llm = FakeLLM(['{"score": 8}', "答案"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw)
    graph.invoke({"question": "OSPF 邻居状态怎么样"}, config=CFG("d3"))
    assert gw.calls == [("show_ospf_neighbor", {"host": "core1"})]


def test_non_device_state_question_skips_gateway():
    gw = FakeGateway()
    llm = FakeLLM(['{"score": 8}', "答案"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw)
    out = graph.invoke({"question": "如何在 Catalyst 9300 上配置 OSPF 存根区域"},
                       config=CFG("d4"))
    assert gw.calls == []
    assert out["tool_calls"] == []
    assert len(llm.calls) == 2  # 打分+生成，无诊断插页


def test_ping_tool_target_extracted_from_question():
    """ping 需要目标参数：从问题提取点分十进制 IP 作为 target 传入 gateway。"""
    gw = FakeGateway({"ping": "0% packet loss"})
    llm = FakeLLM(['{"score": 8}', "可达。"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw)
    out = graph.invoke({"question": "core1 到 10.0.12.2 好像不通了"},
                       config=CFG("d4b"))
    assert gw.calls == [("ping", {"host": "core1", "target": "10.0.12.2"})]
    assert out["tool_calls"][0]["tool"] == "ping"


def test_interface_class_question_diagnoses_tool_sequence_in_order():
    """修复轮 1（t02 根因）：shutdown/接口类问题按序调用元组内全部工具，每个输出
    各成一条【设备实况】伪片段进生成上下文与引用；修复轮 2 补第三工具
    get_running_config——`shutdown` 配置行闭合「管理性关闭」归因。"""
    gw = FakeGateway({
        "show_ip_interface_brief": "eth3 down/down 无地址",
        "show_ospf_neighbor": "10.255.0.2 Full eth1",
        "get_running_config": "interface eth3\n shutdown",
    })
    llm = FakeLLM(['{"score": 8}', "core1 的 eth3 被管理性 shutdown。"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw)
    out = graph.invoke({"question": "core1 的 eth3 接口好像有问题，OSPF 邻居关系断了，业务也中断了，帮我看看"},
                       config=CFG("d4d"))
    assert gw.calls == [("show_ip_interface_brief", {"host": "core1"}),
                        ("show_ospf_neighbor", {"host": "core1"}),
                        ("get_running_config", {"host": "core1"})]
    assert [c["tool"] for c in out["tool_calls"]] == [
        "show_ip_interface_brief", "show_ospf_neighbor", "get_running_config"]
    gen = _user_text(llm.calls[1])
    assert "eth3 down/down 无地址" in gen  # 证据链含 eth3 相关输出
    assert "10.255.0.2 Full eth1" in gen
    assert "shutdown" in gen  # 配置行可归因「管理性关闭」
    assert out["citations"][-3:] == [
        "[2] 【设备实况】core1（mcp:show_ip_interface_brief）",
        "[3] 【设备实况】core1（mcp:show_ospf_neighbor）",
        "[4] 【设备实况】core1（mcp:get_running_config）",
    ]


def test_ping_without_target_in_question_falls_back_to_default_tool():
    """问题里无可 ping 的目标地址 → 确定性退回接口摘要，不发必失败的废调用。"""
    gw = FakeGateway()
    llm = FakeLLM(['{"score": 8}', "答案"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw)
    out = graph.invoke({"question": "core1 与 acc1 之间的链路好像不通了，帮我看看"},
                       config=CFG("d4c"))
    assert gw.calls == [("show_ip_interface_brief", {"host": "core1"})]
    assert out["tool_calls"][0]["tool"] == "show_ip_interface_brief"


def test_tool_output_injected_into_generation_context_and_citations():
    gw = FakeGateway({"show_ospf_neighbor": "10.0.0.2 1 FULL/DR 00:00:11 10.0.12.2"})
    llm = FakeLLM(['{"score": 8}', "core1 有邻居处于 Full 状态。"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw)
    out = graph.invoke({"question": Q}, config=CFG("d5"))
    gen = _user_text(llm.calls[1])
    assert "【设备实况】core1" in gen  # 实况片段进入生成提示词
    assert "FULL/DR" in gen  # 工具原文可见
    assert "10.0.12.2" in gen
    assert out["citations"] == [
        "[1] Catalyst 9300 > 路由配置 > OSPF（d1）",
        "[2] 【设备实况】core1（mcp:show_ospf_neighbor）",  # 引用追加设备实况条目
    ]
    assert out["handoff"] is False


def test_tool_error_fail_open_answer_still_generated():
    gw = FakeGateway(error=RuntimeError("lab down"))
    llm = FakeLLM(['{"score": 8}', "手册答案"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw)
    out = graph.invoke({"question": Q}, config=CFG("d6"))
    assert out["answer"] == "手册答案"  # 生成未被工具异常阻断
    assert "工具错误" in out["tool_calls"][0]["output"]
    assert "RuntimeError" in out["tool_calls"][0]["output"]
    # 错误文本同样作为实况注入（LLM 可感知"设备不可达"），引用仍有实况条目
    assert out["citations"] == [
        "[1] Catalyst 9300 > 路由配置 > OSPF（d1）",
        "[2] 【设备实况】core1（mcp:show_ospf_neighbor）",
    ]


def test_long_tool_output_truncated():
    gw = FakeGateway({"show_ospf_neighbor": "x" * 5000})
    llm = FakeLLM(['{"score": 8}', "答案"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw)
    out = graph.invoke({"question": Q}, config=CFG("d7"))
    assert len(out["tool_calls"][0]["output"]) == 2000  # 截断上限，护住提示词窗口


# ---------------------------------------------------------------------------
# 与纠错路径/路由路径的交互
# ---------------------------------------------------------------------------

def test_state_question_low_grade_bypasses_grade_gate_to_diagnose():
    """实况问题不被手册打分门拦截：打分再低也直达 diagnose（t17 失败模式修复）。

    手册片段对「查设备当前状态」类问题本就不构成可回答依据，按手册打分必然低分，
    旧逻辑 → 改写重检 → fallback，diagnose 永不执行；绕过后零改写、零二次打分。
    """
    gw = FakeGateway({"get_running_config": "description xx-unknown-777"})
    llm = FakeLLM(['{"score": 1}', "core2 的 eth1 描述被改为 xx-unknown-777。"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw)
    out = graph.invoke({"question": "core2 的 eth1 端口描述好像被人改过，帮我检查下当前的配置"},
                       config=CFG("d8"))
    assert gw.calls == [("get_running_config", {"host": "core2"})]
    assert out["retries"] == 0  # 不再先浪费一次改写重检
    assert len(llm.calls) == 2  # 打分 + 生成（无改写、无二次打分）
    assert out["handoff"] is False


def test_state_question_diagnose_even_when_retries_exhausted():
    """重试额度耗尽的实况问题也不 fallback：诊断直达而非拒答（tools=True 语义）。"""
    gw = FakeGateway()
    llm = FakeLLM(['{"score": 2}', "答案"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw, max_rewrite=0)
    out = graph.invoke({"question": Q}, config=CFG("d8b"))
    assert out["handoff"] is False
    assert gw.calls == [("show_ospf_neighbor", {"host": "core1"})]


def test_non_state_low_grade_still_rewrites_and_never_calls_gateway():
    """非实况问题保持原纠错路径：低分 → 改写重检（gateway 全程不被触碰）。"""
    gw = FakeGateway()
    llm = FakeLLM(['{"score": 2}', "Catalyst 9300 OSPF 存根区域配置命令",
                   '{"score": 8}', "答案"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw)
    out = graph.invoke({"question": "如何在 Catalyst 9300 上配置 OSPF 存根区域"},
                       config=CFG("d8c"))
    assert out["retries"] == 1
    assert gw.calls == []
    assert out["tool_calls"] == []
    assert len(llm.calls) == 4  # 打分+改写+重检打分+生成


def test_fallback_path_never_calls_gateway():
    """非实况问题重试额度耗尽 → 仍 fallback，且 fallback 永不触 gateway。"""
    gw = FakeGateway()
    llm = FakeLLM(['{"score": 2}'])
    graph = build_crag_graph(FakeRetriever([_chunk("无关")]), llm, tracer=FakeTracer(),
                             tools=True, gateway=gw, max_rewrite=0)
    out = graph.invoke({"question": "今天天气怎么样"}, config=CFG("d9"))
    assert out["handoff"] is True
    assert gw.calls == []


def test_direct_route_with_tools_skips_diagnose():
    from netrag.agent.query_router import RoutedRetriever

    def seeded():
        r = FakeRetriever([_chunk()])
        return r

    gw = FakeGateway()
    llm = FakeLLM(["direct"])
    retr = RoutedRetriever({"default": seeded()})
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), route=True,
                             tools=True, gateway=gw)
    out = graph.invoke({"question": "今天天气怎么样"}, config=CFG("d10"))
    assert out["route"] == "direct"
    assert gw.calls == []  # direct 终态不触设备
    assert "tool_calls" not in out or out["tool_calls"] in ([], None)


def test_diagnose_event_in_single_trace():
    tracer = FakeTracer()
    gw = FakeGateway()
    llm = FakeLLM(['{"score": 8}', "答案"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=tracer,
                             tools=True, gateway=gw)
    graph.invoke({"question": Q}, config=CFG("d11"))
    assert len(tracer.traces) == 1  # 一次 invoke 仍恰好一条 trace
    events = dict(tracer.traces[0].events)
    assert "diagnose" in events
    assert events["diagnose"]["tool"] == "show_ospf_neighbor"


# ---------------------------------------------------------------------------
# 兼容保证：tools=False 与 T7-T9 一致
# ---------------------------------------------------------------------------

def test_tools_false_default_never_touches_gateway():
    gw = FakeGateway()
    llm = FakeLLM(['{"score": 8}', "答案"])
    graph = build_crag_graph(FakeRetriever([_chunk()]), llm, tracer=FakeTracer(),
                             gateway=gw)  # 默认 tools=False
    out = graph.invoke({"question": Q}, config=CFG("c1"))
    assert gw.calls == []
    assert "tool_calls" not in out or out["tool_calls"] in ([], None)
    assert out["citations"] == ["[1] Catalyst 9300 > 路由配置 > OSPF（d1）"]
    assert len(llm.calls) == 2


def test_top_k_state_override_per_invocation():
    """state["top_k"] 覆盖构建默认（API /ask 的 top_k 透传机制）。"""
    llm = FakeLLM(['{"score": 8}', "答案"])
    retr = FakeRetriever([_chunk()])
    graph = build_crag_graph(retr, llm, tracer=FakeTracer(), top_k=5)
    graph.invoke({"question": "q", "top_k": 2}, config=CFG("k1"))
    assert retr.top_ks == [2]
    llm2 = FakeLLM(['{"score": 8}', "答案"])
    retr2 = FakeRetriever([_chunk()])
    graph2 = build_crag_graph(retr2, llm2, tracer=FakeTracer(), top_k=5)
    graph2.invoke({"question": "q"}, config=CFG("k2"))
    assert retr2.top_ks == [5]  # 未传 → 构建默认，行为与 T7 一致


def test_tool_calls_field_in_state_typedef():
    assert "tool_calls" in CRAGState.__annotations__
    assert "host" in CRAGState.__annotations__
