# T14 VLAN 生成端迭代：6 任务重测（2026-09-08）

## 1. 口径与运行环境

- **重测对象**：t23-t28（access_vlan_wrong 6 条；基线 conclusion_correct=0/6、tools_reasonable=6/6，
  见 [2026-09-07-e2e-30.md](2026-09-07-e2e-30.md) §5.2/§8）。
- **唯一变量**：生成 SYSTEM prompt 两轮迭代（`9892596`：通用对比陈述引导；`17f90e9`：追加
  「失 IP + 另一 VLAN 子接口存在 = 迁移证据、禁止『可能无关』hedge」）。检索、诊断工具映射、
  判分校准、temperature 0.2 全部未动；`【出处】`页脚与「未找到」兜底措辞不变。
- **运行**：`scripts/run_e2e.py --tasks data/tasks/e2e_30.yaml --ids t23,t24,t25,t26,t27,t28`
  （每轮 18 次 LLM 调用 = 6 题 × 3）；逐字记录
  `data/llm_cache/t14_results/agent-20260908-002355.jsonl`（迭代 1）、
  `agent-20260908-004551.jsonl`（迭代 2）。
- **迭代预算**：按批准上限 2 轮 prompt 迭代执行，2/2 用满即停（未动工具映射）。

## 2. 结果（conclusion / tools 分列）

| 轮 | prompt | conclusion_correct | tools_reasonable | 数据 |
| --- | --- | --- | --- | --- |
| 基线（2026-09-07） | v2 收紧+实况认可 | 0/6 | 6/6 | agent-20260907-* |
| 迭代 1（9892596） | +通用对比陈述引导 | **0/6** | 6/6 | agent-20260908-002355 |
| 迭代 2（17f90e9） | +失IP+新子接口=迁移证据、禁 hedge | **1/6** | 6/6 | agent-20260908-004551 |

**预期「多数翻盘」未发生**（1/6）；两轮迭代均未达多数翻转，按协议如实记录并停止。

### 迭代 2 逐条 verdict

| 任务 | 故障 | conclusion | 迁移陈述证据（逐字摘录） |
| --- | --- | --- | --- |
| t23 | acc1 retag→200 | **✓** | 「VLAN100的地址已经从`eth1.100`迁移至`eth1.200`，但`eth1.200`接口当前处于down状态」——方向正确，PASS |
| t24 | acc1 retag→300 | ✗ | 全文无迁移陈述（len 2395 长篇展开手册步骤），judge：「仅泛泛说配置有问题」 |
| t25 | acc1 wrong_port→eth2 | ✗ | 陈述了迁移但**方向反了**：「VLAN100 的地址已从 `eth2.100` 迁移至 `eth1.100`」（期望 eth1.100→eth2.100） |
| t26 | core1 retag→200 | ✗ | 仅提「eth2.100 无 IPv4 地址」，未提 eth2.200 |
| t27 | core1 retag→300 | ✗ | 无迁移陈述（len 219 短答） |
| t28 | core1 wrong_port→eth3 | ✗ | 「错误地认为迁移到了 eth2」（judge 逐字） |

## 3. 归因（诚实，逐字证据）

1. **迭代 1 无效的机制**：通用对比陈述引导的前提是「实况显示地址在接口间移动」，但
   `show_vlan`（FRR 无 vlan 插件回退 `show interface brief`）对 **down 子接口不显示地址列**——
   t23 实况只有 `eth1.100 up（仅链路本地地址）/ eth1.200 down（地址列空白）`，迁移后的
   地址值**在可见证据中不存在**。模型在收紧约束（逐论断须有原文依据）下正确地拒绝断言
   迁移，退回「eth1.200 可能是一个无关的子接口」（t23 迭代 1 逐字）。
2. **迭代 2 部分有效但方向不可判定**：把「失 IP + 另一 VLAN 子接口存在」钉为迁移证据、
   禁止无关化措辞后，4/6 条答案出现了迁移陈述（t23/t25/t26/t28），但**方向正确率 1/4**
   （t25 方向反、t28 目的地错）——两处可观测事实（谁失了 IP、谁存在）不能判定「地址去了哪」，
   模型实际在猜。t24/t27 仍未触发引导。
3. **证据链缺口的真实位置**：running-config 才含闭合证据（注入核验序列
   `interface eth1.100 → no ip address 10.100.0.2/24 → interface eth1.200 → description 迁移 → ip address 10.100.0.2/24`，
   见 faults.py 注入实现），但 vlan 类诊断映射只有 `("vlan",) → ("show_vlan",)`，从不取
   running-config。**与 cost 类修复前完全同构**（cost 类补 `get_running_config` 后 0/7→7/7）。
   该修复属诊断映射/图结构变更，不在本轮批准范围（本轮为生成端 prompt 迭代），**未擅动**，
   留待人工决策。
