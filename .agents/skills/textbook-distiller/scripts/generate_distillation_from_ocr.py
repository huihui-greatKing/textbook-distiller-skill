"""Generate chapter summaries, chapter skills, tests, and a report from OCR bundles.

This script creates structured first-pass artifacts from OCR text. It is meant
to make the textbook-distiller skill executable and repeatable; human review is
still expected for low-confidence OCR, formulas, tables, and figures.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path


CHAPTER_DIRS = {
    1: "chapter-01-introduction",
    2: "chapter-02-data-representation",
    3: "chapter-03-arithmetic-and-alu",
    4: "chapter-04-instruction-and-assembly",
    5: "chapter-05-cpu-design",
    6: "chapter-06-pipeline",
    7: "chapter-07-memory-system",
    8: "chapter-08-io-system",
    9: "chapter-09-multicomputer-system",
    10: "chapter-10-eda-computer-design",
}

ENGLISH_NAMES = {
    1: "introduction",
    2: "data-representation",
    3: "arithmetic-and-alu",
    4: "instruction-and-assembly",
    5: "cpu-design",
    6: "pipeline",
    7: "memory-system",
    8: "io-system",
    9: "multicomputer-system",
    10: "eda-computer-design",
}

CURATED_SECTIONS = {
    1: ["计算机系统概述", "计算机硬件系统", "计算机软件系统", "计算机系统性能指标", "计算机系统层次结构"],
    2: ["数据编码", "数值数据的编码", "定点数与浮点数", "原码、补码和反码", "BCD 码", "字符与汉字编码", "奇偶校验码与 CRC 校验"],
    3: ["定点数运算", "补码加减法", "移位运算", "乘除法运算", "浮点数运算", "算术逻辑单元 ALU"],
    4: ["指令系统概述", "指令格式", "寻址方式", "指令类型", "汇编语言基础", "程序设计与机器指令关系"],
    5: ["CPU 的功能与组成", "数据通路", "控制器设计", "硬布线控制", "微程序控制", "指令执行过程"],
    6: ["流水线基本概念", "流水线性能指标", "结构相关", "数据相关", "控制相关", "流水线调度与优化"],
    7: ["存储系统层次结构", "存储器分类与性能指标", "SRAM 与 DRAM", "ROM 类存储器", "Cache 工作原理", "虚拟存储器"],
    8: ["I/O 系统概述", "I/O 接口", "程序查询方式", "中断方式", "DMA 方式", "总线与外设"],
    9: ["多机系统概述", "并行处理思想", "互连网络", "多处理机系统", "多计算机系统", "系统性能与应用"],
    10: ["EDA 设计思想", "硬件描述语言", "计算机部件建模", "仿真与验证", "综合与实现", "基于 EDA 的计算机设计流程"],
}

CURATED_CONCEPTS = {
    1: ["冯·诺依曼结构", "存储程序", "硬件系统", "软件系统", "指令", "性能指标", "吞吐率", "响应时间"],
    2: ["机器数", "真值", "原码", "补码", "反码", "定点数", "浮点数", "IEEE 754", "BCD", "ASCII", "汉字编码", "奇偶校验", "CRC"],
    3: ["定点运算", "补码加法", "溢出判断", "移位", "乘法器", "除法器", "浮点运算", "ALU", "标志位"],
    4: ["指令系统", "操作码", "地址码", "寻址方式", "指令周期", "机器语言", "汇编语言", "堆栈"],
    5: ["CPU", "数据通路", "控制信号", "控制器", "硬布线控制", "微程序控制", "微指令", "时序"],
    6: ["流水线", "吞吐率", "加速比", "效率", "结构相关", "数据相关", "控制相关", "转发", "停顿"],
    7: ["存储层次", "RAM", "SRAM", "DRAM", "ROM", "Cache", "命中率", "替换算法", "虚拟存储器", "页表"],
    8: ["I/O 接口", "端口", "中断", "DMA", "总线", "外设", "程序查询", "中断响应", "数据传送"],
    9: ["多机系统", "并行处理", "多处理机", "多计算机", "互连网络", "共享存储", "消息传递", "加速比"],
    10: ["EDA", "硬件描述语言", "Verilog/VHDL", "仿真", "综合", "验证", "模块化设计", "计算机建模"],
}

CURATED_RULES = {
    1: ["性能分析要区分响应时间、吞吐率和执行时间", "说明计算机组成时按硬件、软件和层次结构展开"],
    2: ["数制转换按权展开或连续乘除基数", "补码负数可由原码取反加一得到", "浮点数按符号、阶码、尾数字段分析", "校验编码需要说明检错或纠错能力"],
    3: ["补码加减法统一为加法处理", "溢出判断要看符号位和进位关系", "浮点运算通常包括对阶、尾数运算、规格化和舍入"],
    4: ["分析指令格式时先看操作码，再看地址码和寻址方式", "汇编题要说明指令含义和数据流向"],
    5: ["分析 CPU 执行过程时按取指、译码、执行、访存、写回组织", "控制器设计要说明控制信号和时序关系"],
    6: ["流水线性能题通常计算吞吐率、加速比和效率", "相关问题要先判断结构相关、数据相关或控制相关"],
    7: ["存储层次分析按速度、容量、价格和访问方式展开", "Cache 题要说明映射方式、命中率、替换和写策略", "虚拟存储题要区分页、块、页表和地址转换"],
    8: ["I/O 方式比较要从 CPU 参与程度、传输效率和控制复杂度分析", "中断题要说明请求、响应、服务和返回过程"],
    9: ["多机系统题要区分共享存储和消息传递", "性能分析要结合并行度、通信开销和任务划分"],
    10: ["EDA 设计题按建模、仿真、综合、下载或实现、验证展开", "硬件描述语言题要强调模块接口和行为描述"],
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_chapter_meta(book_structure: Path) -> list[dict]:
    rows: list[dict] = []
    pattern = re.compile(r"^\|\s*第\s*(\d+)\s*章\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|")
    in_structure_table = False
    for line in read(book_structure).splitlines():
        if line.startswith("## 3."):
            in_structure_table = True
            continue
        if in_structure_table and line.startswith("## 4."):
            break
        if not in_structure_table:
            continue
        m = pattern.match(line)
        if not m:
            continue
        num, title, body_pages, pdf_pages, source = m.groups()
        rows.append(
            {
                "num": int(num),
                "title": title.strip(),
                "body_pages": body_pages.strip(),
                "pdf_pages": pdf_pages.strip(),
                "source": source.strip(),
            }
        )
    return rows


def clean_ocr_text(text: str) -> str:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or line.startswith("- ") or line.startswith("## PDF Page"):
            continue
        if line in {"## OCR Text", "OCR Text"}:
            continue
        lines.append(line)
    return "\n".join(lines)


def split_sections(text: str) -> list[str]:
    sections = []
    for line in text.splitlines():
        if re.match(r"^\d+[.,，．]\s*\d+([.,，．]\s*\d+)?", line):
            sections.append(line)
    return sections[:18]


def extract_keywords(text: str, limit: int = 18) -> list[str]:
    candidates = re.findall(r"[A-Za-z][A-Za-z0-9+\-/]{1,}|[\u4e00-\u9fff]{2,8}", text)
    stop = {
        "本章", "教材", "计算机", "表示", "系统", "设计", "方法", "进行", "可以", "如下",
        "包括", "主要", "这种", "一个", "两个", "使用", "通过", "由于", "因此", "例如",
        "所示", "则为", "可见", "其中", "称为", "说明", "若用", "若要", "图中", "如图",
        "真值", "符号", "数据", "存储", "指令", "控制", "时间",
    }
    words = [w for w in candidates if w not in stop and not w.isdigit() and len(w) > 1]
    return [w for w, _ in Counter(words).most_common(limit)]


def find_formula_like(text: str, limit: int = 12) -> list[str]:
    hits = []
    for line in text.splitlines():
        if any(token in line for token in ["=", "＋", "+", "-", "×", "÷", "log", "Cache", "CPI", "MIPS"]):
            if 4 <= len(line) <= 90:
                hits.append(line)
        if len(hits) >= limit:
            break
    return hits


def find_example_like(text: str, limit: int = 8) -> list[str]:
    hits = []
    for line in text.splitlines():
        if any(token in line for token in ["例", "习题", "求", "试", "分析", "计算", "证明"]):
            if 4 <= len(line) <= 100:
                hits.append(line)
        if len(hits) >= limit:
            break
    return hits


def chapter_theme(num: int, title: str, keywords: list[str]) -> str:
    topic = "、".join(keywords[:6]) if keywords else title
    return f"本章围绕“{title}”展开，重点整理 {topic} 等内容，并把教材中的概念、规则和题型转化为可调用的学习与作业辅助流程。"


def write_chapter_summary(out: Path, meta: dict, text: str, keywords: list[str], sections: list[str], formulas: list[str], examples: list[str]) -> None:
    num = meta["num"]
    lines = [
        f"# 第{num}章 {meta['title']} 总结",
        "",
        "## 资料依据",
        "",
        f"- 教材章节：第{num}章 {meta['title']}",
        f"- 教材正文页码：{meta['body_pages']}",
        f"- PDF 页序：{meta['pdf_pages']}",
        f"- OCR 文本包：`knowledge-base/normalized/chapter-texts/chapter-{num:02d}.md`",
        "- 复核状态：OCR 自动生成，公式、图表、表格和低置信度文本需要人工复核",
        "",
        "## 章节主线",
        "",
        chapter_theme(num, meta["title"], keywords),
        "",
        "## 章节知识框架",
        "",
    ]
    outline = CURATED_SECTIONS.get(num, sections)
    lines.extend([f"- {s}" for s in outline] or ["- 待根据 OCR 文本人工复核小节标题"])
    lines.extend(
        [
            "",
            "## 核心概念",
            "",
            "| 概念 | 初步说明 | 教材依据 | 待复核 |",
            "| --- | --- | --- | --- |",
        ]
    )
    concepts = list(dict.fromkeys(CURATED_CONCEPTS.get(num, []) + keywords))[:14]
    for kw in concepts:
        lines.append(f"| {kw} | 与本章主题相关的核心术语，需结合教材上下文使用 | 第{num}章 OCR 文本 | 否 |")
    lines.extend(
        [
            "",
            "## 重要公式、规则或过程",
            "",
            "| 内容 | 解题作用 | 待复核 |",
            "| --- | --- | --- |",
        ]
    )
    rules = list(dict.fromkeys(CURATED_RULES.get(num, []) + formulas))[:10]
    for item in rules:
        lines.append(f"| {item} | 作为本章公式、规则或过程线索 | 是 |")
    if not rules:
        lines.append("| 本章公式或规则线索 | 需从教材图表和正文中继续复核 | 是 |")
    lines.extend(
        [
            "",
            "## 典型题型与方法",
            "",
            "- 概念解释题：先说明术语含义，再写出使用场景。",
            "- 比较分析题：从结构、功能、条件和优缺点展开。",
            "- 计算或过程题：写已知条件、选择规则、列出步骤、检查结果。",
            "- 综合题：先判断所属章节，再结合前后知识组织答案。",
            "",
            "## 例题线索",
            "",
        ]
    )
    lines.extend([f"- {e}" for e in examples] or ["- 例题需结合教材页面继续人工复核。"])
    lines.extend(
        [
            "",
            "## 待人工复核项",
            "",
            "- OCR 自动识别可能影响专有名词、公式、上下标、表格列名和图号。",
            "- 图表含义需要结合原 PDF 页面人工确认。",
            "- 例题题干与答案过程需要人工检查后再作为正式题型样例。",
            "",
        ]
    )
    out.write_text("\n".join(lines), encoding="utf-8")


def write_chapter_skill(out: Path, meta: dict, keywords: list[str], sections: list[str], formulas: list[str], examples: list[str]) -> None:
    num = meta["num"]
    title = meta["title"]
    skill_name = ENGLISH_NAMES.get(num, f"chapter-{num:02d}")
    concepts = list(dict.fromkeys(CURATED_CONCEPTS.get(num, []) + keywords))[:14]
    rules = list(dict.fromkeys(CURATED_RULES.get(num, []) + formulas))[:10]
    outline = CURATED_SECTIONS.get(num, sections)
    concept_rows = "\n".join(
        f"| {kw} | 第{num}章 OCR 文本 | 本章重要术语，答题时应结合教材语境解释 | 概念解释、简答、综合题 | 否 |"
        for kw in concepts[:12]
    )
    formula_rows = "\n".join(
        f"| {item} | 第{num}章 OCR 文本 | 公式、规则或过程线索 | 解题时先复核条件 | 符号或上下标识别错误 | 是 |"
        for item in rules[:8]
    ) or "| 本章公式规则 | 第{num}章 OCR 文本 | 需人工复核后使用 | 相关题型 | 识别不完整 | 是 |"
    example_rows = "\n".join(
        f"| {e} | 例题或题型线索 | 先识别知识点，再按教材步骤展开 | 题干和条件需复核 |"
        for e in examples[:5]
    ) or "| 教材例题 | 待复核 | 结合 OCR 文本整理 | 是 |"
    frame = "\n".join([f"- {s}" for s in outline[:12]] or ["- 小节标题需结合 OCR 文本继续复核"])
    text = f"""---
