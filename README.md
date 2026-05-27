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

当前项目交付内容：

- `BOOK_STRUCTURE.md` 教材章节结构和页码映射；
- `knowledge-base/evidence/ocr-notes/ocr-run-log.md` OCR 运行记录；
- `knowledge-base/normalized/chapter-summaries/` 第 1 章到第 10 章章节总结；
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

`skills/textbook-distiller/` 是项目内部用于规范蒸馏流程的实现材料，不作为本课程项目的主要交付成果。它的作用是保证 OCR、章节整理、Skill 生成和测试评价过程有统一规则。

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
