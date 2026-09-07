# S3 RAGAS 四指标（50 条分层抽样，judge=deepseek，assembly=parent-window，prompt=v3，scoring=artifact-stripped，hybrid+rerank）

- 日期：2026-09-08
- git：`f5779fa`（**Run D / RAGAS 最终口径**：prompt=v3 = Run C 收紧版 + 两轮对比陈述引导
  `9892596`+`17f90e9`；评分=judge 可见答案经 `strip_eval_artifacts` 剥离伪影，ef9c4cb）

| 指标 | 值 |
|---|---|
| faithfulness（忠实度（答案可由 contexts 支撑）） | 0.851 |
| answer_relevancy（答案相关性（贴合问题）） | 0.904 |
| context_precision（上下文精度（期望内容排前）） | 0.851 |
| context_recall（上下文召回（期望子块被覆盖）） | 0.884 |
| 评测条数 n | 50 |
| 跳过（无 ground truth） | 0 |
| 单条失败 | 0 |
| 生成缓存命中（跳过生成 LLM） | 50 |
| 伪影剥离命中（剥离后变短的条数） | 44 |
| 剥离字符总数 | 12392 |
| faithfulness 非空计数 /50 | 45 |
| answer_relevancy 非空计数 /50 | 50 |
| context_precision 非空计数 /50 | 50 |
| context_recall 非空计数 /50 | 50 |


## 参数与判据

- golden：data/golden/s3_full.yaml（200 条；抽样域 factual 100、troubleshoot 40），分层比例抽样 n=50
  （seed=42，最大余数法配额）
- 检索：hybrid(dense+bm25+sparse|rerank)，top_k=5，recall_n=20，rrf_k=60（hybrid 时）
- 生成：Qwen/Qwen2.5-72B-Instruct（SiliconFlow），answer_with_citations 父块窗口（cap 6000）；
  生成缓存命中 50/50 条——50 条答案全部为 v3 prompt 产物：49 条由首轮运行生成并落盘
  （该轮判分阶段被中断，生成缓存已持久化），1 条由 60s 判分轮补生成；**最终 240s 判分轮
  零生成调用**。50/50 均与 T6/Run B/C 答案不同（v3 为被测变量）
- 装配：**parent-window**（RAGAS contexts 经 answer.build_generation_contexts 取父块窗口，与生成 LLM 实际可见片段严格一致——T6 验证序列 Run B 装配修正）
- 评分口径：**artifact-stripped**（judge 只见 ragas_runner.strip_eval_artifacts 剥离后的答案——
  剥【出处】脚注块与"（手册片段未涉及，建议人工确认）"逃生舱句；两者恒被判无据陈述、
  系统性压低 faithfulness（0.333=1/3 定量实证）并拖垮 relevancy；原始答案仍入生成缓存与
  逐条记录（raw_len/stripped_len）可审计）
- RAGAS：ragas 0.3.1，judge=deepseek（DEEPSEEK_MODEL env 值：deepseek-v4-flash）（temperature=0，LangchainLLMWrapper）；
  嵌入：本地 BAAI/bge-m3（dense，Bgem3LangchainEmbeddings）；
  ground truth = 期望子块全文（Milvus 点查拼接）；raise_exceptions=False
- 指标名对应：answer_relevancy 即 ragas ResponseRelevancy（0.3.x 的 .name）
- 观测：tracer=LangfuseTracer（langfuse 有密钥时自动选 Cloud，否则本地 JSONL 兜底），
  trace_id=45d8740d1db9482435bf17a4264595bc

## 与 T6 基线对照（差异 = judge+装配 双变量，非单变量）

同抽样（50 条，seed=42）、同生成（Qwen2.5-72B，生成缓存命中）；但 T6 基线为 child-chunks 装配、本次为 parent-window，judge 后端与装配同时变化——
本行 Δ 为双变量（judge+装配）合成差异，单变量结论另见：Run A 对照行（纯 judge 效应 f+0.098）与 Run B-vs-Run A 对照行（纯装配效应 f+0.049）；非空计数 <40 的指标只作参考。

| 指标 | 本次（parent-window） | T6 基线（judge=Qwen2.5-72B@SiliconFlow，assembly=child-chunks）（n=48-49） | Δ |
|---|---|---|---|
| 忠实度（答案可由 contexts 支撑） | 0.851 | 0.654 | +0.197 |
| 答案相关性（贴合问题） | 0.904 | 0.800 | +0.104 |
| 上下文精度（期望内容排前） | 0.851 | 0.881 | -0.030 |
| 上下文召回（期望子块被覆盖） | 0.884 | 0.844 | +0.040 |

