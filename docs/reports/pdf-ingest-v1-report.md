# PDF 摄取管线 v1 报告（pdf_v1）

日期：2026-09-05（Fix Round 1：2026-09-06）　范围：data/pdf/ 新语料入库 + chunks/chunks_naive 双索引重建 + ask 切换 HybridRetriever

## 1. 结论（Status: DONE）

- 238 个 PDF / 14,425 页入索引，`chunks` 45,744 行（12,330 父块 + 33,414 子块），`chunks_naive` 19,061 行；陈旧 c9311 数据清零。
- 验收两问（中/英）出处均命中 `cisco-c9300-17.9-vlan-cg`（面包屑可见），Qwen2.5-72B 生成连贯无乱码；7B 在中文问英文语料场景出现数字错乱/复读（A/B 见 §5），已把 `.env` 的 `LLM_MODEL` 切为 72B。
- 测试：`uv run pytest -q` 42 passed（含 milvus/gpu 标记 10 项，全部真机通过）；`-m "not milvus and not gpu"` 32 passed。

## 2. 入库统计

### 2.1 语料（data/manifests/pdf_v1.yaml，238 docs，由 scripts/gen_pdf_manifest.py 扫描生成）

| 厂商 | 文件 | 页数 | 跳过页(图片主导/空) | 书签标题命中/未命中 | 表格md | md字符 |
|---|---|---|---|---|---|---|
| Huawei (V600R025C00 四卷+告警+案例集, V600R024C10 三卷) | 228 | 9,125 | 71 | 5,009 / 207 | 6,236 | 9.65M |
| Cisco 17.9 (VLAN/Layer2/IP Routing/Security) | 4 | 1,790 | 48 | 2,289 / 4 | 1,031 | 3.06M |
| H3C R1110 (二层/IP路由/安全 × 配置指导+命令参考) | 6 | 3,510 | 29 | 6,083 / 745 | 84 | 3.60M |
| **合计** | **238** | **14,425** | **148** | **13,381 / 956 (93.3%)** | **7,351** | **16.3M** |

- 池中未入库 550 个 PDF（其余厂商卷、V600R024C10 未选卷、Cisco 其余 12 本、H3C 其余分册、华为各卷整本合集等）。
- ground truth markdown 全部提交 git（`data/processed_pdf/`，238 个 .md，约 23MB）；原始 650MB `data/pdf/` 入 `.gitignore`（与 data/raw 同策略，路径凭证在 manifest）。

### 2.2 索引（Milvus localhost:19530）

| collection | 重建前 | 重建后 | 说明 |
|---|---|---|---|
| chunks（hybrid: dense+BM25函数+bge稀疏） | 680 | **45,744** | = 12,330 父块(is_parent=true) + 33,414 子块 |
| chunks_naive（纯稠密对照） | 100 | **19,061** | chunk_naive(size=512, overlap=50) |
| 残留 c9311 陈旧数据 | 有 | **0** | drop 后重建随之清除 |

按厂商 children/parents/naive：huawei 21,820/4,641/12,636；cisco 4,457/2,185/2,049；h3c 7,137/5,504/4,376。

### 2.3 耗时

| 阶段 | 耗时 | 速率 |
|---|---|---|
| PDF→md 转换（23,550 页含 9 本误入的整本合集，后被剔除） | ~26 min | ~15 页/s（pdfplumber，含 find_tables） |
| 全量重建（md 复用，纯切分+embedding+入库，238 docs） | **12m14s** | children ~43/s（bge-m3 cuda:0 fp16, batch=64） |
| 首次全链路（转换+切分+embedding，247 docs） | 38m56s | 每文件一行进度 + 每 10 文件累计/ETA |

## 3. 管线实现

