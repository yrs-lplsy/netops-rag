# S3 快版检索评测（200 条四类分层 golden set，PDF v1 语料）

- 日期：2026-09-06
- git：`4e38154`

| 指标 | 值 |
|---|---|
| naive 全题(非reject) n=170 | R@5=0.806 doc=0.806 parent=— any=0.812 |
| naive factual n=100 | R@5=0.750 doc=0.760 parent=— any=0.750 |
| naive troubleshoot n=40 | R@5=0.925 doc=0.850 parent=— any=0.925 |
| naive multihop n=30 | R@5=0.833 doc=0.900 parent=— any=0.867 |
| naive reject RejectPass@5 [正确未命中|标记词] | 1.000 |
| naive reject RejectPass@5 [正确未命中|内容重叠≥3词] | 0.433 |
| hybrid 三路 全题(非reject) n=170 | R@5=0.712 doc=0.841 parent=0.724 any=0.747 |
| hybrid 三路 factual n=100 | R@5=0.690 doc=0.800 parent=0.710 any=0.690 |
| hybrid 三路 troubleshoot n=40 | R@5=0.850 doc=0.925 parent=0.850 any=0.850 |
| hybrid 三路 multihop n=30 | R@5=0.600 doc=0.867 parent=0.600 any=0.800 |
| hybrid 三路 reject RejectPass@5 [正确未命中|标记词] | 1.000 |
| hybrid 三路 reject RejectPass@5 [正确未命中|内容重叠≥3词] | 0.033 |
| hybrid 三路+rerank 全题(非reject) n=170 | R@5=0.776 doc=0.888 parent=0.788 any=0.812 |
| hybrid 三路+rerank factual n=100 | R@5=0.790 doc=0.860 parent=0.800 any=0.790 |
| hybrid 三路+rerank troubleshoot n=40 | R@5=0.850 doc=0.925 parent=0.875 any=0.850 |
| hybrid 三路+rerank multihop n=30 | R@5=0.633 doc=0.933 parent=0.633 any=0.833 |
| hybrid 三路+rerank reject RejectPass@5 [正确未命中|标记词] | 1.000 |
| hybrid 三路+rerank reject RejectPass@5 [正确未命中|内容重叠≥3词] | 0.067 |
| 版本子集 hybrid(+filter) Recall@k [chunk-id] | 0.800 |
| 版本子集 hybrid(+filter) DocRecall@k [doc] | 0.933 |
| 版本子集 naive(+filter) Recall@k [文本重叠] | 0.733 |
| 版本子集 naive(+filter) DocRecall@k [doc] | 0.933 |
| 版本子集 hybrid(无filter,诊断) Recall@k [chunk-id] | 0.667 |
| 版本子集 hybrid(无filter,诊断) DocRecall@k [doc] | 0.867 |


## 参数与口径

- 参数：recall_n=20，rrf_k=60，top_k=5；golden：data/golden/s3_full.yaml（200 条 =
  factual 100（含版本 filter 15）/
  troubleshoot 40 /
  multihop 30 /
  reject 30）；语料：PDF v1 全量
  （hybrid chunks 43,950 行 = 12,243 父 + 31,707 子；naive chunks_naive 18,946 行）
- 判据：[chunk-id]=命中精确等于期望子块 id（multihop 只认 primary，即"首条命中"；naive 因 id
  空间不同退化为文本重叠>=0.5，先验阈值未调优）；[any]=任一期望子块进入 top-5
  （仅 multihop 单列）；[parent]=任一 top-5 命中的 parent_id 等于期望（primary）子块的
  parent_id（naive 无 parent 字段不适用）；[doc]=任一 top-5 命中 doc_id 属于期望文档
- **reject 口径（两层，均可证伪）**：期望命中=空；"正确未命中"（RejectPass@5）要求 top-5
  所有命中既不触发第一层也不触发第二层。第一层 [标记词] = 命中 text/breadcrumb 不含主题标记词
  （生成前经全语料 grep 验证 0 命中，故正常情况下恒通过，仅作回归护栏）：
  reject-大模型 → ['大模型', 'LLM', '神经网络', 'ChatGPT']；reject-Kubernetes容器网络 → ['Kubernetes', 'k8s', '容器编排']；reject-自动化运维工具链 → ['Ansible', 'Zabbix', 'Prometheus', '自动化运维']；reject-Docker容器技术 → ['Docker', 'docker']。
  第二层 [内容重叠] = 命中 text 与题干实义词（ASCII 术语 + 中文 2-gram，去停用词）交集
  <3 个；该层可真实触发失败（语料偶现"容器/镜像"等词即误杀），是更严的
  行为口径——若 RejectPassOverlap < 1.000 为真实信号，本任务不调参
