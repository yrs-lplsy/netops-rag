"""S3 快版检索评测：data/golden/s3_full.yaml（200 条四类分层）在三配置矩阵上的召回数字。

判据（沿 run_s2_eval.py 的标注模式）：
- chunk-id：hybrid 判据=命中精确等于期望子块 id；multihop 期望 2 条子块（有序，
  primary 在前），chunk 判据只认 primary（"首条命中"），另单列"任一命中"率；
  naive 索引是独立 id 空间（doc#nN vs doc#cN），chunk 判据退化为文本重叠：
  期望子块内容 token >=50% 出现在命中 chunk 中（阈值先验取 0.5，未对测试集调优）。
- parent：任一 top-k 命中的 parent_id 等于期望子块的 parent_id（章节级；naive 无
  parent 字段不适用；multihop 以 primary 的 parent 为准）。
- doc：任一 top-k 命中的 doc_id 属于期望文档。
- reject（期望命中=空，考拒答前置的检索口径）：双层"正确未命中"判据，任一层未触发误命中才记
  通过——①主题标记词（生成前经全语料 grep 验证 0 命中，回归护栏）；②题干实义词与命中 text
  重叠 >=3 个（可证伪，更严）。两层分别报告 → 记 RejectPass@k / RejectPassOverlap@k。

矩阵：naive / hybrid(dense+bm25+sparse) / hybrid 同配置+rerank；版本 filter 子集
（filters 对 naive 与 hybrid 同等应用，另有 hybrid 无 filter 诊断行，仅观测过滤
贡献，不作为主结果）。

用法：uv run python scripts/run_s3_eval.py [--golden PATH] [--k 5] [--skip-rerank]
                                     [--date YYYY-MM-DD] [--out PATH]
"""

import argparse
import os
import re
import sys
from collections import defaultdict
from dataclasses import replace
from datetime import date
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from netrag.config import Settings
from netrag.embedding.bge_m3 import BGEM3Embedder
from netrag.embedding.reranker import BgeReranker
from netrag.eval.golden import load_golden
from netrag.eval.report import write_report
from netrag.index.milvus_client import get_milvus, wait_healthy
from netrag.retrieval.hybrid import HybridRetriever
from netrag.retrieval.naive import NaiveRetriever

OVERLAP_THRESHOLD = 0.5
QTYPES = ("factual", "troubleshoot", "multihop", "reject")

# reject 主题标记词（与 build_golden_s3.py REJECT_TOPICS 的核验词一致；
# 生成前已验证：全语料 0 命中）。qid 前缀匹配。
REJECT_MARKERS: dict[str, list[str]] = {
    "reject-大模型": ["大模型", "LLM", "神经网络", "ChatGPT"],
    "reject-Kubernetes容器网络": ["Kubernetes", "k8s", "容器编排"],
    "reject-自动化运维工具链": ["Ansible", "Zabbix", "Prometheus", "自动化运维"],
    "reject-Docker容器技术": ["Docker", "docker"],
}

# reject 第二层判据（可证伪）的分词停用词：泛函数词/提问套话，不参与内容词重叠
_REJECT_STOPWORDS = {
    "的", "了", "在", "是", "和", "与", "或", "及", "对", "把", "被", "为", "以",
    "如何", "什么", "怎么", "哪些", "哪种", "是否", "为什么", "请问", "问题",
    "使用", "进行", "需要", "可以", "能够", "通过", "以及", "同时", "另外",
    "确保", "出现", "导致", "检查", "确认", "发现", "遇到", "无法", "不能",
    "如果", "但是", "还有", "就是", "例如", "比如", "情况", "时候", "这个", "那个",
    "正确", "错误", "成功", "失败", "配置", "网络", "设备",
}
OVERLAP_FALSE_HIT_WORDS = 3  # 任一 top-5 命中与问题实义词重叠 >=3 即判误命中