- **manifest**（`scripts/gen_pdf_manifest.py` → `data/manifests/pdf_v1.yaml`）：目录扫描+白名单规则，字段 vendor/model/sw_version/volume/doc_id/title/source_path；doc_id 全局唯一且含版本（如 `hw-v600r025c00-eth-switch-01-04`、`cisco-c9300-17.9-vlan-cg`、`h3c-r1110-l2sw-cfg`），生成时断言唯一性与文件存在性。
- **解析**（`src/netrag/ingestion/pdf_to_md.py` 重构）：
  - 文字行 `extract_words(x_tolerance=1.5)`（思科 PDF 默认 3.0 会把英文粘成 "ConfiguringVTP"，1.5 校准后正常且中文无损）；
  - 面包屑标题：PDF 书签（pypdfium2 outline）按目标页调度，与页面行「去空白相等」+相邻两行双序拼接匹配，升级为 markdown 标题（书签层级+2）；未匹配标题插页首兜底；
  - 页眉脚剔除：华为（系列名/「配置指南-」行/版权行）、思科（8pt 页眉脚 vs 10pt 正文，首2/末3行）、H3C（页码 1-11/罗马数字/目录点线）；
  - 表格 find_tables 按框线转 markdown 管道表，按 bbox 扣除表内文字后按几何位置插回正文流，跨页表（页首+同列数）自动续行；整页边框误检（>85% 页面积）丢弃；
  - 图片主导页跳过：剔页眉脚后 <50 字且有大图（≥15% 页面积）整页跳过（本次命中 29 页，另有 119 页纯空页）；
  - 段落重组还原中文硬换行；`#` 开头的命令注释行转义，防被 section_tree 当标题。
- **切分/索引**：复用 `chunker_structured`（表格/代码硬边界，面包屑入 chunk 元数据）、`bm25_field.build_bm25_text`、`hybrid_schema`/`naive_schema`；编排脚本 `scripts/ingest_pdf.py`（--limit/--filter 试跑、--reuse-md、--md-only、--skip-naive、分批 flush、逐文件进度行）。
- **BgeTokenCounter** 新增 `CachedTokenCounter`（切分器对行/块重复计数，大语料下 memo 砍掉大半 tokenize 开销）。

## 4. ask.py 改造

- 默认 `--retriever hybrid`（HybridRetriever 三路 RRF + bge-reranker-v2-m3 精排 + 父块回填，recall_n 提到 48），保留 `--retriever naive` 对照与 `--no-rerank`。
- 问句型号别名（9300/S17xx/S57xx/S67xx/R1110）自动下推为标量过滤 `model == "…"`（`--no-filter` 可关）。动因：中文问英文语料时 dense/BM25 排序都不敌同语言字面重叠，无过滤时中文问句 top5 全是华为/H3C 中文块；下推过滤后命中目标文档，是最可靠且可解释的跨语言路由。
- `answer.answer_with_citations` 生成改用父块回填的整节文本（≤6000 字/块）：子块常把「Before you begin」与 SUMMARY STEPS 表切开，7B 面对残缺步骤拒答；出处引用仍列子块面包屑+doc_id。
- 注意：`HybridRetriever.retrieve` 的 filters 只进 dense/sparse/bm25 各路的 AnnSearchRequest.expr，语义正确。

## 5. LLM 7B vs 72B A/B（问句：如何在 Catalyst 9300 上创建 VLAN 20，检索完全相同）

- **7B（Qwen2.5-7B-Instruct）**：出处正确命中 cisco VLAN 文档，但生成退化——
  > 「要创建 VLAN 22，，，，，，请按照以下 VLAN ID 为例进行配置… Ent Ent Ent Ent vlan entent VLAN ID。【出处】[4]] Catalyst 931 VLAN Configuration Guide…」
  英文问句下好一些但仍篡改数字（"VLAN 2 … Catalyst 9311 … vlan 211"）。
- **72B（Qwen2.5-72B-Instruct）**：两问均连贯、步骤与命令忠实于手册：
  > 「1. 进入全局配置模式 Device# configure terminal；2. 输入 VLAN ID… Device(config)# vlan 20；3.（可选）name test20；4. media ethernet；5. end；6. show vlan …」
- 结论：乱码/复读是 7B 对破碎/英文表格上下文的退化，检索侧无问题；**已把 .env 默认 LLM 切为 72B**（代码默认值 config.py 仍 7B，未动）。

## 6. 验收记录

