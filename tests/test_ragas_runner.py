"""RAGAS runner 单测：只测数据组装 / 封装接线 / 跳过与错误计数，不触真实 ragas evaluate。

真 LLM、真 Milvus、真 GPU 模型一律用 stub 替代；ragas.evaluate 被 monkeypatch，
ragas 内部（指标实现/prompt）只在 Part D 真实运行中覆盖。
"""

import json
import math
import re

import pandas as pd
import pytest

import ragas

from netrag.config import Settings
from netrag.embedding.base import EmbeddingOutput
from netrag.eval.golden import GoldenItem
from netrag.eval.ragas_runner import (
    Bgem3LangchainEmbeddings,
    build_judge_llm,
    fetch_chunk_texts,
    run_ragas,
)
from netrag.retrieval.base import MetadataFilter, RetrievedChunk


# ---------- stubs ----------


class StubEmbedder:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def embed_documents(self, texts: list[str]) -> EmbeddingOutput:
        self.calls.append(list(texts))
        return EmbeddingOutput(dense=[[1.0, 2.0]] * len(texts))

    def embed_query(self, text: str) -> EmbeddingOutput:
        return EmbeddingOutput(dense=[[3.0, 4.0]])


class FakeClient:
    """query(filter='chunk_id in ["a", ...]') → 返回已知行，模拟 Milvus 点查。"""

    def __init__(self, rows: list[dict]) -> None:
        self._rows = {r["chunk_id"]: r for r in rows}
        self.queries: list[tuple] = []

    def query(self, collection, filter=None, output_fields=None, limit=None):
        self.queries.append((collection, filter))
        ids = re.findall(r'"([^"]+)"', filter or "")
        return [dict(self._rows[i]) for i in ids if i in self._rows]


class FakeRetriever:
    name = "fake"

    def __init__(self, client) -> None:
        self._client = client
        self.calls: list[tuple] = []

    def retrieve(self, query, top_k=5, filters=None):
        self.calls.append((query, top_k, filters))
        return [
            RetrievedChunk(
                chunk_id=f"c{i}", text=f"hit{i}-{query}", score=1.0 / (i + 1),
                doc_id="d1", breadcrumb="面包屑", vendor="v", model="m", sw_version="s",
            )
            for i in range(top_k)
        ]


class FakeLLM:
    def __init__(self) -> None:
        self.calls: list[list[dict]] = []

    def chat(self, messages, temperature=0.2, max_tokens=2048):
        self.calls.append(messages)
        return "生成答案"


class FakeResult:
    def __init__(self, df: pd.DataFrame) -> None:
        self._df = df

    def to_pandas(self) -> pd.DataFrame:
        return self._df


def _mk_item(qid: str, chunk_ids: list[str], qtype: str = "factual",
             filters: MetadataFilter | None = None) -> GoldenItem:
    return GoldenItem(qid=qid, question=f"问题{qid}", qtype=qtype,
                      expected_doc_ids=["d1"], expected_chunk_ids=chunk_ids, filters=filters)


def _install_fake_evaluate(monkeypatch, captured: dict, df: pd.DataFrame):
    def fake_evaluate(dataset, metrics=None, llm=None, embeddings=None, **kw):
        captured["rows"] = [s.model_dump() for s in dataset]
        captured["metric_names"] = [m.name for m in (metrics or [])]
        captured["llm"] = llm
        captured["embeddings"] = embeddings
        captured["kw"] = kw
        return FakeResult(df)

    monkeypatch.setattr(ragas, "evaluate", fake_evaluate)


# ---------- tests ----------


def test_bgem3_wrapper_lazy_dense_only():
    w = Bgem3LangchainEmbeddings("BAAI/bge-m3")  # 未注入 embedder → 懒加载，构造不触模型
    assert w._embedder is None
    stub = StubEmbedder()
    w2 = Bgem3LangchainEmbeddings("BAAI/bge-m3", embedder=stub)
    docs = w2.embed_documents(["a", "b"])
    assert docs == [[1.0, 2.0], [1.0, 2.0]]
    assert stub.calls == [["a", "b"]]
    assert w2.embed_query("q") == [3.0, 4.0]


