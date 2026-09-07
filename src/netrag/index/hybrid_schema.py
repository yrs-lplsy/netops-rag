"""Hybrid 索引 schema：dense HNSW + BM25 函数稀疏 + bge 词元稀疏 + 标量过滤 + 父子 chunk。

PARENTS 并入 chunks（原因：Milvus 2.5.6 实测拒绝无向量 schema，
create_collection 报 MilvusException(1100, "schema does not contain vector field")，
2026-09-04 集成验证）。采用任务书回退方案：父块与子块同存 `chunks` 集合，
父块 is_parent=True、dense 填零向量、bm25_text/bge_sparse 置空（不参与向量检索）；
检索子块时统一加 `is_parent == false` 标量过滤，父块按唯一 chunk_id（或 parent_id
+ `is_parent == true`）查询。PARENTS 保留为 chunks 别名，调用方 flush/query 无需感知。
create_hybrid/insert_hybrid 的 `collection` 参数（默认 CHUNKS）用于集成测试隔离
（如 test_hybrid_smoke），不污染真实索引；回退布局下父子同集合，参数即该单一集合名。

与任务书代码的另两处偏差（均因 pymilvus 2.5.18 / Milvus 2.5.6 实际行为，已实测）：
- BM25 Function 必须经 schema.add_function(fn) 挂到 schema；
  create_collection(..., functions=[fn]) 不会把函数带给服务端（bm25_sparse 不被
  识别为函数输出字段，建 BM25 索引报 "only BM25 Function output field support
  BM25 metric type"）。
- 稀疏索引算法 DAOC_MAXSIM 需 Milvus 2.6，2.5.6 支持集为
  [TAAT_NAIVE, DAAT_WAND, DAAT_MAXSCORE]，这里取 DAAT_MAXSCORE。
"""

from pymilvus import DataType, Function, FunctionType, MilvusClient

from netrag.embedding.base import Embedder
from netrag.ingestion.types import Chunk

CHUNKS = "chunks"
PARENTS = CHUNKS  # 回退方案：无独立 chunk_parents 集合（见模块 docstring）

DENSE_DIM = 1024
# 统一集合需容纳父块整节文本（任务书 chunk_parents.text=65535）；子块按 [:8000] 截断
TEXT_MAX = 65535
_CHILD_TEXT_CAP = 8000
_PARENT_TEXT_CAP = 65000
_BREADCRUMB_CAP = 2000
_BM25_TEXT_CAP = 16000


def create_hybrid(client: MilvusClient, drop: bool = False, collection: str = CHUNKS) -> None:
    if drop and client.has_collection(collection):
        client.drop_collection(collection)
    if client.has_collection(collection):
        return
    schema = client.create_schema(auto_id=False, enable_dynamic_field=False)
    schema.add_field("chunk_id", DataType.VARCHAR, is_primary=True, max_length=128)
    schema.add_field("parent_id", DataType.VARCHAR, max_length=128)  # 父块自身为 ""
    schema.add_field("is_parent", DataType.BOOL)
    schema.add_field("doc_id", DataType.VARCHAR, max_length=128)
    schema.add_field("vendor", DataType.VARCHAR, max_length=32)
    schema.add_field("model", DataType.VARCHAR, max_length=64)
    schema.add_field("sw_version", DataType.VARCHAR, max_length=32)
    schema.add_field("breadcrumb", DataType.VARCHAR, max_length=2048)
    schema.add_field("text", DataType.VARCHAR, max_length=TEXT_MAX)
    schema.add_field("bm25_text", DataType.VARCHAR, max_length=16384,
                     enable_analyzer=True, analyzer_params={"type": "chinese"})
    schema.add_field("dense", DataType.FLOAT_VECTOR, dim=DENSE_DIM)
    schema.add_field("bm25_sparse", DataType.SPARSE_FLOAT_VECTOR)  # BM25 函数输出，insert 不写
    schema.add_field("bge_sparse", DataType.SPARSE_FLOAT_VECTOR)  # bge-m3 lexical weights
    schema.add_function(Function(name="bm25_fn", function_type=FunctionType.BM25,
                                 input_field_names=["bm25_text"],
                                 output_field_names=["bm25_sparse"]))
    idx = client.prepare_index_params()
    idx.add_index(field_name="dense", index_type="HNSW", metric_type="COSINE",
                  params={"M": 16, "efConstruction": 200})
    idx.add_index(field_name="bm25_sparse", index_type="SPARSE_INVERTED_INDEX", metric_type="BM25",
                  params={"inverted_index_algo": "DAAT_MAXSCORE"})  # DAOC_MAXSIM 需 Milvus 2.6
    idx.add_index(field_name="bge_sparse", index_type="SPARSE_INVERTED_INDEX", metric_type="IP")
    client.create_collection(collection, schema=schema, index_params=idx)


def insert_hybrid(client: MilvusClient, parents: list[Chunk], children: list[Chunk],
                  embedder: Embedder, batch: int = 16, collection: str = CHUNKS) -> None:
    zero = [0.0] * DENSE_DIM  # 父块不参与向量检索，dense 占位零向量
    for i in range(0, len(parents), batch):
        rows = [{
            "chunk_id": p.chunk_id, "parent_id": "", "is_parent": True,
            "doc_id": p.doc_id, "vendor": p.vendor, "model": p.model,
            "sw_version": p.sw_version, "breadcrumb": p.breadcrumb[:_BREADCRUMB_CAP],
            "text": p.text[:_PARENT_TEXT_CAP], "bm25_text": "",
            "dense": zero, "bge_sparse": {},
        } for p in parents[i:i + batch]]
        client.insert(collection, rows)
    for i in range(0, len(children), batch):
        part = children[i:i + batch]
        out = embedder.embed_documents([c.text for c in part])
        rows = [{
            "chunk_id": c.chunk_id, "parent_id": c.parent_id or "", "is_parent": False,
            "doc_id": c.doc_id, "vendor": c.vendor, "model": c.model,
            "sw_version": c.sw_version, "breadcrumb": c.breadcrumb[:_BREADCRUMB_CAP],
            "text": c.text[:_CHILD_TEXT_CAP], "bm25_text": (c.bm25_text or "")[:_BM25_TEXT_CAP],
            "dense": d, "bge_sparse": sp,
            # strict=True：dense/sparse 任一与文本数不等即抛错，不静默兜底
        } for c, d, sp in zip(part, out.dense, out.sparse, strict=True)]
        client.insert(collection, rows)