4. 基线报告 §5.2 的「证据链已闭合（show_vlan 单工具输出同时含两事实）」表述经本轮逐字
   复核**需要修正**：「新标签铁证」（新子接口存在、down）确实在，但「失 IP」侧的地址值与
   「新接口持 IP」侧的地址值都不可见——迁移语义按收紧口径不可 grounded 断言，tools 6/6
   与 conclusion 0/6 并存的根因是证据可见性而非生成能力不足。

## 4. 更新后的 e2e 最终口径

| 指标 | 前口径 | **本轮后口径** | 目标 |
| --- | --- | --- | --- |
| conclusion_correct（30 题） | 24/30（80.0%） | **25/30（83.3%）** | 83.3%（25/30）**达标** |
| tools_reasonable（30 题） | 30/30 | 30/30 | — |
| VLAN 标签改错（6 题） | 0/6 | 1/6（t23） | — |

**组成口径如实声明**：25 = 24（旧 prompt 下测得，shutdown 6/6 + desc 9/9 + no_vlan 2/2 +
cost 7/7，这些类无失败且新增指令为 VLAN 场景专属）+ 1（新 prompt 下测得）。**未对 24 条做
新 prompt 全量复测**（预算原因），严格同口径全量数字需复测确认；本轮结论「VLAN 类 1/6、
总 25/30」按此构成成立。

## 5. lab 纪律与事件

- 两轮各 6 题 inject 全部核验通过、judge 0 解析失败、402/429 = 0、handoff = 0。
- 迭代 1 第 26 行后 post-reset 曾 `clean=False`（eth2.100 地址未恢复残留），由下一任务
  （t27）的重置自愈；迭代 2 全程 `reset_all_clean=true`。终态人工复核：4 主机
  diff_from_baseline 均空、healthy=True。

## 6. 复现

```bash
uv run python scripts/run_e2e.py --tasks data/tasks/e2e_30.yaml \
  --ids t23,t24,t25,t26,t27,t28
```

## 7. 结论与后续建议（仅记录，不擅动）

- 生成端 prompt 迭代（2 轮预算内）把 VLAN 类从 0/6 提到 1/6，总口径 25/30 达标；
  但「多数翻转」未达成，剩余缺口**不在生成措辞**（引导已生效、陈述已出现），在
  **证据可见性**：brief 输出对 down 接口不显示地址，迁移方向不可判定。
- 建议（待人工决策）：vlan 类诊断元组补 `get_running_config`（与 shutdown/cost 类
  同构闭合），预期可将迁移方向从「猜」变为「读」；工程把握与 cost 类修复相当。

---

# T14 续：vlan 类诊断映射补全 get_running_config 后重验（2026-09-08）

## 8. 修复内容（§7 建议获准执行）

- **唯一变量**：`src/netrag/agent/crag.py` 的 `_STATE_TOOL_MAP` 中 vlan 类
  `("vlan",) → ("show_vlan",)` 改为 `("vlan",) → ("show_vlan", "get_running_config")`
  （与 shutdown 三元组/cost 二元组同构收尾：show_vlan 证子接口存在/失链，running-config
  的 `no ip address`+迁移命令序列归因「地址迁到哪个新标签」，证据链闭合）。
  生成 prompt（v3，`17f90e9`）、检索、判分、temperature 0.2 全部未动。
- TDD：先改 `tests/test_crag_tools.py` 两处预期（mapping 表 + t30 优先级锚，
  t30 断言 `("show_vlan", "get_running_config")` 不回归）确认红，再改实现转绿；
  全量 `pytest -m "not milvus and not gpu"` 378 passed / 12 skipped。
- T7-T9 测试文件未动。

## 9. 重验结果（conclusion / tools 分列）

| 轮 | 诊断工具 | conclusion_correct | tools_reasonable | 数据 |
| --- | --- | --- | --- | --- |
| 迭代 2（17f90e9，单工具 show_vlan） | show_vlan | 1/6 | 6/6 | agent-20260908-004551 |
| **本轮（+get_running_config）** | show_vlan + get_running_config | **5/6** | 6/6 | agent-20260908-014849 |

运行：`run_e2e.py --ids t23..t28`，18 次 LLM 调用（6 题 × 3），0 错误、402/429=0、
handoff=0、`reset_all_clean=true`。

### 逐条 verdict

