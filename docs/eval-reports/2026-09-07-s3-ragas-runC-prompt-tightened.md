# S3 RAGAS 四指标（50 条分层抽样，judge=deepseek，assembly=parent-window，prompt=tightened，hybrid+rerank）

- 日期：2026-09-07
- git：`2ea669c`
- **第二轮迭代 Run C**：唯一变量 = 生成 SYSTEM prompt（收紧：逐论断须有片段原文依据、禁止自补命令/步骤、
  未覆盖显式标注"（手册片段未涉及，建议人工确认）"、引用编号对齐；【出处】页脚与"未找到"兜底措辞不变）。
  temperature 仍为 LLMClient 默认 0.2（未动）。对照基线 = Run B
  （`2026-09-06-s3-ragas-runB-parent-window.md`，prompt 未收紧，其余同口径）

| 指标 | 值 |
|---|---|
| faithfulness（忠实度（答案可由 contexts 支撑）） | 0.755 |
| answer_relevancy（答案相关性（贴合问题）） | 0.792 |
| context_precision（上下文精度（期望内容排前）） | 0.883 |
| context_recall（上下文召回（期望子块被覆盖）） | 0.883 |
| 评测条数 n | 50 |
| 跳过（无 ground truth） | 0 |
| 单条失败 | 0 |
| 生成缓存命中（跳过生成 LLM） | 0 |
| faithfulness 非空计数 /50 | 42 |
| answer_relevancy 非空计数 /50 | 49 |
| context_precision 非空计数 /50 | 48 |
| context_recall 非空计数 /50 | 48 |


## 参数与判据

- golden：data/golden/s3_full.yaml（200 条；抽样域 factual 100、troubleshoot 40），分层比例抽样 n=50
  （seed=42，最大余数法配额）
- 检索：hybrid(dense+bm25+sparse|rerank)，top_k=5，recall_n=20，rrf_k=60（hybrid 时）
- 生成：Qwen/Qwen2.5-72B-Instruct（SiliconFlow），answer_with_citations 父块窗口（cap 6000）；
  生成缓存命中 0/50 条——**收紧后的 SYSTEM prompt 使全部 50 条重新生成**（prompt 变化正是被测变量）。
  生成缓存文件为新路径 `data/llm_cache/ragas_gen_s50_seed42_runC_promptTightened.json`：
  run_ragas 的缓存顶层 key（golden|qtypes|n|seed|retriever|k|llm_model）**不含 prompt 内容**，
  若沿用 Run B 的缓存文件会 50/50 全部命中旧答案、收紧完全不生效，故另立缓存文件（旧文件原样保留）
- 装配：**parent-window**（RAGAS contexts 经 answer.build_generation_contexts 取父块窗口，与生成 LLM 实际可见片段严格一致——T6 验证序列 Run B 装配修正）
- RAGAS：ragas 0.3.1，judge=deepseek（DEEPSEEK_MODEL env 值：deepseek-v4-flash）（temperature=0，LangchainLLMWrapper）；
  嵌入：本地 BAAI/bge-m3（dense，Bgem3LangchainEmbeddings）；
  ground truth = 期望子块全文（Milvus 点查拼接）；raise_exceptions=False
- 指标名对应：answer_relevancy 即 ragas ResponseRelevancy（0.3.x 的 .name）
- 观测：tracer=LangfuseTracer（langfuse 有密钥时自动选 Cloud，否则本地 JSONL 兜底），
  trace_id=6d882eccce53644d727baaf4ba00c39d

## 与 T6 基线对照（差异 = judge+装配+prompt 多变量，非单变量）

同抽样（50 条，seed=42）；但 T6 基线为 child-chunks 装配、Qwen2.5-72B judge、旧 prompt 且答案为缓存复用，
本运行为 parent-window 装配、deepseek judge、**收紧后新 prompt（答案已变）**——三变量合成差异，
**不能**作任何单变量结论（单变量结论见：Run A 对照行判 judge 效应、Run B-vs-Run A 判装配效应、
本报告 Run B-vs-Run C 对照行判 prompt 效应）。

