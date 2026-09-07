import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tests"))

import pytest

from netrag.ingestion.pdf_to_md import (OutlineItem, _Line, _match_headings, _remerge_cjk,
                                        _strip_furniture, _table_md, convert_pdf, pages_to_blocks)
from synth_pdf import make_pdf_path


def test_heading_by_font_size_rank():
    lines = [(14.0, "第一章 VLAN 配置"), (10.0, "正文段落一"), (12.0, "1.1 创建 VLAN"), (10.0, "正文段落二")]
    blocks = pages_to_blocks(lines)
    kinds = [b.kind for b in blocks]
    assert kinds[0] == "heading"
    assert kinds[1] == "paragraph"
    assert kinds[2] == "heading"
    assert blocks[0].text == "第一章 VLAN 配置"


def test_all_same_size_all_paragraph():
    blocks = pages_to_blocks([(10.0, "a"), (10.0, "b")])
    assert all(b.kind == "paragraph" for b in blocks)


# ---------------------------------------------------- 页眉脚剔除（Fix Round 1 Finding 3）

def _line(size, text, top=100.0):
    return _Line(top=top, size=size, text=text)


def test_strip_furniture_huawei():
    lines = [_line(10.5, "S1700, S5700, S6700 系列交换机", top=20),
             _line(10.5, "配置指南-以太网交换 4 VLAN配置", top=30),
             _line(10.5, "正文第一行", top=60),
             _line(10.5, "文档版本 02 (2026-03-03) 版权所有 © 华为技术有限公司 133", top=750)]
    out = _strip_furniture(lines, "huawei", "标题")
    assert [l.text for l in out] == ["正文第一行"]


def test_strip_furniture_alarm_header():
    lines = [_line(10.5, "告警处理 27 FEI告警", top=20), _line(10.5, "正文")]
    out = _strip_furniture(lines, "huawei", "标题")
    assert [l.text for l in out] == ["正文"]  # Fix Round 1 Finding 4：告警处理卷页眉


def test_strip_furniture_cisco_size_rule():
    lines = [_line(8.0, "Configuring VTP", top=7),
             _line(8.0, "VLAN Configuration Guide, Cisco IOS XE Cupertino 17.9.x (Catalyst 9300 Switches)", top=750),
             _line(8.0, "4", top=760),
             _line(10.0, "Real body text stays here", top=300)]
    out = _strip_furniture(lines, "cisco", "VLAN Configuration Guide, Cisco IOS XE Cupertino 17.9.x")
    assert [l.text for l in out] == ["Real body text stays here"]


def test_strip_furniture_h3c_page_numbers_and_dot_leaders():
    lines = [_line(9.0, "1-11", top=750), _line(9.0, "iii", top=760),
             _line(10.5, "1.4 接口批量配置····················· 1-1", top=100),
             _line(10.5, "正文", top=200)]
    out = _strip_furniture(lines, "h3c", "H3C")
    assert [l.text for l in out] == ["正文"]


# ---------------------------------------------------- 书签标题匹配

def test_match_headings_single_and_split_pair():
    lines = [_line(12.0, "1.1", top=120), _line(12.0, "LoopBack接口简介", top=117),  # 编号/标题拆两个 y 桶（序颠倒）
             _line(10.5, "正文行")]
    heads = [OutlineItem(level=1, title="1.1 LoopBack接口简介", page=0, order=0)]
    matched, unmatched, rest = _match_headings(lines, heads)
    assert not unmatched
    assert len(matched) == 1 and matched[0][2] == "1.1 LoopBack接口简介"
    assert [l.text for l in rest] == ["正文行"]  # 两行都被消费


def test_match_headings_unmatched_counted():
    lines = [_line(10.5, "正文行")]
    heads = [OutlineItem(level=0, title="不存在的标题", page=0, order=0)]
    matched, unmatched, rest = _match_headings(lines, heads)
    assert not matched and len(unmatched) == 1
    assert [l.text for l in rest] == ["正文行"]


# ---------------------------------------------------- 表格 md

def test_table_md_basic_and_empty_filter():
    md, ncols = _table_md([["命令", "说明"], ["display this", "查看当前配置"], [None, None]])
    assert ncols == 2
    assert md.splitlines()[0] == "| 命令 | 说明 |"
    assert "---" in md.splitlines()[1]
    assert _table_md([["只有一个格子"]]) is None  # 空表/版式框


