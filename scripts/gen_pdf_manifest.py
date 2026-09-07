"""从 data/pdf/ 目录扫描 + 白名单规则生成 data/manifests/pdf_v1.yaml。

v1 白名单（任务书规定，其余文件留在池子不入库）：
- Huawei V600R025C00：配置指南-以太网交换 / IP路由 / 安全 / 接口管理 四卷全部章节 PDF
  + 告警处理 + 典型配置案例集（案例集在 S1700, S5700, S6700（V600版本）(pdf)/ 下）
- Huawei V600R024C10：配置指南-以太网交换 / IP路由 / 安全 三卷
- Cisco IOS XE 17.9（Catalyst 9300）：VLAN / Layer 2 / IP Routing / Security 四本
- H3C R1110：二层技术-以太网交换 / 三层技术-IP路由 / 安全 三个主题的 配置指导+命令参考 分册

排除规则：
- 各华为卷目录下与目录同名的整本手册 PDF（内容 = 全部章节之和，避免重复入库）
- 非 PDF 文件

doc_id 规则（全局唯一且含版本信息）：
- huawei: hw-{sw_version小写}-{卷代码}-{文件名序号}，如 hw-v600r025c00-eth-switch-01-04
- cisco : cisco-c9300-{版本}-{书代码}，如 cisco-c9300-17.9-vlan-cg
- h3c   : h3c-{型号}-{主题代码}-{cfg|cmd}，如 h3c-r1110-l2sw-cfg

用法：uv run python scripts/gen_pdf_manifest.py
"""

import re
import sys
from datetime import date
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parents[1]
PDF_ROOT = REPO / "data" / "pdf"
OUT = REPO / "data" / "manifests" / "pdf_v1.yaml"

HW_SERIES = "S1700, S5700, S6700"
HW_DIR_25 = f"{HW_SERIES} V600R025C00"
HW_DIR_24 = f"{HW_SERIES} V600R024C00".replace("C00", "C10")  # 目录名实为 V600R024C10
HW_DIR_V600 = f"{HW_SERIES}（V600版本）(pdf)"

# 华为卷目录名 -> (卷代码, 卷中文名)
HW_VOLUMES = {
    "以太网交换": ("eth-switch", "以太网交换"),
    "IP路由": ("ip-route", "IP路由"),
    "安全": ("security", "安全"),
    "接口管理": ("interface", "接口管理"),
    "告警处理": ("alarm", "告警处理"),
}
NUM_PREFIX = re.compile(r"^(\d{2}-\d{1,3})\s+(.+)$")

CISCO_BOOKS = {  # 文件名前缀 -> (书代码, 中文题名)
    "VLAN Configuration Guide": ("vlan-cg", "VLAN Configuration Guide"),
    "Layer 2 Configuration Guide": ("layer2-cg", "Layer 2 Configuration Guide"),
    "IP Routing Configuration Guide": ("ip-routing-cg", "IP Routing Configuration Guide"),
    "Security Configuration Guide": ("security-cg", "Security Configuration Guide"),
}

H3C_TOPICS = {  # 分册序号前缀 -> (主题代码, 中文题名)
    "03": ("l2sw", "二层技术-以太网交换"),
    "05": ("iproute", "三层技术-IP路由"),
    "09": ("security", "安全"),
}

# 供单测的纯函数：目录/文件名 (pdf) 后缀剥离、文件名解析与 manifest 条目构造
_HW_VOL = "配置指南"


def strip_pdf_suffix(name: str) -> str:
    """剥离目录/文件名结尾的 "(pdf)" 后缀并去尾空白。

    华为卷目录名带 "(pdf)"（如 "…以太网交换(pdf)"）而整本 PDF 文件名不带
    （"…以太网交换.pdf"），整本合集排除必须先剥离再比对（Fix Round 1 评审回归点）。
    """
    return name[:-len("(pdf)")].strip() if name.endswith("(pdf)") else name.strip()


