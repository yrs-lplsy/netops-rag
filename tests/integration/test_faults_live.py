"""faults.py 真机往返（marker: ``lab``，无 LLM）：注入 → running 核验 → 重置 → 基线收敛。

只抽 2 个代表性故障做冒烟（shutdown=接口级、access_vlan_wrong retag=子接口级；
30 条任务的逐一注入/核验/重置走 scripts/run_e2e.py --validate，不进 pytest）。
纪律同 faults.py：全程不 write memory，跑完 git 工作区应保持干净（bind-mount
基线文件不被触碰）。
"""

import pathlib
import subprocess

import pytest

from netrag.tools_mcp.device import DeviceConnection
from netrag.tools_mcp.faults import LAB_FRR_HOSTS, FaultLab

pytestmark = [pytest.mark.lab]

ROOT = pathlib.Path(__file__).resolve().parents[2]

CASES = [
    ("core1", "shutdown_interface", {"iface": "eth3"}),
    ("acc1", "access_vlan_wrong", {"mode": "retag", "vlan": 200}),
]


@pytest.fixture(scope="module", autouse=True)
def _final_reset():
    """模块兜底：无论测试结局如何，收尾全量重置 + 等 OSPF 3×Full。"""
    yield
    try:
        lab = FaultLab(DeviceConnection())
        lab.reset()
        lab.wait_healthy(timeout=90)
    except Exception:  # noqa: BLE001 — 兜底清理不掩盖原测试结果
        pass


def _lab_deployed() -> bool:
    try:
        proc = subprocess.run(
            ["docker", "ps", "--filter", "name=clab-netops-", "--format", "{{.Names}}"],
            capture_output=True, text=True, timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    names = {n.strip() for n in proc.stdout.splitlines() if n.strip()}
    return {f"clab-netops-{h}" for h in LAB_FRR_HOSTS} <= names


@pytest.mark.parametrize("host,kind,param", CASES)
def test_inject_verify_reset_roundtrip(host, kind, param):
    if not _lab_deployed():
        pytest.skip("lab not deployed")
    lab = FaultLab(DeviceConnection())
    lab.reset()  # 起点干净
    assert lab.wait_healthy(), "起跑前 OSPF 未收敛到 3×Full"

    inj = lab.inject(host, kind, param)
    assert inj["verified"], f"注入未在 running 中核验到: {inj['verify_detail']}"
    assert lab.diff_from_baseline(host)[0], "注入后 running 应相对基线有漂移"

    rep = lab.reset([host])
    assert rep[host]["changed"], "重置应有实际下发"
    added, removed = lab.diff_from_baseline(host)
    assert added == [] and removed == [], f"重置后未收敛回基线: +{added} -{removed}"
    assert lab.wait_healthy(), "重置后 OSPF 未恢复 3×Full"
