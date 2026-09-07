import pytest

from netrag.embedding.dummy import DummyEmbedder
from netrag.index.hybrid_schema import PARENTS, create_hybrid, insert_hybrid
from netrag.index.milvus_client import get_milvus, wait_healthy
from netrag.ingestion.types import Chunk, DocMeta

pytestmark = pytest.mark.milvus

META = DocMeta(vendor="cisco", model="C9300", sw_version="17.9", doc_id="d1", title="手册")

# PARENTS 并入 chunks（原因：Milvus 2.5.6 拒绝无向量 schema，
# MilvusException(1100, "schema does not contain vector field")，2026-09-04 实测）。
# 父块 is_parent=True + dense 零向量，检索子块统一加 is_parent == false 过滤。

# 独立测试 collection：避免 drop 共享的 chunks（真实 680 行 hybrid 索引）
TEST_COLLECTION = "test_hybrid_smoke"


def _parent(n):
    return Chunk(chunk_id=f"d1#p{n}", doc_id="d1", text=f"父块{n}整节内容 " * 20,
                 breadcrumb="手册 > 节" + str(n), vendor="cisco", model="C9300",
                 sw_version="17.9", is_parent=True)


def _child(n, parent_id):
    return Chunk(chunk_id=f"d1#c{n}", doc_id="d1", text=f"ospf network-type 子块{n} " * 5,
                 breadcrumb="手册 > 节1", vendor="cisco", model="C9300",
                 sw_version="17.9", parent_id=parent_id)


def test_create_insert_query_roundtrip():
    client = get_milvus()
    wait_healthy(client)
    try:
        create_hybrid(client, drop=True, collection=TEST_COLLECTION)
        parents = [_parent(1), _parent(2)]
        children = [_child(1, "d1#p1"), _child(2, "d1#p1"), _child(3, "d1#p2")]
        for c in children:
            c.bm25_text = "手册 节1 ospf network-type " * 3
        insert_hybrid(client, parents, children, DummyEmbedder(dim=1024),
                      collection=TEST_COLLECTION)
        client.flush(TEST_COLLECTION)
        client.flush(PARENTS)  # 回退布局下 PARENTS 即 chunks 别名，真实集合不受影响
        got = client.query(TEST_COLLECTION, filter='chunk_id == "d1#p1"',
                           output_fields=["text", "breadcrumb", "is_parent"])
        assert got and "父块1" in got[0]["text"]
        assert got[0]["is_parent"] is True
        # 子块检索：is_parent == false 过滤后按 parent_id 关联
        n = client.query(TEST_COLLECTION, filter='parent_id == "d1#p1" and is_parent == false',
                         output_fields=["chunk_id", "parent_id"])
        assert len(n) == 2
        assert {r["chunk_id"] for r in n} == {"d1#c1", "d1#c2"}
    finally:
        client.drop_collection(TEST_COLLECTION)


def test_bm25_function_search():
    """BM25 函数字段（chinese analyzer）可被检索，且 is_parent 过滤生效。"""
    client = get_milvus()
    wait_healthy(client)
    try:
        create_hybrid(client, drop=True, collection=TEST_COLLECTION)
        parents = [_parent(1)]
        children = [_child(1, "d1#p1"), _child(2, "d1#p1")]
        for c in children:
            c.bm25_text = "手册 节1 ospf network-type " * 3
        insert_hybrid(client, parents, children, DummyEmbedder(dim=1024),
                      collection=TEST_COLLECTION)
        client.flush(TEST_COLLECTION)
        res = client.search(TEST_COLLECTION, data=["ospf 子块"], anns_field="bm25_sparse",
                            limit=10, filter="is_parent == false", output_fields=["chunk_id"])
        hits = res[0]
        assert hits and hits[0]["entity"]["chunk_id"] in {"d1#c1", "d1#c2"}
        # 父块 bm25_text 为空，不该出现在 BM25 命中里
        assert all(h["distance"] > 0 for h in hits)
    finally:
        client.drop_collection(TEST_COLLECTION)
