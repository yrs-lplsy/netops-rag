# S3 RAGAS 四指标基线（50 条分层抽样，hybrid+rerank）

- 日期：2026-09-06
- git：`41b376b`

| 指标 | 值 |
|---|---|
| faithfulness（忠实度（答案可由 contexts 支撑）） | 0.654 |
| answer_relevancy（答案相关性（贴合问题）） | 0.800 |
| context_precision（上下文精度（期望内容排前）） | 0.881 |
| context_recall（上下文召回（期望子块被覆盖）） | 0.844 |
| 评测条数 n | 49 |
| 跳过（无 ground truth） | 0 |
| 单条失败 | 1 |
| faithfulness 非空计数 /49 | 48 |
| answer_relevancy 非空计数 /49 | 49 |
| context_precision 非空计数 /49 | 49 |
| context_recall 非空计数 /49 | 49 |


## 参数与判据

- golden：data/golden/s3_full.yaml（200 条；抽样域 factual 100、troubleshoot 40），分层比例抽样 n=50
  （seed=42，最大余数法配额）
- 检索：hybrid(dense+bm25+sparse|rerank)，top_k=5，recall_n=20，rrf_k=60（hybrid 时）
- 生成：Qwen/Qwen2.5-72B-Instruct（SiliconFlow），answer_with_citations 父块窗口（cap 6000）
- RAGAS：ragas 0.3.1，judge 同模型（temperature=0，LangchainLLMWrapper）；
  嵌入：本地 BAAI/bge-m3（dense，Bgem3LangchainEmbeddings）；
  ground truth = 期望子块全文（Milvus 点查拼接）；raise_exceptions=False
- 指标名对应：answer_relevancy 即 ragas ResponseRelevancy（0.3.x 的 .name）
- 观测：tracer=LangfuseTracer（langfuse 有密钥时自动选 Cloud，否则本地 JSONL 兜底），
  trace_id=3ce94d856a8cfa20eedad34f9a0856ea

## 与 T4 部分基线的对照

- T4 部分基线 0.655/0.881/0.987/0.810（n=9-11）仅供参考；本次重测与 T4 的数值差异
  同时受抽样集不同（n=50 vs 30）与有效覆盖不同（T4 各指标非空仅 9-11，
  余额耗尽所致）影响，不归因于系统变化

## 主结果

| 指标 | 均值 |
|---|---|
| faithfulness（忠实度（答案可由 contexts 支撑）） | 0.654 |
| answer_relevancy（答案相关性（贴合问题）） | 0.800 |
| context_precision（上下文精度（期望内容排前）） | 0.881 |
| context_recall（上下文召回（期望子块被覆盖）） | 0.844 |
| 评测条数 n | 49 |
| 跳过（无 ground truth） | 0 |
| 单条失败 | 1 |
| faithfulness 非空计数 /49 | 48 |
| answer_relevancy 非空计数 /49 | 49 |
| context_precision 非空计数 /49 | 49 |
| context_recall 非空计数 /49 | 49 |

## 逐条明细（n=49）