def test_bgem3_wrapper_is_langchain_embeddings():
    from langchain_core.embeddings import Embeddings as LCEmbeddings

    assert issubclass(Bgem3LangchainEmbeddings, LCEmbeddings)


def test_build_judge_llm_wraps_chatopenai():
    s = Settings(sf_api_key="sk-test", llm_model="Qwen/Qwen2.5-72B-Instruct",
                 sf_base_url="https://api.siliconflow.cn/v1")
    from ragas.llms import LangchainLLMWrapper

    w = build_judge_llm(s)
    assert isinstance(w, LangchainLLMWrapper)
    inner = w.langchain_llm
    assert inner.model_name == "Qwen/Qwen2.5-72B-Instruct"
    assert inner.temperature == 0
    assert inner.openai_api_base == "https://api.siliconflow.cn/v1"
    assert inner.openai_api_key.get_secret_value() == "sk-test"


def test_fetch_chunk_texts_dedup_and_batch():
    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"}])
    out = fetch_chunk_texts(client, ["g1", "g1", "g0"])  # g0 缺失
    assert out == {"g1": "期望文本1"}
    assert client.queries and client.queries[0][0] == "chunks"


def test_run_ragas_assembly_skip_and_means(monkeypatch):
    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"},
                         {"chunk_id": "g2", "text": "期望文本2"}])
    ret = FakeRetriever(client)
    llm = FakeLLM()
    items = [
        _mk_item("q1", ["g1"]),
        _mk_item("q2", ["g1", "g2"], qtype="troubleshoot"),
        _mk_item("q3", ["g-missing"]),  # 期望子块缺失 → skip
    ]
    captured: dict = {}
    df = pd.DataFrame({
        "user_input": ["问题q1", "问题q2"],
        "faithfulness": [0.9, 0.5],
        "answer_relevancy": [0.8, float("nan")],
        "context_precision": [1.0, 0.7],
        "context_recall": [1.0, 0.6],
    })
    _install_fake_evaluate(monkeypatch, captured, df)
    judge, emb = object(), object()
    out = run_ragas(items, ret, llm, judge_llm=judge, embeddings=emb, k=3, progress_every=1)

    assert captured["metric_names"] == ["faithfulness", "answer_relevancy",
                                        "context_precision", "context_recall"]
    assert captured["kw"]["raise_exceptions"] is False
    assert captured["llm"] is judge and captured["embeddings"] is emb

    rows = captured["rows"]
    assert len(rows) == 2  # q3 被 skip
    assert rows[0]["user_input"] == "问题q1"
    assert rows[0]["response"] == "生成答案"
    assert rows[0]["retrieved_contexts"] == ["hit0-问题q1", "hit1-问题q1", "hit2-问题q1"]
    assert rows[0]["reference"] == "期望文本1"
    assert rows[1]["reference"] == "期望文本1\n\n期望文本2"
    assert len(llm.calls) == 2  # 每个非 skip 条目一次生成

    assert ret.calls[0][1] == 3  # top_k 透传
    assert out["n"] == 2 and out["skipped"] == 1
    assert [p["qid"] for p in out["per_item"]] == ["q1", "q2"]
    assert math.isclose(out["means"]["faithfulness"], 0.7)
    assert math.isclose(out["means"]["answer_relevancy"], 0.8)  # NaN 不计入均值
    assert math.isclose(out["means"]["context_precision"], 0.85)
    assert out["per_item"][1]["answer_relevancy"] is None  # NaN → None
    assert any(s[0] == "q3" for s in out["skipped_detail"])


