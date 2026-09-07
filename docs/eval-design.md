# 评测口径设计：三层判据与 golden set 质量保障

> 本文记录 netops-rag 检索评测的口径设计决策与一次真实的评测集缺陷修复全过程。
> 配套证据：`docs/eval-reports/`（所有数字由 `scripts/run_s3_eval.py` 生成，可一行复现）。

## 1. 为什么需要三层口径

"检索正确"不是单一标准。回答"检索到文件就行，还是必须检索到那个分块？"取决于消费方：

- 生成层有**父块回填**时，命中同章节的任意子块即可还原完整上下文 → 按子块判定过严；
- 引用溯源要求精确到章节面包屑 → 按文档判定过宽；
- 考察切分与排序质量时 → 必须按子块判定。

因此每道题**同时**按三层口径计算并分列报告（表格逐行标注判据），不预设哪个是"唯一真相"：

| 口径 | 判定标准 | 回答的问题 |
|---|---|---|
| **chunk-id** | 期望分块 id 出现在 Top-5 | 切分粒度与排序是否精确命中 |
| **parent** | 命中分块与期望分块同属一个父块（章节） | 粒度偏差是否影响上下文还原 |
| **doc** | Top-5 任一命中来自期望文档 | 是否检索到了正确的手册/版本 |

配套设计：

- **naive 检索器**的 chunk 级判据单独标注为 `[文本重叠]`（旧索引窗口与结构化子块 id 空间不相交，按内容重叠率 ≥50% 判定），与 hybrid 的严格 id 判据不混排比较；
- **多跳题**（期望含两个分块）报双率：`首条命中`（主分块在 Top-5）与 `任一命中`；
- **带 filters 的题**（如 `sw_version=V600R025C00`）对**所有检索器对称应用过滤**，保证对比只反映切分与排序差异；另有"不加过滤"的诊断行量化过滤本身的贡献。

## 2. 拒答题的两层判据（可证伪性设计）

拒答题（手册中不存在的主题，期望为空）的"检索正确"容易做成不可证伪的指标：若判定标记词在语料中零命中，则指标恒为 1.000、永不回归。设计为两层分报：

- **标记词层**（回归护栏）：Top-5 命中含主题标记词即失败——当前语料标记词零命中，该层恒 1.000，仅用于语料扩张后守护；
- **内容重叠层**（可证伪）：问题分词去停用词后与任一命中文本重叠 ≥3 个实义词即判误命中——该层能真实触发（实测 naive 0.433 / hybrid 0.033 / +rerank 0.067，说明 naive 大窗口会把主题邻近内容也捞回）。

## 3. golden set 质量保障机制

1. **均衡采样**：按厂商/文档分桶配额 + 桶内随机，禁止文档顺序截断（曾导致某文档零覆盖）；
2. **出题溯源**：每题由某个具体 chunk 的原文生成，qid 记录该 chunk——"预期分块"即出题所依据的原文段，可机器验证；
3. **grounding 审计**：题面关键词必须出现在期望 chunk 原文中；
4. **全量 QC + 如实台账**：乱码/口吃/无指代/陈述句/近重复逐条淘汰，台账记录每条的淘汰原因；
5. **不变量测试**：yaml 级断言（总数/四类分布/qid 全局唯一/版本题≥15）进 pytest，防回归；
6. **LLM 磁盘缓存**：出题调用可复现，修复轮零 API 成本。

## 4. 案例：TOC 目录页缺陷的发现与修复（2026-09-06）

### 发现

人工抽查演示中随机抽取一条 (`cisco-c9300-17.9-layer2-cg…#c10`，"如何配置 MSTP Hello Time")，取回期望原文后发现是**目录页**（breadcrumb 带 "Contents"，正文为 "Terminology 35 / Hop Count 36" 式页码行）。全量扫描确认：**170 条非拒答题中 11 条（6.5%）期望 chunk 为目录页**，全部集中在思科整书（PDF 带长目录；华为章节 PDF 无此问题）。

### 根因

思科目录页列举了全部功能名词，grounding 审计的**词面匹配**对目录文本天然失明——"Hello Time" 确实出现在目录里，但目录不能回答"如何配置"。

### 修复

- 新增 `is_toc_chunk(breadcrumb, text)` 双签名判定（Contents 标记 / 点引线行占比 >0.5 且行数≥4），接入**出题源池构建**与 **QC 淘汰**两处；
- 11 条坏题**原地重指**：qid 保持不变（评测历史可比），题目与期望 chunk 换为同文档真实内容块，其余 189 条逐字节未动（diff 验证）；
- 新增 4 个单测（含用真实语料目录样例的回归锁）。

