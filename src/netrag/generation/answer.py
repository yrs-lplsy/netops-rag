from dataclasses import dataclass

from netrag.generation.llm import LLMClient
from netrag.retrieval.base import RetrievedChunk

# 第二轮迭代（2026-09-07）prompt 收紧：Run B 归因发现 3 条参数化泄漏（答案混入记忆中的、
# 片段里不存在的命令/步骤）+ 1 条编造（DeviceA→DeviceG），根因是 7B/72B 生成模型用
# 自身知识补全手册片段未覆盖的细节。收紧后：逐论断须有片段原文依据，未覆盖内容显式
# 标注交人工确认；【出处】页脚与"未找到"兜底措辞不变（既有契约，单测钉住）。
# 人工决策（2026-09-07，先导 t02 失败模式）：诊断节点已注入「【设备实况】{host}」
# 伪片段，但本 prompt 只认手册片段 → 生成弃用实况、复述手册步骤。把设备实况输出
# 提为与手册并列的依据来源（总述「与」、逐论断「或」），反泄漏约束对手册内容不变。
SYSTEM = (
    "你是网络设备排障助手。仅依据给定手册片段与设备实况输出回答；"
    "答案中的每个技术论断（命令、参数、取值、步骤）都必须能在手册片段或设备实况输出中找到原文依据，"
    "禁止用你自己的知识补充片段中没有的命令或步骤；"
    "片段未覆盖的内容明确标注'（手册片段未涉及，建议人工确认）'；"
    "引用编号与所使用的片段一一对应；"
    "答案末尾单独列出【出处】列表，格式：[编号] 面包屑。"
    "片段中没有答案就回答：手册中未找到相关内容。"
)

# 检索命中子块，生成用父块（整节，含完整步骤/表格）：子块常把命令步骤与
# 前提说明切开，7B 模型面对残缺步骤会拒答或复读（pdf_v1 报告「问题与决策」）。
# 父块截窗以子块在父块中的位置为中心（头部截断会丢掉位于长父块后半的命中，
# 评审 Fix Round 1 发现）；窗口外加省略标记，找不到子块位置时退回头部截断。
_PARENT_CONTEXT_CAP = 6000
_WINDOW_BEFORE = 1000
_ELLIPSIS_HEAD = "…[前文省略]…"
_ELLIPSIS_TAIL = "…[后文省略]…"


def _parent_window(parent_text: str, child_text: str,
                   cap: int = _PARENT_CONTEXT_CAP) -> str:
    """取父块中包含子块的窗口：[子块起点-1000, 起点+(cap-1000))，边界对齐到行首。"""
    pos = parent_text.find(child_text)
    if pos < 0 and len(child_text) > 200:
        pos = parent_text.find(child_text[:200])  # 子块入库时被 [:8000] 截过，退而求其次
    if pos < 0:
        return parent_text[:cap]  # 退路：头部截断
    start = max(0, pos - _WINDOW_BEFORE)
    if start > 0:  # 起点对齐到行首，避免截半个句子
        nl = parent_text.rfind("\n", 0, start)
        if nl > 0:
            start = nl + 1
    end = min(len(parent_text), pos + (cap - _WINDOW_BEFORE))
    if end < len(parent_text):  # 终点对齐到行尾
        nl = parent_text.find("\n", end)
        if nl > 0:
            end = nl
    window = parent_text[start:end]
    if start > 0:
        window = _ELLIPSIS_HEAD + "\n" + window
    if end < len(parent_text):
        window = window + "\n" + _ELLIPSIS_TAIL
    return window


def build_generation_contexts(chunks: list[RetrievedChunk]) -> list[str]:
    """每个检索块的生成可见上下文，按检索顺序一一对应。

    无 parent_text → 子块全文；有 parent_text → 父块窗口（_parent_window）。
    answer_with_citations（生成）与 ragas_runner（assembly=parent-window 评测装配）
    共用本函数：保证 RAGAS 评测的 contexts 与 LLM 实际看到的片段严格一致（T6 验证
    序列 Run B 的装配修正——此前评测用子块文本而生成看父块窗口，faithfulness 被
    系统性压低）。
    """
    return [_parent_window(c.parent_text, c.text) if c.parent_text else c.text
            for c in chunks]


@dataclass
class AnswerResult:
    text: str
    citations: list[str]


def answer_with_citations(question: str, chunks: list[RetrievedChunk], llm: LLMClient) -> AnswerResult:
    bodies = build_generation_contexts(chunks)
    parts = [f"[{i+1}] {c.breadcrumb}\n{body}" for i, (c, body) in enumerate(zip(chunks, bodies))]
    ctx = "\n\n".join(parts)
    user = f"手册片段：\n{ctx}\n\n问题：{question}"
    text = llm.chat([{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}])
    citations = [f"[{i+1}] {c.breadcrumb}（{c.doc_id}）" for i, c in enumerate(chunks)]
    return AnswerResult(text=text, citations=citations)
