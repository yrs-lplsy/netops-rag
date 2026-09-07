import pytest

from netrag.config import Settings
from netrag.embedding.bge_m3 import BGEM3Embedder
from netrag.embedding.reranker import BgeReranker

pytestmark = pytest.mark.gpu


def test_bge_m3_dense_sparse():
    emb = BGEM3Embedder(Settings.from_env().embed_model)
    out = emb.embed_query("华为S5735 ospf network-type 怎么配置")
    assert len(out.dense[0]) == 1024
    assert len(out.sparse[0]) > 0
    assert all(isinstance(k, int) and isinstance(v, float) for k, v in out.sparse[0].items())


def test_reranker_scores():
    rr = BgeReranker(Settings.from_env().rerank_model)
    scores = rr.rerank("ospf network-type", ["ospf network-type broadcast 命令说明", "vlan 20 创建方法"])
    assert len(scores) == 2
    assert scores[0] > scores[1]
