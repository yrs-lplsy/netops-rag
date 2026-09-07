# S1 naive 基线检索评测（k=5）

- 日期：2026-09-04
- git：`62a329e`

| 指标 | 值 |
|---|---|
| golden 条数 | 44 |
| Recall@5 (chunk) | 0.864 |
| Recall@5 (doc) | 1.000 |
| MRR (chunk) | 0.659 |

## 未命中样例（前 10）

- `cisco-c9300-17.9-ospf#cisco-c9300-17.9-ospf#n20` 使用ospf进程ID的命令是什么？
  - top3: ['cisco-c9300-17.9-ospf#n26', 'cisco-c9300-17.9-ospf#n9', 'cisco-c9300-17.9-ospf#n17'] 期望: ['cisco-c9300-17.9-ospf#n20']
- `cisco-c9300-17.9-stp#cisco-c9300-17.9-stp#n1` Spanning Tree协议中，设备的端口如何成为根设备的端口是如何定义的？
  - top3: ['cisco-c9300-17.9-stp#n12', 'cisco-c9300-17.9-stp#n2', 'cisco-c9300-17.9-stp#n3'] 期望: ['cisco-c9300-17.9-stp#n1']
- `cisco-c9300-17.9-stp#cisco-c9300-17.9-stp#n11` 如何设备端口成为根端口？
  - top3: ['cisco-c9300-17.9-stp#n12', 'cisco-c9300-17.9-stp#n23', 'cisco-c9300-17.9-stp#n21'] 期望: ['cisco-c9300-17.9-stp#n11']
- `cisco-c9300-17.9-vlan#cisco-c9300-17.9-vlan#n2` 配置VLAN时设备并启用路由功能时需要将SDM选择哪个模板？
  - top3: ['cisco-c9300-17.9-vlan#n7', 'cisco-c9300-17.9-vlan#n5', 'cisco-c9300-17.9-stp#n7'] 期望: ['cisco-c9300-17.9-vlan#n2']
- `cisco-c9300-17.9-vlan#cisco-c9300-17.9-vlan#n10` 如何配置Normal范围的VLAN中的VLAN ID参数？
  - top3: ['cisco-c9300-17.9-vlan#n12', 'cisco-c9300-17.9-vlan#n8', 'cisco-c9300-17.9-stp#n21'] 期望: ['cisco-c9300-17.9-vlan#n10']
- `cisco-c9300-17.9-vlan#cisco-c9300-17.9-vlan#n11` 配置的VLAN ID范围是多少？
  - top3: ['cisco-c9300-17.9-vlan#n12', 'cisco-c9300-17.9-vlan#n8', 'cisco-c9300-17.9-stp#n28'] 期望: ['cisco-c9300-17.9-vlan#n11']

## 偏差分析

实测 chunk Recall@5 = 0.864，高于预期区间（0.55–0.75）。未调整任何数字，可能原因：

1. **语料规模极小**：仅 80 个 chunk、3 篇同厂商/同型号（Catalyst 9300 17.9）手册，dense 检索在如此小的候选池中区分度高；真实生产语料（数百篇、多厂商）下同链路指标通常显著下降。
2. **题目由期望 chunk 直接派生**：golden 问题由 LLM 阅读期望 chunk 后生成，措辞与 chunk 内容相近（多数含原样命令/参数名），相当于"可见文档的改写问句"，比真实用户问题简单。
3. **覆盖与未命中构成**（44 条 = ospf 18 / stp 12 / vlan 14，三篇手册均有题目）：未命中共 6 条，分档 recall 为 ospf 17/18（0.944）、stp 10/12（0.833）、vlan 11/14（0.786）。文档级 Recall@5 = 1.000，即所有题目的期望文档都进了 top-5，不存在"整篇检索错文档"的情况；但 6 条未命中中有 3 条（vlan n2/n10/n11）的 top-5 里混入了跨文档的 stp chunk（VLAN 手册中生成树相关内容与 STP 手册主题相邻所致），另外 3 条（ospf n20、stp n1、stp n11）为纯同文档相邻 chunk 干扰——naive 固定窗口切分（512/50）把命令表切成内容高度相似的相邻 chunk，chunk 级判定天然偏严。
4. **MRR 0.659 < Recall@5 0.864**：命中多落在 rank 2–5 而非 rank 1，同样反映相邻/同主题 chunk 干扰，为 S2（父子 chunk + rerank）留出提升空间。

结论：0.864 是该小语料、chunk 派生问题设定下的诚实测量值，作为 S1 naive 基线与 S2 对比使用；引用到目标口径/对外材料时应注明语料规模（80 chunk / 3 篇手册）与测量条件。