def parse_hw_stem(stem: str) -> tuple[str, str]:
    """章节文件名 -> (序号, 章节题名)。无数字前缀时序号取文件名去空白。"""
    m = NUM_PREFIX.match(stem)
    if m:
        return m.group(1).replace(" ", ""), m.group(2).strip()
    return re.sub(r"\s+", "-", stem), stem.strip()


def hw_doc_entry(vol_base: str, sw_version: str, vol_code: str, volume: str,
                 stem: str) -> dict:
    """一个章节 PDF 的 manifest 条目（doc_id 含版本，卷内以序号唯一）。"""
    seq, chapter = parse_hw_stem(stem)
    return {
        "doc_id": f"hw-{sw_version.lower()}-{vol_code}-{seq}",
        "vendor": "huawei",
        "model": HW_SERIES,
        "sw_version": sw_version,
        "volume": volume,
        "title": f"{vol_base} {seq} {chapter}",
        "kind": "pdf",
    }


def h3c_parse_name(name: str, kind_cn: str) -> tuple[str, str] | None:
    """H3C 分册文件名 -> (主题代码, 中文题名)；非白名单主题返回 None。"""
    m = re.match(r"^(\d{2})-(.+?)" + kind_cn + r"-整本手册\.pdf$", name)
    if not m or m.group(1) not in H3C_TOPICS:
        return None
    return H3C_TOPICS[m.group(1)]


def cisco_match_book(name: str) -> tuple[str, str] | None:
    """思科书文件名 -> (书代码, 中文题名)；不在 v1 白名单返回 None。"""
    for prefix, code_cn in CISCO_BOOKS.items():
        if name.startswith(prefix):
            return code_cn
    return None


def hw_volume_docs(vol_dir: Path, sw_version: str, volume_cn: str, vol_code: str) -> list[dict]:
    docs = []
    # 整本手册文件名无 "(pdf)" 后缀而目录名有（如 目录"…以太网交换(pdf)" vs
    # 文件"…以太网交换.pdf"），必须剥掉后缀再比对，否则整本合集漏排除（v1 修过的 bug）
    vol_base = strip_pdf_suffix(vol_dir.name)
    whole_book = vol_base + ".pdf"
    volume = f"配置指南-{volume_cn}" if vol_code != "alarm" else "告警处理"
    for f in sorted(vol_dir.glob("*.pdf")):
        if f.name == whole_book:
            continue
        entry = hw_doc_entry(vol_base, sw_version, vol_code, volume, f.stem)
        # source_path 相对 repo 根；卷目录在 repo 外（单测 tmp_path）时退回绝对路径
        entry["source_path"] = str(f.relative_to(REPO)) if f.is_relative_to(REPO) else str(f)
        docs.append(entry)
    return docs


