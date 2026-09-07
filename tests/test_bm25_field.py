from netrag.ingestion.bm25_field import build_bm25_text, extract_exact_terms


def test_extract_cli_interface_version_errorcode():
    text = """
Device(config)# vlan 20
Device(config-vlan)# name test20
接口 GigabitEthernet0/0/1 已启用。
软件版本 V800R021，对应 VRP 平台。
报错：%LINK-3-UPDOWN: Interface GigabitEthernet0/0/1, changed state to down
升级版本 17-9-1。
"""
    terms = extract_exact_terms(text)
    joined = " ".join(terms)
    assert "vlan 20" in joined
    assert "gigabitethernet0/0/1" in joined.lower()
    assert "v800r021" in joined.lower()
    assert "17-9-1" in joined.lower()
    assert "%link-3-updown" in joined.lower()


def test_prose_and_comment_lines_rejected():
    text = """
OSPF is an Interior Gateway Protocol used for routing.
# vlan batch 10 20
Device(config)# vlan 20
display ospf lsdb
interface tengigabitethernet ports deliver line rate forwarding on every one
"""
    terms = extract_exact_terms(text)
    joined = " ".join(terms)
    assert "interior gateway protocol" not in joined.lower()  # 散文句不捕获
    assert "vlan batch" not in joined.lower()  # # 注释行不捕获
    assert "vlan 20" in joined  # 真实提示符命令保留
    assert "display ospf lsdb" in joined  # 裸关键词命令保留
    assert "line rate forwarding" not in joined.lower()  # 超长散文行不捕获


def test_build_bm25_text_weights_exact_terms():
    text = "Device(config)# vlan 20\n上述命令用于创建 VLAN。"
    bm = build_bm25_text(text, "手册 > VLAN 配置")
    assert bm.count("vlan") >= 3  # 精确词加权
    assert "手册" in bm and "配置" in bm
    assert bm == bm.lower()
    assert all(ch.isalnum() or ch.isspace() for ch in bm.replace("%", "").replace("-", "").replace("/", ""))
