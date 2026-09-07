"""查询路由 + HyDE 单元测试：注入 FakeLLM/假检索器，零网络。

覆盖：三类分类分支（exact/fuzzy/direct）、垃圾输出 fail-safe 回 fuzzy（融合路径
是通用路径，误伤方向安全）、恰好一次 LLM 调用、路由判据与 HyDE「文档段不是答案」
的提示词断言、RoutedRetriever 映射分发（未知 route 回 default、工厂懒构造缓存、
缺 default 键报错）、build_routed_retriever 变体路径正确。
"""

import pytest

from netrag.agent.query_router import (
    RoutedRetriever,
    build_routed_retriever,
    hydep_expand,
    route_query,
)


class FakeLLM:
    """按脚本依次吐回复，并记录每次 chat 的入参供提示词断言。"""

    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def chat(self, messages, temperature=0.2, max_tokens=2048):
        self.calls.append({"messages": messages, "temperature": temperature,
                           "max_tokens": max_tokens})
        assert self.responses, "脚本回复耗尽：发起了计划外的 LLM 调用"
        return self.responses.pop(0)


class FakeRetriever:
    name = "fake"

    def __init__(self, tag=""):
        self.tag = tag
        self.queries = []

    def retrieve(self, query, top_k=5, filters=None):
        self.queries.append((query, top_k, filters))
        return []


def _user_text(call):
    return "\n".join(m["content"] for m in call["messages"] if m["role"] == "user")


# ---------------------------------------------------------------------------
# route_query：三类分支 + 健壮解析 + fail-safe
# ---------------------------------------------------------------------------

def test_route_exact_one_call_question_in_prompt():
    llm = FakeLLM(["exact"])
    assert route_query("display interface brief 的作用", llm) == "exact"
    assert len(llm.calls) == 1  # 恰好一次 LLM 调用
    assert "display interface brief 的作用" in _user_text(llm.calls[0])


def test_route_fuzzy_and_direct_branches():
    assert route_query("交换机端口频繁up-down怎么排查", FakeLLM(["fuzzy"])) == "fuzzy"
    assert route_query("今天天气怎么样", FakeLLM(["direct"])) == "direct"


def test_route_parse_is_robust_to_noise():
    # 大小写/首尾空白/前后缀噪声：首个落在三类词表中的 token 生效
    assert route_query("q", FakeLLM(["  Exact\n"])) == "exact"
    assert route_query("q", FakeLLM(["类别：FUZZY"])) == "fuzzy"
    assert route_query("q", FakeLLM(["分类结果 - Direct。"])) == "direct"
    assert route_query("q", FakeLLM(["这是fuzzy类"])) == "fuzzy"  # 无空格也认得出


def test_route_garbage_falls_back_to_fuzzy():
    # 解析失败 → "fuzzy"（通用三路/融合路径兜底，方向安全）
    for bad in ("", "   ", "我不知道", "命令？", "exactt或fuzzy之类的吧"):
        assert route_query("q", FakeLLM([bad])) == "fuzzy", bad


def test_route_prompt_contains_criteria_examples():
    llm = FakeLLM(["exact"])
    route_query("display interface brief 的作用", llm)
    system = llm.calls[0]["messages"][0]["content"]
    assert "exact" in system and "fuzzy" in system and "direct" in system
    assert "命令" in system and "报错码" in system  # exact 判据：命令/参数/报错码
    assert "故障现象" in system  # fuzzy 判据
    assert "display interface" in system  # 示例进入提示词
    assert "up-down" in system  # fuzzy 示例进入提示词


# ---------------------------------------------------------------------------
# hydep_expand：假设文档段 + 垃圾输出回空串
# ---------------------------------------------------------------------------

def test_hydep_success_one_call_question_in_prompt():
    hyde = "本文档介绍端口频繁up-down的排障步骤：首先检查光模块收发光功率……"
    llm = FakeLLM([hyde])
    q = "交换机端口频繁up-down怎么排查"
    assert hydep_expand(q, llm) == hyde
    assert len(llm.calls) == 1  # 恰好一次 LLM 调用
    assert q in _user_text(llm.calls[0])


