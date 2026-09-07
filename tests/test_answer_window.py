"""answer 父块开窗与生成上下文装配单测（评审 Fix Round 1 Finding 2/3 + T6 验证序列 Run B）。"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from netrag.generation.answer import (
    _ELLIPSIS_HEAD,
    _ELLIPSIS_TAIL,
    _parent_window,
    SYSTEM,
    answer_with_citations,
    build_generation_contexts,
)
from netrag.retrieval.base import RetrievedChunk


def _make_parent(n_paras: int) -> str:
    return "\n\n".join(f"段落{i}：" + "内容" * 30 for i in range(n_paras))


_LONG_PARENT = _make_parent(200)  # ~1.4 万字符，保证开窗两端都有省略


def _chunk(text: str, parent_text: str | None = None, breadcrumb: str = "面包屑") -> RetrievedChunk:
    return RetrievedChunk(chunk_id="c1", text=text, score=1.0, doc_id="d1",
                          breadcrumb=breadcrumb, vendor="v", model="m", sw_version="s",
                          parent_text=parent_text)


def test_child_in_second_half_gets_window_with_ellipsis():
    child = "段落18：" + "内容" * 30
    win = _parent_window(_LONG_PARENT, child)
    assert child in win  # 命中子块不被头截断丢掉
    assert _ELLIPSIS_HEAD in win  # 窗口前有省略标记
    assert _ELLIPSIS_TAIL in win  # 窗口后仍有内容 → 尾省略标记
    # cap=6000，终点对齐到行尾可再放宽一行（<100 字符）+ 两端省略标记
    assert len(win) <= 6000 + 100 + 2 * len(_ELLIPSIS_HEAD) + 10


def test_child_at_head_no_head_ellipsis():
    child = _LONG_PARENT[:100]
    win = _parent_window(_LONG_PARENT, child)
    assert child in win
    assert not win.startswith(_ELLIPSIS_HEAD)  # 位于父块头部，前省略不出现
    assert _ELLIPSIS_TAIL in win


def test_child_not_found_falls_back_to_head_truncation():
    win = _parent_window(_LONG_PARENT, "父块里根本不存在的子块文本")
    assert win == _LONG_PARENT[:6000]
    assert _ELLIPSIS_HEAD not in win and _ELLIPSIS_TAIL not in win


def test_short_parent_returned_whole():
    parent = "短父块，全部内容都在这里。"
    win = _parent_window(parent, "短父块")
    assert win == parent  # 无省略标记


# ---------- SYSTEM prompt：第二轮迭代收紧（防参数化泄漏/编造），出处与兜底措辞不变 ----------


def test_system_keeps_citation_footer_and_notfound_fallback():
    """收紧不得破坏既有契约：【出处】页脚格式 + 未找到兜底措辞原样保留。"""
    assert "【出处】" in SYSTEM
    assert "[编号] 面包屑" in SYSTEM
    assert "手册中未找到相关内容" in SYSTEM
    assert "仅依据给定手册片段与设备实况输出回答" in SYSTEM


def test_system_accepts_device_state_as_grounding_source():
    """修复 t02 失败模式（诊断拿到实况但生成弃用）：prompt 必须认设备实况为
    与手册并列的依据来源，且既有反泄漏约束对手册内容原样保留。"""
    # 两个来源并列出现：总述用「与」，逐论断用「或」（任一来源可支撑论断）
    assert "手册片段与设备实况输出" in SYSTEM
    assert "手册片段或设备实况输出" in SYSTEM
    # 保留的约束：出处页脚 / 未找到兜底 / 反泄漏（手册内容）
    assert "【出处】" in SYSTEM
    assert "手册中未找到相关内容" in SYSTEM
    assert "禁止" in SYSTEM and "自己的知识" in SYSTEM
    assert "手册片段未涉及" in SYSTEM and "人工确认" in SYSTEM


def test_system_every_claim_must_have_passage_grounding():
    """反泄漏约束1：每个技术论断（命令/参数/取值/步骤）必须能在片段找到原文依据。"""
    assert "每个技术论断" in SYSTEM
    assert "原文依据" in SYSTEM
    for kw in ("命令", "参数", "步骤"):
        assert kw in SYSTEM, f"约束须点名 {kw} 这类论断载体"


def test_system_out_of_scope_must_be_flagged():
    """反泄漏约束2：片段未覆盖的内容必须显式标注，不许静默混入。"""
    assert "手册片段未涉及" in SYSTEM
    assert "人工确认" in SYSTEM


def test_system_forbids_own_knowledge_supplementation():
    """反泄漏约束3：禁止用模型自身知识补充命令或步骤（参数化泄漏的根因）。"""
    assert "禁止" in SYSTEM
    assert "自己的知识" in SYSTEM


def test_system_citation_numbers_correspond_to_passages():
    """反泄漏约束4：引用编号与所用片段对应（防编号错配）。"""
    assert "引用编号" in SYSTEM


# ---------- build_generation_contexts：生成可见上下文的唯一装配函数（Run B）----------


def test_build_generation_contexts_child_without_parent():
    ctx = build_generation_contexts([_chunk("子块全文")])
    assert ctx == ["子块全文"]


def test_build_generation_contexts_parent_window_when_present():
    win = _parent_window(_LONG_PARENT, "段落18：" + "内容" * 30)
    ctx = build_generation_contexts([_chunk("段落18：" + "内容" * 30, parent_text=_LONG_PARENT)])
    assert ctx == [win]


def test_build_generation_contexts_mixed_order_preserved():
    child_a = "段落18：" + "内容" * 30
    ctx = build_generation_contexts([
        _chunk("纯子块"),
        _chunk(child_a, parent_text=_LONG_PARENT),
    ])
    assert ctx[0] == "纯子块"
    assert ctx[1] == _parent_window(_LONG_PARENT, child_a)


class _CapturingLLM:
    def __init__(self) -> None:
        self.calls: list[list[dict]] = []

    def chat(self, messages, temperature=0.2, max_tokens=2048):
        self.calls.append(messages)
        return "答案"


def test_answer_with_citations_prompt_bodies_equal_build_generation_contexts():
    """装配唯一来源：进 prompt 的每段正文必须 == build_generation_contexts 输出（逐字节）。"""
    child_a = "段落18：" + "内容" * 30
    chunks = [_chunk("纯子块", breadcrumb="文档A/章1"),
              _chunk(child_a, parent_text=_LONG_PARENT, breadcrumb="文档B/章2")]
    llm = _CapturingLLM()
    answer_with_citations("问题？", chunks, llm)
    user = llm.calls[0][1]["content"]
    for i, body in enumerate(build_generation_contexts(chunks)):
        assert f"[{i+1}] {chunks[i].breadcrumb}\n{body}" in user
