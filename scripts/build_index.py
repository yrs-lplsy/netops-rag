import argparse
import os
import sys
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import yaml

from netrag.config import Settings
from netrag.embedding.bge_m3 import BGEM3Embedder
from netrag.embedding.tokenizer import BgeTokenCounter
from netrag.ingestion.chunker_naive import chunk_naive
from netrag.ingestion.fetcher import fetch_all
from netrag.ingestion.types import DocMeta
from netrag.index.milvus_client import get_milvus, wait_healthy
from netrag.index.naive_schema import create_naive, insert_naive


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["naive", "hybrid"], default="naive")
    ap.add_argument("--manifest", default="data/manifests/s1_cisco.yaml")
    ap.add_argument("--drop", action="store_true")
    args = ap.parse_args()
    s = Settings.from_env()

    manifest_path = Path(args.manifest)
    md_paths = fetch_all(manifest_path, s.data_dir / "raw", s.data_dir / "processed")
    meta_by_doc = {d["doc_id"]: d for d in yaml.safe_load(manifest_path.read_text())["docs"]}
    counter = BgeTokenCounter(s.embed_model)

    if args.mode == "hybrid":
        from netrag.ingestion.bm25_field import build_bm25_text
        from netrag.ingestion.chunker_structured import chunk_structured
        from netrag.index.hybrid_schema import CHUNKS, PARENTS, create_hybrid, insert_hybrid

        all_parents, all_children = [], []
        for p in md_paths:
            doc_id = p.stem
            m = meta_by_doc[doc_id]
            meta = DocMeta(vendor=m["vendor"], model=m["model"], sw_version=m["sw_version"],
                           doc_id=doc_id, title=m["title"])
            parents, children = chunk_structured(p.read_text(), meta, counter)
            for c in children:
                c.bm25_text = build_bm25_text(c.text, c.breadcrumb)
            print(f"{doc_id}: {len(parents)} parents / {len(children)} children")
            all_parents.extend(parents)
            all_children.extend(children)

        client = get_milvus()
        wait_healthy(client)
        create_hybrid(client, drop=args.drop)
        insert_hybrid(client, all_parents, all_children, BGEM3Embedder(s.embed_model))
        client.flush(CHUNKS)
        client.flush(PARENTS)
        print(f"indexed {len(all_children)} children / {len(all_parents)} parents")
        return

    all_chunks = []
    for p in md_paths:
        doc_id = p.stem
        m = meta_by_doc[doc_id]
        meta = DocMeta(vendor=m["vendor"], model=m["model"], sw_version=m["sw_version"],
                       doc_id=doc_id, title=m["title"])
        chunks = chunk_naive(p.read_text(), meta, counter)
        print(f"{doc_id}: {len(chunks)} naive chunks")
        all_chunks.extend(chunks)

    client = get_milvus()
    wait_healthy(client)
    create_naive(client, drop=args.drop)
    insert_naive(client, all_chunks, BGEM3Embedder(s.embed_model))
    client.flush("chunks_naive")
    print(f"indexed {len(all_chunks)} chunks into chunks_naive")


if __name__ == "__main__":
    main()
