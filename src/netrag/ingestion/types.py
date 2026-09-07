from dataclasses import dataclass


@dataclass
class DocMeta:
    vendor: str
    model: str
    sw_version: str
    doc_id: str
    title: str


@dataclass
class Chunk:
    chunk_id: str
    doc_id: str
    text: str
    breadcrumb: str
    vendor: str
    model: str
    sw_version: str
    parent_id: str | None = None
    is_parent: bool = False
    bm25_text: str | None = None
