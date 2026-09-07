# S3 RAGAS 四指标（50 条分层抽样，judge=deepseek，assembly=child-chunks，hybrid+rerank）

- 日期：2026-09-07
- git：`a2647b6`

| 指标 | 值 |
|---|---|
| faithfulness（忠实度（答案可由 contexts 支撑）） | 0.752 |
| answer_relevancy（答案相关性（贴合问题）） | 0.858 |
| context_precision（上下文精度（期望内容排前）） | 0.860 |
| context_recall（上下文召回（期望子块被覆盖）） | 0.889 |
| 评测条数 n | 50 |
| 跳过（无 ground truth） | 0 |
| 单条失败 | 0 |
| 生成缓存命中（跳过生成 LLM） | 50 |
| faithfulness 非空计数 /50 | 49 |
| answer_relevancy 非空计数 /50 | 50 |
| context_precision 非空计数 /50 | 50 |
| context_recall 非空计数 /50 | 50 |


## 参数与判据

- golden：data/golden/s3_full.yaml（200 条；抽样域 factual 100、troubleshoot 40），分层比例抽样 n=50
  （seed=42，最大余数法配额）
- 检索：hybrid(dense+bm25+sparse|rerank)，top_k=5，recall_n=20，rrf_k=60（hybrid 时）
- 生成：Qwen/Qwen2.5-72B-Instruct（SiliconFlow），answer_with_citations 父块窗口（cap 6000）；
  生成缓存命中 50/50 条（命中条目生成 LLM 零调用，答案与 T6 基线逐字节一致）
- 装配：**child-chunks**（RAGAS contexts = 检索命中子块文本，与 T6 基线一致；生成可见的仍是父块窗口——装配错位本运行未修，仅隔离 judge 变量）
- RAGAS：ragas 0.3.1，judge=deepseek（DEEPSEEK_MODEL env 值：deepseek-v4-flash）（temperature=0，LangchainLLMWrapper）；
  嵌入：本地 BAAI/bge-m3（dense，Bgem3LangchainEmbeddings）；
  ground truth = 期望子块全文（Milvus 点查拼接）；raise_exceptions=False
- 指标名对应：answer_relevancy 即 ragas ResponseRelevancy（0.3.x 的 .name）
- 观测：tracer=LangfuseTracer（langfuse 有密钥时自动选 Cloud，否则本地 JSONL 兜底），
  trace_id=c6cdf98e24c13392e74e45ba748dc57e

## 与 T6 基线对照（差异 = 纯 judge 后端差异）

同抽样（50 条，seed=42）、同生成（Qwen2.5-72B，生成缓存命中）、同装配（child-chunks），
唯一变量为 judge 后端（deepseek（DEEPSEEK_MODEL env 值：deepseek-v4-flash） vs 72B judge）；非空计数 <40 的指标只作参考。

| 指标 | 本次（deepseek） | T6 基线（judge=Qwen2.5-72B@SiliconFlow，assembly=child-chunks）（n=48-49） | Δ |
|---|---|---|---|
| 忠实度（答案可由 contexts 支撑） | 0.752 | 0.654 | +0.098 |
| 答案相关性（贴合问题） | 0.858 | 0.800 | +0.058 |
| 上下文精度（期望内容排前） | 0.860 | 0.881 | -0.021 |
| 上下文召回（期望子块被覆盖） | 0.889 | 0.844 | +0.045 |

## 主结果

| 指标 | 均值 |
|---|---|
| faithfulness（忠实度（答案可由 contexts 支撑）） | 0.752 |
| answer_relevancy（答案相关性（贴合问题）） | 0.858 |
| context_precision（上下文精度（期望内容排前）） | 0.860 |
| context_recall（上下文召回（期望子块被覆盖）） | 0.889 |
| 评测条数 n | 50 |
| 跳过（无 ground truth） | 0 |
| 单条失败 | 0 |
| 生成缓存命中（跳过生成 LLM） | 50 |
| faithfulness 非空计数 /50 | 49 |
| answer_relevancy 非空计数 /50 | 50 |
| context_precision 非空计数 /50 | 50 |
| context_recall 非空计数 /50 | 50 |

