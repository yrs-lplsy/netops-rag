"""CRAG 问答 CLI：检索 → LLM 打分 → 高分生成 / 低分改写重检 / 拒答转人工。

用法：
    uv run python scripts/ask_crag.py --question "如何在 Catalyst 9300 上配置 OSPF 存根区域" \
        [--threshold 6.0] [--retriever hybrid|naive] [--top-k 5] [--no-filter] [--route] \
        [--history '["华为S5735支持多少VLAN？","S5735支持最多32个VLAN。"]'] [--force-condense]

与 scripts/ask.py 的差别：生成前由 LLM 对检索片段整体打 1-10 分，低于阈值先改写
查询重检一轮，仍低则拒答并置 handoff（转人工）。一次 invoke 一条 trace（Langfuse
或 JSONL 兜底），打分与改写事件全部落观测。

--history 传入扁平 JSON 字符串数组（用户问/助手答 依次成对），启用多轮指代消解
（condense 节点，指代词启发式命中才花 1 次 LLM；--force-condense 绕过启发式）。
"""

import argparse
import datetime as _dt
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from netrag.agent.crag import build_crag_graph
from netrag.config import Settings
from netrag.embedding.bge_m3 import BGEM3Embedder
from netrag.generation.llm import LLMClient
from netrag.index.milvus_client import get_milvus, wait_healthy
from netrag.retrieval.base import MetadataFilter
from netrag.retrieval.hybrid import HybridRetriever

# 复用 ask.py 的问句型号→标量过滤下推（中文问英文语料，实体下推最可靠）
from ask import detect_filter


class _FilteredRetriever:
    """问句型号过滤包装：CRAG 图内检索统一走它，改写查询同样带过滤。"""

    def __init__(self, inner, filters: MetadataFilter | None):
        self._inner = inner
        self._filters = filters
        self.name = inner.name + (f"; model={filters.model}" if filters else "")

    def retrieve(self, query, top_k=5, filters=None, route=None):
        kwargs: dict = {"top_k": top_k, "filters": self._filters}
        if route is not None:  # 仅 RoutedRetriever（--route）认识 route 参数
            kwargs["route"] = route
        return self._inner.retrieve(query, **kwargs)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--question", required=True)
    ap.add_argument("--threshold", type=float, default=6.0)
    ap.add_argument("--retriever", choices=["hybrid", "naive"], default="hybrid",
                    help="hybrid=三路RRF+精排+父块回填（默认），naive=纯稠密对照")
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--no-filter", action="store_true", help="关闭问句型号→标量过滤下推")
    ap.add_argument("--history", default=None,
                    help="多轮历史，扁平 JSON 字符串数组，用户问/助手答依次成对，"
                         "如 '[\"q1\",\"a1\",\"q2\",\"a2\"]'；提供即启用指代消解")
    ap.add_argument("--force-condense", action="store_true",
                    help="绕过指代词启发式，强制 LLM 改写（需配合 --history）")
    ap.add_argument("--route", action="store_true",
                    help="查询类型路由：exact→BM25直查，fuzzy→HyDE+dense，"
                         "direct→超纲直答不检索（默认关闭=无条件三路融合）")
    args = ap.parse_args()

    history = []
    if args.history:
        flat = json.loads(args.history)
        if len(flat) % 2 != 0 or not all(isinstance(x, str) for x in flat):
            ap.error("--history 必须是偶数个字符串（用户问/助手答依次成对）")
        history = [(flat[i], flat[i + 1]) for i in range(0, len(flat), 2)]

    settings = Settings.from_env()
    client = get_milvus()
    wait_healthy(client)
    embedder = BGEM3Embedder(settings.embed_model)
    if args.route:
        from netrag.agent.query_router import build_routed_retriever
        from netrag.embedding.reranker import BgeReranker

        # 路由模式：exact→BM25单路 / fuzzy→dense单路(+HyDE) / default→三路融合，
        # 各变体共享精排器；按需懒构造，未命中的路由不实例化
        inner = build_routed_retriever(client, embedder,
                                       reranker=BgeReranker(settings.rerank_model),
                                       recall_n=48)
    elif args.retriever == "naive":
        from netrag.retrieval.naive import NaiveRetriever

        inner = NaiveRetriever(client, embedder)
    else:
        from netrag.embedding.reranker import BgeReranker

        inner = HybridRetriever(client, embedder, BgeReranker(settings.rerank_model),
                                recall_n=48)
    retriever = _FilteredRetriever(inner, None if args.no_filter else detect_filter(args.question))

    llm = LLMClient()
    graph = build_crag_graph(retriever, llm, settings=settings,
                             threshold=args.threshold, top_k=args.top_k,
                             condense=bool(history), route=args.route)
    thread_id = f"crag-{_dt.datetime.now().strftime('%Y%m%d-%H%M%S')}"
    state: dict = {"question": args.question}
    if history:
        state["history"] = history
        state["force_condense"] = args.force_condense
    final = graph.invoke(state, config={"configurable": {"thread_id": thread_id}})

    meta = final.get("trace_meta") or {}
    print(f"[retriever: {retriever.name}; threshold={args.threshold}; thread={thread_id}]")
    if args.route:
        print(f"[route: {final.get('route')} | hyde: "
              f"{(final.get('hyde') or '')[:60]}{'…' if len(final.get('hyde') or '') > 60 else ''}]")
    if final.get("orig_question") and final["orig_question"] != final.get("question"):
        print(f"[condense: {final['orig_question']!r} -> {final['question']!r}]")
    print(f"[grades: {meta.get('grades')} | rewrites: "
          f"{[r['to'] for r in meta.get('rewrites', [])]} | retries: {final.get('retries')}]")
    print(f"[handoff: {final.get('handoff')}]")
    print(final.get("answer", ""))
    print("\n出处：")
    for c in final.get("citations", []):
        print(" " + c)


if __name__ == "__main__":
    main()
