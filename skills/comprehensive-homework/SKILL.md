---
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
