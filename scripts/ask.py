import argparse
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from netrag.config import Settings
from netrag.embedding.bge_m3 import BGEM3Embedder
from netrag.generation.answer import answer_with_citations
from netrag.generation.llm import LLMClient
from netrag.index.milvus_client import get_milvus, wait_healthy
from netrag.observability.tracer import get_tracer
from netrag.retrieval.base import MetadataFilter
from netrag.retrieval.hybrid import HybridRetriever

# 问题里的型号别名 → 索引里的 model 值。中文提问检索英文语料时稠密/稀疏排序都弱
# （bge-m3 跨语言相似度不敌同语言字面重叠），问句明确带型号时下推为标量过滤，
# 是最可靠的跨语言路由手段（pdf_v1 报告「问题与决策」）。
_MODEL_ALIASES = [
    (re.compile(r"9300", re.I), "Catalyst 9300"),
    (re.compile(r"\b(?:s17|s57|s67)\d{2}\b", re.I), "S1700, S5700, S6700"),
    (re.compile(r"\br1110\b", re.I), "R1110"),
]


def detect_filter(question: str) -> MetadataFilter | None:
    for pat, model in _MODEL_ALIASES:
        if pat.search(question):
            return MetadataFilter(model=model)
    return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("question")
    ap.add_argument("--retriever", choices=["hybrid", "naive"], default="hybrid",
                    help="hybrid=三路RRF+精排+父块回填（默认），naive=纯稠密对照")
    ap.add_argument("--top-k", type=int, default=5)
    ap.add_argument("--no-rerank", action="store_true", help="hybrid 关闭精排")
    ap.add_argument("--no-filter", action="store_true", help="关闭问句型号→标量过滤下推")
    args = ap.parse_args()
    settings = Settings.from_env()
    client = get_milvus()
    wait_healthy(client)
    embedder = BGEM3Embedder(settings.embed_model)
    filters = None if args.no_filter else detect_filter(args.question)
    if args.retriever == "naive":
        from netrag.retrieval.naive import NaiveRetriever

        retriever = NaiveRetriever(client, embedder)
    else:
        from netrag.embedding.reranker import BgeReranker

        reranker = None if args.no_rerank else BgeReranker(settings.rerank_model)
        retriever = HybridRetriever(client, embedder, reranker, recall_n=48)

    tracer = get_tracer(settings, run_name="ask")
    trace_ref = None
    with tracer.trace("ask", meta={"question": args.question, "retriever": args.retriever,
                                   "top_k": args.top_k, "model": settings.llm_model}) as trace:
        trace_ref = trace.id
        with trace.span("retrieve", meta={"top_k": args.top_k,
                                          "filters": vars(filters) if filters else None}) as span:
            chunks = retriever.retrieve(args.question, top_k=args.top_k, filters=filters)
            span.event("retrieved", chunk_ids=[c.chunk_id for c in chunks],
                       scores=[round(c.score, 4) for c in chunks])
        with trace.span("generate", meta={"n_chunks": len(chunks)}) as gen:
            result = answer_with_citations(args.question, chunks, LLMClient())
            gen.event("answered", answer_chars=len(result.text),
                      n_citations=len(result.citations))
    print(f"[retriever: {retriever.name}{'; model=' + filters.model if filters else ''}]")
    print(result.text)
    print("\n出处：")
    for c in result.citations:
        print(" " + c)
    where = getattr(tracer, "path", None) or f"langfuse {trace_ref or 'cloud'}"
    print(f"[trace: {where}]", file=sys.stderr)


if __name__ == "__main__":
    main()

