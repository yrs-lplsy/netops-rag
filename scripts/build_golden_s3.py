"""S3 生成 200 条四类分层 golden set（PDF v1 语料，hybrid chunks 子块）。

分布：factual 100（huawei-V600R025 / huawei-V600R024 / cisco / h3c 各 25，其中
跨版本 filter 题 >=15，锚定 md diff 实测的版本差异内容）/ troubleshoot 40 /
multihop 30 / reject 30（4 个经全语料验证不存在的主题）。

采样纪律：只从 hybrid `chunks` 的子块（is_parent == false）生成；桶内按文档
round-robin + 每文档/每卷上限采样，避免 doc-order 截断（S1 教训）；近空/目录/
纯型号表片段上行剔除；TOC 目录 chunk（`is_toc_chunk`：面包屑含 Contents 或点线
目录行主导，2026-09-06 修复轮新增）在采样池与 QC 双重拦截。QC 全量跑（乱码/
结巴/外语夹杂/无指代宾语/陈述句/重复/TOC/grounding 审计），淘汰带原因入台账。

修复模式（--repair-toc）：只重指出题源命中 TOC 签名的既有条目——qid 保持不变
（评测历史可比），题目/期望 chunk 自真实内容 chunk 重生成（同 qtype、同 vendor
桶、与全集查重），yaml 重写 + review queue 追加 TOC修复台账；不动其他条目。

输出：data/golden/s3_full.yaml + data/golden/s3_review_queue.md（抽样 40 条 +
生成统计 + 淘汰台账 + 版本对核验记录）。所有统计由本脚本打印/写文件。

用法：uv run python scripts/build_golden_s3.py
"""

import argparse
import difflib
import hashlib
import json
import os
import random
import re
import signal
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from netrag.config import Settings
from netrag.eval.builder import (
    PROMPT,
    REJECT_PROMPT,
    TROUBLESHOOT_PROMPT,
    _is_garbage,
    generate_multihop_items,
    generate_questions,
    pick_multihop_pairs,
    select_troubleshoot_chunks,
)
from netrag.eval.golden import GoldenItem, load_golden, save_golden
from netrag.generation.llm import LLMClient
from netrag.index.milvus_client import get_milvus, wait_healthy
from netrag.retrieval.base import MetadataFilter
from netrag.ingestion.types import Chunk

REPO = Path(__file__).resolve().parents[1]
MD = REPO / "data" / "processed_pdf"
OUT_YAML = REPO / "data" / "golden" / "s3_full.yaml"
OUT_REVIEW = REPO / "data" / "golden" / "s3_review_queue.md"

SEED = 20260905
TARGETS = {"factual": 100, "troubleshoot": 40, "multihop": 30, "reject": 30}
FACT_QUOTA = {"hw25": 25, "hw24": 25, "cisco": 25, "h3c": 25}
VERSION_TARGET = {"hw25": 8, "hw24": 7}  # 合计 >=15 版本 filter 题
TS_QUOTA = {"hw25": 14, "hw24": 8, "cisco": 4, "h3c": 8, "hwcase": 6}
MH_QUOTA = {"hw25": 9, "hw24": 5, "cisco": 8, "h3c": 8}
DOC_CAP = {"hw25": 3, "hw24": 3, "cisco": 10, "h3c": 8}
VOL_CAP = {"hw25": 20, "hw24": 15}

VERSION_PROMPT = (
    "根据以下网络设备手册片段（属于华为 {ver} 版本文档），写一个中文事实型问题。"
    "问题中必须包含版本号 {ver}，以及片段里的具体特性名/命令/参数名，答案能由该片段直接回答。"
    "不要出现'片段''上文'这类指代。只输出问题本身。\n\n片段：\n{text}"
)

# ---------------- TOC/目录 chunk 判别（2026-09-06 修复轮） ----------------
# 缺陷：cisco 整本书 PDF 的目录页被采为出题源（11 条坏题，huawei 分章 PDF 干净）——
# book 级 Contents 页（正文被抽成无换行的"标题 页码"长串）与章首 mini-TOC（"• …,
# on page N" 列表）都提到特性名，grounding 审计因此放行，但它们无法答题。
# 判别签名（控制器核验，恰好命中全部 11 条坏题、197 个期望 chunk 中无其他）：
# ① breadcrumb 含 "Contents"；② 点线目录行主导：> _TOC_DOTLEADER_RATIO 的非空行
#    以 "非空白标题 + 页码" 结尾。
# 已知良性误伤：hw/h3c 5 条 CLI 回显/日志碎片（行尾数字密集）同样被剔除——本就不
# 是合格出题素材，且当前 golden 无一期望 chunk 命中（全量核验见 task-3 报告 TOC修复节）。
_TOC_BREADCRUMB_MARK = "Contents"
_TOC_DOTLEADER_RE = re.compile(r"\S+\s+\d{1,4}\s*$")
_TOC_DOTLEADER_RATIO = 0.5
_TOC_MIN_LINES = 4  # 非空行少于该数不判点线主导（防"Step 3"式短片段误杀）


def is_toc_chunk(breadcrumb: str, text: str) -> bool:
    """TOC/目录 chunk 判别：面包屑含 "Contents"，或点线目录行占非空行多数。"""
    if _TOC_BREADCRUMB_MARK in (breadcrumb or ""):
        return True
    lines = [ln for ln in (text or "").splitlines() if ln.strip()]
    if len(lines) < _TOC_MIN_LINES:
        return False
    dots = sum(1 for ln in lines if _TOC_DOTLEADER_RE.search(ln))
    return dots / len(lines) > _TOC_DOTLEADER_RATIO


