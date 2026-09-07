from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class EmbeddingOutput:
    dense: list[list[float]]
    sparse: list[dict[int, float]] = field(default_factory=list)


class Embedder(Protocol):
    dim: int

    def embed_documents(self, texts: list[str]) -> EmbeddingOutput: ...

    def embed_query(self, text: str) -> EmbeddingOutput: ...


class TokenCounter(Protocol):
    def count(self, text: str) -> int: ...
