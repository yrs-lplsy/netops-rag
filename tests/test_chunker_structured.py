from netrag.embedding.dummy import DummyTokenCounter
from netrag.ingestion.chunker_structured import chunk_structured
from netrag.ingestion.types import DocMeta

META = DocMeta(vendor="cisco", model="C9300", sw_version="17.9", doc_id="d1", title="手册")

MD = """# 指南

## 创建 VLAN

vlan 命令用于创建 VLAN。

```
Device> enable
Device# configure terminal
Device(config)# vlan 20
Device(config-vlan)# name test20
```

### 参数表

| 参数 | 说明 |
|---|---|
| id | VLAN 编号 |
| name | VLAN 名称 |

## 空节标题
"""


def test_parents_children_linked():
    parents, children = chunk_structured(MD, META, DummyTokenCounter(), child_min=3, child_max=20)
    assert len(parents) >= 2  # 创建 VLAN、参数表（伪节/空节除外）
    assert all(p.is_parent for p in parents)
    assert all(not c.is_parent for c in children)
    parent_ids = {p.chunk_id for p in parents}
    assert all(c.parent_id in parent_ids for c in children)
    vlan_parent = next(p for p in parents if "创建 VLAN" in p.breadcrumb)
    assert "vlan 20" in vlan_parent.text


def test_code_block_atomic():
    parents, children = chunk_structured(MD, META, DummyTokenCounter(), child_min=1, child_max=5)
    code_children = [c for c in children if "configure terminal" in c.text]
    assert code_children, "代码块内容不得被丢弃"
    for c in code_children:
        assert "vlan 20" in c.text and "name test20" in c.text  # 代码块整体在一个子块


def test_oversized_paragraph_subsplit():
    lines = [" ".join(f"s{i}w{j}" for j in range(10)) for i in range(40)]  # 40 行 × 10 词
    md = "# 长文\n\n## 长段\n\n" + "\n".join(lines)
    parents, children = chunk_structured(md, META, DummyTokenCounter(), child_min=1, child_max=25)
    long_children = [c for c in children if any(f"s{i}w0" in c.text for i in range(40))]
    assert long_children, "长段内容不得被丢弃"
    # 超长段落按行二次切分后，任何子块不得超 child_max
    assert all(DummyTokenCounter().count(c.text) <= 25 for c in long_children)
    # 无内容丢失：所有不同的词都保留
    expected = {f"s{i}w{j}" for i in range(40) for j in range(10)}
    got = set(" ".join(c.text for c in long_children).split())
    assert expected <= got


def test_table_split_with_header_template():
    big_table_md = "# T\n\n## 表节\n\n| 参数 | 说明 |\n|---|---|\n" + "\n".join(
        f"| p{i} | 说明{i} |" for i in range(30))
    parents, children = chunk_structured(big_table_md, META, DummyTokenCounter(), child_min=1, child_max=8)
    table_children = [c for c in children if "p0" in c.text or "p29" in c.text]
    assert table_children
    assert all("参数" in c.text and "说明" in c.text for c in table_children)  # 表头模板拼进每个子块