## 逐条明细（n=50）

| qid | qtype | faithfulness | answer_relevancy | context_precision | context_recall |
|---|---|---|---|---|---|
| h3c-r1110-security-cmd#h3c-r1110-security-cmd#c100 | factual | 0.750 | 0.922 | 0.756 | 1.000 |
| hw-v600r024c10-ip-route-01-12#c7#ver | factual | 0.500 | 0.900 | 1.000 | 1.000 |
| hw-v600r025c00-eth-switch-01-10#c26#ver | factual | 0.000 | 0.862 | 0.804 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1004 | factual | 0.500 | 0.916 | 1.000 | 1.000 |
| hw-v600r024c10-security-01-08#hw-v600r024c10-security-01-08#c17 | factual | 1.000 | 1.000 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-67#hw-v600r025c00-alarm-01-67#c15 | factual | 1.000 | 0.984 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-105#hw-v600r025c00-alarm-01-105#c1000 | factual | 1.000 | 0.974 | 1.000 | 1.000 |
| hw-v600r025c00-security-01-24#hw-v600r025c00-security-01-24#c3 | factual | 1.000 | 0.904 | 1.000 | 1.000 |
| hw-v600r024c10-ip-route-01-09#c71#ver | factual | 0.000 | 0.851 | 1.000 | 0.542 |
| h3c-r1110-security-cfg#h3c-r1110-security-cfg#c100 | factual | 0.667 | 0.909 | 1.000 | 1.000 |
| cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c106 | factual | 1.000 | 0.893 | 0.679 | 0.000 |
| hw-v600r024c10-ip-route-01-05#c87#ver | factual | 0.800 | 0.626 | 1.000 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1 | factual | 1.000 | 0.630 | 1.000 | 1.000 |
| cisco-c9300-17.9-vlan-cg#cisco-c9300-17.9-vlan-cg#c10 | factual | 1.000 | 0.997 | 0.500 | 0.000 |
| hw-v600r025c00-eth-switch-01-11#c57#ver | factual | 1.000 | 0.833 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cfg#h3c-r1110-l2sw-cfg#c105 | factual | 1.000 | 0.922 | 1.000 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1002 | factual | 1.000 | 0.940 | 0.887 | 1.000 |
| hw-v600r025c00-eth-switch-01-06#hw-v600r025c00-eth-switch-01-06#c10 | factual | 1.000 | 0.655 | 0.867 | 1.000 |
| hw-v600r025c00-ip-route-01-08#hw-v600r025c00-ip-route-01-08#c100 | factual | 1.000 | 0.943 | 1.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1002 | factual | 0.250 | 0.903 | 0.917 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c100 | factual | 0.333 | 0.786 | 0.867 | 1.000 |
| h3c-r1110-l2sw-cmd#h3c-r1110-l2sw-cmd#c102 | factual | 0.933 | 1.000 | 0.750 | 0.500 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1004 | factual | 0.846 | 0.854 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-55#hw-v600r025c00-alarm-01-55#c15 | factual | 1.000 | 0.907 | 1.000 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1001 | factual | 0.800 | 0.959 | 1.000 | 1.000 |
| cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c10 | factual | 1.000 | 0.864 | 1.000 | 1.000 |
| h3c-r1110-security-cmd#h3c-r1110-security-cmd#c1001 | factual | 1.000 | 0.979 | 1.000 | 1.000 |
| cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c1001 | factual | 0.450 | 0.000 | 0.000 | 0.400 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1002 | factual | 1.000 | 0.996 | 1.000 | 1.000 |
| hw-v600r025c00-eth-switch-01-03#c30#ver | factual | 1.000 | 0.801 | 0.700 | 1.000 |
| hw-v600r025c00-security-01-18#hw-v600r025c00-security-01-18#c15 | factual | 1.000 | 0.946 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cmd#h3c-r1110-l2sw-cmd#c103 | factual | 1.000 | 0.708 | 0.917 | 1.000 |
| hw-v600r024c10-eth-switch-01-03#hw-v600r024c10-eth-switch-01-03#c10 | factual | 0.750 | 0.955 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cfg#h3c-r1110-l2sw-cfg#c100 | factual | 0.750 | 1.000 | 1.000 | 1.000 |
| hw-v600r025c00-security-01-09#hw-v600r025c00-security-01-09#c1 | factual | 1.000 | 0.767 | 1.000 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1000 | factual | 0.250 | 0.924 | 1.000 | 1.000 |
| hw-v600r024c10-ip-route-01-08#hw-v600r024c10-ip-route-01-08#c123 | troubleshoot | 0.600 | 0.931 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-01#hw-v600r025c00-alarm-01-01#c6 | troubleshoot | 0.375 | 0.824 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-44#hw-v600r025c00-alarm-01-44#c7 | troubleshoot | 1.000 | 0.838 | 1.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c14 | troubleshoot | 0.560 | 0.895 | 0.200 | 1.000 |
| hw-v600-case-01-03#hw-v600-case-01-03#c656 | troubleshoot | — | 0.936 | 1.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c19 | troubleshoot | 0.000 | 0.000 | 0.000 | 0.000 |
| hw-v600-case-01-03#hw-v600-case-01-03#c997 | troubleshoot | 0.400 | 0.803 | 1.000 | 1.000 |
| hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c204 | troubleshoot | 0.727 | 0.890 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-16#hw-v600r025c00-alarm-01-16#c22 | troubleshoot | 1.000 | 0.992 | 0.250 | 1.000 |
| cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c69 | troubleshoot | 0.800 | 0.957 | 0.000 | 1.000 |
| hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c57 | troubleshoot | 0.786 | 0.961 | 1.000 | 1.000 |
| hw-v600r024c10-eth-switch-01-10#hw-v600r024c10-eth-switch-01-10#c3 | troubleshoot | 0.000 | 0.984 | 0.917 | 0.000 |
| hw-v600r025c00-alarm-01-99#hw-v600r025c00-alarm-01-99#c45 | troubleshoot | 1.000 | 0.928 | 1.000 | 1.000 |
| hw-v600r025c00-eth-switch-01-03#hw-v600r025c00-eth-switch-01-03#c8 | troubleshoot | 1.000 | 0.973 | 1.000 | 1.000 |

