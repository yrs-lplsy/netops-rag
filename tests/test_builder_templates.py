"""三类新 golden 模板（troubleshoot/multihop/reject）的单测：全部用 MockLLM，不触网。"""

from netrag.eval.builder import (
    is_troubleshoot_candidate,
    generate_questions,
    generate_multihop_items,
    generate_reject_items,
    pick_multihop_pairs,
)
from netrag.ingestion.types import Chunk


class MockLLM:
    """按顺序返回预设回复的假 LLM。"""

    def __init__(self, replies: list[str]):
        self._replies = list(replies)
        self.prompts: list[str] = []

    def chat(self, messages: list[dict], temperature: float = 0.2, max_tokens: int = 2048) -> str:
        self.prompts.append(messages[-1]["content"])
        return self._replies.pop(0)


def _chunk(cid: str, text: str, parent: str | None = None, doc: str = "doc1") -> Chunk:
    return Chunk(chunk_id=cid, doc_id=doc, text=text, breadcrumb=doc, vendor="huawei",
                 model="S5700", sw_version="V600R025C00", parent_id=parent)


TROUBLE_TEXT = (
    "VLAN不通故障处理：某用户报障无法跨VLAN通信，同VLAN内主机可以互访。处理步骤：先在网关设备上执行"
    "display vlan查看VLAN是否创建，再执行display port vlan检查端口划分，确认属于该VLAN的端口是否以"
    "tag/untag方式加入；若端口未加入VLAN，在接口视图下执行port default vlan重新划分。"
)
TROUBLE_TEXT2 = (
    "STP环路故障排查：网络中出现广播风暴且MAC地址表震荡。常见故障原因是端口路径成本配置不一致或根桥规划"
    "不合理。处理方法：执行display stp root查看根桥是否符合规划，执行display stp brief观察端口角色与"
    "状态，定位收发异常的端口后，检查其对端设备是否不支持BPDU穿透。"
)
CONCEPT_TEXT = (
    "VLANIF接口原理描述：VLANIF接口是一种三层逻辑接口，通过将VLAN与网络层关联，实现VLAN间的三层互通。"
    "VLANIF接口的状态取决于该VLAN内物理端口的up/down状态，只有VLAN内存在处于up状态的物理端口时，"
    "VLANIF接口才会进入up状态。"
)
CMD_TEXT = (
    "配置VLAN间互通的操作步骤：1. 执行命令system-view进入系统视图。2. 执行命令interface vlanif "
    "vlan-id创建VLANIF接口并进入VLANIF接口视图。3. 执行命令ip address ip-address { mask | mask-length }"
    "配置VLANIF接口的IP地址。使用举例：为VLAN 10的网关配置IP地址10.1.1.1/24。"
)
PLAIN_TEXT = "VLAN的缺省配置：所有端口缺省属于VLAN 1。本章介绍VLAN的基本配置与维护。"


# ---- troubleshoot ----

def test_troubleshoot_candidate_keyword_heuristic():
    assert is_troubleshoot_candidate(TROUBLE_TEXT)
    assert is_troubleshoot_candidate("Troubleshooting STP flapping. " * 5)
    assert not is_troubleshoot_candidate(PLAIN_TEXT)


def test_generate_troubleshoot_questions():
    chunks = [
        _chunk("doc1#c1", TROUBLE_TEXT),
        _chunk("doc1#c2", TROUBLE_TEXT2),
        _chunk("doc1#c3", PLAIN_TEXT),  # 非候选，应被跳过
    ]
    llm = MockLLM(["跨VLAN不通时如何排查？", "STP环路如何处理？"])
    items = generate_questions(chunks, llm, qtype="troubleshoot")
    assert [it.qtype for it in items] == ["troubleshoot", "troubleshoot"]
    assert items[0].expected_chunk_ids == ["doc1#c1"]
    assert items[1].expected_chunk_ids == ["doc1#c2"]
    assert "故障" in llm.prompts[0]  # 提示词里带故障处理语境


# ---- multihop ----

def test_pick_multihop_pairs_same_doc_different_parents():
    chunks = [
        _chunk("doc1#c1", CONCEPT_TEXT, parent="doc1#p1"),
        _chunk("doc1#c2", CMD_TEXT, parent="doc1#p2"),
        _chunk("doc1#c3", "同父块的相邻子块，只是配置步骤的重复描述，不应与c2配对。", parent="doc1#p2"),
        _chunk("doc2#c1", CONCEPT_TEXT, parent="doc2#p1", doc="doc2"),
    ]
    pairs = pick_multihop_pairs(chunks)
    assert len(pairs) == 1
    prim, sec = pairs[0]
    # primary=命令/配置侧 chunk，secondary=原理侧 chunk，且必须同 doc
    assert prim.chunk_id == "doc1#c2"
    assert sec.chunk_id == "doc1#c1"


def test_generate_multihop_items_expected_both_chunks_primary_first():
    prim = _chunk("doc1#c2", CMD_TEXT, parent="doc1#p2")
    sec = _chunk("doc1#c1", CONCEPT_TEXT, parent="doc1#p1")
    llm = MockLLM(["VLANIF接口为何要在创建后配置IP地址才能实现VLAN间三层互通？"])
    items = generate_multihop_items([(prim, sec)], llm)
    assert len(items) == 1
    it = items[0]
    assert it.qtype == "multihop"
    assert it.expected_chunk_ids == ["doc1#c2", "doc1#c1"]
    assert it.expected_doc_ids == ["doc1"]


# ---- reject ----

def test_generate_reject_items_empty_expected():
    llm = MockLLM(["如何用Kubernetes部署容器网络的CNI插件并配置网络策略？"])
    items = generate_reject_items(["Kubernetes容器网络"], llm)
    assert len(items) == 1
    it = items[0]
    assert it.qtype == "reject"
    assert it.expected_chunk_ids == []
    assert it.expected_doc_ids == []
    assert it.filters is None
    assert "Kubernetes" in it.question


def test_generate_reject_items_qids_globally_unique():
    # 30 个主题各 1 条（生产形态）：qid 必须全局唯一（主题 slug 各不相同）
    topics = [f"主题{i}" for i in range(30)]
    llm = MockLLM([f"关于主题{i}的一个非常具体的问题应该怎么问？" for i in range(30)])
    items = generate_reject_items(topics, llm)
    qids = [it.qid for it in items]
    assert len(set(qids)) == len(qids) == 30


def test_generate_reject_items_variants_increment_per_theme():
    # 同主题多变体：序号必须真实递增（评审 Finding 2 回归门）
    llm = MockLLM(["这个问题很长足够通过最短长度检查了吗？", "第二个变体也足够长可以通过检查了吗？"])
    items = generate_reject_items(["某主题"], llm, variants_per_theme=2)
    assert [it.qid for it in items] == ["reject-某主题-01", "reject-某主题-02"]
    # 同主题重复出现在列表中：序号继续递增不重置
    llm = MockLLM(["第一次提问的内容足够长了吗？", "第二次提问的内容也足够长了吗？"])
    items = generate_reject_items(["某主题", "某主题"], llm)
    assert [it.qid for it in items] == ["reject-某主题-01", "reject-某主题-02"]


def test_all_templates_strip_and_clean_output():
    chunks = [_chunk("doc1#c1", TROUBLE_TEXT)]
    llm = MockLLM(['  "接口频繁up-down如何排查？"\n'])
    items = generate_questions(chunks, llm, qtype="troubleshoot")
    assert items[0].question == "接口频繁up-down如何排查？"
