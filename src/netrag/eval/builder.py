import re

from netrag.eval.golden import GoldenItem
from netrag.generation.llm import LLMClient
from netrag.ingestion.types import Chunk

PROMPT = (
    "根据以下网络设备手册片段，写一个可以用该片段直接回答的中文事实型问题。"
    "问题必须包含片段中的具体命令或参数名，不要出现'片段''上文'这类指代。只输出问题本身。\n\n片段：\n{text}"
)

TROUBLESHOOT_PROMPT = (
    "以下是一份网络设备手册中的故障处理片段，描述了某个故障现象及其排查/处理方法。"
    "请以网络运维工程师的视角写一个中文排障问题：先自然描述故障现象，再问如何排查或如何处理"
    "（例如'……出现某现象，该如何排查/处理？'）。问题要包含现象中的具体关键词（协议/命令/告警名），"
    "答案必须能由该片段直接给出。不要出现'片段''上文'这类指代。只输出问题本身。\n\n片段：\n{text}"
)

MULTIHOP_PROMPT = (
    "以下是一个网络设备手册文档中的两个相关片段：片段A是配置/命令侧内容，片段B是原理/说明侧内容。"
    "请写一个中文问题，要求：必须同时结合片段A和片段B的信息才能完整回答（单看任何一个片段都不够）；"
    "问题中包含两段内容的具体关键词（命令名/协议名/参数名）；不要出现'片段A''片段B''上文'这类指代。"
    "只输出问题本身。\n\n片段A：\n{a}\n\n片段B：\n{b}"
)

REJECT_PROMPT = (
    "请以网络运维工程师向技术手册提问的口吻，写一个关于「{theme}」的具体中文问题。"
    "要求：问题具体、包含该主题的常见术语（像真实用户会问的话）；"
    "但网络设备配置手册中不存在该主题的内容，任何交换机/路由器手册都无法回答它。只输出问题本身。"
)

# 排障候选关键词（spec 指定的启发式）
TROUBLESHOOT_KEYWORDS = ("故障", "排查", "处理方法", "解决", "Troubleshooting", "处理步骤", "常见故障")
_TROUBLESHOOT_RE = re.compile("|".join(TROUBLESHOOT_KEYWORDS), re.IGNORECASE)

# 近空/目录/纯型号表等垃圾片段的上行剔除（不浪费 LLM 调用）
_MIN_TEXT_LEN = 100
_SECNUM_RE = re.compile(r"\d+(?:\.\d+)+\s+\S+")  # 线性匹配，避免嵌套量词回溯爆炸
_JUNK_PREFIXES = ("表头: | 系列 | 支持产品 |",)


def is_troubleshoot_candidate(text: str) -> bool:
    """故障处理片段启发式：命中排障关键词即候选。"""
    return bool(_TROUBLESHOOT_RE.search(text))


def _is_garbage(text: str) -> bool:
    t = text.strip()
    if len(t) < _MIN_TEXT_LEN:
        return True
    if any(t.startswith(p) for p in _JUNK_PREFIXES):
        return True
    if len(_SECNUM_RE.findall(t)) >= 4:  # 目录式编号列表行
        return True
    lines = [ln for ln in t.splitlines() if ln.strip()]
    if lines and sum(1 for ln in lines if ln.lstrip().startswith("|")) / len(lines) > 0.6:
        return True  # 纯表格碎片（型号表/特性信息表），不出题素材
    return False


_CMD_RE = re.compile(
    r"(配置步骤|操作步骤|命令格式|使用实例|配置举例|执行命令|display |undo |reset "
    r"|show \w|switch\(config|configure terminal|Example:|Step \d)", re.IGNORECASE)
_CONCEPT_RE = re.compile(
    r"(原理描述|原理|机制|概念|简介|注意事项|背景信息"
    r"|Information About|Guidelines|Restrictions|Overview)", re.IGNORECASE)


def _chunk_roles(c: Chunk) -> set[str]:
    roles = set()
    if _CMD_RE.search(c.text):
        roles.add("cmd")
    if _CONCEPT_RE.search(c.text):
        roles.add("concept")
    return roles


def select_troubleshoot_chunks(chunks: list[Chunk]) -> list[Chunk]:
    """筛出故障处理候选片段并剔除近空/垃圾片段。"""
    return [c for c in chunks if not _is_garbage(c.text) and is_troubleshoot_candidate(c.text)]


