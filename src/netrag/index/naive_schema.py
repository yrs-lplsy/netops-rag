from pymilvus import DataType, MilvusClient

from netrag.embedding.base import Embedder
from netrag.ingestion.types import Chunk

COLLECTION = "chunks_naive"


def create_naive(client: MilvusClient, drop: bool = False, collection: str = COLLECTION) -> None:
    if drop and client.has_collection(collection):
        client.drop_collection(collection)
    if client.has_collection(collection):
        return
    schema = client.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field("chunk_id", DataType.VARCHAR, is_primary=True, max_length=128)
    schema.add_field("doc_id", DataType.VARCHAR, max_length=128)
    schema.add_field("vendor", DataType.VARCHAR, max_length=32)
    schema.add_field("model", DataType.VARCHAR, max_length=64)
    schema.add_field("sw_version", DataType.VARCHAR, max_length=32)
    schema.add_field("text", DataType.VARCHAR, max_length=8192)
    schema.add_field("dense", DataType.FLOAT_VECTOR, dim=1024)
    idx = client.prepare_index_params()
    idx.add_index(field_name="dense", index_type="HNSW", metric_type="COSINE",
                  params={"M": 16, "efConstruction": 200})
    client.create_collection(collection, schema=schema, index_params=idx)


def insert_naive(client: MilvusClient, chunks: list[Chunk], embedder: Embedder, batch: int = 32,
                 collection: str = COLLECTION) -> None:
    for i in range(0, len(chunks), batch):
        part = chunks[i:i + batch]
        out = embedder.embed_documents([c.text for c in part])
        rows = [
            {"chunk_id": c.chunk_id, "doc_id": c.doc_id, "vendor": c.vendor,
             "model": c.model, "sw_version": c.sw_version, "text": c.text[:8000], "dense": d}
            for c, d in zip(part, out.dense)
        ]
        client.insert(collection, rows)