| 指标 | 本次（prompt=tightened） | T6 基线（judge=Qwen2.5-72B@SiliconFlow，assembly=child-chunks）（n=48-49） | Δ |
|---|---|---|---|
| 忠实度（答案可由 contexts 支撑） | 0.755 | 0.654 | +0.101 |
| 答案相关性（贴合问题） | 0.792 | 0.800 | -0.008 |
| 上下文精度（期望内容排前） | 0.883 | 0.881 | +0.002 |
| 上下文召回（期望子块被覆盖） | 0.883 | 0.844 | +0.039 |

## 与 Run B（judge=deepseek，assembly=parent-window，prompt 旧）对照（差异 = 纯 prompt 差异）

同抽样（50 条，seed=42）、同 judge（deepseek（DEEPSEEK_MODEL env 值：deepseek-v4-flash））、
同装配（parent-window），**唯一变量为生成 SYSTEM prompt（未收紧 → 收紧，git 2ea669c）**；
生成侧 50/50 全部重新生成（答案变化 = 被测对象本身的变化，非缓存复用）；
非空计数 <40 的指标只作参考。

| 指标 | 本次 Run C（prompt=tightened）（有效 n） | Run B（prompt 旧）（有效 n） | Δ |
|---|---|---|---|
| 忠实度（答案可由 contexts 支撑） | 0.755（42/50） | 0.801（46/50） | -0.046 |
| 答案相关性（贴合问题） | 0.792（49/50） | 0.856（49/50） | -0.064 |
| 上下文精度（期望内容排前） | 0.883（48/50） | 0.850（48/50） | +0.033 |
| 上下文召回（期望子块被覆盖） | 0.883（48/50） | 0.880（48/50） | +0.003 |

## 主结果

| 指标 | 均值 |
|---|---|
| faithfulness（忠实度（答案可由 contexts 支撑）） | 0.755 |
| answer_relevancy（答案相关性（贴合问题）） | 0.792 |
| context_precision（上下文精度（期望内容排前）） | 0.883 |
| context_recall（上下文召回（期望子块被覆盖）） | 0.883 |
| 评测条数 n | 50 |
| 跳过（无 ground truth） | 0 |
| 单条失败 | 0 |
| 生成缓存命中（跳过生成 LLM） | 0 |
| faithfulness 非空计数 /50 | 42 |
| answer_relevancy 非空计数 /50 | 49 |
| context_precision 非空计数 /50 | 48 |
| context_recall 非空计数 /50 | 48 |

## 第二轮迭代目标样例 before→after（Run B → Run C，人工比对缓存答案逐句）

7/7 归因中 3 条参数化泄漏 + 1 条编造为本次收紧的直接目标（judge=deepseek-v4-flash 不变）：

| qid | 归因 | Run B f | Run C f | 答案级证据（缓存逐字比对） |
|---|---|---|---|---|
| hw-v600r024c10-eth-switch-01-10#c3 | 参数知识泄漏 | 0.195 | 0.483（+0.288） | 旧答案 8 步中 5-8 步为记忆性通用排障（display interface/cpu-usage/logbuffer/联系支持，无据）；新答案删去全部无据通用步骤，仅留 4 步且每条命令挂引用——**泄漏内容消失**，f 大幅回升 |
| hw-v600-case-01-03#c656 | 参数知识泄漏 | 0.300 | —（judge NaN） | 新答案对旧泄漏段（monitor-link 配置）**显式标注"（手册片段未涉及，建议人工确认）"**——收紧的逃生口按设计生效；judge 该条 8 次重试超时未出分，无法给出 before→after 数值（不造数） |
| hw-v600-case-01-03#c997 | 参数知识泄漏（轻） | 0.438 | 0.571（+0.133） | 旧答案混入的无据命令 `re-authenticate user` 在新答案中**已消失**，其余步骤逐条挂引用 |
| hw-v600r025c00-eth-switch-01-10#c26#ver | 生成确实编造 | 0.000 | 0.778（+0.778） | **DeviceG 实体混淆仍在**（新答案依旧写 DeviceG 的 RPL owner 端口被阻塞）；f 回升主要因新答案补写了 CTX[5] 内逐字有据的 WTR/NRRB 机制句，有据句占比稀释了无据句——judge 打分行为变化，**非反编造约束直接修复**，该条遗留问题未解 |