### 修复前后（同一脚本、同一指标）

| 指标 (k=5, n=170) | 修复前 | 修复后 |
|---|---|---|
| chunk-id R@5 naive / hybrid / +rerank | 0.771 / 0.694 / 0.741 | **0.806 / 0.712 / 0.776** |
| doc R@5 naive / hybrid / +rerank | 0.806 / 0.841 / 0.888 | 0.806 / 0.841 / 0.888（不变，符合预期：doc 期望未动） |

chunk 级上升而 doc 级持平，与缺陷机理预测一致——目录 chunk 几乎不可被检索命中，剔除坏题后严格口径自然回升。

### 经验

1. **词面 grounding 对目录/索引类文本失效**：评测集构建的审计需要语义级校验兜底（或像本文一样，靠人工抽查+全量特征扫描补位）；
2. **负例与坏题和好题同样有价值**：11 条坏题修复过程沉淀了 `is_toc_chunk` 判定器，未来语料扩张直接复用；
3. **口径分层让缺陷定位成为可能**：doc 级持平 + chunk 级回升的组合，一眼锁定缺陷影响的是"切分粒度"而非"文档路由"。

## 5. 当前口径基线（TOC 修复后，n=170，k=5）

| 配置 | chunk-id R@5 | doc R@5 |
|---|---|---|
| naive（文本重叠判据） | 0.806 | 0.806 |
| hybrid 三路（dense+bm25+sparse, RRF） | 0.712 | 0.841 |
| hybrid + bge-reranker 精排 | 0.776 | **0.888** |

版本过滤题子集（n=15）：hybrid 有 filter chunk 0.800 / doc 0.933 vs 无过滤诊断 chunk 0.667 / doc 0.867（过滤正贡献；详见 docs/eval-reports/2026-09-06-s3-retrieval.md 版本子集节）。
拒答内容重叠层：naive 0.433 / hybrid 0.033 / +rerank 0.067（越低越好，hybrid+rerank 最不易误捞）。

## 6. 数字迭代史：每轮实测、诊断出的问题与解决方案

> 目标数字（67%→88%、faithfulness 0.78→0.92）为项目启动前的目标口径。以下为各阶段真实实测记录：
> 每轮的数字、暴露的问题、诊断依据与落地解法。所有报告可由仓库脚本一行复现。

### 第一轮：S1 naive 基线（旧 HTML 语料 3 篇 / 80 chunks，44 题）

- 实测：chunk R@5 0.864 / doc 1.000 / MRR 0.659
- 诊断出的问题：①首轮出题按文档顺序截断导致 vlan 文档零覆盖（QC 抽查发现）；②LLM 出题对确定性坏 chunk（乱码/口吃）4 轮重试仍失败
- 解法：三文档均衡采样 + 全量 QC + grounding 审计 + 每条淘汰记录台账（本轮重建为 44 题终版）

### 第二轮：S2 对比与消融（旧语料扩至 4 篇 / 103 题）

- 实测：doc 级 naive 0.951 / hybrid 0.841→0.864(融合池) / +rerank 0.903；单路 dense 0.689 / **bm25 0.146** / sparse 0.301；融合池天花板 Recall@30=0.864
- 诊断出的问题：
  ①**naive 反超 hybrid**——小语料 + 窗口式切分下，naive 大窗口靠词面重叠轻易命中；
  ②**BM25 路对"中文问题×英文语料"是纯噪声**（0.146@5），三路融合反把 dense 从 0.689 拖到 0.583；
  ③Qwen2.5-7B 对碎片化表格上下文输出乱码复读（A/B 实证）
- 解法（按序落地）：①语料扩容到真实规模（PDF 管线 v1，221 文档/43,950 chunks）→ 第三轮反转确认消失；
  ②查询路由（T9）：BM25 仅对 exact 类命令查询激活；③生成模型切 72B
- 教训：**消融实验（单路/双路/三路）是把"融合指标差"定位到"具体哪一路坏"的关键**——没有单路诊断就只能盲目调参

### 第三轮：PDF 真实语料首测（221 文档 / 200 题四类）

- 实测（n=170）：doc 级 naive 0.794 / hybrid 0.824 / +rerank 0.894——语料扩容后 naive 反超如期消失
- 诊断出的问题：
  ①**reject 判据不可证伪**（标记词在语料零命中 → 指标恒 1.000）；
  ②**reject QC 旁路**（淘汰项记了台账但未真删，台账与实际不符）；
  ③ask 答案质量弱：子块上下文残缺导致 7B 拒答/复读
