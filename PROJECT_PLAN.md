# 项目执行计划

本项目分为五个阶段推进。当前只完成阶段一，后续阶段需要在用户提供教材 PDF、截图、PPT 或课堂笔记后再继续。

## 阶段一：创建教材蒸馏器 Skill

### 阶段目标

先完成 `skills/textbook-distiller/SKILL.md`，明确教材资料读取、OCR 检查、章节识别、知识点抽取、方法蒸馏、章节 Skill 生成、测试验证和课程报告生成的统一流程。

### 输入材料

- 项目要求；
- 课程名称；
- 目标教材名称；
- 预期目录结构；
- 后续输出目标。

### 具体任务

- 创建项目目录结构；
- 编写 `README.md`；
- 编写 `AGENTS.md`；
- 编写 `PROJECT_PLAN.md`；
- 编写 `skills/textbook-distiller/SKILL.md`；
- 为后续资料、测试和示例文件建立轻量占位。

### 输出文件

- `README.md`；
- `AGENTS.md`；
- `PROJECT_PLAN.md`；
- `skills/textbook-distiller/SKILL.md`；
- 项目基础目录结构。

### 检查标准

- 项目定位是学生课程实践；
- 当前阶段没有直接总结教材章节；
- 当前阶段没有运行 OCR；
- 当前阶段没有生成上台汇报材料；
- 元 Skill 中包含完整的教材蒸馏流程；
- 后续章节 Skill 有统一模板。

## 阶段二：读取教材目录与资料清单

### 阶段目标

根据教材 PDF 建立 `BOOK_STRUCTURE.md`，明确教材章节结构、页码范围、资料文件对应关系和待复核项。

### 输入材料

- 教材 PDF；
- 教材截图；
- 课程 PPT；
- 课堂笔记；
- 实验指导书；
- 作业资料。

### 具体任务

- 将原始资料放入 `knowledge-base/raw/`；
- 检查 PDF 是否可复制文字；
- 判断是否需要 OCR 或图像识别；
- 识别章、节、小节标题；
- 记录每章页码范围；
- 建立教材资料清单；
- 将不清楚的标题、页码、图表和公式列入待复核项。

### 输出文件

- `BOOK_OVERVIEW.md`；
- `BOOK_STRUCTURE.md`；
- `knowledge-base/index.md`；
- `knowledge-base/evidence/ocr-notes/` 下的识别记录；
- 待人工复核列表。

### 检查标准

- 能说明资料来源和文件对应关系；
- 能区分可读 PDF 和扫描版 PDF；
- 章节结构清晰；
- 页码范围可追踪；
- 不确定内容已经标注“待人工复核”。

## 阶段三：逐章蒸馏

### 阶段目标

按照第 1 章到第 10 章逐章生成章节 Skill，形成每章的知识点、题型、例题、测试题和作业书写模板。

### 输入材料

- `BOOK_STRUCTURE.md`；
- 教材对应章节内容；
- OCR 或图像识别结果；
- 课堂 PPT 和笔记；
- 已复核的图表、公式和页码。

### 具体任务

- 按章节读取资料；
- 抽取核心概念和重要定义；
- 整理公式、规则、图表和术语；
- 提炼教材中的解题步骤；
- 整理典型题型和易错点；
- 生成章节 `SKILL.md`；
- 为每章补充测试提示词。

### 输出文件

- `skills/chapter-01-introduction/SKILL.md`；
- `skills/chapter-02-data-representation/SKILL.md`；
- `skills/chapter-03-arithmetic-and-alu/SKILL.md`；
- `skills/chapter-04-instruction-and-assembly/SKILL.md`；
- `skills/chapter-05-cpu-design/SKILL.md`；
- `skills/chapter-06-pipeline/SKILL.md`；
- `skills/chapter-07-memory-system/SKILL.md`；
- `skills/chapter-08-io-system/SKILL.md`；
- `skills/chapter-09-multicomputer-system/SKILL.md`；
- `skills/chapter-10-eda-computer-design/SKILL.md`；
- 章节知识点、题型、例题和测试题。

### 检查标准

- 每章 Skill 能单独调用；
- 每章都有对应教材章节和页码来源；
- 重要概念、公式、图表、题型和易错点完整；
- 作业书写模板符合课程作业风格；
- 没有大段照抄教材原文；
- 待复核内容没有被写成确定结论。

## 阶段四：生成综合作业 Skill

### 阶段目标

生成 `skills/comprehensive-homework/SKILL.md`，用于根据题目自动判断所属章节并调用对应章节 Skill，帮助组织适合作业书写的答案过程。

### 输入材料

- 已完成的章节 Skill；
- 章节题型索引；
- 作业题目样例；
- 作业书写模板；
- 课程常用评分要求。

### 具体任务

- 建立题目到章节的判断规则；
- 设计综合作业 Skill 的调用流程；
- 整理作业答案结构；
- 保留必要计算步骤和文字说明；
- 避免只给结论；
- 补充综合测试提示词。

### 输出文件

- `skills/comprehensive-homework/SKILL.md`；
- `examples/homework-writing-template.md`；
- `tests/test-prompts.md` 中的综合作业测试题。

### 检查标准

- 能根据题目判断相关章节；
- 能调用对应章节 Skill；
- 答案结构适合课程作业；
- 计算题保留步骤；
- 简答题有清楚的知识依据；
- 不把不确定内容写成教材结论。

## 阶段五：生成课程报告

### 阶段目标

形成最终课程报告 `DISTILLATION_REPORT.md`，总结项目背景、资料说明、蒸馏流程、Skill 设计过程、测试验证、项目成果、不足与改进。

### 输入材料

- 完整教材蒸馏结果；
- 已生成的章节 Skill；
- 综合作业 Skill；
- 测试题与评价结果；
- 待复核项处理记录。

### 具体任务

- 整理项目题目来源和背景；
- 说明教材资料情况；
- 总结项目思路和实现流程；
- 说明 Skill 设计过程；
- 汇总测试验证结果；
- 整理项目成果；
- 写明不足与改进方向；
- 形成学生课程实践报告。

### 输出文件

- `DISTILLATION_REPORT.md`。

### 检查标准

- 报告语气像学生课程实践报告；
- 不写成上台汇报材料；
- 不夸大 AI 作用；
- 能说明项目完成了什么；
- 能说明哪些内容经过测试；
- 能说明哪些内容仍需人工复核。

