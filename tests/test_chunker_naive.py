from netrag.ingestion.chunker_naive import chunk_naive
from netrag.ingestion.types import DocMeta
from netrag.embedding.dummy import DummyTokenCounter

META = DocMeta(vendor="cisco", model="Catalyst 9300", sw_version="17.9",
               doc_id="doc1", title="T")


def make_md(words: int) -> str:
    return "\n\n".join(f"para{i} " + " ".join(f"w{j}" for j in range(60)) for i in range(words // 60 + 1))


def test_window_size_and_ids():
    chunks = chunk_naive(make_md(1000), META, DummyTokenCounter(), size=200, overlap=20)
    assert all(c.chunk_id.startswith("doc1#n") for c in chunks)
    # 任何 chunk 不超窗口，且存在接近窗口大小的 chunk（贪心合并生效）
    sizes = [DummyTokenCounter().count(c.text) for c in chunks]
    assert all(s <= 210 for s in sizes)
    assert max(sizes) >= 150
    assert chunks[0].breadcrumb == "T"
    assert chunks[0].vendor == "cisco"


def test_small_doc_single_chunk():
    chunks = chunk_naive("hello world", META, DummyTokenCounter())
    assert len(chunks) == 1
    assert chunks[0].chunk_id == "doc1#n1"


def test_overlap_present():
    md = "\n\n".join(" ".join(f"w{i}" for i in range(50)) for _ in range(8))
    chunks = chunk_naive(md, META, DummyTokenCounter(), size=100, overlap=20)
    assert len(chunks) >= 2
    tail = chunks[0].text.split()[-10:]
    assert any(w in chunks[1].text.split() for w in tail)
