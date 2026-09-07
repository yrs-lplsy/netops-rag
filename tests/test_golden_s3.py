"""S3 golden set 质量门：QC 判定函数单测 + s3_full.yaml 级不变量（qid 唯一等）。

build_golden_s3.py 的 QC 逻辑在脚本内，用 importlib 加载模块直接调用（改动最小），
避免把评测脚本抽成库。
"""

import importlib.util
import sys
from collections import Counter
from pathlib import Path

from netrag.eval.golden import load_golden

REPO = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location("build_golden_s3_mod", REPO / "scripts" / "build_golden_s3.py")
_mod = importlib.util.module_from_spec(_spec)
sys.modules.setdefault("build_golden_s3_mod", _mod)
_spec.loader.exec_module(_mod)


# ---- qc_check 判定函数 ----

def test_qc_length_bounds():
    assert _mod.qc_check("短", None) == "length"
    assert _mod.qc_check("如何配置VLAN的IP地址？" * 30, None) == "length"
    assert _mod.qc_check("如何配置VLAN的IP地址？", None) is None


def test_qc_referent_and_non_question_and_stutter():
    assert _mod.qc_check("片段中如何配置VLAN的IP地址？", None) == "referent"
    assert _mod.qc_check("在本文档中如何配置VLAN的IP地址？", None) == "referent"
    assert _mod.qc_check("VLAN可以配置IP地址。", None) == "non-question"
    assert _mod.qc_check("如何配置如何配置如何配置VLAN？", None) == "stutter"


def test_qc_grounding_ascii_terms_must_hit_expected_text():
    q = "执行 display xxx-unknown-command 命令后哪个字段表示状态？"
    assert _mod.qc_check(q, "display vlan 查看VLAN信息。") .startswith("grounding")
    assert _mod.qc_check(q, "执行display xxx-unknown-command命令后，state字段表示状态。") is None


# ---- s3_full.yaml 不变量（防回归，评审 Finding 2） ----

def test_s3_full_yaml_invariants():
    items = load_golden(REPO / "data" / "golden" / "s3_full.yaml")
    assert len(items) == 200
    qids = [it.qid for it in items]
    assert len(set(qids)) == len(qids), "qid 必须全局唯一"
    assert Counter(it.qtype for it in items) == {
        "factual": 100, "troubleshoot": 40, "multihop": 30, "reject": 30}
    assert all(it.expected_chunk_ids == [] and it.expected_doc_ids == []
               for it in items if it.qtype == "reject")
    # 版本 filter 题不变量（>=15，filters 指向两个华为版本）
    ver = [it for it in items if it.filters]
    assert len(ver) >= 15
    assert {it.filters.sw_version for it in ver} == {"V600R024C10", "V600R025C00"}
    assert all(it.filters.sw_version in ("V600R024C10", "V600R025C00") for it in ver)


# ---- is_toc_chunk：TOC 目录 chunk 判别（2026-09-06 修复轮） ----

# 真实语料样例（Milvus hybrid chunks 实测，见 task-3 报告 TOC修复节）
_CISCO_BOOK = "Catalyst 9300 Security Configuration Guide, Cisco IOS XE Cupertino 17.9.x"
# book 级 Contents 页：PDF 抽取把"标题 页码"粘成无换行长串，只有面包屑可判
_TOC_BLOB_BC = f"{_CISCO_BOOK} > Contents"
_TOC_BLOB_TEXT = (
    "Password Recovery 4 Terminal Line Telnet Configuration 5 Username and Password Pairs 5 "
    "Privilege Levels 5 AES Password Encryption and Master Encryption Keys 5 "
    "How to Configure Switch Access with Passwords and Privileges 6 "
    "Setting or Changing a Static Enable Password 6 Disabling Password Recovery 9 "
    "Setting a Telnet Password for a Terminal Line 10 Configuring Username and Password Pairs 11")
# 章首 mini-TOC：面包屑是正常章节名，靠"• 标题, on page N"行主导判别
_TOC_MINI_BC = "Catalyst 9300 VLAN Configuration Guide, Cisco IOS XE Cupertino 17.9.x > Configuring Voice VLANs"
_TOC_MINI_TEXT = (
    "• Prerequisites for Voice VLANs, on page 37\n• Restrictions for Voice VLANs, on page 37\n"
    "• Information About Voice VLAN, on page 38\n• How to Configure Voice VLANs, on page 40\n"
    "• Monitoring Voice VLAN, on page 43\n• Where to Go Next, on page 43\n"
    "• Additional References, on page 44\n• Feature History Voice VLAN, on page 44")
# 干净内容：h3c 命令参考（真实语料 h3c-r1110-l2sw-cmd#c103 节选）
_CLEAN_CMD_TEXT = (
    "display mac-address 命令用来显示 MAC 地址表信息。\n【命令】\n"
    "display mac-address [ mac-address [ vlan vlan-id ] | dynamic | static | blackhole ]\n"
    "【视图】任意视图\n【参数】\n"
    "dynamic：显示动态 MAC 地址表项。static：显示静态 MAC 地址表项。\n"
    "blackhole：显示黑洞 MAC 地址表项。\n"
    "【使用指导】使用本命令可以查看静态、动态、黑洞和多端口单播 MAC 地址表项。")
