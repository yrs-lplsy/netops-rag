from dataclasses import asdict, dataclass, field
from pathlib import Path

import yaml

from netrag.retrieval.base import MetadataFilter


@dataclass
class GoldenItem:
    qid: str
    question: str
    qtype: str
    expected_doc_ids: list[str]
    expected_chunk_ids: list[str]
    filters: MetadataFilter | None = None


def save_golden(items: list[GoldenItem], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = []
    for it in items:
        d = asdict(it)
        d["filters"] = (asdict(it.filters) if it.filters else None)
        data.append(d)
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))


def load_golden(path: Path) -> list[GoldenItem]:
    items = []
    for d in yaml.safe_load(path.read_text()):
        f = d.get("filters")
        items.append(GoldenItem(
            qid=d["qid"], question=d["question"], qtype=d["qtype"],
            expected_doc_ids=d["expected_doc_ids"], expected_chunk_ids=d["expected_chunk_ids"],
            filters=MetadataFilter(**f) if f else None,
        ))
    return items
