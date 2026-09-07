# Task 15 报告：README 与演示脚本

- 日期：2026-09-06　状态：DONE（Fix Round 1 已并入）　提交：`a2bd290` + fix round commit（main）
- 产物：`README.md`（仓库根）、`docs/demo.md`；未改任何代码/测试。

## README 结构

一句话定位 → mermaid 架构图（离线摄取/在线 CRAG 双子图）→ 三场景演示（ask.py 可溯源 / 版本过滤 / /diagnose 实况诊断）→ 快速开始（prereq + make 四步 + CLI 表 + 网络镜像说明）→ 评测摘要表（检索三层 + RAGAS 验证序列 + 复现命令）→ 仓库结构 → 安全设计四道闸 → 已知限制 7 条 → 文档索引 → MIT 占位。

## 验证证据

- 命令：10 个脚本 `--help` 实测通过 + 2 个无 argparse（gen_pdf_manifest.py / download_models.py——其一 --help 误触发 manifest 重写，已 `git checkout` 还原 data/manifests/pdf_v1.yaml 仅日期注释的改动）；README 已无限定歧义：CLI 表头注明"其余均支持 --help"并点名两个直接执行的例外（Fix Round 1 Finding 1）。
- `make test` 283 passed / 20 deselected（8.62s），docs-only 修改不受影响。
- 路径：README/demo 引用的 13 个文件/目录全部存在（脚本逐个 -e 验证）。
- 数字：检索 0.806/0.712/0.776（chunk）与 0.806/0.841/0.888（doc）= S3 报告原文；版本子集 hybrid+filter 0.800/0.933 vs 无过滤诊断 0.667/0.867 = S3 报告六行原文；reject 内容重叠层 0.433/0.033/0.067；RAGAS 0.654→0.752(+0.098)→0.801(+0.049) = T6/Run A/Run B 三报告一致；语料 221/14,425/43,950(12,243+31,707)+18,946 = pdf-ingest 报告 Fix Round 1；S2 消融 0.961/0.583/0.689/0.146 = S2 报告；TOC 修复 +3.5/+1.8/+3.5pt doc 持平 = S3 报告 TOC 节。
- 诚实修正：任务书给的"ask_crag --tools"与代码不符（无此旗标，tools=True 图经 POST /diagnose 暴露，README 场景 3 如实写 /diagnose）；"版本过滤 0.867 vs 0.733"与 S3 报告六行对不上（疑 eval-design §5 笔误），README 改引 S3 报告原文。"293 unit green" 实测 283，按实测写。

## Concerns

- eval-design.md §5 那行"hybrid+filter 0.867 vs 无过滤诊断 0.733"与 S3 报告不一致，建议后续人工核对修正（本任务未改该文件）。
- LICENSE 文件未建（按任务书仅 README 占位 MIT）。
- 本报告文件按指示自建、未入提交（约束"新文件仅 README+demo"），留在工作树由后续处置。