- 解法：①双层判据（标记词层=护栏 + 内容重叠层=可证伪，后者实测 naive 0.433 / +rerank 0.067）；
  ②QC 与 factual 同路径 continue 真删 + yaml 级不变量测试；③父块子文本开窗接入生成（替代头截断）

### 第四轮：TOC 缺陷修复后复测（同轮详见 §4）

- chunk 级 R@5：naive 0.771→0.806 / hybrid 0.694→0.712 / +rerank 0.741→0.776；doc 级持平 0.806/0.841/0.888
- 诊断出的新增问题：2 条 multihop 次分块为薄 Feature History 段（同章节亲和配对副产品，已披露待改）；思科语料无故障处理卷，troubleshoot 题支撑弱于华为（语料固有）

### 当前结论（截至本轮）

- **目标"88%"终点与 doc 级 hybrid+rerank 实测 0.888 吻合；起点 67% 在任何已测配置下不存在**（naive 在"题目由 chunk 原文生成"的评测集上天然强）。
  处置：保留本迭代史作为决策依据；候选方案（A 采用实测 80.6→88.8 / B 困难版 golden set 症状式问法重建）已记录待后续选择
- 写作建议：对外表述时主动讲三层口径 + 本节迭代史（每轮用什么诊断定位问题、解法是什么）——比任何单一数字更能证明评测工程能力

## 7. RAGAS faithfulness 迭代方案（已执行：基线→A→B→C→Run D final）

基线（充值后重测，50 条分层抽样，有效 n=48-49）：faithfulness **0.654** / relevancy 0.800 / precision 0.881 / recall 0.844。

### 杠杆①（优先）：修正评测装配错位

- 问题：RAGAS 的 contexts 用**子块文本**，但生成实际可见的是**父块窗口**——答案引用了窗口内、子块之外的内容会被误判为不忠实（系统性压低，跨运行一致）
- 方案：装配改为 contexts=父块窗口文本（与生成可见上下文一致），ground truth 不变；这是修 bug 而非调参
- 预期方向：faithfulness 显著抬升；context_precision/recall 口径不变
- 成本：生成已磁盘缓存，只重跑 judge ≈ ¥2-3/轮

### 第二轮迭代：生成 prompt 收紧

- 问题：答案偶发引用无支撑内容（逐条明细中 faithfulness<0.5 的样例）
- 方案：生成 prompt 增加"仅依据给定片段，无支撑则明确说明"约束 + 引用编号对齐检查；对 faithfulness 低分样例做归因后再调
- 预期方向：faithfulness 提升；需观察 relevancy 不降

### 执行协议（启动时照此跑）

每轮：50 条同抽样（seed=42）→ 生成缓存命中 → judge 重跑 → 报告追加"迭代轮 N"小节 → 与上轮逐指标对比。跑 2-3 轮实测出轨迹，**终点数字是多少对外表述就写多少**；judge 换异构模型（DeepSeek-V3）做一次对照，消除自评偏差疑虑。

### 验证序列结果（2026-09-06/07）

换 judge 重测（Run A）→ 修装配重测（Run B）→ 低分归因，顺序固定、每轮单变量。
同抽样（50 条，seed=42）、同生成（磁盘缓存逐字节一致，两轮 cache 命中 50/50，且 fresh 检索
child 文本与缓存逐字节比对通过）；报告：`docs/eval-reports/2026-09-06-s3-ragas-runA-deepseek-judge.md`、
`2026-09-06-s3-ragas-runB-parent-window.md`（脚本生成，git 54154e5）。

| 轮 | judge | 装配 | faithfulness | relevancy | precision | recall | 有效 n（f/rel/prec/rec） |
|---|---|---|---|---|---|---|---|
| T6 基线 | Qwen2.5-72B（与生成同模型） | child-chunks | 0.654 | 0.800 | 0.881 | 0.844 | 48/49/49/49 |
| Run A | deepseek-v4-flash（DEEPSEEK_MODEL env） | child-chunks | 0.752 | 0.858 | 0.860 | 0.889 | 49/50/50/50 |
| Run B | deepseek-v4-flash | parent-window | 0.801 | 0.856 | 0.850 | 0.880 | 46/49/48/48 |

- **judge 效应**（T6→Run A，+0.098 faithfulness）：72B 同模型 judge 并未因自评偏差抬高
  faithfulness，异构 judge 反而给分更高——绝对值不可跨 judge 比较（英文 prompt × 中文语料
  未校准），"faithfulness 偏低"不能归因于 judge 选型
- **装配效应**（Run A→Run B，+0.049 faithfulness）：杠杆①（contexts=父块窗口）实测有效，
  但只解释剩余缺口的一部分；precision/recall 微降（-0.010/-0.009）在 ±0.1 抽样噪声内
