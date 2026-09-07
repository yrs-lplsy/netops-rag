"""pdf_v1 摄取编排：manifest 白名单 → PDF→md（ground truth 入 data/processed_pdf/）
→ chunk_structured 切分（parents/children）→ bm25 字段 → bge-m3 稠密+稀疏 → Milvus。

同时重建两个 collection：
- chunks        hybrid（dense+BM25 函数+bge 稀疏，父块并入 is_parent=True）
- chunks_naive  naive（纯稠密，对照用）

用法：
  uv run python scripts/ingest_pdf.py --limit 1 --drop   # 单文件全链路试跑
  uv run python scripts/ingest_pdf.py --drop             # 全量重建（默认清空两集合）
  uv run python scripts/ingest_pdf.py --md-only          # 只生成 md 不动索引

长任务分批：每文件打印一行进度（文件数/chunk 数/耗时/速率），每 10 文件打印累计与 ETA。
"""

import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

import yaml

from netrag.config import Settings
from netrag.embedding.bge_m3 import BGEM3Embedder
from netrag.embedding.tokenizer import CachedTokenCounter
from netrag.index.milvus_client import get_milvus, wait_healthy
from netrag.index.naive_schema import create_naive, insert_naive
from netrag.ingestion.bm25_field import build_bm25_text
from netrag.ingestion.chunker_naive import chunk_naive
from netrag.ingestion.chunker_structured import chunk_structured
from netrag.ingestion.pdf_to_md import convert_pdf
from netrag.ingestion.types import DocMeta

# VARCHAR max_length 按 UTF-8 字节校验（Milvus 2.5 实测），中文 3 字节/字，
# 中文语料在 schema 上限附近会超字节长，这里按保守字节预算截断（见报告「问题与决策」）。
_BREADCRUMB_MAX = 600
_BM25_TEXT_MAX = 5000


def _fmt_secs(s: float) -> str:
    m, sec = divmod(int(s), 60)
    h, m = divmod(m, 60)
    return f"{h:02d}:{m:02d}:{sec:02d}"


