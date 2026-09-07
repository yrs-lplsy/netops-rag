from netrag.config import Settings


def test_from_env_reads_overrides(monkeypatch, tmp_path):
    monkeypatch.setenv("SILICONFLOW_API_KEY", "sk-test")
    monkeypatch.setenv("MILVUS_URI", "http://127.0.0.1:19530")
    s = Settings.from_env(env_file=tmp_path / "absent.env")
    assert s.sf_api_key == "sk-test"
    assert s.milvus_uri == "http://127.0.0.1:19530"


def test_from_env_defaults(monkeypatch, tmp_path):
    # 环境变量可能被先前用例加载 repo .env（load_dotenv）污染，先清干净再断言代码默认值
    for k in ("HF_ENDPOINT", "MILVUS_URI", "SILICONFLOW_API_KEY", "SILICONFLOW_BASE_URL",
              "LLM_MODEL", "EMBED_MODEL", "RERANKER_MODEL"):
        monkeypatch.delenv(k, raising=False)
    s = Settings.from_env(env_file=tmp_path / "absent.env")
    assert s.hf_endpoint == "https://hf-mirror.com"
    assert s.sf_base_url == "https://api.siliconflow.cn/v1"
    assert s.llm_model == "Qwen/Qwen2.5-7B-Instruct"
    assert s.embed_model == "BAAI/bge-m3"
    assert s.sf_api_key == ""


def test_from_env_reads_deepseek_overrides(monkeypatch, tmp_path):
    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-ds-test")
    monkeypatch.setenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
    monkeypatch.setenv("DEEPSEEK_MODEL", "deepseek-chat")
    s = Settings.from_env(env_file=tmp_path / "absent.env")
    assert s.deepseek_api_key == "sk-ds-test"
    assert s.deepseek_base_url == "https://api.deepseek.com/v1"
    assert s.deepseek_model == "deepseek-chat"


def test_from_env_deepseek_defaults_empty(monkeypatch, tmp_path):
    # 模型名不设代码默认：调用方（judge 后端）必须校验非空并指路 env 变量
    for k in ("DEEPSEEK_API_KEY", "DEEPSEEK_BASE_URL", "DEEPSEEK_MODEL"):
        monkeypatch.delenv(k, raising=False)
    s = Settings.from_env(env_file=tmp_path / "absent.env")
    assert s.deepseek_api_key == ""
    assert s.deepseek_base_url == "https://api.deepseek.com"
    assert s.deepseek_model == ""
