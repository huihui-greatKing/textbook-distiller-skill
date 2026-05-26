# 项目执行计划

本项目分为五个阶段推进。当前版本已经从“只做项目架构”升级为可复用的教材蒸馏 Skill，并完成一次《计算机组成与设计》教材的全量蒸馏验证。

## 阶段一：创建并升级教材蒸馏器 Skill

### 阶段目标

完成 `skills/textbook-distiller/SKILL.md`，让它同时支持规划模式和全量蒸馏模式。

### 输入材料

- 项目要求；
- 教材资料；
- 课程实践目标；
- 后续输出目标。

### 具体任务

- 创建项目目录结构；
- 编写项目说明和协作规则；
- 编写 `textbook-distiller` 元 Skill；
- 增加 OCR、章节文本切分和蒸馏生成脚本；
- 明确证据追踪、待复核和测试验证规则。

### 输出文件

- `README.md`
- `AGENTS.md`
- `PROJECT_PLAN.md`
- `skills/textbook-distiller/SKILL.md`
- `skills/textbook-distiller/scripts/`

### 检查标准

- Skill 不绑定单一教材；
- 支持规划模式；
- 支持全量蒸馏模式；
- 能处理扫描版教材；
- 能生成章节 Skill、测试和报告；
- 输出风格保持学生课程实践项目。

## 阶段二：读取教材目录与资料清单

### 阶段目标

根据教材 PDF 建立 `BOOK_STRUCTURE.md`，明确教材章节结构、页码范围、资料文件对应关系和待复核项。

### 输入材料

- 完整本教材 PDF；
- 分章或分段 PDF；
- OCR 检查结果。

### 具体任务

- 登记原始资料；
- 检查 PDF 文本可提取性；
- 判断扫描版处理方式；
- 建立教材页码与 PDF 页序关系；
- 识别章、节、小节标题；
- 标注页码、目录、图表、公式和表格待复核项。

### 输出文件

- `BOOK_OVERVIEW.md`
- `BOOK_STRUCTURE.md`
- `knowledge-base/raw/source-files.md`
- `knowledge-base/evidence/ocr-notes/pdf-readability-check.md`
- `knowledge-base/evidence/ocr-notes/page-map-notes.md`

### 检查标准

- 能说明资料来源和文件对应关系；
- 能区分可读 PDF 和扫描版 PDF；
- 页码范围可追踪；
- 不确定内容进入待人工复核项。

## 阶段三：逐章蒸馏

### 阶段目标

按照第 1 章到第 10 章逐章生成章节总结和章节 Skill，形成知识点、题型、例题线索、测试题和作业书写模板。

### 输入材料

- `BOOK_STRUCTURE.md`
- 整本 OCR 文本；
- 章节 OCR 文本包；
- 图表、公式和表格复核记录。

### 具体任务

- 运行整本 OCR；
- 切分章节 OCR 文本；
- 抽取核心概念、公式规则、图表线索、题型和易错点；
- 生成章节总结；
- 生成章节 `SKILL.md`；
- 为每章补充测试提示词。

### 输出文件

- `knowledge-base/evidence/ocr-notes/ocr-run-log.md`
- `knowledge-base/normalized/chapter-summaries/`
- `skills/chapter-01-introduction/SKILL.md`
- `skills/chapter-02-data-representation/SKILL.md`
- `skills/chapter-03-arithmetic-and-alu/SKILL.md`
- `skills/chapter-04-instruction-and-assembly/SKILL.md`
- `skills/chapter-05-cpu-design/SKILL.md`
- `skills/chapter-06-pipeline/SKILL.md`
- `skills/chapter-07-memory-system/SKILL.md`
- `skills/chapter-08-io-system/SKILL.md`
- `skills/chapter-09-multicomputer-system/SKILL.md`
- `skills/chapter-10-eda-computer-design/SKILL.md`

### 检查标准

- 每章 Skill 结构一致；
- 每章包含知识框架、核心概念、公式规则、图表整理、题型方法和待复核项；
- 不大段照抄教材；
- OCR 不确定内容明确标注。

## 阶段四：生成综合作业 Skill

### 阶段目标

根据题目自动判断章节并调用对应章节 Skill，辅助生成课程作业式答案。

### 输入材料

- 第 1 章到第 10 章章节 Skill；
- 跨章关联索引；
- 作业书写模板。

### 具体任务

- 建立章节路由规则；
- 设计作业式答案结构；
- 保留计算题关键步骤；
- 保留简答题教材式表达；
- 标注不确定内容。

### 输出文件

- `skills/comprehensive-homework/SKILL.md`
- `examples/homework-writing-template.md`

### 检查标准

- 能判断题目所属章节；
- 能调用对应章节 Skill；
- 答案包含题目分析、知识点、过程、结论和自检；
- 不把不确定内容写成确定结论。

## 阶段五：生成测试、评价和课程报告

### 阶段目标

形成最终测试、评价标准和课程实践报告。

### 输入材料

- 章节 Skill；
- 综合作业 Skill；
- OCR 运行记录；
- 待复核项；
- 迭代日志。

### 具体任务

- 每章生成至少 5 条测试提示词；
- 评价章节路由、教材依据、作业表达、OCR 风险和结构统一；
- 总结项目背景、思路、过程、成果和不足；
- 记录自我检查和修复过程。

### 输出文件

- `tests/test-prompts.md`
- `tests/evaluation.md`
- `tests/meta-skill-checklist.md`
- `DISTILLATION_REPORT.md`
- `ITERATION_LOG.md`

### 检查标准

- 测试覆盖第 1 章到第 10 章；
- 评价标准可操作；
- 报告语气像学生课程实践；
- 不写成商业项目；
- 不夸大 AI 作用。