def _load_topic_markers() -> dict[str, list[str]]:
    """从 build_golden_s3.py 的 REJECT_TOPICS 取（主题→标记词）单一事实源。"""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "build_golden_s3_topics",
        Path(__file__).resolve().parents[1] / "scripts" / "build_golden_s3.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    m: dict[str, list[str]] = {}
    for _theme, markers, topics in mod.REJECT_TOPICS:
        for t in topics:
            m[t] = markers
    return m


_TOPIC_MARKERS = _load_topic_markers()


def reject_markers_for(qid: str) -> list[str]:
    m = re.match(r"^reject-(.+)-\d{2}$", qid)
    stem = m.group(1) if m else qid
    if stem not in _TOPIC_MARKERS:
        raise KeyError(f"reject 题无法识别主题: {qid}")
    return _TOPIC_MARKERS[stem]


def _content_words(text: str) -> set[str]:
    """实义词 = ASCII 术语（len>=2）+ 中文 2-gram，去停用词。"""
    toks = {t.lower() for t in re.findall(r"[A-Za-z][A-Za-z0-9.\-_/]{1,}", text)}
    toks |= {text[i:i + 2] for i in range(len(text) - 1)
             if "\u4e00" <= text[i] <= "\u9fff" and "\u4e00" <= text[i + 1] <= "\u9fff"}
    return toks - _REJECT_STOPWORDS


def _is_false_hit(it, hit_text: str, hit_breadcrumb: str) -> bool:
    """第一层（主题标记词，必要条件式）。"""
    return any(m in hit_text or m in hit_breadcrumb for m in reject_markers_for(it.qid))


def _is_false_hit_overlap(q_words: set[str], hit_text: str) -> bool:
    """第二层（内容词重叠，可证伪）：命中与问题实义词交集 >=3 视为误命中。

    该层能真实触发失败（如语料中偶现"容器/镜像"等词被误杀），是更严的行为口径。
    """
    return len(q_words & _content_words(hit_text)) >= OVERLAP_FALSE_HIT_WORDS


def _content_tokens(text: str) -> set[str]:
    toks = set(t.lower() for t in re.findall(r"[A-Za-z][A-Za-z0-9-]{1,}|\d[\d.]*", text))
    return toks | set(re.findall(r"[\u4e00-\u9fff]", text))


class _Acc:
    """单配置×单子集的指标累计器。"""

    def __init__(self) -> None:
        self.first: list[int] = []  # primary（首条）命中 rank，0=未命中
        self.any_hit: list[int] = []  # 任一期望 id 命中 rank
        self.doc = 0
        self.parent = 0
        self.reject_pass = 0  # 第一层：主题标记词
        self.reject_pass_ov = 0  # 第二层：内容词重叠（更严，可证伪）
        self.reject_total = 0
        self.n = 0

    def row(self, k: int) -> dict[str, float]:
        n = max(1, self.n)
        out = {f"Recall@{k}": sum(1 for r in self.first if 0 < r <= k) / n,
               f"DocRecall@{k}": self.doc / n,
               "MRR": sum(1 / r for r in self.first if 0 < r <= k) / n}
        if self.first:
            out[f"ParentRecall@{k}"] = self.parent / self.n
        if self.any_hit:
            out[f"AnyHit@{k}"] = sum(1 for r in self.any_hit if 0 < r <= k) / len(self.any_hit)
        if self.reject_total:
            out[f"RejectPass@{k}"] = self.reject_pass / self.reject_total
            out[f"RejectPassOverlap@{k}"] = self.reject_pass_ov / self.reject_total
        return out


