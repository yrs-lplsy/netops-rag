from dataclasses import dataclass
from typing import Protocol


@dataclass
class RetrievedChunk:
    chunk_id: str
    text: str
    score: float
    doc_id: str
    breadcrumb: str
    vendor: str
    model: str
    sw_version: str
    parent_id: str | None = None
    parent_text: str | None = None


@dataclass
class MetadataFilter:
    vendor: str | None = None
    model: str | None = None
    sw_version: str | None = None

    def to_milvus_expr(self) -> str | None:
        parts = [
            f'{k} == "{v}"' for k, v in
            (("vendor", self.vendor), ("model", self.model), ("sw_version", self.sw_version)) if v
        ]
        return " and ".join(parts) if parts else None


class Retriever(Protocol):
    name: str

    def retrieve(self, query: str, top_k: int = 5,
                 filters: MetadataFilter | None = None) -> list[RetrievedChunk]: ...
