import hashlib

from netrag.embedding.base import EmbeddingOutput


def _stable_vec(text: str, dim: int) -> list[float]:
    h = hashlib.sha256(text.encode("utf-8")).digest()
    vec = [(h[i % len(h)] / 255.0) - 0.5 for i in range(dim)]
    norm = sum(x * x for x in vec) ** 0.5 or 1.0
    return [x / norm for x in vec]


def _stable_sparse(text: str) -> dict[int, float]:
    """确定性伪稀疏词元：2-4 个 (token_id, 正权重)，与 BGEM3Embedder 输出同构。"""
    h = hashlib.sha256(("sparse:" + text).encode("utf-8")).digest()
    n = 2 + h[0] % 3
    out: dict[int, float] = {}
    for i in range(n):
        tok = int.from_bytes(h[1 + i * 4:5 + i * 4], "big") % 100000
        out[tok] = round(0.5 + h[1 + i] / 255.0, 4)
    return out


class DummyEmbedder:
    def __init__(self, dim: int = 8) -> None:
        self.dim = dim

    def embed_documents(self, texts: list[str]) -> EmbeddingOutput:
        return EmbeddingOutput(dense=[_stable_vec(t, self.dim) for t in texts],
                               sparse=[_stable_sparse(t) for t in texts])

    def embed_query(self, text: str) -> EmbeddingOutput:
        return self.embed_documents([text])


class DummyTokenCounter:
    def count(self, text: str) -> int:
        return len(text.split())