def toc_reason(item: GoldenItem, chunk_by_id: dict[str, Chunk]) -> str | None:
    """QC：期望 chunk 为 TOC 目录页 → 不能作为答题依据，淘汰带原因。"""
    for cid in item.expected_chunk_ids:
        c = chunk_by_id.get(cid)
        if c is not None and is_toc_chunk(c.breadcrumb, c.text):
            return f"toc-chunk({cid.rsplit('#', 1)[-1]})"
    return None

# 拒答主题：子话题逐一经全语料关键词验证不存在（验证记录写入 review queue）
REJECT_TOPICS: list[tuple[str, list[str]]] = [
    ("大模型", ["大模型", "LLM", "神经网络", "ChatGPT"], [
        "大模型训练任务的GPU资源调度", "大模型推理服务的部署与扩缩容", "基于RAG的大模型知识库问答系统搭建",
        "大模型Agent自动巡检网络设备", "大模型量化压缩后精度评估", "大模型训练集群的故障域隔离",
        "大模型告警根因归因平台", "大模型prompt注入攻击防护"]),
    ("Kubernetes容器网络", ["Kubernetes", "k8s", "容器编排"], [
        "Kubernetes CNI插件选型与安装", "Kubernetes Ingress流量暴露配置", "Kubernetes NetworkPolicy网络策略下发",
        "Kubernetes service mesh流量治理", "Kubernetes集群etcd备份恢复", "Kubernetes节点亲和性调度配置",
        "Kubernetes Helm应用发布回滚", "Kubernetes跨集群服务发现"]),
    ("自动化运维工具链", ["Ansible", "Zabbix", "Prometheus", "自动化运维"], [
        "Ansible playbook批量配置下发", "Zabbix监控交换机端口流量模板", "Prometheus抓取网络设备指标",
        "Grafana可视化监控大盘搭建", "自动化巡检机器人编排", "网络配置基线核查工具选型",
        "运维工单系统与CMDB联动", "ELK日志平台采集网络设备日志"]),
    ("Docker容器技术", ["Docker", "docker"], [
        "Dockerfile镜像构建优化", "Docker容器端口映射配置", "docker0网桥网段修改",
        "私有镜像仓库Harbor搭建", "Docker日志驱动与轮转", "Docker Swarm集群组网"]),
]


def norm(t: str) -> str:
    return re.sub(r"\s+", "", t)


def bucket_of(doc_id: str) -> str:
    if doc_id.startswith("hw-v600-case"):
        return "hwcase"
    if doc_id.startswith("hw-v600r025c00"):
        return "hw25"
    if doc_id.startswith("hw-v600r024c10"):
        return "hw24"
    if doc_id.startswith("cisco"):
        return "cisco"
    if doc_id.startswith("h3c"):
        return "h3c"
    return "other"


def volume_of(doc_id: str) -> str:
    if doc_id.startswith("hw-"):
        m = re.match(r"hw-v600\w*-(.+?)-\d+-\d+$", doc_id)
        return m.group(1) if m else doc_id
    return doc_id  # cisco 整本书 / h3c 分册各自成卷


def load_children() -> list[Chunk]:
    client = get_milvus()
    wait_healthy(client)
    rows = {}
    it = client.query_iterator("chunks", filter="is_parent == false",
                               output_fields=["chunk_id", "doc_id", "parent_id", "vendor",
                                              "model", "sw_version", "breadcrumb", "text"],
                               batchSize=4000)
    while True:
        batch = it.next()
        if not batch:
            break
        for r in batch:
            rows[r["chunk_id"]] = Chunk(
                chunk_id=r["chunk_id"], doc_id=r["doc_id"], text=r["text"],
                breadcrumb=r["breadcrumb"], vendor=r["vendor"], model=r["model"],
                sw_version=r["sw_version"], parent_id=r["parent_id"] or None)
    it.close()
    print(f"loaded {len(rows)} children from hybrid chunks")
    return list(rows.values())


def ordered_pool(chunks: list[Chunk], bucket: str, rng: random.Random) -> list[Chunk]:
    """桶内可用子块池（剔除近空/TOC 目录页/纯型号表），文档 round-robin 展开：
    每文档至多 DOC_CAP 条、每卷至多 VOL_CAP 条，防 doc-order 截断（S1 教训）。"""
    by_doc: dict[str, list[Chunk]] = defaultdict(list)
    for c in chunks:
        if bucket_of(c.doc_id) == bucket and not _is_garbage(c.text) \
                and not is_toc_chunk(c.breadcrumb, c.text):
            by_doc[c.doc_id].append(c)
    docs = sorted(by_doc)
    rng.shuffle(docs)
    dcap, vcap = DOC_CAP.get(bucket, 4), VOL_CAP.get(bucket, 10 ** 9)
    vol_cnt: Counter = Counter()
    pool: list[Chunk] = []
    for rnd in range(dcap):
        for d in docs:
            if rnd >= len(by_doc[d]):
                continue
            v = volume_of(d)
            if vol_cnt[v] >= vcap:
                continue
            pool.append(by_doc[d][rnd])
            vol_cnt[v] += 1
    return pool


# ---------------- QC ----------------

