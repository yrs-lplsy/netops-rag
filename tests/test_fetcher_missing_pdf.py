import yaml

from netrag.ingestion.fetcher import fetch_all


def test_missing_pdf_skips_with_warning_no_crash(tmp_path, capsys):
    """纯 pdf 清单且 PDF 不存在：fetch_all 应跳过并告警，而不是抛 FileNotFoundError。

    清单只含 pdf 条目，因此整个流程不触网（html 分支才会走 requests）。
    """
    manifest = {
        "docs": [
            {
                "doc_id": "fake-vendor-doc",
                "vendor": "fake",
                "model": "fake",
                "sw_version": "1.0",
                "title": "不存在的 PDF",
                "kind": "pdf",
                "source_path": str(tmp_path / "not_downloaded.pdf"),
            }
        ]
    }
    manifest_path = tmp_path / "manifest.yaml"
    manifest_path.write_text(yaml.safe_dump(manifest, allow_unicode=True), encoding="utf-8")

    out = fetch_all(manifest_path, tmp_path / "raw", tmp_path / "processed")

    assert out == []  # 缺失 PDF 被跳过：不产出文件、不进入返回列表
    assert not (tmp_path / "processed" / "fake-vendor-doc.md").exists()
    stdout = capsys.readouterr().out
    assert "[WARN]" in stdout
    assert "PDF 缺失" in stdout
    assert "fake-vendor-doc" in stdout
