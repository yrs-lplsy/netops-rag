"""合成 PDF 构造器（测试专用）：手工拼最小 PDF 字节，不依赖额外三方库。

支持：
- 每页若干文字行（字号/y/文本，用于字号相关的页眉脚与标题匹配测试）
- 可选图片 XObject（2x2 像素拉伸到指定 bbox，用于图片主导页跳过测试）
- 可选书签 outline（层级/标题/目标页，用于书签面包屑匹配测试）

页面对象编号：catalog=1、pages=2、每页 (page obj, content obj) 从 3 顺序分配，
其后字体、图片（如有）、outline 根与条目（如有）。
"""

import tempfile
from pathlib import Path


def _esc(s: str) -> str:
    return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def _outline_tree(outline: list[tuple[int, str, int]], item_nums: list[int],
                  outlines_root: int, page_obj_nums: list[int]) -> dict[int, dict]:
    items: dict[int, dict] = {}
    stack: list[tuple[int, int]] = []  # (level, outline idx)
    for i, (level, title, pno) in enumerate(outline):
        while stack and stack[-1][0] >= level:
            stack.pop()
        items[i] = {"parent": outlines_root if not stack else item_nums[stack[-1][1]],
                    "title": title, "dest": page_obj_nums[pno],
                    "first": None, "last": None, "count": 0, "prev": None, "next": None}
        if stack:
            p = stack[-1][1]
            items[p]["count"] += 1
            if items[p]["last"] is not None:
                items[items[p]["last"]]["next"] = i
                items[i]["prev"] = items[p]["last"]
            else:
                items[p]["first"] = i
            items[p]["last"] = i
        stack.append((level, i))
    return items


def build_pdf(page_specs: list[dict], outline: list[tuple[int, str, int]] | None = None) -> bytes:
    """page_specs: [{"lines": [(字号, y, 文本), ...], "image_bbox": (x0, y0, x1, y1) | None}]。

    image_bbox 用 PDF 坐标（原点左下）；outline 项为 (level, title, page_index)。
    """
    n = len(page_specs)
    objs: dict[int, bytes] = {}
    page_obj_nums = []
    content_obj_nums = []
    num = 3
    for _ in range(n):
        page_obj_nums.append(num)
        content_obj_nums.append(num + 1)
        num += 2
    font_num = num
    num += 1
    image_num = None
    if any(p.get("image_bbox") for p in page_specs):
        image_num = num
        num += 1
    has_outline = bool(outline)
    outlines_root = item_nums = None
    if has_outline:
        outlines_root = num
        item_nums = [outlines_root + 1 + i for i in range(len(outline))]
        num += 1 + len(outline)

    objs[font_num] = b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>"
    if image_num is not None:
        raw = bytes([255, 0, 0, 0, 255, 0, 0, 0, 255, 0, 255, 0])  # 2x2 RGB
        objs[image_num] = (f"<< /Type /XObject /Subtype /Image /Width 2 /Height 2 "
                           f"/ColorSpace /DeviceRGB /BitsPerComponent 8 /Length {len(raw)} >>\nstream\n"
                           ).encode() + raw + b"\nendstream"

    for i, spec in enumerate(page_specs):
        streams = [f"BT /F1 {size} Tf 72 {y} Td ({_esc(text)}) Tj ET"
                   for size, y, text in spec.get("lines", [])]
        res = f"<< /Font << /F1 {font_num} 0 R >>"
        if spec.get("image_bbox") and image_num is not None:
            x0, y0, x1, y1 = spec["image_bbox"]
            streams.append(f"q {x1 - x0:.0f} 0 0 {y1 - y0:.0f} {x0:.0f} {y0:.0f} cm /Im0 Do Q")
            res += f" /XObject << /Im0 {image_num} 0 R >>"
        res += " >>"
        content = "\n".join(streams).encode()
        objs[content_obj_nums[i]] = (b"<< /Length " + str(len(content)).encode()
                                     + b" >>\nstream\n" + content + b"\nendstream")
        objs[page_obj_nums[i]] = (f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
                                  f"/Contents {content_obj_nums[i]} 0 R /Resources {res} >>").encode()

    kids = " ".join(f"{x} 0 R" for x in page_obj_nums)
    objs[2] = f"<< /Type /Pages /Kids [{kids}] /Count {n} >>".encode()

    cat = f"<< /Type /Catalog /Pages 2 0 R"
    if has_outline:
        tree = _outline_tree(outline, item_nums, outlines_root, page_obj_nums)
        top = [i for i, (lv, _, _) in enumerate(outline) if lv == 0]
        objs[outlines_root] = (f"<< /Type /Outlines /First {item_nums[top[0]]} 0 R "
                               f"/Last {item_nums[top[-1]]} 0 R /Count {len(outline)} >>").encode()
        for i, it in tree.items():
            b = (f"/Title ({_esc(it['title'])}) /Parent {it['parent']} 0 R "
                 f"/Dest [{it['dest']} 0 R /XYZ null null null]")
            if it["prev"] is not None:
                b += f" /Prev {item_nums[it['prev']]} 0 R"
            if it["next"] is not None:
                b += f" /Next {item_nums[it['next']]} 0 R"
            if it["first"] is not None:
                b += f" /First {item_nums[it['first']]} 0 R /Last {item_nums[it['last']]} 0 R /Count {it['count']}"
            objs[item_nums[i]] = ("<< " + b + " >>").encode()
        cat += f" /Outlines {outlines_root} 0 R"
    objs[1] = (cat + " >>").encode()

    # xref 装配
    out = b"%PDF-1.4\n"
    offsets: dict[int, int] = {}
    for obj_num in sorted(objs):
        offsets[obj_num] = len(out)
        out += f"{obj_num} 0 obj\n".encode() + objs[obj_num] + b"\nendobj\n"
    xref_pos = len(out)
    max_num = max(objs)
    out += f"xref\n0 {max_num + 1}\n".encode() + b"0000000000 65535 f \n"
    for obj_num in range(1, max_num + 1):
        out += f"{offsets[obj_num]:010d} 00000 n \n".encode()
    out += (f"trailer\n<< /Size {max_num + 1} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF\n").encode()
    return out


def write_pdf(page_specs: list[dict], outline: list[tuple[int, str, int]] | None = None,
              directory: str | None = None) -> str:
    """构建并落盘，返回文件路径（配合 pytest tmp_path 使用）。"""
    data = build_pdf(page_specs, outline)
    f = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False, dir=directory)
    f.write(data)
    f.close()
    return f.name


def make_pdf_path(page_specs: list[dict], outline=None) -> Path:
    return Path(write_pdf(page_specs, outline))