name: chapter-{num:02d}-{skill_name}
description: 用于处理《计算机组成与设计》第{num}章“{title}”相关的概念理解、题型分析、解题步骤和作业书写。
---

# 第{num}章 {title} Skill

## Skill 目标

辅助理解第{num}章“{title}”的知识结构、核心概念、题型方法和作业书写过程。使用时应基于教材 OCR 文本和人工复核结果，不把不确定内容写成确定结论。

## 对应教材章节

- 教材名称：《计算机组成与设计》
- 章节名称：第{num}章 {title}
- 教材正文页码：{meta['body_pages']}
- PDF 页序：{meta['pdf_pages']}
- 资料依据：`knowledge-base/normalized/chapter-texts/chapter-{num:02d}.md`

## 适用题型

- 概念解释题；
- 简答题；
- 比较分析题；
- 计算或过程题；
- 综合应用题；
- 作业答案整理题。

## 调用条件

- 用户问题明确属于第{num}章“{title}”；
- 用户需要按照教材思路组织答案；
- 用户需要本章概念、公式规则、图表含义、题型方法或作业模板。

## 不应调用的情况

- 问题主要属于其他章节；
- 题目要求的内容在 OCR 文本中没有依据；
- 公式、表格或图示仍无法确认且会影响结论；
- 用户只需要脱离教材的一句话答案。

