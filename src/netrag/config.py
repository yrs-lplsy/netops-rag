import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

_REPO_ROOT = Path(__file__).resolve().parents[2]


@dataclass
class Settings:
    hf_endpoint: str = "https://hf-mirror.com"
    milvus_uri: str = "http://localhost:19530"
    sf_api_key: str = ""
    sf_base_url: str = "https://api.siliconflow.cn/v1"
    llm_model: str = "Qwen/Qwen2.5-7B-Instruct"
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    deepseek_model: str = ""  # 模型名不设默认：调用方必须校验非空（防漂移硬编码）
    embed_model: str = "BAAI/bge-m3"
    rerank_model: str = "BAAI/bge-reranker-v2-m3"
    langfuse_public_key: str = ""
    langfuse_secret_key: str = ""
    langfuse_host: str = "https://cloud.langfuse.com"
    approve_secret: str = ""  # /approvals/{id}/approve 共享密钥门；空=不设防（启动警告）
    data_dir: Path = field(default_factory=lambda: _REPO_ROOT / "data")
    reports_dir: Path = field(default_factory=lambda: _REPO_ROOT / "docs" / "eval-reports")

    @classmethod
    def from_env(cls, env_file: Path | None = None) -> "Settings":
        if env_file is None:
            env_file = _REPO_ROOT / ".env"
        if env_file.exists():
            load_dotenv(env_file)
        get = lambda k, d: os.environ.get(k, d)  # noqa: E731
        return cls(
            hf_endpoint=get("HF_ENDPOINT", cls.hf_endpoint),
            milvus_uri=get("MILVUS_URI", "http://localhost:19530"),
            sf_api_key=get("SILICONFLOW_API_KEY", ""),
            sf_base_url=get("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1"),
            llm_model=get("LLM_MODEL", "Qwen/Qwen2.5-7B-Instruct"),
            deepseek_api_key=get("DEEPSEEK_API_KEY", ""),
            deepseek_base_url=get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            deepseek_model=get("DEEPSEEK_MODEL", ""),
            embed_model=get("EMBED_MODEL", "BAAI/bge-m3"),
            rerank_model=get("RERANKER_MODEL", "BAAI/bge-reranker-v2-m3"),
            langfuse_public_key=get("LANGFUSE_PUBLIC_KEY", ""),
            langfuse_secret_key=get("LANGFUSE_SECRET_KEY", ""),
            langfuse_host=get("LANGFUSE_HOST", "https://cloud.langfuse.com"),
            approve_secret=get("APPROVE_SECRET", ""),
        )