def _eval_once(retriever, items, k: int, exp_texts: dict[str, str],
               exp_parent: dict[str, str], naive_texts: dict[str, set[str]] | None,
               collect_misses: bool = False):
    """遍历一次检索：multihop 的 first/any 分开记；reject 只记正确未命中。

    naive_texts 非 None 时为 naive 通道（chunk 判据=文本重叠）。返回 (per-qtype
    _Acc, misses)。"""
    accs: dict[str, _Acc] = defaultdict(_Acc)
    misses: list = []
    for it in items:
        hits = retriever.retrieve(it.question, top_k=k, filters=it.filters)
        a = accs[it.qtype]
        a.n += 1
        if it.qtype == "reject":
            q_words = _content_words(it.question)
            marker_false = 0
            overlap_false = 0
            for h in hits:
                marker_false += int(_is_false_hit(it, h.text, h.breadcrumb))
                overlap_false += int(_is_false_hit_overlap(q_words, h.text))
            a.reject_pass += int(marker_false == 0)
            a.reject_pass_ov += int(overlap_false == 0)
            a.reject_total += 1
            if collect_misses and (marker_false or overlap_false):
                tag = "标记词" if marker_false else "内容重叠"
                misses.append((it, [f"{h.doc_id}:{h.text[:40]}" for h in hits[:3]], tag))
            continue
        primary = it.expected_chunk_ids[0]
        if naive_texts is not None:  # naive：期望子块 token 重叠 >=0.5 视为命中
            pri_toks = _content_tokens(exp_texts[primary])
            first = next((i for i, h in enumerate(hits, start=1)
                          if pri_toks and len(pri_toks & naive_texts[h.chunk_id]) / len(pri_toks)
                          >= OVERLAP_THRESHOLD), 0)
            any_toks = [_content_tokens(exp_texts[cid]) for cid in it.expected_chunk_ids
                        if cid in exp_texts]
            any_hit = next((i for i, h in enumerate(hits, start=1)
                            if any(t and len(t & naive_texts[h.chunk_id]) / len(t)
                                   >= OVERLAP_THRESHOLD for t in any_toks)), 0)
        else:
            ids = [h.chunk_id for h in hits]
            first = next((i for i, cid in enumerate(ids, start=1) if cid == primary), 0)
            any_hit = next((i for i, cid in enumerate(ids, start=1)
                            if cid in it.expected_chunk_ids), 0)
        a.first.append(first)
        a.any_hit.append(any_hit)
        if any(h.doc_id in it.expected_doc_ids for h in hits):
            a.doc += 1
        ep = exp_parent.get(primary)
        if ep and any(h.parent_id and h.parent_id == ep for h in hits):
            a.parent += 1
        if first == 0 and collect_misses:
            misses.append((it, [h.chunk_id for h in hits[:3]], ""))
    return accs, misses


def _subset_accs(accs, qtypes) -> _Acc:
    """把多个 qtype 的 _Acc 合并成一个子集视角（对 n 与计数重新归一）。"""
    out = _Acc()
    for qt in qtypes:
        a = accs.get(qt)
        if not a:
            continue
        out.n += a.n
        out.first.extend(a.first)
        out.any_hit.extend(a.any_hit)
        out.doc += a.doc
        out.parent += a.parent
        out.reject_pass += a.reject_pass
        out.reject_pass_ov += a.reject_pass_ov
        out.reject_total += a.reject_total
    return out


def _norm_md(t: str) -> str:
    return re.sub(r"\s+", "", t)