def main() -> None:
    docs: list[dict] = []
    skipped_pool = 0

    # --- Huawei V600R025C00：四卷 + 告警处理 ---
    root25 = PDF_ROOT / "Huawei" / HW_DIR_25
    for d in sorted(root25.iterdir()):
        if not d.is_dir():
            continue
        name = d.name
        if name.endswith("(pdf)"):
            name = name[:-len("(pdf)")].strip()
        if "告警处理" in name:
            docs += hw_volume_docs(d, "V600R025C00", "告警处理", "alarm")
        elif any(f"配置指南-{v}" in name for v in ("以太网交换", "IP路由", "安全", "接口管理")):
            cn = next(v for v in ("以太网交换", "IP路由", "安全", "接口管理") if f"配置指南-{v}" in name)
            code, _ = HW_VOLUMES[cn]
            docs += hw_volume_docs(d, "V600R025C00", cn, code)
        else:
            skipped_pool += len(list(d.glob("*.pdf")))

    # --- Huawei 典型配置案例集（V600版本）---
    case_root = PDF_ROOT / "Huawei" / HW_DIR_V600 / f"{HW_SERIES}系列交换机 典型配置案例集（V600版本）(pdf)"
    if case_root.exists():
        case_base = strip_pdf_suffix(case_root.name)  # 整本合集文件名无 "(pdf)" 后缀
        for f in sorted(case_root.glob("*.pdf")):
            if f.name == case_base + ".pdf":
                continue  # 整本合集排除
            entry = hw_doc_entry(case_base, "V600", "case", "典型配置案例集", f.stem)
            entry["doc_id"] = f"hw-v600-case-{parse_hw_stem(f.stem)[0]}"
            entry["source_path"] = str(f.relative_to(REPO))
            docs.append(entry)

    # --- Huawei V600R024C10：三卷 ---
    root24 = PDF_ROOT / "Huawei" / HW_DIR_24
    for d in sorted(root24.iterdir()):
        if not d.is_dir():
            continue
        name = d.name[:-len("(pdf)")].strip() if d.name.endswith("(pdf)") else d.name
        if any(f"配置指南-{v}" in name for v in ("以太网交换", "IP路由", "安全")):
            cn = next(v for v in ("以太网交换", "IP路由", "安全") if f"配置指南-{v}" in name)
            code, _ = HW_VOLUMES[cn]
            docs += hw_volume_docs(d, "V600R024C10", cn, code)
        else:
            skipped_pool += len(list(d.glob("*.pdf")))

    # --- Cisco 17.9 四本 ---
    cisco_dir = PDF_ROOT / "Cisco" / "Catalyst 9300"
    for f in sorted(cisco_dir.glob("*.pdf")):
        hit = cisco_match_book(f.name)
        if not hit:
            skipped_pool += 1
            continue
        code, cn = hit
        docs.append({
            "doc_id": f"cisco-c9300-17.9-{code}",
            "vendor": "cisco",
            "model": "Catalyst 9300",
            "sw_version": "17.9",
            "volume": cn,
            "title": f"Catalyst 9300 {cn}, Cisco IOS XE Cupertino 17.9.x",
            "kind": "pdf",
            "source_path": str(f.relative_to(REPO)),
        })

    # --- H3C R1110 三主题 配置指导 + 命令参考 ---
    for sub, kind, kind_cn in [("配置指导", "cfg", "配置指导"), ("命令参考", "cmd", "命令参考")]:
        h3c_dir = PDF_ROOT / "H3C" / "R1110" / sub
        for f in sorted(h3c_dir.glob("*.pdf")):
            hit = h3c_parse_name(f.name, kind_cn)
            if not hit:
                skipped_pool += 1
                continue
            code, topic_cn = hit
            docs.append({
                "doc_id": f"h3c-r1110-{code}-{kind}",
                "vendor": "h3c",
                "model": "R1110",
                "sw_version": "R1110",
                "volume": f"{topic_cn}{kind_cn}",
                "title": f"H3C R1110 {topic_cn}{kind_cn}",
                "kind": "pdf",
                "source_path": str(f.relative_to(REPO)),
            })

    # doc_id 全局唯一性断言
    ids = [d["doc_id"] for d in docs]
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        sys.exit(f"doc_id 重复: {dup}")
    for d in docs:
        assert (REPO / d["source_path"]).exists(), d["source_path"]

    OUT.parent.mkdir(parents=True, exist_ok=True)
    header = (
        f"# pdf_v1 语料白名单：v1 入库范围见 scripts/gen_pdf_manifest.py 头注释；\n"
        f"# 由脚本扫描生成（{date.today().isoformat()}），勿手工编辑；data/pdf/ 本体不入 git。\n"
        f"version: pdf_v1\n"
        f"total_docs: {len(docs)}\n"
        f"docs:\n"
    )
    body = yaml.safe_dump(docs, allow_unicode=True, sort_keys=False, width=120)
    OUT.write_text(header + body)
    by_vendor = {}
    for d in docs:
        by_vendor[d["vendor"]] = by_vendor.get(d["vendor"], 0) + 1
    print(f"manifest -> {OUT}：{len(docs)} docs {by_vendor}，池中排除 {skipped_pool} 个 PDF")


if __name__ == "__main__":
    main()
