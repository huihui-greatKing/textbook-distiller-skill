# 案例：使用 textbook-distiller 处理《计算机组成与设计》教材

## 案例定位

本案例用于说明 `textbook-distiller` 如何在真实课程资料中使用。它既可以作为阶段确认模式的样例，也可以作为全流程授权模式的验证样例：先保留资料登记、可读性检查和页码映射，再继续执行整本 OCR、章节文本切分、章节总结和章节 Skill 生成。

## 适用目的

- 作为以后处理其他教材时的参考样例；
- 检查资料登记、PDF 可读性检查、目录识别和页码映射是否完整；
- 展示扫描版教材进入 OCR 前应保留哪些证据；
- 说明教材项目产物和通用 Skill 本体应如何分离维护。

## 本案例已形成的阶段产物

| 阶段 | 产物 | 作用 |
|---|---|---|
| 资料登记 | `knowledge-base/raw/source-files.md` | 记录教材文件、路径、页数、用途和 OCR 需求 |
| 可读性检查 | `knowledge-base/evidence/ocr-notes/pdf-readability-check.md` | 判断 PDF 是否可直接抽取文字，并记录检查结论 |
| 页码映射 | `knowledge-base/evidence/ocr-notes/page-map-notes.md` | 记录教材页码与 PDF 物理页序的对应关系 |
| 目录结构 | `BOOK_STRUCTURE.md` | 记录章、页码范围、分册文件对应关系和待复核点 |
| 蒸馏计划 | `knowledge-base/normalized/chapter-distillation-plan.md` | 为后续逐章生成章节 Skill 提供计划 |
| 整本 OCR | `knowledge-base/evidence/ocr-notes/fulltext/` | 保存逐页 OCR 文本、JSONL 证据和 OCR 摘要 |
| 章节文本包 | `knowledge-base/normalized/chapter-texts/` | 按 `BOOK_STRUCTURE.md` 将 OCR 文本切分到各章 |

## 复用到其他教材时的步骤

1. 复制或保留 `skills/textbook-distiller/` 作为通用 Skill；
2. 为新教材新建项目目录，保留同样的 `knowledge-base/`、`skills/`、`tests/`、`examples/` 结构；
3. 先执行资料登记，生成 `knowledge-base/raw/source-files.md`；
4. 再执行 PDF 可读性检查，生成 `knowledge-base/evidence/ocr-notes/pdf-readability-check.md`；
5. 如果是扫描版，先建立页码映射和 OCR 计划；
6. 目录和页码确认后，如果用户授权，可以连续执行整本 OCR 和章节文本切分；
7. 基于章节文本包生成章节总结和章节 Skill；
8. 每章 Skill 完成后，用测试提示词检查调用条件、解题步骤和待复核项。

## 维护建议

- 通用规则、模板和质量检查应放在 `skills/textbook-distiller/`；
- 某一本教材的资料清单、目录、页码映射和蒸馏结果应放在对应项目的 `knowledge-base/` 与章节 `skills/` 中；
- 大体积页面图片、PDF 原文和临时 OCR 缓存不建议提交到 Git；
- 能帮助复用的方法、提示词和案例说明可以放入 `examples/`。

## 后续可继续补充

- 整本 OCR 运行记录；
- 章节 Skill 生成样例；
- 测试题与评价标准样例；
- 课程报告生成样例。