# 干净内容：行尾偶有数字但不成主导（真实语料 hw-v600-case QoS 配置回显的形态）
_CLEAN_MIXED_TEXT = (
    "[DeviceB] interface 10ge 1/0/2\n[DeviceB] qos queue 5 shaping cir 3000 pir 5000 kbps\n"
    "执行以上命令后查看配置结果。\n配置端口队列整形，使语音、视频、数据业务的带宽满足规划。\n"
    "步骤4 配置端口队列整形完成后，需要保存配置并重启端口。")


def test_is_toc_chunk_real_toc_examples():
    # ① book 级 Contents（面包屑判别；正文无换行时点线行判别失效）
    assert _mod.is_toc_chunk(_TOC_BLOB_BC, _TOC_BLOB_TEXT)
    # ② 章首 mini-TOC（点线目录行主导，面包屑是正常章节名）
    assert _mod.is_toc_chunk(_TOC_MINI_BC, _TOC_MINI_TEXT)
    # 面包屑判别与正文形态无关
    assert _mod.is_toc_chunk(_TOC_BLOB_BC, "")


def test_is_toc_chunk_clean_content_not_flagged():
    assert not _mod.is_toc_chunk(
        "H3C R1110 二层技术-以太网交换命令参考 > 04-MAC地址表命令 > 1.1.1 display mac-address",
        _CLEAN_CMD_TEXT)
    # 行尾数字 <50%：混合配置回显不误杀
    assert not _mod.is_toc_chunk("S1700 V600R024C10 配置指南-QoS > 配置端口队列整形",
                                 _CLEAN_MIXED_TEXT)
    # 阈值恰在 0.5（4/8 行）不判 TOC（严格大于）
    half = "\n".join(["标题一 12", "标题二 13", "正文说明一行", "再一行说明",
                      "标题三 14", "正文继续", "更多正文", "结尾说明"])
    assert not _mod.is_toc_chunk("某手册 > 某章", half)
    # 短片段护栏：非空行 < _TOC_MIN_LINES 时不判点线主导（如真实语料 layer2-cg#c103
    # "Use Cisco Feature Navigator..." + "3 C H A P T E R" 两行尾数巧合不误杀）
    assert not _mod.is_toc_chunk(
        "Catalyst 9300 Layer 2 Configuration Guide > Configuring Loop Detection Guard "
        "> Feature History for Loop Detection Guard",
        "Use Cisco Feature Navigator to find information about platform and software "
        "image support. To access Cisco Feature Navigator, go to http://www.cisco.com/go/cfn."
        "\n\n3 C H A P T E R")
    assert not _mod.is_toc_chunk("", "")


def test_toc_reason_reports_first_bad_expected_chunk():
    chunks = {
        "d#c9": _mod.Chunk(chunk_id="d#c9", doc_id="d", text=_CLEAN_CMD_TEXT,
                           breadcrumb="手册 > 命令参考", vendor="h3c", model="",
                           sw_version="", parent_id="p1"),
        "d#c10": _mod.Chunk(chunk_id="d#c10", doc_id="d", text=_TOC_BLOB_TEXT,
                            breadcrumb=_TOC_BLOB_BC, vendor="cisco", model="",
                            sw_version="", parent_id="p2"),
    }
    good = _mod.GoldenItem(qid="q1", question="如何查看MAC地址表项？", qtype="factual",
                           expected_doc_ids=["d"], expected_chunk_ids=["d#c9"])
    bad = _mod.GoldenItem(qid="q2", question="如何配置密码？", qtype="factual",
                          expected_doc_ids=["d"], expected_chunk_ids=["d#c9", "d#c10"])
    assert _mod.toc_reason(good, chunks) is None
    assert _mod.toc_reason(bad, chunks) == "toc-chunk(c10)"
    assert _mod.toc_reason(bad, {}) is None  # chunk 不在索引中不误判


# ---- TOC 修复回归锁：11 条坏题 qid 不变，期望 chunk 不得再指向已知 TOC chunk ----

_TOC_CHUNK_IDS = {
    "cisco-c9300-17.9-security-cg#c10", "cisco-c9300-17.9-security-cg#c14",
    "cisco-c9300-17.9-security-cg#c19", "cisco-c9300-17.9-layer2-cg#c10",
    "cisco-c9300-17.9-layer2-cg#c13", "cisco-c9300-17.9-layer2-cg#c19",
    "cisco-c9300-17.9-layer2-cg#c104", "cisco-c9300-17.9-vlan-cg#c10",
    "cisco-c9300-17.9-vlan-cg#c11", "cisco-c9300-17.9-vlan-cg#c107",
    "cisco-c9300-17.9-ip-routing-cg#c352",
}


def test_s3_full_yaml_no_toc_expected_chunks():
    items = load_golden(REPO / "data" / "golden" / "s3_full.yaml")
    used = {cid for it in items for cid in it.expected_chunk_ids}
    assert not used & _TOC_CHUNK_IDS, "期望 chunk 不得为已核验的 TOC 目录 chunk"