- filters 对 naive 与 hybrid 同等应用（spec 口径）；hybrid 无 filter 行仅为诊断，不作主结果
- **本任务只测量，不做调参**（调参属 T6）

## 主结果

见上方汇总表：三配置（naive / hybrid 三路 / hybrid 三路+rerank）× 全题与分 qtype。
naive 无 parent 字段，其行 parent 列记 "—"（不适用）。

## 版本 filter 子集（15 条，均在 factual）

- hybrid(+filter) Recall@k [chunk-id] = 0.800
- hybrid(+filter) DocRecall@k [doc] = 0.933
- naive(+filter) Recall@k [文本重叠] = 0.733
- naive(+filter) DocRecall@k [doc] = 0.933
- hybrid(无filter,诊断) Recall@k [chunk-id] = 0.667
- hybrid(无filter,诊断) DocRecall@k [doc] = 0.867

### 版本子集构成（脚本自动分级）

分级口径：题干实义词（ASCII 术语 + 中文 2-gram 去停用词）全部出现在对方版本全语料 →
**区域级差异**（期望 chunk 位于版本独有区域——见生成台账核验，但答案内容两版本均出现，
该题同时考过滤机制而非版本独有事实）；否则 → **内容级差异**（题干含对方版本不存在的事实词）。

- 区域级差异（5 条）：hw-v600r025c00-eth-switch-01-07#c94#ver；hw-v600r025c00-eth-switch-01-11#c57#ver；hw-v600r025c00-ip-route-01-06#c125#ver；hw-v600r024c10-eth-switch-01-03#c55#ver；hw-v600r024c10-ip-route-01-06#c137#ver
- 内容级差异（10 条）：hw-v600r025c00-eth-switch-01-03#c30#ver；hw-v600r025c00-eth-switch-01-04#c15#ver；hw-v600r025c00-eth-switch-01-10#c26#ver；hw-v600r025c00-ip-route-01-05#c84#ver；hw-v600r025c00-ip-route-01-07#c278#ver；hw-v600r024c10-eth-switch-01-04#c17#ver；hw-v600r024c10-eth-switch-01-07#c60#ver；hw-v600r024c10-ip-route-01-05#c87#ver；hw-v600r024c10-ip-route-01-09#c71#ver；hw-v600r024c10-ip-route-01-12#c7#ver

## 未命中样例（hybrid 三路，chunk-id|首条判据 + reject 误命中，前 15 条）

- `hw-v600r025c00-eth-switch-01-11#c57#ver`（factual，期望 c57）在华为 V600R025C00 版本文档中，配置完成后，使用哪个命令可以在PE上查看透明传输的二层协议的组播目的MAC地址和Group MAC地址？ → top3: ['c40', 'c33', 'c26']
- `hw-v600r024c10-ip-route-01-09#c71#ver`（factual，期望 c71）在华为 V600R024C10 版本文档中，哪些系列的设备支持通过 `undo portswitch` 命令将接口从二层模式切换到三层模式？ → top3: ['c35', 'c34', 'c125']
- `hw-v600r024c10-ip-route-01-12#c7#ver`（factual，期望 c7）在华为 V600R024C10 版本文档中，为了实现DeviceA仅向DeviceB提供172.16.17.0/24、172.16.18.0/24和172.16.19.0/24这三个特定的Internet路由，可以使用哪种方法，并简述该方法的配置步骤？ → top3: ['c72', 'c76', 'c238']
- `hw-v600r025c00-alarm-01-92#hw-v600r025c00-alarm-01-92#c1`（factual，期望 c1）用户登录Telnet服务器失败的频率过高时，哪个命令可以用来清除登录失败记录？ → top3: ['c7', 'c12', 'c757']
- `hw-v600r024c10-ip-route-01-03#hw-v600r024c10-ip-route-01-03#c11`（factual，期望 c11）静态路由配置了选路依赖迭代深度可能导致什么变化？ → top3: ['c26', 'c25', 'c25']
- `hw-v600r024c10-security-01-05#hw-v600r024c10-security-01-05#c16`（factual，期望 c16）S6750-H系列设备使用display ip source check user-bind status命令可以查看什么？ → top3: ['c23', 'c28', 'c24']
- `hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c10`（factual，期望 c10）通过执行什么命令可以修改BGP路由的缺省本地优先级？ → top3: ['c965', 'c689', 'c565']
- `hw-v600r024c10-ip-route-01-05#hw-v600r024c10-ip-route-01-05#c100`（factual，期望 c100）执行命令display ospf [ process-id ] peer，可以查看什么信息？ → top3: ['c86', 'c89', 'c246']
- `cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c10`（factual，期望 c10）使用class class-default命令匹配BFD数据包时，需要注意什么？ → top3: ['c1815', 'c878', 'c661']
- `cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c10`（factual，期望 c1007）在配置访问控制列表时，如何使用`igmp-type`参数匹配特定的IGMP消息类型？ → top3: ['c125', 'c1101', 'c126']
- `cisco-c9300-17.9-vlan-cg#cisco-c9300-17.9-vlan-cg#c10`（factual，期望 c115）当你在配置了语音VLAN的接口上启用端口安全时，必须将该端口上的最大允许安全地址设置为多少？ → top3: ['c476', 'c795', 'c472']
- `cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c100`（factual，期望 c100）如何在未运行MBGP的情况下配置MSDP的默认对等体？ → top3: ['c46', 'c45', 'c16']
- `cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c1001`（factual，期望 c1001）如何在配置模式下将接口配置为第3层以太网接口并关联VRF？ → top3: ['c61', 'c97', 'c25']
- `cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1000`（factual，期望 c1000）使用time-range全局配置命令可以基于什么来选择性地应用扩展ACL？ → top3: ['c44', 'c43', 'c108']
- `cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c103`（factual，期望 c103）如何使用Cisco Feature Navigator查找平台和软件镜像支持的信息？ 若要访问Cisco Feature Navigator，应前往哪个网址？ → top3: ['c503', 'c459', 'c593']

