# 大语言模型幻觉评估方法综述 研究资料包

整理日期：2026-11-06

已打包：16篇核心论文 + 108篇独立重要论文，共124篇可解析PDF；12个相关官方源码仓库快照。

先打开 research_map.md 查看核心阅读顺序和每篇重要论文对应的研究方面、核心论文及负责人。paper_catalog.csv 可以用Excel打开和筛选；references.bib 是初步引用库；metadata/final_manifest.json 包含下载URL、SHA256、页数和核验状态。

重要：这是经书目信息、原始落地页及PDF首页核验的选题阅读库，不是逐篇全文精读报告。“对应核心”是本项目概念关联，不是论文直接引用关系。方法优劣和实验结果须在精读时填写，不作未验证的性能结论。传统摘要/翻译评估研究用于解释方法源流，多语言、医学、法律论文用于讨论泛化边界；最终8页报告应精选证据，不能罗列全部文献。

核心目录 papers/core；重要目录 papers/important。文件编号有间断，来自筛除错链、重复版本和未获得全文的记录，不代表缺失文件。

code/repositories.json 记录原仓库、下载状态、提交SHA与许可证；每个ZIP保留仓库自身LICENSE。源码未安装或执行。未下载模型权重，不承诺全部实验开箱即跑。

去重以规范化标题、下载文件SHA256和人工识别的会议版/预印本重复为依据。少量论文无机器可提取作者/日期，CSV保留空值，最终引用请以原始PDF核对；不编造字段。references.bib优先使用arXiv版本信息，最终报告应优先替换为正式发表记录。

候选来源：EdinburghNLP/awesome-hallucination-detection、综述作者LuckyyySTA/Awesome-LLM-hallucination及siyaqi/Awesome-Hallu-Eval；这些只是发现入口，PDF来自arXiv、ACL Anthology、Nature等原始来源。sources保留索引快照便于追溯，不代表接受其中全部描述。

metadata/packaging_exclusions.json 和 excluded.json 记录未纳入项。无关或重复已下载文件移到当前文件夹 screening_excluded，不进入正式资料包。源码和论文仅供课程研究，转发时请遵守各来源许可。
