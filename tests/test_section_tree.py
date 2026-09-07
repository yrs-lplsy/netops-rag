from netrag.ingestion.section_tree import parse_sections

MD = """# VLAN 配置指南

前言文字。

## 创建 VLAN

使用 vlan 命令。

### vlan 命令参数

参数说明表。

## 删除 VLAN

使用 no vlan。
"""


def test_sections_and_breadcrumbs():
    secs = parse_sections(MD, doc_title="C9300 17-9 手册")
    titles = [s.title for s in secs]
    assert titles == ["VLAN 配置指南", "创建 VLAN", "vlan 命令参数", "删除 VLAN"]
    bc = {s.title: s.breadcrumb for s in secs}
    assert bc["VLAN 配置指南"] == "C9300 17-9 手册 > VLAN 配置指南"
    assert bc["创建 VLAN"] == "C9300 17-9 手册 > VLAN 配置指南 > 创建 VLAN"
    assert bc["vlan 命令参数"] == "C9300 17-9 手册 > VLAN 配置指南 > 创建 VLAN > vlan 命令参数"
    body = next(s for s in secs if s.title == "创建 VLAN")
    assert "vlan 命令" in body.body_md and "参数说明表" not in body.body_md


def test_content_before_first_heading():
    secs = parse_sections("开头散文字\n\n# A\n\n内容", doc_title="D")
    assert secs[0].title == "" and secs[0].level == 0
    assert "开头散文字" in secs[0].body_md
