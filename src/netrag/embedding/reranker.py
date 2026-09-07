import os


class BgeReranker:
    def __init__(self, model_name: str = "BAAI/bge-reranker-v2-m3") -> None:
        # 与 bge_m3.py 同因：FlagEmbedding/transformers 对 repo id 会触网
        # （list_repo_templates 等），网络抖动即超时；先解析为本地缓存快照路径
        # （scripts/download_models.py 已预下载），本地路径可直接加载、不重下载
        if not os.path.isdir(model_name):
            from huggingface_hub import snapshot_download

            try:
                model_name = snapshot_download(
                    repo_id=model_name,
                    allow_patterns=["*.json", "pytorch_model.bin", "*.safetensors",
                                    "sentencepiece.bpe.model", "tokenizer*"],
                )
            except Exception:
                # 全量已在本地缓存（download_models.py）：网络抖动时直接用缓存快照，
                # 绝不触发重下载
                from huggingface_hub import scan_cache_dir

                snaps = [s for r in scan_cache_dir().repos if r.repo_id == model_name
                         for s in r.revisions]
                if not snaps:
                    raise
                model_name = str(max(snaps, key=lambda s: s.last_modified).path)
        from FlagEmbedding import FlagReranker

        self._model = FlagReranker(model_name, use_fp16=True, devices=["cuda:0"])

    def rerank(self, query: str, texts: list[str]) -> list[float]:
        pairs = [[query, t] for t in texts]
        scores = self._model.compute_score(pairs, normalize=True)
        return [float(s) for s in (scores if isinstance(scores, list) else [scores])]
