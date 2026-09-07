import re
from dataclasses import dataclass

from netrag.embedding.base import TokenCounter
from netrag.ingestion.section_tree import parse_sections
from netrag.ingestion.types import Chunk, DocMeta

_FENCE = re.compile(r"```.*?```", re.DOTALL)
_TABLE = re.compile(r"(?:^\|.*\|\s*$\n?)+", re.MULTILINE)
_PARENT_CAP = 4000


@dataclass
class _Block:
    kind: str  # paragraph | code | table
    text: str


def _split_blocks(body_md: str) -> list[_Block]:
    fences = [(_FENCE, "code"), (_TABLE, "table")]
    spans: list[tuple[int, int, str]] = []
    for pat, kind in fences:
        for m in pat.finditer(body_md):
            if not any(s < m.end() and m.start() < e for s, e, _ in spans):
                spans.append((m.start(), m.end(), kind))
    spans.sort()
    blocks: list[_Block] = []
    pos = 0
    for s, e, kind in spans:
        if body_md[pos:s].strip():
            blocks.append(_Block("paragraph", body_md[pos:s].strip()))
        blocks.append(_Block(kind, body_md[s:e].strip()))
        pos = e
    if body_md[pos:].strip():
        blocks.append(_Block("paragraph", body_md[pos:].strip()))
    return blocks


def _split_table_rows(table_text: str, counter: TokenCounter, max_tokens: int) -> list[str]:
    lines = table_text.split("\n")
    header = [l for l in lines[:2] if l.strip().startswith("|")]
    body = [l for l in lines[2:] if l.strip()]
    tmpl = "表头: " + " ".join(header) + "\n" if header else ""
    groups, cur, cur_len = [], [], 0
    for l in body:
        n = counter.count(l)
        if cur and cur_len + n > max_tokens:
            groups.append(tmpl + "\n".join(cur))
            cur, cur_len = [], 0
        cur.append(l)
        cur_len += n
    if cur:
        groups.append(tmpl + "\n".join(cur))
    return groups


def _split_paragraph_lines(text: str, counter: TokenCounter, max_tokens: int) -> list[str]:
    lines = text.split("\n")
    parts, cur, cur_len = [], [], 0
    for line in lines:
        n = counter.count(line)
        if cur and cur_len + n > max_tokens:
            parts.append("\n".join(cur))
            cur, cur_len = [], 0
        cur.append(line)
        cur_len += n
    if cur:
        parts.append("\n".join(cur))
    return parts


def chunk_structured(md_text: str, meta: DocMeta, counter: TokenCounter,
                     child_min: int = 180, child_max: int = 500) -> tuple[list[Chunk], list[Chunk]]:
    parents: list[Chunk] = []
    children: list[Chunk] = []
    for sec in parse_sections(md_text, meta.title):
        if not sec.body_md.strip():
            continue
        p_seq = len(parents) + 1
        p_id = f"{meta.doc_id}#p{p_seq}"
        body = sec.body_md
        if counter.count(body) > _PARENT_CAP:
            acc, acc_len, cut = [], 0, []
            for para in body.split("\n\n"):
                n = counter.count(para)
                if acc and acc_len + n > _PARENT_CAP:
                    cut.append("\n\n".join(acc))
                    acc, acc_len = [], 0
                acc.append(para)
                acc_len += n
            cut.append("\n\n".join(acc))
            body = cut[0] + "\n\n<!-- truncated -->"
        parents.append(Chunk(
            chunk_id=p_id, doc_id=meta.doc_id, text=body, breadcrumb=sec.breadcrumb,
            vendor=meta.vendor, model=meta.model, sw_version=meta.sw_version, is_parent=True,
        ))
        blocks = _split_blocks(sec.body_md)
        units: list[_Block] = []
        for b in blocks:
            if b.kind == "table" and counter.count(b.text) > child_max:
                for g in _split_table_rows(b.text, counter, child_max):
                    units.append(_Block("table", g))
            elif b.kind == "paragraph" and counter.count(b.text) > child_max:
                for part in _split_paragraph_lines(b.text, counter, child_max):
                    units.append(_Block("paragraph", part))
            else:
                units.append(b)
        cur: list[str] = []
        cur_kind: str | None = None
        cur_len = 0

        def flush() -> None:
            nonlocal cur, cur_kind, cur_len
            if not cur:
                return
            children.append(Chunk(
                chunk_id=f"{meta.doc_id}#c{len(children) + 1}", doc_id=meta.doc_id,
                text="\n\n".join(cur), breadcrumb=sec.breadcrumb,
                vendor=meta.vendor, model=meta.model, sw_version=meta.sw_version, parent_id=p_id,
            ))
            cur, cur_kind, cur_len = [], None, 0

        for b in units:
            n = counter.count(b.text)
            hard = b.kind in ("code", "table")
            if hard:
                flush()
                cur, cur_kind, cur_len = [b.text], b.kind, n
                flush()
                continue
            if cur_kind is None:
                cur_kind = "paragraph"
            if cur and (cur_len + n > child_max or cur_len >= child_min):
                flush()
            cur.append(b.text)
            cur_len += n
        if cur:
            flush()
    return parents, children
