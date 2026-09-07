import time

from pymilvus import MilvusClient

from netrag.config import Settings


def get_milvus(uri: str | None = None) -> MilvusClient:
    uri = uri or Settings.from_env().milvus_uri
    return MilvusClient(uri=uri)


def wait_healthy(client: MilvusClient, timeout_s: int = 60) -> None:
    deadline = time.time() + timeout_s
    last_err: Exception | None = None
    while time.time() < deadline:
        try:
            client.get_server_version()
            return
        except Exception as e:  # noqa: BLE001 - 启动期任何错误都重试
            last_err = e
            time.sleep(3)
    raise TimeoutError(f"milvus not healthy in {timeout_s}s: {last_err}")
