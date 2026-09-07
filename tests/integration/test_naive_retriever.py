import pytest

from netrag.embedding.dummy import DummyEmbedder
from netrag.index.milvus_client import get_milvus, wait_healthy
from netrag.index.naive_schema import create_naive, insert_naive
from netrag.ingestion.types import Chunk, DocMeta
from netrag.retrieval.base import MetadataFilter
from netrag.retrieval.naive import NaiveRetriever

pytestmark = pytest.mark.milvus

META = DocMeta(vendor="cisco", model="Catalyst 9300", sw_version="17.9", doc_id="doc1", title="T")

CHUNK1_TEXT = "ospf network-type broadcast 配置说明"

# 独立测试 collection：避免 drop 共享的 chunks_naive（真实 80 行索引）
TEST_COLLECTION = "test_naive_smoke"


def _chunk(n: int, text: str) -> Chunk:
    return Chunk(chunk_id=f"doc1#n{n}", doc_id="doc1", text=text,
                 breadcrumb="T", vendor="cisco", model="Catalyst 9300", sw_version="17.9")


def test_roundtrip_search():
    client = get_milvus()
    wait_healthy(client)
    try:
        create_naive(client, drop=True, collection=TEST_COLLECTION)
        # DummyEmbedder 默认 dim=8，必须与 naive schema 的 dense dim=1024 一致
        insert_naive(client, [
            _chunk(1, CHUNK1_TEXT),
            _chunk(2, "vlan 20 创建与命名配置说明"),
            _chunk(3, "stp root primary 生成树根桥配置"),
        ], DummyEmbedder(dim=1024), collection=TEST_COLLECTION)
        client.flush(TEST_COLLECTION)
        r = NaiveRetriever(client, DummyEmbedder(dim=1024), collection=TEST_COLLECTION)
        # DummyEmbedder 是哈希伪随机向量，查询与文档文本完全一致时 cosine=1 确定命中自身
        hits = r.retrieve(CHUNK1_TEXT, top_k=2)
        assert hits[0].chunk_id == "doc1#n1"
        assert len(hits) == 2
        assert hits[0].score == pytest.approx(1.0, abs=1e-4)
        assert hits[0].doc_id == "doc1"
        assert hits[0].vendor == "cisco"
        assert hits[0].model == "Catalyst 9300"
        assert hits[0].sw_version == "17.9"
        assert CHUNK1_TEXT in hits[0].text

        # MetadataFilter 走真实 Milvus 标量过滤：命中存在的 sw_version，不存在的为空
        matched = r.retrieve(CHUNK1_TEXT, top_k=3, filters=MetadataFilter(sw_version="17.9"))
        assert matched and all(h.sw_version == "17.9" for h in matched)
        assert r.retrieve(CHUNK1_TEXT, top_k=3, filters=MetadataFilter(sw_version="17.0")) == []
    finally:
        client.drop_collection(TEST_COLLECTION)