def pick_multihop_pairs(chunks: list[Chunk]) -> list[tuple[Chunk, Chunk]]:
    """同一文档内选（命令/配置侧, 原理/说明侧）跨父块片段对，primary=配置/命令侧。

    规则：同 doc_id、不同 parent_id、角色互补（cmd × concept）、双方非垃圾片段；
    每个命令侧父块与每个原理侧片段至多配 1 对（线性：角色/文档索引预计算）。
    """
    usable = [c for c in chunks if not _is_garbage(c.text) and c.parent_id]
    roles = {c.chunk_id: _chunk_roles(c) for c in usable}
    by_doc_concept: dict[str, list[Chunk]] = {}
    for c in usable:
        if "concept" in roles[c.chunk_id]:
            by_doc_concept.setdefault(c.doc_id, []).append(c)
    pairs: list[tuple[Chunk, Chunk]] = []
    used_cmd_parents: set[str] = set()
    used_concept: set[str] = set()
    for prim in usable:
        if "cmd" not in roles[prim.chunk_id] or prim.parent_id in used_cmd_parents:
            continue
        for sec in by_doc_concept.get(prim.doc_id, []):
            if sec.chunk_id in used_concept or sec.parent_id == prim.parent_id:
                continue
            pairs.append((prim, sec))
            used_cmd_parents.add(prim.parent_id)
            used_concept.add(sec.chunk_id)
            break
    return pairs


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().strip('"').strip("“”").strip())


def generate_questions(chunks: list[Chunk], llm: LLMClient, qtype: str = "factual",
                       max_items: int = 0) -> list[GoldenItem]:
    """事实型/排障型单片段生成：qtype=factual|troubleshoot。"""
    if qtype == "troubleshoot":
        pool = select_troubleshoot_chunks(chunks)
        prompt = TROUBLESHOOT_PROMPT
    else:
        pool = [c for c in chunks if not _is_garbage(c.text)]
        prompt = PROMPT
    items: list[GoldenItem] = []
    for c in pool[:max_items or len(pool)]:
        q = _clean(llm.chat([{"role": "user", "content": prompt.format(text=c.text[:2000])}]))
        if not q or len(q) < 8:
            continue
        items.append(GoldenItem(
            qid=f"{c.doc_id}#{c.chunk_id}", question=q, qtype=qtype,
            expected_doc_ids=[c.doc_id], expected_chunk_ids=[c.chunk_id],
        ))
    return items


def generate_multihop_items(pairs: list[tuple[Chunk, Chunk]], llm: LLMClient,
                            max_items: int = 0) -> list[GoldenItem]:
    """双片段多跳生成：expected_chunk_ids=[primary, secondary]（有序，primary 在前）。"""
    items: list[GoldenItem] = []
    for prim, sec in pairs[:max_items or len(pairs)]:
        content = MULTIHOP_PROMPT.format(a=prim.text[:1500], b=sec.text[:1500])
        q = _clean(llm.chat([{"role": "user", "content": content}]))
        if not q or len(q) < 12:
            continue
        items.append(GoldenItem(
            qid=f"{prim.doc_id}#{prim.chunk_id}+{sec.chunk_id}", question=q, qtype="multihop",
            expected_doc_ids=[prim.doc_id],
            expected_chunk_ids=[prim.chunk_id, sec.chunk_id],
        ))
    return items


def generate_reject_items(themes: list[str], llm: LLMClient,
                          variants_per_theme: int = 1,
                          max_items: int = 0,
                          prompt_template: str = REJECT_PROMPT) -> list[GoldenItem]:
    """拒答类生成：主题须事先验证语料中不存在；期望命中恒为空。

    qid 序号按主题内变体真实递增（-01/-02/...），保证全局唯一。
    prompt_template 可注入（生成脚本用简短提示做超长重试）。
    """
    items: list[GoldenItem] = []
    budget = max_items or len(themes) * variants_per_theme
    theme_counts: dict[str, int] = {}
    for theme in themes:
        base = theme_counts.get(theme, 0)
        theme_counts[theme] = base + variants_per_theme
        for i in range(variants_per_theme):
            if len(items) >= budget:
                return items
            q = _clean(llm.chat([{"role": "user", "content": prompt_template.format(theme=theme)}]))
            if not q or len(q) < 8:
                continue
            slug = re.sub(r"[^0-9A-Za-z\u4e00-\u9fff]+", "-", theme).strip("-")
            items.append(GoldenItem(
                qid=f"reject-{slug}-{base + i + 1:02d}", question=q, qtype="reject",
                expected_doc_ids=[], expected_chunk_ids=[],
            ))
    return items
