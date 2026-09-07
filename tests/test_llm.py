import httpx
import pytest

from netrag.config import Settings
from netrag.generation.llm import LLMClient, LLMConfigError


def _mock_client(payload: dict) -> LLMClient:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json=payload)

    s = Settings(sf_api_key="sk-test", llm_model="test-model")
    return LLMClient(s, http_client=httpx.Client(transport=httpx.MockTransport(handler)))


def test_missing_key_raises():
    with pytest.raises(LLMConfigError):
        LLMClient(Settings(sf_api_key=""))


def test_chat_returns_content():
    payload = {"choices": [{"message": {"content": "答案文本"}}], "usage": {"total_tokens": 10}}
    client = _mock_client(payload)
    out = client.chat([{"role": "user", "content": "hi"}])
    assert out == "答案文本"
