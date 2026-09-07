from netrag.embedding.base import EmbeddingOutput
from netrag.embedding.dummy import DummyEmbedder, DummyTokenCounter


def test_dummy_embedder_shapes_and_determinism():
    emb = DummyEmbedder(dim=8)
    out = emb.embed_documents(["display interface", "ospf network-type"])
    assert isinstance(out, EmbeddingOutput)
    assert len(out.dense) == 2 and len(out.dense[0]) == 8
    # sparse 与 dense 等长（每文本 2-4 个确定性词元），与 BGEM3Embedder 输出同构
    assert len(out.sparse) == 2
    assert all(2 <= len(sp) <= 4 and all(w > 0 for w in sp.values()) for sp in out.sparse)
    assert out.sparse[0] == emb.embed_documents(["display interface"]).sparse[0]  # 确定性
    assert out.sparse[0] != out.sparse[1]  # 不同文本不同词元
    again = emb.embed_query("display interface")
    assert again.dense[0] == out.dense[0]
    assert emb.dim == 8


def test_dummy_token_counter():
    tc = DummyTokenCounter()
    assert tc.count("a b  c") == 3
    assert tc.count("") == 0