- **低分归因**（Run B faithfulness<0.5 共 7 条，人工逐句比对 contexts 全量归因 7/7；
  Fix Round 1 补齐 2 条）：

| qid | Run B f | 句级证据 | 归因 |
|---|---|---|---|
| hw-v600r025c00-eth-switch-01-03#c30#ver | 0.000 | 唯一内容句与 CTX1 近逐字一致（"仅支持静态LACP模式"） | **judge 误判**（有据判 0） |
| cisco-c9300-17.9-security-cg#c19 | 0.000 | 答案为拒答（无内容主张）；检索 5 段全是华为语料，Cisco 段未召回 | **judge 误判/指标伪影**（拒答无 claims 计 0；真正失分在检索未召回） |
| hw-v600r025c00-alarm-01-67#c15 | 0.333 | 唯一内容句（设备形态清单）与 CTX1/2/3 逐字一致；两条【出处】行被计为无据陈述 | **judge 误判/指标伪影**（0.333=1/3，出处脚注伪影的定量实证） |
| hw-v600r024c10-eth-switch-01-10#c3 | 0.195 | 步骤1-4 有据（fast-detection/timer/tc-protection 在 CTX）；步骤5-8 通用排障无据 | **参数知识泄漏**（有据与记忆混写） |
| hw-v600-case-01-03#c656 | 0.300 | 步骤1-4/8 命令块与 CTX2 近逐字一致；步骤5-7/10 无据 | **参数知识泄漏**（同上） |
| hw-v600-case-01-03#c997 | 0.438 | 自动重认证表述/display portal-server state/收集日志步骤均逐字有据；`re-authenticate user` 命令无据 | **参数知识泄漏（轻）**+出处脚注伪影（1 条命令无据，其余有据被 2 条出处行稀释） |
| hw-v600r025c00-eth-switch-01-10#c26#ver | 0.000 | contexts 与 gold 均明确 DeviceA，答案称 DeviceG（CTX3/5 子环场景实体混淆） | **生成确实编造**（正确答案在 context 内未用） |

  - 计数（7/7）：参数知识泄漏 3 / judge 误判（含指标伪影）3 / 生成确实编造 1
  - 结构性发现（0.333=1/3 类分数为定量实证）：answer_with_citations 的【出处】脚注行在
    faithfulness 陈述拆分中恒为"无据句"，系统性压低所有条目（短答案受害更重）
- **第二轮迭代待人工决策**：7 条低分中 3 条属参数知识泄漏（prompt 收紧直接可修，其中 1 条轻微）；
  3 条为 judge/指标伪影（判前剥离【出处】行、拒答条目单列口径即可，非生成侧问题）；
  1 条为生成实体混淆（收紧 prompt 或有边际帮助，本质需反幻觉约束）。
  装配修正（杠杆①）已完成并保留为显式选项（--assembly parent-window）；
  评测侧伪影修复与第二轮迭代互不替代，建议人工分开决策。
- 成本记录：两轮 judge 合计 DeepSeek 余额 57.93→40.85（≈¥17，显著超 ¥1-2/轮预算——
  deepseek-v4-flash 为推理型模型、计费含推理 token，parent-window 装配后 prompt 更大）；
  402 事件 0 次；未跑第二轮迭代

### 第二轮迭代结果（2026-09-07，Run C：prompt 收紧重测）

实现（2ea669c，TDD）：SYSTEM 增加四条约束——每个技术论断（命令/参数/取值/步骤）须有片段原文依据、
禁止用自己的知识补充命令或步骤、未覆盖内容显式标注"（手册片段未涉及，建议人工确认）"、引用编号与
片段一一对应；【出处】页脚与"未找到"兜底措辞原样保留；temperature 仍 0.2 未动。
唯一变量 = 生成 prompt（同 50 条 seed=42 抽样、同 deepseek-v4-flash judge、同 parent-window 装配）。
生成 50/50 全量重新生成（0 命中）；**坑：生成缓存顶层 key 不含 prompt 内容，沿用旧缓存文件会
50/50 静默命中旧答案、实验失效——已另立缓存文件（旧文件保留），未来 prompt 变更须同样处理**。

| 轮 | faithfulness | relevancy | precision | recall | 有效 n（f/rel/prec/rec） |
|---|---|---|---|---|---|
| Run B（prompt 旧） | 0.801 | 0.856 | 0.850 | 0.880 | 46/49/48/48 |
| Run C（prompt 收紧） | 0.755 | 0.792 | 0.883 | 0.883 | 42/49/48/48 |
| Δ | **-0.046** | -0.064 | +0.033 | +0.003 | |

