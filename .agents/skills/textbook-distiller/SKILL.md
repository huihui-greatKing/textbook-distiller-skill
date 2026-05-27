---
name: textbook-distiller
description: 用于将教材 PDF、截图、PPT 或课堂资料蒸馏成可调用、可测试、可复用的 AI Skill 系统；支持分阶段审慎执行，也支持在用户明确授权后连续完成整本教材 OCR、章节总结、章节 Skill、综合作业 Skill、测试与课程报告。
---

# 教材蒸馏为 AI Skill 的元技能

## 1. 定位

本 Skill 是“教材蒸馏元技能”，用于设计和执行教材到 AI Skill 系统的转换流程。它不是普通摘要工具，也不是直接生成答案的工具，而是先建立资料检查、证据追踪、章节边界、质量门禁、测试验证和人工复核机制，再生成章节总结、章节 Skill、综合作业 Skill、测试文件和课程报告。

使用本 Skill 时，先确认运行模式：

- **阶段确认模式**：每个阶段完成后输出结果并等待确认，适合资料不完整、OCR 质量不确定或用户只想做部分工作的情况。
- **全流程授权模式**：当用户明确要求“直接继续做”“运行整本教材 OCR”“总结具体章节”“生成全部章节 Skill”或同等意思时，可以连续执行资料登记、可读性检查、整本 OCR、章节切分、逐章蒸馏、测试和报告整理；遇到严重阻塞时再停止说明。

进入教材正文处理、逐章蒸馏、批量 OCR 或批量生成前，必须确认用户已经授权对应范围。授权后不要机械地在每个小阶段停顿。

本 Skill 必须保持通用：不绑定某一本教材、某一门课程或固定章节名。换教材时，只替换输入资料、蒸馏范围和目标输出，仍使用同一套流程、门禁和模板。

## 2. 参考文件

本 Skill 使用渐进加载。先读本文件；只有任务需要时，再读取下列 reference：

- `references/methodology.md`：蒸馏方法论、运行模式、阶段流程、证据追踪、候选筛选、跨章关联。
- `references/templates.md`：输入检查表、阶段输出格式、文件命名、章节 Skill 完整模板。
- `references/evaluation.md`：强制停止规则、反幻觉规则、质量门禁、测试矩阵和评分 rubric。
- `scripts/ocr_textbook.py`：将扫描版或图片版 PDF OCR 为逐页 Markdown 和 JSONL 证据。
- `scripts/build_chapter_texts.py`：按 `BOOK_STRUCTURE.md` 将逐页 OCR 文本切分为章节文本包。
- `scripts/generate_distillation_from_ocr.py`：基于章节 OCR 文本包生成章节总结、章节 Skill、综合作业 Skill、测试和报告草稿。

优先只读取与当前阶段相关的 reference，避免把无关模板一次性加载进上下文。

## 3. 适用范围

可以处理：

- 扫描版教材 PDF；
- 可复制文字的教材 PDF；
- 教材截图；
- 课程 PPT；
- 课堂笔记；
- 实验指导书；
- 作业资料；
- 需要保留教材思路的复习、作业和课程报告资料。

不适合处理：

- 没有任何资料依据的教材内容生成；
- 只要一句话答案的问题；
- 不需要保留教材思路的百科式总结；
- 要求编造教材没有写明内容的任务；
- 要求无视资料依据、OCR 质量和待复核项直接编造结论的任务。

## 4. 核心原则

- 证据先行：知识点、公式、图表、例题和解题方法都要能追溯到教材页码、截图、PPT 页或笔记位置。
- 双模式执行：资料不完整时使用阶段确认模式；用户明确授权时使用全流程授权模式连续推进。
- 可执行优先：能用脚本稳定完成的步骤优先使用脚本，例如 PDF 页数检查、整本 OCR、章节文本切分和索引生成。
- 候选筛选：先建立候选知识点、候选题型、候选方法，再筛选进入章节 Skill；未纳入内容记录合并、淘汰或待复核原因。
- 原子化 Skill：每章 Skill 有明确调用条件、排除条件、输入、输出、自检和测试提示词。
- 学习目标对齐：每章输出要对齐“理解概念、掌握方法、规范作业、通过测试”四类目标。
- 评价驱动：先定义测试维度和评分标准，再检查 Skill 是否真的能被调用。
- 人工复核：OCR 不清楚、公式表格图示不确定、页码异常和目录缺失必须进入待复核项。
- 不夸大 AI：输出语气保持学生课程实践风格，定位为辅助理解、辅助复习、辅助规范作业书写。