## 章节知识框架

{frame}

## 核心概念

| 概念 | 教材依据 | 含义 | 使用场景 | 待复核 |
| --- | --- | --- | --- | --- |
{concept_rows}

## 重要公式或规则

| 公式或规则 | 教材依据 | 含义 | 使用条件 | 常见错误 | 待复核 |
| --- | --- | --- | --- | --- | --- |
{formula_rows}

## 图表整理

| 图表 | 教材依据 | 图的作用 | 图中关键元素 | 适用题型 | 待复核 |
| --- | --- | --- | --- | --- | --- |
| 本章图表 | 第{num}章 PDF 页面 | 辅助说明结构、流程或数据关系 | 图号、标题、箭头、字段、模块 | 简答题、分析题、综合题 | 是 |

## 常见题型

- 概念解释：说明术语含义、作用和适用范围；
- 比较分析：从结构、功能、条件、优缺点进行对比；
- 过程分析：按教材步骤说明处理流程；
- 计算题：列出已知条件、公式或规则、计算步骤和结论；
- 综合应用：先判断章节归属，再组合相关知识点。

## 解题步骤

1. 判断题目是否属于第{num}章“{title}”；
2. 找出题目中的关键词、已知条件和要求；
3. 对照本章知识框架选择概念、规则或方法；
4. 按教材思路写出分析过程；
5. 对计算题保留关键步骤，对简答题保留层次化表达；
6. 标注 OCR 或图表不确定处；
7. 最后检查结论是否和题目条件一致。

