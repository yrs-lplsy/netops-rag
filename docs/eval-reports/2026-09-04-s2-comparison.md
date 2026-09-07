# S2 检索升级对比与消融

- 日期：2026-09-05
- git：`de70984`

| 指标 | 值 |
|---|---|
| naive Recall@5 [chunk-id/文本重叠] | 0.961 |
| naive MRR | 0.850 |
| naive Recall@5 [doc] | 0.951 |
| hybrid(dense+bm25+sparse) Recall@5 [chunk-id] | 0.583 |
| hybrid(dense+bm25+sparse) MRR | 0.366 |
| hybrid(dense+bm25+sparse) Recall@5 [parent] | 0.621 |
| hybrid(dense+bm25+sparse) Recall@5 [doc] | 0.864 |
| hybrid(dense+bm25) Recall@5 [chunk-id] | 0.680 |
| hybrid(dense+bm25) MRR | 0.460 |
| hybrid(dense+bm25) Recall@5 [parent] | 0.699 |
| hybrid(dense+bm25) Recall@5 [doc] | 0.893 |
| hybrid(dense+sparse) Recall@5 [chunk-id] | 0.583 |
| hybrid(dense+sparse) MRR | 0.369 |
| hybrid(dense+sparse) Recall@5 [parent] | 0.612 |
| hybrid(dense+sparse) Recall@5 [doc] | 0.854 |
| hybrid(dense+bm25+sparse|rerank) Recall@5 [chunk-id] | 0.718 |
| hybrid(dense+bm25+sparse|rerank) MRR | 0.588 |
| hybrid(dense+bm25+sparse|rerank) Recall@5 [parent] | 0.748 |
| hybrid(dense+bm25+sparse|rerank) Recall@5 [doc] | 0.903 |


## 参数与口径

- 参数：recall_n=20，rrf_k=60，top_k=5；golden：103 条（版本过滤 15 条）
- naive 索引：同语料 4 文档 100 chunk（ospf 27 / stp 33 / vlan17.9 20 / vlan17.7 20），所有配置（含 naive）对带 filters 的题同样应用 filters
- 判据标注：[chunk-id]=命中精确等于期望子块 id（naive 因 id 空间不同退化为文本重叠≥0.5，先验阈值未调优）；[parent]=任一 top-5 命中的 parent_id 等于期望子块的 parent_id（章节级，naive 无 parent 字段不适用）；[doc]=任一 top-5 命中的 doc_id 属于期望文档
- 主结果行：
- hybrid(dense+bm25+sparse): Recall@5 [chunk-id]=0.583 MRR=0.366 [parent]=0.621 [doc]=0.864
- hybrid(dense+bm25): Recall@5 [chunk-id]=0.680 MRR=0.460 [parent]=0.699 [doc]=0.893
- hybrid(dense+sparse): Recall@5 [chunk-id]=0.583 MRR=0.369 [parent]=0.612 [doc]=0.854
- hybrid(dense+bm25+sparse|rerank): Recall@5 [chunk-id]=0.718 MRR=0.588 [parent]=0.748 [doc]=0.903
- naive（文本重叠判据）: Recall@5=0.961 MRR=0.850 [doc]=0.951（parent 不适用）

## 版本过滤子集（15 条）

- hybrid(dense+bm25+sparse): Recall@5 [chunk-id]=0.667 MRR=0.316 [parent]=0.800 [doc]=1.000
- naive（文本重叠判据）: Recall@5=1.000 MRR=0.833 [doc]=1.000

## 单路消融诊断（chunk-id 判据，103 条全量）

- hybrid(dense)（chunk-id 判据）: Recall@5=0.689 Recall@20=0.825
- hybrid(bm25)（chunk-id 判据）: Recall@5=0.146 Recall@20=0.165
- hybrid(sparse)（chunk-id 判据）: Recall@5=0.301 Recall@20=0.515

**BM25 路是主要噪声源**：Task 13 的 `bm25_text` 只保留命令型行（英文命令/参数），与中文 golden 题几乎无词法交集，单路 Recall@5 仅 0.146；RRF 等权融合两个弱路把 dense 单路 0.689 拉低到三路 0.583（dense+bm25 0.680 > 三路，sparse 融合亦无增益）。

## 融合池天花板（精排池上界，chunk-id 判据）

- hybrid(dense+bm25+sparse)（recall_n=30，top_k=30）: **Recall@30=0.864**
- 即使精排器完美（把池内期望子块总排到第 1），Recall@5 上限即该池召回值；等价单点复现：`--paths dense,bm25,sparse --k 30 --recall-n 30`。
- 剩余任务书调参杆不可行或方向相反：child_max 500→400 需重建 hybrid 索引 → 全部期望 chunk id 失效；BM25 加权 3→5 需重建且实测单路 Recall@5=0.146，加权只会放大噪声。

## 未命中样例（默认配置 hybrid 三路，chunk-id 判据，前 8）

- `c35`（cisco-c9300-17.9-vlan）删除一个VLAN后其关联的端口会怎样？ → top3: ['c7', 'c13', 'c34']
- `c49`（cisco-c9300-17.9-vlan）使用接口模板给接口应用 VLAN 命令前，需要先做什么？ → top3: ['c3', 'c25', 'c10']
- `c60`（cisco-c9300-17.9-vlan）可以将端口分配给哪个范围的VLAN？ → top3: ['c13', 'c7', 'c4']
- `c8`（cisco-c9300-17.7-vlan）可以配置多少个VLAN同时生效？ → top3: ['c13', 'c4', 'c3']
- `c35`（cisco-c9300-17.7-vlan）删除一个VLAN后 会使得该VLAN分配的端口变为不活跃状态吗？ → top3: ['c7', 'c13', 'c34']
- `c16`（cisco-c9300-17.9-ospf）OSPF的Hello间隔时间是多少秒？ → top3: ['c83', 'c81', 'c12']
- `c21`（cisco-c9300-17.9-ospf）配置特权EXEC模式需要输入什么命令？ → top3: ['c64', 'c165', 'c125']
- `c69`（cisco-c9300-17.9-ospf）如何进入特权EXEC模式需要输入哪个命令？ → top3: ['c64', 'c99', 'c165']