## 5. 输入检查

每次使用前，先检查：

1. 教材名称是否明确；
2. 教材文件是否存在；
3. 蒸馏范围是否明确；
4. 输出目标是否明确；
5. 是否需要 OCR；
6. 是否保留图表、公式、例题；
7. 是否生成作业模板、测试题、课程报告；
8. 是否存在待人工复核项。

信息不完整时，先输出“缺失信息清单”，不要直接进入执行。输入检查表见 `references/templates.md`。

## 6. 阶段流程

### 阶段 0：任务确认

确认本轮只做什么，以及使用哪种运行模式。任务类型包括：精进 Skill、建立项目结构、资料清单、可读性检查、目录计划、整本 OCR、单章蒸馏、全书蒸馏、综合作业 Skill、测试评价或课程报告。

如果用户只要求优化 Skill、模板、规则或检查表，则只处理元 Skill 本身。

如果用户明确要求连续处理整本教材，则进入全流程授权模式：先记录输入与风险，再连续运行 OCR、章节切分、逐章蒸馏和验证；只在证据缺失、工具失败、页码无法对应、OCR 大面积不可读等严重问题时停止。

### 阶段 1：资料登记

只登记文件，不总结内容。输出 `knowledge-base/raw/source-files.md`，记录文件名、路径、页数、文件作用、是否需要 OCR 和待复核项。

### 阶段 2：可读性检查

判断 PDF 是否能直接抽取文字。文本字符数为 0 时，应判断为扫描版或图片版，进入 OCR 准备；不要据此认定 PDF 损坏，也不要直接总结教材。

输出 `knowledge-base/evidence/ocr-notes/pdf-readability-check.md`。

### 阶段 2A：整本 OCR 执行

在用户授权后执行。优先使用 `scripts/ocr_textbook.py` 对完整教材 PDF 做逐页 OCR，输出逐页 Markdown、JSONL 证据、manifest 和 OCR 摘要。OCR 输出可以很大，默认作为生成产物保存，不应直接提交到通用 Skill 仓库。

推荐命令：

```powershell
py skills/textbook-distiller/scripts/ocr_textbook.py --pdf "<教材PDF>" --out-dir knowledge-base/evidence/ocr-notes/fulltext --zoom 2.0
```

OCR 完成后记录平均置信度、低置信度行数、缺页、空页和待复核内容。

### 阶段 3：目录识别计划

先识别目录页和章节边界，建立教材页码与 PDF 页序对应关系。页码范围、分段文件页数异常、目录缺失全部记录为待复核。

输出 `BOOK_STRUCTURE.md`。

目录确认后，可用 `scripts/build_chapter_texts.py` 将整本 OCR 文本切分为章节包：

```powershell
py skills/textbook-distiller/scripts/build_chapter_texts.py --ocr-dir knowledge-base/evidence/ocr-notes/fulltext --book-structure BOOK_STRUCTURE.md --out-dir knowledge-base/normalized/chapter-texts
```

切分完成后，可用 `scripts/generate_distillation_from_ocr.py` 生成第一版章节总结、章节 Skill、综合作业 Skill、测试评价和报告草稿：

```powershell
py skills/textbook-distiller/scripts/generate_distillation_from_ocr.py --project-root .
```

脚本生成的是可复核草稿。正式提交前应检查章节标题、核心概念、公式规则、图表线索、测试提示词和待人工复核项。

### 阶段 4：逐章蒸馏计划与章节总结

为每章生成蒸馏计划；在全流程授权模式下，同时基于章节 OCR 文本生成章节总结。章节总结应包括章节主线、核心概念、公式规则、图表线索、题型方法、易错点和待复核项。不要大段照抄 OCR 文本。

计划包括章节名称、输入文件、页码范围、核心任务、候选知识点来源、候选题型来源、预计输出、人工复核点、跨章关联和压力测试方向。

### 阶段 5：章节 Skill 生成

在阶段确认模式下，只有用户确认后执行；在全流程授权模式下，完成章节 OCR 和章节总结后可连续执行。每章生成 `skills/chapter-xx-english-name/SKILL.md`，并按完整模板写入目标、章节依据、适用题型、调用条件、排除条件、知识框架、核心概念、公式规则、图表、解题步骤、例题、作业模板、常见错误、自检、测试提示词和待复核项。