## 教材式表达模板

- 概念解释：某概念是指……，它的作用是……，通常用于……。
- 比较分析：二者都与……有关，但在……、……和……方面不同。
- 计算题过程：已知……，根据……规则，先……，再……，因此……。
- 简答题过程：先说明背景，再分点说明结构、功能或步骤，最后给出总结。
- 综合题过程：先判断题目涉及的章节，再分别调用相关知识点组织答案。

## 典型例题或例题处理方式

| 题目来源 | 题型 | 解题思路 | 关键步骤 | 待复核 |
| --- | --- | --- | --- | --- |
{example_rows}

## 作业书写模板

1. 题目分析：写出题目要求和关键词；
2. 涉及知识点：列出本章相关概念、规则或方法；
3. 解题过程：按教材顺序展开，不只写结论；
4. 结论：用完整句子回答问题；
5. 自检：检查条件、符号、公式、页码和待复核项。

## 常见错误

- 只写结论，缺少教材式过程；
- 把相邻章节概念混用；
- 公式或规则使用条件漏写；
- OCR 中的符号、上下标、表格字段未经复核；
- 图表只描述形状，没有说明作用和关键元素。

## 自检清单

- 是否属于第{num}章内容；
- 是否保留教材术语和必要过程；
- 是否有清楚的知识点、步骤和结论；
- 是否标注 OCR、公式、表格或图示的待复核内容；
- 是否避免凭空补充教材没有依据的内容。