def _body_for_chunk(md_text: str) -> str:
    """去掉 md 首行的 `# 文档题名`（ground truth 用），切分时题名经 meta.title 传入
    parse_sections，避免它再进标题栈导致面包屑里题名重复。"""
    lines = md_text.split("\n")
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).strip()
    return md_text


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default="data/manifests/pdf_v1.yaml")
    ap.add_argument("--output-dir", default="data/processed_pdf")
    ap.add_argument("--limit", type=int, default=0, help="只处理前 N 个文件（试跑）")
    ap.add_argument("--filter", default="", help="只处理 doc_id 含该子串的文件（试跑）")
    ap.add_argument("--reuse-md", action="store_true", help="md 已存在则跳过转换")
    ap.add_argument("--md-only", action="store_true", help="只生成/更新 md，不索引")
    ap.add_argument("--skip-naive", action="store_true", help="不重建 chunks_naive")
    ap.add_argument("--no-drop", action="store_true", help="不清空 collection（增量追加）")
    ap.add_argument("--embed-batch", type=int, default=64)
    ap.add_argument("--flush-every", type=int, default=10, help="每 N 个文件 flush 一次")
    ap.add_argument("--min-md-chars", type=int, default=500,
                    help="转换后 md 少于该字符数 warn+跳过不入库（扉页/目录等近空文档）")
    args = ap.parse_args()
    s = Settings.from_env()
    repo = Path(__file__).resolve().parents[1]

    manifest = repo / args.manifest
    docs = yaml.safe_load(manifest.read_text())["docs"]
    if args.filter:
        docs = [d for d in docs if args.filter in d["doc_id"]]
    if args.limit:
        docs = docs[: args.limit]
    out_dir = repo / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    client, embedder, counter = None, None, None
    if not args.md_only:
        client = get_milvus()
        wait_healthy(client)
        stats_before = {c: client.get_collection_stats(c)["row_count"]
                        for c in ("chunks", "chunks_naive") if client.has_collection(c)}
        print(f"rebuild 前 collection 行数: {stats_before}")
        if not args.no_drop:
            from netrag.index.hybrid_schema import create_hybrid

            create_hybrid(client, drop=True)
        if not args.skip_naive:
            create_naive(client, drop=True)
        embedder = BGEM3Embedder(s.embed_model)
        counter = CachedTokenCounter(s.embed_model)
    else:
        counter = CachedTokenCounter(s.embed_model)

    t_all = time.time()
    tot = {"pages": 0, "img_skip": 0, "parents": 0, "children": 0, "naive": 0, "md_chars": 0}
    since_flush = 0

    for i, d in enumerate(docs):
        t0 = time.time()
        doc_id = d["doc_id"]
        md_path = out_dir / f"{doc_id}.md"
        if args.reuse_md and md_path.exists():
            md = md_path.read_text()
            st_summary = "md-reused"
        else:
            md, st = convert_pdf(repo / d["source_path"], vendor=d["vendor"],
                                 doc_title=d["title"])
            md_path.write_text(md)
            st_summary = st.summary()
            tot["pages"] += st.pages_total
            tot["img_skip"] += st.pages_skipped_image + st.pages_skipped_empty
        tot["md_chars"] += len(md)

        if len(md) < args.min_md_chars:
            tot["skipped_tiny"] = tot.get("skipped_tiny", 0) + 1
            print(f"[{i + 1}/{len(docs)}] {doc_id} | [WARN] md 仅 {len(md)} 字符（<{args.min_md_chars}，扉页/目录类近空文档），跳过不入库")
            continue

        if not args.md_only:
            meta = DocMeta(vendor=d["vendor"], model=d["model"], sw_version=d["sw_version"],
                           doc_id=doc_id, title=d["title"])
            body = _body_for_chunk(md)
            parents, children = chunk_structured(body, meta, counter)
            for c in children:
                c.breadcrumb = c.breadcrumb[:_BREADCRUMB_MAX]
                c.bm25_text = build_bm25_text(c.text, c.breadcrumb)[:_BM25_TEXT_MAX]
            from netrag.index.hybrid_schema import insert_hybrid

            insert_hybrid(client, parents, children, embedder, batch=args.embed_batch)
            tot["parents"] += len(parents)
            tot["children"] += len(children)

            n_naive = 0
            if not args.skip_naive:
                from netrag.index.naive_schema import insert_naive

                naive_chunks = chunk_naive(body, meta, counter)
                insert_naive(client, naive_chunks, embedder, batch=args.embed_batch)
                tot["naive"] += len(naive_chunks)
                n_naive = len(naive_chunks)

            since_flush += 1
            if since_flush >= args.flush_every:
                client.flush("chunks")
                if not args.skip_naive:
                    client.flush("chunks_naive")
                since_flush = 0

        dt = time.time() - t0
        print(f"[{i + 1}/{len(docs)}] {doc_id} | {st_summary} "
              f"| par={tot['parents'] if not args.md_only else '-'} ch={tot['children'] if not args.md_only else '-'} "
              f"naive={tot['naive'] if not args.md_only else '-'} | {dt:.1f}s")

        if (i + 1) % 10 == 0 and not args.md_only:
            elapsed = time.time() - t_all
            rate = tot["children"] / elapsed if elapsed else 0.0
            eta = elapsed / (i + 1) * (len(docs) - i - 1)
            print(f"  == 累计 {tot} | elapsed {_fmt_secs(elapsed)} | children {rate:.1f}/s | ETA {_fmt_secs(eta)}")

    if not args.md_only:
        client.flush("chunks")
        if not args.skip_naive:
            client.flush("chunks_naive")
        stats_after = {c: client.get_collection_stats(c)["row_count"]
                       for c in ("chunks", "chunks_naive") if client.has_collection(c)}
        print(f"rebuild 后 collection 行数: {stats_after}")
        print(f"索引总量: {tot}")
        print(f"总耗时 {_fmt_secs(time.time() - t_all)}")
    else:
        print(f"md-only 完成：{len(docs)} 个文件 -> {out_dir}，累计 {tot}")


if __name__ == "__main__":
    main()
