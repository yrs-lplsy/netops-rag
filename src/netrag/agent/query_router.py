"""查询类型路由（route_query）+ HyDE 假设文档扩展（hydep_expand）+ 检索分发器。

背景（机制性修复，见 docs/eval-reports/2026-09-06-s3-retrieval.md）：混合语料上
BM25 对中文问句噪声大——三路融合 chunk R@5=0.712 低于纯稠密 0.806，拖累了融合
结果；但 BM25 对精确命令/报错码查询（术语字面匹配）仍是利器。故按查询类型
条件激活 BM25，而不是无条件三路融合：

    exact  = 明确的命令/参数/报错码查询（"display interface"、"ospf network-type"、
             错误码）→ BM25 单路直查（字面匹配最准）
    fuzzy  = 故障现象描述/模糊运维问题（"端口频繁up-down怎么办"、"网络很卡"）
             → HyDE 假设文档段 + 纯稠密检索（语义泛化最好）
    direct = 寒暄/超纲/与网络设备运维无关 → 不检索，直接 canned 回复

fail-safe 方向：
- route_query 解析失败一律按 "fuzzy" 兜底——通用三路/稠密路径本就是缺省检索方式，
  误分类的代价是「多用通用检索」而非「漏检」。
- hydep_expand 输出为空/纯空白 → 返回 ""，调用方跳过 HyDE 直接用原问题。

fuzzy 检索的 HyDE 用法（刻意选简单方案，已评估否决 RRF 双查合并）：以
「hyde 文本 + 原问题」拼接为单一查询走 dense 单路——hyde 段落丰富查询的语义
向量，原问题锚定用户意图；不做两次检索合并，避免引入第二套融合权重。
"""

from __future__ import annotations

import re
from typing import Any

from netrag.retrieval.hybrid import HybridRetriever

ROUTE_SYSTEM = (
    "你是网络设备运维问题的查询类型分类器。把用户问题分为三类，只输出类别单词：\n"
    "exact：明确的命令/参数/报错码查询（如 \"display interface\"、\"ospf network-type\"、"
    "错误码）；\n"
    "fuzzy：故障现象描述或模糊运维问题（如 \"端口频繁up-down怎么办\"、\"网络很卡\"）；\n"
    "direct：寒暄或超纲、与网络设备运维无关的问题（如 \"今天天气怎么样\"）。\n"
    "只输出 exact、fuzzy 或 direct 之一，不要任何其他文字。"
)

HYDE_SYSTEM = (
    "你是网络设备手册写作助手。针对用户问题写一段假设性的手册/文档段落（150-300字），"
    "内容是看起来能回答该问题的文档正文（含命令、参数、步骤等术语）——"
    "不是对用户的直接回答，不要解释、前言或标题。"
)

_VALID_ROUTES = ("exact", "fuzzy", "direct")

_ROUTE_MAX_TOKENS = 8  # 分类只输出一个词
_HYDE_MAX_TOKENS = 512  # 150-300 中文字约 300-450 token，留余量

# 类别词两侧不得紧邻 ASCII 字母：防止 "exactt"/"fuzzyish" 这类垃圾词误命中
_ROUTE_WORD_RE = {v: re.compile(rf"(?<![a-z]){v}(?![a-z])") for v in _VALID_ROUTES}


def _parse_route(text: str) -> str:
    """从 LLM 输出解析类别：取最早出现的、两侧非 ASCII 字母的类别词
    （"exactt" 不算 exact，"这是fuzzy类" 算 fuzzy）；全部落空 → "fuzzy"
    （fail-safe，通用融合路径兜底）。"""
    lowered = (text or "").strip().lower()
    hits = []
    for v in _VALID_ROUTES:
        m = _ROUTE_WORD_RE[v].search(lowered)
        if m:
            hits.append((m.start(), v))
    if hits:
        return min(hits)[1]
    return "fuzzy"


def route_query(question: str, llm: Any, settings: Any = None) -> str:
    """一次 LLM 调用把问题分为 exact/fuzzy/direct；解析失败回 "fuzzy"。

    llm 需提供 .chat(messages, temperature=, max_tokens=) -> str（LLMClient 兼容）；
    settings 预留（当前无配置项，行为由注入的 llm 决定）。
    """
    out = llm.chat([{"role": "system", "content": ROUTE_SYSTEM},
                    {"role": "user", "content": question}],
                   temperature=0.0, max_tokens=_ROUTE_MAX_TOKENS)
    return _parse_route(out)


def hydep_expand(question: str, llm: Any, settings: Any = None) -> str:
    """一次 LLM 调用生成假设性手册/文档段落（HyDE）；空/垃圾输出 → ""。

    返回 "" 时调用方应跳过 HyDE，直接用原问题检索（fail-open 不阻断主链路）。
    """
    out = llm.chat([{"role": "system", "content": HYDE_SYSTEM},
                    {"role": "user", "content": f"问题：{question}\n\n请输出假设的文档段落："}],
                   max_tokens=_HYDE_MAX_TOKENS)
    return (out or "").strip()


class RoutedRetriever:
    """route → retriever 分发包装：exact/fuzzy 各挂一个检索器，未知路由回 default。

    mapping 的值可以是现成检索器对象（需有 .retrieve），也可以是零参工厂 callable
    （首次用到才构造并缓存——避免为不会命中的路由加载组件）。"default" 键必填：
    垃圾/未知路由一律回落通用检索器，与 route_query 的 fuzzy 兜底方向一致。
    """

    def __init__(self, mapping: dict[str, Any]) -> None:
        if "default" not in mapping:
            raise ValueError("RoutedRetriever mapping 必须包含 'default' 键")
        self._mapping = dict(mapping)
        self._built: dict[str, Any] = {}

    def for_route(self, route: str) -> Any:
        name = route if route in self._mapping else "default"
        if name not in self._built:
            value = self._mapping[name]
            self._built[name] = value() if callable(value) else value
        return self._built[name]

    @property
    def name(self) -> str:
        parts = [k for k in self._mapping if k != "default"]
        return f"routed({'+'.join(parts)}|default)" if parts else "routed(default)"

    def retrieve(self, query: str, top_k: int = 5,
                 filters: Any = None, route: str = "default") -> list:
        return self.for_route(route).retrieve(query, top_k=top_k, filters=filters)


def build_routed_retriever(client, embedder, reranker=None,
                           collection: str = "chunks",
                           parents_collection: str = "chunk_parents",
                           recall_n: int = 20, rrf_k: int = 60) -> RoutedRetriever:
    """从 base 配置（client+embedder+reranker 工厂参数）懒构造三个 HybridRetriever 变体。

    exact → paths=("bm25",)（BM25 按需激活）；fuzzy → paths=("dense",)（配 HyDE）；
    default → 三路融合。各变体共享精排器与召回参数，首次命中该路由才实例化。
    """
    def make(paths: tuple[str, ...]):
        return lambda: HybridRetriever(
            client, embedder, reranker=reranker, collection=collection,
            parents_collection=parents_collection, paths=paths,
            rrf_k=rrf_k, recall_n=recall_n)

    return RoutedRetriever({
        "exact": make(("bm25",)),
        "fuzzy": make(("dense",)),
        "default": make(("dense", "bm25", "sparse")),
    })