def test_hydep_output_stripped():
    llm = FakeLLM(["  假设文档段落内容。  "])
    assert hydep_expand("q", llm) == "假设文档段落内容。"


def test_hydep_garbage_returns_empty_string():
    for bad in ("", "   ", "\n"):
        assert hydep_expand("q", FakeLLM([bad])) == ""


def test_hydep_prompt_demands_doc_passage_not_answer():
    llm = FakeLLM(["假设文档段落"])
    hydep_expand("端口频繁up-down怎么排查", llm)
    system = llm.calls[0]["messages"][0]["content"]
    assert "文档" in system  # 生成的是假设性手册/文档段落
    assert "150-300" in system  # 长度约束进入提示词
    assert "不是" in system  # 明确不是对用户的直接回答


# ---------------------------------------------------------------------------
# RoutedRetriever：映射分发 + 懒构造 + default 兜底
# ---------------------------------------------------------------------------

def test_routed_retriever_dispatches_by_route():
    exact, fuzzy, default = FakeRetriever("exact"), FakeRetriever("fuzzy"), FakeRetriever("default")
    rr = RoutedRetriever({"exact": exact, "fuzzy": fuzzy, "default": default})
    rr.retrieve("show version", top_k=3, route="exact")
    rr.retrieve("网络很卡", top_k=5, route="fuzzy")
    assert exact.queries == [("show version", 3, None)]  # 查询与 top_k 原样透传
    assert fuzzy.queries == [("网络很卡", 5, None)]
    assert default.queries == []  # 未被路由到


def test_routed_retriever_unknown_route_falls_back_to_default():
    default = FakeRetriever()
    rr = RoutedRetriever({"exact": FakeRetriever(), "default": default})
    rr.retrieve("q", route="whatever")  # 未知/垃圾分类 route → default
    assert len(default.queries) == 1
    assert rr.retrieve("q") is not None  # route 参数缺省即 default


def test_routed_retriever_lazy_factory_cached():
    calls = []

    def factory():
        calls.append(1)
        return FakeRetriever("built")

    rr = RoutedRetriever({"exact": factory, "default": FakeRetriever()})
    assert calls == []  # 懒构造：声明时不实例化
    rr.retrieve("q1", route="exact")
    rr.retrieve("q2", route="exact")
    assert len(calls) == 1  # 工厂只调用一次并缓存


def test_routed_retriever_requires_default_key():
    with pytest.raises(ValueError):
        RoutedRetriever({"exact": FakeRetriever()})


def test_routed_retriever_has_name():
    rr = RoutedRetriever({"exact": FakeRetriever(), "fuzzy": FakeRetriever(),
                          "default": FakeRetriever()})
    assert "routed" in rr.name and "exact" in rr.name and "fuzzy" in rr.name


# ---------------------------------------------------------------------------
# build_routed_retriever：从 base 配置构造的变体路径正确
# ---------------------------------------------------------------------------

class FakeMilvus:
    def has_collection(self, name):
        return False


class FakeEmbedder:
    pass


def test_build_routed_retriever_variant_paths():
    rr = build_routed_retriever(FakeMilvus(), FakeEmbedder())
    assert rr.for_route("exact")._paths == ("bm25",)  # exact → BM25 单路直查
    assert rr.for_route("fuzzy")._paths == ("dense",)  # fuzzy → 纯稠密（配 HyDE）
    assert rr.for_route("default")._paths == ("dense", "bm25", "sparse")  # 通用三路
    assert "bm25" in rr.for_route("exact").name
    assert "dense" in rr.for_route("fuzzy").name


def test_build_routed_retriever_passes_recall_and_reranker():
    class FakeReranker:
        pass

    reranker = FakeReranker()
    rr = build_routed_retriever(FakeMilvus(), FakeEmbedder(), reranker=reranker,
                                recall_n=48)
    assert rr.for_route("exact")._reranker is reranker  # 精排器透传
    assert rr.for_route("exact")._recall_n == 48