def test_run_ragas_passes_filters(monkeypatch):
    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"}])
    ret = FakeRetriever(client)
    captured: dict = {}
    df = pd.DataFrame({"user_input": ["问题q1"], "faithfulness": [1.0],
                       "answer_relevancy": [1.0], "context_precision": [1.0],
                       "context_recall": [1.0]})
    _install_fake_evaluate(monkeypatch, captured, df)
    f = MetadataFilter(sw_version="V600R025C00")
    run_ragas([_mk_item("q1", ["g1"], filters=f)], ret, FakeLLM(),
              judge_llm=object(), embeddings=object(), k=5, progress_every=0)
    assert ret.calls[0][2] is f


def test_run_ragas_item_error_counted_not_fatal(monkeypatch):
    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"}])
    ret = FakeRetriever(client)

    class FlakyRetriever(FakeRetriever):
        def retrieve(self, query, top_k=5, filters=None):
            if "q-boom" in query:
                raise RuntimeError("boom")
            return super().retrieve(query, top_k=top_k, filters=filters)

    captured: dict = {}
    df = pd.DataFrame({"user_input": ["问题q-ok"], "faithfulness": [0.9],
                       "answer_relevancy": [0.9], "context_precision": [0.9],
                       "context_recall": [0.9]})
    _install_fake_evaluate(monkeypatch, captured, df)
    items = [_mk_item("q-ok", ["g1"]), _mk_item("q-boom", ["g1"])]
    out = run_ragas(items, FlakyRetriever(client), FakeLLM(),
                    judge_llm=object(), embeddings=object(), k=5, progress_every=0)
    assert out["n"] == 1 and len(out["errors"]) == 1
    assert out["errors"][0][0] == "q-boom"
    assert out["means"]["faithfulness"] == 0.9


def test_run_ragas_row_count_mismatch_raises(monkeypatch):
    """ragas 返回行数与评测条目数不一致 → 必须响亮失败，拒绝 zip 错配（评审 Fix Round 1）。"""
    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"}])
    ret = FakeRetriever(client)
    captured: dict = {}
    # 只返回 1 行（实际评测 2 条）——模拟未来 ragas 版本重排/丢行
    df = pd.DataFrame({"user_input": ["问题q1"], "faithfulness": [0.9],
                       "answer_relevancy": [0.9], "context_precision": [0.9],
                       "context_recall": [0.9]})
    _install_fake_evaluate(monkeypatch, captured, df)
    items = [_mk_item("q1", ["g1"]), _mk_item("q2", ["g1"], qtype="troubleshoot")]
    with pytest.raises(RuntimeError, match="2"):
        run_ragas(items, ret, FakeLLM(), judge_llm=object(), embeddings=object(),
                  k=5, progress_every=0)


def test_run_ragas_requires_judge_and_embeddings():
    ret = FakeRetriever(FakeClient([]))
    with pytest.raises(ValueError):
        run_ragas([_mk_item("q1", ["g1"])], ret, FakeLLM())


def test_run_ragas_requires_milvus_client_on_retriever():
    class NoClient:
        name = "noclient"

        def retrieve(self, query, top_k=5, filters=None):
            return []

    with pytest.raises(ValueError):
        run_ragas([_mk_item("q1", ["g1"])], NoClient(), FakeLLM(),
                  judge_llm=object(), embeddings=object())


# ---------- judge 后端切换（DeepSeek OpenAI 兼容 / SiliconFlow）----------


def test_build_judge_llm_siliconflow_backend_explicit():
    s = Settings(sf_api_key="sk-test", llm_model="Qwen/Qwen2.5-72B-Instruct",
                 sf_base_url="https://api.siliconflow.cn/v1")
    w = build_judge_llm(s, backend="siliconflow")
    inner = w.langchain_llm
    assert inner.model_name == "Qwen/Qwen2.5-72B-Instruct"
    assert inner.temperature == 0
    assert inner.openai_api_base == "https://api.siliconflow.cn/v1"
    assert inner.openai_api_key.get_secret_value() == "sk-test"


