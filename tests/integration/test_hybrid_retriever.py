import pytest

from netrag.embedding.dummy import DummyEmbedder
from netrag.index.hybrid_schema import PARENTS, create_hybrid, insert_hybrid
from netrag.index.milvus_client import get_milvus, wait_healthy
from netrag.ingestion.types import Chunk, DocMeta
from netrag.retrieval.hybrid import HybridRetriever

pytestmark = pytest.mark.milvus

META = DocMeta(vendor="cisco", model="C9300", sw_version="17.9", doc_id="d1", title="手册")

# 独立测试 collection（Task 14 模式）：不 drop 共享的 chunks（真实 680 行 hybrid 索引）
TEST_COLLECTION = "test_hybrid_smoke2"

# 回退布局：父块并入 chunks（PARENTS 即 CHUNKS 别名），父块 is_parent=True +
# 零向量/空 bm25 占位；检索子块统一加 is_parent == false 过滤。
C1_TEXT = "ospf network-type broadcast 配置"


class _InvertedReranker:
    """无 GPU 的 reranker 替身：打分与文本长度负相关，验证精排与 name 后缀。"""

    def rerank(self, query: str, texts: list[str]) -> list[float]:
        return [-float(len(t)) for t in texts]


def _build():
    client = get_milvus()
    wait_healthy(client)
    create_hybrid(client, drop=True, collection=TEST_COLLECTION)
    parents = [Chunk(chunk_id="d1#p1", doc_id="d1", text="ospf 网络类型整节父块",
                     breadcrumb="手册 > OSPF > network-type", vendor="cisco", model="C9300",
                     sw_version="17.9", is_parent=True)]
    children = [
        Chunk(chunk_id="d1#c1", doc_id="d1", text=C1_TEXT,
              breadcrumb="手册 > OSPF > network-type", vendor="cisco", model="C9300",
              sw_version="17.9", parent_id="d1#p1"),
        Chunk(chunk_id="d1#c2", doc_id="d1", text="vlan 20 创建",
              breadcrumb="手册 > VLAN", vendor="cisco", model="C9300",
              sw_version="17.9", parent_id="d1#p1"),
    ]
    for c in children:
        c.bm25_text = c.text.lower() + " " + c.breadcrumb
    insert_hybrid(client, parents, children, DummyEmbedder(dim=1024),
                  collection=TEST_COLLECTION)
    client.flush(TEST_COLLECTION)
    client.flush(PARENTS)  # PARENTS 即 chunks 别名，flush 共享真实集合无副作用
    return client


def test_three_path_and_parent_backfill():
    client = _build()
    try:
        r = HybridRetriever(client, DummyEmbedder(dim=1024), collection=TEST_COLLECTION)
        # DummyEmbedder 是哈希伪随机向量（稠密/稀疏无语义）：查询与目标子块文本完全
        # 一致时三路均确定第一（cosine=1 / 稀疏全重合 / BM25 全词命中），RRF 结果确定
        hits = r.retrieve(C1_TEXT, top_k=2)
        assert hits[0].chunk_id == "d1#c1"
        assert hits[0].parent_text == "ospf 网络类型整节父块"
        # 父块是零向量/空 bm25 占位行，is_parent == false 过滤后不得混入结果
        assert all(h.chunk_id != "d1#p1" for h in hits)
        assert r.name == "hybrid(dense+bm25+sparse)"
    finally:
        client.drop_collection(TEST_COLLECTION)


def test_paths_subset_changes_name_but_works():
    client = _build()
    try:
        r = HybridRetriever(client, DummyEmbedder(dim=1024), collection=TEST_COLLECTION,
                            paths=("dense",))
        hits = r.retrieve("ospf network-type", top_k=1)
        assert len(hits) == 1
        assert r.name == "hybrid(dense)"
    finally:
        client.drop_collection(TEST_COLLECTION)


def test_version_filter():
    client = _build()
    try:
        from netrag.retrieval.base import MetadataFilter
        r = HybridRetriever(client, DummyEmbedder(dim=1024), collection=TEST_COLLECTION)
        assert r.retrieve("ospf", top_k=3, filters=MetadataFilter(sw_version="17.7")) == []
        assert r.retrieve("ospf", top_k=3, filters=MetadataFilter(sw_version="17.9"))
    finally:
        client.drop_collection(TEST_COLLECTION)


def test_reranker_reorders_and_names():
    client = _build()
    try:
        r = HybridRetriever(client, DummyEmbedder(dim=1024), collection=TEST_COLLECTION,
                            reranker=_InvertedReranker())
        assert r.name == "hybrid(dense+bm25+sparse|rerank)"
        # 逆序精排：召回池里最长文本（父块同集合但被 is_parent 过滤，最长子块=c1）
        # 得最低分，c1 不再第一；父块回填仍生效
        hits = r.retrieve(C1_TEXT, top_k=2)
        assert len(hits) == 2
        assert hits[0].chunk_id == "d1#c2"
        assert hits[1].chunk_id == "d1#c1"
        assert hits[1].parent_text == "ospf 网络类型整节父块"
    finally:
        client.drop_collection(TEST_COLLECTION)
