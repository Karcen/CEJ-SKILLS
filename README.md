# CEJ SKILLS

**从经济学论文中提炼可复用的研究方法。**  
*Reusable research skills distilled from economics papers.*

CEJ SKILLS 是面向经济学研究的 AI 技能包，基于 *Cambridge Journal of Economics*（CJE）2022–2026 年的选读论文，将概念辨析、机制分析、证据判断和论文论证转化为可调用的研究工作方法。

它适合研究构思、文献讨论、研究设计检查和稿件修改。每个模块都包含使用条件、判断方法、适用边界和可追溯的论文来源，可用于 Codex，也可由其他支持读取 Markdown 指令的助手使用。

[English](#english) · [技能模块](#技能模块) · [快速开始](#快速开始) · [来源与边界](#来源与边界)

## 能帮你做什么

- **澄清研究对象。** 检查“分配”“金融化”“工作质量”等概念是否被不同指标替代，明确观测单位与比较范围。
- **拆解机制。** 区分行动者、激励、制度约束和结果，提出能与主要解释相区分的竞争解释。
- **判断证据。** 按概念、理论、历史、经验和政策命题分别评估证据，控制因果解释与外推范围。
- **改进论证。** 找到稿件真正改变的判断，将概念、机制、证据和贡献连接起来。
- **处理专题问题。** 分析收入分配、气候投资及充足性政策中的约束、传导渠道与实施条件。

## 技能模块

| 模块 | 适用任务 |
|---|---|
| [`cej-research`](cej-research/SKILL.md) | 主入口：研究设计、概念与指标、制度机制、证据判断、论文论证 |
| [`cej-distributional-macro`](cej-distributional-macro/SKILL.md) | 区分要素与个人分配，在不同宏观约束下分析分配政策 |
| [`cej-climate-investment-policy`](cej-climate-investment-policy/SKILL.md) | 分析不确定性、需求与融资如何影响气候投资，比较政策工具 |
| [`cej-sufficiency-policy-review`](cej-sufficiency-policy-review/SKILL.md) | 评估充足性政策的目标、分配影响和实施路径 |
| [`cej-library-research`](cej-library-research/SKILL.md) | 检索另行配置的本地 CJE 全文库，返回 DOI、文档路径和 PDF 页码 |

一般研究问题从 `cej-research` 开始；专题任务选择对应模块。前四个模块可独立阅读使用，全文检索模块需要额外配置本地语料。

## 快速开始

### 在 Codex 中使用

下载或克隆本仓库，将需要的 `cej-*` 目录放入 `~/.codex/skills/`。保留目录中的 `SKILL.md`、`references/` 及其他资源。

```bash
git clone https://github.com/Karcen/CEJ-SKILLS.git
mkdir -p ~/.codex/skills
cp -R CEJ-SKILLS/cej-* ~/.codex/skills/
```

如果本地已存在同名技能，先比较内容再更新。私有仓库需要具备访问权限并完成 GitHub 身份验证。

在提示中调用技能并提供研究材料：

```text
使用 $cej-research 审阅下面的研究设计。
重点检查概念与指标是否对应、机制能否区分，以及结论是否超出证据。
请说明哪些修改会影响研究结论，并保留可追溯的来源。
```

### 在 DeepSeek 等助手中使用

提供相关模块的 `SKILL.md`，并在需要时补充其中链接的参考文件。支持本地文件读取的环境可直接指定路径；其他环境可上传对应文件。

```text
先读取 cej-research/SKILL.md，按任务需要读取其 references 文件。
用这些方法检查我的论文引言：本文究竟改变了哪个已有判断？
请区分论文原有证据、作者解释和你的修改建议。
```

### 配置本地全文检索（可选）

仓库不附带论文 PDF、抽取全文或数据库。若已有与本工具兼容的本地语料，在 `cej-library-research` 目录运行：

```bash
python3 scripts/search_corpus.py   --corpus-root "/path/to/CJE_papers"   --build --query '"minimum wage"' --limit 5
```

需要 Python 3 和 SQLite FTS5。语料结构见[语料说明](cej-library-research/references/corpus-contract.md)。脚本在本地建立索引和查询，不调用外部服务。检索结果用于定位原文；命中也可能来自参考文献，引用前须检查上下文。

## 使用示例

**研究设计**

> 使用 `cej-research` 检查“高交易频率反映过度自信”的解释。区分交易次数、换手率、活跃天数与观察期，提出其他可能机制，并说明现有数据能否将其区分。

**政策分析**

> 使用 `cej-climate-investment-policy` 比较补贴、公共投资与融资支持。分别讨论它们解决的约束、私人投资响应，以及执行中的分配影响。

**稿件修改**

> 使用 `cej-research` 修改这段讨论。明确哪些结果属于相关性、哪些有因果识别支持，并将制度背景与结论的适用条件连接起来。

这些是技能应用示例，不是来源论文对上述具体问题给出的实证结论。

## 来源与边界

当前版本从 **12 篇论文的选定章节**提炼方法，覆盖 2022–2026 年，2026 年来源较多。每篇的 DOI、阅读范围和提炼用途见[来源地图](cej-research/references/source-map.md)；专题模块另附来源笔记。技能中的流程和应用示例是综合后的研究建议，不是作者原话。

配套本地语料快照含 **281 份已校验文档、6,309 页**，包括论文、目录与声明。下载和建立索引不代表全部精读或逐篇蒸馏。当前已知范围内题录均有校验文件，但尚未完成所有官方期次目录的逐项对账。覆盖状态见 [`corpus-status.json`](corpus-status.json)，文档哈希与来源记录见 [`provenance.json`](provenance.json)。

本项目不是 CJE 官方工具、投稿指南或全刊观点总结。正式投稿要求应查阅期刊当前指南；具体结论、数值和公式应回到原文核对。来源论文的权利归相应权利人所有，使用本技能包不授予论文全文的访问或再分发权。

## 扩充方法

新增来源时，先阅读相关正文，再记录 DOI、实际阅读章节、提炼出的决策规则及其适用条件。补充能改变研究判断的内容，避免按题名生成结论，或把某一篇文章的立场写成通用规则。

---

## English

**CEJ SKILLS turns selected economics papers into reusable research instructions for AI assistants.** It draws on papers published in the *Cambridge Journal of Economics* (CJE) during 2022–2026, with an emphasis on concepts, mechanisms, institutions, evidence and argument.

Use it to develop research questions, examine whether measures match concepts, distinguish competing explanations, assess the reach of empirical claims, and revise a paper's contribution. Each skill provides decision criteria, conditions of use and traceable sources.

### Modules

| Skill | Purpose |
|---|---|
| `cej-research` | Research design, conceptual distinctions, institutional mechanisms, evidence and argument |
| `cej-distributional-macro` | Income distribution under different macroeconomic constraints |
| `cej-climate-investment-policy` | Uncertainty, demand, finance and climate investment policy |
| `cej-sufficiency-policy-review` | Goals, distributional implications and implementation of sufficiency policies |
| `cej-library-research` | Retrieval and source verification in a separately configured local corpus |

Start with `cej-research` for general research tasks. Copy the desired `cej-*` folders into `~/.codex/skills/` and invoke the skill in your prompt. Alternatively, provide a module's `SKILL.md` and its relevant reference files to an assistant such as DeepSeek. Instructions are primarily in Chinese. A private repository requires access permission and GitHub authentication.

For example:

> Use `cej-research` to review this research design. Check whether its measures represent the stated concepts, which rival mechanisms remain observationally equivalent, and which claims exceed the evidence. Explain how each proposed revision changes the research judgment.

The first four skills can be used without the local paper library. The retrieval module requires Python 3, SQLite FTS5 and a compatible local corpus; see its [corpus contract](cej-library-research/references/corpus-contract.md). The repository does not distribute paper PDFs, extracted full texts or the database.

### Sources and scope

The current synthesis draws on **selected sections of 12 papers**, spanning all five years with greater coverage of 2026. The [source map](cej-research/references/source-map.md) identifies each DOI, reading scope and contribution to the skills. Procedures and application examples are the project's synthesis, not quotations or claims of author endorsement.

The accompanying local corpus snapshot contains **281 validated documents and 6,309 pages**, including articles, contents and notices. Downloading and indexing do not imply that every document has been read or distilled. All currently known scoped catalogue records have validated files, but exhaustive reconciliation against every official issue table of contents remains incomplete. See the status and provenance files for details.

This is an independent research aid, not an official CJE product, submission guide or statement of journal consensus. Check original papers before citing precise findings, equations or estimates. Rights in source publications remain with their respective holders; this package does not grant access or redistribution rights to those publications.

To extend the skills, read the relevant source material and record its DOI, reviewed sections, actionable research rule and conditions of use. Add guidance that changes a research decision rather than reproducing abstracts or treating one author's position as a universal rule.
