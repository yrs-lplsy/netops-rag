"""scripts/run_ragas.py 的 CLI 参数单测（零 API、零 Milvus：只测参数解析）。"""

import importlib.util
import sys
from pathlib import Path

import pytest

_SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "run_ragas.py"


def _load_script():
    spec = importlib.util.spec_from_file_location("run_ragas_script", _SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_judge_flag_default_deepseek():
    """默认 judge=deepseek（人工决策：降成本+消自评偏差）。"""
    args = _load_script().parse_args([])
    assert args.judge == "deepseek"


def test_judge_flag_accepts_siliconflow():
    args = _load_script().parse_args(["--judge", "siliconflow"])
    assert args.judge == "siliconflow"


def test_judge_flag_rejects_unknown_backend():
    with pytest.raises(SystemExit):
        _load_script().parse_args(["--judge", "openai"])


def test_assembly_flag_default_child_chunks():
    args = _load_script().parse_args([])
    assert args.assembly == "child-chunks"


def test_assembly_flag_accepts_parent_window():
    args = _load_script().parse_args(["--assembly", "parent-window"])
    assert args.assembly == "parent-window"


def test_assembly_flag_rejects_unknown():
    with pytest.raises(SystemExit):
        _load_script().parse_args(["--assembly", "full-doc"])


def test_timeout_flag_default_and_passthrough():
    """ragas RunConfig.timeout 默认 60s：DeepSeek 推理型 judge 单调用常超时，需可调。"""
    args = _load_script().parse_args([])
    assert args.timeout == 60  # 不传保持 ragas 默认，历史行为不变
    args = _load_script().parse_args(["--timeout", "240"])
    assert args.timeout == 240


# ---------- 评审 Fix Round 1 Finding 1：T6 对照段措辞按装配口径切换 ----------


def test_t6_comparison_child_chunks_is_single_variable():
    mod = _load_script()
    text = mod.t6_comparison_text("child-chunks", {}, "deepseek")
    assert "纯 judge 后端差异" in text
    assert "双变量" not in text


def test_t6_comparison_parent_window_is_two_variable():
    """Run B 口径：T6 是 child-chunks，judge+装配同时变——必须标注双变量并指路单变量结论。"""
    mod = _load_script()
    text = mod.t6_comparison_text("parent-window", {}, "deepseek")
    assert "双变量" in text
    assert "纯 judge 后端差异" not in text
    assert "Run A" in text  # 指路单变量结论所在