INTERROG_RE = re.compile(r"？|\?|如何|什么|怎么|怎样|哪些|多少|是否|为什么|哪个|何种|几|吗|呢")
REFERENT_RE = re.compile(r"片段|上文|本节|本章|该文档|此文档|(?<![版])本文档|如下所示|以下内容|上述|手册中")
STUTTER_RE = re.compile(r"(.{2,6})\1{2,}")
ASCII_TERM_RE = re.compile(r"[A-Za-z][A-Za-z0-9.\-_/]{1,}")


def qc_check(q: str, grounding_text: str | None) -> str | None:
    """返回淘汰原因，None=通过。grounding_text=None 时跳过 grounding 审计。"""
    if len(q) < 8 or len(q) > 160:
        return "length"
    if STUTTER_RE.search(q):
        return "stutter"
    if REFERENT_RE.search(q):
        return "referent"
    if not INTERROG_RE.search(q):
        return "non-question"
    cjk = sum(1 for ch in q if "\u4e00" <= ch <= "\u9fff")
    if cjk < max(4, int(len(q) * 0.2)):  # 外语夹杂/乱码
        return "non-CJK"
    # 重复片段（同句内 3 连重复短语的宽松版已在 stutter 覆盖）
    if grounding_text is not None:
        gt = norm(grounding_text).lower()
        toks = [t.lower() for t in ASCII_TERM_RE.findall(q)]
        if toks:
            cov = sum(1 for t in toks if t in gt) / len(toks)
            if cov < 0.8:
                return f"grounding(ascii {cov:.2f})"
        else:
            qc = [ch for ch in q if "\u4e00" <= ch <= "\u9fff"]
            if qc:
                gc = sum(1 for ch in qc if ch in gt) / len(qc)
                if gc < 0.55:
                    return f"grounding(cjk {gc:.2f})"
    return None


class QCDedup:
    """全量查重：归一化精确重复 + 字符 bigram Jaccard 近重复。"""

    def __init__(self, thresh: float = 0.85) -> None:
        self.seen: list[set] = []
        self.thresh = thresh

    @staticmethod
    def _bigrams(q: str) -> set:
        s = re.sub(r"[\s，。？！、：;,'\"?\-（）()]+", "", q)
        return {s[i:i + 2] for i in range(len(s) - 1)} if len(s) > 1 else {s}

    def check(self, q: str) -> str | None:
        bg = self._bigrams(q)
        for other in self.seen:
            inter = len(bg & other)
            if inter and inter / max(1, len(bg | other)) >= self.thresh:
                return "duplicate"
            if inter / max(1, min(len(bg), len(other))) >= 0.95:
                return "duplicate"
        return None

    def add(self, q: str) -> None:
        self.seen.append(self._bigrams(q))


# ---------------- 版本差异核验 ----------------

def _chapter_regions(mine_lines: list[str], other_lines: list[str], budget_s: int = 60) -> list[str]:
    """单章 diff → 本版本独有归一化文本块。两侧先剔除纯型号表行/空行
    （避免 difflib 在重复表格行上二次方爆炸，且这些块本就不作为出题素材）；
    单章限时 budget_s 秒，超时放弃（SIGALRM）。"""
    def keep(ln: str) -> bool:
        s = ln.strip()
        return bool(s) and not s.startswith("|") and "支持产品" not in s

    a = [ln for ln in mine_lines if keep(ln)]
    b = [ln for ln in other_lines if keep(ln)]
    regions: list[str] = []

    class _Timeout(Exception):
        pass

    def _alarm(sig, frm):
        raise _Timeout

    old = signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(budget_s)
    try:
        sm = difflib.SequenceMatcher(None, a, b, autojunk=True)  # autojunk 必开：False 在重复表格行上二次方爆炸
        for tag, i1, i2, _j1, _j2 in sm.get_opcodes():
            if tag == "equal":
                continue
            block = norm("".join(a[i1:i2]))
            if len(block) >= 120:
                regions.append(block)
    except _Timeout:
        print(f"    chapter diff timeout({budget_s}s), skipped", flush=True)
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)
    return regions


