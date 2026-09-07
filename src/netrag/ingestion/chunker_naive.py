from netrag.embedding.base import TokenCounter
from netrag.ingestion.types import Chunk, DocMeta


def _split_paragraphs(md_text: str) -> list[str]:
    paras = [p.strip() for p in md_text.split("\n\n") if p.strip()]
    return paras or [md_text.strip()]


def chunk_naive(md_text: str, meta: DocMeta, counter: TokenCounter, size: int = 512, overlap: int = 50) -> list[Chunk]:
    paras = _split_paragraphs(md_text)
    units: list[list[str]] = []  # 每个单元=一行，行内不再切
    for p in paras:
        units.extend(p.split("\n"))
    chunks: list[Chunk] = []
    cur: list[str] = []
    cur_len = 0
    seq = 0

    def flush() -> None:
        nonlocal cur, cur_len, seq
        if not cur:
            return
        seq += 1
        chunks.append(Chunk(
            chunk_id=f"{meta.doc_id}#n{seq}", doc_id=meta.doc_id, text="\n".join(cur).strip(),
            breadcrumb=meta.title, vendor=meta.vendor, model=meta.model, sw_version=meta.sw_version,
        ))
        # overlap：保留尾部若干行直到累计 token 接近 overlap
        kept: list[str] = []
        kept_len = 0
        for line in reversed(cur):
            l = counter.count(line)
            if kept_len + l > overlap and kept:
                break
            kept.insert(0, line)
            kept_len += l
        cur, cur_len = kept, kept_len

    for line in units:
        l = counter.count(line)
        if cur and cur_len + l > size:
            flush()
        cur.append(line)
        cur_len += l
    flush()
    return chunks
