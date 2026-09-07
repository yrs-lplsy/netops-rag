import re
from dataclasses import dataclass

_HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*$", re.MULTILINE)


@dataclass
class Section:
    title: str
    level: int
    breadcrumb: str
    body_md: str


def parse_sections(md_text: str, doc_title: str) -> list[Section]:
    marks = [(m.group(1).__len__(), m.group(2), m.start(), m.end()) for m in _HEADING.finditer(md_text)]
    sections: list[Section] = []
    title_stack: list[tuple[int, str]] = []
    if not marks or marks[0][2] > 0:
        head = md_text[: marks[0][2] if marks else len(md_text)]
        sections.append(Section(title="", level=0, breadcrumb=doc_title, body_md=head.strip()))
    for i, (level, title, _s, e) in enumerate(marks):
        nxt = marks[i + 1][2] if i + 1 < len(marks) else len(md_text)
        while title_stack and title_stack[-1][0] >= level:
            title_stack.pop()
        title_stack.append((level, title))
        breadcrumb = " > ".join([doc_title] + [t for _, t in title_stack])
        body = md_text[e:nxt].strip()
        sections.append(Section(title=title, level=level, breadcrumb=breadcrumb, body_md=body))
    return sections