def test_build_judge_llm_deepseek_backend_attrs():
    s = Settings(sf_api_key="", llm_model="Qwen/Qwen2.5-7B-Instruct",
                 deepseek_api_key="sk-ds-test", deepseek_model="deepseek-v4-flash",
                 deepseek_base_url="https://api.deepseek.com")
    w = build_judge_llm(s, backend="deepseek")
    inner = w.langchain_llm
    # 模型名只来自 Settings（env），不硬编码
    assert inner.model_name == "deepseek-v4-flash"
    assert inner.temperature == 0
    assert inner.openai_api_base == "https://api.deepseek.com"
    assert inner.openai_api_key.get_secret_value() == "sk-ds-test"


def test_build_judge_llm_deepseek_missing_key_tells_env_var():
    s = Settings(deepseek_api_key="", deepseek_model="deepseek-v4-flash")
    with pytest.raises(ValueError, match="DEEPSEEK_API_KEY"):
        build_judge_llm(s, backend="deepseek")


def test_build_judge_llm_deepseek_missing_model_tells_env_var():
    s = Settings(deepseek_api_key="sk-ds-test", deepseek_model="")
    with pytest.raises(ValueError, match="DEEPSEEK_MODEL"):
        build_judge_llm(s, backend="deepseek")


def test_build_judge_llm_unknown_backend_raises():
    with pytest.raises(ValueError, match="backend"):
        build_judge_llm(Settings(sf_api_key="sk-test"), backend="openai")


# ---------- 生成缓存：整跑跳生成、部分命中补生成、检索确定性校验 ----------


def _write_cache(path, key: str, rows: list[dict]) -> None:
    path.write_text(json.dumps({"key": key, "rows": rows}, ensure_ascii=False), encoding="utf-8")


def test_run_ragas_gen_cache_full_hit_skips_llm(monkeypatch, tmp_path):
    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"}])
    ret = FakeRetriever(client)
    llm = FakeLLM()
    cache = tmp_path / "gen.json"
    _write_cache(cache, "k1", [{"qid": "q1", "user_input": "问题q1", "response": "缓存答案",
                                "retrieved_contexts": ["hit0-问题q1", "hit1-问题q1"]}])
    captured: dict = {}
    df = pd.DataFrame({"user_input": ["问题q1"], "faithfulness": [0.9],
                       "answer_relevancy": [0.9], "context_precision": [0.9],
                       "context_recall": [0.9]})
    _install_fake_evaluate(monkeypatch, captured, df)
    out = run_ragas([_mk_item("q1", ["g1"])], ret, llm, judge_llm=object(),
                    embeddings=object(), k=2, progress_every=0,
                    gen_cache_path=cache, cache_key="k1")
    assert llm.calls == []  # 生成 LLM 一分钱不花
    assert captured["rows"][0]["response"] == "缓存答案"
    # contexts 由 fresh 检索按当前装配重建（不是从缓存读），child 文本与缓存逐字节一致
    assert captured["rows"][0]["retrieved_contexts"] == ["hit0-问题q1", "hit1-问题q1"]
    assert out["cache_hits"] == 1
    assert out["n"] == 1 and out["errors"] == []


def test_run_ragas_gen_cache_partial_hit_regenerates_missing(monkeypatch, tmp_path):
    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"}])
    ret = FakeRetriever(client)
    llm = FakeLLM()
    cache = tmp_path / "gen.json"
    _write_cache(cache, "k1", [{"qid": "q1", "user_input": "问题q1", "response": "缓存答案",
                                "retrieved_contexts": ["hit0-问题q1", "hit1-问题q1"]}])
    captured: dict = {}
    df = pd.DataFrame({"user_input": ["问题q1", "问题q2"], "faithfulness": [0.9, 0.8],
                       "answer_relevancy": [0.9, 0.8], "context_precision": [0.9, 0.8],
                       "context_recall": [0.9, 0.8]})
    _install_fake_evaluate(monkeypatch, captured, df)
    items = [_mk_item("q1", ["g1"]), _mk_item("q2", ["g1"], qtype="troubleshoot")]
    out = run_ragas(items, ret, llm, judge_llm=object(), embeddings=object(),
                    k=2, progress_every=0, gen_cache_path=cache, cache_key="k1")
    assert len(llm.calls) == 1  # 只补生成缓存缺失的 q2
    assert out["cache_hits"] == 1
    assert [p["qid"] for p in out["per_item"]] == ["q1", "q2"]
    rows = {r["qid"]: r for r in json.loads(cache.read_text(encoding="utf-8"))["rows"]}
    assert rows["q1"]["response"] == "缓存答案" and rows["q2"]["response"] == "生成答案"


