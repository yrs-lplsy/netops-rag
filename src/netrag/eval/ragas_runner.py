"""RAGAS 四指标评测接入：faithfulness / answer_relevancy / context_precision / context_recall。

接线说明（ragas 0.3.1）：
- judge LLM：Settings.llm_model（SiliconFlow OpenAI 兼容端点）包成 LangchainLLMWrapper；
- 嵌入：本地 bge-m3（dense）包成 langchain Embeddings，供 ResponseRelevancy 的
  问题生成相似度打分，不触网、不重下载；
- 数据组装：检索 top-k → answer_with_citations（父块窗口）→ SingleTurnSample 行
  （question/answer/contexts/ground_truth）；ground_truth = 期望子块全文从 Milvus
  点查拼回，期望子块缺失的条目跳过并计数，绝不造数；
- 单条失败（检索/生成异常）单独计入 errors，不中断整体；ragas evaluate 显式
  raise_exceptions=False（0.3.1 默认即 False，显式写出走读可见）。

依赖约束：ragas 0.3.x 与 langchain 1.x 不兼容（ragas 引用
langchain_community.chat_models.vertexai，0.4 里已删），故 langchain 全家钉在
0.3.x（见 pyproject）。
"""

import json
import re
from pathlib import Path

import ragas
from langchain_core.embeddings import Embeddings

from netrag.config import Settings
from netrag.eval.golden import GoldenItem
from netrag.retrieval.base import RetrievedChunk


# 评测侧伪影（eval-design §7 归因表 + Run C caveats 的定量实证）：
# ①【出处】脚注块——生成答案末尾的引用列表，faithfulness 陈述拆分恒计为"无据句"
#   （hw-…-alarm-01-67#c15 的 0.333=1/3 即 2 条脚注行所致）；
# ②逃生舱句——prompt 要求对片段未覆盖内容显式标注"（手册片段未涉及，建议人工确认）"，
#   该句同样被计为无据陈述，且与 relevancy 塌 0 强关联（Run C 两条 0.854/0.967→0）。
# 两者都是评分口径伪影而非语义缺陷，判前剥离；原始答案仍入缓存/记录可审计。
_FOOTER_MARK = "【出处】"
_ESCAPE_HATCH = "（手册片段未涉及，建议人工确认）"
# 逃生舱句：从上一句界（。！？；或换行）之后到标记及其句末标点的整句
_ESCAPE_SENT_RE = re.compile(r"[^。！？；\n]*" + re.escape(_ESCAPE_HATCH) + r"[。！？；]?")


def strip_eval_artifacts(answer: str) -> str:
    """剥离答案中的评测伪影：【出处】脚注块（该行至末尾）与逃生舱句，返回供 judge 打分的文本。

    纯函数、幂等；正常内容句不受影响。脚注块整体删除（含其后所有引用行）；
    逃生舱句按句删除（含句内标记前的前缀与句末标点）。两步都不改写保留内容。
    """
    lines = answer.splitlines()
    for i, ln in enumerate(lines):
        if ln.lstrip().startswith(_FOOTER_MARK):
            lines = lines[:i]
            break
    text = "\n".join(lines)
    text = _ESCAPE_SENT_RE.sub("", text)
    return text.rstrip()  # 脚注/句剥离残留的行尾空白一并去掉，保留内容不被改写


class Bgem3LangchainEmbeddings(Embeddings):
    """BGEM3Embedder → langchain Embeddings（只用 dense；sparse 通路 ragas 用不上）。

    懒加载：构造时不触 GPU 模型，首次 embed 才加载本地缓存快照。
    ragas 按 isinstance(LangchainEmbeddings) 识别，必须真继承 langchain Embeddings。
    """

    def __init__(self, model_name: str, embedder=None) -> None:
        self._model_name = model_name
        self._embedder = embedder

    def _get_embedder(self):
        if self._embedder is None:
            from netrag.embedding.bge_m3 import BGEM3Embedder

            self._embedder = BGEM3Embedder(self._model_name)
        return self._embedder

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []
        out = self._get_embedder().embed_documents(list(texts))
        return [[float(v) for v in vec] for vec in out.dense]

    def embed_query(self, text: str) -> list[float]:
        out = self._get_embedder().embed_query(text)
        return [float(v) for v in out.dense[0]]