def classify_version_items(ver_items) -> dict[str, str]:
    """版本 filter 题分级（评审 Finding 4③）：题干实义词（ASCII 术语 + 中文
    2-gram 去停用词，剔除版本号本身）全部出现在对方版本全语料 → "区域级差异"
    （期望 chunk 位于版本独有区域——见生成台账核验，但答案内容两版本均出现，
    该题同时考过滤机制而非版本独有事实）；否则 → "内容级差异"（题干含对方版本
    不存在的事实词）。"""
    md_dir = Path(__file__).resolve().parents[1] / "data" / "processed_pdf"
    corpus = {}
    for ver in ("024c10", "025c00"):
        corpus[ver] = _norm_md("".join(p.read_text() for p in md_dir.glob(f"hw-v600r{ver}-*.md")))
    levels: dict[str, str] = {}
    for it in ver_items:
        other = corpus["024c10" if it.filters.sw_version == "V600R025C00" else "025c00"]
        q = re.sub(r"v600r(?:024c10|025c00|024|025)", "", it.question, flags=re.IGNORECASE)
        absent = [w for w in _content_words(q) if w.lower() not in other]
        levels[it.qid] = "区域级差异" if not absent else "内容级差异"
    return levels


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--golden", default="data/golden/s3_full.yaml")
    ap.add_argument("--k", type=int, default=5)
    ap.add_argument("--skip-rerank", action="store_true")
    ap.add_argument("--recall-n", type=int, default=20)
    ap.add_argument("--rrf-k", type=int, default=60)
    ap.add_argument("--date", default=None, help="报告文件名日期覆盖")
    ap.add_argument("--out", default=None, help="报告输出路径覆盖")
    args = ap.parse_args()

    items = load_golden(Path(args.golden))
    client = get_milvus()
    wait_healthy(client)
    embedder = BGEM3Embedder(Settings.from_env().embed_model)
    k = args.k

    # 期望子块全文（naive 重叠判据）+ parent_id（parent 判据）；分批查询
    exp_ids = sorted({cid for it in items for cid in it.expected_chunk_ids})
    exp_texts: dict[str, str] = {}
    exp_parent: dict[str, str] = {}
    for i in range(0, len(exp_ids), 64):
        flt = "chunk_id in [" + ", ".join(f'"{c}"' for c in exp_ids[i:i + 64]) + "]"
        for r in client.query("chunks", filter=flt,
                              output_fields=["chunk_id", "text", "parent_id"], limit=64):
            exp_texts[r["chunk_id"]] = r["text"]
            exp_parent[r["chunk_id"]] = r["parent_id"]

    # naive 索引已 18,946 行：query 上限 16384，改用 query_iterator 全量拉取
    naive_texts: dict[str, set[str]] = {}
    it = client.query_iterator("chunks_naive", filter='text != ""',
                               output_fields=["chunk_id", "text"], batchSize=4000)
    while True:
        batch = it.next()
        if not batch:
            break
        for r in batch:
            naive_texts[r["chunk_id"]] = _content_tokens(r["text"])
    it.close()
    print(f"golden {len(items)} items; naive corpus {len(naive_texts)} chunk texts loaded", flush=True)

    def hybrid(paths=("dense", "bm25", "sparse"), reranker=None):
        return HybridRetriever(client, embedder, reranker=reranker, paths=paths,
                               recall_n=args.recall_n, rrf_k=args.rrf_k)

    ver_items = [it for it in items if it.filters]
    non_reject = [it for it in items if it.qtype != "reject"]

    # ---- 三配置矩阵 ----
    configs = [("naive", None), ("hybrid(dense+bm25+sparse)", hybrid()),
               ("hybrid(+rerank)", hybrid(reranker=BgeReranker(Settings.from_env().rerank_model)))]
    if args.skip_rerank:
        configs = configs[:2]
    results: dict[str, dict] = {}
    misses_3way: list = []
    for name, ret in configs:
        print(f"== {name}（k={k}） ==", flush=True)
        use_naive = name == "naive"
        if use_naive:
            ret = NaiveRetriever(client, embedder)
        accs, misses = _eval_once(ret, items, k, exp_texts, exp_parent,
                                  naive_texts if use_naive else None,
                                  collect_misses=(name == "hybrid(dense+bm25+sparse)"))
        accs["ALL"] = _subset_accs(accs, [q for q in QTYPES if q != "reject"])
        results[name] = accs
        if name == "hybrid(dense+bm25+sparse)":
            misses_3way = misses
        for qt in QTYPES + ("ALL",):
            a = accs.get(qt)
            if a and a.n:
                if qt == "reject":
                    m = a.row(k)
                    print(f"  {qt}: RejectPass@{k}={m[f'RejectPass@{k}']:.3f} "
                          f"RejectPassOverlap@{k}={m[f'RejectPassOverlap@{k}']:.3f}", flush=True)
                else:
                    print(f"  {qt}: " + " ".join(f"{mm}={v:.3f}" for mm, v in a.row(k).items()), flush=True)

    # ---- 版本 filter 子集（filters 对两个检索器同等应用）+ hybrid 无 filter 诊断 ----
    print(f"== 版本 filter 子集（{len(ver_items)} 条） ==", flush=True)
    ver_rows: dict[str, str] = {}
    if ver_items:
        vm, _ = _eval_once(hybrid(), ver_items, k, exp_texts, exp_parent, None)
        vn, _ = _eval_once(NaiveRetriever(client, embedder), ver_items, k,
                           exp_texts, exp_parent, naive_texts)
        a_vm, a_vn = _subset_accs(vm, ("factual",)), _subset_accs(vn, ("factual",))
        ver_rows["hybrid(+filter) Recall@k [chunk-id]"] = f"{a_vm.row(k)[f'Recall@{k}']:.3f}"
        ver_rows["hybrid(+filter) DocRecall@k [doc]"] = f"{a_vm.row(k)[f'DocRecall@{k}']:.3f}"
        ver_rows["naive(+filter) Recall@k [文本重叠]"] = f"{a_vn.row(k)[f'Recall@{k}']:.3f}"
        ver_rows["naive(+filter) DocRecall@k [doc]"] = f"{a_vn.row(k)[f'DocRecall@{k}']:.3f}"
        acc_nf, _ = _eval_once(hybrid(), [replace(it, filters=None) for it in ver_items],
                               k, exp_texts, exp_parent, None)
        a_nf = _subset_accs(acc_nf, ("factual",))
        ver_rows["hybrid(无filter,诊断) Recall@k [chunk-id]"] = f"{a_nf.row(k)[f'Recall@{k}']:.3f}"
        ver_rows["hybrid(无filter,诊断) DocRecall@k [doc]"] = f"{a_nf.row(k)[f'DocRecall@{k}']:.3f}"
        for key, val in ver_rows.items():
            print(f"  {key} = {val}", flush=True)

    # ---- 版本题分级（区域级 vs 内容级，脚本按题干实义词在对方版本全语料命中率判定） ----
    ver_levels: dict[str, str] = classify_version_items(ver_items)

    # ---- 汇总表 ----
    rows: dict[str, str] = {}
    cfg_label = {"naive": "naive",
                 "hybrid(dense+bm25+sparse)": "hybrid 三路",
                 "hybrid(+rerank)": "hybrid 三路+rerank"}
    for name, _ in configs:
        accs = results[name]
        lab = cfg_label[name]
        for qt in ("ALL",) + QTYPES:
            a = accs.get(qt)
            if not a or not a.n:
                continue
            m = a.row(k)
            suffix = {"ALL": "全题(非reject)", "factual": "factual", "troubleshoot": "troubleshoot",
                      "multihop": "multihop", "reject": "reject"}[qt]
            if qt == "reject":
                rows[f"{lab} {suffix} RejectPass@{k} [正确未命中|标记词]"] = f"{m[f'RejectPass@{k}']:.3f}"
                rows[f"{lab} {suffix} RejectPass@{k} [正确未命中|内容重叠≥{OVERLAP_FALSE_HIT_WORDS}词]"] = \
                    f"{m[f'RejectPassOverlap@{k}']:.3f}"
            else:
                extra = " parent=—" if name == "naive" else f" parent={m[f'ParentRecall@{k}']:.3f}"
                if f"AnyHit@{k}" in m:
                    extra += f" any={m[f'AnyHit@{k}']:.3f}"
                rows[f"{lab} {suffix} n={a.n}"] = (
                    f"R@{k}={m[f'Recall@{k}']:.3f} doc={m[f'DocRecall@{k}']:.3f}{extra}")
    for key, val in ver_rows.items():
        rows[f"版本子集 {key}"] = val.replace("@k", f"@{k}")

    # ---- 报告正文 ----
    body = f"""
## 参数与口径

- 参数：recall_n={args.recall_n}，rrf_k={args.rrf_k}，top_k={k}；golden：{args.golden}（{len(items)} 条 =
  factual {sum(1 for i in items if i.qtype == 'factual')}（含版本 filter {len(ver_items)}）/
  troubleshoot {sum(1 for i in items if i.qtype == 'troubleshoot')} /
  multihop {sum(1 for i in items if i.qtype == 'multihop')} /
  reject {sum(1 for i in items if i.qtype == 'reject')}）；语料：PDF v1 全量
  （hybrid chunks 43,950 行 = 12,243 父 + 31,707 子；naive chunks_naive 18,946 行）
- 判据：[chunk-id]=命中精确等于期望子块 id（multihop 只认 primary，即"首条命中"；naive 因 id
  空间不同退化为文本重叠>={OVERLAP_THRESHOLD}，先验阈值未调优）；[any]=任一期望子块进入 top-{k}
  （仅 multihop 单列）；[parent]=任一 top-{k} 命中的 parent_id 等于期望（primary）子块的
  parent_id（naive 无 parent 字段不适用）；[doc]=任一 top-{k} 命中 doc_id 属于期望文档
- **reject 口径（两层，均可证伪）**：期望命中=空；"正确未命中"（RejectPass@{k}）要求 top-{k}
  所有命中既不触发第一层也不触发第二层。第一层 [标记词] = 命中 text/breadcrumb 不含主题标记词
  （生成前经全语料 grep 验证 0 命中，故正常情况下恒通过，仅作回归护栏）：
  {"；".join(f"{p} → {ms}" for p, ms in REJECT_MARKERS.items())}。
  第二层 [内容重叠] = 命中 text 与题干实义词（ASCII 术语 + 中文 2-gram，去停用词）交集
  <{OVERLAP_FALSE_HIT_WORDS} 个；该层可真实触发失败（语料偶现"容器/镜像"等词即误杀），是更严的
  行为口径——若 RejectPassOverlap < 1.000 为真实信号，本任务不调参
- filters 对 naive 与 hybrid 同等应用（spec 口径）；hybrid 无 filter 行仅为诊断，不作主结果
- **本任务只测量，不做调参**（调参属 T6）

## 主结果

见上方汇总表：三配置（naive / hybrid 三路 / hybrid 三路+rerank）× 全题与分 qtype。
naive 无 parent 字段，其行 parent 列记 "—"（不适用）。

## 版本 filter 子集（{len(ver_items)} 条，均在 factual）

""" + ("\n".join(f"- {key} = {val}" for key, val in ver_rows.items()) if ver_rows else "- 无版本 filter 题") + f"""

### 版本子集构成（脚本自动分级）

分级口径：题干实义词（ASCII 术语 + 中文 2-gram 去停用词）全部出现在对方版本全语料 →
**区域级差异**（期望 chunk 位于版本独有区域——见生成台账核验，但答案内容两版本均出现，
该题同时考过滤机制而非版本独有事实）；否则 → **内容级差异**（题干含对方版本不存在的事实词）。

""" + ("\n".join(
        f"- {lv}（{sum(1 for v in ver_levels.values() if v == lv)} 条）："
        + "；".join(q for q, v in ver_levels.items() if v == lv)
        for lv in ("区域级差异", "内容级差异") if any(v == lv for v in ver_levels.values()))
        or "- 无") + f"""

## 未命中样例（hybrid 三路，chunk-id|首条判据 + reject 误命中，前 {min(15, len(misses_3way))} 条）

""" + ("\n".join(
        f"- `{it.qid}`（{it.qtype}{'，' + tag if tag else ''}，期望 {','.join(i.split('#')[-1] for i in it.expected_chunk_ids[:2]) or '空'}）"
        f"{it.question} → top{min(3, len(ids))}: {[i.split('#')[-1] for i in ids]}"
        for it, ids, tag in misses_3way[:15]) or "- 无") + """

## 说明

- reject 题无期望文档，不计入全题 chunk/doc 指标；multihop 的 chunk 行即"首条命中"，any 行为"任一命中"
- 本报告全部数字由本脚本单次运行产出（MEASURE ONLY）；hybrid 相对 naive 的差距是 T9 路由前的已知状态，
  原因分析见 S2 报告（BM25 中文错配/RRF 弱路稀释），此处不展开
"""

    out = args.out or f"docs/eval-reports/{args.date or date.today().isoformat()}-s3-retrieval.md"
    write_report(Path(out), title="S3 快版检索评测（200 条四类分层 golden set，PDF v1 语料）",
                 summary_rows=rows, body_md=body)


if __name__ == "__main__":
    main()
