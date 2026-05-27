# 《计算机组成与设计》教材蒸馏为 AI Skill 的课程实践

## 项目背景

本项目围绕《计算机组成与设计》教材展开，希望把教材内容转化为可调用的 AI Skill，用于辅助理解知识点、规范解题过程和整理作业答案。

本项目不是直接让 AI 简单总结教材，而是先设计一套教材蒸馏流程，再用这套流程处理教材。处理流程包括教材资料读取、扫描版 PDF 可读性检查、OCR 或页面图像识别、章节目录识别、知识点抽取、图表与公式整理、解题方法提炼、章节 Skill 生成、作业书写模板生成、测试题与评价标准生成、课程报告生成。

项目的设计重点是先把处理规则和输出格式确定下来，再按照固定流程处理教材。这样可以减少随意总结带来的遗漏，也能让后续每章生成的 Skill 保持统一结构，便于测试、检查和复用。

## 项目目标

- 对整本教材进行 OCR 和章节结构整理；
- 按章节蒸馏教材内容；
- 生成章节 Skill；
- 生成作业书写模板；
- 生成测试题；
- 形成课程报告。

## 项目特点

- 先设计规则，再处理教材；
- 先建立教材结构，再逐章蒸馏；
- 不直接生成答案，而是保留教材的知识框架和解题思路；
- 对扫描版教材加入 OCR 和人工复核流程；
- 每个章节 Skill 都要可以单独调用；
- 最终结果可测试、可检查、可复用。

## 项目实现流程

资料整理 → 目录识别 → 知识点抽取 → 方法蒸馏 → Skill 生成 → 测试验证 → 报告整理。

具体实现时，先整理教材 PDF、截图、PPT、笔记等资料，判断资料是否可直接读取；再建立教材目录和页码范围；然后按章节抽取概念、公式、图表、题型和易错点；接着把教材中的解题过程整理成可复用的方法；最后生成章节 Skill、综合作业 Skill、测试题和课程报告。

## 项目当前成果

项目已经完成对《计算机组成与设计》教材的全量蒸馏验证。当前成果重点是教材处理后的课程实践材料，包括章节结构、OCR 记录、章节总结、章节 Skill、综合作业 Skill、测试评价文件和课程报告。

使用 `textbook-distiller` 处理教材时，交付重点是“教材跑出来的结果”，也就是下面这些课程实践成果：

- `BOOK_STRUCTURE.md` 教材章节结构和页码映射；
- `knowledge-base/evidence/ocr-notes/ocr-run-log.md` OCR 运行记录；
- `knowledge-base/normalized/study-guide.md` 面向复习和作业的整本教材蒸馏总览；
- `knowledge-base/normalized/concepts/` 第 1 章到第 10 章知识点提炼；
- `knowledge-base/normalized/problem-types/` 第 1 章到第 10 章题型与作业方法；
- `knowledge-base/normalized/chapter-summaries/` 第 1 章到第 10 章复习式章节总结；
- `skills/chapter-*/SKILL.md` 第 1 章到第 10 章章节 Skill；
- `skills/comprehensive-homework/SKILL.md` 综合作业 Skill；
- `tests/test-prompts.md` 和 `tests/evaluation.md` 测试与评价文件；
- `DISTILLATION_REPORT.md` 课程实践报告。

## 目录说明

```text
computer-organization-book2skill/
├── README.md
├── AGENTS.md
├── PROJECT_PLAN.md
├── BOOK_OVERVIEW.md
├── BOOK_STRUCTURE.md
├── INDEX.md
├── DISTILLATION_REPORT.md
├── knowledge-base/
├── skills/
├── tests/
└── examples/
```

其中 `skills/chapter-xx-xxx/` 是本教材蒸馏后生成的章节 Skill；`tests/` 用于保存测试题和评价标准；`examples/` 用于保存运行提示词和作业书写模板。

`skills/textbook-distiller/` 也保存在本仓库中，它是用于生成上述成果的教材蒸馏 Skill。它可以继续维护和复用，但在使用它处理某一本教材时，最终交付应以教材蒸馏结果为主，而不是只交付这个元 Skill 本身。

因此，判断一次教材蒸馏是否有用，不能只看是否生成了目录、模板和检查表，还要看是否产出了能直接帮助复习和作业的内容，例如章节主线、核心概念解释、常见题型、解题步骤、作业表达方式和易错点。

当前版本进一步把教材蒸馏目标调整为“学习理解 + 复习整理 + 题型训练 + 作业书写辅助”。章节 Skill 不应只是本章概要，而应能讲透概念、整理公式和图表、归纳典型题型、给出作业式解题过程，并提供自测题和参考答案。

- `skills/textbook-distiller/SKILL.md`：核心流程、边界和阶段规则；
- `skills/textbook-distiller/references/methodology.md`：证据追踪、候选筛选、跨章关联等方法论；
- `skills/textbook-distiller/references/templates.md`：输入检查表、输出格式和章节 Skill 完整模板；
- `skills/textbook-distiller/references/evaluation.md`：强制停止、反幻觉、测试矩阵和评分标准。

## 复现方式

如果需要复现本项目的教材蒸馏过程，应先把教材 PDF 或相关资料放入 `knowledge-base/raw/`，再按照 `textbook-distiller` 中定义的流程进行资料读取、目录识别、OCR、逐章蒸馏和测试验证。

如果教材是扫描版，应先进行 OCR 或页面图像识别，并把识别不清楚的标题、公式、图表、表格和页码写入待人工复核列表，不能把不确定内容直接写成确定结论。

复现整本教材处理时，可以使用类似指令：

```text
请使用 textbook-distiller 对这本教材进入全流程授权模式：完成资料登记、整本 OCR、章节文本切分、逐章总结、章节 Skill、测试评价和课程报告；中间结果落盘，严重阻塞时再停止说明。
```

## Python 环境与复核

项目基础 Python 依赖记录在 `requirements.txt`。后续如果需要重新配置环境，可在项目目录下执行：

```powershell
py -m pip install -r requirements.txt
```

如果需要检查项目内部的 `textbook-distiller` 结构，可使用 Codex Skill 校验脚本，并在 Windows 下开启 UTF-8 模式：

```powershell
$env:PYTHONUTF8='1'
py "<Codex skill-creator quick_validate.py 路径>" skills\textbook-distiller
```

如果输出 `Skill is valid!`，说明项目内部流程文件的基础结构有效。课程项目主要检查对象仍然是章节 Skill、测试评价文件和课程报告。