def build_judge_llm(settings: Settings, backend: str = "siliconflow"):
    """Settings → ChatOpenAI(temperature=0) → LangchainLLMWrapper。

    backend="siliconflow"：保持 T6 基线行为（Settings.llm_model，SF OpenAI 兼容端点）；
    backend="deepseek"：DEEPSEEK_* env（OpenAI 兼容端点 https://api.deepseek.com），
    模型名只来自 env（不硬编码），缺失 key/模型名时报错并指路对应 env 变量。
    """
    from langchain_openai import ChatOpenAI
    from ragas.llms import LangchainLLMWrapper

    if backend == "siliconflow":
        if not settings.sf_api_key:
            raise ValueError("SILICONFLOW_API_KEY 未配置，无法构造 judge LLM")
        model, api_key, base_url = settings.llm_model, settings.sf_api_key, settings.sf_base_url
    elif backend == "deepseek":
        if not settings.deepseek_api_key:
            raise ValueError("judge 后端 deepseek 需要 DEEPSEEK_API_KEY（.env 中配置后重试）")
        if not settings.deepseek_model:
            raise ValueError("judge 后端 deepseek 需要 DEEPSEEK_MODEL（.env 中设模型名后重试，"
                             "代码不设默认模型防硬编码漂移）")
        model, api_key, base_url = (settings.deepseek_model, settings.deepseek_api_key,
                                    settings.deepseek_base_url)
    else:
        raise ValueError(f"未知 judge backend：{backend!r}（可选 siliconflow / deepseek）")
    chat = ChatOpenAI(model=model, api_key=api_key, base_url=base_url, temperature=0)
    return LangchainLLMWrapper(chat)


def fetch_chunk_texts(client, chunk_ids: list[str], batch: int = 64) -> dict[str, str]:
    """按 chunk_id 批量点查 chunks 集合，返回 {chunk_id: text}（缺失 id 不在结果里）。"""
    from netrag.index.hybrid_schema import CHUNKS

    out: dict[str, str] = {}
    ids = sorted(set(chunk_ids))
    for i in range(0, len(ids), batch):
        flt = "chunk_id in [" + ", ".join(f'"{c}"' for c in ids[i:i + batch]) + "]"
        for r in client.query(CHUNKS, filter=flt,
                              output_fields=["chunk_id", "text"], limit=batch):
            out[r["chunk_id"]] = r["text"]
    return out


def _assemble_contexts(chunks: list[RetrievedChunk], assembly: str) -> list[str]:
    """RAGAS contexts 装配：child-chunks（子块文本，T6 口径）| parent-window（生成可见）。"""
    if assembly == "parent-window":
        from netrag.generation.answer import build_generation_contexts

        return build_generation_contexts(chunks)
    return [c.text for c in chunks]