1. `uv run python scripts/ask.py --retriever hybrid "如何在 Catalyst 9300 上创建 VLAN 20"`：出处 [1]-[5] 全部 `cisco-c9300-17.9-vlan-cg`，含面包屑「… > Configuring VLANs > How to Configure Normal-Range VLANs > Creating or Modifying an Ethernet VLAN」；72B 生成连贯（摘录见 §5）。
2. 英文 "How to create VLAN 20 on Catalyst 9300"：同样全命中 cisco VLAN 文档，输出连贯无乱码。
3. `uv run pytest -m "not milvus and not gpu"`：32 passed；`uv run pytest -q`（含 milvus/gpu 标记）：**42 passed**（gpu 测试真机加载 bge-m3/reranker 通过，milvus 集成测试对测试 collection 通过）。
4. 入库统计：§2。

## 7. 遇到的问题与决策

1. **思科 PDF 词粘连**：默认 x_tolerance=3 提取 "Eachdeviceinthe…"。校准 1.5 全局使用。
2. **书签与页内标题不逐字相等**：思科页眉与书签同名（每页误配成标题）→ 先剔页眉脚再匹配；H3C 编号与标题被拆成相邻两个 y 桶（"1.1"+"LoopBack接口…"）→ 相邻两行双序拼接匹配；仍未匹配的 956 个（93.3% 命中）插页首，报告计数。
3. **页脚混排字号躲过剔除**：华为页脚「文档版本 02 (2026-03-03) 版权所有…」不同字号被拆行，残留 "02 (2026-03-03) © 128" 碎片 → 行分组改为仅按 y（字号取行内最大），碎片整行归并后被剔除，跨页表格续行也随之生效。
4. **整本合集漏排除（已修复）**：华为卷目录名带 `(pdf)` 后缀而整本 PDF 文件名不带，首版 manifest 按目录名+`.pdf` 比对失败，9 本整本合集（~9,125 页）被误入库（索引曾达 72,061 行）。修复后 238 docs、45,744 行重建。
5. **命令注释行变假标题**：配置示例 `# 配置DeviceB` 被 section_tree 当 markdown 标题，面包屑被命令串污染 → 正文 `#` 行转义；md 首行 `# 题名` 在切分前剥离（题名经 meta 传入，避免面包屑重复）。
6. **H3C 表格多为无框线底纹表**：find_tables 检出率低（84 张），text 策略误检严重（整页当表）不可用，保持 lines 策略，未检出的表格以普通文本行保留（内容不丢，仅无表格结构）。
7. **VARCHAR max_length 按字节校验**：中文 3 字节/字，接近上限的 bm25_text/breadcrumb 可能超；ingest 侧按保守预算截断（bm25_text≤5000 字、breadcrumb≤600 字），chunk 文本上限（子 8000/父 65000 字符）远低于 65535 字节风险线之下（父块实际 ≤4000 token≈2.5 万字节）。
8. **data/pdf 不入 git**：650MB 原始语料与 data/raw 同策略忽略；可复现性由 manifest（路径白名单）+ data/processed_pdf（转换产物）承担。

## 8. 遗留与建议（v2）

- 中文问句跨语言检索仍推荐带型号；后续可加查询翻译/HyDE 或 bge-m3 双语 query 扩写，弱化对显式型号的依赖。
- 告警/日志类文档（华为告警处理 107 册）结构高度模板化，可做专门字段抽取（告警名/OID/恢复动作）提升精确召回。
- H3C 底纹表格如需结构化，可引入图像表格识别或按列 x 坐标聚类。
- `chunks_naive` 仅供 naive 对照，与 hybrid 共用同一批 md，二者 chunk 数差异（19,061 vs 33,414）来自切分策略不同，属预期。

## 9. 提交记录

- `fc82d82` chore: data/pdf 原始PDF语料(650MB)入 .gitignore，manifest+processed_pdf 作可复现凭证
- `fbd85ce` feat: pdf_v1 摄取管线——manifest 白名单生成器 + pdf_to_md 重构 + ingest_pdf 编排 + ask 换 HybridRetriever
- `499115b` fix: 整本手册合集漏排除 + ask 问句型号别名下推标量过滤（含 238 个 ground truth md 与 manifest）
- `bb8c4dc` feat: answer 生成改用父块回填上下文 + ground truth md/manifest 修正入库

