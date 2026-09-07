import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from netrag.config import Settings
from netrag.embedding.bge_m3 import BGEM3Embedder
from netrag.eval.golden import load_golden
from netrag.eval.metrics import mrr, recall_at_k
from netrag.eval.report import write_report
from netrag.index.milvus_client import get_milvus, wait_healthy
from netrag.retrieval.naive import NaiveRetriever


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--golden", default="data/golden/s1_factual.yaml")
    ap.add_argument("--out", required=True)
    ap.add_argument("--k", type=int, default=5)
    args = ap.parse_args()

    items = load_golden(Path(args.golden))
    client = get_milvus()
    wait_healthy(client)
    retriever = NaiveRetriever(client, BGEM3Embedder())

    ranked_chunk, ranked_doc, misses = [], [], []
    for it in items:
        hits = retriever.retrieve(it.question, top_k=args.k, filters=it.filters)
        ids = [h.chunk_id for h in hits]
        docs = [h.doc_id for h in hits]
        ranked_chunk.append(ids)
        ranked_doc.append(docs)
        if not set(ids[:args.k]) & set(it.expected_chunk_ids):
            misses.append((it.qid, it.question, ids[:3], it.expected_chunk_ids))

    r5 = recall_at_k(ranked_chunk, [it.expected_chunk_ids for it in items], args.k)
    r5_doc = recall_at_k(ranked_doc, [it.expected_doc_ids for it in items], args.k)
    m = mrr(ranked_chunk, [it.expected_chunk_ids for it in items])

    body = ["## 未命中样例（前 10）", ""]
    for qid, q, got, exp in misses[:10]:
        body.append(f"- `{qid}` {q}\n  - top3: {got} 期望: {exp}")
    write_report(
        path=Path(args.out),
        title=f"S1 naive 基线检索评测（k={args.k}）",
        summary_rows={
            "golden 条数": str(len(items)),
            "Recall@5 (chunk)": f"{r5:.3f}",
            "Recall@5 (doc)": f"{r5_doc:.3f}",
            "MRR (chunk)": f"{m:.3f}",
        },
        body_md="\n".join(body),
    )


if __name__ == "__main__":
    main()
