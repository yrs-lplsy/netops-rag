# S3 RAGAS 四指标（50 条分层抽样，judge=deepseek，assembly=parent-window，hybrid+rerank）

- 日期：2026-09-07
- git：`54154e5`

| 指标 | 值 |
|---|---|
| faithfulness（忠实度（答案可由 contexts 支撑）） | 0.801 |
| answer_relevancy（答案相关性（贴合问题）） | 0.856 |
| context_precision（上下文精度（期望内容排前）） | 0.850 |
| context_recall（上下文召回（期望子块被覆盖）） | 0.880 |
| 评测条数 n | 50 |
| 跳过（无 ground truth） | 0 |
| 单条失败 | 0 |
| 生成缓存命中（跳过生成 LLM） | 50 |
| faithfulness 非空计数 /50 | 46 |
| answer_relevancy 非空计数 /50 | 49 |
| context_precision 非空计数 /50 | 48 |
| context_recall 非空计数 /50 | 48 |


## 参数与判据

- golden：data/golden/s3_full.yaml（200 条；抽样域 factual 100、troubleshoot 40），分层比例抽样 n=50
  （seed=42，最大余数法配额）
- 检索：hybrid(dense+bm25+sparse|rerank)，top_k=5，recall_n=20，rrf_k=60（hybrid 时）
- 生成：Qwen/Qwen2.5-72B-Instruct（SiliconFlow），answer_with_citations 父块窗口（cap 6000）；
  生成缓存命中 50/50 条（命中条目生成 LLM 零调用，答案与 T6 基线逐字节一致）
- 装配：**parent-window**（RAGAS contexts 经 answer.build_generation_contexts 取父块窗口，与生成 LLM 实际可见片段严格一致——T6 验证序列 Run B 装配修正）
- RAGAS：ragas 0.3.1，judge=deepseek（DEEPSEEK_MODEL env 值：deepseek-v4-flash）（temperature=0，LangchainLLMWrapper）；
  嵌入：本地 BAAI/bge-m3（dense，Bgem3LangchainEmbeddings）；
  ground truth = 期望子块全文（Milvus 点查拼接）；raise_exceptions=False
- 指标名对应：answer_relevancy 即 ragas ResponseRelevancy（0.3.x 的 .name）
- 观测：tracer=LangfuseTracer（langfuse 有密钥时自动选 Cloud，否则本地 JSONL 兜底），
  trace_id=d6fa3170c7ff11f4ffbc72994f8bcebe

## 与 T6 基线对照（差异 = judge+装配 双变量，非单变量）

同抽样（50 条，seed=42）、同生成（Qwen2.5-72B，生成缓存命中）；但 T6 基线为 child-chunks 装配、本次为 parent-window，judge 后端与装配同时变化——
本行 Δ 为双变量（judge+装配）合成差异（评审 Fix Round 1 Finding 1 更正：此前误标"纯 judge 后端差异"），单变量结论另见：Run A 对照行（纯 judge 效应 f+0.098）与本报告下方 Run B-vs-Run A 对照行（纯装配效应 f+0.049）；非空计数 <40 的指标只作参考。

| 指标 | 本次（parent-window） | T6 基线（judge=Qwen2.5-72B@SiliconFlow，assembly=child-chunks）（n=48-49） | Δ |
|---|---|---|---|
| 忠实度（答案可由 contexts 支撑） | 0.801 | 0.654 | +0.147 |
| 答案相关性（贴合问题） | 0.856 | 0.800 | +0.056 |
| 上下文精度（期望内容排前） | 0.850 | 0.881 | -0.031 |
| 上下文召回（期望子块被覆盖） | 0.880 | 0.844 | +0.036 |

## 与 Run A（judge=deepseek，assembly=child-chunks） 对照（差异 = 纯装配差异）

同抽样（50 条，seed=42）、同生成（缓存命中，答案逐字节一致）、同 judge（deepseek（DEEPSEEK_MODEL env 值：deepseek-v4-flash）），
唯一变量为 contexts 装配口径（child-chunks → parent-window）；非空计数 <40 的指标只作参考。