- 逃生口标注（"手册片段未涉及，建议人工确认"）在全样本中的使用：Run C 5/50 条，Run B 0/50 条
- 全局 faithfulness 不升反降（0.801→0.755）：目标 4 条中 3 条有分数者全部回升，但收紧同时改变了
  其余条目的答案形态，出现新的低分条目（如 h3c-r1110-iproute-cmd#c100 0.500→0.000、
  cisco-c9300-17.9-vlan-cg#c10 1.000→0.286、hw-v600r024c10-ip-route-01-09#c71#ver 1.000→0.000、
  hw-v600r024c10-eth-switch-01-03#c10 1.000→0.571、h3c-r1110-iproute-cfg#c1000 1.000→0.571）；
  且 f 有效 n 从 46 降到 42（judge 超时 NaN 增多），均值基底不同——净效应 -0.046 为"目标条目修复"
  与"新增低分条目 + 覆盖变化"的合成，不能解读为"收紧伤害忠实度"的单一定向结论

## relevancy trade-off（诚实呈现）

- answer_relevancy 0.856 → 0.792（**-0.064**）：收紧后答案更长的推理铺垫 + 显式"未涉及"标注 +
  逐条引用挂靠，对 ResponseRelevancy（答案-问题嵌入相似度）不利；个别条目塌到 0
  （hw-v600r025c00-alarm-01-01#c6 0.854→0.000、cisco-c9300-17.9-security-cg#c1002 0.967→0.000）。
  **证据关联（评审发现）**：这两条恰为 5 个含"（手册片段未涉及，建议人工确认）"标记句样例中
  有分数的 2 条——标记句/标注化答案不仅被 faithfulness 计为无据陈述（见 caveats 伪影通道），
  也同时与 relevancy 崩 0 强关联，relevancy 的下降有相当部分可能是同源指标伪影而非真实语义劣化
- 该 trade-off 与 n=50 的 ±0.1 量级抽样噪声同量级，方向可信但幅度不精确；**收紧以 relevancy
  为代价未能换来 faithfulness 净收益**——第二轮迭代按当前措辞单独使用不达标

## 逐条明细（n=50）

