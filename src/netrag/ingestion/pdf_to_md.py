"""PDF → markdown 转换（pdfplumber 文字/表格 + 书签面包屑 + 页眉脚剔除 + 图片主导页跳过）。

设计（pdf_v1 管线，2026-09-05）：
- 文字行：extract_words(x_tolerance=1.5) 按 y 聚行。1.5 是校准值：思科 9300 PDF 默认 3.0
  会把英文单词粘连（"ConfiguringVTP"），1.5 正常分词且中文不受影响。
- 面包屑标题：PDF 书签（pypdfium2 outline，pdfplumber 自身依赖，已锁定）按 dest 页码
  调度到页面，与页面行做「去空白相等」匹配后升级为 markdown 标题（书签层级+2 级，
  h1 留给文档题名）；正文 → section_tree.parse_sections 自然组装面包屑。
- 页眉脚剔除：按厂商校准规则（华为系列名/「配置指南-」行/版权行；思科 8pt 页眉脚；
  H3C 页码「1-11」/罗马数字/目录点线）；思科页眉文字与书签同名，必须先剔除再匹配标题。
- 表格：find_tables 按框线定位，单元格转 markdown 管道表，按 bbox 把表内文字从正文行
  中扣除，表格 md 按几何位置插回正文流；跨页表格（下一页表顶在页首且列数相同）合并。
- 图片主导页跳过：剔除页眉脚后正文 < 50 字且存在占页面 ≥15% 面积的图 → 整页跳过
  （拓扑图页，文字层只有图注碎片）。
- 段落重组：前一行未以句末标点收尾且当前行非列表项 → 并段（中文手册硬换行还原）。
"""

import re
from dataclasses import dataclass, field

_X_TOL = 1.5  # 思科 PDF 词间距校准值，见模块 docstring

# 纯页码：阿拉伯 / 罗马数字 / H3C「1-11」式
_PAGE_NUM = re.compile(r"^(?:\d{1,4}|[ivxlcdm]{1,7}|\d{1,3}-\d{1,3})$", re.IGNORECASE)
# 目录点线引导符（……… / ...... / ········）
_DOT_LEADER = re.compile(r"(?:\.{6,}|…{4,}|·{6,}|．{6,})")
# 列表/编号项起始符：●•-–*、1. / 1、 / (1) / （1） / a. 等
_BULLET = re.compile(r"^(?:[●•‣◦·*\-\u2013\u2014]|\d{1,3}\s*[.、）)]|[（(]\d{1,3}[)）]|[a-zA-Z]\s*[.、])\s*")
_SENT_END = tuple("。！？；：.?!:」』）)】»\"'")
_HW_SERIES_LINE = "S1700, S5700, S6700 系列交换机"


@dataclass
class Block:
    kind: str  # heading | paragraph
    text: str


@dataclass
class PdfConvertStats:
    pages_total: int = 0
    pages_emitted: int = 0
    pages_skipped_image: int = 0
    pages_skipped_empty: int = 0
    headings_matched: int = 0
    headings_unmatched: int = 0
    tables: int = 0
    chars: int = 0

    def summary(self) -> str:
        return (f"pages {self.pages_emitted}/{self.pages_total} "
                f"(img-skip {self.pages_skipped_image}, empty {self.pages_skipped_empty}), "
                f"headings {self.headings_matched}+{self.headings_unmatched}unmatched, "
                f"tables {self.tables}, chars {self.chars}")


def pages_to_blocks(lines: list[tuple[float, str]]) -> list[Block]:
    """旧接口（按字号排名判标题），保留给既有调用方/测试。"""
    sizes = sorted({s for s, _ in lines}, reverse=True)
    heading_sizes = set(sizes[:2]) if len(sizes) >= 2 else set()
    blocks: list[Block] = []
    for size, text in lines:
        text = text.strip()
        if not text:
            continue
        blocks.append(Block(kind="heading" if size in heading_sizes else "paragraph", text=text))
    return blocks


# ---------------------------------------------------------------- 书签 outline

@dataclass
class OutlineItem:
    level: int
    title: str
    page: int
    order: int  # 全书顺序，同级去重/排序用