# ---------------------------------------------------- 表格单元格 CJK 空格合并（Fix Round 2）

def test_remerge_cjk_merges_split_words():
    # x_tolerance=1.5 把 (1.5,3.0]pt 的 CJK 对齐字距切成了词界 → 合并回
    assert _remerge_cjk("接口类 型") == "接口类型"
    assert _remerge_cjk("Trunk接 口") == "Trunk接口"  # 合并的是 接_口，不是 Trunk_接
    assert _remerge_cjk("判断VLAN在本接口的属 性") == "判断VLAN在本接口的属性"
    assert _remerge_cjk("先剥离帧的PVID Tag，然 后再发送") == "先剥离帧的PVID Tag，然后再发送"


def test_remerge_cjk_keeps_legal_spaces():
    # ASCII-ASCII / ASCII-CJK 边界是合法空格，不动
    assert _remerge_cjk("VLAN 20") == "VLAN 20"
    assert _remerge_cjk("Trunk 接口") == "Trunk 接口"
    assert _remerge_cjk("say 你 好") == "say 你好"  # ASCII_你 保留、你_好 合并


def test_remerge_cjk_fullwidth_punct():
    assert _remerge_cjk("配置 ，保存") == "配置，保存"
    assert _remerge_cjk("步骤 （可选） 完成") == "步骤（可选）完成"


def test_table_md_remerge_per_cell_not_across_columns():
    md, ncols = _table_md([["接口类 型", "VLAN 20"], ["Trunk接 口", "配置 ，保存"]])
    assert ncols == 2
    assert "| 接口类型 | VLAN 20 |" in md  # 各自合并
    assert "| Trunk接口 | 配置，保存 |" in md
    assert md.count(" | ") == 2  # 每行数据行 1 个分列符，原样保留，未跨列合并


# ---------------------------------------------------- convert_pdf 集成（合成 PDF）

_BODY = [(10.0, 720 - i * 14, f"Normal body line {i} the quick brown fox jumps over the lazy dog")
         for i in range(5)]


def test_convert_pdf_skips_image_dominated_page(tmp_path):
    # 页1：<50 字 + 大图（占页面 >15%）→ 整页跳过；页2：同样大图但文字多 → 保留
    p = make_pdf_path([
        {"lines": [(12.0, 700, "Hi")], "image_bbox": (50, 60, 560, 740)},
        {"lines": _BODY, "image_bbox": (50, 60, 560, 740)},
    ])
    md, st = convert_pdf(p, vendor="", doc_title="synthetic")
    assert st.pages_total == 2 and st.pages_skipped_image == 1 and st.pages_emitted == 1
    assert "Hi" not in md
    assert "Normal body line 0" in md


def test_convert_pdf_keeps_text_page_without_image_rule(tmp_path):
    p = make_pdf_path([{"lines": _BODY}])
    md, st = convert_pdf(p, vendor="", doc_title="synthetic")
    assert st.pages_skipped_image == 0
    assert "Normal body line 0" in md


def test_convert_pdf_outline_headings_matched(tmp_path):
    p = make_pdf_path(
        [{"lines": [(14.0, 700, "Chapter One"), (12.0, 660, "1.1 Target Heading"),
                    (10.0, 620, "body text under heading")]}],
        outline=[(0, "Chapter One", 0), (1, "1.1 Target Heading", 0)])
    md, st = convert_pdf(p, vendor="", doc_title="synthetic")
    assert st.headings_matched == 2 and st.headings_unmatched == 0
    assert "## Chapter One" in md  # 书签层级+2
    assert "### 1.1 Target Heading" in md
    assert "body text under heading" in md


def test_convert_pdf_escapes_config_comment_hash(tmp_path):
    # 命令注释行 "# 配置" 不得变成 markdown 标题（否则面包屑被命令串污染）
    p = make_pdf_path([{"lines": [(10.0, 700, "# configure DeviceB"), (10.0, 680, "vlan 20")]}])
    md, st = convert_pdf(p, vendor="huawei", doc_title="synthetic")
    assert "\n# configure" not in md  # 没有 h1 假标题
    assert "\\# configure DeviceB" in md