| qid | qtype | faithfulness | answer_relevancy | context_precision | context_recall |
|---|---|---|---|---|---|
| h3c-r1110-security-cmd#h3c-r1110-security-cmd#c100 | factual | — | — | — | — |
| hw-v600r024c10-ip-route-01-12#c7#ver | factual | — | 0.903 | — | — |
| hw-v600r025c00-eth-switch-01-10#c26#ver | factual | 0.778 | 0.776 | 0.700 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1004 | factual | — | 0.848 | 1.000 | 1.000 |
| hw-v600r024c10-security-01-08#hw-v600r024c10-security-01-08#c17 | factual | 0.800 | 0.992 | 1.000 | 0.875 |
| hw-v600r025c00-alarm-01-67#hw-v600r025c00-alarm-01-67#c15 | factual | 1.000 | 0.941 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-105#hw-v600r025c00-alarm-01-105#c1000 | factual | 1.000 | 0.961 | 1.000 | 1.000 |
| hw-v600r025c00-security-01-24#hw-v600r025c00-security-01-24#c3 | factual | 1.000 | 0.997 | 1.000 | 1.000 |
| hw-v600r024c10-ip-route-01-09#c71#ver | factual | 0.000 | 0.849 | 1.000 | 0.542 |
| h3c-r1110-security-cfg#h3c-r1110-security-cfg#c100 | factual | 0.750 | 0.892 | 1.000 | 1.000 |
| cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c106 | factual | 0.800 | 0.833 | 0.679 | 0.091 |
| hw-v600r024c10-ip-route-01-05#c87#ver | factual | 0.833 | 0.577 | 1.000 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1 | factual | 1.000 | 0.593 | 1.000 | 1.000 |
| cisco-c9300-17.9-vlan-cg#cisco-c9300-17.9-vlan-cg#c10 | factual | 0.286 | 0.940 | 0.500 | 0.000 |
| hw-v600r025c00-eth-switch-01-11#c57#ver | factual | 1.000 | 0.854 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cfg#h3c-r1110-l2sw-cfg#c105 | factual | 0.783 | 0.980 | 1.000 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1002 | factual | — | 0.981 | 0.867 | 1.000 |
| hw-v600r025c00-eth-switch-01-06#hw-v600r025c00-eth-switch-01-06#c10 | factual | 1.000 | 0.652 | 1.000 | 1.000 |
| hw-v600r025c00-ip-route-01-08#hw-v600r025c00-ip-route-01-08#c100 | factual | 0.909 | 1.000 | 1.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1002 | factual | 0.781 | 0.000 | 1.000 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c100 | factual | 0.000 | 0.790 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cmd#h3c-r1110-l2sw-cmd#c102 | factual | — | 0.000 | 0.750 | 0.500 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1004 | factual | 0.909 | 0.791 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-55#hw-v600r025c00-alarm-01-55#c15 | factual | 1.000 | 0.934 | 1.000 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1001 | factual | 0.875 | 0.965 | 0.833 | 1.000 |
| cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c10 | factual | 1.000 | 0.951 | 1.000 | 1.000 |
| h3c-r1110-security-cmd#h3c-r1110-security-cmd#c1001 | factual | 1.000 | 0.959 | 1.000 | 1.000 |
| cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c1001 | factual | 0.588 | 0.000 | 0.000 | 0.400 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1002 | factual | 1.000 | 0.964 | 1.000 | 1.000 |
| hw-v600r025c00-eth-switch-01-03#c30#ver | factual | 0.000 | 0.851 | 0.867 | 1.000 |
| hw-v600r025c00-security-01-18#hw-v600r025c00-security-01-18#c15 | factual | 1.000 | 0.957 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cmd#h3c-r1110-l2sw-cmd#c103 | factual | 1.000 | 0.697 | 0.917 | 1.000 |
| hw-v600r024c10-eth-switch-01-03#hw-v600r024c10-eth-switch-01-03#c10 | factual | 0.571 | 0.969 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cfg#h3c-r1110-l2sw-cfg#c100 | factual | 0.800 | 0.962 | 1.000 | 1.000 |
| hw-v600r025c00-security-01-09#hw-v600r025c00-security-01-09#c1 | factual | 1.000 | 0.801 | 1.000 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1000 | factual | 0.571 | 0.961 | 1.000 | 1.000 |
| hw-v600r024c10-ip-route-01-08#hw-v600r024c10-ip-route-01-08#c123 | troubleshoot | — | 0.981 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-01#hw-v600r025c00-alarm-01-01#c6 | troubleshoot | 0.455 | 0.000 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-44#hw-v600r025c00-alarm-01-44#c7 | troubleshoot | 1.000 | 0.971 | 1.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c14 | troubleshoot | 0.818 | 0.801 | 0.200 | 1.000 |
| hw-v600-case-01-03#hw-v600-case-01-03#c656 | troubleshoot | — | 0.931 | 0.500 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c19 | troubleshoot | 0.000 | 0.000 | 0.000 | 0.000 |
| hw-v600-case-01-03#hw-v600-case-01-03#c997 | troubleshoot | 0.571 | 0.843 | 0.917 | 1.000 |
| hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c204 | troubleshoot | 0.700 | 0.827 | 0.917 | 1.000 |
| hw-v600r025c00-alarm-01-16#hw-v600r025c00-alarm-01-16#c22 | troubleshoot | — | 0.910 | 0.750 | 1.000 |
| cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c69 | troubleshoot | 0.875 | 0.773 | 1.000 | 1.000 |
| hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c57 | troubleshoot | 0.846 | 0.888 | 1.000 | 1.000 |
| hw-v600r024c10-eth-switch-01-10#hw-v600r024c10-eth-switch-01-10#c3 | troubleshoot | 0.483 | 0.984 | 1.000 | 0.000 |
| hw-v600r025c00-alarm-01-99#hw-v600r025c00-alarm-01-99#c45 | troubleshoot | 0.933 | 0.840 | 1.000 | 1.000 |
| hw-v600r025c00-eth-switch-01-03#hw-v600r025c00-eth-switch-01-03#c8 | troubleshoot | 1.000 | 0.931 | 1.000 | 1.000 |

