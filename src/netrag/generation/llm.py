import httpx
from openai import OpenAI

from netrag.config import Settings


class LLMConfigError(RuntimeError):
    pass


class LLMClient:
    def __init__(self, settings: Settings | None = None, http_client: httpx.Client | None = None) -> None:
        self._settings = settings or Settings.from_env()
        if not self._settings.sf_api_key:
            raise LLMConfigError("SILICONFLOW_API_KEY 未配置，请复制 .env.example 为 .env 并填入")
        self._client = OpenAI(
            api_key=self._settings.sf_api_key,
            base_url=self._settings.sf_base_url,
            http_client=http_client,
        )

    def chat(self, messages: list[dict], temperature: float = 0.2, max_tokens: int = 2048) -> str:
        resp = self._client.chat.completions.create(
            model=self._settings.llm_model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content or ""
