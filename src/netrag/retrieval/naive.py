from pymilvus import MilvusClient

from netrag.embedding.base import Embedder
from netrag.retrieval.base import MetadataFilter, RetrievedChunk


class NaiveRetriever:
    name = "naive"

    def __init__(self, client: MilvusClient, embedder: Embedder, collection: str = "chunks_naive") -> None:
        self._client = client
        self._embedder = embedder
        self._collection = collection

    def retrieve(self, query: str, top_k: int = 5,
                 filters: MetadataFilter | None = None) -> list[RetrievedChunk]:
        q = self._embedder.embed_query(query).dense[0]
        res = self._client.search(
            self._collection, data=[q], limit=top_k,
            filter=(filters.to_milvus_expr() if filters else None) or "",
            output_fields=["doc_id", "vendor", "model", "sw_version", "text"],
            search_params={"metric_type": "COSINE", "params": {"ef": 64}},
        )
        hits = res[0]
        # naive collection 无 breadcrumb 字段，用 doc_id 充当文档级出处
        return [RetrievedChunk(
            chunk_id=h["chunk_id"], text=h["entity"]["text"], score=h["distance"],
            doc_id=h["entity"]["doc_id"], breadcrumb=h["entity"]["doc_id"],
            vendor=h["entity"]["vendor"], model=h["entity"]["model"],
            sw_version=h["entity"]["sw_version"],
        ) for h in hits]