## 跳过与失败（不造数）

- 跳过 0 条：无
- 单条失败 0 条：无

## 诚实的局限（caveats）

- - **judge 为异构模型**（deepseek（DEEPSEEK_MODEL env 值：deepseek-v4-flash））：消除与生成同模型的自评偏差（72B 基线的系统性风险），但异构 judge 对中文陈述抽取的校准同样未验证，绝对值仍只作相对对比；与 72B judge 的数值差异方向见对照表（纯 judge 后端差异）
- **ragas 指标 prompt 为英文**，语料/问答为中文混合：faithfulness 的陈述抽取与
  context_recall 的语句分类在中文上未做校准，绝对值只作相对基线（跨迭代对比用），
  不与公开英文 benchmark 直接可比
- ground truth 用期望子块全文拼 reference：多期望子块（multihop，本期未抽样）会稀释
  precision/recall 判分，故 multihop/reject 不在本期口径
- **本任务只测量不调参**；抽样 n=50，均值抽样误差不小（±0.1 量级），
  结论以跨版本相对变化为准
- RAGAS 评测的 contexts 用**子块文本**（ground truth 同为期望子块），而生成实际可见的是
  **父块窗口**（spec 规定口径）：faithfulness 只对生成可见上下文的子集打分，答案引用了
  父块窗口内、子块之外的内容时会被误判为不忠实——该系统性压低方向已知，跨运行一致，
  只影响绝对值不影响相对对比（装配修正另行单变量重测）
- 逐条分数中"—"为该条该指标 judge 调用失败（raise_exceptions=False下 NaN：TPM 限速
  429 / 余额不足 402 等 API 错误重试耗尽），未计入均值；
  各指标"非空计数"行即该均值的实际样本量——覆盖面过低的均值只作参考