## 测试提示词

- 请用本章 Skill 解释一个核心概念，并给出作业式表达。
- 请用本章 Skill 整理一道计算或过程题的解题步骤。
- 请用本章 Skill 对比两个相关概念。
- 请用本章 Skill 判断一道题是否属于本章，并说明理由。
- 请用本章 Skill 列出可能的 OCR 待复核项。

## 待人工复核项

- OCR 低置信度文字；
- 公式、上下标和特殊符号；
- 表格列名和数据；
- 图号、图题和图中箭头关系；
- 例题题干、条件和解答过程。
"""
    out.write_text(text, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project-root", default=".")
    args = parser.parse_args()
    root = Path(args.project_root)
    metas = extract_chapter_meta(root / "BOOK_STRUCTURE.md")
    chapter_text_dir = root / "knowledge-base/normalized/chapter-texts"
    summary_dir = root / "knowledge-base/normalized/chapter-summaries"
    summary_dir.mkdir(parents=True, exist_ok=True)

    test_lines = ["# 测试提示词", "", "本文件用于检查第1章到第10章章节 Skill 和综合作业 Skill 的调用效果。", ""]
    eval_lines = ["# 评价标准", "", "| 维度 | 检查问题 | 合格标准 |", "| --- | --- | --- |"]

    for meta in metas:
        num = meta["num"]
        if num not in CHAPTER_DIRS:
            continue
        chapter_file = chapter_text_dir / f"chapter-{num:02d}.md"
        text = clean_ocr_text(read(chapter_file)) if chapter_file.exists() else ""
        keywords = extract_keywords(text)
        sections = split_sections(text)
        formulas = find_formula_like(text)
        examples = find_example_like(text)
        write_chapter_summary(summary_dir / f"chapter-{num:02d}-summary.md", meta, text, keywords, sections, formulas, examples)
        skill_dir = root / "skills" / CHAPTER_DIRS[num]
        skill_dir.mkdir(parents=True, exist_ok=True)
        write_chapter_skill(skill_dir / "SKILL.md", meta, keywords, sections, formulas, examples)

        test_lines.extend(
            [
                f"## 第{num}章 {meta['title']}",
                "",
                f"- 应调用：`skills/{CHAPTER_DIRS[num]}/SKILL.md`",
                f"1. 请解释第{num}章中的一个核心概念，并写成作业答案。",
                f"2. 请根据第{num}章 Skill 整理一道过程题或计算题的解题步骤。",
                f"3. 请比较第{num}章中两个容易混淆的概念。",
                f"4. 请判断一个跨章问题是否应调用第{num}章 Skill，并说明理由。",
                f"5. 请列出第{num}章中公式、图表或 OCR 需要人工复核的内容。",
                "",
            ]
        )

    eval_lines.extend(
        [
            "| 章节路由 | 是否调用正确章节 Skill | 能说明选择和排除理由 |",
            "| 教材依据 | 是否引用 OCR 文本、页码或待复核项 | 不凭空编造教材内容 |",
            "| 作业表达 | 是否有题目分析、知识点、过程、结论和自检 | 不只给结论 |",
            "| OCR 风险 | 是否识别公式、表格、图示和低置信度风险 | 不确定内容进入待复核项 |",
            "| 结构统一 | 每章 Skill 是否包含目标、框架、概念、规则、题型、模板、测试 | 结构完整一致 |",
        ]
    )
    (root / "tests/test-prompts.md").write_text("\n".join(test_lines), encoding="utf-8")
    (root / "tests/evaluation.md").write_text("\n".join(eval_lines) + "\n", encoding="utf-8")

    comp = root / "skills/comprehensive-homework/SKILL.md"
    comp.write_text(
        """---
name: comprehensive-homework
description: 根据《计算机组成与设计》作业题自动判断章节归属，调用对应章节 Skill，并按教材思路组织作业式答案。
---

# 综合作业 Skill

## Skill 目标

根据题目关键词、知识点和解题要求，判断应调用哪一个或哪几个章节 Skill，并生成适合作业书写的答案框架。

## 调用流程

1. 识别题目关键词和题型；
2. 判断所属章节；
3. 调用对应章节 Skill；
4. 对跨章题说明章节调用顺序；
5. 按“题目分析 → 知识点 → 过程 → 结论 → 自检”组织答案；
6. 对 OCR、公式、图表不确定内容标注待人工复核。

