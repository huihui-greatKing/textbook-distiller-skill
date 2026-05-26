# 后续运行项目可复制提示词

本文件保存后续使用 `textbook-distiller` 元 Skill 时可直接复制的提示词。每条提示词都限定本轮范围，避免自动进入下一阶段。

## 1. 检查项目结构

```text
请使用 textbook-distiller Skill 只检查当前项目结构是否符合课程项目要求。本轮只检查目录和关键文件是否存在，不读取教材内容，不 OCR，不识别目录，不生成章节 Skill。

输出文件：如有必要，只更新 INDEX.md 或项目结构检查说明。

完成后请输出本轮完成内容、新增或修改文件、关键结论、待人工复核项、下一步建议，并等待我确认，不要自动进入下一阶段。
```

## 2. 登记教材资料

```text
请使用 textbook-distiller Skill 只登记我提供的教材资料。本轮只记录文件名、文件路径、页数、文件作用和是否可能需要 OCR，不总结教材正文，不识别目录，不抽取知识点，不生成章节 Skill。

输出文件：knowledge-base/raw/source-files.md。

完成后请输出本轮完成内容、新增或修改文件、关键结论、待人工复核项、下一步建议，并等待我确认，不要自动进入下一阶段。
```

## 3. 检查 PDF 可读性

```text
请使用 textbook-distiller Skill 只检查教材 PDF 是否能直接抽取文字。本轮只统计文本可提取情况，判断是否需要 OCR，不运行 OCR，不总结正文，不识别目录，不生成章节 Skill。

输出文件：knowledge-base/evidence/ocr-notes/pdf-readability-check.md。

完成后请输出本轮完成内容、新增或修改文件、关键结论、待人工复核项、下一步建议，并等待我确认，不要自动进入下一阶段。
```

## 4. 识别目录和章节结构

```text
请使用 textbook-distiller Skill 只识别教材目录和章节结构。本轮只处理目录页、章节目次和章节边界，不逐章总结正文，不抽取知识点，不生成章节 Skill。

输出文件：BOOK_STRUCTURE.md。

完成后请输出本轮完成内容、新增或修改文件、关键结论、待人工复核项、下一步建议，并等待我确认，不要自动进入下一阶段。
```

## 5. 建立教材页码与 PDF 页序对应关系

```text
请使用 textbook-distiller Skill 只建立教材页码与 PDF 页序的对应关系。本轮只核对页码、页序、分段文件范围和异常项，不总结教材内容，不生成章节 Skill。

输出文件：BOOK_STRUCTURE.md 和 knowledge-base/evidence/ocr-notes/page-map-notes.md。

完成后请输出本轮完成内容、新增或修改文件、关键结论、待人工复核项、下一步建议，并等待我确认，不要自动进入下一阶段。
```

## 6. 蒸馏单章

```text
请使用 textbook-distiller Skill 只蒸馏第 X 章。本轮只处理我确认的这一章，基于已确认的 OCR 或文本资料抽取知识框架、核心概念、公式规则、图表说明、解题步骤、作业模板和测试提示词。

请先建立候选知识点、候选题型和候选方法，再筛选进入章节 Skill；未纳入的候选项要记录合并、淘汰或待复核原因。章节 Skill 必须写清楚调用条件、不应调用的情况、跨章关联和测试提示词。

不要处理其他章节，不生成综合作业 Skill，不生成课程报告，不把 OCR 不清楚的内容写成确定结论。

输出文件：skills/chapter-xx-english-name/SKILL.md，并按需要更新 tests/test-prompts.md、knowledge-base/evidence/candidate-notes/ 和 knowledge-base/normalized/cross-links.md。

完成后请输出本轮完成内容、新增或修改文件、关键结论、待人工复核项、下一步建议，并等待我确认，不要自动进入下一阶段。
```

## 7. 生成综合作业 Skill

```text
请使用 textbook-distiller Skill 只生成综合作业 Skill。本轮只基于已经完成并确认的多个章节 Skill，设计根据题目判断章节、选择对应 Skill、组织作业式答案和标注不确定内容的流程。

不要重新蒸馏教材正文，不生成新章节 Skill，不生成课程报告。

输出文件：skills/comprehensive-homework/SKILL.md 和 examples/homework-writing-template.md。

完成后请输出本轮完成内容、新增或修改文件、关键结论、待人工复核项、下一步建议，并等待我确认，不要自动进入下一阶段。
```

## 8. 生成测试与评价文件

```text
请使用 textbook-distiller Skill 只生成测试与评价文件。本轮只基于已完成并确认的章节 Skill 和综合作业 Skill，整理测试提示词和评价标准。

不要重新读取教材正文，不 OCR，不生成新章节 Skill，不生成课程报告。

输出文件：tests/test-prompts.md 和 tests/evaluation.md。

完成后请输出本轮完成内容、新增或修改文件、关键结论、待人工复核项、下一步建议，并等待我确认，不要自动进入下一阶段。
```

## 9. 做 Skill 压力测试

```text
请使用 textbook-distiller Skill 只做 Skill 压力测试。本轮只基于已经完成并确认的章节 Skill，设计正常题、跨章题、边界题、证据不足题和诱导题，检查 Skill 是否会误调用、编造、跳过过程或忽略待复核项。

不要重新读取教材正文，不 OCR，不生成新章节 Skill，不生成课程报告。

输出文件：tests/test-prompts.md 和 tests/evaluation.md。

完成后请输出本轮完成内容、新增或修改文件、关键结论、待人工复核项、下一步建议，并等待我确认，不要自动进入下一阶段。
```

## 10. 生成课程报告

```text
请使用 textbook-distiller Skill 只生成课程报告。本轮只基于已经完成并确认的资料清单、章节结构、章节 Skill、综合作业 Skill、测试文件和评价结果，整理学生课程实践报告。

不要生成 PPT，不创建 presentation 目录，不写演讲稿，不写答辩问题，不夸大 AI 作用。

输出文件：DISTILLATION_REPORT.md。

完成后请输出本轮完成内容、新增或修改文件、关键结论、待人工复核项、下一步建议，并等待我确认。
```