def verify_and_pick_version_chunks(chunks: list[Chunk], rng: random.Random) -> dict:
    """版本独有内容核验（eth-switch + ip-route 两卷，024/025 逐章 md diff）：

    1. 对每对同章 md 跑 difflib opcodes（剔除型号表行），取本版本独有的
       归一化文本块（>=120 字符）为"版本差异区域"；
    2. 区域 3 探针（首/中/尾 60 字符）在对方版本全语料精确缺席 → 区域核验通过；
    3. 找出覆盖区域探针的非垃圾子块（每文档至多 1 条）作为版本 filter 题的
       期望 chunk。
    返回 {bucket: [chunk, ...]}，全部核验记录打印供报告引用。
    """
    ver_corpus = {}
    for ver in ("024c10", "025c00"):
        ver_corpus[ver] = norm("".join(p.read_text() for p in MD.glob(f"hw-v600r{ver}-*.md")))
    result: dict[str, list[Chunk]] = {}
    pairs = [("hw25", "025c00", "024c10"), ("hw24", "024c10", "025c00")]
    for bucket, ver, other in pairs:
        other_text = ver_corpus[other]
        by_doc: dict[str, list[Chunk]] = defaultdict(list)
        for c in chunks:
            if bucket_of(c.doc_id) == bucket and not _is_garbage(c.text):
                by_doc[c.doc_id].append(c)
        verified: list[Chunk] = []
        seen_doc: set = set()
        n_region = 0
        mine_files = sorted(MD.glob(f"hw-v600r{ver}-eth-switch-01-*.md")) + \
            sorted(MD.glob(f"hw-v600r{ver}-ip-route-01-*.md"))
        for mf in mine_files:
            stem = mf.stem.replace(f"hw-v600r{ver}-", "")  # e.g. eth-switch-01-04
            other_file = MD / f"hw-v600r{other}-{stem}.md"
            if not other_file.exists() or stem.endswith(("00-1", "00-2")):
                continue
            doc_id = f"hw-v600r{ver}-{stem}"
            doc_chunks = by_doc.get(doc_id, [])
            if not doc_chunks:
                continue
            regions = _chapter_regions(mf.read_text().splitlines(), other_file.read_text().splitlines())
            for region in regions:
                n_region += 1
                probes = [region[:60], region[len(region) // 2:len(region) // 2 + 60], region[-60:]]
                if any(p in other_text for p in probes):
                    continue  # 对方版本全语料确有该内容 → 非版本独有
                covering = [c for c in doc_chunks if any(p in norm(c.text) for p in probes)]
                covering.sort(key=lambda c: -len(c.text))
                for c in covering:  # 每文档至多 1 条版本题
                    if c.doc_id in seen_doc or is_toc_chunk(c.breadcrumb, c.text):
                        continue
                    seen_doc.add(c.doc_id)
                    verified.append(c)
                    print(f"  delta[{ver}] {c.chunk_id} :: {c.text[:60]!r}", flush=True)
                    break
        result[bucket] = verified
        print(f"version-delta [{bucket}]: {len(verified)} verified chunks "
              f"(regions checked {n_region})", flush=True)
    return result


def filter_mechanism_pairs(chunks: list[Chunk]) -> list[tuple[Chunk, str]]:
    """回退：跨版本字节相同的片段（归一化后相等），作为纯过滤机制测试。"""
    idx: dict[str, list[Chunk]] = defaultdict(list)
    for c in chunks:
        if bucket_of(c.doc_id) in ("hw25", "hw24") and not _is_garbage(c.text):
            idx[norm(c.text)[:400]].append(c)
    out = []
    for key, group in idx.items():
        b25 = [c for c in group if bucket_of(c.doc_id) == "hw25"]
        b24 = [c for c in group if bucket_of(c.doc_id) == "hw24"]
        if b25 and b24 and len(norm(group[0].text)) >= 150:
            out.append((group[0], b25[0].doc_id if bucket_of(group[0].doc_id) == "hw24" else b24[0].doc_id))
    return out


# ---------------- 生成主流程 ----------------

def gen_class(pool: list[Chunk], llm, qtype: str, target: int, dedup: QCDedup,
              texts: dict, ledger: list, rng: random.Random, prompt_extra: str | None = None,
              sw_prefix: str = "", chunk_by_id: dict[str, Chunk] | None = None) -> list[GoldenItem]:
    kept: list[GoldenItem] = []
    i = 0
    while len(kept) < target and i < len(pool):
        batch = pool[i:i + 10]
        i += 10
        if prompt_extra is None:
            items = generate_questions(batch, llm, qtype=qtype)
        else:  # 版本 filter 题：脚本级 prompt（要求带版本号）
            items = []
            for c in batch:
                q = llm.chat([{"role": "user", "content": prompt_extra.format(ver=sw_prefix, text=c.text[:2000])}])
                q = re.sub(r"\s+", " ", q.strip().strip('"').strip("“”").strip())
                if len(q) >= 8:
                    items.append(GoldenItem(
                        qid=f"{c.chunk_id}#ver", question=q, qtype="factual",
                        expected_doc_ids=[c.doc_id], expected_chunk_ids=[c.chunk_id],
                        filters=MetadataFilter(sw_version=sw_prefix)))
        for src, it in zip(batch, items):
            if len(kept) >= target:
                break
            reason = (toc_reason(it, chunk_by_id) if chunk_by_id else None) or \
                qc_check(it.question, "\n".join(texts[cid] for cid in it.expected_chunk_ids))
            if reason:
                ledger.append((it, reason))
                print(f"    drop[{reason}] {it.question[:60]}", flush=True)
                continue
            reason = dedup.check(it.question)
            if reason:
                ledger.append((it, reason))
                print(f"    drop[{reason}] {it.question[:60]}", flush=True)
                continue
            dedup.add(it.question)
            kept.append(it)
        done = min(i, len(pool))
        print(f"  [{qtype}] processed {done}/{len(pool)} kept {len(kept)}/{target}", flush=True)
    return kept


REJECT_CONCISE_HINT = "只问一个最具体的点，问题控制在60字以内，不要展开多个方面。"


def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().strip('"').strip("“”").strip())


class CachedLLM:
    """llm.chat 磁盘缓存（sha1(prompt|temperature|max_tokens) → 回复）。

    目的：重跑/修复轮不重复计费且生成结果可复现（同 prompt 恒同回复）。
    缓存文件不入 git（data/llm_cache/ 在 .gitignore）。
    """

    def __init__(self, inner, path: Path) -> None:
        self._inner = inner
        self._path = path
        self._cache: dict = json.loads(path.read_text()) if path.exists() else {}
        self.hits = 0
        self.misses = 0

    def chat(self, messages: list[dict], temperature: float = 0.2, max_tokens: int = 2048) -> str:
        key = hashlib.sha1(
            f"{messages[-1]['content']}|{temperature}|{max_tokens}".encode()).hexdigest()
        if key not in self._cache:
            self._cache[key] = self._inner.chat(messages, temperature=temperature,
                                                max_tokens=max_tokens)
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(json.dumps(self._cache, ensure_ascii=False))
            self.misses += 1
        else:
            self.hits += 1
        return self._cache[key]


def dedupe_qids(items: list[GoldenItem]) -> None:
    """qid 全局唯一（评审 Finding 2）：跨类同 chunk 冲突时后续项加 ~N 后缀。"""
    from collections import Counter
    ctr: Counter = Counter()
    for it in items:
        ctr[it.qid] += 1
        if ctr[it.qid] > 1:
            it.qid = f"{it.qid}~{ctr[it.qid]}"
    assert len({it.qid for it in items}) == len(items), "qid 去重失败"


def gen_reject_with_qc(llm, topics: list[str], ledger: list, dedup: QCDedup) -> list[GoldenItem]:
    """reject 生成 + 全量 QC：QC 失败真删（绝不入集），失败主题用简短提示重试一轮。

    qid 序号 = 主题在 topics 列表中的序号（01..NN，全局唯一）。
    """
    survivors: list[GoldenItem] = []
    remaining = list(enumerate(topics, start=1))
    for rnd, hint in enumerate(("", REJECT_CONCISE_HINT)):
        if not remaining:
            break
        if rnd:
            print(f"reject retry pass {rnd}（简短提示）: {len(remaining)} 条待补", flush=True)
        still: list = []
        for pos, topic in remaining:
            q = _clean(llm.chat([{"role": "user", "content": REJECT_PROMPT.format(theme=topic) + hint}]))
            it = GoldenItem(qid=f"reject-{topic}-{pos:02d}", question=q, qtype="reject",
                            expected_doc_ids=[], expected_chunk_ids=[])
            reason = qc_check(q, None) if q else "empty"
            if reason:
                ledger.append((it, reason))  # 真删：不进 survivors
                still.append((pos, topic))
                print(f"    drop[{reason}] {(q or '')[:60]}", flush=True)
                continue
            survivors.append(it)
        remaining = still
    out: list[GoldenItem] = []
    for it in survivors:
        reason = dedup.check(it.question)
        if reason:
            ledger.append((it, reason))
            print(f"    drop[{reason}] {it.question[:60]}", flush=True)
            continue
        dedup.add(it.question)
        out.append(it)
    return out


# ---------------- 修复模式（--repair-toc，2026-09-06） ----------------

# cisco 排障候选的修复轮放宽：cisco 整本书无独立故障处理卷，原 Troubleshooting 关键词
# 候选几乎全落在 mini-TOC 上（被 is_toc_chunk 拦截后仅剩 1 条未用）；为 troubleshoot
# 坏题补候选，改用故障语义宽匹配（失败/不生效/不一致等描述性内容，仍非 TOC 非垃圾）。
REPAIR_FAULT_RE = re.compile(
    r"(fails?|failure|cannot|unable|does not work|not working|not effective|"
    r"incorrect|inconsisten|misconfig|problem|invalid|loss|lost)", re.IGNORECASE)
REPAIR_MAX_CALLS = 30  # LLM 实调预算护栏，超过即中止（不写盘）


def _single_question(cand: Chunk, qtype: str, llm) -> GoldenItem | None:
    """单片段出题：与 builder.generate_questions 同 prompt/同清洗（保证可命中缓存）。"""
    prompt = TROUBLESHOOT_PROMPT if qtype == "troubleshoot" else PROMPT
    q = _clean(llm.chat([{"role": "user", "content": prompt.format(text=cand.text[:2000])}]))
    if not q or len(q) < 8:
        return None
    return GoldenItem(qid=f"{cand.doc_id}#{cand.chunk_id}", question=q, qtype=qtype,
                      expected_doc_ids=[cand.doc_id], expected_chunk_ids=[cand.chunk_id])


def _same_doc_first(cands: list, doc: str, rng: random.Random) -> list:
    """先乱序再稳定排序：同文档候选优先，组内保持随机序（确定性由 SEED 保证）。"""
    rng.shuffle(cands)
    cands.sort(key=lambda c: c.doc_id != doc)
    return cands


_BC_BOOK_MARK = "Cisco IOS XE Cupertino"


def _multihop_pair_coherent(prim: Chunk, sec: Chunk) -> bool:
    """pair 主题亲和度：去掉书名段后两面包屑存在同章节段（同章节的 cmd×concept，
    防止 LLM 把两章内容编织成语料中不存在的"冲突"场景——首轮修复实测教训）。"""
    def segs(bc: str) -> set[str]:
        return {s.strip().lower() for s in (bc or "").split(" > ")
                if s.strip() and _BC_BOOK_MARK not in s}
    return bool(segs(prim.breadcrumb) & segs(sec.breadcrumb))


def repair_toc(llm, rng: random.Random) -> None:
    """重指出题源命中 is_toc_chunk 签名的既有条目：qid 不变，题目/期望 chunk 重生成。

    只动命中条目：同 qtype、同 vendor 桶（cisco）、候选同文档优先、与全集查重；
    全部成功才写盘（save_golden + review queue 追加 TOC修复台账）。
    """
    items = load_golden(OUT_YAML)
    chunks = load_children()
    chunk_by_id = {c.chunk_id: c for c in chunks}
    texts = {c.chunk_id: f"{c.text}\n{c.breadcrumb}" for c in chunks}
    bad = [it for it in items if it.qtype != "reject" and toc_reason(it, chunk_by_id)]
    print(f"repair-toc: {len(bad)} items flagged with TOC expected chunks", flush=True)
    for it in bad:
        print(f"  {it.qid} [{it.qtype}] :: {it.question[:50]}", flush=True)
    if not bad:
        print("nothing to repair")
        return

    used = {cid for it in items for cid in it.expected_chunk_ids}
    dedup = QCDedup()
    for it in items:
        dedup.add(it.question)  # 与全集查重（含被替换旧题，更严）
    new_bgs: list[set] = []  # 修复轮内部近重复护栏（阈值比全集严：同轮新题易同题材）

    def near_dup_with_new(q: str) -> str | None:
        bg = dedup._bigrams(q)
        for other in new_bgs:
            inter = len(bg & other)
            if inter and inter / max(1, len(bg | other)) >= 0.55:
                return f"near-dup(new {inter / max(1, len(bg | other)):.2f})"
        return None

    cisco = [c for c in chunks if bucket_of(c.doc_id) == "cisco"]
    repairs: list[dict] = []

    def candidates_for(it: GoldenItem) -> list:
        doc = it.expected_doc_ids[0]
        if it.qtype == "multihop":
            pairs = [p for p in pick_multihop_pairs(cisco)
                     if not is_toc_chunk(p[0].breadcrumb, p[0].text)
                     and not is_toc_chunk(p[1].breadcrumb, p[1].text)
                     and p[0].chunk_id not in used and p[1].chunk_id not in used]
            rng.shuffle(pairs)
            pairs.sort(key=lambda p: (p[0].doc_id != doc,
                                      not _multihop_pair_coherent(p[0], p[1])))
            return pairs
        if it.qtype == "troubleshoot":
            prim = [c for c in select_troubleshoot_chunks(cisco)
                    if not is_toc_chunk(c.breadcrumb, c.text)]
            wide = [c for c in cisco if not _is_garbage(c.text)
                    and not is_toc_chunk(c.breadcrumb, c.text)
                    and REPAIR_FAULT_RE.search(c.text)]
            pool = [c for c in {c.chunk_id: c for c in prim + wide}.values()
                    if c.chunk_id not in used]
            return _same_doc_first(pool, doc, rng)
        pool = [c for c in ordered_pool(chunks, "cisco", rng) if c.chunk_id not in used]
        return _same_doc_first(pool, doc, rng)

    for it in bad:
        done = False
        for cand in candidates_for(it):
            if llm.misses >= REPAIR_MAX_CALLS:
                raise RuntimeError(f"LLM 实调超过预算 {REPAIR_MAX_CALLS}，中止（未写盘）")
            if it.qtype == "multihop":
                got = generate_multihop_items([cand], llm)
                nit = got[0] if got else None
            else:
                nit = _single_question(cand, it.qtype, llm)
            if nit is None:
                continue
            reason = toc_reason(nit, chunk_by_id) or qc_check(
                nit.question, "\n".join(texts[cid] for cid in nit.expected_chunk_ids))
            if not reason:
                reason = dedup.check(nit.question) or near_dup_with_new(nit.question)
            if reason:
                print(f"    drop[{reason}] {nit.question[:50]}", flush=True)
                continue
            dedup.add(nit.question)
            new_bgs.append(dedup._bigrams(nit.question))
            old_q, old_cids = it.question, list(it.expected_chunk_ids)
            it.question, it.expected_chunk_ids = nit.question, list(nit.expected_chunk_ids)
            it.expected_doc_ids = list(nit.expected_doc_ids)
            used |= set(nit.expected_chunk_ids)
            repairs.append({"qid": it.qid, "qtype": it.qtype, "old_question": old_q,
                            "old_cids": old_cids, "new_question": it.question,
                            "new_cids": it.expected_chunk_ids})
            print(f"  repointed -> {it.qid}\n    new: {it.question}", flush=True)
            done = True
            break
        if not done:
            raise RuntimeError(f"{it.qid} 未找到合格替换候选（未写盘）")

    save_golden(items, OUT_YAML)
    patch_review_queue(repairs)
    print(f"llm cache: {llm.hits} hits / {llm.misses} misses", flush=True)
    print(f"repointed {len(repairs)} items; written: {OUT_YAML}")


def patch_review_queue(repairs: list[dict]) -> None:
    """抽样区被重指 qid 的两行原位替换；文末追加 TOC修复台账（其余内容不动）。"""
    lines = OUT_REVIEW.read_text().splitlines()
    by_qid = {r["qid"]: r for r in repairs}
    for i, ln in enumerate(lines):
        m = re.match(r"- `([^`]+)` ", ln)
        if m and m.group(1) in by_qid:
            r = by_qid[m.group(1)]
            lines[i] = f"- `{r['qid']}` {r['new_question']}"
            if i + 1 < len(lines) and lines[i + 1].lstrip().startswith("- 期望："):
                lines[i + 1] = "  - 期望：" + ", ".join(r["new_cids"])
    lines += ["", "## TOC修复台账（2026-09-06）", "",
              "缺陷：11 条期望 chunk 为 cisco 整本书 PDF 的目录页（book 级 Contents 页 / 章首 mini-TOC），"
              "无法答题——生成管线把 TOC chunk 采为出题源，grounding 审计因 TOC 文本提及特性名而放行。修复：",
              "1. `build_golden_s3.py` 新增 `is_toc_chunk` 判别（breadcrumb 含 Contents，或点线目录行主导），"
              "采样池构造与 QC 双重拦截；",
              "2. 以下 qid 保持不变（评测历史可比），题目/期望 chunk 自真实内容 chunk 重生成"
              "（同 qtype、同 cisco 桶、原题均无版本 filter 语义、与全集查重不重复）：", ""]
    for r in repairs:
        lines.append(f"- `{r['qid']}`（{r['qtype']}）期望 "
                     f"{'+'.join(c.rsplit('#', 1)[-1] for c in r['old_cids'])} → "
                     f"{'+'.join(c.rsplit('#', 1)[-1] for c in r['new_cids'])}")
        lines.append(f"  - 旧题：{r['old_question']}")
        lines.append(f"  - 新题：{r['new_question']}")
    OUT_REVIEW.write_text("\n".join(lines) + "\n")
    print(f"review queue updated: {OUT_REVIEW}", flush=True)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="只做采样/核验，不调 LLM 不写盘")
    ap.add_argument("--repair-toc", action="store_true",
                    help="修复模式：只重指出题源为 TOC 目录页的既有条目（qid 保持不变）")
    ap.add_argument("--llm-cache", default=str(REPO / "data" / "llm_cache" / "s3_gen.json"),
                    help="LLM 回复磁盘缓存（可复现，不重复计费）；不存在则冷启动")
    args = ap.parse_args()
    rng = random.Random(SEED)

    if args.repair_toc:
        repair_toc(CachedLLM(LLMClient(Settings.from_env()), Path(args.llm_cache)), rng)
        return

    chunks = load_children()
    chunk_by_id = {c.chunk_id: c for c in chunks}
    # grounding 审计用全文 = chunk 正文 + breadcrumb（版本号/章节标题常在面包屑里）
    texts = {c.chunk_id: f"{c.text}\n{c.breadcrumb}" for c in chunks}
    buckets: dict[str, list[Chunk]] = defaultdict(list)
    for c in chunks:
        buckets[bucket_of(c.doc_id)].append(c)
    for b, lst in sorted(buckets.items()):
        print(f"bucket {b}: {len(lst)} children, {len({c.doc_id for c in lst})} docs")

    # ---- reject 主题缺席核验（全语料）----
    all_md = "\n".join(p.read_text() for p in MD.glob("*.md"))
    verify_lines, reject_flat = [], []
    for theme, markers, topics in REJECT_TOPICS:
        hits = {m: all_md.count(m) for m in markers}
        bad = {m: n for m, n in hits.items() if n > 0}
        verify_lines.append((theme, hits))
        assert not bad, f"reject 主题 {theme} 标记词在语料中出现: {bad}"
        reject_flat.extend((theme, t) for t in topics)
    print(f"reject themes verified absent: {[t for t, _, _ in REJECT_TOPICS]}", flush=True)

    # ---- 版本差异核验 ----
    ver_chunks = verify_and_pick_version_chunks(chunks, rng)
    for b, lst in ver_chunks.items():
        print(f"version-delta verified chunks [{b}]: {len(lst)}")
        for c in lst[:20]:
            print(f"   {c.chunk_id} :: {c.text[:50]!r}")

    if args.dry_run:
        for b in ("hw25", "hw24", "cisco", "h3c"):
            print(f"pool[{b}] = {len(ordered_pool(chunks, b, random.Random(SEED)))}")
        ts = {b: len(select_troubleshoot_chunks([c for c in chunks if bucket_of(c.doc_id) == b]))
              for b in ("hw25", "hw24", "cisco", "h3c", "hwcase")}
        print("troubleshoot candidates:", ts)
        mh = {b: len(pick_multihop_pairs([c for c in chunks if bucket_of(c.doc_id) == b]))
              for b in ("hw25", "hw24", "cisco", "h3c")}
        print("multihop pairs:", mh)
        return

    llm = CachedLLM(LLMClient(Settings.from_env()), Path(args.llm_cache))
    ledger: list = []
    dedup = QCDedup()
    items: list[GoldenItem] = []

    # ---- factual：先版本 filter 题（>=15），再各桶补齐 25 ----
    fm_used = 0
    for b in ("hw25", "hw24"):
        ver = "V600R025C00" if b == "hw25" else "V600R024C10"
        pool = ver_chunks[b][:VERSION_TARGET[b]]
        got = gen_class(pool, llm, "factual", VERSION_TARGET[b], dedup, texts, ledger, rng,
                        prompt_extra=VERSION_PROMPT, sw_prefix=ver, chunk_by_id=chunk_by_id)
        items.extend(got)
        print(f"factual[{b}] version-filter items: {len(got)}", flush=True)
    n_ver = len([it for it in items if it.filters])
    need = 15 - n_ver
    if need > 0:  # 回退：最多 3 条纯过滤机制题（跨版本同文），报告中单独标注
        for c, _other_doc in filter_mechanism_pairs(chunks)[:min(need, 3)]:
            ver = "V600R025C00" if bucket_of(c.doc_id) == "hw25" else "V600R024C10"
            got = gen_class([c], llm, "factual", 1, dedup, texts, ledger, rng,
                            prompt_extra=VERSION_PROMPT, sw_prefix=ver, chunk_by_id=chunk_by_id)
            if got:
                got[0].qid = f"{c.chunk_id}#fm"
                items.append(got[0])
                fm_used += 1
    for b, quota in FACT_QUOTA.items():
        rest = quota - len([it for it in items
                            if it.qtype == "factual" and bucket_of(it.expected_doc_ids[0]) == b
                            and it.expected_chunk_ids])
        if rest <= 0:
            continue
        got = gen_class(ordered_pool(chunks, b, rng), llm, "factual", rest, dedup, texts,
                        ledger, rng, chunk_by_id=chunk_by_id)
        print(f"factual[{b}] regular items: {len(got)}", flush=True)
        items.extend(got)

    # ---- troubleshoot ----
    for b, quota in TS_QUOTA.items():
        pool = [c for c in select_troubleshoot_chunks(buckets[b])
                if not is_toc_chunk(c.breadcrumb, c.text)]  # mini-TOC 含 Troubleshooting 词，拦截
        rng.shuffle(pool)
        got = gen_class(pool, llm, "troubleshoot", quota, dedup, texts, ledger, rng,
                        chunk_by_id=chunk_by_id)
        print(f"troubleshoot[{b}]: {len(got)}/{quota} (candidates {len(pool)})", flush=True)
        items.extend(got)

    # ---- multihop ----
    for b, quota in MH_QUOTA.items():
        pairs = [p for p in pick_multihop_pairs(buckets[b])
                 if not is_toc_chunk(p[0].breadcrumb, p[0].text)
                 and not is_toc_chunk(p[1].breadcrumb, p[1].text)]
        rng.shuffle(pairs)
        kept: list[GoldenItem] = []
        i = 0
        while len(kept) < quota and i < len(pairs):
            batch = pairs[i:i + 5]
            i += 5
            for it in generate_multihop_items(batch, llm):
                if len(kept) >= quota:
                    break
                gt = "\n".join(texts[cid] for cid in it.expected_chunk_ids)
                reason = toc_reason(it, chunk_by_id) or qc_check(it.question, gt)
                if not reason:
                    reason = dedup.check(it.question)
                if reason:
                    ledger.append((it, reason))
                    continue
                dedup.add(it.question)
                kept.append(it)
            print(f"  [multihop:{b}] processed {min(i, len(pairs))}/{len(pairs)} kept {len(kept)}/{quota}", flush=True)
        print(f"multihop[{b}]: {len(kept)}/{quota} (pairs {len(pairs)})", flush=True)
        items.extend(kept)

    # ---- reject ----
    reject_items = gen_reject_with_qc(llm, [t for _, t in reject_flat], ledger, dedup)
    assert len(reject_items) == TARGETS["reject"], \
        f"reject 两轮生成（含简短重试）后仍不足 {TARGETS['reject']} 条: {len(reject_items)}"
    items.extend(reject_items)
    print(f"reject items: {len(reject_items)}", flush=True)

    # ---- 汇总 & 校验 ----
    cnt = Counter((it.qtype, bucket_of(it.expected_doc_ids[0]) if it.expected_doc_ids else "reject")
                  for it in items)
    print("== 生成统计（类 × 桶） ==", flush=True)
    for k, v in sorted(cnt.items()):
        print(f"  {k}: {v}")
    print(f"total = {len(items)}")
    print("== 淘汰台账 ==", flush=True)
    for reason, n in Counter(r for _, r in ledger).most_common():
        print(f"  {reason}: {n}")

    dedupe_qids(items)
    save_golden(items, OUT_YAML)
    write_review(items, ledger, cnt, verify_lines)
    print(f"llm cache: {llm.hits} hits / {llm.misses} misses", flush=True)
    print(f"written: {OUT_YAML}\nwritten: {OUT_REVIEW}")


