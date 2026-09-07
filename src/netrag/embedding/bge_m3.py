import os

from netrag.embedding.base import EmbeddingOutput

_SNAPSHOT_PATTERNS = [
    "*.json", "pytorch_model.bin", "*.safetensors",
    "sentencepiece.bpe.model", "colbert_linear.pt", "sparse_linear.pt",
]


class BGEM3Embedder:
    dim = 1024

    def __init__(self, model_name: str = "BAAI/bge-m3", batch_size: int = 16, max_length: int = 1024) -> None:
        # FlagEmbedding 内部对 repo 全量 snapshot_download，hf-mirror 对 imgs/.DS_Store 返回 403；
        # 先解析为本地缓存快照路径（scripts/download_models.py 已预下载），本地路径可直接加载
        if not os.path.isdir(model_name):
            from huggingface_hub import snapshot_download

            model_name = snapshot_download(repo_id=model_name, allow_patterns=_SNAPSHOT_PATTERNS)
        from FlagEmbedding import BGEM3FlagModel

        self._model = BGEM3FlagModel(model_name, use_fp16=True, devices=["cuda:0"])
        self.batch_size = batch_size
        self.max_length = max_length

    def _encode(self, texts: list[str]) -> EmbeddingOutput:
        out = self._model.encode(
            texts, batch_size=self.batch_size, max_length=self.max_length,
            return_dense=True, return_sparse=True,
            # FlagEmbedding 1.4.2 的参数名是 return_colbert_vecs；写 return_colbert 会落入
            # **kwargs 并透传给 tokenizer.pad()，transformers 5.x 会抛 TypeError
            return_colbert_vecs=False,
        )
        dense = [v.tolist() for v in out["dense_vecs"]]
        sparse = [{int(k): float(w) for k, w in lw.items()} for lw in out["lexical_weights"]]
        return EmbeddingOutput(dense=dense, sparse=sparse)

    def embed_documents(self, texts: list[str]) -> EmbeddingOutput:
        return self._encode(texts)

    def embed_query(self, text: str) -> EmbeddingOutput:
        return self._encode([text])