def test_run_ragas_gen_cache_key_mismatch_regenerates_all(monkeypatch, tmp_path):
    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"}])
    ret = FakeRetriever(client)
    llm = FakeLLM()
    cache = tmp_path / "gen.json"
    _write_cache(cache, "other-key", [{"qid": "q1", "user_input": "问题q1",
                                       "response": "旧key答案", "retrieved_contexts": []}])
    captured: dict = {}
    df = pd.DataFrame({"user_input": ["问题q1"], "faithfulness": [0.9],
                       "answer_relevancy": [0.9], "context_precision": [0.9],
                       "context_recall": [0.9]})
    _install_fake_evaluate(monkeypatch, captured, df)
    run_ragas([_mk_item("q1", ["g1"])], ret, llm, judge_llm=object(), embeddings=object(),
              k=2, progress_every=0, gen_cache_path=cache, cache_key="k1")
    assert len(llm.calls) == 1
    assert captured["rows"][0]["response"] == "生成答案"
    assert captured["rows"][0]["retrieved_contexts"] == ["hit0-问题q1", "hit1-问题q1"]


def test_run_ragas_aborts_before_judge_on_cache_context_mismatch(monkeypatch, tmp_path):
    """fresh 检索的 child 文本与缓存记录逐字节不一致 → 判定前响亮失败（同抽样同生成前提被破坏）。"""
    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"}])
    ret = FakeRetriever(client)
    llm = FakeLLM()
    cache = tmp_path / "gen.json"
    _write_cache(cache, "k1", [{"qid": "q1", "user_input": "问题q1", "response": "缓存答案",
                                "retrieved_contexts": ["语料变了之后的文本"]}])
    captured: dict = {}
    df = pd.DataFrame({"user_input": ["问题q1"], "faithfulness": [0.9],
                       "answer_relevancy": [0.9], "context_precision": [0.9],
                       "context_recall": [0.9]})
    _install_fake_evaluate(monkeypatch, captured, df)
    with pytest.raises(RuntimeError, match="q1"):
        run_ragas([_mk_item("q1", ["g1"])], ret, llm, judge_llm=object(),
                  embeddings=object(), k=2, progress_every=0,
                  gen_cache_path=cache, cache_key="k1")
    assert "rows" not in captured  # judge（ragas.evaluate）一次都没跑，不烧钱


# ---------- 装配口径：parent-window（Run B）与生成可见严格一致 ----------


def test_run_ragas_parent_window_assembly_matches_generation_bodies(monkeypatch):
    """assembly=parent-window：contexts 必须与 answer_with_citations 喂给 LLM 的正文逐字节一致。"""
    from netrag.generation.answer import _parent_window, build_generation_contexts

    parent = "前提说明。" * 300  # 长父块，保证开窗非平凡
    child = parent[500:600]

    class ParentRetriever(FakeRetriever):
        def retrieve(self, query, top_k=5, filters=None):
            return [_chunk_with_parent(f"hit{i}-{query}", parent, child if i == 0 else None)
                    for i in range(top_k)]

    def _chunk_with_parent(text, p_text, c_text):
        return RetrievedChunk(chunk_id="c", text=c_text or text, score=1.0, doc_id="d1",
                              breadcrumb="面包屑", vendor="v", model="m", sw_version="s",
                              parent_text=p_text)

    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"}])
    captured: dict = {}
    df = pd.DataFrame({"user_input": ["问题q1"], "faithfulness": [0.9],
                       "answer_relevancy": [0.9], "context_precision": [0.9],
                       "context_recall": [0.9]})
    _install_fake_evaluate(monkeypatch, captured, df)
    run_ragas([_mk_item("q1", ["g1"])], ParentRetriever(client), FakeLLM(),
              judge_llm=object(), embeddings=object(), k=3, progress_every=0,
              assembly="parent-window")
    ctxs = captured["rows"][0]["retrieved_contexts"]
    # 生成侧喂给 LLM 的正文（capturing fake LLM 抓 user 消息）
    llm = FakeLLM()
    from netrag.generation.answer import answer_with_citations

    chunks = ParentRetriever(client).retrieve("问题q1", top_k=3)
    answer_with_citations("问题q1", chunks, llm)
    user = llm.calls[0][1]["content"]
    for i, body in enumerate(build_generation_contexts(chunks)):
        assert f"[{i+1}] 面包屑\n{body}" in user
        assert ctxs[i] == body  # RAGAS contexts == 生成可见正文（Run B 的全部目的）
    assert ctxs[0] == _parent_window(parent, child)  # 父块窗口而非子块全文