## 跳过与失败（不造数）

- 跳过 0 条：无
- 单条失败 0 条：无

## 诚实的局限（caveats）

- **judge 为异构模型**（deepseek（DEEPSEEK_MODEL env 值：deepseek-v4-flash））：消除与生成同模型的自评偏差（72B 基线的系统性风险），但异构 judge 对中文陈述抽取的校准同样未验证，绝对值仍只作相对对比；judge 与 Run B 完全一致，Run B-vs-Run C 对照为纯 prompt 差异
- **f 有效 n=42（Run B 为 46）**：本次 judge 单任务超时（timeout=240s）重试耗尽的 NaN 偏多
  （逐条明细 f 列 8 条"—"，日志可见 13 次 TimeoutError 重试；Run B 为 4 条），
  推理型 judge 对更长/更结构化答案的陈述抽取更慢可能是诱因；非 402（余额充足）非 429
- **f 缺失与处理相关（非随机），两轮均值构成不同（评审发现）**：8 条 f-NaN 的新答案均长
  **1137 字符 vs 全体 528（2.2 倍）**（极端例 hw-v600r025c00-alarm-01-16#c22 747→2061）——
  答案变长部分是 prompt 效应，长答案更易触发 judge 超时，故 f 的缺失集中于长答案条目，
  Run B（46 条有分）与 Run C（42 条有分）的均值基于**不同条目构成**；且长度本身对 f 方向
  存疑（更多有据细节可抬 f，固定无据开销被稀释也可能抬 f，与 judge 抽取难度反向）——
  -0.046 的净差异解读需打此折扣
- **标记句指标伪影通道（评审发现）**：本次 prompt 引入的逃生舱句"（手册片段未涉及，建议
  人工确认）"与【出处】脚注同类——RAGAS faithfulness 拆句会把该句计为**无据陈述**（与
  eval-design §7 已录的脚注伪影同机制）。5 条含标记样例中 2 条有 f 分（0.781/0.455），
  该 2 条与下述 3 条 f-NaN 均被该伪影压分——**f 下降的一部分可能是干预自身的指标伪影，
  方向对干预有利（真实收紧效果可能好于表观）**；评测侧剥离此类句属未批准范围，只记录不处理
- **ragas 指标 prompt 为英文**，语料/问答为中文混合：faithfulness 的陈述抽取与
  context_recall 的语句分类在中文上未做校准，绝对值只作相对基线（跨迭代对比用），
  不与公开英文 benchmark 直接可比
- ground truth 用期望子块全文拼 reference：多期望子块（multihop，本期未抽样）会稀释
  precision/recall 判分，故 multihop/reject 不在本期口径
- **本任务只测量不调参**；抽样 n=50，均值抽样误差不小（±0.1 量级），
  结论以跨版本相对变化为准
- **装配修正已生效**：本运行 contexts 为父块窗口（生成可见全集），T6 报告中
  "contexts=子块而生成见父块窗口导致 faithfulness 被系统性压低"的错位在本运行不存在；
  与 child-chunks 运行的差异即该错位的量化影响
- 逐条分数中"—"为该条该指标 judge 调用失败（raise_exceptions=False下 NaN：TPM 限速
  429 / 余额不足 402 等 API 错误重试耗尽），未计入均值；
  各指标"非空计数"行即该均值的实际样本量——覆盖面过低的均值只作参考
- **成本与 402**：生成 50 次 SiliconFlow（新 prompt 全量重新生成，估 ~¥1.5-2；SiliconFlow 余额
  接口已废弃无法精确查询），judge DeepSeek 余额 40.85 → 26.70 = **¥14.15**（200 任务 + 超时重试，
  超出 ~¥8-9 预估）；**402 事件 0 次**，429 事件 0 次，单条生成失败 0 次
- **Cache 语义**：生成缓存 key 不含 prompt 内容——本次第二轮迭代暴露的坑，未来任何 prompt 变更
  必须另立缓存文件，否则旧答案静默命中、实验失效（本次已按新文件处理，旧缓存原样保留）