- 目标样例（缓存答案人工逐句比对 + judge 分数）：#c3 泄漏 0.195→0.483（记忆性通用步骤全删、
  命令全挂引用）；#c997 轻泄漏 0.438→0.571（无据命令 `re-authenticate user` 消失）；
  #c656 泄漏 judge 8 次重试超时 NaN 无分数，但答案对旧泄漏段显式标注"手册片段未涉及，建议人工
  确认"（逃生口按设计生效，全样本 5/50 条使用，Run B 为 0/50）；#c26#ver 编造 0.000→0.778
  **但 DeviceG 实体混淆仍在**——f 回升是新答案补写 CTX 内逐字有据的机制句稀释了无据句（judge
  打分行为变化），反编造约束并未修复该条
- relevancy trade-off：-0.064（两条 0.854/0.967 塌到 0），与答案变长、 hedging/标注增多对
  ResponseRelevancy 嵌入相似度不利一致；幅度与 ±0.1 抽样噪声同量级，方向可信
  （评审补注：塌 0 的两条恰为含"手册片段未涉及"标记句的样例，标记句与【出处】脚注同被
  faithfulness 计无据陈述、5 条标记样例 f 也被伪影压分——f/rel 下降部分属干预自身指标伪影，
  方向对干预有利；且 f 缺失非随机：8 条 NaN 新答案均长 1137 vs 全体 528（2.2×，例 #c22
  747→2061），两轮均值构成不同。详见 RunC 报告 caveats）
- 全局 f 下降的构成：目标 4 条中 3 条有分者全部回升，但其余条目出现新低分（#c100 0.500→0.000、
  vlan#c10 1.000→0.286 等 5 条明显回退）+ f 有效 n 46→42（judge 超时 NaN 增多）——净效应为合成，
  不能单向解读
- 成本与事件：生成 50 次 SiliconFlow（估 ~¥1.5-2，余额接口废弃无法精确查询）+ judge DeepSeek
  40.85→26.70 = ¥14.15（超 ~¥8-9 预估，超时重试加剧）；402 事件 0 次
- **结论**：第二轮迭代未达标（f 净 -0.046、rel -0.064）。目标泄漏条目确有修复证据（答案层面明确、
  judge 分数同向），但代价是 relevancy 下降与其余条目的新低分，且 #c26 编造未被直接修复；
  f 有效 n 下降也放大了均值波动。**建议（仅记录，不跑第三轮）**：①保留收紧 prompt 中"泄漏条目
  修复"的机制价值与人类可读的显式标注（对生产可信度有独立价值，不必回滚，但也不必再单独迭代
  措辞）；②f 的剩余缺口主要在评测侧伪影（【出处】脚注行恒判无据句）与检索未召回（#c19），
  归因表指向的两项评测侧/检索侧修复优先级高于继续调生成 prompt；③judge 超时 NaN 增多提示
  parent-window+长答案下 240s timeout 与 max_workers=8 需重估（下一轮先降 workers 再看覆盖）。

### 最终口径（2026-09-08，Run D：prompt v3 + 伪影剥离，`f5779fa`）

第三轮 = 生成端 v3 prompt（v2 收紧 + 两轮对比陈述引导 `9892596`+`17f90e9`，答案 50/50 新生成）
+ 评测侧伪影剥离落地（ef9c4cb：judge 可见答案剥【出处】脚注与逃生舱句，Run C caveats ②的
落地）；检索/装配/judge/temperature 全部未动。缓存另立
`data/llm_cache/ragas_gen_s50_seed42_runD_final.json`。

| 轮 | faithfulness | relevancy | precision | recall | 有效 n（f/rel/prec/rec） |
|---|---|---|---|---|---|
| Run B（prompt 旧） | 0.801 | 0.856 | 0.850 | 0.880 | 46/49/48/48 |
| Run C（v2 收紧） | 0.755 | 0.792 | 0.883 | 0.883 | 42/49/48/48 |
| **Run D（v3 + stripped，最终）** | **0.851** | **0.904** | 0.851 | 0.884 | **45/50/50/50** |
| Δ(D−C) | +0.096 | +0.112 | -0.032 | +0.001 | |
| Δ(D−B) | +0.050 | +0.048 | +0.001 | +0.004 | |

- **Δ 归因（如实，双变量不可拆）**：D−C 同时含 prompt v2→v3 与剥离两效应——剥离为机械
  回升（44/50 条被剥 12392 字符的恒判无据句）、「v3 净语义增益 = +0.096」不成立；
  方向上「v3 至少无害、f/rel 为四轮历史最高、vs Run B 全指标不劣」成立。prec -0.032 在
  ±0.1 抽样噪声内不解读。vlan 诊断工具修复不在 RAGAS 集生效路径（属 e2e 口径）。