| 指标 | 本次（assembly=parent-window） | Run A（judge=deepseek，assembly=child-chunks） | Δ |
|---|---|---|---|
| 忠实度（答案可由 contexts 支撑） | 0.801 | 0.752 | +0.049 |
| 答案相关性（贴合问题） | 0.856 | 0.858 | -0.002 |
| 上下文精度（期望内容排前） | 0.850 | 0.860 | -0.010 |
| 上下文召回（期望子块被覆盖） | 0.880 | 0.889 | -0.009 |

## 主结果

| 指标 | 均值 |
|---|---|
| faithfulness（忠实度（答案可由 contexts 支撑）） | 0.801 |
| answer_relevancy（答案相关性（贴合问题）） | 0.856 |
| context_precision（上下文精度（期望内容排前）） | 0.850 |
| context_recall（上下文召回（期望子块被覆盖）） | 0.880 |
| 评测条数 n | 50 |
| 跳过（无 ground truth） | 0 |
| 单条失败 | 0 |
| 生成缓存命中（跳过生成 LLM） | 50 |
| faithfulness 非空计数 /50 | 46 |
| answer_relevancy 非空计数 /50 | 49 |
| context_precision 非空计数 /50 | 48 |
| context_recall 非空计数 /50 | 48 |

## 逐条明细（n=50）