完整模板见 `references/templates.md`。

### 阶段 6：综合作业 Skill 生成

只有多个章节 Skill 已完成后执行。生成 `skills/comprehensive-homework/SKILL.md`，用于题目路由、章节 Skill 选择、作业式答案组织、过程保留和不确定内容标注。

### 阶段 7：测试验证

生成 `tests/test-prompts.md` 和 `tests/evaluation.md`。测试应覆盖正常题、跨章题、边界题、证据不足题、诱导题和作业书写题。

测试矩阵和评分 rubric 见 `references/evaluation.md`。

### 阶段 8：课程报告整理

生成 `DISTILLATION_REPORT.md`。报告应包含项目背景、资料说明、项目思路、蒸馏流程、Skill 设计过程、测试验证、项目成果、不足与改进和总结。不要生成 PPT、演讲稿或答辩问题。

## 7. 强制停止与继续规则

遇到以下情况必须停止并等待确认：

- 找不到用户指定的教材文件；
- OCR 工具不可用且没有替代方案；
- 页码范围与文件页数不一致；
- 目录识别不完整；
- OCR 大面积为空或平均置信度明显异常；
- 公式、表格、图示无法确认；
- 用户只要求优化 Skill；
- 用户明确限制本轮范围；
- 即将执行会覆盖已有人工整理成果的操作。

停止时说明：当前完成了什么、为什么停止、需要确认什么、下一步建议。

以下情况不应机械停止：

- 用户已经明确授权整本 OCR 或全书蒸馏；
- PDF 是扫描版，但可通过 OCR 工具继续处理；
- 局部 OCR 不清楚但可以标注待复核并继续处理其他页面；
- 单章内容存在少量公式或图表不确定，但不影响生成带待复核项的章节 Skill 草稿。

## 8. 反幻觉

- 没有教材依据，不得编造章节内容；
- OCR 不清楚的地方不能写成确定结论；
- 不能用常识替代教材原文；
- 可以补充常见课程知识，但必须标注“教材未明确，需人工确认”；
- 不得大段照抄教材；
- 不确定内容统一写入待人工复核项；
- 输出应提炼知识框架、解题方法和表达方式。
- OCR 原文只作为证据和工作材料，章节总结与 Skill 应使用自己的组织语言。

## 9. 输出格式

每轮任务结束后使用固定结构：

```markdown
### 本轮完成内容

### 新增或修改文件

### 关键结论

### 待人工复核项

### 下一步建议

### 是否继续
```

如果下一步会进入教材正文处理、逐章蒸馏或批量生成，必须等待用户确认。

## 10. 文件规范

- 教材资料登记：`knowledge-base/raw/source-files.md`
- OCR 检查：`knowledge-base/evidence/ocr-notes/pdf-readability-check.md`
- 整本 OCR 文本：`knowledge-base/evidence/ocr-notes/fulltext/`
- 章节 OCR 文本包：`knowledge-base/normalized/chapter-texts/`
- 候选与淘汰记录：`knowledge-base/evidence/candidate-notes/`
- 图表说明：`knowledge-base/evidence/figure-notes/`
- 公式表格说明：`knowledge-base/evidence/formula-table-notes/`
- 跨章关联索引：`knowledge-base/normalized/cross-links.md`
- 章节 Skill：`skills/chapter-xx-english-name/SKILL.md`
- 综合作业 Skill：`skills/comprehensive-homework/SKILL.md`
- 测试题：`tests/test-prompts.md`
- 评价标准：`tests/evaluation.md`
- 作业模板：`examples/homework-writing-template.md`

## 11. 自检清单

- [ ] 是否先确认本轮任务边界；
- [ ] 是否完成输入检查；
- [ ] 是否按阶段执行并等待确认；
- [ ] 如果用户授权全流程，是否连续完成 OCR、切分、总结和验证；
- [ ] 是否保留证据来源；
- [ ] 是否记录候选、合并、淘汰和待复核项；
- [ ] 是否明确章节 Skill 的调用条件和排除条件；
- [ ] 是否包含跨章关联；
- [ ] 是否包含测试矩阵和评分标准；
- [ ] 是否适合扫描版教材；
- [ ] 是否避免跳过资料清单和目录识别；
- [ ] 是否适合不同教材复用。
