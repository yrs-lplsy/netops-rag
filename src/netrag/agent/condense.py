"""多轮指代消解（condense）：把依赖对话历史的追问改写为独立完整的问题。

流程与成本控制：

    无 history → 原样返回（0 次 LLM）
    有 history 且命中指代词启发式（或 force=True）→ 恰好 1 次 LLM 改写
    有 history 但未命中启发式且未强制 → 原样返回（0 次 LLM）

指代词启发式（保守、可预测，宁漏勿误）：
- 中文词做子串匹配：它/他们/这个/那个/该/上述/刚才/之前/上面
- 英文词做整词匹配（\\b 边界，忽略大小写）：same/it/its/this/that
  —— 否则 "switch" 里的 "it"、"monitoring" 里的 "it" 会误命中。
- 已知局限：多跳追问（"那它的呢"之外的 "S5735 的 STP 与 9300 的相比如何"）
  不含指代词但同样受益于改写，启发式会漏——调用方可用 force=True 绕过。
- 误命中方向是安全的：提示词明确「若问题本身已独立，原样返回」，
  LLM 会把自含问题原样吐回。

fail-open：LLM 输出为空/纯空白时返回原问题——改写失败不能阻断问答主链路。
"""

from __future__ import annotations

import re
from typing import Any

CONDENSE_SYSTEM = (
    "你是多轮对话问题改写器。结合对话历史，把用户最新的追问改写为一个独立完整、"
    "不依赖上下文就能理解的问题。"
    "必须原样保留问题中的设备型号、软件版本、接口名、协议名等实体，不得改写或删除。"
    "若追问本身已经独立完整，原样返回，不要改写。"
    "只输出改写后的问题本身，不要任何解释或前缀。"
)

# 中文指代词：子串匹配；英文：整词匹配（见模块 docstring 的已知局限）
_CJK_REFERENTS = ("它", "他们", "这个", "那个", "该", "上述", "刚才", "之前", "上面")
_EN_REFERENT_RE = re.compile(r"\b(?:same|it|its|this|that)\b", re.IGNORECASE)

_ANSWER_EXCERPT = 500  # 历史回答截断长度：改写只需指代对象，不必全文
_CONDENSE_MAX_TOKENS = 128


def has_referent(question: str) -> bool:
    """判断问题是否含指代词（见模块 docstring：可预测、宁漏勿误）。"""
    if any(w in (question or "") for w in _CJK_REFERENTS):
        return True
    return bool(_EN_REFERENT_RE.search(question or ""))


def condense_question(history: list[tuple[str, str]], question: str, llm: Any,
                      settings: Any = None, force: bool = False) -> str:
    """把依赖历史的追问改写为独立问题；不需要改写时原样返回。

    history 为 [(user_q, assistant_a), ...]（assistant 回答过长会被截断）；
    llm 需提供 .chat(messages, temperature=, max_tokens=) -> str（LLMClient 兼容）；
    settings 预留（当前无配置项，行为完全由注入的 llm 决定）；
    force=True 绕过指代词启发式（多跳无指代问题建议强制）。
    """
    if not history:
        return question
    if not force and not has_referent(question):
        return question
    turns = "\n\n".join(
        f"用户：{u}\n助手：{(a or '')[:_ANSWER_EXCERPT]}" for u, a in history
    )
    user = (f"对话历史：\n{turns}\n\n最新问题：{question}\n\n"
            f"请输出改写后的独立问题：")
    out = llm.chat([{"role": "system", "content": CONDENSE_SYSTEM},
                    {"role": "user", "content": user}],
                   temperature=0.0, max_tokens=_CONDENSE_MAX_TOKENS)
    rewritten = (out or "").strip().strip('"').strip()
    return rewritten or question  # fail-open：空输出回原问题