## 与 Run B / Run C 对照（最终口径 vs 历史两轮）

同抽样（50 条，seed=42）、同 judge（deepseek-v4-flash）、同装配（parent-window）、同检索。
Run D 相对 Run C 的差异为**双变量**：①生成 SYSTEM prompt v2→v3（+两轮对比陈述引导，
答案已变：50/50 重新生成）；②评分口径 artifact-stripping（judge 可见答案剥【出处】脚注与
逃生舱句——Run C 报告已实证脚注恒判无据、单条 0.333=纯脚注伪影）。**Δ(C→D) 为两效应
合成，未做交叉实验（用 Run C 答案+剥离重判）拆分，机械效应与真实语义收益不可分**；
有效 n <40 的均值只作参考（本次四指标均 ≥45）。

| 指标 | **Run D（v3+stripped）**（有效 n） | Run C（v2 tightened，未剥离）（有效 n） | Δ(D−C) | Run B（旧 prompt，未剥离）（有效 n） | Δ(D−B) |
|---|---|---|---|---|---|
| 忠实度（答案可由 contexts 支撑） | 0.851（45/50） | 0.755（42/50） | +0.096 | 0.801（46/50） | +0.050 |
| 答案相关性（贴合问题） | 0.904（50/50） | 0.792（49/50） | +0.112 | 0.856（49/50） | +0.048 |
| 上下文精度（期望内容排前） | 0.851（50/50） | 0.883（48/50） | -0.032 | 0.850（48/50） | +0.001 |
| 上下文召回（期望子块被覆盖） | 0.884（50/50） | 0.883（48/50） | +0.001 | 0.880（48/50） | +0.004 |

### Δ 归因（如实）

- **f +0.096 / rel +0.112（vs Run C）**：主要归因两机制——①剥离的**机械效应**：Run C 的
  【出处】脚注与逃生舱句每条恒被判无据陈述（压 f）且拉低答案-问题嵌入相似度（压 rel，
  Run C 报告 relevancy trade-off 节），Run D 中 44/50 条被剥离共 12392 字符，这部分分值
  回升**不是答案语义变化**；②v3 prompt 的真实语义收益（对比陈述引导下答案更贴合问题
  语义）——两部分占比未拆分。方向上「v3 至少无害、剥离后 f/rel 为历史最高」成立；
  「v3 相对 v2 的净语义增益 = +0.096」**不成立**（含机械效应）。
- **prec -0.032（vs Run C）**：检索侧完全未动，prec 的波动属 judge 无关的 context 指标
  抽样/判分噪声（±0.1 量级），不解读为退化。
- **vs Run B 全指标不劣**（f +0.050 / rel +0.048 / prec +0.001 / rec +0.004）：最终口径
  相对最初 parent-window 口径四指标全部持平或改善，且该 Δ 同样含 prompt+剥离双变量。
- **vlan 诊断工具修复（`f5779fa`）不在本评测集生效路径**：RAGAS 集为手册问答
  （factual/troubleshoot），无设备实况问题；该修复只影响 e2e 排障口径（见
  2026-09-07-e2e-vlan-iter.md §8-§12，vlan 类 1/6→5/6、总 29/30）。

## 主结果

| 指标 | 均值 |
|---|---|
| faithfulness（忠实度（答案可由 contexts 支撑）） | 0.851 |
| answer_relevancy（答案相关性（贴合问题）） | 0.904 |
| context_precision（上下文精度（期望内容排前）） | 0.851 |
| context_recall（上下文召回（期望子块被覆盖）） | 0.884 |
| 评测条数 n | 50 |
| 跳过（无 ground truth） | 0 |
| 单条失败 | 0 |
| 生成缓存命中（跳过生成 LLM） | 50 |
| 伪影剥离命中（剥离后变短的条数） | 44 |
| 剥离字符总数 | 12392 |
| faithfulness 非空计数 /50 | 45 |
| answer_relevancy 非空计数 /50 | 50 |
| context_precision 非空计数 /50 | 50 |
| context_recall 非空计数 /50 | 50 |

## 逐条明细（n=50）

