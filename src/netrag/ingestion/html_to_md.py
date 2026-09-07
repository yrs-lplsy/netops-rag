from bs4 import BeautifulSoup
from markdownify import markdownify as mdify


def convert_html(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    # button 为 UI 控件文案（如章节 TOC 的 Close），非文档正文；
    # markdownify 的 strip 只去标签不弃文本，故用 decompose 连文本一并移除
    for tag in soup(["script", "style", "nav", "footer", "header", "button"]):
        tag.decompose()
    # 思科真实页面：正文是 #fw-content 内的 [role=main]（div#pageContentDiv）；
    # aboutBias/saveDocumentMessage 等 boilerplate 位于 fw-content 内、role=main 外，
    # 只取 fw-content 仍会漏杂讯，故 [role=main] 优先。逐级回退兼容旧选择器/fixture。
    node = (
        soup.select_one("[role=main]")
        or soup.select_one("#fw-content")
        or soup.select_one("#mainContent")
        or soup.body
        or soup
    )
    text = mdify(str(node), heading_style="ATX", strip=["img"])
    return text.strip() + "\n"