| 任务 | 故障 | conclusion | 迁移陈述证据（逐字摘录） |
| --- | --- | --- | --- |
| t23 | acc1 retag→200 | **✓** | 「`eth1.200` 接口的状态为 `down`，但配置了 IPv4 地址 `10.100.0.2/24`……已从 `eth1.100` 迁移至 `eth1.200`」 |
| t24 | acc1 retag→300 | ✗（judge 判） | **judge 误判**，见下（方向陈述正确：eth1.100→eth1.300） |
| t25 | acc1 wrong_port→eth2 | **✓** | 「`eth2.100` 子接口状态为 `up`，并且配置了 IPv4 地址 `10.100.0.2/24`……已从 `eth1.100` 迁移至 `eth2.100`」（迭代 2 方向曾反，本轮读 running-config 后正确） |
| t26 | core1 retag→200 | **✓** | 「eth2.200……配置了IPv4地址10.100.0.1/24……已从原子接口eth2.100迁移至子接口eth2.200」（迭代 2 曾只提 eth2.100） |
| t27 | core1 retag→300 | **✓** | 「`eth2.300` 接口状态为 `down`，但配置了IPv4地址 `10.100.0.1/24`……已从 `eth2.100` 迁移至 `eth2.300`」（迭代 2 曾无迁移陈述） |
| t28 | core1 wrong_port→eth3 | **✓** | 「`eth3.100`……配置了IPv4地址 `10.100.0.1/24`……已从 `eth2.100` 迁移至 `eth3.100`」（迭代 2 曾误指 eth2） |

- **修复机制与预期一致**：6/6 题诊断均调用双工具；迁移方向从「猜」（迭代 2 方向正确率
  1/4）变为「读」（本轮 6/6 答案迁移方向全部正确，含被判 FAIL 的 t24），证明缺口确在
  证据可见性而非生成能力。
- **t24 判为 FAIL 属 judge 误判（如实记录，官方分不改）**：answer 逐字
  「`eth1.100` 接口的 IPv4 地址已消失……`eth1.300` 接口配置了 IPv4 地址 `10.100.0.2/24`……
  已从 `eth1.100` 迁移至 `eth1.300`」——与 expected_conclusion 一致且 grounded 于
  running-config 工具输出（`interface eth1.300` + `ip address 10.100.0.2/24`，工具 [7]）；
  judge reason「实际输出中 eth1.300 没有配置该地址」与该工具输出**直接矛盾**
  （judge 疑似只核对了 show_vlan 输出——down 子接口地址列空白，恰为本轮修复前的同款盲区）。
  judge 判分不改分，但该条按工具输出核验为 agent 正确。

## 10. 抽查不回归（--no-judge，3 题 × 2 调用 = 6 调用）

| 任务 | 工具调用 | 答案要点 | 结论 |
| --- | --- | --- | --- |
| t02（shutdown） | brief + neighbor + running（三元组不变） | eth3 down + shutdown 行 | 不回归 |
| t17（desc 乱码） | get_running_config（单工具不变） | description=xx-unknown-777 | 不回归 |
| t30（no_vlan） | show_vlan + get_running_config（新二元组） | eth1.100 IP 摘除确认 | 不回归 |

数据：agent-20260908-020028.jsonl；6 调用 0 错误、`reset_all_clean=true`。

## 11. lab 事件与恢复（如实记录）

- 首轮重跑 6 题全部「起跑前 OSPF 未收敛」跳过（agent-20260908-013524.jsonl，
  0 LLM 调用）：排查发现 clab 数据面链路丢失（core1 仅剩 lo+mgmt eth0，OSPF 邻居全空）
  ——容器曾被重启而 clab 链路未随之恢复。
- 恢复：`netops/clab-runner:0.79.0` 容器内 `deploy --reconfigure -t netops.clab.yml`
  原拓扑原配置重部（镜像全本地，无网络拉取），5 节点 running、链路重建，
  `wait_healthy()`=True 后方才重跑；Milvus 同因掉线，按 `make milvus-up` 同口径
  `docker compose up -d --pull never` 恢复（镜像本地命中）。

## 12. 更新后的 e2e 最终口径（本节为最终版，覆盖 §4）

| 指标 | 前口径（§4） | **本轮后最终口径** | 目标 |
| --- | --- | --- | --- |
| conclusion_correct（30 题） | 25/30（83.3%） | **29/30（96.7%）** | 83.3%（25/30）**超额达标** |
| tools_reasonable（30 题，判分覆盖内） | 30/30 | 30/30（24 基线 + vlan 6/6） | — |
| VLAN 标签改错（6 题） | 1/6 | **5/6** | — |

**组成口径如实声明**：29 = 24（早期 prompt 下测得：shutdown 6/6 + desc 9/9 + no_vlan 2/2 +
cost 7/7，这些类无失败；本轮 t02/t17/t30 抽查确认行为不回归，但**未对 24 条做全量复测**）
+ 5（本轮 v3 prompt + 双工具诊断下测得）。若计入 t24 的 judge 误判修正则为 30/30，
官方口径维持 29/30。

## 13. 复现

```bash
uv run python scripts/run_e2e.py --tasks data/tasks/e2e_30.yaml \
  --ids t23,t24,t25,t26,t27,t28          # vlan 6 题（本轮 5/6）
uv run python scripts/run_e2e.py --tasks data/tasks/e2e_30.yaml \
  --ids t02,t17,t30 --no-judge           # 抽查不回归（本轮通过）
```