def test_run_ragas_default_assembly_stays_child_chunks(monkeypatch):
    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"}])
    captured: dict = {}
    df = pd.DataFrame({"user_input": ["问题q1"], "faithfulness": [0.9],
                       "answer_relevancy": [0.9], "context_precision": [0.9],
                       "context_recall": [0.9]})
    _install_fake_evaluate(monkeypatch, captured, df)
    run_ragas([_mk_item("q1", ["g1"])], FakeRetriever(client), FakeLLM(),
              judge_llm=object(), embeddings=object(), k=2, progress_every=0)
    assert captured["rows"][0]["retrieved_contexts"] == ["hit0-问题q1", "hit1-问题q1"]


def test_run_ragas_unknown_assembly_raises():
    with pytest.raises(ValueError, match="assembly"):
        run_ragas([_mk_item("q1", ["g1"])], FakeRetriever(FakeClient([{"chunk_id": "g1", "text": "t"}])),
                  FakeLLM(), judge_llm=object(), embeddings=object(), k=1, progress_every=0,
                  assembly="wrong")


def test_run_ragas_parent_window_cache_stores_child_texts(monkeypatch, tmp_path):
    """评审 Fix Round 1 Finding 2：缓存只持久化原始 child 文本（校验基准），装配仅发生在评测时。"""
    from netrag.generation.answer import _parent_window

    parent = "前提说明。" * 300
    child = parent[500:600]

    class ParentRetriever(FakeRetriever):
        def retrieve(self, query, top_k=5, filters=None):
            return [RetrievedChunk(chunk_id=f"c{i}", text=child if i == 0 else f"hit{i}",
                                   score=1.0, doc_id="d1", breadcrumb="面包屑", vendor="v",
                                   model="m", sw_version="s", parent_text=parent)
                    for i in range(top_k)]

    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"}])
    captured: dict = {}
    df = pd.DataFrame({"user_input": ["问题q1"], "faithfulness": [0.9],
                       "answer_relevancy": [0.9], "context_precision": [0.9],
                       "context_recall": [0.9]})
    _install_fake_evaluate(monkeypatch, captured, df)
    cache = tmp_path / "gen.json"
    run_ragas([_mk_item("q1", ["g1"])], ParentRetriever(client), FakeLLM(),
              judge_llm=object(), embeddings=object(), k=2, progress_every=0,
              gen_cache_path=cache, cache_key="k1", assembly="parent-window")
    # 评测装配：contexts 是父块窗口
    assert captured["rows"][0]["retrieved_contexts"][0] == _parent_window(parent, child)
    # 缓存落盘：child 文本（未来重跑的字节校验基准），绝非装配后文本
    rows = json.loads(cache.read_text(encoding="utf-8"))["rows"]
    assert rows[0]["retrieved_contexts"] == [child, "hit1"]
    assert "…[前文省略]…" not in json.dumps(rows, ensure_ascii=False)


# ---------- 评测侧伪影剥离：strip_eval_artifacts + run_ragas 接线 ----------


