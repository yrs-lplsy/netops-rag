"""Containerlab 仿真 lab 冒烟测试（marker: ``lab``）。

前置条件：先 ``make lab-up`` 部署拓扑（deploy/containerlab/netops.clab.yml）；
lab 未部署时快速 skip（测试不负责自动部署）。

覆盖：
  1. inventory.yaml 覆盖全部 5 节点（core1/core2/acc1/acc2/nc1）与 frr/netconf 两组
  2. 所有节点 SSH/NETCONF 端口可达（TCP socket connect）
  3. netmiko 登录 core1（FRR vtysh CLI），``show version`` 输出包含 FRR
  4. ncclient 连接 nc1（NETCONF over SSH），``<get>`` ietf-yang-library 模块清单返回数据
"""

import pathlib
import socket
import subprocess

import pytest
import yaml

pytestmark = [pytest.mark.lab]

ROOT = pathlib.Path(__file__).resolve().parents[2]
INVENTORY_PATH = ROOT / "deploy" / "containerlab" / "inventory.yaml"
EXPECTED_NODES = {"core1", "core2", "acc1", "acc2", "nc1"}
EXPECTED_GROUPS = {"frr", "netconf"}


def _lab_deployed() -> bool:
    """lab 是否已部署：docker 中存在 netops 拓扑全部节点容器（等价于
    clab inspect 可见）；任何失败都算未部署。"""
    try:
        proc = subprocess.run(
            ["docker", "ps", "--filter", "name=clab-netops-", "--format", "{{.Names}}"],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    if proc.returncode != 0:
        return False
    names = {n.strip() for n in proc.stdout.splitlines() if n.strip()}
    return {f"clab-netops-{n}" for n in EXPECTED_NODES} <= names


@pytest.fixture(scope="module")
def inventory() -> dict:
    if not _lab_deployed():
        pytest.skip("lab not deployed")
    inv = yaml.safe_load(INVENTORY_PATH.read_text())
    assert isinstance(inv, dict) and "nodes" in inv
    return inv


def _auth(node: dict, inv: dict) -> dict:
    g = inv["groups"][node["group"]]
    return {
        "host": node["host"],
        "port": int(node["port"]),
        "username": g["username"],
        "password": g["password"],
    }


def test_inventory_covers_all_nodes(inventory: dict):
    nodes = set(inventory["nodes"])
    assert EXPECTED_NODES <= nodes, f"inventory 缺少节点: {EXPECTED_NODES - nodes}"
    groups = set(inventory["groups"])
    assert EXPECTED_GROUPS <= groups, f"inventory 缺少分组: {EXPECTED_GROUPS - groups}"


def test_all_nodes_ports_reachable(inventory: dict):
    for name, node in inventory["nodes"].items():
        addr = (node["host"], int(node["port"]))
        with socket.create_connection(addr, timeout=5):
            pass  # 连接成功即认为端口开放


def test_netmiko_core1_show_version_frr(inventory: dict):
    import netmiko

    # 驱动名来自 inventory（netmiko 4.x 无 frr 驱动；FRR 节点 root 登录即
    # vtysh CLI，inventory 统一标 linux 驱动，勿传 "frr"）
    node = inventory["nodes"]["core1"]
    group = inventory["groups"][node["group"]]
    auth = _auth(node, inventory)
    conn = netmiko.ConnectHandler(
        device_type=node.get("netmiko_device_type", group.get("netmiko_device_type")),
        host=auth["host"],
        port=auth["port"],
        username=auth["username"],
        password=auth["password"],
        timeout=30,
    )
    try:
        out = conn.send_command("show version")
    finally:
        conn.disconnect()
    assert "FRR" in out, f"show version 输出无 FRR: {out[:200]!r}"


def test_ncclient_nc1_yang_library(inventory: dict):
    from ncclient import manager

    auth = _auth(inventory["nodes"]["nc1"], inventory)
    with manager.connect(
        host=auth["host"],
        port=auth["port"],
        username=auth["username"],
        password=auth["password"],
        hostkey_verify=False,
        allow_agent=False,
        look_for_keys=False,
        timeout=30,
    ) as m:
        assert m.connected
        # 镜像未内置接口状态插件，<get> interfaces 返回空；
        # 改查 ietf-yang-library 模块清单（netopeer2 原生提供，必含 ietf-interfaces）
        reply = m.get(
            filter=(
                "subtree",
                '<modules-state xmlns="urn:ietf:params:xml:ns:yang:ietf-yang-library"/>',
            )
        )
        assert reply.ok
        data = str(reply.data_xml)
        assert "ietf-interfaces" in data, f"yang-library 数据无 ietf-interfaces: {data[:200]!r}"
