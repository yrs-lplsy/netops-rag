import pytest

from netrag.index.milvus_client import get_milvus, wait_healthy

pytestmark = pytest.mark.milvus


def test_get_milvus_and_healthy():
    client = get_milvus()
    wait_healthy(client, timeout_s=90)
    assert client.get_server_version().startswith("2.5")
