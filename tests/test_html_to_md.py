from pathlib import Path

from netrag.ingestion.html_to_md import convert_html

FIXTURE = Path(__file__).parent / "fixtures" / "sample_cisco.html"


def test_convert_keeps_content_drops_chrome():
    md = convert_html(FIXTURE.read_text())
    assert "vlan 20" in md
    assert "| Command |" in md or "Command" in md
    assert "global nav" not in md
    assert "footer" not in md
    assert "var x" not in md
    assert md.lstrip().startswith("# VLAN Configuration Guide")


def test_convert_falls_back_to_body():
    md = convert_html("<html><body><h1>Only</h1><p>text</p></body></html>")
    assert "# Only" in md and "text" in md


def test_convert_prefers_fw_content_over_body():
    # 思科真实页面容器 id 是 fw-content（评审发现：#mainContent 在线上并不存在）
    html = (
        "<html><body><ul><li>Skip to content</li></ul>"
        '<div id="fw-content"><h1>OSPF Guide</h1>'
        "<p>Use router ospf to enable OSPF.</p></div>"
        "<footer>[Log in] to Save Content</footer></body></html>"
    )
    md = convert_html(html)
    assert "# OSPF Guide" in md
    assert "router ospf" in md
    assert "Skip to content" not in md
    assert "Log in" not in md


def test_convert_prefers_role_main_and_strips_ui_buttons():
    # 线上 fw-content 内仍混有 aboutBias/saveDocumentMessage 等 boilerplate，
    # 真正正文是其内的 [role=main]（div#pageContentDiv）；UI 按钮文案（如 Close）也应剥离
    html = (
        '<html><body><div id="fw-content">'
        '<div class="aboutBias"><h3>Bias-Free Language</h3>'
        "<p>boilerplate text</p></div>"
        '<div class="saveDocumentMessage">[Log in] to Save Content</div>'
        '<div id="pageContentDiv" role="main"><button id="chapterToc-close">Close</button>'
        "<h1>Configuring VLANs</h1><p>Create vlan 20 with a name.</p></div>"
        "</div></body></html>"
    )
    md = convert_html(html)
    assert "# Configuring VLANs" in md
    assert "vlan 20" in md
    assert "Bias-Free Language" not in md
    assert "[Log in]" not in md
    assert "Close" not in md
