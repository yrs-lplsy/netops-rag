from pathlib import Path

from netrag.eval.golden import GoldenItem, load_golden, save_golden


def test_golden_roundtrip(tmp_path: Path):
    items = [GoldenItem(qid="doc1#doc1#n3", question="如何配置？", qtype="factual",
                        expected_doc_ids=["doc1"], expected_chunk_ids=["doc1#n3"])]
    p = tmp_path / "g.yaml"
    save_golden(items, p)
    assert load_golden(p) == items