- 判分事件（如实）：首次完整判分误用 timeout=60s（Run B/C 口径为 240s）致 f 有效 n=15、
  rec=18（79 次 TimeoutError），该轮数字作废；按 240s 重判后 TimeoutError 5 次、四指标
  有效 n 全部 ≥40。judge 不缓存，两轮判分均实付 ≈¥15.2（余额 26.70→11.54）；402=0、429=0。
  详见 [2026-09-08-s3-ragas-final.md](eval-reports/2026-09-08-s3-ragas-final.md)。

### CRAG 评测（对齐③，2026-09-07，troubleshoot 40 条开/关对比+救回损失配对）

脚本 scripts/run_crag_eval.py（纯函数单测 tests/test_run_crag_eval_script.py；结果 store
data/llm_cache/crag_eval/raw.json，报告 docs/eval-reports/2026-09-07-crag.md）。
子集 = s3_full.yaml 中 qtype=troubleshoot 的 40 条（模糊类代理；**40≠80 属已知口径差异，原样报告**）。
口径：自动解决 = 非 fallback 且 citations 命中期望文档；转人工 = handoff=True；初次低置信 = 首次
grade < threshold；crag_off = 同检索 top_k=5 直答（Run C 收紧 prompt）；crag_on = build_crag_graph(
threshold, max_rewrite, route=False)（T9 路由不进本评测，推迟 S4）。

| 配置 | 自动解决 | 转人工 | 初次低置信 | 改写触发 |
|---|---|---|---|---|
| crag_off | 92.5%（37/40） | —（无机制） | — | — |
| crag_on（6.0/1） | 92.5%（37/40） | 0%（0/40） | 1/40 | 1/40 |
| on_t1（7.0/1，调参轮1） | 92.5%（37/40） | 0% | 2/40 | 2/40 |

- 配对逐题：救回 0 / 损失 0，40 条结果转移在 off/on 间完全一致（保持解决 37、双败 3）——CRAG 在本子集
  是可证的无操作：纠错回路仅 1/40 触发（grade 4→改写→7→生成，该题基线本就解决），其余全部首检 ≥6 直通
- 双败 3 条（`…alarm-01-01#c6`、`…security-cg#c19`、`…case-01-03#c575`）全是**检索侧未召回**（期望文档
  不进 top-5）且 grade 给主题相近的错误文档打 8 分——打分器分辨不出"相关但不正确"，CRAG 纠错回路
  结构上不可达；修复需动 grade 提示词或检索器，超出"只调调用参数"边界
- 调参（spec §8）：仅跑第 1 轮 threshold 6.0→7.0（唯一作用带非空的杠杆）→ Δ=0 触发无改善即停；
  第 2/3 轮（threshold 5.0 作用带 [5,6) 为空、max_rewrite=2 无耗尽重写样本）经证据分析无信息量，未烧预算
- **对齐③判定：待人工决策**——目标值 ≥85% 被测量值 92.5% 超过，但达标归因于检索侧（hybrid+rerank），
  与 CRAG 无关；叙事的机制部分（75%→85% 由 CRAG 提升、转人工 6%）与测量相悖（Δ=0、转人工 0%）。
  不把「75%→85% 由 CRAG 达成」写入材料；若要支撑原叙事需 ≥80 条模糊类子集或先修检索侧
- 成本与事件：SiliconFlow（Qwen2.5-72B）合计 206 次 LLM 调用（off 40 / on 82 / on_t1 84），估 ~¥2；
  402 事件 0 次，error 0，两配置均 40/40 全覆盖

### T14 Phase 1：端到端排障评测基建 + 30 条任务起草 + 3 条先导（2026-09-07，先导后 STOP 待校准）

**范围**：Phase 1 刻意止步于全量 30 条之前——任务清单交人工校准（用户参与点），未产生
任何"30 条 xx%"口径数字；以下先导结果仅是机制验证与问题暴露。

**基建机制**（`src/netrag/tools_mcp/faults.py` + `scripts/run_e2e.py`）：
- 故障注入 5 类：shutdown_interface（iface）/ ospf_cost_skyhigh（iface, cost=65535）/
  description_garbage（iface, text）/ no_vlan（vlan）/ access_vlan_wrong（mode=retag|wrong_port）。
  FRR 10.4.3 实测语义：内核态 VLAN 子接口（NETOPS_VLANS 启动创建）`no interface` 删不掉
  （zebra 重导入），no_vlan 落地为摘 IP；FRR-only 子接口（eth1.200 等错误标签）可整体
  `no interface` 删除，retag 通道成立；`no ip ospf cost 65535` 带值 no 形式被接受。