## 版本子集构成（人工核验记录）

两版 VLAN 手册各 8/7 条镜像题（filter `sw_version=17.9/17.7`，期望 chunk 指向对应版本手册）。其中 c8/c25/c49 三对 chunk 两版本**文本确有差异**（17.9 独有 VTP 名长句/media 命令表 Note/接口模板告诫，diff 实测 ratio 0.81–0.97），c10/c15/c35/c60/c78 五对字节级相同（同质特性，仅作过滤机制测试——期望 chunk 必须落在 filter 指定文档）。naive 在 filter 后候选池仅 20 chunk，得高分属小池效应；hybrid 过滤本身工作正常（无跨版本误检），低分与其整体检索质量一致。

## naive 判据说明（口径可比性）

s2_mixed 的期望 chunk 是 hybrid 子块（`doc#cN`），naive 索引是独立切分的 `doc#nN`，按 chunk_id 匹配对 naive 恒为 0，故 naive 的 chunk 行用文本重叠判据（宽松）；[doc] 与 [parent] 判据为 naive/hybrid 共用的对称锚点——naive 无 parent 字段，doc 级为两检索器可直接对比的粒度。

## 调参记录（数字对齐流程，逐杆追加，历史轮次实测值）

### Round 1：recall_n 20→30（其余默认，chunk-id 判据）

- hybrid(+rerank): Recall@5 **0.757** MRR 0.608（↑0.718，精排池变大）
- hybrid(dense+bm25+sparse): 0.544（↓0.583，池变大但弱路噪声稀释了无精排的排序）
- hybrid(dense+bm25): 0.660；hybrid(dense+sparse): 0.534；naive 不受影响（0.961）
- 复现：`--recall-n 30`

### Round 2：recall_n=30 基础上 rrf_k 60→40

- hybrid(+rerank): Recall@5 **0.757**（无变化）；hybrid 三路 0.563；dense+bm25 0.660；dense+sparse 0.544
- 复现：`--recall-n 30 --rrf-k 40`

### 停止依据

实测最佳 0.757 距 0.88 差 12.3pct > 3pct，且融合池天花板（见上）< 0.88——按 spec §8 停止调参，保留实测数字。

## 偏差分析（对比 88% 目标，未改任何数字）

1. **BM25 专用字段与中文查询错配是根因**：`bm25_text`（Task 13，仅命令型行）对英文查询有效（Task 15 spot check `ospf network-type` 命中 c144），对中文 golden 题无词法交集（单路 Recall@5=0.146）。RRF 等权融合使该噪声路实际降低了 dense 质量（0.689→0.583）。改进方向（超出本任务范围）：bm25_text 同时纳入中文叙述句或查询侧翻译/混编，或对 BM25 路降权。
2. **rerank 是本链路最有效的升级**（三路 0.583→精排 0.718，+0.136；Round1 池扩大后再 +3.9pct 至 0.757），但受融合池天花板 0.864 限制。
3. **naive 与 hybrid 的对称锚点**：doc 级判据下 naive 0.951 vs hybrid 三路 0.864 / 精排 0.903；naive chunk 行的高分部分来自宽松的内容重叠判据与 100 个大窗口小池，但 doc 级对称对比同样显示 naive 领先，混合链路在本语料上未超过 naive 基线是实测事实。
4. **版本过滤子集**：过滤机制工作正常（15 条无跨版本误检）；hybrid 低分来自上述整体检索质量问题而非过滤本身。
5. **结论**：S2 混合链路未达到 88% 目标（实测最佳 hybrid+rerank chunk Recall@5=0.757，默认配置 0.718）。**"67%→88%" 的目标叙事与实测不符**：本报告 naive（重建后同语料）chunk 0.961 / doc 0.951，hybrid+rerank chunk 0.718 / doc 0.903。是否修订目标数字（或注明口径：小语料 4 文档/103 题/判据）交由用户决策。所有数字均为脚本单次运行实测，调参轮次逐杆追加，无手改。

## 复现性修订（Fix Round 1，2026-09-05）

本文件此前有 4 处数字来自临时 probe 脚本（未入库），本次全部改为由提交的 `scripts/run_s2_eval.py` 直接产出，逐项对账：

1. **单路消融（dense/bm25/sparse Recall@5/@20）**：probe → 脚本"单路消融诊断"一节（默认运行即产出；单点复现 `--paths dense` 等）。数值与 probe 一致。
2. **parent 判据（三路 0.621 / 精排 0.748）**：probe → 主表 [parent] 行，默认运行即产出。数值与 probe 一致。
3. **融合池天花板（Recall@30=0.864）**：probe → "融合池天花板"一节（默认运行即产出；单点复现 `--paths dense,bm25,sparse --k 30 --recall-n 30`）。数值与 probe 一致。
4. **naive doc 级（0.951）**：旧脚本 body 行 → 主表 [doc] 行。数值一致。
5. **指标命名修正**：`evaluate` 此前无论 k 取值都输出 "Recall@5"；现按实际 k 命名（Recall@5 / DocRecall@5 / ParentRecall@5）。
6. 调参记录两轮数字为历史轮次（上一脚本版本）实测，评测逻辑未变，可用 `--recall-n 30` / `--recall-n 30 --rrf-k 40` 复现。

