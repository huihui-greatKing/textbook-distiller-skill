# 《计算机组成与设计》教材蒸馏为 AI Skill 的课程实践

## 项目背景

本项目围绕《计算机组成与设计》教材展开，希望把教材内容转化为可调用的 AI Skill，用于辅助理解知识点、规范解题过程和整理作业答案。

本项目不是直接让 AI 总结教材，而是先构建一个“教材蒸馏器 Skill”。该 Skill 用来规范教材处理流程，包括教材资料读取、扫描版 PDF 可读性检查、OCR 或页面图像识别、章节目录识别、知识点抽取、图表与公式整理、解题方法提炼、章节 Skill 生成、作业书写模板生成、测试题与评价标准生成、课程报告生成。

项目的设计重点是先把处理规则和输出格式确定下来，再按照固定流程处理教材。这样可以减少随意总结带来的遗漏，也能让后续每章生成的 Skill 保持统一结构，便于测试、检查和复用。

## 项目目标

- 构建教材蒸馏器 Skill；
- 使用该 Skill 处理整本教材；
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

## 当前阶段说明

项目已经完成“项目架构设计”和“教材蒸馏器 Skill”的创建。当前版本的 `textbook-distiller` 支持两种使用方式：一种是按阶段确认后逐步推进，另一种是在用户明确授权后连续执行整本教材 OCR、章节总结、章节 Skill 生成、测试与课程报告整理。

本阶段输出的核心内容是：

- 项目目录结构；
- 项目说明文档；
- 后续协作约束；
- 五阶段执行计划；
- `skills/textbook-distiller/SKILL.md` 元 Skill；
- `skills/textbook-distiller/scripts/ocr_textbook.py` 整本 OCR 脚本；
- `skills/textbook-distiller/scripts/build_chapter_texts.py` 章节 OCR 文本切分脚本。

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

其中 `skills/textbook-distiller/` 是当前阶段的核心目录。后续阶段会在 `skills/chapter-xx-xxx/` 中逐章生成章节 Skill，在 `tests/` 中补充测试题和评价标准，在 `examples/` 中补充例题整理和作业书写模板。

`textbook-distiller` 采用渐进加载结构：

- `skills/textbook-distiller/SKILL.md`：核心流程、边界和阶段规则；
- `skills/textbook-distiller/references/methodology.md`：证据追踪、候选筛选、跨章关联等方法论；
- `skills/textbook-distiller/references/templates.md`：输入检查表、输出格式和章节 Skill 完整模板；
- `skills/textbook-distiller/references/evaluation.md`：强制停止、反幻觉、测试矩阵和评分标准。

## 后续使用方式

后续处理教材时，应先把教材 PDF 或相关资料放入 `knowledge-base/raw/`，再调用 `textbook-distiller` Skill 进行资料读取、目录识别、OCR、逐章蒸馏和测试验证。

如果教材是扫描版，应先进行 OCR 或页面图像识别，并把识别不清楚的标题、公式、图表、表格和页码写入待人工复核列表，不能把不确定内容直接写成确定结论。

如果已经确认要直接处理整本教材，可以使用类似指令：

```text
请使用 textbook-distiller 对这本教材进入全流程授权模式：完成资料登记、整本 OCR、章节文本切分、逐章总结、章节 Skill、测试评价和课程报告；中间结果落盘，严重阻塞时再停止说明。
```

## Python 环境与 Skill 校验

项目基础 Python 依赖记录在 `requirements.txt`。后续如果需要重新配置环境，可在项目目录下执行：

```powershell
py -m pip install -r requirements.txt
```

校验 `textbook-distiller` 是否符合 Codex Skill 结构时，建议使用 UTF-8 模式：

```powershell
$env:PYTHONUTF8='1'
py "C:\Users\wanghui\.codex\skills\.system\skill-creator\scripts\quick_validate.py" skills\textbook-distiller
```

如果输出 `Skill is valid!`，说明 Skill 的基础结构有效。

## 个人 Skill 安装与更新

`textbook-distiller` 已安装为个人 Codex Skill：

```text
C:\Users\wanghui\.codex\skills\textbook-distiller
```

安装方式是目录链接，指向本项目中的源目录：

```text
D:\西电\作业\计组\课本蒸馏\skill\computer-organization-book2skill\skills\textbook-distiller
```

因此后续要完善这个 Skill 时，直接修改本项目的 `skills/textbook-distiller/` 即可；个人 Skill 会同步看到这些修改。修改后建议重新运行校验：

```powershell
$env:PYTHONUTF8='1'
py "C:\Users\wanghui\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "C:\Users\wanghui\.codex\skills\textbook-distiller"
```

新增或更新 Skill 后，建议重启 Codex 以便重新加载技能列表和元数据。