def read_outline(pdf_path) -> list[OutlineItem]:
    """读 PDF 书签 → (层级, 标题, 目标页)。无书签返回空表（回退到纯正文流）。"""
    import pypdfium2 as pdfium

    items: list[OutlineItem] = []
    try:
        with pdfium.PdfDocument(str(pdf_path)) as pdf:
            for bm in pdf.get_toc():
                dest = bm.get_dest()
                page = dest.get_index() if dest else None
                title = (bm.get_title() or "").strip()
                if page is None or not title:
                    continue
                items.append(OutlineItem(level=bm.level, title=title, page=int(page), order=len(items)))
    except Exception as e:  # noqa: BLE001 - 损坏 outline 不阻断摄取
        print(f"[WARN] outline 读取失败 {pdf_path}: {e}")
    return items


# ---------------------------------------------------------------- 页面行/表格

@dataclass
class _Line:
    top: float
    size: float
    text: str


@dataclass
class _TableBlk:
    top: float
    md: str
    ncols: int
    rows: list[list[str]]


def _norm(text: str) -> str:
    return re.sub(r"\s+", "", text)


# 仅表格单元格后处理（Fix Round 2）：x_tolerance=1.5 只会切分不会合并——单元格内
# (1.5, 3.0]pt 的 CJK 对齐字距被当词界，产生 "接口类 型"/"Trunk接 口"/"属 性" 碎片。
# 只合并 CJK-CJK 与 CJK-全角标点 边界的单空格；ASCII-ASCII / ASCII-CJK 边界
# （"VLAN 20"、"Trunk 接口"）是合法空格，不动。OID 数字碎片（"…205. 1.2"）不在
# 此处理（deferred，见报告 §11）。正文路径不调用（1.5 分词是原本行为，不回归）。
_CJK = "\u4e00-\u9fff\u3400-\u4dbf"
_CJK_PUNCT = "，。、；：！？""''（）《》【】…—·"
_CJK_SPACE_CJK = re.compile(rf"(?<=[{_CJK}]) (?=[{_CJK}])")
_CJK_SPACE_PUNCT = re.compile(rf"(?<=[{_CJK}]) (?=[{_CJK_PUNCT}])")
_PUNCT_SPACE_CJK = re.compile(rf"(?<=[{_CJK_PUNCT}]) (?=[{_CJK}])")


def _remerge_cjk(cell: str) -> str:
    cell = _CJK_SPACE_CJK.sub("", cell)
    cell = _CJK_SPACE_PUNCT.sub("", cell)
    cell = _PUNCT_SPACE_CJK.sub("", cell)
    return cell


def _cell(c) -> str:
    return _remerge_cjk("" if c is None else str(c).replace("\n", " ").strip())


def _table_md(rows: list[list[str]]) -> tuple[str, int] | None:
    rows = [[_cell(c) for c in r] for r in rows if any(_cell(c) for c in r)]
    if len(rows) < 2 or sum(len(r) for r in rows) < 4:
        return None  # 空表/版式框，非数据表
    ncols = max(len(r) for r in rows)
    rows = [r + [""] * (ncols - len(r)) for r in rows]
    md = "| " + " | ".join(rows[0]) + " |\n"
    md += "|" + "---|" * ncols + "\n"
    md += "\n".join("| " + " | ".join(r) + " |" for r in rows[1:])
    return md, ncols