def test_strip_eval_artifacts_footer_only_answer_becomes_empty():
    """答案只剩【出处】脚注块 → 剥离后为空（faithfulness 不再被脚注行计为无据陈述）。"""
    from netrag.eval.ragas_runner import strip_eval_artifacts

    ans = "【出处】\n[1] 华为/以太网交换/VLAN 配置（hw-v600#c15）\n[2] 另一面包屑（d2）"
    assert strip_eval_artifacts(ans) == ""


def test_strip_eval_artifacts_removes_footer_keeps_content():
    from netrag.eval.ragas_runner import strip_eval_artifacts

    ans = ("eth1.100 子接口未配置 IPv4 地址。\n\n"
           "【出处】\n[1] 配置指南/VLAN（d1）\n[2] 故障处理/接口管理（d2）")
    out = strip_eval_artifacts(ans)
    assert "eth1.100 子接口未配置 IPv4 地址。" in out
    assert "【出处】" not in out
    assert "配置指南" not in out
    assert out.endswith("eth1.100 子接口未配置 IPv4 地址。")


def test_strip_eval_artifacts_removes_escape_hatch_sentence():
    """逃生舱句（手册片段未涉及，建议人工确认）整句剥离，含句号与行内前缀。"""
    from netrag.eval.ragas_runner import strip_eval_artifacts

    ans = ("配置步骤如下：执行 display this 查看配置。\n"
           "补全 STP 模式命令（手册片段未涉及，建议人工确认）。\n"
           "最后保存配置。")
    out = strip_eval_artifacts(ans)
    assert "手册片段未涉及" not in out
    assert "补全 STP 模式命令" not in out  # 整句（含前缀）被剥
    assert "display this 查看配置" in out
    assert "最后保存配置" in out


def test_strip_eval_artifacts_normal_content_untouched():
    from netrag.eval.ragas_runner import strip_eval_artifacts

    ans = "端口配置为 trunk 模式，允许 VLAN 100 通过。\n配置命令：port link-type trunk。"
    assert strip_eval_artifacts(ans) == ans


def test_run_ragas_scores_stripped_response_keeps_raw_in_cache_and_records(monkeypatch, tmp_path):
    """接线：RAGAS 拿剥离后答案打分；缓存与 per_item 保留原始答案 + 双长度记录。"""
    client = FakeClient([{"chunk_id": "g1", "text": "期望文本1"}])
    ret = FakeRetriever(client)

    class FooterLLM:
        def __init__(self) -> None:
            self.calls = []

        def chat(self, messages, temperature=0.2, max_tokens=2048):
            self.calls.append(messages)
            return ("真实内容句。\n"
                    "标注句（手册片段未涉及，建议人工确认）。\n"
                    "【出处】\n[1] 面包屑（d1）")

    captured: dict = {}
    df = pd.DataFrame({"user_input": ["问题q1"], "faithfulness": [0.9],
                       "answer_relevancy": [0.9], "context_precision": [0.9],
                       "context_recall": [0.9]})
    _install_fake_evaluate(monkeypatch, captured, df)
    cache = tmp_path / "gen.json"
    out = run_ragas([_mk_item("q1", ["g1"])], ret, FooterLLM(), judge_llm=object(),
                    embeddings=object(), k=1, progress_every=0,
                    gen_cache_path=cache, cache_key="k1")
    # judge 看到的是剥离后答案：脚注块与逃生舱句都不进 EvaluationDataset
    resp = captured["rows"][0]["response"]
    assert resp == "真实内容句。"
    assert "【出处】" not in resp and "手册片段未涉及" not in resp
    # 缓存保留原始答案（未来换剥离规则可重评，不必重新生成）
    cached_resp = json.loads(cache.read_text(encoding="utf-8"))["rows"][0]["response"]
    assert "标注句" in cached_resp and "【出处】" in cached_resp
    # per_item 双长度记录
    rec = out["per_item"][0]
    assert rec["raw_len"] > rec["stripped_len"] > 0