## 10. Fix Round 1（2026-09-06，评审 4 项 Important/Minor 修复）

修复内容（commit `67259ce` fix + `6635c50` test）：

1. **表格提取 x_tolerance 校准（Important）**：`Table.extract()` 此前用 pdfplumber 默认 x_tolerance=3.0，英文单元格粘连（"CommandorAction"/"configureterminal"）；现与正文一致传 `x_tolerance=1.5`（pdf_to_md.py `_page_lines`）。
2. **父块上下文按子块开窗（Important）**：answer.py 由头部截断 `parent_text[:6000]` 改为 `_parent_window()`——定位子块在父块中的位置，取 [起点-1000, 起点+5000) 窗口、边界对齐行首/行尾，窗口外加 `…[前文省略]…`/`…[后文省略]…`；找不到子块位置时退回头部截断。
3. **测试补齐（Important）**：新增 21 个单测（32→53）。合成 PDF 构造器 `tests/synth_pdf.py`（手拼最小 PDF 字节：文字行/图片 XObject/outline，零新增依赖）；覆盖：图片主导页跳过（<50 字+大图 → 跳过，正常页保留）、页眉脚剔除（华为系列名/版权行/「告警处理」页眉、思科 8pt 页眉脚、H3C 页码/点线）、书签标题匹配（含「编号+标题拆两个 y 桶」的双序拼接匹配、未命中计数）、`_table_md`、manifest 白名单纯函数（(pdf) 后缀剥离/卷过滤/doc_id 含版本唯一/整本合集排除）、`_parent_window` 开窗（子块在后半/父块头部/找不到/短父块）。另修 test_config 环境变量污染（delenv 后断言默认值）。
4. **告警页眉 + 近空文档（fold Minor）**：strip 前缀表加「告警处理」；ingest 侧转换后 md <500 字符（扉页/目录类）warn+跳过不入库（本次 17 个）。

文档一致性：`.env.example` 的 LLM_MODEL 注明「PDF语料A/B后运行时默认72B（7B中文表格复读）」；config.py 代码默认值保持 7B 不动。

### 10.1 全量重转换+重建统计（238 docs，24m37s，含重转换 ~15min + 重切分重嵌入）

| 厂商 | 入索引文件 | 页数 | 跳过页(图/空) | 书签命中/未命中 | 表格md | md字符 |
|---|---|---|---|---|---|---|
| Huawei | 211（-17 近空） | 9,009 | 42 | 5,001 / 207 | 6,236 | 9.61M |
| Cisco | 4 | 1,790 | 48 | 2,289 / 4 | 1,031 | 3.08M |
| H3C | 6 | 3,510 | 29 | 6,083 / 745 | 84 | 3.60M |
| **合计** | **221** | **14,309** | **119** | **13,373 / 956** | **7,351** | **16.3M** |

索引：`chunks` 45,744 → **43,970**（父 12,243 + 子 31,727；行数下降 = 17 个近空 TOC 文档不再入库 + 告警页眉行剔除）；`chunks_naive` 18,981；c9311 残留 0。分批进度逐文件/每 10 文件打印照常。

### 10.2 cisco vlan-cg.md 表格行修复前后对比

修复前（粘连）：

```
| CommandorAction |
|---|
| enable Example: Device> enable |
| configureterminal Example: Device# configure terminal |
| vtpdomaindomain-name Example: Device(config)# vtp domain eng_group |
```

修复后（分词正常）：

```
| Command or Action |
|---|
| enable Example: Device> enable |
| configure terminal Example: Device# configure terminal |
| vtp domain domain-name Example: Device(config)# vtp domain eng_group |
```

全文档粘连变体检索计数：`CommandorAction|configureterminal|vtpdomaindomain` 修复后 0 次。

### 10.3 Fix Round 1 验收重跑

- `ask.py --retriever hybrid "如何在 Catalyst 9300 上创建 VLAN 20"`：出处 [1]-[5] 全命中 cisco-c9300-17.9-vlan-cg；72B 输出连贯（configure terminal → vlan 20 → name → media → end → show vlan，含命令示例，无乱码复读）。
- 英文同问：出处全命中 cisco-c9300-17.9-vlan-cg，输出连贯。
- `uv run pytest -m "not milvus and not gpu"`：**53 passed**（新增 21 计入）；全量 `pytest -q`：**63 passed**。

