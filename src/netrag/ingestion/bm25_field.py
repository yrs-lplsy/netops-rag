import re

_INTERFACE = re.compile(r"\b(?:[A-Za-z]{2,}(?:\d+/\d+/\d+))\b")
_VERSION = re.compile(r"\b(?:V\d{2,4}R\d{3}[A-Z]?|\d{1,2}-\d{1,2}-\d{1,2}|VRP)\b", re.IGNORECASE)
_ERRCODE = re.compile(r"%[A-Za-z0-9_-]{4,}")
_CLI_LINE = re.compile(r"^\s*(?:Device|Switch|Router|huawei|H3C)?\s*\(?\S*\)?#\s*(.+)$|^\s*(?:display|show|vlan|ospf|interface|stp|port|undo|no)\s+.+$",
                       re.MULTILINE | re.IGNORECASE)
_SPLIT = re.compile(r"[^0-9a-zA-Z\u4e00-\u9fff]+")
_PROMPT_PREFIX = re.compile(r"^(?:Device|Switch|Router)?\s*\(?\S*\)?#\s*")
_SENTENCE_ENDINGS = (".", "。", ";", "，", "、")
_PROSE_MARKERS = (" is ", " are ", "的", " the ")
_MAX_CMD_WORDS = 8


def _is_command_like(cmd: str, full_line: str) -> bool:
    """过滤散文句与 # 注释，仅保留命令型行。"""
    if full_line.lstrip().startswith("#"):  # 井号注释行
        return False
    if cmd.endswith(_SENTENCE_ENDINGS):  # 句末标点 → 散文
        return False
    padded = f" {cmd.lower()} "
    if any(marker in padded for marker in _PROSE_MARKERS):  # 散文标记
        return False
    if len(cmd.split()) > _MAX_CMD_WORDS:  # 命令不会太长
        return False
    return True


def extract_exact_terms(text: str) -> list[str]:
    terms: list[str] = []
    for m in _INTERFACE.finditer(text):
        terms.append(m.group(0))
    for m in _VERSION.finditer(text):
        terms.append(m.group(0))
    for m in _ERRCODE.finditer(text):
        terms.append(m.group(0))
    for m in _CLI_LINE.finditer(text):
        full_line = m.group(0).strip()
        cmd = (m.group(1) or full_line).strip()
        cmd = _PROMPT_PREFIX.sub("", cmd)
        if cmd and _is_command_like(cmd, full_line):
            terms.append(cmd)
    return terms


def build_bm25_text(chunk_text: str, breadcrumb: str) -> str:
    exact = extract_exact_terms(chunk_text)
    base = _SPLIT.sub(" ", f"{breadcrumb} {chunk_text}").lower().strip()
    exact_norm: list[str] = []
    for t in exact:
        exact_norm.extend(_SPLIT.sub(" ", t.lower()).split())
    seen: dict[str, int] = {}
    for w in exact_norm:
        if w:
            seen[w] = 3
    tokens = base.split() + [w for w, n in seen.items() for _ in range(n)]
    out = " ".join(tokens)
    return out[:12000]