def _page_lines(page) -> tuple[list[_Line], list[_TableBlk], float]:
    """一页 → (正文行, 表格块, 最大图片面积占比)。表内文字已从正文行扣除。"""
    tables: list[_TableBlk] = []
    boxes: list[tuple[float, float, float, float]] = []  # 与 tables 一一对应
    page_area = float(page.width) * float(page.height) or 1.0
    try:
        for t in page.find_tables():
            bbox_area = (t.bbox[2] - t.bbox[0]) * (t.bbox[3] - t.bbox[1])
            if bbox_area > 0.85 * page_area:
                continue  # 页面边框误检为整页表，跳过以免吞掉全部正文
            # extract 的 x_tolerance 必须与正文一致：默认 3.0 会把英文单元格粘成
            # "CommandorAction"/"configureterminal"（评审 Fix Round 1 发现）
            made = _table_md(t.extract(x_tolerance=_X_TOL) or [])
            if made:
                md, ncols = made
                tables.append(_TableBlk(top=t.bbox[1], md=md, ncols=ncols, rows=[]))
                boxes.append(t.bbox)
    except Exception:  # noqa: BLE001 - 个别页表格定位崩溃不阻断
        tables = []

    def in_table(w) -> bool:
        return any(b[0] - 1 <= w["x0"] and w["x1"] <= b[2] + 1
                   and b[1] - 2 <= w["top"] and w["bottom"] <= b[3] + 2
                   for b in boxes)

    words = [w for w in page.extract_words(extra_attrs=["size"], x_tolerance=_X_TOL)
             if not in_table(w)]
    # 仅按 y 聚行（页脚混排字号整行归并后才能命中剔除规则），行字号取行内最大
    rows_y: dict[int, list[dict]] = {}
    for w in words:
        rows_y.setdefault(int(w["top"] // 3), []).append(w)
    lines = [_Line(top=k * 3.0, size=max(w["size"] for w in ws),
                   text=" ".join(w["text"] for w in sorted(ws, key=lambda w: w["x0"])))
             for k, ws in sorted(rows_y.items())]

    img_ratio = 0.0
    for im in page.images:
        r = (im["x1"] - im["x0"]) * (im["bottom"] - im["top"]) / page_area
        img_ratio = max(img_ratio, r)
    return lines, tables, img_ratio


def _strip_furniture(lines: list[_Line], vendor: str, doc_title: str) -> list[_Line]:
    """剔除页眉/页脚。规则按厂商校准（见模块 docstring），通用规则兜底。"""
    out = lines[:]
    title_norm = _norm(doc_title) if doc_title else None

    def is_page_num(l: _Line) -> bool:
        return l.size <= 10 and bool(_PAGE_NUM.match(l.text.strip()))

    if vendor == "cisco":
        # 思科：页眉（章节名/书名）与页脚（书名+页码）均为 8pt，正文 10pt
        out = [l for i, l in enumerate(out)
               if not (l.size <= 9 and (i < 2 or i >= len(out) - 3))]
        out = [l for l in out if not (title_norm and _norm(l.text) == title_norm)]
    else:
        # 华为/H3C：页眉含系列名/「配置指南-」，页脚含版权行/纯页码；目录点线行
        kept: list[_Line] = []
        for l in out:
            t = l.text.strip()
            if t == _HW_SERIES_LINE:
                continue
            if t.startswith(("配置指南-", "命令参考", "典型配置", "告警处理")) and l.size <= 10.5 and len(t) < 60:
                continue
            if "版权所有" in t or "文档版本" in t:
                continue
            if _DOT_LEADER.search(t):
                continue
            if is_page_num(l):
                continue
            kept.append(l)
        out = kept
    return out


# ---------------------------------------------------------------- 标题匹配

def _match_headings(lines: list[_Line], heads: list[OutlineItem]) -> \
        tuple[list[tuple[float, int, str]], list[tuple[float, int, str]], list[_Line]]:
    """把本页书签标题匹配到行。返回 (匹配到的 (top, level, title), 未匹配的同元组, 剩余行)。

    先做单行「去空白相等」，再做相邻两行拼接匹配（长标题跨行换行）；
    未匹配的标题插到页首（多数是章封面页，正文尚未开始，插页首位置正确）。
    """
    remain = lines[:]
    matched: list[tuple[float, int, str]] = []
    unmatched: list[tuple[float, int, str]] = []
    used = [False] * len(remain)
    for h in heads:
        want = _norm(h.title)
        if not want:
            continue
        hit = next((i for i, l in enumerate(remain) if not used[i] and _norm(l.text) == want), None)
        if hit is None and len(want) >= 8:
            # 相邻两行拼接匹配（长标题跨行/编号与标题字号微差被拆成两个 y 桶，两种拼接序都试）
            hit = next((i for i in range(len(remain) - 1)
                        if not used[i] and not used[i + 1]
                        and want in (_norm(remain[i].text) + _norm(remain[i + 1].text),
                                     _norm(remain[i + 1].text) + _norm(remain[i].text))), None)
            if hit is not None:
                used[hit] = used[hit + 1] = True
                matched.append((min(remain[hit].top, remain[hit + 1].top), h.level, h.title))
                continue
        if hit is not None:
            used[hit] = True
            matched.append((remain[hit].top, h.level, h.title))
        else:
            unmatched.append((-1.0, h.level, h.title))
    rest = [l for i, l in enumerate(remain) if not used[i]]
    return matched, unmatched, rest


# ---------------------------------------------------------------- 段落重组

def _is_bullet(text: str) -> bool:
    return bool(_BULLET.match(text.strip()))


def _merge_paragraph(fragments: list[str]) -> str:
    """硬换行还原：前一行不以句末标点结尾且当前行不是列表项 → 空格拼接（西文）/直接拼接。"""
    out = ""
    for frag in fragments:
        frag = frag.strip()
        if not frag:
            continue
        if not out:
            out = frag
        elif out[-1] in _SENT_END or _is_bullet(frag) or _is_bullet(out):
            out += "\n" + frag
        elif out[-1].isascii() and frag[0].isascii():
            out += " " + frag
        else:
            out += frag
    return out


# ---------------------------------------------------------------- 主转换

def convert_pdf(pdf_path, vendor: str = "", doc_title: str = "",
                min_text_chars: int = 50, image_area_ratio: float = 0.15) -> tuple[str, PdfConvertStats]:
    """PDF → (markdown, 统计)。markdown 首行为 `# doc_title`（缺省用文件名）。"""
    import pdfplumber

    outline = read_outline(pdf_path)
    by_page: dict[int, list[OutlineItem]] = {}
    for it in outline:
        by_page.setdefault(it.page, []).append(it)

    stats = PdfConvertStats()
    out_parts: list[str] = []
    last_block_ncols: int | None = None  # 跨页表合并：上一个表格的列数

    with pdfplumber.open(pdf_path) as pdf:
        stats.pages_total = len(pdf.pages)
        for pno, page in enumerate(pdf.pages):
            lines, tables, img_ratio = _page_lines(page)
            lines = _strip_furniture(lines, vendor, doc_title)
            text_chars = sum(len(l.text) for l in lines) + sum(len(t.md) for t in tables)
            heads = by_page.get(pno, [])

            if text_chars < min_text_chars and img_ratio >= image_area_ratio:
                stats.pages_skipped_image += 1
                stats.headings_unmatched += len(heads)
                continue  # 图片主导页（拓扑图）：整页跳过
            if not lines and not tables:
                stats.pages_skipped_empty += 1
                stats.headings_unmatched += len(heads)
                continue

            matched, unmatched, rest = _match_headings(lines, heads)
            stats.headings_matched += len(matched)
            stats.headings_unmatched += len(unmatched)

            # 页面内容流：行/表格/标题按几何位置归并（未匹配标题 top=-1 → 页首）
            flow: list[tuple[float, int, object]] = ([(l.top, 0, l) for l in rest]
                                                     + [(t.top, 1, t) for t in tables]
                                                     + [(m[0], -1, m) for m in matched + unmatched])
            flow.sort(key=lambda x: (x[0], x[1]))

            para: list[str] = []

            def flush_para() -> None:
                nonlocal para
                if para:
                    merged = _merge_paragraph(para)
                    if merged:
                        out_parts.append(merged)
                    para = []

            for top, kind, obj in flow:
                if kind == -1:  # 书签标题
                    depth = max(2, min(6, obj[1] + 2))
                    flush_para()
                    out_parts.append(f"{'#' * depth} {obj[2]}")
                    last_block_ncols = None
                elif kind == 1:  # 表格
                    flush_para()
                    md_lines = obj.md.split("\n")
                    body_rows = md_lines[2:] if len(md_lines) > 2 else []
                    if top < 30 and last_block_ncols == obj.ncols:
                        # 跨页表：本页表顶在页首且上一块是同列数表格 → 行合并
                        out_parts[-1] += "\n" + "\n".join(body_rows)
                    else:
                        out_parts.append(obj.md)
                    last_block_ncols = obj.ncols
                    stats.tables += 1
                else:  # 正文行
                    last_block_ncols = None
                    t = obj.text
                    # 命令注释行「# xxx」转义，避免被 section_tree 当成 markdown 标题
                    para.append("\\" + t if t.startswith("#") else t)
            flush_para()
            stats.pages_emitted += 1

    title = doc_title or str(pdf_path).split("/")[-1]
    stats.chars = sum(len(p) for p in out_parts)
    md = f"# {title}\n\n" + "\n\n".join(out_parts) + "\n"
    return md, stats


def pdf_to_md(pdf_path) -> str:
    """旧接口：仅返回 markdown 文本（fetcher.py 兼容）。"""
    md, _ = convert_pdf(pdf_path)
    return md