| qid | qtype | faithfulness | answer_relevancy | context_precision | context_recall |
|---|---|---|---|---|---|
| h3c-r1110-security-cmd#h3c-r1110-security-cmd#c100 | factual | 1.000 | 1.000 | 0.756 | 1.000 |
| hw-v600r024c10-ip-route-01-12#c7#ver | factual | — | 0.833 | 1.000 | 1.000 |
| hw-v600r025c00-eth-switch-01-10#c26#ver | factual | 0.800 | 0.875 | 0.867 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1004 | factual | 1.000 | 0.978 | 1.000 | 1.000 |
| hw-v600r024c10-security-01-08#hw-v600r024c10-security-01-08#c17 | factual | 1.000 | 0.992 | 1.000 | 0.778 |
| hw-v600r025c00-alarm-01-67#hw-v600r025c00-alarm-01-67#c15 | factual | 1.000 | 0.981 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-105#hw-v600r025c00-alarm-01-105#c1000 | factual | 1.000 | 0.903 | 1.000 | 1.000 |
| hw-v600r025c00-security-01-24#hw-v600r025c00-security-01-24#c3 | factual | 1.000 | 0.995 | 0.867 | 1.000 |
| hw-v600r024c10-ip-route-01-09#c71#ver | factual | 0.000 | 0.852 | 1.000 | 0.421 |
| h3c-r1110-security-cfg#h3c-r1110-security-cfg#c100 | factual | 0.800 | 0.946 | 1.000 | 1.000 |
| cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c106 | factual | 0.875 | 0.936 | 1.000 | 0.083 |
| hw-v600r024c10-ip-route-01-05#c87#ver | factual | 0.833 | 0.799 | 1.000 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1 | factual | 1.000 | 0.959 | 1.000 | 1.000 |
| cisco-c9300-17.9-vlan-cg#cisco-c9300-17.9-vlan-cg#c10 | factual | 0.500 | 0.943 | 0.000 | 0.000 |
| hw-v600r025c00-eth-switch-01-11#c57#ver | factual | 0.333 | 0.989 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cfg#h3c-r1110-l2sw-cfg#c105 | factual | 0.909 | 0.997 | 1.000 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1002 | factual | 1.000 | 0.984 | 0.887 | 1.000 |
| hw-v600r025c00-eth-switch-01-06#hw-v600r025c00-eth-switch-01-06#c10 | factual | 1.000 | 0.712 | 0.867 | 1.000 |
| hw-v600r025c00-ip-route-01-08#hw-v600r025c00-ip-route-01-08#c100 | factual | 0.889 | 0.944 | 1.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1002 | factual | — | 0.860 | 0.917 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c100 | factual | 0.556 | 0.864 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cmd#h3c-r1110-l2sw-cmd#c102 | factual | 0.864 | 0.956 | 0.750 | 0.500 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c1004 | factual | 0.882 | 0.990 | 0.833 | 1.000 |
| hw-v600r025c00-alarm-01-55#hw-v600r025c00-alarm-01-55#c15 | factual | 0.600 | 0.972 | 0.750 | 1.000 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1001 | factual | 1.000 | 0.963 | 0.833 | 1.000 |
| cisco-c9300-17.9-layer2-cg#cisco-c9300-17.9-layer2-cg#c10 | factual | 1.000 | 0.951 | 1.000 | 1.000 |
| h3c-r1110-security-cmd#h3c-r1110-security-cmd#c1001 | factual | 1.000 | 0.946 | 1.000 | 1.000 |
| cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c1001 | factual | 0.846 | 0.000 | 0.000 | 0.400 |
| h3c-r1110-iproute-cmd#h3c-r1110-iproute-cmd#c1002 | factual | 1.000 | 0.999 | 1.000 | 1.000 |
| hw-v600r025c00-eth-switch-01-03#c30#ver | factual | 1.000 | 0.850 | 1.000 | 1.000 |
| hw-v600r025c00-security-01-18#hw-v600r025c00-security-01-18#c15 | factual | 1.000 | 0.952 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cmd#h3c-r1110-l2sw-cmd#c103 | factual | 1.000 | 0.684 | 0.917 | 1.000 |
| hw-v600r024c10-eth-switch-01-03#hw-v600r024c10-eth-switch-01-03#c10 | factual | 0.750 | 0.971 | 1.000 | 1.000 |
| h3c-r1110-l2sw-cfg#h3c-r1110-l2sw-cfg#c100 | factual | 1.000 | 0.978 | 1.000 | 1.000 |
| hw-v600r025c00-security-01-09#hw-v600r025c00-security-01-09#c1 | factual | 1.000 | 0.756 | 1.000 | 1.000 |
| h3c-r1110-iproute-cfg#h3c-r1110-iproute-cfg#c1000 | factual | 1.000 | 0.968 | 1.000 | 1.000 |
| hw-v600r024c10-ip-route-01-08#hw-v600r024c10-ip-route-01-08#c123 | troubleshoot | 0.316 | 0.986 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-01#hw-v600r025c00-alarm-01-01#c6 | troubleshoot | 0.667 | 0.986 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-44#hw-v600r025c00-alarm-01-44#c7 | troubleshoot | 1.000 | 0.987 | 1.000 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c14 | troubleshoot | 1.000 | 0.899 | 0.367 | 1.000 |
| hw-v600-case-01-03#hw-v600-case-01-03#c656 | troubleshoot | — | 0.941 | 0.917 | 1.000 |
| cisco-c9300-17.9-security-cg#cisco-c9300-17.9-security-cg#c19 | troubleshoot | 0.842 | 0.653 | 0.000 | 0.000 |
| hw-v600-case-01-03#hw-v600-case-01-03#c997 | troubleshoot | 0.500 | 0.865 | 0.917 | 1.000 |
| hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c204 | troubleshoot | 0.917 | 0.898 | 1.000 | 1.000 |
| hw-v600r025c00-alarm-01-16#hw-v600r025c00-alarm-01-16#c22 | troubleshoot | — | 0.990 | 0.250 | 1.000 |
| cisco-c9300-17.9-ip-routing-cg#cisco-c9300-17.9-ip-routing-cg#c69 | troubleshoot | 1.000 | 0.992 | 0.000 | 1.000 |
| hw-v600r024c10-ip-route-01-07#hw-v600r024c10-ip-route-01-07#c57 | troubleshoot | 0.600 | 0.917 | 1.000 | 1.000 |
| hw-v600r024c10-eth-switch-01-10#hw-v600r024c10-eth-switch-01-10#c3 | troubleshoot | — | 0.990 | 0.950 | 0.000 |
| hw-v600r025c00-alarm-01-99#hw-v600r025c00-alarm-01-99#c45 | troubleshoot | 1.000 | 0.897 | 1.000 | 1.000 |
| hw-v600r025c00-eth-switch-01-03#hw-v600r025c00-eth-switch-01-03#c8 | troubleshoot | 1.000 | 0.898 | 0.887 | 1.000 |