| qid | qtype | faithfulness | answer_relevancy | context_precision | context_recall |
|---|---|---|---|---|---|
| h3c-r1110-security-cmd#h3c-r1110-security-cmd#c100 | factual | — | 0.959 | — | — |
| hw-v600r024c10-ip-route-01-12#c7#ver | factual | — | — | — | — |
| hw-v600r025c00-eth-switch-01-10#c26#ver | factual | 0.000 | 0.856 | 0.867 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1004 | factual | 1.000 | 0.923 | 1.000 | 1.000 |
| hw-v600r024c10-security-01-08#hw-v600r024c10-security-01-08#c17 | factual | 1.000 | 1.000 | 1.000 | 0.875 |
| hw-v600r025c00-alarm-01-67#hw-v600r025c00-alarm-01-67#c15 | factual | 0.333 | 0.981 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-105#hw-v600r025c00-alarm-01-105#c1000 | factual | 1.000 | 0.983 | 1.000 | 1.000 |
| hw-v600r025c00-security-01-24#hw-v600r025c00-security-01-24#c3 | factual | 1.000 | 0.920 | 1.000 | 1.000 |
| hw-v600r024c10-ip-route-01-09#c71#ver | factual | 1.000 | 0.887 | 1.000 | 0.389 |
| h3c-r1110-security-cfg#h3c-r1110-security-cfg#c100 | factual | 0.900 | 0.829 | 1.000 | 1.000 |
| cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c106 | factual | 1.000 | 0.916 | 0.679 | 0.091 |
| hw-v600r024c10-ip-route-01-05#c87#ver | factual | 0.500 | 0.613 | 1.000 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1 | factual | 1.000 | 0.631 | 1.000 | 1.000 |
| cisco-c9300-17.9-vlan-cg#cisco-c9300-17.9-vlan-cg#c10 | factual | 1.000 | 0.957 | 0.500 | 0.000 |
| hw-v600r025c00-eth-switch-01-11#c57#ver | factual | 1.000 | 0.879 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cfg#h3c-r1110-l2sw-cfg#c105 | factual | 1.000 | 0.896 | 1.000 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1002 | factual | 1.000 | 0.938 | 0.887 | 1.000 |
| hw-v600r025c00-eth-switch-01-06#hw-v600r025c00-eth-switch-01-06#c10 | factual | 1.000 | 0.655 | 1.000 | 1.000 |
| hw-v600r025c00-ip-route-01-08#hw-v600r025c00-ip-route-01-08#c100 | factual | 0.800 | 0.999 | 1.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1002 | factual | — | 0.967 | 1.000 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c100 | factual | 0.500 | 0.788 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cmd#h3c-r1110-l2sw-cmd#c102 | factual | 0.931 | 1.000 | 0.750 | 0.500 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1004 | factual | 0.867 | 0.848 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-55#hw-v600r025c00-alarm-01-55#c15 | factual | 1.000 | 0.868 | 0.917 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1001 | factual | 0.800 | 0.966 | 1.000 | 1.000 |
| cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c10 | factual | 1.000 | 0.810 | 1.000 | 1.000 |
| h3c-r1110-security-cmd#h3c-r1110-security-cmd#c1001 | factual | 1.000 | 0.954 | 1.000 | 1.000 |
| cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c1001 | factual | 0.500 | 0.000 | 0.000 | 0.400 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1002 | factual | 1.000 | 0.959 | 1.000 | 1.000 |
| hw-v600r025c00-eth-switch-01-03#c30#ver | factual | 0.000 | 0.850 | 1.000 | 1.000 |
| hw-v600r025c00-security-01-18#hw-v600r025c00-security-01-18#c15 | factual | 1.000 | 0.956 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cmd#h3c-r1110-l2sw-cmd#c103 | factual | 1.000 | 0.688 | 0.917 | 1.000 |
| hw-v600r024c10-eth-switch-01-03#hw-v600r024c10-eth-switch-01-03#c10 | factual | 1.000 | 0.967 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cfg#h3c-r1110-l2sw-cfg#c100 | factual | 1.000 | 0.978 | 1.000 | 1.000 |
| hw-v600r025c00-security-01-09#hw-v600r025c00-security-01-09#c1 | factual | 1.000 | 0.742 | 1.000 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1000 | factual | 1.000 | 0.921 | 1.000 | 1.000 |
| hw-v600r024c10-ip-route-01-08#hw-v600r024c10-ip-route-01-08#c123 | troubleshoot | — | 0.983 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-01#hw-v600r025c00-alarm-01-01#c6 | troubleshoot | 0.600 | 0.854 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-44#hw-v600r025c00-alarm-01-44#c7 | troubleshoot | 1.000 | 0.833 | 1.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c14 | troubleshoot | 0.519 | 0.964 | 0.367 | 1.000 |
| hw-v600-case-01-03#hw-v600-case-01-03#c656 | troubleshoot | 0.300 | 0.948 | 0.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c19 | troubleshoot | 0.000 | 0.000 | 0.000 | 0.000 |
| hw-v600-case-01-03#hw-v600-case-01-03#c997 | troubleshoot | 0.438 | 0.813 | 0.917 | 1.000 |
| hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c204 | troubleshoot | 0.867 | 0.870 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-16#hw-v600r025c00-alarm-01-16#c22 | troubleshoot | 1.000 | 0.991 | 0.250 | 1.000 |
| cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c69 | troubleshoot | 1.000 | 0.897 | 0.000 | 1.000 |
| hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c57 | troubleshoot | 1.000 | 0.891 | 1.000 | 1.000 |
| hw-v600r024c10-eth-switch-01-10#hw-v600r024c10-eth-switch-01-10#c3 | troubleshoot | 0.195 | 0.990 | 0.756 | 0.000 |
| hw-v600r025c00-alarm-01-99#hw-v600r025c00-alarm-01-99#c45 | troubleshoot | 1.000 | 0.850 | 1.000 | 1.000 |
| hw-v600r025c00-eth-switch-01-03#hw-v600r025c00-eth-switch-01-03#c8 | troubleshoot | 0.800 | 0.958 | 1.000 | 1.000 |

## 跳过与失败（不造数）

- 跳过 0 条：无
- 单条失败 0 条：无

## 诚实的局限（caveats）

- - **judge 为异构模型**（deepseek（DEEPSEEK_MODEL env 值：deepseek-v4-flash））：消除与生成同模型的自评偏差（72B 基线的系统性风险），但异构 judge 对中文陈述抽取的校准同样未验证，绝对值仍只作相对对比；与 72B judge 的数值差异见对照表（该行在 parent-window 装配下为 judge+装配双变量，单变量结论见 Run A 对照行与 Run B-vs-Run A 对照行）
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

