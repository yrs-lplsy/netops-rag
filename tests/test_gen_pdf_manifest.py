"""gen_pdf_manifest.py 白名单规则纯函数单测（评审 Fix Round 1 Finding 3）。

scripts/ 非包模块，用 importlib 从路径加载。
"""

import importlib.util
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[1]
_SPEC = importlib.util.spec_from_file_location(
    "gen_pdf_manifest", _REPO / "scripts" / "gen_pdf_manifest.py")
gen = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(gen)


def test_strip_pdf_suffix():
    # 目录名带 "(pdf)"、整本文件名不带——剥离后才能比对（v1 漏排除的根因）
    assert gen.strip_pdf_suffix("S1700, S5700, S6700 V600R025C00 配置指南-以太网交换(pdf)") == \
        "S1700, S5700, S6700 V600R025C00 配置指南-以太网交换"
    assert gen.strip_pdf_suffix("S1700, S5700, S6700 V600R025C00 配置指南-以太网交换") == \
        "S1700, S5700, S6700 V600R025C00 配置指南-以太网交换"
    assert gen.strip_pdf_suffix("  abc ") == "abc"


def test_parse_hw_stem():
    assert gen.parse_hw_stem("01-04 VLAN配置") == ("01-04", "VLAN配置")
    assert gen.parse_hw_stem("01-100 VFS告警") == ("01-100", "VFS告警")
    assert gen.parse_hw_stem("扉页") == ("扉页", "扉页")  # 无数字前缀兜底


def test_hw_doc_entry_doc_id_contains_version_and_unique():
    a = gen.hw_doc_entry("vol", "V600R025C00", "eth-switch", "配置指南-以太网交换", "01-04 VLAN配置")
    b = gen.hw_doc_entry("vol", "V600R024C10", "eth-switch", "配置指南-以太网交换", "01-04 VLAN配置")
    assert a["doc_id"] == "hw-v600r025c00-eth-switch-01-04"
    assert b["doc_id"] == "hw-v600r024c10-eth-switch-01-04"  # 版本在 doc_id 里，跨版本不冲突
    assert a["doc_id"] != b["doc_id"]
    assert a["title"] == "vol 01-04 VLAN配置"
    assert a["kind"] == "pdf"


def test_cisco_match_book_whitelist():
    assert gen.cisco_match_book("VLAN Configuration Guide Cisco IOS XE Cupertino 17.9.x (Catalyst 9300).pdf") \
        == ("vlan-cg", "VLAN Configuration Guide")
    assert gen.cisco_match_book("Security Configuration Guide, Cisco IOS XE Cupertino 17.9.x (Catalyst 9300 Switches).pdf")[0] \
        == "security-cg"
    assert gen.cisco_match_book("BGP EVPN VXLAN Configuration Guide, Cisco IOS XE Cupertino 17.9.x.pdf") is None


def test_h3c_parse_name_whitelist():
    assert gen.h3c_parse_name("03-二层技术-以太网交换配置指导-整本手册.pdf", "配置指导") == \
        ("l2sw", "二层技术-以太网交换")
    assert gen.h3c_parse_name("05-三层技术-IP路由命令参考-整本手册.pdf", "命令参考") == \
        ("iproute", "三层技术-IP路由")
    assert gen.h3c_parse_name("06-IP组播配置指导-整本手册.pdf", "配置指导") is None  # 非白名单主题
    assert gen.h3c_parse_name("01-基础配置指导-整本手册.pdf", "配置指导") is None


def test_hw_volume_docs_excludes_whole_book(tmp_path):
    vol = tmp_path / "S1700, S5700, S6700 V600R025C00 配置指南-以太网交换(pdf)"
    vol.mkdir()
    (vol / "S1700, S5700, S6700 V600R025C00 配置指南-以太网交换.pdf").write_bytes(b"whole")  # 整本合集
    (vol / "01-04 VLAN配置.pdf").write_bytes(b"c1")
    docs = gen.hw_volume_docs(vol, "V600R025C00", "以太网交换", "eth-switch")
    assert [d["doc_id"] for d in docs] == ["hw-v600r025c00-eth-switch-01-04"]  # 整本被排除
