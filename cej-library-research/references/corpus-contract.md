# 本地语料与状态约定

语料根目录下：

- `catalog/download_audit.json`：元数据、下载与身份校验、页数、SHA-256、原文许可声明及阅读状态。`all_issues_complete` 只有在官网档案与实际文件核对完成后才能设为真。
- `text/<PDF 文件名去掉扩展名>.txt`：由本地 PDF 提取，换页符 `\f` 对应 PDF 分页。它可能含断行、连字、公式损坏或扫描空页，不能仅凭字符数认定提取准确。
- `index/cje.sqlite`：可重建的本地 FTS 索引，不是论文原件或已经人工核对的结论集。

`pdf_validated` 表示 PDF 可解析，并在首页找到 DOI，或首页题名词与题录高度匹配；具体依据见 `identity_check`。它不表示所有图表、公式和正文已逐页审读。`pdf_parse_valid_identity_pending` 应先做身份核对，默认不用于全文索引。

`reading_status` 独立于文件状态；自动提取和检索不会把论文改为“已读”。参考文献里的主题词命中不是正文主张的证据。`pdf_page` 从 1 开始，`printed_pages` 则是题录给出的整篇印刷页范围，两者不可互换。

查询脚本依赖 Python 标准库以及当前 Python 的 SQLite 所含 FTS5。它不下载文件、不读取浏览器会话、不上传文本；在缺少语料或 FTS5 的环境中，需要提供正确的本地语料及兼容运行时。

本次实际检查：以 minimum wage 查询已返回 Heise（2026）的引言以及参考文献页，说明必须读命中上下文，不能把排序靠前当作结论。加入每篇默认最多两个命中后，可同时检查其他论文；它改善来源多样性，不证明文献回顾已经完整。

本交付的 requested_scope 为 2022–2026、卷46–50。281 个已知题录均有校验文件；逐期官网目录尚未全部对齐，因此 requested_scope_complete=false。全历史 all_issues_complete=false 与用户缩小的任务范围不是同一个分母。
