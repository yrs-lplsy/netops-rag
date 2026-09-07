"""经 hf-mirror 预下载模型到本机 HF 缓存，FlagEmbedding/transformers 之后离线加载。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from netrag.config import Settings


def main() -> None:
    s = Settings.from_env()
    # huggingface_hub 在 import 时读取 HF_ENDPOINT 常量，必须在 import 前设置
    os.environ.setdefault("HF_ENDPOINT", s.hf_endpoint)
    # hf-mirror 无法代理 xet CAS 服务器（cas-server.xethub.hf.co），强制经典 HTTP 下载
    os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
    from huggingface_hub import snapshot_download

    for repo in (s.embed_model, s.rerank_model):
        # 仅下载加载所需文件：hf-mirror 对 imgs/.DS_Store 等垃圾文件返回 403，
        # onnx/ 目录另有 2.3GB 且 FlagEmbedding/transformers 加载用不到
        path = snapshot_download(
            repo_id=repo,
            allow_patterns=[
                "*.json", "pytorch_model.bin", "*.safetensors",
                "sentencepiece.bpe.model", "colbert_linear.pt", "sparse_linear.pt",
            ],
        )
        print(f"downloaded {repo} -> {path}")


if __name__ == "__main__":
    main()