## 跳过与失败（不造数）

- 跳过 0 条：无
- 单条失败 0 条：无

## 诚实的局限（caveats）

- **judge 为异构模型**（deepseek（DEEPSEEK_MODEL env 值：deepseek-v4-flash））：消除与生成同模型的自评偏差（72B 基线的系统性风险），但异构 judge 对中文陈述抽取的校准同样未验证，绝对值仍只作相对对比；与 72B judge 的数值差异方向见对照表（纯 judge 后端差异）
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
- **judge 两轮历史（如实）**：首次运行（生成 49/50 后判分阶段被外部中断，判分期极短）
  之后，第一次完整判分误用脚本默认 timeout=60s（Run B/C 判分口径为 240s），79 次
  TimeoutError 致 f 有效 n 仅 15、rec 仅 18（f 0.878/rec 0.861 @ n=15/18，该轮数字
  **作废不用**，未进入任何结论）；按 Run C 同口径 timeout=240s 重判后 TimeoutError 降为
  5 次，四指标有效 n=45/50/50/50 全部 ≥40，本报告数字以 240s 轮为准（trace 45d8740d…；
  60s 轮 trace 979fd966… 的同名报告文件已被 240s 轮覆盖）。judge 不缓存，60s/240s 两轮
  判分成本均实付（见下）。f 有效 n=45 中 5 条 NaN 的答案均长偏长（与 Run C 的"长答案
  更易超时"观察同向），均值基底与 Run C（42 条）构成不同，跨轮 Δ 解读需打此折扣
- **成本与 402**：SiliconFlow 生成共 50 次 v3 答案（49 + 1，分布见上）+ 首轮 1 条生成失败
  重试（沉没）；judge DeepSeek 实付 ≈ ¥15.2（余额 26.70 → 19.21 → 11.54，其中 60s 作废轮
  与 240s 终版轮各约一半），超出单轮 ~¥8-9 预估的原因为 timeout=60s 作废轮；
  60s/240s 两轮日志 **402 事件 0 次、429 事件 0 次**，单条生成失败 0 次
- **生成缓存语义（教训复用）**：cache key 不含 prompt 内容——v3 prompt 沿用 Run C 缓存
  文件会静默命中旧答案，故 Run D 另立缓存文件
  `data/llm_cache/ragas_gen_s50_seed42_runD_final.json`（Run C 缓存原样保留）