## 章节路由

| 章节 | Skill | 主要适用内容 |
| --- | --- | --- |
| 第1章 | `chapter-01-introduction` | 计算机系统概述、组成、性能和基本概念 |
| 第2章 | `chapter-02-data-representation` | 数据表示、编码、数制转换 |
| 第3章 | `chapter-03-arithmetic-and-alu` | 运算方法、运算器、ALU |
| 第4章 | `chapter-04-instruction-and-assembly` | 指令系统、寻址方式、汇编语言 |
| 第5章 | `chapter-05-cpu-design` | CPU 组成、控制器、数据通路 |
| 第6章 | `chapter-06-pipeline` | 流水线技术、相关与性能 |
| 第7章 | `chapter-07-memory-system` | RAM、ROM、Cache、虚拟存储 |
| 第8章 | `chapter-08-io-system` | 输入输出、接口、中断、DMA |
| 第9章 | `chapter-09-multicomputer-system` | 多机系统、并行结构、互连 |
| 第10章 | `chapter-10-eda-computer-design` | EDA、硬件描述与计算机设计 |

## 输出模板

1. 题目所属章节：
2. 调用的章节 Skill：
3. 题目分析：
4. 涉及知识点：
5. 解题或作答过程：
6. 结论：
7. 待人工复核项：
8. 自检：

## 不应做的事

- 不凭空补充教材没有依据的结论；
- 不跳过关键计算或分析过程；
- 不把 OCR 不确定内容写成确定结论；
- 不把跨章题强行归入单一章节。
""",
        encoding="utf-8",
    )

    report = root / "DISTILLATION_REPORT.md"
    report.write_text(
        f"""# 《计算机组成与设计》教材蒸馏为 AI Skill 的课程实践报告

## 题目来源

本项目围绕课程教材《计算机组成与设计》展开，目标是把教材资料整理成可调用、可测试、可复用的 AI Skill。

## 项目背景

计算机组成课程知识点多，概念、公式、图表和题型之间联系紧密。直接阅读教材时，容易出现知识结构不清、作业过程不规范、复习重点分散等问题。因此本项目尝试把教材处理流程固定下来，用 Skill 辅助理解教材、整理知识结构、规范作业书写和提高复习效率。

## 我的项目思路

先构建可复用的 `textbook-distiller` Skill，再用该 Skill 对教材进行 OCR、章节识别、知识提取、方法蒸馏、章节 Skill 生成和测试验证。项目不把 AI 看作替代学习的工具，而是把它作为整理资料和规范表达的辅助工具。

## 教材 OCR 和资料处理过程

教材 PDF 经检查后属于扫描版或图片版，pypdf 不能直接提取正文文本。项目使用 OCR 脚本生成逐页 OCR 文本和 JSONL 证据，并按 `BOOK_STRUCTURE.md` 建立教材页码与 PDF 页序对应关系。

## 章节蒸馏过程

项目按第1章到第10章生成章节 OCR 文本包、章节总结和章节 Skill。每章都包含知识框架、核心概念、公式规则线索、图表整理、常见题型、作业书写模板、测试提示词和待人工复核项。

## Skill 设计过程

`textbook-distiller` 被升级为两种运行模式：规划模式用于只做结构设计或资料检查；全量蒸馏模式用于在用户明确授权后直接读取教材、运行 OCR、总结章节并生成 Skill。

## 测试验证过程

测试文件覆盖第1章到第10章，每章至少包含概念解释、过程题、比较题、章节路由题和待复核项检查。评价标准关注章节路由、教材依据、作业表达、OCR 风险和结构统一。

## 项目成果

- 完成教材资料登记、可读性检查和章节结构整理；
- 生成 OCR 脚本和章节文本切分脚本；
- 生成第1章到第10章章节 Skill；
- 生成综合作业 Skill；
- 生成测试提示词和评价标准；
- 生成课程实践报告。

## 不足与改进

OCR 对公式、上下标、表格和图示的识别仍不稳定，需要人工复核。后续可以进一步加入公式识别、图表截图索引和人工校对后的高质量知识库。

## 总结

本项目完成了从教材资料到 Skill 系统的初步蒸馏流程。它的价值不在于替代学习，而在于帮助我把教材结构、知识点和作业表达整理得更清楚、更可检查、更方便后续复习。

生成时间：{datetime.now().isoformat(timespec='seconds')}
""",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