- **重置机制 = 基线 diff 收敛**（非故障台账）：每节点 running-config 与
  `deploy/containerlab/configs/<host>/frr.conf` 规范化比对（passive-interface≡ip ospf
  passive 归一、boilerplate/注释剔除、FRR-only 新上下文整块 no、基线内逐叶 negate），
  no 掉多余行 + 回放缺失行。**全程不 write memory**——bind-mount 基线文件与 git 不被触碰
  （与 T12 write 路径的 teardown 痛点不同源）。干净节点零下发。30/30 注入→核验→重置→
  基线收敛（`run_e2e.py --validate` 全 PASS，单循环 24-33s）；OSPF 重收敛由 wait_healthy
  显式等（shutdown 类恢复 ~5-15s）。
- 评测流：reset → inject → CRAG(tools=True) 以任务问句 invoke（state["host"] 显式传入）
  → judge（同 Qwen temp0，{conclusion_correct, tools_reasonable}）→ reset。逐条增量落
  `data/llm_cache/t14_results/*.jsonl`（gitignored）。

**任务清单**（`data/tasks/e2e_30.yaml`，schema：task_id/fault{host,kind,param}/question/
expected_conclusion/expected_tools/difficulty）：分布 = desc 9 / cost 7 / shutdown 6 /
avw 6 / no_vlan 2（**no_vlan 物理上限 2**：基线仅一对 VLAN100 子接口，4 条缺口按
QC"同 (host,kind,param) 不重复"规则分配给其余类——是否接受或扩 lab 基线，待校准）。
难度 easy7/medium18/hard5；主机分布 core1 12 / core2 7 / acc1 7 / acc2 4（acc2 仅 2 条
链路且无 VLAN 子接口）。30 条故障全部经真机验证注入可观测、重置可收敛。问句经
确定性路由审计（crag.py 启发式）修订至 30/30 路由进 expected_tools。

**3 条先导**（t02/t17/t30，easy；LLM 10 次 = grade 4 + rewrite 1 + generate 2 + judge 3，
单条 3/4/3；另起草阶段 2 次，本 phase 合计 12 次，预算 15 内；402=0；wall 42-56s/条）：
- t30（no_vlan acc1，easy）：**PASS/PASS**。grade8 → show_vlan(→brief) 见 eth1.100 无
  IPv4 → 答案明确点出事实 → judge 双真。
- t02（shutdown core1:eth3，easy）：**FAIL/FAIL**。grade9 → diagnose 正确调
  show_ospf_neighbor 且输出可观测（3 邻居变 2，acc2 邻居消失）→ **但生成答案给的是手册
  通用排查步骤**（华为告警文档口径），未基于设备实况下结论。机制链路通，败在生成端：
  answer_with_citations 的"逐论断须有片段依据"prompt 与"基于实况下诊断结论"目标错位。
- t17（desc core2:eth1，easy，**修订前措辞**）：**FAIL/FAIL**。grade2→改写→grade2→
  fallback 转人工，diagnose 未触发。两个叠加原因：①问句缺状态关键词（先导后已修订入
  清单，30/30 路由审计通过）；②结构性问题——lab 实况类问题在手册语料上检索天然低分，
  **grade 门在 diagnose 之前**，低分即转人工，Agent 永远看不到设备实况。

**待人工校准（STOP 点）**：
1. 判分标准：conclusion_correct 要求点中具体接口/地址/取值是否过严/过松？tools_reasonable
   在 diagnose 单工具设计下如何给分（t02 调对了工具仍因生成端失败判 False）？
2. 难度分布（easy7/med18/hard5）与 kind 分布（no_vlan 仅 2）是否接受？
3. 生成端改造：diagnose 命中时是否切换"诊断式"生成 prompt（先报实况结论再引手册步骤）？
   这是 t02 类失败的直接修复杠杆，属 T13 后图结构变更，需决策。
4. grade 门位置：实况类问题是否绕过/降低检索 grade 门（否则 30 条全量预计大量 fallback）？
   同为图结构决策。
5. 工具面：是否给 diagnose 增加 show_ip_route（cost/绕行类唯一硬证据）与 ping？
   （当前 10 只读工具无路由表/连通性观测，cost 类故障的"绕行"症状不可直接观测。）

## 8. T14 端到端评测（对齐④）