## 说明

- reject 题无期望文档，不计入全题 chunk/doc 指标；multihop 的 chunk 行即"首条命中"，any 行为"任一命中"
- 本报告全部数字由本脚本单次运行产出（MEASURE ONLY）；hybrid 相对 naive 的差距是 T9 路由前的已知状态，
  原因分析见 S2 报告（BM25 中文错配/RRF 弱路稀释），此处不展开

## TOC修复（重指 11 条目录页坏题前后对比）

golden set 修复（`4e38154`：出题源采样与 QC 双重排除 TOC 目录 chunk，11 条坏题 qid 不变、题目与期望 chunk 重指到真实内容 chunk；含 2 条 multihop 换为同章节 cmd×concept 配对）前后，本脚本以相同参数各单次运行，两轮数字均由脚本汇总表自动提取，非手填：

| 指标 | 修复前 | 修复后 | Δ |
|---|---|---|---|
| naive R@5 [chunk|文本重叠]（ALL n=170） | 0.771 | 0.806 | +0.035 |
| hybrid 三路 R@5 [chunk-id]（ALL n=170） | 0.694 | 0.712 | +0.018 |
| hybrid 三路+rerank R@5 [chunk-id]（ALL n=170） | 0.741 | 0.776 | +0.035 |
| naive DocRecall@5（ALL） | 0.806 | 0.806 | +0.000 |
| hybrid 三路 DocRecall@5（ALL） | 0.841 | 0.841 | +0.000 |
| hybrid 三路+rerank DocRecall@5（ALL） | 0.888 | 0.888 | +0.000 |

分 qtype R@5（修复前 → 修复后）：

- factual：naive 0.720→0.750 / hybrid 三路 0.680→0.690 / hybrid 三路+rerank 0.760→0.790
- troubleshoot：naive 0.875→0.925 / hybrid 三路 0.800→0.850 / hybrid 三路+rerank 0.800→0.850
- multihop：naive 0.800→0.833 / hybrid 三路 0.600→0.600 / hybrid 三路+rerank 0.600→0.633

- **chunk 级全线上升（naive +3.5pt / hybrid +1.8pt / +rerank +3.5pt）、doc 级三配置持平（0.806/0.841/0.888）**：符合修复前预期——TOC 期望 chunk 与书内正文同 doc（doc 判据本可命中），但目录页是特性名堆叠文本，chunk-id 几乎不可检索；重指后期望 chunk 变为可检索的真实内容块
- 版本 filter 子集（hybrid +filter 0.800/0.933 等六行）与 reject 两层口径（1.000；0.433/0.033/0.067）逐字节不变：本修复未触碰 huawei 与 reject 条目
- 修复前未命中样例中的 4 条 cisco TOC 坏题（security/layer2/vlan #c10，chunk-id 恒不可检索）已随重指消失
