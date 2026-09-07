from pathlib import Path
import time

import requests
import yaml

from netrag.ingestion.html_to_md import convert_html
from netrag.ingestion.pdf_to_md import pdf_to_md

# 思科文档站有 Akamai 防护：裸 UA 会被 403，且 Akamai 还校验 TLS 指纹（JA3），
# Python requests 的 OpenSSL 指纹即使带完整浏览器头也 403（2026-09-04 实测），
# 因此优先用 curl_cffi 模拟 Chrome 指纹；未安装 curl_cffi 的环境退回 requests。
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.cisco.com/",
}

try:
    from curl_cffi import requests as _creq

    def _http_get(url: str) -> requests.Response:
        return _creq.get(url, headers=HEADERS, impersonate="chrome", timeout=60)
except ImportError:

    def _http_get(url: str) -> requests.Response:
        return requests.get(url, headers=HEADERS, timeout=60)


def load_manifest(path: Path) -> list[dict]:
    return yaml.safe_load(path.read_text())["docs"]


def _get_with_retry(url: str, retries: int = 3) -> requests.Response:
    last: Exception | None = None
    for i in range(retries):
        resp = _http_get(url)
        if resp.status_code < 400:
            return resp
        last = RuntimeError(f"HTTP {resp.status_code} for {url}")
        time.sleep(3 * (i + 1))
    raise last  # type: ignore[misc]


def fetch_all(manifest_path: Path, raw_dir: Path, processed_dir: Path) -> list[Path]:
    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    out: list[Path] = []
    for doc in load_manifest(manifest_path):
        md_path = processed_dir / f"{doc['doc_id']}.md"
        if doc.get("kind") == "pdf":
            src = Path(doc["source_path"])
            if not src.exists():
                print(f"[WARN] PDF 缺失，跳过: {doc['doc_id']} ({doc['source_path']}) — 请从厂商官网下载后重跑")
                continue
            md_path.write_text(pdf_to_md(src))
            out.append(md_path)
            print(f"converted {doc['doc_id']}: {src.name} -> {md_path.name}")
            continue
        resp = _get_with_retry(doc["source_url"])
        raw = raw_dir / f"{doc['doc_id']}.html"
        raw.write_text(resp.text)
        md_path.write_text(convert_html(resp.text))
        out.append(md_path)
        print(f"fetched {doc['doc_id']}: {len(resp.text) // 1024}KB html -> {md_path.name}")
    return out