def run_ragas(items: list[GoldenItem], retriever, llm_client,
              judge_llm=None, embeddings=None, k: int = 5,
              progress_every: int = 5, run_config=None,
              gen_cache_path: Path | None = None, cache_key: str = "",
              assembly: str = "child-chunks") -> dict:
    """跑通 检索→生成→RAGAS 四指标，返回 per_item / means / n / skipped / cache_hits。

    - ground truth：期望子块全文（Milvus 点查）按 expected_chunk_ids 顺序拼接；
      任一期望子块缺失或条目本无期望子块（如 reject）→ 跳过并计数；
    - assembly：RAGAS contexts 装配口径。默认 "child-chunks"（检索命中子块文本，
      T6 基线口径）；"parent-window" 经 answer.build_generation_contexts 取父块窗口
      ——与生成 LLM 实际可见片段严格一致（T6 验证序列 Run B 的装配修正）；其他值
      ValueError；
    - 检索/生成异常：计入 errors（含 repr），不中断整体；
    - means：df 列均值（NaN 自动忽略）；per_item 单值 NaN 记 None；
    - gen_cache_path（可选）：生成结果落盘缓存，key 不匹配即失效；命中条目跳过生成 LLM
      只重跑 judge——judge 阶段（402/进程被杀）中断后可低成本续跑；支持部分命中（缺失
      条目只补生成）。检索照常执行：contexts 按当前装配由 fresh 检索重建，缓存中的
      retrieved_contexts（child 文本）仅作逐字节确定性校验基准，不一致判前响亮失败。
      返回 cache_hits = 命中缓存跳过生成的条数。
    """
    from ragas import EvaluationDataset
    from ragas.metrics import ContextPrecision, ContextRecall, Faithfulness, ResponseRelevancy

    if judge_llm is None or embeddings is None:
        raise ValueError("judge_llm 与 embeddings 必须显式传入（避免 ragas 回落 OpenAI 默认）")
    if assembly not in ("child-chunks", "parent-window"):
        raise ValueError(f"未知 assembly 口径：{assembly!r}（可选 child-chunks / parent-window）")
    client = getattr(retriever, "_client", None)
    if client is None:
        raise ValueError("retriever 需持有 _client（Milvus）用于点查期望子块文本作为 ground truth")

    gt = fetch_chunk_texts(client, [cid for it in items for cid in it.expected_chunk_ids])

    def _skip_reason(it: GoldenItem) -> str | None:
        if not it.expected_chunk_ids:
            return "无期望子块（无 ground truth）"
        missing = [cid for cid in it.expected_chunk_ids if cid not in gt]
        if missing:
            return f"期望子块缺失 {len(missing)}/{len(it.expected_chunk_ids)}"
        return None

    skip_reasons: dict[str, str] = {}
    eligible: list[GoldenItem] = []
    for it in items:
        reason = _skip_reason(it)
        if reason:
            skip_reasons[it.qid] = reason
        else:
            eligible.append(it)
    skipped_detail: list[tuple[str, str]] = list(skip_reasons.items())

    # 生成缓存：命中条目跳过生成 LLM（key 校验）；检索仍执行——contexts 按当前装配由
    # fresh 检索重建（缓存里的 retrieved_contexts 是 child 文本，仅作确定性校验基准：
    # 与 fresh 检索逐字节比对，不一致说明"同抽样同生成"前提被破坏，判前响亮失败），
    # 部分命中（如 T6 有 1 条 429 未入缓存）只补生成缺失条目
    cached_rows: dict[str, dict] = {}
    if gen_cache_path is not None and eligible and gen_cache_path.exists():
        try:
            data = json.loads(gen_cache_path.read_text(encoding="utf-8"))
            if data.get("key") == cache_key:
                eligible_qids = {it.qid for it in eligible}
                cached_rows = {r["qid"]: r for r in data.get("rows", [])
                               if r["qid"] in eligible_qids}
                if cached_rows:
                    print(f"[ragas-run] 生成缓存命中 {len(cached_rows)}/{len(eligible)} 条"
                          f"（{gen_cache_path}），命中条目跳过生成 LLM（检索照常重建 contexts）",
                          flush=True)
        except Exception as exc:  # noqa: BLE001 — 缓存坏了当没有，走重新生成
            print(f"[ragas-run] 生成缓存读取失败（忽略，重新生成）：{exc!r}", flush=True)

    errors: list[tuple[str, str]] = []
    evaluated: list[tuple[GoldenItem, dict]] = []
    dataset_rows: list[dict] = []  # judge 可见行（response 已剥离伪影）
    child_texts_by_qid: dict[str, list[str]] = {}  # 缓存持久化用：原始 child 文本（校验基准）
    cache_hits = 0
    ctx_mismatch: list[tuple[str, list[str], list[str]]] = []
    total = len(items)
    for i, it in enumerate(items, start=1):
        if it.qid in skip_reasons:
            continue
        cached = cached_rows.get(it.qid)
        try:
            chunks: list[RetrievedChunk] = retriever.retrieve(it.question, top_k=k, filters=it.filters)
            fresh_child = [c.text for c in chunks]
            child_texts_by_qid[it.qid] = fresh_child
            if cached is None:
                from netrag.generation.answer import answer_with_citations

                answer = answer_with_citations(it.question, chunks, llm_client)
                response = answer.text
            else:
                # 检索确定性校验：fresh child 文本必须与缓存（恒为 child 文本）逐字节一致
                if fresh_child != list(cached["retrieved_contexts"]):
                    ctx_mismatch.append((it.qid, fresh_child, list(cached["retrieved_contexts"])))
                response = cached["response"]
                cache_hits += 1
        except Exception as e:  # 单条失败不拖垮整体，如实计数
            errors.append((it.qid, repr(e)))
            print(f"[ragas-run] 生成失败 {it.qid}: {e!r}", flush=True)  # 402 等余额故障要能实时看见
            continue
        row = {
            "user_input": it.question,
            "response": response,  # 原始答案：进缓存与 per_item 记录（可审计/可换剥离规则重评）
            "retrieved_contexts": _assemble_contexts(chunks, assembly),
            "reference": "\n\n".join(gt[cid] for cid in it.expected_chunk_ids),
        }
        # 判前剥离评分伪影（【出处】脚注块 + 逃生舱句）：只影响 judge 可见的 response，
        # 不回写 row/缓存（评审归因：脚注行恒判无据句，Run C 定量实证 0.333=1/3）
        dataset_rows.append({**row, "response": strip_eval_artifacts(response)})
        evaluated.append((it, row))
        if progress_every and (len(evaluated) % progress_every == 0 or i == total):
            print(f"[ragas-run] {len(evaluated)}/{total} 条已就绪（{it.qid}）", flush=True)
    if ctx_mismatch:  # 判前失败：judge 还没花钱，先修检索确定性
        parts = []
        for qid, fresh, old in ctx_mismatch:
            first_diff = next((a for a, b in zip(fresh, old) if a != b), "?")
            parts.append(f"{qid}（fresh {len(fresh)}条 vs cached {len(old)}条，首条差={first_diff!r}）")
        raise RuntimeError(
            f"生成缓存一致性校验失败 {len(ctx_mismatch)} 条：fresh 检索 child 文本与缓存不一致，"
            f"同抽样同生成前提被破坏，拒绝继续 judge。{'；'.join(parts)}")
    if gen_cache_path is not None and evaluated:
        try:  # 生成落盘：judge 阶段（402/被杀）中断后重跑只花 judge 的钱。
            # retrieved_contexts 恒存原始 child 文本（检索确定性校验基准，装配无关）——
            # 评审 Fix Round 1 Finding 2：装配后文本入缓存会让未来重跑字节校验必然失败
            gen_cache_path.parent.mkdir(parents=True, exist_ok=True)
            gen_cache_path.write_text(json.dumps(
                {"key": cache_key,
                 "rows": [{"qid": it.qid, "user_input": row["user_input"],
                           "response": row["response"],
                           "retrieved_contexts": child_texts_by_qid[it.qid]}
                          for it, row in evaluated]},
                ensure_ascii=False), encoding="utf-8")
            print(f"[ragas-run] 生成结果已缓存 → {gen_cache_path}", flush=True)
        except Exception as exc:  # noqa: BLE001 — 缓存失败不影响评测本身
            print(f"[ragas-run] 生成缓存写入失败（忽略）：{exc!r}", flush=True)

    if not evaluated:
        return {"per_item": [], "means": {}, "n": 0, "cache_hits": cache_hits,
                "skipped": len(skipped_detail), "skipped_detail": skipped_detail,
                "errors": errors}

    dataset = EvaluationDataset.from_list(dataset_rows)
    metrics = [Faithfulness(), ResponseRelevancy(), ContextPrecision(), ContextRecall()]
    # 经模块属性调用（非 from-import 绑定）：单测 monkeypatch ragas.evaluate 可生效
    result = ragas.evaluate(dataset, metrics=metrics, llm=judge_llm, embeddings=embeddings,
                            raise_exceptions=False, run_config=run_config)
    df = result.to_pandas()

    import pandas as pd

    # 行数护栏（评审 Fix Round 1）：pyproject 允许 ragas 小版本漂移，未来版本若重排/丢行，
    # 逐行 zip 会把分数错配到错误 qid——宁肯响亮失败也不静默错配
    if len(df) != len(evaluated):
        raise RuntimeError(
            f"ragas 返回行数 {len(df)} 与评测条目数 {len(evaluated)} 不一致，"
            "拒绝逐行对齐（防止分数错配到错误 qid）")
    metric_names = [m.name for m in metrics]
    per_item = []
    for (it, row), (_, drow) in zip(evaluated, df.iterrows()):
        rec: dict = {"qid": it.qid, "qtype": it.qtype}
        for m in metric_names:
            v = drow.get(m)
            rec[m] = None if v is None or pd.isna(v) else float(v)
        # 双长度记录：原始/剥离后答案长度（伪影剥离口径的审计面）
        raw = row["response"]
        rec["raw_len"] = len(raw)
        rec["stripped_len"] = len(strip_eval_artifacts(raw))
        per_item.append(rec)
    means = {}
    for m in metric_names:
        if m in df.columns:
            col = pd.to_numeric(df[m], errors="coerce").dropna()
            means[m] = float(col.mean()) if len(col) else None
    return {"per_item": per_item, "means": means, "n": len(evaluated),
            "cache_hits": cache_hits,
            "skipped": len(skipped_detail), "skipped_detail": skipped_detail,
            "errors": errors}