## 11. Fix Round 2（2026-09-06，表格单元格 CJK 空格合并）

**回归背景**：Fix Round 1 的 x_tolerance=1.5 只会切分不会合并——中文表格单元格内 (1.5, 3.0]pt 的对齐字距被当词界，产生 "接口类 型"/"Trunk接 口"/"属 性" 碎片（hw-eth-switch-01-04.md 65 个表格行含 CJK-空格-CJK，正文仅 12 行，差额即表格特有），并已随重转换固化进 6,236 个华为表格行和两个 collection。

**修复**（commit `3d5d608` + `790da78`）：pdf_to_md.py 新增 `_remerge_cjk(cell)`，仅表格路径（`_table_md`→`_cell`）调用，正文不动（1.5 分词是原本行为，不回归）。合并两类单空格：CJK-CJK、CJK-全角标点（，。、；：！？""''（）《》【】…—·）；ASCII-ASCII / ASCII-CJK 边界合法空格不动（"VLAN 20"、"Trunk 接口" 保留——"Trunk接 口" 合并的是 接_口）。新增 4 个单测（合并/保留/全角标点/逐列独立不跨列），单测 53→57。

### 11.1 hw-eth-switch-01-04.md 同一行修复前后对比

修复前（L114-120）：

```
| 接口类 型 | 接收帧处理过程 | 发送帧处理过程 |
| Trunk接 口 | 判断数据帧VLAN Tag： ● 无Tag，则添加本接口PVID Tag。当PVID 在允许通过的VLAN ID列表里时，则允许 该VLAN帧进入… | 判断VLAN在本接口的属 性： … 先 剥离帧的PVID Tag， 然后再发送。 |
```

修复后（同一表）：

```
| 接口类型 | 接收帧处理过程 | 发送帧处理过程 |
| Trunk接口 | 判断数据帧VLAN Tag： ● 无Tag，则添加本接口PVID Tag。当PVID 在允许通过的VLAN ID列表里时，则允许该VLAN帧进入… | 判断VLAN在本接口的属性： … 先剥离帧的PVID Tag，然后再发送。 |
```

全语料 CJK-空格-CJK 残留：表格行 **65（hw-01-04 单文档）→ 0（全 238 文档）**；正文行 7,628 处为正常中文分词空格，不属于本修复范围（正文不调用合并）。

### 11.2 全量重转换+重建统计（238 docs，27m00s）

| collection | 修复前（Fix Round 1） | 修复后 |
|---|---|---|
| chunks | 43,970（父 12,243 + 子 31,727） | **43,950**（父 12,243 + 子 31,707） |
| chunks_naive | 18,981 | **18,946** |

入索引 221 文档（17 近空跳过）/ 14,425 页 / img+empty 跳过 172 / 书签命中 13,373-956 / 表格 7,351；c9311 残留 0；进度分批打印照旧。

### 11.3 验收重跑

- 中/英 "…创建 VLAN 20 … Catalyst 9300"：出处均全命中 cisco-c9300-17.9-vlan-cg；72B 输出连贯（configure terminal → vlan 20 → name → media → end），无乱码复读。
- `uv run pytest -m "not milvus and not gpu"`：57 passed；全量：**67 passed**。

### 11.4 遗留项（deferred，明确不修）

1. **OID 数字碎片**："…205. 1.2" 式 ASCII 数字串内的空格（x_tolerance 切分所致）——收益低风险高（易误合版本号/命令参数），不处理。
2. **<1.5pt 残留粘连 1 处**：cisco-c9300-17.9-security-cg.md:2264 表头 "CommandorAction"——该表渲染字距 <1.5pt，再降阈值会引发中文粘连回归，保留现状。
3. **`_parent_window` 对大表格子块/截断父块不生效**：父块超 4,000 token 被截断（含 `<!-- truncated -->`）或子块文本不在父块可见范围时，`find` 落空退回头部截断，此时窗口不含命中子块；待 v2 引入 parent 分段存储后再处理。