| qid | qtype | faithfulness | answer_relevancy | context_precision | context_recall |
|---|---|---|---|---|---|
| h3c-r1110-security-cmd#h3c-r1110-security-cmd#c100 | factual | — | 0.957 | 0.950 | 1.000 |
| hw-v600r024c10-ip-route-01-12#c7#ver | factual | 0.400 | 0.910 | 0.917 | 0.750 |
| hw-v600r025c00-eth-switch-01-10#c26#ver | factual | 0.000 | 0.752 | 1.000 | 0.429 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1004 | factual | 0.727 | 0.931 | 1.000 | 0.889 |
| hw-v600r024c10-security-01-08#hw-v600r024c10-security-01-08#c17 | factual | 0.833 | 0.779 | 1.000 | 0.167 |
| hw-v600r025c00-alarm-01-67#hw-v600r025c00-alarm-01-67#c15 | factual | 0.333 | 0.873 | 1.000 | 0.750 |
| hw-v600r025c00-alarm-01-105#hw-v600r025c00-alarm-01-105#c1000 | factual | 0.500 | 0.904 | 1.000 | 1.000 |
| hw-v600r025c00-security-01-24#hw-v600r025c00-security-01-24#c3 | factual | 0.571 | 0.881 | 1.000 | 1.000 |
| hw-v600r024c10-ip-route-01-09#c71#ver | factual | 0.500 | 0.819 | 1.000 | 0.091 |
| h3c-r1110-security-cfg#h3c-r1110-security-cfg#c100 | factual | 0.625 | 0.912 | 1.000 | 1.000 |
| cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c106 | factual | 0.750 | 0.879 | 0.679 | 0.400 |
| hw-v600r024c10-ip-route-01-05#c87#ver | factual | 1.000 | 0.626 | 0.750 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1 | factual | 1.000 | 0.628 | 1.000 | 1.000 |
| cisco-c9300-17.9-vlan-cg#cisco-c9300-17.9-vlan-cg#c10 | factual | 1.000 | 0.864 | 0.679 | 0.000 |
| hw-v600r025c00-eth-switch-01-11#c57#ver | factual | 0.857 | 0.790 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cfg#h3c-r1110-l2sw-cfg#c105 | factual | 0.750 | 0.948 | 1.000 | 0.750 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1002 | factual | 0.833 | 0.972 | 1.000 | 1.000 |
| hw-v600r025c00-eth-switch-01-06#hw-v600r025c00-eth-switch-01-06#c10 | factual | 0.667 | 0.563 | 0.950 | 1.000 |
| hw-v600r025c00-ip-route-01-08#hw-v600r025c00-ip-route-01-08#c100 | factual | 0.800 | 0.961 | 1.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1002 | factual | 0.350 | 0.850 | 0.887 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c100 | factual | 0.600 | 0.747 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cmd#h3c-r1110-l2sw-cmd#c102 | factual | 0.950 | 0.803 | 1.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1004 | factual | 1.000 | 0.832 | 0.950 | 1.000 |
| hw-v600r025c00-alarm-01-55#hw-v600r025c00-alarm-01-55#c15 | factual | 0.750 | 0.809 | 1.000 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1001 | factual | 0.800 | 0.946 | 1.000 | 1.000 |
| cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c10 | factual | 0.500 | 0.812 | 0.806 | 1.000 |
| h3c-r1110-security-cmd#h3c-r1110-security-cmd#c1001 | factual | 0.571 | 0.932 | 1.000 | 1.000 |
| cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c1001 | factual | 0.500 | 0.000 | 0.000 | 0.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1002 | factual | 1.000 | 0.898 | 1.000 | 1.000 |
| hw-v600r025c00-eth-switch-01-03#c30#ver | factual | 0.500 | 0.769 | 1.000 | 1.000 |
| hw-v600r025c00-security-01-18#hw-v600r025c00-security-01-18#c15 | factual | 0.667 | 0.876 | 0.867 | 1.000 |
| h3c-r1110-l2sw-cmd#h3c-r1110-l2sw-cmd#c103 | factual | 0.500 | 0.845 | 1.000 | 1.000 |
| hw-v600r024c10-eth-switch-01-03#hw-v600r024c10-eth-switch-01-03#c10 | factual | 1.000 | 0.669 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cfg#h3c-r1110-l2sw-cfg#c100 | factual | 1.000 | 0.823 | 0.867 | 1.000 |
| hw-v600r025c00-security-01-09#hw-v600r025c00-security-01-09#c1 | factual | 0.500 | 0.679 | 1.000 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1000 | factual | 0.250 | 0.754 | 1.000 | 1.000 |
| hw-v600r024c10-ip-route-01-08#hw-v600r024c10-ip-route-01-08#c123 | troubleshoot | 0.714 | 0.913 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-01#hw-v600r025c00-alarm-01-01#c6 | troubleshoot | 0.400 | 0.890 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-44#hw-v600r025c00-alarm-01-44#c7 | troubleshoot | 1.000 | 0.783 | 1.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c14 | troubleshoot | 0.438 | 0.849 | 0.200 | 1.000 |
| hw-v600-case-01-03#hw-v600-case-01-03#c656 | troubleshoot | 0.000 | 0.898 | 1.000 | 0.714 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c19 | troubleshoot | 0.000 | 0.000 | 0.804 | 0.400 |
| hw-v600-case-01-03#hw-v600-case-01-03#c997 | troubleshoot | 0.571 | 0.682 | 1.000 | 1.000 |
| hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c204 | troubleshoot | 0.875 | 0.898 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-16#hw-v600r025c00-alarm-01-16#c22 | troubleshoot | 1.000 | 0.806 | 0.887 | 1.000 |
| cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c69 | troubleshoot | 0.500 | 0.794 | 0.000 | 1.000 |
| hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c57 | troubleshoot | 1.000 | 0.913 | 1.000 | 1.000 |
| hw-v600r024c10-eth-switch-01-10#hw-v600r024c10-eth-switch-01-10#c3 | troubleshoot | 0.368 | 0.964 | 0.000 | 0.000 |
| hw-v600r025c00-alarm-01-99#hw-v600r025c00-alarm-01-99#c45 | troubleshoot | 0.923 | 0.804 | 1.000 | 1.000 |

## 跳过与失败（不造数）

- 跳过 0 条：无
- 单条失败 1 条：`hw-v600r025c00-eth-switch-01-03#hw-v600r025c00-eth-switch-01-03#c8` RateLimitError("Error code: 429 - {'code': 50602, 'message': 'Request was rejected due to rate limiting. Details: TPM limit reached.', 'data': None}")

## 诚实的局限（caveats）

- **judge 与生成同模型**（Qwen2.5-72B）：自评偏差（self-preference）系统性风险存在，
  faithfulness 可能偏高；后续可换异构 judge（如 DeepSeek-V3）对照
- **ragas 指标 prompt 为英文**，语料/问答为中文混合：faithfulness 的陈述抽取与
  context_recall 的语句分类在中文上未做校准，绝对值只作相对基线（T6 迭代对比用），
  不与公开英文 benchmark 直接可比
- ground truth 用期望子块全文拼 reference：多期望子块（multihop，本期未抽样）会稀释
  precision/recall 判分，故 multihop/reject 不在本期口径
- **本任务只测量不调参**（调参属 T6）；抽样 n=50，均值抽样误差不小（±0.1 量级），
  结论以跨版本相对变化为准
- RAGAS 评测的 contexts 用**子块文本**（ground truth 同为期望子块），而生成实际可见的是
  **父块窗口**（spec 规定口径）：faithfulness 只对生成可见上下文的子集打分，答案引用了
  父块窗口内、子块之外的内容时会被误判为不忠实——该系统性压低方向已知，跨运行一致，
  只影响绝对值不影响相对对比
- 逐条分数中"—"为该条该指标 judge 调用失败（raise_exceptions=False 下 NaN：SiliconFlow
  TPM 限速 429 / 余额不足 402 等 API 错误重试耗尽），未计入均值；
  各指标"非空计数"行即该均值的实际样本量——覆盖面过低的均值只作参考