**口径**：全流程真实排障——`reset_lab → 故障注入（核验）→ CRAG(tools=True) 排障（Milvus 检索 + gateway 只读工具实况采集 + 生成）→ LLM 判分 → reset_lab 收敛核验`，30 条任务（5 类故障 × lab 可表达变体，难度 easy 7 / medium 18 / hard 5）。与前两层口径（golden 检索层、RAGAS 忠实层）正交：本层评「注入的故障能否被诊断出来并说对」。

**判分**：judge 单次输出 `{conclusion_correct, tools_reasonable}`——结论须点中期望结论的关键事实（具体接口号/地址/取值）；工具合理性由运行器两级校准 + judge 裁量（期望 1 个且恰调用该工具→恒 true；多预期子集→true、零调用→false；越权场景 judge 按「至少一个预期工具且无越权」裁量）。LLM 预算 3 次/题（打分+生成+判分，CountingLLM 单题计量）。

**全量实测（2026-09-07，含 cost 类同构修复复测）**：最终口径 conclusion **24/30（80.0%）**，tools **30/30（100%）**；分类：接口关闭 6/6、描述乱码 9/9、IP 摘除 2/2、cost 抬高 7/7（修复前 0/7——show_ip_route 证「绕路存在」、running-config 证 cost 65535 行归因，与 shutdown 类同构）、**VLAN 标签改错 conclusion 0/6**（tools 6/6：证据已闭合，缺口纯在生成侧「地址迁移」表达，记为已知限制/潜在改进项）。首轮 56.7% → 最终 80.0% 的提升全部来自诊断证据链闭合（shutdown/cost 两类 +running-config），未动判分口径；未达 83.3% 目标（差 1 题），缺口即 VLAN 类。逐字记录见 [docs/eval-reports/2026-09-07-e2e-30.md](eval-reports/2026-09-07-e2e-30.md)。

**最终口径（2026-09-08，vlan 类诊断映射修复后）**：conclusion **29/30（96.7%）**，tools **30/30**。
修复内容 = `_STATE_TOOL_MAP` vlan 类 `("vlan",)→("show_vlan", "get_running_config")`（`f5779fa`，
与 shutdown/cost 类同构收尾：show_vlan 证子接口存在/失链、running-config 的 `no ip address`+
迁移命令序列归因迁移方向——show_vlan 对 down 子接口不显示地址列，单工具下迁移方向不可判定，
此为前口径 1/6 的真实根因）。vlan 类 1/6 → **5/6**（6/6 答案迁移方向全部正确；唯一 FAIL 的
t24 经工具输出核验为 judge 误判——running-config 明确含 `interface eth1.300` + `ip address
10.100.0.2/24`，judge reason 与该输出直接矛盾，官方分不改）；生成 prompt v3 两轮迭代期内
t02（shutdown）补 running-config 后 0→PASS、cost 类同构修复 0/7→7/7。**组成口径如实声明**：
29 = 24（2026-09-07 旧 prompt 下测得的 shutdown 6/6 + desc 9/9 + no_vlan 2/2 + cost 7/7，
未全量复测；t02/t17/t30 本轮 --no-judge 抽查行为不回归，**但 v3 措辞对非 vlan 题有可观测
外溢：t30（纯 IP 摘除）答案出现伪迁移句「地址已从原子接口迁移至 eth1 接口」1 题实测，
judge 影响未测、全量 judge 覆盖缺失**）+ 5（v3 prompt + 双工具诊断下测得）。
逐字记录见 [docs/eval-reports/2026-09-07-e2e-vlan-iter.md](eval-reports/2026-09-07-e2e-vlan-iter.md) §8-§13。

**经验**：① 排障型评测的成败首先取决于**证据链是否闭合**——「目标事实只存在于某一视图」（config 行/接口表）时，诊断工具映射必须覆盖该视图，judge 无法凭手册补证；② 7B/72B 生成模型「看得见异常、说不出差异结论」（t23 看见 eth1.100 失 IP + eth1.200 down 但不点破迁移），对答案抽取的引导是下一层杠杆；③ 运行器直判校准把 judge 噪声从 tools 维度剥离（23/30 直判），judge 噪声残留集中在越权裁量场景；④ 生成端 prompt 迭代（2 轮）与诊断侧证据闭合的对比：前者 vlan 类仅 0/6→1/6，后者同口径 1/6→5/6——**证据可见性缺口无法靠措辞引导绕过**，先闭合证据链再谈生成（与 cost 类 0/7→7/7 同律）；⑤ lab 运维：clab 容器重启会丢数据面链路（OSPF 全空、仅剩 mgmt 口），须 `clab deploy --reconfigure` 重部并 `wait_healthy` 后方可评测。

