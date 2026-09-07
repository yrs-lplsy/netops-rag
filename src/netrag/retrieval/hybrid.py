"""三路混合检索：dense + BM25 函数 + bge 稀疏 → RRFRanker 融合 → 可选精排 → 父块回填。

与任务书代码的两处偏差（沿 Task 14 回退布局与 pymilvus 2.5.18 实测行为）：
- 父块并入检索集合（Milvus 2.5.6 拒绝无向量 schema，独立 chunk_parents 建不出来，
  hybrid_schema.PARENTS 即 CHUNKS）。父块是零向量/空 bm25 占位行，检索统一加
  `is_parent == false` 排除；父块回填按 `chunk_id in [...] and is_parent == true`
  在同一集合内查询。parents_collection 参数保留兼容任务书接口：该集合确实存在时
  查它，否则（默认）回落到检索集合本身。
- pymilvus 2.5.18 的 MilvusClient.hybrid_search 无 filter 参数——filter 会落入
  **kwargs 被静默吞掉、过滤不生效（读源码 milvus_client.py/grpc_handler.py 验证）；
  标量过滤必须写入每个 AnnSearchRequest.expr（子请求各带表达式，服务端逐路应用）。
"""

from pymilvus import AnnSearchRequest, MilvusClient, RRFRanker

from netrag.embedding.base import Embedder
from netrag.embedding.reranker import BgeReranker
from netrag.retrieval.base import MetadataFilter, RetrievedChunk

_FIELDS = ["chunk_id", "parent_id", "doc_id", "vendor", "model", "sw_version", "breadcrumb", "text"]


class HybridRetriever:
    def __init__(self, client: MilvusClient, embedder: Embedder,
                 reranker: BgeReranker | None = None,
                 collection: str = "chunks", parents_collection: str = "chunk_parents",
                 paths: tuple[str, ...] = ("dense", "bm25", "sparse"),
                 rrf_k: int = 60, recall_n: int = 20) -> None:
        self._client = client
        self._embedder = embedder
        self._reranker = reranker
        self._collection = collection
        # 回退布局：父块与子块同集合；若指定的父集合不存在（默认 chunk_parents 建不出
        # 来），父块查询回落到检索集合本身
        self._parents = parents_collection if client.has_collection(parents_collection) else collection
        self._paths = paths
        self._rrf_k = rrf_k
        self._recall_n = recall_n
        self.name = f"hybrid({'+'.join(paths)}{'|rerank' if reranker else ''})"

    def retrieve(self, query: str, top_k: int = 5,
                 filters: MetadataFilter | None = None) -> list[RetrievedChunk]:
        emb = self._embedder.embed_query(query)
        expr = "is_parent == false"  # 父块占位行不参与向量检索
        fexpr = filters.to_milvus_expr() if filters else None
        if fexpr:
            expr = f"{expr} and ({fexpr})"
        reqs = []
        if "dense" in self._paths:
            reqs.append(AnnSearchRequest(
                data=[emb.dense[0]], anns_field="dense",
                param={"metric_type": "COSINE", "params": {"ef": 64}},
                limit=self._recall_n, expr=expr))
        if "bm25" in self._paths:
            # BM25 路传原始 query 文本，由服务端 BM25 函数按 chinese analyzer 编码
            reqs.append(AnnSearchRequest(
                data=[query], anns_field="bm25_sparse",
                param={"metric_type": "BM25"}, limit=self._recall_n, expr=expr))
        if "sparse" in self._paths:
            reqs.append(AnnSearchRequest(
                data=[emb.sparse[0]], anns_field="bge_sparse",
                param={"metric_type": "IP"}, limit=self._recall_n, expr=expr))
        if not reqs:
            return []
        res = self._client.hybrid_search(
            self._collection, reqs=reqs, ranker=RRFRanker(self._rrf_k),
            limit=max(top_k * 4, self._recall_n), output_fields=_FIELDS,
        )
        chunks = [RetrievedChunk(
            chunk_id=h["chunk_id"], text=h["entity"]["text"], score=h["distance"],
            doc_id=h["entity"]["doc_id"], breadcrumb=h["entity"]["breadcrumb"],
            vendor=h["entity"]["vendor"], model=h["entity"]["model"],
            sw_version=h["entity"]["sw_version"], parent_id=h["entity"]["parent_id"] or None,
        ) for h in res[0]]
        if self._reranker and chunks:
            scores = self._reranker.rerank(query, [c.text for c in chunks])
            chunks = [c for c, _ in sorted(zip(chunks, scores), key=lambda x: -x[1])]
        chunks = chunks[:top_k]
        pids = sorted({c.parent_id for c in chunks if c.parent_id})
        if pids:
            flt = f'chunk_id in [{", ".join(f"{p!r}" for p in pids)}]'.replace("'", '"')
            if self._parents == self._collection:  # 回退布局：父块与子块同集合
                flt += " and is_parent == true"
            rows = self._client.query(self._parents, filter=flt,
                                      output_fields=["chunk_id", "text"])
            pmap = {r["chunk_id"]: r["text"] for r in rows}
            for c in chunks:
                c.parent_text = pmap.get(c.parent_id)
        return chunks