def write_review(items, ledger, cnt, verify_lines) -> None:
    rng = random.Random(SEED)
    lines = ["# S3 golden set 抽查队列（40 条）与生成台账", "",
             f"- 全集：`s3_full.yaml` 共 {len(items)} 条；分布：" +
             "，".join(f"{k[0]}×{k[1]}={v}" for k, v in sorted(cnt.items())), "",
             "## 分类抽样", ""]
    sample_n = {"factual": 16, "troubleshoot": 10, "multihop": 8, "reject": 6}
    for qt, n in sample_n.items():
        pool = [it for it in items if it.qtype == qt]
        # factual 抽样保证含版本 filter 题
        if qt == "factual":
            ver = [it for it in pool if it.filters][:4]
            rest = rng.sample([it for it in pool if not it.filters], n - len(ver))
            pool = ver + rest
        else:
            pool = rng.sample(pool, min(n, len(pool)))
        lines.append(f"### {qt}（{len(pool)} 条）")
        lines.append("")
        for it in pool:
            flt = f" filters={{{it.filters.sw_version}}}" if it.filters else ""
            exp = ", ".join(it.expected_chunk_ids) if it.expected_chunk_ids else "（空，应拒答）"
            lines.append(f"- `{it.qid}` {it.question}")
            lines.append(f"  - 期望：{exp}{flt}")
        lines.append("")
    lines += ["## reject 主题缺席核验（全语料 processed_pdf 238 文档 grep 实测）", ""]
    for theme, hits in verify_lines:
        lines.append(f"- {theme}: " + ", ".join(f"`{m}`×{n}" for m, n in hits.items()) + " → 全部 0，确认缺席")
    lines += ["", "## 淘汰台账（QC 全量）", ""]
    for reason, n in Counter(r for _, r in ledger).most_common():
        lines.append(f"- {reason}: {n} 条")
    lines.append("")
    for it, reason in ledger:
        lines.append(f"- [{reason}] `{it.qid}` {it.question[:80]}")
    OUT_REVIEW.write_text("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
