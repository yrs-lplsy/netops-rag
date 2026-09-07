"""多轮指代消解（condense）单元测试：注入 FakeLLM，零网络。

覆盖：无历史直通（0 调用）、指代词启发式两分支、force 绕过启发式、
实体保留指令进入提示词、长历史回答截断、空/垃圾输出 fail-open 回原问题。
"""

from netrag.agent.condense import (
    _ANSWER_EXCERPT,
    condense_question,
    has_referent,
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


def _user_text(call):
    return "\n".join(m["content"] for m in call["messages"] if m["role"] == "user")


HISTORY = [("华为S5735支持多少VLAN？", "S5735支持最多32个VLAN，其中活动VLAN 8个。")]


# ---------------------------------------------------------------------------
# 启发式本身：可预测（含指代词→消解；不含→直通）
# ---------------------------------------------------------------------------

def test_has_referent_branches():
    assert has_referent("它的生成树模式有哪些？") is True  # 中文指代
    assert has_referent("上述配置如何验证？") is True
    assert has_referent("Does it support STP?") is True  # 英文独立词
    assert has_referent("如何在 Catalyst 9300 上配置 OSPF 存根区域") is False  # 无指代
    assert has_referent("switch 的端口聚合怎么配") is False  # it 是 switch 子串，不算


def test_no_history_returns_question_unchanged_zero_calls():
    llm = FakeLLM([])
    q = "它的生成树模式有哪些？"
    assert condense_question([], q, llm) == q
    assert llm.calls == []  # 无历史零 LLM 调用


def test_referent_word_with_history_condenses_one_call():
    llm = FakeLLM(["华为S5735交换机支持哪些生成树模式？"])
    out = condense_question(HISTORY, "它的生成树模式有哪些？", llm)
    assert out == "华为S5735交换机支持哪些生成树模式？"
    assert len(llm.calls) == 1  # 恰好一次 LLM 调用
    sent = _user_text(llm.calls[0])
    assert "华为S5735支持多少VLAN？" in sent  # 历史问题进入提示词
    assert "它的生成树模式有哪些？" in sent  # 追问进入提示词


def test_self_contained_question_with_history_passthrough_zero_calls():
    llm = FakeLLM([])
    q = "如何在 Catalyst 9300 上配置 OSPF 存根区域"  # 无指代词
    assert condense_question(HISTORY, q, llm) == q
    assert llm.calls == []  # 启发式未命中 → 不花 LLM 调用


def test_force_bypasses_heuristic():
    llm = FakeLLM(["如何在 Catalyst 9300 上配置 OSPF stub area"])
    q = "如何在 Catalyst 9300 上配置 OSPF 存根区域"  # 无指代词也强制消解
    out = condense_question(HISTORY, q, llm, force=True)
    assert out == "如何在 Catalyst 9300 上配置 OSPF stub area"
    assert len(llm.calls) == 1


def test_prompt_demands_entity_preservation_and_identity_fallback():
    llm = FakeLLM(["改写后的问题"])
    condense_question(HISTORY, "它的生成树模式有哪些？", llm)
    system = llm.calls[0]["messages"][0]["content"]
    assert "独立" in system  # 改写为独立完整的问题
    assert "设备型号" in system and "软件版本" in system and "接口名" in system
    assert "原样保留" in system  # 实体必须保留
    assert "原样返回" in system  # 已独立则原样返回


def test_long_history_answer_truncated_in_prompt():
    long_answer = "头部内容" + "A" * 800 + "TAIL_MARKER超出截断"
    llm = FakeLLM(["改写后的问题"])
    condense_question([("q1", long_answer)], "它的端口数是多少？", llm)
    sent = _user_text(llm.calls[0])
    assert "A" * (_ANSWER_EXCERPT - 100) in sent  # 截断长度内的内容保留
    assert "TAIL_MARKER" not in sent  # 超长部分被截掉


def test_fail_open_on_empty_or_garbage_output():
    for bad in ("", "   ", "\n"):
        llm = FakeLLM([bad])
        assert condense_question(HISTORY, "它的生成树模式有哪些？", llm) == "它的生成树模式有哪些？"


def test_output_stripped():
    llm = FakeLLM(['  "华为S5735支持哪些生成树模式？"  '])
    out = condense_question(HISTORY, "它的生成树模式有哪些？", llm)
    assert out == "华为S5735支持哪些生成树模式？"  # 去首尾空白与引号
