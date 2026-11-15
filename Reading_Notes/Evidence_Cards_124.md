# 124篇文献的证据卡片

本文件把分类和逐篇阅读笔记中的原有判断放在同一处，供五位组员核查与摘录。每条的“研究定位”和“限制”来自现有笔记或已审阅研究地图；它们是本组阅读记录，不能代替论文原文。正式报告引用具体数值时，仍须逐项核对原文页码、表格和实验设置。

字段说明：技术主类与评价对象来自 `Taxonomy_124.csv`；研究定位优先取 `Research_Map_Reviewed.md` 的“主类”，否则取该笔记第一个实质小节；限制优先取研究地图“次类”，否则取笔记中明确的局限或待办小节。

## C01 · Survey of Hallucination in Natural Language Generation

- **层级／研究角色：** core／综述/概念
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 —；次类 无
- **研究定位：** 跨任务历史与定义
- **需核查的条件或限制：** IE/QA/NLI/LM方法谱系、来源外真实与任务差异。
- **阅读笔记中的证据片段：** 这篇综述提供跨NLG任务的基础脉络，适合解释幻觉评估如何从摘要、数据到文本、翻译、对话中的“来源不忠实”发展到开放LLM世界知识事实性。结构为共性概念与方法（§2–6）、任务特有研究（§7–12）、LLM更新（§13）。它不是只针对ChatGPT时代的综述，也不是2026最新方法目录。
- **来源：** [精读笔记](notes/core/C01_NLG_Hallucination_Survey.md)；[论文页面](https://arxiv.org/abs/2202.03629)

## C02 · A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions

- **层级／研究角色：** core／综述/概念
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 —；次类 无
- **研究定位：** LLM事实性/忠实性和成因
- **需核查的条件或限制：** RAG失败分解、检测与基准。
- **阅读笔记中的证据片段：** 本文将LLM幻觉分为factuality与faithfulness，按data/training/inference梳理成因及缓解，并单独详细分析RAG。这是组织框架贡献，不是发明一种可计算、已验证完备且互斥的误差分类。它面向开放LLM及信息检索应用，比C01早期任务分节更关注知识边界和端到端检索系统。
- **来源：** [精读笔记](notes/core/C02_LLM_Hallucination_Taxonomy.md)；[论文页面](https://arxiv.org/abs/2311.05232)

## C03 · Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models

- **层级／研究角色：** core／综述/概念
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 —；次类 无
- **研究定位：** 三种参照冲突和生成/识别能力
- **需核查的条件或限制：** 生命周期、不确定性和跨语言。
- **阅读笔记中的证据片段：** Input-conflicting：偏离用户任务指令或用户提供资料；context-conflicting：与模型自己先前生成内容冲突；fact-conflicting：与世界知识不符或无法据此核验（第3–5页）。特别注意C02的context inconsistency指用户提供上下文，而本篇context-conflicting指模型生成历史；不能看到同一个context词就合并标签。
- **来源：** [精读笔记](notes/core/C03_Sirens_Song.md)；[论文页面](https://arxiv.org/abs/2309.01219)

## C04 · A Survey of Automatic Hallucination Evaluation on Natural Language Generation

- **层级／研究角色：** core／综述/概念
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 —；次类 无
- **研究定位：** 自动评估管线
- **需核查的条件或限制：** SF/WF四象限、检索证据、元评估、实际部署。
- **阅读笔记中的证据片段：** 本文专注text-only Automatic Hallucination Evaluation（AHE），排除纯人工评价、缓解技术及多模态系统，覆盖pre/post-LLM方法。相比C01–C03，更贴近我们的选题“评估方法”，包括证据获取、比较机制、内部信号、LLM裁判及应用限制。应借鉴其问题拆解，而非将本组综述写成其105方法清单的改述。
- **来源：** [精读笔记](notes/core/C04_Automatic_Evaluation_Survey.md)；[论文页面](https://arxiv.org/abs/2404.12041)

## C05 · TruthfulQA: Measuring How Models Mimic Human Falsehoods

- **层级／研究角色：** core／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 T;J;H
- **研究定位：** 基准与协议
- **需核查的条件或限制：** 训练裁判、拒答/信息性、版本漂移。纠正初筛将其主要放在裁判类的偏重。
- **阅读笔记中的证据片段：** 作者关心imitative falsehood：训练文本中常见的错误信念、误解、阴谋论等，使模型通过模仿产生错误答案。它与不熟悉实体导致的任意猜测、输入不忠实、工具调用错误并不完全等价。基准以英文短问答为主，817题覆盖38类，问题刻意诱导错误信念；它不是从真实用户流量随机抽样得到的风险估计器。
- **来源：** [精读笔记](notes/core/C05_TruthfulQA.md)；[论文页面](https://arxiv.org/abs/2109.07958)

## C06 · HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models

- **层级／研究角色：** core／基准/数据
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 —；次类 H;J
- **研究定位：** 合成与人工标注基准
- **需核查的条件或限制：** 识别、提示/证据干预、格式解析、选择偏差。
- **阅读笔记中的证据片段：** HaluEval同时包含“指令生成的任务特定错误”与“人工标注的一般用户问答”。核心任务是给定回答，识别是否含幻觉；不是要求被测模型直接生成答案后测其自然幻觉发生率。将“识别准确率62.59%”解释成“模型生成62.59%正确答案”属于任务混淆。
- **来源：** [精读笔记](notes/core/C06_HaluEval.md)；[论文页面](https://arxiv.org/abs/2305.11747)

## C07 · FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation

- **层级／研究角色：** core／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 E；次类 J
- **研究定位：** 原子事实与证据核验
- **需核查的条件或限制：** 模型整体分数估计、知识源限制与覆盖。
- **阅读笔记中的证据片段：** 长回答通常混合正确、错误和无关内容；一句话也可能包含多个事实。只给整段或整句一个真假标签，会把“只有一处错误”和“几乎全部错误”压成同一类别。作者将评价单位下沉到原子事实，考察每条事实是否由指定可信知识源支持。其贡献同时包含一个评价定义、一套人工标注流程、一个自动估计器和模型评价案例，四者不能混为一谈。
- **来源：** [精读笔记](notes/core/C07_FActScore.md)；[论文页面](https://arxiv.org/abs/2305.14251)

## C08 · SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models

- **层级／研究角色：** core／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 T;J
- **研究定位：** 自采样一致性
- **需核查的条件或限制：** NLI/LLM裁判、黑盒访问、预算。
- **阅读笔记中的证据片段：** 当只能调用API获得文本，拿不到概率、隐藏状态，也没有外部事实库时，能否识别模型的事实错误？作者假设已学到的事实在多次随机采样中较一致，缺乏知识时生成内容较分散。这是事实风险代理，不是事实真值的逻辑保证。
- **来源：** [精读笔记](notes/core/C08_SelfCheckGPT.md)；[论文页面](https://arxiv.org/abs/2303.08896)

## C09 · AlignScore: Evaluating Factual Consistency with a Unified Alignment Function

- **层级／研究角色：** core／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 E
- **研究定位：** 训练式语义对齐
- **需核查的条件或限制：** 跨任务NLI、分块聚合、训练测试重叠。
- **阅读笔记中的证据片段：** 模型判定文本b中的信息是否存在于文本a且不与a矛盾。这是相对上下文的方向性支持关系，不是判断b在现实世界中是否为真，也不是普通语义相似度。即使输入本身有错，对输入完全忠实的输出也可能得高分。
- **来源：** [精读笔记](notes/core/C09_AlignScore.md)；[论文页面](https://arxiv.org/abs/2305.16739)

## C10 · Detecting hallucinations in large language models using semantic entropy

- **层级／研究角色：** core／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 无
- **研究定位：** 语义不确定性
- **需核查的条件或限制：** 自采样、聚类、拒答与confabulation范围。
- **阅读笔记中的证据片段：** 第1页将confabulation限定为错误且随随机种子等无关细节变化的输出。它明确不解决稳定复述错误训练数据、系统性推理失败或有目的误导。这不是宣传时泛指的“所有幻觉检测”。不能因为方法没有检出自信稳定的错误，就说它违背了自己提出的研究目标；但用户若需要检测所有事实风险，这确实是适用边界。
- **来源：** [精读笔记](notes/core/C10_Semantic_Entropy.md)；[论文页面](https://www.nature.com/articles/s41586-024-07421-0)

## C11 · TRUE: Re-evaluating Factual Consistency Evaluation

- **层级／研究角色：** core／元评估/审计
- **评价对象：** 来源忠实性
- **技术：** 主类 —；次类 E;T
- **研究定位：** 检测器元评估
- **需核查的条件或限制：** 来源忠实性、样本级AUROC、标签映射。
- **阅读笔记中的证据片段：** TRUE不是训练一个新的文本生成器，也不以评估所有现实事实为目标。它把11个已有数据集转成统一格式，研究现有自动指标能否识别每个样本相对其grounding的事实不一致。核心动机是：系统级相关性高不保证单个回答能被正确筛选，因此需要样本级元评估。
- **来源：** [精读笔记](notes/core/C11_TRUE.md)；[论文页面](https://arxiv.org/abs/2204.04991)

## C12 · RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models

- **层级／研究角色：** core／基准/数据
- **评价对象：** 来源忠实性
- **技术：** 主类 —；次类 T;H
- **研究定位：** RAG来源条件及跨度基准
- **需核查的条件或限制：** 细粒度定位、监督检测、风险覆盖。
- **阅读笔记中的证据片段：** RAG将检索内容放进上下文，但模型仍可能反驳材料或编出无支持细节。本文通过自然生成而非刻意让模型编错的数据，建立回答级与片段级人工标签，用于评价检测器。
- **来源：** [精读笔记](notes/core/C12_RAGTruth.md)；[论文页面](https://arxiv.org/abs/2401.00396)

## C13 · FELM: Benchmarking Factuality Evaluation of Large Language Models

- **层级／研究角色：** core／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 E;J;H
- **研究定位：** 多领域细粒度事实基准
- **需核查的条件或限制：** 声明分解、金标参考与数据版本。
- **阅读笔记中的证据片段：** FELM收集LLM在开放式提示下自然生成的错误，标注细粒度segment和证据，用来评价自动事实检测器。它不是单纯给生成模型排“谁幻觉更多”的榜。与只覆盖维基实体或新闻摘要的基准相比，扩展到世界知识、科技、数学、推理和写作推荐。
- **来源：** [精读笔记](notes/core/C13_FELM.md)；[论文页面](https://arxiv.org/abs/2310.00741)

## C14 · Do My Eyes Deceive Me? A Survey of Human Evaluations of Hallucinations in NLG

- **层级／研究角色：** core／综述/概念
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 H；次类 J
- **研究定位：** 人工评价及报告可靠性
- **需核查的条件或限制：** 标注程序、定义与样本选择。
- **阅读笔记中的证据片段：** 这篇元研究考察幻觉人评如何定义、执行和报告，目的是检查作为自动指标“金标准”的人工标签是否有充分的程序依据。核心结论是定义和报告方式差异很大，很多研究缺少评价指南、界面、质量保证、IAA和参与者信息。它主要提供报告透明度证据，不直接测量人工标签正确率、所有人评的总体可靠性或某个自动检测器性能。
- **来源：** [精读笔记](notes/core/C14_Human_Evaluation_Survey.md)；[论文页面](https://aclanthology.org/2025.inlg-main.4/)

## C15 · An Audit on the Perspectives and Challenges of Hallucinations in NLP

- **层级／研究角色：** core／综述/概念
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 —；次类 无
- **研究定位：** 概念及术语审计
- **需核查的条件或限制：** 社会技术情境、实践者问卷与感知。
- **阅读笔记中的证据片段：** 本篇结合两个研究：103篇同行评审论文的概念审计，以及171名研究者/实践者的问卷。RQ1考察幻觉的定义和框架，RQ2考察研究者的理解与实际遭遇。它不是幻觉检测器、生成模型测评榜或对真实幻觉发生率的估计。
- **来源：** [精读笔记](notes/core/C15_Hallucination_Audit.md)；[论文页面](https://aclanthology.org/2024.emnlp-main.375/)

## C16 · The Pitfalls of Defining Hallucination

- **层级／研究角色：** core／综述/概念
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 —；次类 无
- **研究定位：** 定义与测量有效性
- **需核查的条件或限制：** 双向蕴含、遗漏、语用、任务适配。
- **阅读笔记中的证据片段：** 作者指出不同“幻觉分类”隐含不同评估目标：有的只问输出是否包含来源不支持的信息，有的再分冲突与无法支持，有的按错误数字、实体、词语分类。分类之间并不一一对应，也可能漏掉信息遗漏。核心贡献是用双向逻辑蕴含对结构化数据到文本任务给出更系统的分析，然后明确这种分析向开放LLM任务推广的限制。
- **来源：** [精读笔记](notes/core/C16_Defining_Hallucination.md)；[论文页面](https://aclanthology.org/2024.cl-2.10/)

## I001 · Factuality of Large Language Models: A Survey

- **层级／研究角色：** important／综述/概念
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 —；次类 无
- **研究定位：** 事实性/来源支持/相关性的概念边界及分解—检索—验证中间评价
- **需核查的条件或限制：** 二手综述证据、输出协议身份、开放世界识别、粒度/顺序/宏微及错误先验。
- **阅读笔记中的证据片段：** 作者尝试把术语、评估、改善和工程难点放在同一框架。结构为：第2节澄清hallucination/factuality/trustworthiness；第3节按答案空间讨论评估；第4节按模型生命周期梳理改善；第5节简述视觉语言；第6节提出中间步骤评价、检索和延迟的瓶颈。真正适合本作业借鉴的是评价构念与管线误差，而不是将所有改善方法都展开成同等篇幅。
- **来源：** [精读笔记](notes/important/I001_Factuality_Survey.md)；[论文页面](https://aclanthology.org/2024.emnlp-main.1088/)

## I002 · A New Benchmark and Reverse Validation Method for Passage-level Hallucination Detection

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 E
- **研究定位：** 黑盒整段实体反向问答/特征匹配自检
- **需核查的条件或限制：** any-error目标与百分比容错、实体去名/substring/别名、全阳性子集及阈值先验、缓存复算、热门度代理和多角色知识相关性。
- **阅读笔记中的证据片段：** 作者提出PHD：以实体为主题的整段Wikipedia式回答，只要一处非事实或不可核实就判non-factual；提出Reverse Validation（RV）：从回答构造描述问题，再让LM反向找实体，与原实体比较。动机是在检测到可能错误时才启动昂贵检索，或在无数据库时作初筛。
- **来源：** [精读笔记](notes/important/I002_PHD_Reverse_Validation.md)；[论文页面](https://arxiv.org/abs/2310.06498)

## I003 · A Token-level Reference-free Hallucination Detection Benchmark for Free-form Text Generation

- **层级／研究角色：** important／基准/数据
- **评价对象：** 来源忠实性
- **技术：** 主类 —；次类 H;T
- **研究定位：** 已知词/短语目标的无原文推理二元判别
- **需核查的条件或限制：** 有原文人核、扰动/主动选样、前缀/双向权限、共识选择、词子词索引、概率特征身份、Brier及隐藏测试复现边界。
- **阅读笔记中的证据片段：** HADES是较早的细粒度、无外部reference的幻觉基准。每条样本给一篇经过扰动的Wikipedia文本、已高亮的目标词/短语和目标位置，要求判断这个指定目标是否hallucination。数据中其他位置即使也错，标注任务要求忽略。它不是让模型从整篇自由搜索全部错误，也没有报告端到端候选发现recall或精确span边界F1。
- **来源：** [精读笔记](notes/important/I003_HADES.md)；[论文页面](https://arxiv.org/abs/2104.08704)

## I004 · BAMBOO: A Comprehensive Benchmark for Evaluating Long Text Modeling Capacities of Large Language Models

- **层级／研究角色：** important／基准/数据
- **评价对象：** 来源忠实性
- **技术：** 主类 —；次类 无
- **研究定位：** 长文来源条件的句子/摘要级二元支持性判断
- **需核查的条件或限制：** **Yes/非幻觉正类**与反向指标、合成扰动/缺证据、格式评分、长度/指令/证据位置/检索成本及多任务分母。
- **阅读笔记中的证据片段：** 论文的总目标是长文本建模评价，五任务分别为问答、幻觉检测、文本排序、说话人预测与私有API代码补全，不是一篇覆盖全部幻觉类型的综合检测论文。两项相关数据 SenHallu 和 AbsHallu 给整篇NLP论文作来源、再给一句话假设或摘要级假设，模型回答假设是否由来源蕴涵。正文把“与来源冲突或超出来源”都称hallucination（本地PDF4页）；公开prompt明示来源蕴涵答Yes，冲突或任何hallucination答No。因而目标最接近长来源条件的二元支持性／事实一致性判断，并非无来源世界知识核查、开放式生成的错误率，也不提供错误位置或修正。论文文字又用“蕴涵或矛盾”概括二分，却没有明确中性／未提及样本怎样构造、标注和区分；不能预设“未提及必为矛盾”。
- **来源：** [精读笔记](notes/important/I004_BAMBOO.md)；[论文页面](https://arxiv.org/abs/2309.13345)

## I005 · ETF: An Entity Tracing Framework for Hallucination Detection in Code Summaries

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 E；次类 J;H
- **研究定位：** 代码来源条件的实体—描述句核验
- **需核查的条件或限制：** AST/NER覆盖、函数版本、unknown外部依赖、entity与summary宏指标及any-error聚合。全CSV审计尚待下载。
- **阅读笔记中的证据片段：** 本文评估Java代码摘要是否忠实说明给定代码，属于来源条件的事实一致性，不是检查生成代码可否编译，也不是评价摘要的完整性、简洁性或代码自身是否正确。真实程序中的函数名、注释可能误导模型，因此“摘要看起来合理”不足以证明与实现一致。
- **来源：** [精读笔记](notes/important/I005_ETF.md)；[论文页面](https://arxiv.org/abs/2410.14748)

## I006 · Enoki: Efficient Multi-Level Hallucination Detection

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 E；次类 T;J
- **研究定位：** 文本锚定OpenIE事实的claim核验与span投影
- **需核查的条件或限制：** 三元组遗漏/递进多计、neutral并入冲突、教师自动标注、Span Coverage F1单字符满分反例、来源聚类/阈值/后端成本及数据版本。
- **阅读笔记中的证据片段：** 输入是参考context与模型生成answer，目标同时输出可核验的事实单位、每单位是否由来源支持、以及answer中的错误字符span。ENOKI把回答按spaCy切句，抽取与回答词面锚定的OpenIE三元组(subject,predicate,object)，把每个三元组言语化成假设，经NLI式验证；不被来源蕴涵的三元组将其object或递进新信息delta投影回原回答字符位置。因此它绕过“先完全自由改写原子命题、再把错误命题反向对齐字符串”的独立对齐步骤，但仍依赖抽取器产生准确字符span、分组和映射；称“无需单独claim-to-span alignment模块”不能简化成“无需对齐”。
- **来源：** [精读笔记](notes/important/I006_ENOKI.md)；[论文页面](https://arxiv.org/abs/2609.00581)

## I007 · FRANK: A Benchmark for Factuality Metrics

- **层级／研究角色：** important／元评估/审计
- **评价对象：** 来源忠实性
- **技术：** 主类 —；次类 H;E;T
- **研究定位：** 错误分类与元评估
- **需核查的条件或限制：** 生成器混杂、人工标签、官方修正和共同样本相关重算。
- **阅读笔记中的证据片段：** 一个指标可以凭借识别某个生成器的风格，获得很高的汇总相关性，却不能在同一生成器内部区分事实正确与错误的摘要。FRANK同时提供语言学错误分类、人工标注基准和控制模型/数据集后的元评估。因此它不只是“又一个摘要数据集”，而是综述中讨论评价混杂、错误覆盖与人评可靠性的关键原始证据。
- **来源：** [精读笔记](notes/important/I007_FRANK.md)；[论文页面](https://aclanthology.org/2021.naacl-main.383/)

## I008 · FactCHD: Benchmarking Fact-Conflicting Hallucination Detection

- **层级／研究角色：** important／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 T;J;H
- **研究定位：** 复杂推理合成问答检测与标签条件解释监督
- **需核查的条件或限制：** 阳性F1/格式覆盖、词面解释元评价、知识信息预算、多角色错误相关性、label/reason身份及训练测试完整重复。
- **阅读笔记中的证据片段：** 论文关注给定用户问题Q和模型回答R，判断是否有fact-conflicting hallucination，并生成解释。与只输出一个分数的检测不同，它要求标签和理由；与RAGTruth、FAVA不同，主评价不要求完整错误字符跨度；与TruthfulQA不同，它主要评估检测器对固定问答的判断，不能把检测F1当被检测生成器本身的真确率。
- **来源：** [精读笔记](notes/important/I008_FactCHD.md)；[论文页面](https://arxiv.org/abs/2310.12086)

## I010 · Fine-grained Hallucination Detection and Editing for Language Models

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 J；次类 H
- **研究定位：** 开放域六类细粒度事实性与检索编辑的合成监督
- **需核查的条件或限制：** 不可核实/主观构念、句级类型与span区别、批次/多标分母、标签可逆性、宏平均身份、检索配置/信息保留及公开代码复现缺口。
- **阅读笔记中的证据片段：** FAVA同时提出六类幻觉分类、FAVABENCH人标基准和一个检索增强的检测/编辑模型。任务不只判整篇有无错误，而是说明哪里错、是哪一类、可否局部改正。模型以Llama2-Chat7B初始化，用合成错误及带类型的修订目标训练；推理时检索证据，再生成带标签与修改的原文。
- **来源：** [精读笔记](notes/important/I010_FAVA.md)；[论文页面](https://arxiv.org/abs/2401.06855)

## I011 · FreshLLMs: Refreshing Large Language Models with Search Engine Augmentation

- **层级／研究角色：** important／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 E;J;H
- **研究定位：** 时间敏感的开放域问答和宽松/严格双模式评价
- **需核查的条件或限制：** 错误前提、附加事实与拒答、FreshEval人机一致口径、搜索证据/答框/提示长度混杂、动态金标与历史API版本。
- **阅读笔记中的证据片段：** FreshQA要求回答开放式现实世界问题，按答案更新速度分四类：never-changing、slow-changing（数年内变）、fast-changing（一年内或更快）、false-premise（题目预设本身是假的）。每类再有一跳和多跳。构造时NLP研究者和线上雇员写题，手工剔除重复、无效、争议/过易，验证答案与支持URL，收集别名/日期格式等有效答案，并记录下一次检查日期；超过每周更新频率的题被排除。600条为test四类各125，共500；dev四类各25，共100；另15例从候选池提作few-shot示范，并非额外“615条test”。dev当时未用于论文选参，但后续方法研究可能使用，不能永久称其独立。随着动态答案变化，题目可能重分类，保持每类125只对初始版本成立（PDF2–3）。
- **来源：** [精读笔记](notes/important/I011_FreshLLMs_FreshQA.md)；[论文页面](https://arxiv.org/abs/2310.03214)

## I012 · Generating Benchmarks for Factuality Evaluation of Language Models

- **层级／研究角色：** important／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 U;E
- **研究定位：** 受控事实集合上的白盒LM四选一似然排序测验
- **需核查的条件或限制：** 五类扰动/NLI与语言模型过滤、真假候选标签污染、知识与表层捷径、检索证据、成对与四选一指标区别及开放生成筛选/neutral分母。
- **阅读笔记中的证据片段：** 作者认为在自由生成后抽取事实做核验会偏向模型本来容易生成的常见事实，长尾事实覆盖不足。FACTOR把预先选定的真实语料变为“前缀t+原文事实续句c++三条经扰动的反事实候选c-”，测模型是否将原文候选排第一。这使考察事实集合由语料决定，而不是由被测模型选择生成什么。它仍是受控四选一似然排序代理指标，不是观察到的自由生成幻觉发生率，也不是对任意模型回答逐句判真；需要可访问每个候选的token概率，不适用于只返回文本的纯黑盒API。
- **来源：** [精读笔记](notes/important/I012_FACTOR.md)；[论文页面](https://arxiv.org/abs/2307.06908)

## I013 · HALoGEN: Fantastic LLM Hallucinations and Where to Find Them

- **层级／研究角色：** important／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 E;J;H
- **研究定位：** 九场景生成事实与拒答的跨域基准
- **需核查的条件或限制：** 来源/世界参照混合、每回答宏原子错误率与微率、空原子分母、程序/索引/LLM核验器覆盖、真值单类推理、引用存在与支持区别、训练语料A/B/C归因强度及资源计数审计。
- **阅读笔记中的证据片段：** HALoGEN提供10923提示、九类场景，约14模型×10923≈152922潜在响应，摘要约150k为近似值。九类题目计数相加准确：代码包1085、科学文献1780、摘要1278、简化1000、人物传记682、历史会面1500、错误预设1084、二元推理1500、数值推理1014，合计10923。前六（代码、摘要、简化、传记、二元和数值推理）预期回答，后三（科学文献、历史会面、错误预设）预期拒答。二元推理虽然用单类正确答案筛选题目，表1仍把它归“应答”而非“拒答”；该分类直接决定utility公式。
- **来源：** [精读笔记](notes/important/I013_HALoGEN.md)；[论文页面](https://aclanthology.org/2025.acl-long.71/)

## I014 · HalluLens: LLM Hallucination Benchmark

- **层级／研究角色：** important／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 J;H
- **研究定位：** 训练语料/输入一致性定义与动态外在幻觉测验
- **需核查的条件或限制：** Wikipedia训练代理、动态题的金标质量、拒答—条件错误—总体正确三分母、LongWiki检索/裁判误差及F1聚合、虚构实体存在性、药域全拒答、裁判提示与现存解析代码口径。
- **阅读笔记中的证据片段：** 作者主张事实性相对外部可信真值和时间判断，幻觉相对模型实际接触过的训练语料或当前用户输入判断。其“extrinsic幻觉”是输出与训练语料不一致，且输入没有支持/否定；“intrinsic幻觉”是输出与当前输入不一致。按此定义，模型照搬训练语料中的过时错误可“不幻觉但不真实”；生成与输入冲突的现实真事实则“幻觉但事实正确”。这是作者的操作性立场，并非领域公认且可直接验证的普适分类：实际训练集、去重、时间和模型是否真正见过/记住某事实通常不可观测；“语料中任一材料支持即不幻觉”在互相矛盾来源下会过宽。综述应把这个观点与FreshQA时效事实性、HALoGEN多源定义、FActScore世界知识验证并列讨论，不把“过时错误不算幻觉”说成客观定理。
- **来源：** [精读笔记](notes/important/I014_HalluLens.md)；[论文页面](https://aclanthology.org/2025.acl-long.1176/)

## I015 · Hallucinated but Factual! Inspecting the Factuality of Hallucinations in Abstractive Summarization

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 E；次类 H
- **研究定位：** 实体概率与世界事实性
- **需核查的条件或限制：** 源外真实、标注Unknown映射、KNN监督、指标作奖励及源码缩放。
- **阅读笔记中的证据片段：** 摘要中来源未明确支持的实体不一定现实错误；正确背景信息可改善理解，例如将只有姓的Juncker补全姓名与职务。作者提出ENTFA，分别判断entity是否由来源支持、是否世界真实；并用分类器作离线RL奖励减少非事实实体。本文是C01/C04“factual hallucination”讨论的原始实证来源，应优先引用，而非只复述综述概念。
- **来源：** [精读笔记](notes/important/I015_EntFA_Factual_Hallucination.md)；[论文页面](https://aclanthology.org/2022.acl-long.236/)

## I016 · Hallucination Detection: A Probabilistic Framework Using Embeddings Distance Analysis

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 U
- **研究定位：** 关键词嵌入/类内距离KDE的响应分类代理
- **需核查的条件或限制：** 截止日期即真假标签的模型身份混淆、同题重采样、成对距离伪重复、KDE概率/超参选择、附录反例、跨数据集基线不可比和增长百分比算术。
- **阅读笔记中的证据片段：** 作者希望用“幻觉文本和非幻觉文本在嵌入空间距离分布不同”建立检测器。核心数据构造：问GPT-4设计64个关于2022-09至2023-09时段的问题，分别给Llama-2-7B与Llama-3.1-8B多次采样；根据作者所写训练截止时间，把所有Llama-2答案标为幻觉，把所有Llama-3.1答案标为非幻觉。没有对任一回答逐条事实标注，也没有列出“该模型实际知道/不知道此事实”的核验。其实际监督目标是生成模型身份与训练截止标签，与回答真假完全重合；即便分类准确，也无法从现有设置识别距离差异来自真假、模型风格、训练语料、模型规模、量化误差或采样。论文自己限制节承认Llama-3.1会有被错标真实的回答，但没有承认Llama-2也可能正确回答后截止事实（可从上下文推理、广泛规律、拒答、推测偶中或更新模型等）。“没有事后知识⇒必然幻觉”在逻辑上不成立。
- **来源：** [精读笔记](notes/important/I016_Embedding_Distance.md)；[论文页面](https://arxiv.org/abs/2502.08663)

## I017 · Halo: Estimation and Reduction of Hallucinations in Open-Source Weak Large Language Models

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 U
- **研究定位：** 黑盒多答句级蕴含一致性
- **需核查的条件或限制：** SummaC有向算子与对称性断言、NBA人标相关和标注单位、知识注入的实体/事实泄漏、教师阈值调用成本、简答/CoT反向量化结果与一致错答盲点。原HALOCHECK最终实现及原始人标待核。
- **阅读笔记中的证据片段：** 论文围绕三个问题：RQ1能否无外部知识地估计幻觉严重程度，RQ2能否在不追加人工指令的条件下向BLOOM7B注入NBA领域知识，RQ3能否用GPT-4教师在推理时选择性改进学生答案。其核心HALOCHECK对同一题采样n=5条回答，计算回答之间的句级SummaCzs推理分数，再求成对平均μ；作者称范围[-1,1]，负值视为矛盾、正值视为一致。n=5作者注明是任意选取，未报告采样数敏感性。该量的直接构念是回答集合的相互一致程度，不是单条回答对世界事实或给定证据的正确率；稳定重复的错答可获高分，彼此不同但都正确的答法可能低分。论文自己在PDF6承认两者可分，在PDF7承认事实性相关弱于一致性相关。因此综述应把它放进黑盒自一致检测，而非有外部证据的事实核验。
- **来源：** [精读笔记](notes/important/I017_HALO_HaloCheck.md)；[论文页面](https://arxiv.org/abs/2308.11764)

## I018 · Language Models Hallucinate, but May Excel at Fact Verification

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 J；次类 E
- **研究定位：** 有检索证据的指令模型事实裁判与人工元评估
- **需核查的条件或限制：** 生成任务段落保留分母、无证≠虚假、答案词软概率/硬标签接口、检索/对抗证据质量、真句比例与any-error聚合、共指/数词迁移及SciFact训练污染。公开原始行/源码待固定提交复核。
- **阅读笔记中的证据片段：** 研究先问开放生成在熟悉的维基百科领域究竟多不真实，再问把指令微调模型改作事实判断器是否有效。比较生成器FLAN-T5-11B、Llama-30B、Llama-65B、GPT-3.5（注释定义为text-davinci-003，并非本文另作核验器的gpt-3.5-turbo-0301/ChatGPT）。两种生成任务：SENTCOM接续FEVER测试事实句的前两token；PARAGEN给Wikipedia实体写五句事实段落。四模型×每任务50输入，共400原始生成陈述，用贪心解码和五条人工挑选的事实演示。输入来自FEVER和Wikipedia标题，论文限制了段落实体词在WebText出现100次；其“长尾”是相对SENTCOM，不等同稀有实体任意覆盖。
- **来源：** [精读笔记](notes/important/I018_LLM_Fact_Verification.md)；[论文页面](https://aclanthology.org/2024.naacl-long.62/)

## I019 · Learning to Reason for Hallucination Span Detection

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 J
- **研究定位：** 字符跨度结果奖励的任务专门推理训练
- **需核查的条件或限制：** gold最佳候选、宏奖励/字符微指标、类别mask/标准化、解释忠实性、质量筛选、STD约束与二元/定位及重训/迁移区别。
- **阅读笔记中的证据片段：** RL4HS把幻觉跨度检测看成“提取回答断言→检查输入支持→输出不支持文本”的多步过程，研究显式CoT和任务专门RL能否改善定位。模型从context与answer生成解释和JSON字符串列表，用span-F1作结果奖励，再以GRPO训练；作者提出CAPO调节非幻觉类优势权重，缓解保守地输出空列表的问题。
- **来源：** [精读笔记](notes/important/I019_RL4HS.md)；[论文页面](https://arxiv.org/abs/2510.02173)

## I020 · Monitoring Decoding: Mitigating Hallucination via Evaluating the Factuality of Partial Response during Generation

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 J;E
- **研究定位：** 强参考模型概率比监测的局部token重解码
- **需核查的条件或限制：** 论文加权和/现行代码乘积的版本差异、70B专家信息/成本权限、Top-N候选覆盖、任务真值/裁判差异、延迟吞吐不自洽、重采样token比例错列及直接专家基线。发表提交与模型运行待核。
- **阅读笔记中的证据片段：** 作者认为多次完整采样仍可能反复产生高置信错token，因此每生成m个token就监测这段，若风险高则对该段树搜索替换。目标模型为Llama-2-7B-chat、Llama-3-8B-Instruct、Gemma-2-2B-it；每个小模型都有同家族大专家Llama-2-70B、Llama-3-70B、Gemma-2-27B作参考，需读取两模型同一token的下一词概率。故这是推理时引入强模型和内部logit访问的方法，不是小模型自身的免费不确定度，也不是黑盒或独立外部事实核验器。专家更偏好某token并非该token必真：风格、分词和长尾偏好可影响概率比，专家也会共享错误。论文限制节承认训练知识源缺失时无法纠错，需要外部资料。
- **来源：** [精读笔记](notes/important/I020_Monitoring_Decoding.md)；[论文页面](https://arxiv.org/abs/2503.03106)

## I021 · RealTime QA: What's the Answer Right Now?

- **层级／研究角色：** important／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 无
- **研究定位：** 动态时点问答与检索新鲜度评价
- **需核查的条件或限制：** 公告/证据/提交/评分四时钟、英语周级测验、GCS不足五篇旧Wiki补齐、NOTA选项替换/拒答口径、六周错误分析与全年EM分母差异、日期消融例外及固定金标下延后检索的时间锚错位。历史仓库快照与基线重算待核。
- **阅读笔记中的证据片段：** 论文批评静态QA“问题一旦采集答案永不变”的隐含假设，建立每周更新的英文新闻问答平台：每周六GMT03:00从CNN、USA Today、The Week的本周新闻测验抽约30道多选题，立即用Google Custom Search（GCS）搜上述站点，每题top10网页，解析保存文本、作者与发表日期；模型可使用平台检索包，也可自检索，提交窗口直到下周题发布。新闻来源与问题提取由作者人机协作，因此“实时”实际周级、美国/英国英语新闻范围，不是瞬时全网事实真值。页面后续不断更新，论文表1只对应2022-06-17至2023-06-02的1470题，此前另有2886题可供开发；不应把今日平台榜单和历史表1同一数据集横比。约10–12%的题由新事件触发却问稳定旧事实，论文保留以贴近自然提问；故闭卷模型有时答对不能一概视为时间泄漏。
- **来源：** [精读笔记](notes/important/I021_RealTime_QA.md)；[论文页面](https://arxiv.org/abs/2207.13332)

## I022 · Self-contradictory Hallucinations of Large Language Models: Evaluation, Detection and Mitigation

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 J
- **研究定位：** 同关系抽样触发的二句逻辑矛盾及迭代消冲突
- **需核查的条件或限制：** 原文内部矛盾/跨次采样区别、冲突不判定原句孰真、缺证算假标注、正确事实误删和句数式informativeness、两种SelfCheck比较目标、QA仅阳性人核下界与API token成本。原标注/旧模型复现待核。
- **阅读笔记中的证据片段：** 作者称当同一模型在同一上下文生成两个逻辑上不能同时成立的句子时存在self-contradiction。具体不是直接遍历原回答前后两个原有句子：先生成实体描述x=[x1…xn]，对原句xi用CompactIE抽取(subject,relation,object)，把对象o留空，给原模型同实体、前文x<i和(s,r,)提示，令其另做一次调用生成候选x′i；然后分析xi与x′i是否矛盾。摘要/引言“同一语境两句自矛盾”容易被误读为单篇输出内部矛盾；实际主表的17.7%是原输出中有至少一个抽样替代句与之矛盾的句子比例，不是原输出内任意相邻句矛盾率，也不是17.7%的原句已被外部真值证明为假。该区分直接影响与自一致、事实性检测方法比较。
- **来源：** [精读笔记](notes/important/I022_Self_Contradictory_Hallucinations.md)；[论文页面](https://arxiv.org/abs/2305.15852)

## I023 · Teaching with Lies: Curriculum DPO on Synthetic Negatives for Hallucination Detection

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 J
- **研究定位：** 作者目标是用高质量、难识别的幻觉负例改善二分类检测。对样本i，xi写成“context + question + task instruction”；ytrue被称为factual class completion / gold answer，yhall被称为hallucinated class completion / hallucinated answer，固定偏好对为(xi,ytrue,yhall)。DPO损失是标准偏好似然相对参考模型的logit差：-log σ{β[(log πθ(ytrue|x)-log πθ(yhall|x))-(log πref(ytrue|x)-log πref(yhall|x))]}，β=0.1。图2的医疗例也直观显示chosen是正确答案内容，rejected是错误答案内容；上下文和问题在提示中，但没有画出“待检测的候选答案”如何作为输入，以及是否让模型输出Yes/No。PDF3同时宣称任务…
- **需核查的条件或限制：** 作者目标是用高质量、难识别的幻觉负例改善二分类检测。对样本i，xi写成“context + question + task instruction”；ytrue被称为factual class completion / gold answer，yhall被称为hallucinated class completion / hallucinated answer，固定偏好对为(xi,ytrue,yhall)。DPO损失是标准偏好似然相对参考模型的logit差：-log σ{β[(log πθ(ytrue|x)-log πθ(yhall|x))-(log πref(ytrue|x)-log πref(yhall|x))]}，β=0.1。图2的医疗例也直观显示chosen是正确答案内容，rejected是错误答案内容；上下文和问题在提示中，但没有画出“待检…
- **阅读笔记中的证据片段：** 作者目标是用高质量、难识别的幻觉负例改善二分类检测。对样本i，xi写成“context + question + task instruction”；ytrue被称为factual class completion / gold answer，yhall被称为hallucinated class completion / hallucinated answer，固定偏好对为(xi,ytrue,yhall)。DPO损失是标准偏好似然相对参考模型的logit差：-log σ{β[(log πθ(ytrue|x)-log πθ(yhall|x))-(log πref(ytrue|x)-log πref(yhall|x))]}，β=0.1。图2的医疗例也直观显示chosen是正确答案内容，rejected是错误答案内容；上下文和问题在提示中，但没有画出“待检测的候选答案”如何作为输入，以及是否让模型输出Yes/No。PDF3同时宣称任务…
- **来源：** [精读笔记](notes/important/I023_Teaching_with_Lies.md)；[论文页面](https://arxiv.org/abs/2505.17558)

## I024 · The Dawn After the Dark: An Empirical Study on Factuality Hallucination in Large Language Models

- **层级／研究角色：** important／领域实证/现象分析
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 无
- **研究定位：** 本文把实事幻觉分六类：实体错、关系错、不完整、过时、过度宣称、不可核实。类型不是互斥：一个不完整列表也可能含假的书名；“不可核实”是证据状态，不能逻辑等同已证伪。PDF14表8同一个“列十本书”例列在不完整与不可核实两栏，说明标注类型边界重叠；过时性必须有问答时点，PDF14“现任美国总统”实例不能脱离论文/请求发生时间重新打分。综述应把真实性、可验证性、完整性和时效性作为不同维度。
- **需核查的条件或限制：** 见原笔记；本卡未自动抽出限制段落。
- **阅读笔记中的证据片段：** 本文把实事幻觉分六类：实体错、关系错、不完整、过时、过度宣称、不可核实。类型不是互斥：一个不完整列表也可能含假的书名；“不可核实”是证据状态，不能逻辑等同已证伪。PDF14表8同一个“列十本书”例列在不完整与不可核实两栏，说明标注类型边界重叠；过时性必须有问答时点，PDF14“现任美国总统”实例不能脱离论文/请求发生时间重新打分。综述应把真实性、可验证性、完整性和时效性作为不同维度。
- **来源：** [精读笔记](notes/important/I024_Dawn_After_Dark.md)；[论文页面](https://aclanthology.org/2024.acl-long.586/)

## I026 · FactCheckmate: Preemptively Detecting and Mitigating Hallucinations in LMs

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 U
- **研究定位：** 研究问能否在生成开始前，只看输入问句在白盒LM中的hidden states，判断该LM将来是否给错答案，并在预判风险时改一次内部状态。四个数据集：NQ-open、MMLU、MedMCQA、GSM8K；多选题被转为问题与金答案对，GSM8K只保留最终答案。每个样本先让同一LM根据few-shot问句生成输出，再以输出与唯一金答案exact match给该LM的输入hidden states二元标签；错即“nonfactual/hallucination”，对即“factual”。训练数据按标签下采样近似平衡，各LM共用测试题但有不同训练/验证分割。表6 NQ 6666/4666/1000/1000，MMLU 1844/1292/276/276，MedMCQA 2000/1400/300/300，GSM8K 1040/728/156/156；70/15/15约数。
- **需核查的条件或限制：** 在某层FFN后取输入token隐状态hi^(l)，对token做mean/max/last pooling，再两层ReLU-MLP+sigmoid。按模型和数据集在验证集选层，中后层常较好；训练BCELoss/Adam学习率1e-4、dropout.1、最多50 epoch、验证准确率早停。正文明确fθ输出“将幻觉的概率”，但是图1与PDF6称当分类概率小于等于α=.3才干预，且随机干预候选选fθ概率最高者；若fθ确为幻觉概率，这两个决策方向与目标相反。可能代码将标签1设为正确，或文字写错；必须从数据标签、sigmoid输出、阈值和候选选择代码统一核定。现有PDF内部无法裁决，不能在综述中把方向写死。干预位置为输入最后token、选定层，只调整首个解码步；不同于逐token纠错。
- **阅读笔记中的证据片段：** 研究问能否在生成开始前，只看输入问句在白盒LM中的hidden states，判断该LM将来是否给错答案，并在预判风险时改一次内部状态。四个数据集：NQ-open、MMLU、MedMCQA、GSM8K；多选题被转为问题与金答案对，GSM8K只保留最终答案。每个样本先让同一LM根据few-shot问句生成输出，再以输出与唯一金答案exact match给该LM的输入hidden states二元标签；错即“nonfactual/hallucination”，对即“factual”。训练数据按标签下采样近似平衡，各LM共用测试题但有不同训练/验证分割。表6 NQ 6666/4666/1000/1000，MMLU 1844/1292/276/276，MedMCQA 2000/1400/300/300，GSM8K 1040/728/156/156；70/15/15约数。
- **来源：** [精读笔记](notes/important/I026_FACTCHECKMATE.md)；[论文页面](https://arxiv.org/abs/2410.02899)

## I027 · Adversarial NLI for Factual Correctness in Text Summarisation Models

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 E
- **研究定位：** 对抗监督与域外排序迁移
- **需核查的条件或限制：** 基线实现差异、小基准重复使用、注意力解释与示例标签核查。
- **阅读笔记中的证据片段：** I036指出SNLI/MNLI训练NLI不能可靠排序摘要，且可能依赖词重合捷径。本文提出：先MNLI再用human-and-model adversarial收集的ANLI继续微调，能否提高事实正确候选的排序？这是一种改变训练数据以增加推理鲁棒性的路线，不是直接LLM事实裁判或检索核验。
- **来源：** [精读笔记](notes/important/I027_Adversarial_NLI.md)；[论文页面](https://arxiv.org/abs/2005.11739)

## I029 · Beyond Factuality: A Comprehensive Evaluation of Large Language Models as Knowledge Generators

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 E；次类 J
- **研究定位：** 本文不是直接给最终回答一个单独幻觉分数：形式化两阶段q→k→a，k可来自Wikipedia DPR检索或LLM生成。评价中间知识k的内在四维：事实性（外证据支持/未验证/反证）、相关性、连贯性、信息量；评价用k后的回答a的外在两维：帮助性、有效性。错误模式从NQ和Wizard of Wikipedia各类共160个LLaMA案例主题分析出发。最终实验NQ、WoW测试各随机500例，DPR、FLAN-T5、LLaMA、所谓ChatGPT零/少样本知识生成；回答生成又使用few-shot。如此比较改变了知识来源、模型家族、提示长度和任务，观察到k事实性与a正确率不一一对应是有用现象，但不能推出“事实上错误知识无害”。应区分：①错误是否落在回答所需的关键原子；②检索知识是否相关；③下游生成器是否采纳错误。
- **需核查的条件或限制：** 1. 重新定义可解释的三类事实标签：保留每个si/eij NLI三维原值，先按证据冲突策略合成句级support/refute/unknown互斥标签，再按原子/句段报告比例和校准；对表2 108.55%行追溯代码/表格，避免逐维极值当概率。 2. 验证蕴涵方向与参考依赖：以PRC/China、部分正确、条件/否定、反证与无证样本，分别调用NLI(evidence,claim)及反向，检查式1/7实际代码，比较人工标签。把NQ需金答案的有效性与中间k无参考的事实性分开标注。 3. 从观察到干预：固定同一q、下游回答模型和提示，用正确相关、错误相关、正确不相关、错误不相关的受控知识替换，测答案正确率/采纳率，按关键原子和非关键原子分层；这样才能估事实性与相关性的因果作用。 4. 公平基线和回答质量：加入对话专用检索器、相同知识长度/预算、Wikiped…
- **阅读笔记中的证据片段：** 本文不是直接给最终回答一个单独幻觉分数：形式化两阶段q→k→a，k可来自Wikipedia DPR检索或LLM生成。评价中间知识k的内在四维：事实性（外证据支持/未验证/反证）、相关性、连贯性、信息量；评价用k后的回答a的外在两维：帮助性、有效性。错误模式从NQ和Wizard of Wikipedia各类共160个LLaMA案例主题分析出发。最终实验NQ、WoW测试各随机500例，DPR、FLAN-T5、LLaMA、所谓ChatGPT零/少样本知识生成；回答生成又使用few-shot。如此比较改变了知识来源、模型家族、提示长度和任务，观察到k事实性与a正确率不一一对应是有用现象，但不能推出“事实上错误知识无害”。应区分：①错误是否落在回答所需的关键原子；②检索知识是否相关；③下游生成器是否采纳错误。
- **来源：** [精读笔记](notes/important/I029_CONNER_Beyond_Factuality.md)；[论文页面](https://arxiv.org/abs/2310.07289)

## I031 · Evaluating Factuality in Generation with Dependency-level Entailment

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 E
- **研究定位：** 依存关系蕴含
- **需核查的条件或限制：** 弱监督、局部判断/整体聚合差距、单句来源、排序基准冲突样本。
- **阅读笔记中的证据片段：** 句子级NLI即使在标准蕴含测试准确，也未必能识别生成错误，且不给出错误位置。DAE把输出的增强依存弧作为判断单位：给定来源x和生成文本h，判断弧a表达的head–child语义关系是否由x支持。假定来源和输出的事件/参与者大体对应，除非有证据反对；不是独立核验输出中现实世界实体。
- **来源：** [精读笔记](notes/important/I031_Dependency_Arc_Entailment.md)；[论文页面](https://aclanthology.org/2020.findings-emnlp.322/)

## I032 · FacTool: Factuality Detection in Generative AI -- A Tool Augmented Framework for Multi-Task and Multi-Domain Scenarios

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 E；次类 J
- **研究定位：** 统一流水线是：从生成响应抽claims→每claim生成工具查询→调用工具→收集证据→让规则/LLM判断agreement。统一的是软件接口，四任务的真值对象并不统一：
- **需核查的条件或限制：** I-Chun Chern、Steffi Chern、Shiqi Chen、Weizhe Yuan、Kehua Feng、Chunting Zhou、Junxian He、Graham Neubig、Pengfei Liu，FacTool: Factuality Detection in Generative AI — A Tool Augmented Framework for Multi-Task and Multi-Domain Scenarios。本地arXiv:2307.13528v2（2023-07-26）PDF共25页：1–12页全部正文、13–15页参考、16–25页完整提示和成功/失败案例逐页读；目视核对PDF8表3–4、PDF9表5、PDF12表6、PDF20/22/25失败案例。作者FACTOOL仓库当前README、支持任务、依…
- **阅读笔记中的证据片段：** 统一流水线是：从生成响应抽claims→每claim生成工具查询→调用工具→收集证据→让规则/LLM判断agreement。统一的是软件接口，四任务的真值对象并不统一：
- **来源：** [精读笔记](notes/important/I032_FACTOOL.md)；[论文页面](https://arxiv.org/abs/2307.13528)

## I033 · LLM-based NLG Evaluation: Current Status and Challenges

- **层级／研究角色：** important／综述/概念
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 —；次类 无
- **研究定位：** 图1给出四类：
- **需核查的条件或限制：** Mingqi Gao、Xinyu Hu、Xunjian Yin、Jie Ruan、Xiao Pu、Xiaojun Wan，LLM-based NLG Evaluation: Current Status and Challenges，《Computational Linguistics》51(2)，2025，页661–687。资料库PDF共27页：PDF1–20为摘要、正文、结论与致谢，PDF20–27为完整参考文献；全部逐页阅读。目视核对PDF3图1、PDF12表2、PDF19表4，保存于ReadingNotes/qa/I033p3.png、I033p12.png、I033p19.png。投稿日2024-11-26、修回2025-02-24、接收2025-03-14；作者称文献检索截止2024年6月，但定稿补入若干2025工作，因此“检索截止”和最…
- **阅读笔记中的证据片段：** 图1给出四类：
- **来源：** [精读笔记](notes/important/I033_LLM_based_NLG_Evaluation.md)；[论文页面](https://aclanthology.org/2025.cl-2.9/)

## I034 · Multi-Dimensional Evaluation of Text Summarization with In-Context Learning

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 J；次类 H
- **研究定位：** ICE用同一个LLM和少量(输入、摘要、人工分数)示例分别预测四维0–1分：
- **需核查的条件或限制：** 论文承认只做摘要、部分分析因费用用200样本、依赖175B外部模型。还应增加：闭源模型退役使原实验不可重跑；示例来自测试benchmark同分布；标签分布严重偏斜；prompt输出解析脆弱；只测相关不测事实错误定位；系统均值实验可能self-bias；没有成本、延迟、失败率。
- **阅读笔记中的证据片段：** ICE用同一个LLM和少量(输入、摘要、人工分数)示例分别预测四维0–1分：
- **来源：** [精读笔记](notes/important/I034_ICE.md)；[论文页面](https://arxiv.org/abs/2306.01200)

## I035 · On Faithfulness and Factuality in Abstractive Summarization

- **层级／研究角色：** important／领域实证/现象分析
- **评价对象：** 来源忠实性
- **技术：** 主类 —；次类 H;E;T
- **研究定位：** 忠实性/真实性双轴与XSum人工标注
- **需核查的条件或限制：** 参考导语偏差、NLI/QA、标注粒度和分数重算。
- **阅读笔记中的证据片段：** 来源不支持与世界不真实不是同一个概念。Intrinsic是使用输入已有信息却错误组合、归属或表达；extrinsic是加入来源未直接支持的信息。两类都可能包含真实内容，而可从文章合理推出的改写不算幻觉。作者明确接受能改善摘要、且符合文章与背景知识的真实补充，并未主张所有源外内容都必须删除。
- **来源：** [精读笔记](notes/important/I035_Faithfulness_and_Factuality.md)；[论文页面](https://arxiv.org/abs/2005.00661)

## I036 · Ranking Generated Summaries by Correctness: An Interesting but Challenging Application for Natural Language Inference

- **层级／研究角色：** important／元评估/审计
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 E;H
- **研究定位：** NLI下游元评估与候选重排
- **需核查的条件或限制：** 条件样本、候选预算、句对/全文能力差异及MACE人工标签。
- **阅读笔记中的证据片段：** 本文把“源文档是否蕴含生成摘要”转成NLI的下游测试，并通过重排固定生成候选来隔离检测器作用。只看标准NLI三分类准确率或ROUGE不能回答摘要是否有事实错误。图1“Prince George即将成为哥哥”被摘要成“Prince George将生第二胎”，词重合很高却主语关系严重错误。
- **来源：** [精读笔记](notes/important/I036_NLI_Summary_Ranking.md)；[论文页面](https://aclanthology.org/P19-1213/)

## I037 · SummEval: Re-evaluating Summarization Evaluation

- **层级／研究角色：** important／元评估/审计
- **评价对象：** 来源忠实性
- **技术：** 主类 H；次类 E;T;J
- **研究定位：** 人工评价与指标元评估资源
- **需核查的条件或限制：** 维度混淆、专家修订依赖、系统/实例层级、参考噪声和二值标签敏感性。
- **阅读笔记中的证据片段：** 本文主要贡献是统一评价资源与元评估，不是新幻觉检测器：14类自动评价方法、23篇模型论文的44套输出、统一API，以及专家与众包对16套模型输出的人评。主要问题是旧DUC/TAC评价经验可能无法迁移到质量更高、不同生成风格的神经摘要；各论文人评协议又不一致，难以比较。
- **来源：** [精读笔记](notes/important/I037_SummEval.md)；[论文页面](https://aclanthology.org/2021.tacl-1.24/)

## I040 · Do We Know What We Don’t Know? Studying Unanswerable Questions beyond SQuAD 2.0

- **层级／研究角色：** important／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 H;T
- **研究定位：** QA可答性部件的域外可靠性
- **需核查的条件或限制：** 竞争实体、IDK/不确定性区别、辅助NLI训练与公开数据跨度问题。
- **阅读笔记中的证据片段：** QA型事实指标常问“来源里能否回答这个问题”；若QA把来源无答案强行答成某个实体，就会污染答案比较或可答性分数。这篇不直接设计幻觉指标，而测试其重要部件——来源条件下识别不可答IDK——在域外是否可靠。应放在方法可靠性与QA部件迁移证据中，不伪装成直接评测长文本LLM幻觉的文章。
- **来源：** [精读笔记](notes/important/I040_Unanswerable_Beyond_SQuAD.md)；[论文页面](https://aclanthology.org/2021.findings-emnlp.385/)

## I041 · Evaluating Correctness and Faithfulness of Instruction-Following Models for Question Answering

- **层级／研究角色：** important／评价方法
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 E；次类 J;H
- **研究定位：** 作者把RAG/给段落QA拆成：
- **需核查的条件或限制：** 1. 二维真值矩阵：每个atomic claim分别标world-correct、supported-by-context、contradicted、unknown，再聚合回答；保留“正确但未归因”与“有来源但来源错误”。 2. 长度匹配与对抗最小对：对同答案加正确附加句、错误附加句、否定、候选列表和source原文复制，观察Recall/K-Precision能否区分；按回答长度配对模型。 3. 外部验证元评估：按question cluster拆分，不让四模型同题跨折；leave-one-model/domain-out，三分类faithfulness和claim/span指标并报；bootstrap按question而非行。 4. 拒答作为选择性预测：构造answerable、unanswerable、partial evidence、conf…
- **阅读笔记中的证据片段：** 作者把RAG/给段落QA拆成：
- **来源：** [精读笔记](notes/important/I041_Correctness_and_Faithfulness_QA.md)；[论文页面](https://arxiv.org/abs/2307.16877)

## I042 · FEQA: A Question Answering Evaluation Framework for Faithfulness Assessment in Abstractive Summarization

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 E；次类 无
- **研究定位：** QA来源核验
- **需核查的条件或限制：** 抽象性、人评筛选、答案匹配、问题覆盖和批量接口顺序。
- **阅读笔记中的证据片段：** 目标是评估生成摘要相对于来源的忠实性，不需要参考摘要，也不查世界知识。摘要能与文章就一组问题给出相同答案，可视作局部信息一致的证据。它并不检验文章自身真假，也不保证问题未覆盖的其他内容正确。
- **来源：** [精读笔记](notes/important/I042_FEQA.md)；[论文页面](https://aclanthology.org/2020.acl-main.454/)

## I043 · QuestEval: Summarization Asks for Fact-based Evaluation

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 E；次类 T
- **研究定位：** 双向QA综合评价
- **需核查的条件或限制：** 可答性/正确性、重要性政策、P/R目标冲突与公式/代码版本漂移。
- **阅读笔记中的证据片段：** 一篇摘要既应避免捏造，也应覆盖来源的重要信息。ROUGE等依赖人工参考，单一参考又只覆盖众多合理摘要的一种。QuestEval把这两个需求转成两个方向的问答：从摘要提问，来源能否给出同一答案；从来源提问，摘要能否回答重要问题。前者偏precision，后者偏recall。
- **来源：** [精读笔记](notes/important/I043_QuestEval.md)；[论文页面](https://arxiv.org/abs/2103.12693)

## I044 · ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 E;J;H
- **研究定位：** 域适配RAG裁判与PPI总体估计
- **需核查的条件或限制：** 合成监督、人工抽样、模拟系统排名和统计覆盖条件。
- **阅读笔记中的证据片段：** ARES将RAG评价分成context relevance、answer faithfulness、answer relevance，先合成训练数据、训练轻量分类裁判，再用少量人工标签的PPI校正系统均分并给区间。它不是完全无标签评价：需域内语料、约150或更多人工验证例和至少5个few-shot查询/答案示范，主实验实际用300标签。
- **来源：** [精读笔记](notes/important/I044_ARES.md)；[论文页面](https://aclanthology.org/2024.naacl-long.20/)

## I045 · Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 无
- **研究定位：** 论文问的是：只有黑盒文本接口时，LLM能否给自己的固定答案输出有意义的置信度？它把方法拆成三层：
- **需核查的条件或限制：** 论文问的是：只有黑盒文本接口时，LLM能否给自己的固定答案输出有意义的置信度？它把方法拆成三层：
- **阅读笔记中的证据片段：** 论文问的是：只有黑盒文本接口时，LLM能否给自己的固定答案输出有意义的置信度？它把方法拆成三层：
- **来源：** [精读笔记](notes/important/I045_Can_LLMs_Express_Their_Uncertainty.md)；[论文页面](https://arxiv.org/abs/2306.13063)

## I046 · Complex Claim Verification with Evidence Retrieved in the Wild

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 E；次类 J
- **研究定位：** 传统事实核查数据常直接提供人工justification，或允许搜索到声明发布后的事实核查文章；分类器会读到别人已经综合好的结论。本文要求系统只能使用声明发生时已经存在、且不来自已知fact-checking站点的原始网页，模拟新声明刚出现时的核查。
- **需核查的条件或限制：** 1. 时间有效证据审计：对每页人工核对首次发布日期、最后修改、内容版本和claim cutoff；比较URL时间过滤与真实Wayback快照。 2. 查询预算匹配：generated/gold/original claim在相同10 queries、相同返回页数和token成本下比较；评估subquestion factuality、去语境化与覆盖。 3. coverage × faithfulness二维前沿：每个gold subquestion标“检到支持/检到反证/仅相关/无证据”，每个summary claim标supported/contradicted/added；禁止把幻觉补全算覆盖。 4. 压缩受控实验：raw evidence、extractive 251 tokens、abstractive 251 tokens、oracle s…
- **阅读笔记中的证据片段：** 传统事实核查数据常直接提供人工justification，或允许搜索到声明发布后的事实核查文章；分类器会读到别人已经综合好的结论。本文要求系统只能使用声明发生时已经存在、且不来自已知fact-checking站点的原始网页，模拟新声明刚出现时的核查。
- **来源：** [精读笔记](notes/important/I046_Complex_Claim_Verification_with_Evidence_Retrieved_in_the_Wild.md)；[论文页面](https://arxiv.org/abs/2305.11859)

## I047 · FactKG: Fact Verification via Reasoning on Knowledge Graphs

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 E；次类 T
- **研究定位：** FACTKG从WebNLG 2020的文本—RDF对和DBpedia 2015构造108,674条英文claim，标签SUPPORTED/REFUTED，覆盖One-hop、Conjunction、Existence、Multi-hop、Negation。其优势是可把证据表示成明确关系路径，适合研究结构化事实核验和图推理。
- **需核查的条件或限制：** 见原笔记；本卡未自动抽出限制段落。
- **阅读笔记中的证据片段：** FACTKG从WebNLG 2020的文本—RDF对和DBpedia 2015构造108,674条英文claim，标签SUPPORTED/REFUTED，覆盖One-hop、Conjunction、Existence、Multi-hop、Negation。其优势是可把证据表示成明确关系路径，适合研究结构化事实核验和图推理。
- **来源：** [精读笔记](notes/important/I047_FACTKG.md)；[论文页面](https://arxiv.org/abs/2305.06590)

## I048 · Fact-Checking Complex Claims with Program-Guided Reasoning

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 E；次类 J
- **研究定位：** ProgramFC把复杂claim变成受控程序，只有三个函数：
- **需核查的条件或限制：** 见原笔记；本卡未自动抽出限制段落。
- **阅读笔记中的证据片段：** ProgramFC把复杂claim变成受控程序，只有三个函数：
- **来源：** [精读笔记](notes/important/I048_ProgramFC.md)；[论文页面](https://arxiv.org/abs/2305.12744)

## I050 · GraphEval: A Knowledge-Graph Based LLM Hallucination Evaluation Framework

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 E；次类 J
- **研究定位：** GraphEval只评估closed-domain consistency：回答是否与给定context一致，不检查context本身是否真实，也不覆盖模型训练知识偏离或开放域事实。流程为：
- **需核查的条件或限制：** GraphEval只评估closed-domain consistency：回答是否与给定context一致，不检查context本身是否真实，也不覆盖模型训练知识偏离或开放域事实。流程为：
- **阅读笔记中的证据片段：** GraphEval只评估closed-domain consistency：回答是否与给定context一致，不检查context本身是否真实，也不覆盖模型训练知识偏离或开放域事实。流程为：
- **来源：** [精读笔记](notes/important/I050_GraphEval.md)；[论文页面](https://arxiv.org/abs/2407.10793)

## I051 · Hallucination Detection in LLMs with Topological Divergence on Attention Graphs

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 U
- **研究定位：** 目标是RAG/给定context下的回答级任一幻觉二分类，主要是忠实性而非开放域世界事实。白盒读取生成模型各层各头attention；闭源API不可直接用。每个头把attention wij转为伪距离1-wij，把prompt token集合P内部边距离置零，求把回答token集合R接到P上的最小生成森林权重和，并除以|R|。该量等于修改后0阶persistent homology条形码有限区间长度和，记作MTop-DivG(R,P)。较大值被解释为回答相对prompt更“新”，倾向幻觉。
- **需核查的条件或限制：** 1. 按source/article而非回答行划分，审计同一context跨train/probe/test泄漏；保存各split的source hash。 2. 保留全部自然输出（包括ROUGE中间区、N/A、三人不一致）重新评估AUROC/AUPRC和不同错误率，量化筛选收益。 3. 构造最小对立样本：只替换事实实体/数词，保持token长度、复制率和prompt结构；另用正确同义改写检验新颖性与事实性的解耦。 4. 分层回归控制回答长度、首token attention、词面重叠、拒答、任务和模型，再测MTop-Div增量。 5. 对头选择采用nested validation、跨domain预选/冻结，并绘制100例选择下的多seed头稳定性与真实迁移损失。 6. 比较有向/无向构图、三角对称化、边定义、纯MST和token copying分…
- **阅读笔记中的证据片段：** 目标是RAG/给定context下的回答级任一幻觉二分类，主要是忠实性而非开放域世界事实。白盒读取生成模型各层各头attention；闭源API不可直接用。每个头把attention wij转为伪距离1-wij，把prompt token集合P内部边距离置零，求把回答token集合R接到P上的最小生成森林权重和，并除以|R|。该量等于修改后0阶persistent homology条形码有限区间长度和，记作MTop-DivG(R,P)。较大值被解释为回答相对prompt更“新”，倾向幻觉。
- **来源：** [精读笔记](notes/important/I051_TOHA.md)；[论文页面](https://aclanthology.org/2026.acl-long.704/)

## I052 · INTRYGUE: Induction-Aware Entropy Gating for Reliable RAG Uncertainty Estimation

- **层级／研究角色：** important／评价方法
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 U；次类 E
- **研究定位：** 评价对象是给定检索文本的回答级任一不忠实内容，不是客观世界真值；假文档被忠实复述会得到低风险，作者在限制与风险部分明确承认（PDF10、16）。白盒要求获得生成时注意力和每token logits。
- **需核查的条件或限制：** config/evaluation/default.yaml：seed42、k5、valsize.5；外层KFold3用StratifiedGroupKFold按context分测试集（若传groups），更好地控制同context跨测试泄漏；但训练/验证由普通traintestsplit(... stratify=y)分开，不按context分组，验证的头数选择可看到同一context的训练行。必须核实运行入口确实传groups，不能仅凭类存在断言所有表都分组。
- **阅读笔记中的证据片段：** 评价对象是给定检索文本的回答级任一不忠实内容，不是客观世界真值；假文档被忠实复述会得到低风险，作者在限制与风险部分明确承认（PDF10、16）。白盒要求获得生成时注意力和每token logits。
- **来源：** [精读笔记](notes/important/I052_INTRYGUE.md)；[论文页面](https://arxiv.org/abs/2603.21607)

## I053 · InteGround: On the Evaluation of Verification and Retrieval Planning in Integrative Grounding

- **层级／研究角色：** important／基准/数据
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 —；次类 E;J
- **研究定位：** 给命题ϕ、候选知识库K，找证据子集Σ使Σ蕴含ϕ或¬ϕ；可回答“蕴含/矛盾/都不能证明”。本文实际核验实验折成Entailment与Not entailment两类，负类包含证据缺失，不等同现实命题为假（PDF2–5）。规划实验取K内候选排名，主要看Recall@5，即前五证据覆盖gold条目的比例；这不同于是否找齐所有必要证据，更不同于最终推理正确率。附录直接检索另给F1@5和Acc@5（PDF12–13），不能互换。
- **需核查的条件或限制：** 见原笔记；本卡未自动抽出限制段落。
- **阅读笔记中的证据片段：** 给命题ϕ、候选知识库K，找证据子集Σ使Σ蕴含ϕ或¬ϕ；可回答“蕴含/矛盾/都不能证明”。本文实际核验实验折成Entailment与Not entailment两类，负类包含证据缺失，不等同现实命题为假（PDF2–5）。规划实验取K内候选排名，主要看Recall@5，即前五证据覆盖gold条目的比例；这不同于是否找齐所有必要证据，更不同于最终推理正确率。附录直接检索另给F1@5和Acc@5（PDF12–13），不能互换。
- **来源：** [精读笔记](notes/important/I053_InteGround.md)；[论文页面](https://aclanthology.org/2025.findings-emnlp.732/)

## I054 · Q2: Evaluating Factual Consistency in Knowledge-Grounded Dialogues via Question Generation and Question Answering

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 E；次类 T
- **研究定位：** 知识对话QA/NLI核验
- **需核查的条件或限制：** 闲聊/人格参照、空题回退、精选标注与模拟系统排序。
- **阅读笔记中的证据片段：** 知识对话回复会混合来源事实、对历史的指代、个人偏好、寒暄。把整个回复逐字与知识比对，会错误惩罚合理闲聊。Q²从回复提问题、在指定知识中回答，再用NLI比较答案，试图避开个人内容并适应同义表达。
- **来源：** [精读笔记](notes/important/I054_Q_Squared.md)；[论文页面](https://aclanthology.org/2021.emnlp-main.619/)

## I055 · QuCo-RAG: Quantifying Uncertainty from the Pre-training Corpus for Dynamic Retrieval-Augmented Generation

- **层级／研究角色：** important／评价方法
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 U；次类 E
- **研究定位：** 本文是何时检索的动态RAG，终点主要为QA最终答案EM/F1，附录扩展至ASQA和PubMedQA；并非直接测某条生成事实的真实幻觉概率。预生成先抽问题实体，调用Infini-gram查预训练语料中的精确词面频率，平均频率<1000就用原问题检索。生成中对每句用GPT-4o-mini合成4万例训练的Qwen2.5-0.5B抽三元组，查head/tail实体在1000-token窗口内共现次数；任一对为零便用head+relation检索、再生成该句。
- **需核查的条件或限制：** 见原笔记；本卡未自动抽出限制段落。
- **阅读笔记中的证据片段：** 本文是何时检索的动态RAG，终点主要为QA最终答案EM/F1，附录扩展至ASQA和PubMedQA；并非直接测某条生成事实的真实幻觉概率。预生成先抽问题实体，调用Infini-gram查预训练语料中的精确词面频率，平均频率<1000就用原问题检索。生成中对每句用GPT-4o-mini合成4万例训练的Qwen2.5-0.5B抽三元组，查head/tail实体在1000-token窗口内共现次数；任一对为零便用head+relation检索、再生成该句。
- **来源：** [精读笔记](notes/important/I055_QuCo_RAG.md)；[论文页面](https://arxiv.org/abs/2512.19134)

## I057 · RAGAs: Automated Evaluation of Retrieval Augmented Generation

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 E；次类 J
- **研究定位：** RAG多维自动评价
- **需核查的条件或限制：** 来源忠实性、反向问题相关、上下文集中度、分解覆盖和历史版本/格式边界。
- **阅读笔记中的证据片段：** RAG包含检索和生成，错误可能来自资料不相关、上下文冗余、生成不忠实或答非所问。论文把三项拆开：faithfulness衡量回答是否受已给上下文支持；answer relevance衡量是否回答原问题；context relevance衡量上下文是否集中于答题所需信息。
- **来源：** [精读笔记](notes/important/I057_RAGAs.md)；[论文页面](https://aclanthology.org/2024.eacl-demo.16/)

## I058 · Retrieving Supporting Evidence for LLMs Generated Answers

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 E；次类 J
- **研究定位：** GPT-3.5-turbo以温度0先回答问题。用“问题+所生成答案”作为检索query，从MS MARCO V1约800万篇passage中取排名第一条；比较BM25（文中报告参数k1=0.82、b=0.68）与SPLADE→ANCE→MonoT5→DuoT5神经检索栈；第三种在神经检索top1后让同一LLM作reader抽答案。最后将问题、原答案、检索内容/reader答案交同一LLM，判Yes（相符）、No（矛盾）、Not Related（不相关）。实验为MS MARCO V1 small development的6,980个问题；不是独立真实世界事实库抽样，也不是对长文每条命题逐项评分。论文没有报告可复现的逐题输出、完整人工标注规程、重复随机种子或多个生成器的比较。
- **需核查的条件或限制：** Siqing Huo、Negar Arabzadeh、Charles L. A. Clarke，Retrieving Supporting Evidence for LLMs Generated Answers，REML 2023，本地 arXiv:2306.13781v1（2023-06-23），PDF 7 页。逐页阅读正文、表1–5、图1–8、结论与限制；下列页码均指本地PDF。本文研究生成短答案后从语料找证据，再由同一LLM判断证据与原答案关系。最值得追问的是：检索器用原答案扩展query，能否可靠找到反驳证据？三类输出是否真的对应“幻觉/非幻觉”的世界真值？
- **阅读笔记中的证据片段：** GPT-3.5-turbo以温度0先回答问题。用“问题+所生成答案”作为检索query，从MS MARCO V1约800万篇passage中取排名第一条；比较BM25（文中报告参数k1=0.82、b=0.68）与SPLADE→ANCE→MonoT5→DuoT5神经检索栈；第三种在神经检索top1后让同一LLM作reader抽答案。最后将问题、原答案、检索内容/reader答案交同一LLM，判Yes（相符）、No（矛盾）、Not Related（不相关）。实验为MS MARCO V1 small development的6,980个问题；不是独立真实世界事实库抽样，也不是对长文每条命题逐项评分。论文没有报告可复现的逐题输出、完整人工标注规程、重复随机种子或多个生成器的比较。
- **来源：** [精读笔记](notes/important/I058_Retrieving_Supporting_Evidence_for_LLMs_Generated_Answers.md)；[论文页面](https://arxiv.org/abs/2306.13781)

## I059 · Self-Checker: Plug-and-Play Modules for Fact-Checking with Large Language Models

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 E；次类 J
- **研究定位：** 框架以policy agent依次调用claim processor、query generator、Bing/Wikipedia检索、evidence seeker、verdict counselor。BingCheck的四类为supported、partially supported、refuted、not supported。操作上，任何证据矛盾即refuted；无矛盾且至少一条支持则supported；只证实一部分则partially；无支持/反驳才not supported（PDF5）。这仍是给定检索证据的支持关系，没有外部独立世界真值保证。尤其“至少一条支持”忽略其他未取到的矛盾证据；实际做法是每claim Bing top3，然后抽证据句。
- **需核查的条件或限制：** 固定版本ZIP约121.9 MB、462个保留成员；bingcheck/有401个JSON，而论文记396条，需要按样本ID核对额外文件性质与实验筛选。README把getdataandresources.sh误写成getdata.sh，预处理脚本列表亦与实际清单不一致；“Evaluate Results”三项均写evaluatefever.py，但仓库分别有BingCheck/WiCE脚本，按README照跑会错。experimentbingcheck.py当前源码TEMPERATURE=0、Azuretext003，论文PDF7称temperature .2，版本/设置不符；需锁定论文实际执行提交与配置，不能把当前代码输出视为论文原实验。
- **阅读笔记中的证据片段：** 框架以policy agent依次调用claim processor、query generator、Bing/Wikipedia检索、evidence seeker、verdict counselor。BingCheck的四类为supported、partially supported、refuted、not supported。操作上，任何证据矛盾即refuted；无矛盾且至少一条支持则supported；只证实一部分则partially；无支持/反驳才not supported（PDF5）。这仍是给定检索证据的支持关系，没有外部独立世界真值保证。尤其“至少一条支持”忽略其他未取到的矛盾证据；实际做法是每claim Bing top3，然后抽证据句。
- **来源：** [精读笔记](notes/important/I059_Self_Checker.md)；[论文页面](https://arxiv.org/abs/2305.14623)

## I060 · A Probabilistic Framework for LLM Hallucination Detection via Belief Tree Propagation

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 E
- **研究定位：** 目标是给LLM输出的一条句子/segment预测其现实事实真伪，不是判断其与指定文档的忠实性。根节点原句，子节点由三类方式生成：复合句拆解；支持/反驳前提；把关键数值、姓名等改写为模型认为更正的说法。前两类节点的True/False分数由同一LLM在True or False? statement下取两词logit归一；改写子节点一律设置信心1，不再询问其正确性（PDF4）。新节点与父节点的蕴含/反向蕴含/等价/矛盾由独立NLI判定，(neutral,neutral)丢弃，任一方向contradict归矛盾；错误边会把概率传播到错误结论，论文未给逐边人工准确率。
- **需核查的条件或限制：** 1. 在独立标注校准集和新域/新模型/新时间上测发射分布漂移，做ECE、Brier与幻觉召回的校准曲线；与无标签、少标签基线对照。 2. 人工判树边和拆解claim的蕴含/矛盾/保真，按关系、范围、否定、时间分箱；注入已知边噪声看根后验鲁棒性。 3. 测重复候选、同模型相关错误与改写信心强制1的影响；对同一问题互斥答案构造约束，不允许多个互斥“纠错”同时真。 4. 阈值仅在held-out校准集选择，再在锁定test报告F1/accuracy和AUROC/AUC-PR；每基准公开样本数、阳性率和paired bootstrap区间。 5. 比较问答自检、SelfCheckGPT与BTProp的相同调用/token/延迟预算，避免多分支方法的收益来自更多模型调用。 6. 检查Llama“无外证即False”对最新事实、罕见实体及真正不可判的偏误；增设u…
- **阅读笔记中的证据片段：** 目标是给LLM输出的一条句子/segment预测其现实事实真伪，不是判断其与指定文档的忠实性。根节点原句，子节点由三类方式生成：复合句拆解；支持/反驳前提；把关键数值、姓名等改写为模型认为更正的说法。前两类节点的True/False分数由同一LLM在True or False? statement下取两词logit归一；改写子节点一律设置信心1，不再询问其正确性（PDF4）。新节点与父节点的蕴含/反向蕴含/等价/矛盾由独立NLI判定，(neutral,neutral)丢弃，任一方向contradict归矛盾；错误边会把概率传播到错误结论，论文未给逐边人工准确率。
- **来源：** [精读笔记](notes/important/I060_BTProp.md)；[论文页面](https://aclanthology.org/2025.naacl-long.158/)

## I061 · A Stitch in Time Saves Nine: Detecting and Mitigating Hallucinations of LLMs by Validating Low-Confidence Generation

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 E
- **研究定位：** 概率筛查驱动的逐句外部核验/修复
- **需核查的条件或限制：** 误改成本、传播因果、预算及错误前提条件评价。
- **阅读笔记中的证据片段：** 方法面向文章生成、少量多跳QA和错误前提QA。在文章任务中，不是先写完长文再检查，而是每生成一句就抽关键概念，用模型概率筛出低置信概念，生成核验问题，检索外部证据并判断；发现错误则修复该句，将修复文本作为后续生成历史。
- **来源：** [精读笔记](notes/important/I061_Stitch_in_Time.md)；[论文页面](https://arxiv.org/abs/2307.03987)

## I062 · Asking and Answering Questions to Evaluate the Factual Consistency of Summaries

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 E；次类 无
- **研究定位：** QA双侧答案一致性
- **需核查的条件或限制：** 参考增强证据、题目预算、部件迁移、统计及源码接口可靠性。
- **阅读笔记中的证据片段：** 给定来源X和生成摘要Y，从p(Q|Y)抽问题，比较文章与摘要的答案分布p(A|Q,X)、p(A|Q,Y)，再对问题取期望。实际实现用最可能答案的token-F1，平均K题；并未真的比较完整概率分布。问题由生成内容提出，主要测输出信息支持率，不是输入重要事实被保留的recall。
- **来源：** [精读笔记](notes/important/I062_QAGS.md)；[论文页面](https://aclanthology.org/2020.acl-main.450/)

## I063 · Attention Satisfies: A Constraint-Satisfaction Lens on Factual Errors of Language Models

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 无
- **研究定位：** 作者把查询写成约束集合(Ck,Vk)：Ck是提示中的实体token，Vk是对输出的验证器；任一约束不满足就算“事实错误”。这是查询约束满足的任务定义，既包括知识事实，也包括纯字符串首末字母约束；不能直接推广到自由长答的世界事实性。论文在实验中事先知道约束token（PDF3脚注、9结论），这在开放问题需另行抽取。约束合取，未覆盖OR、否定、时点等复杂逻辑。
- **需核查的条件或限制：** 1. 在保持实体、提示模板、token长度不变的最小对上干预某约束的attention，比较事实准确变化；否则只称预测相关。 2. 与实体流行度、位置、输出概率、隐藏状态等强基线同预算比较，分层报告真正增量AUROC和风险覆盖。 3. 新实体、新关系、新模型、自由长答与多轮上下文作外推，约束token自动抽取纳入端到端误差。 4. 双约束预测用联合模型与简单乘积比较，特别测相关关系与部分满足的概率校准。 5. 对精确匹配及GPT-3.5列表判断抽样人工审计，分开模型错与标签器错，并冻结Wikidata快照。 6. 早停按实际请求报告延迟、错误拦截召回、正确答案误停、拒答覆盖和后续检索成本。
- **阅读笔记中的证据片段：** 作者把查询写成约束集合(Ck,Vk)：Ck是提示中的实体token，Vk是对输出的验证器；任一约束不满足就算“事实错误”。这是查询约束满足的任务定义，既包括知识事实，也包括纯字符串首末字母约束；不能直接推广到自由长答的世界事实性。论文在实验中事先知道约束token（PDF3脚注、9结论），这在开放问题需另行抽取。约束合取，未覆盖OR、否定、时点等复杂逻辑。
- **来源：** [精读笔记](notes/important/I063_Attention_Satisfies.md)；[论文页面](https://arxiv.org/abs/2309.15098)

## I064 · Bold Claims or Self-Doubt? Factuality Hallucination Type Detection via Belief State

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 T
- **研究定位：** 作者让模型对同一问题采样10个自由答案，用SQuAD2.0微调DeBERTa-v3-large抽核心答案，统计最多重复的答案次数。freq=10定义confident，freq<5定义uncertain；5–9次的中间样本无类型标签、从训练/测试两端对照中排除。对检索裁判判错的输出，前者称Overconfident Hallucination（OH），后者称Unaware Hallucination（UH）。重复率是行为稳定性，依赖采样温度、提示和抽取器；它不能证明模型“相信”或“知道”某命题。稳定错误可来自训练数据流行谬误，也可来自解码固定偏差；不稳定正确答也存在。Unaware名称具有强心理学含义，实测只有答案分散。
- **需核查的条件或限制：** 见原笔记；本卡未自动抽出限制段落。
- **阅读笔记中的证据片段：** 作者让模型对同一问题采样10个自由答案，用SQuAD2.0微调DeBERTa-v3-large抽核心答案，统计最多重复的答案次数。freq=10定义confident，freq<5定义uncertain；5–9次的中间样本无类型标签、从训练/测试两端对照中排除。对检索裁判判错的输出，前者称Overconfident Hallucination（OH），后者称Unaware Hallucination（UH）。重复率是行为稳定性，依赖采样温度、提示和抽取器；它不能证明模型“相信”或“知道”某命题。稳定错误可来自训练数据流行谬误，也可来自解码固定偏差；不稳定正确答也存在。Unaware名称具有强心理学含义，实测只有答案分散。
- **来源：** [精读笔记](notes/important/I064_Bold_Claims_or_Self_Doubt.md)；[论文页面](https://aclanthology.org/2025.findings-emnlp.527/)

## I065 · ChatGPT as a Factual Inconsistency Evaluator for Text Summarization

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 J；次类 H
- **研究定位：** LLM裁判的早期摘要实验
- **需核查的条件或限制：** 提示/解析、A/B位置、域混合相关、解释错误与rubric漂移。
- **阅读笔记中的证据片段：** 作者针对指定来源的faithfulness/consistency，设计三种交互：给来源和摘要判yes/no；给来源句和一真一假候选选A/B；给摘要打1–10一致性分。三者分别是二分类、受控二选一排序、连续/序数质量评分，不可共享“accuracy”解释。
- **来源：** [精读笔记](notes/important/I065_ChatGPT_Factual_Inconsistency.md)；[论文页面](https://arxiv.org/abs/2303.15621)

## I066 · Contextualized Sequence Likelihood: Enhanced Confidence Scores for Natural Language Generation

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 E
- **研究定位：** 内部似然的上下文token加权
- **需核查的条件或限制：** attention头监督选择、裁判一致子集、采样基线敏感性及语义聚合实现。
- **阅读笔记中的证据片段：** 作者区分uncertainty与confidence：前者针对输入下的预测分布，后者还依赖具体生成答案。CSL为具体答案打可信排序分，核心问题是序列概率混合了正确性、措辞习惯、语法和非关键内容；不同问题对同一句话的关键token要求不同。
- **来源：** [精读笔记](notes/important/I066_Contextualized_Sequence_Likelihood.md)；[论文页面](https://arxiv.org/abs/2406.01806)

## I067 · DRIFT: Detecting Representational Inconsistencies for Factual Truthfulness

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 U
- **研究定位：** 闭卷QA，模型对每题生成一次答案；GPT-4o比较问题、标准答与生成答，提示还要求“不得加入额外不正确/冲突/多余信息”。因此一个答题正确但比参考多包含无关正确细节的答案也可能判错；同义答案的裁判错误没有双人抽检。DRIFT用目标模型某一中层的question token hidden states，经过池化MLP或4–8层的小Transformer，BCE监督训练“这次答案是否正确”。问题模式在答案产生前预测的是条件于问题和已训练模型的成功概率，可能学主题难度、实体热门度、问句格式；不等于读取某次尚未生成的具体答案的“真实幻觉”。答案模式把输出token也输入探针，评价更强但已晚于生成。
- **需核查的条件或限制：** 见原笔记；本卡未自动抽出限制段落。
- **阅读笔记中的证据片段：** 闭卷QA，模型对每题生成一次答案；GPT-4o比较问题、标准答与生成答，提示还要求“不得加入额外不正确/冲突/多余信息”。因此一个答题正确但比参考多包含无关正确细节的答案也可能判错；同义答案的裁判错误没有双人抽检。DRIFT用目标模型某一中层的question token hidden states，经过池化MLP或4–8层的小Transformer，BCE监督训练“这次答案是否正确”。问题模式在答案产生前预测的是条件于问题和已训练模型的成功概率，可能学主题难度、实体热门度、问句格式；不等于读取某次尚未生成的具体答案的“真实幻觉”。答案模式把输出token也输入探针，评价更强但已晚于生成。
- **来源：** [精读笔记](notes/important/I067_DRIFT.md)；[论文页面](https://arxiv.org/abs/2601.14210)

## I068 · Distinguishing Ignorance from Error in LLM Hallucinations

- **层级／研究角色：** important／领域实证/现象分析
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 T
- **研究定位：** 短答闭卷QA：对每题3-shot提示做1次greedy+5次温度.5采样，最多5 token，按gold答案精确匹配。六次从未答对→HK−（作者称缺知识）；六次都答对→“高知识”，再换提示生成一次greedy：这次答错→HK+，答对→factually correct。中间混合答对的约5%被排除。HK−是“此特定采样协议下未出现gold”，不能证明参数里绝无相关知识；HK+是“曾六次答对却在另提示答错”，不证明模型具有稳定可调用的内在信念。论文通过配置敏感性比较（1000题）报92.2–93.6%类别一致，但不同代理相互一致不等于接近真实知识边界；zero-shot最低仅约80%，仍有显著协议效应。
- **需核查的条件或限制：** 见原笔记；本卡未自动抽出限制段落。
- **阅读笔记中的证据片段：** 短答闭卷QA：对每题3-shot提示做1次greedy+5次温度.5采样，最多5 token，按gold答案精确匹配。六次从未答对→HK−（作者称缺知识）；六次都答对→“高知识”，再换提示生成一次greedy：这次答错→HK+，答对→factually correct。中间混合答对的约5%被排除。HK−是“此特定采样协议下未出现gold”，不能证明参数里绝无相关知识；HK+是“曾六次答对却在另提示答错”，不证明模型具有稳定可调用的内在信念。论文通过配置敏感性比较（1000题）报92.2–93.6%类别一致，但不同代理相互一致不等于接近真实知识边界；zero-shot最低仅约80%，仍有显著协议效应。
- **来源：** [精读笔记](notes/important/I068_Distinguishing_Ignorance_from_Error.md)；[论文页面](https://arxiv.org/abs/2410.22071)

## I069 · Do Androids Know They're Only Dreaming of Electric Sheep?

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 U
- **研究定位：** 任务是给定上下文的忠实性：只要输出内容不被源材料蕴含（无论现实真假）即视为幻觉；直接矛盾叫intrinsic，无支持也无矛盾叫extrinsic。论文特别举“Nubian goat是英国山羊品种”即使现实真、文章未说仍算extrinsic（PDF2）。这与I068/DRIFT的闭卷答案正确性不同，综述应严格分轴。
- **需核查的条件或限制：** 见原笔记；本卡未自动抽出限制段落。
- **阅读笔记中的证据片段：** 任务是给定上下文的忠实性：只要输出内容不被源材料蕴含（无论现实真假）即视为幻觉；直接矛盾叫intrinsic，无支持也无矛盾叫extrinsic。论文特别举“Nubian goat是英国山羊品种”即使现实真、文章未说仍算extrinsic（PDF2）。这与I068/DRIFT的闭卷答案正确性不同，综述应严格分轴。
- **来源：** [精读笔记](notes/important/I069_Do_Androids_Know.md)；[论文页面](https://arxiv.org/abs/2312.17249)

## I070 · Do Language Models Know When They're Hallucinating References?

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 T
- **研究定位：** 作者把计算机科学的书籍/文章标题当作开放域幻觉的“模型生物”。其幻觉定义是生成文字缺少训练资料支持，即groundedness，与世界事实正确性不同。一个网上存在的错误说法可能有训练支持但不真实；一个真实标题可能从未进入某模型训练集。本文没有训练集访问权，以Bing引号搜索是否返回结果代理grounding，故严格说是“标题可检索性”的检测研究，不能直接等同事实核查或训练集溯源。作者的机制假说：模型若真熟悉某书目，应多次给出相近作者；编造书目的作者列表易不一致。稳定性只是统计线索：著名相似书名的作者可被稳定误套，冷门真书目的作者也可能记不住。
- **需核查的条件或限制：** H常是两种真标题拼接或看似合理的“某领域综述”。DQ可对合理虚构题名答真；IQ也会把邻近真实书的作者稳定套到虚构标题。例如Introduction to Operations Research and Decision Making借Introduction to Operations Research作者，附录Enterprise Modeling: Tackling Business Challenges with the 4EM Approach IQ=1而H。反向，附录ChatGPT真实Advanced Logic Synthesis等IQ=0，说明作者记忆缺失不能直接证明题名虚构。附录4×30的人工浏览用于解释案例，非经盲法随机跨模型的完整误差标注。
- **阅读笔记中的证据片段：** 作者把计算机科学的书籍/文章标题当作开放域幻觉的“模型生物”。其幻觉定义是生成文字缺少训练资料支持，即groundedness，与世界事实正确性不同。一个网上存在的错误说法可能有训练支持但不真实；一个真实标题可能从未进入某模型训练集。本文没有训练集访问权，以Bing引号搜索是否返回结果代理grounding，故严格说是“标题可检索性”的检测研究，不能直接等同事实核查或训练集溯源。作者的机制假说：模型若真熟悉某书目，应多次给出相近作者；编造书目的作者列表易不一致。稳定性只是统计线索：著名相似书名的作者可被稳定误套，冷门真书目的作者也可能记不住。
- **来源：** [精读笔记](notes/important/I070_Hallucinating_References.md)；[论文页面](https://arxiv.org/abs/2305.18248)

## I071 · Do Not Design, Learn: A Trainable Scoring Function for Uncertainty Estimation in Generative LLMs

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 T
- **研究定位：** 问题不是检索证据核查，而是为封闭式QA/算术题模型的回答正确性排序提供不确定性分数。传统sequence probability是逐token条件概率连乘，长回答自然偏低；LNS取几何平均，MARS/TokenSAR对重要词赋权。但词义交互、实体类型概率偏置及跨语言工具可用性使固定权重不充分。论文的日期/人名例子说明同等答对率可有不同token概率，但那是描述性证据，未证明全部增益来自消除该偏置。
- **需核查的条件或限制：** TriviaQA Llama2-7B Confidence只文本.750、只概率.721、两者.851，表明两种输入互补；但“只概率”是两层MLP，架构也变，消融并不纯粹隔离信息。去问题.832 vs全输入.851；简单句向量+概率MLP仅.666。附录以Llama3-8B/70B教师生成噪声标签训LARS得.809/.837 vs直接问教师.635/.746，但所谓“without labeled data”其实仍使用教师伪标签与训练成本。序列插入概率词对长答案不适用；难解释哪些实体/词交互使正确性提升。所有主要评价限于简短答案与算术，不能直接扩展到长文多事实、给定来源忠实性、引用真实性。论文没有给ECE、Brier、可靠性图或真实风险覆盖点，因此“calibrated”只能按排序表现理解，不能证明数值概率已校准。未见多随机种子置信区间及人工判题抽…
- **阅读笔记中的证据片段：** 问题不是检索证据核查，而是为封闭式QA/算术题模型的回答正确性排序提供不确定性分数。传统sequence probability是逐token条件概率连乘，长回答自然偏低；LNS取几何平均，MARS/TokenSAR对重要词赋权。但词义交互、实体类型概率偏置及跨语言工具可用性使固定权重不充分。论文的日期/人名例子说明同等答对率可有不同token概率，但那是描述性证据，未证明全部增益来自消除该偏置。
- **来源：** [精读笔记](notes/important/I071_LARS.md)；[论文页面](https://arxiv.org/abs/2406.11278)

## I072 · Entity-level Factual Consistency of Abstractive Text Summarization

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 E；次类 无
- **研究定位：** 实体来源覆盖和训练过滤
- **需核查的条件或限制：** 宽松匹配、空实体、条件测试集、实体计划与关系盲区。
- **阅读笔记中的证据片段：** 作者区分来源未出现的实体名与来源实体之间关系错误，本篇只解决前者，关系留未来工作。源外实体并不必然世界虚假；同名实体出现在来源也不保证语境和关系正确。与I015 EntFA相比，这里没有用外部证据区分来源外真实实体，不能用实体重合指标替代其世界真实性标签。
- **来源：** [精读笔记](notes/important/I072_Entity_Level_Consistency.md)；[论文页面](https://aclanthology.org/2021.eacl-main.235/)

## I073 · Evaluating the Factual Consistency of Abstractive Text Summarization

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 E
- **研究定位：** 合成监督来源一致性
- **需核查的条件或限制：** 版本差异、micro-F1与BAcc、span解释、人机协作和抽象性迁移。
- **阅读笔记中的证据片段：** 事实一致性指摘要只包含来源文章可蕴含的陈述；原文明确区别开放世界fact checking，来源本身可能不真实。因此这属于来源忠实性。模型输入为文档+单个摘要句，输出一致/不一致；不是逐实体真值、开放域检索，也不评价摘要遗漏了多少重要信息。
- **来源：** [精读笔记](notes/important/I073_FactCC.md)；[论文页面](https://arxiv.org/abs/1910.12840)

## I074 · Fast and Accurate Factual Inconsistency Detection Over Long Documents

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 E
- **研究定位：** 长来源分块NLI
- **需核查的条件或限制：** 贪心证据检索、校准定义/端点、缓存分数和公开数据版本核查。
- **阅读笔记中的证据片段：** 本文将幻觉定义为相对指定来源的不一致，记来源事实FD、生成事实FG，希望FG包含于FD。这个形式概括支持关系，不表示算法真正抽取并穷尽两个事实集合，也不检验来源现实真伪。reference-free仍需要完整来源，并非无证据或零资源。
- **来源：** [精读笔记](notes/important/I074_SCALE_Long_Documents.md)；[论文页面](https://arxiv.org/abs/2310.13189)

## I075 · Generating with Confidence: Uncertainty Quantification for Black-box Large Language Models

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 无
- **研究定位：** 黑盒采样语义图及答案级置信
- **需核查的条件或限制：** 输入不确定性、谱/度数/偏心度、风险覆盖、校准与方向性源码差异。
- **阅读笔记中的证据片段：** 论文首先区分 U(x) 与 C(x,s)。前者描述给定输入x后输出分布的分散程度；后者描述某条具体回答s的可信程度。一个问题下同时出现正确与错误答案，U对这些答案相同，C可以不同。这是本篇相对于只给问题计算语义熵的重要贡献。
- **来源：** [精读笔记](notes/important/I075_Generating_with_Confidence.md)；[论文页面](https://arxiv.org/abs/2305.19187)

## I076 · Hallucination Detection in LLMs Using Spectral Features of Attention Maps

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 U
- **研究定位：** 单生成注意力谱的白盒监督探针
- **需核查的条件或限制：** 因果三角矩阵、非标准拉普拉斯解释、混合正确性标签/拒答过滤、提示与长度、跨集迁移和选参协议。
- **阅读笔记中的证据片段：** LapEigvals从一次回答生成过程中的全部层、全部头注意力取特征，以带外部正确性标签的数据训练逻辑回归，预测该回答是否错误。单位是问答实例/整条回答，非逐个事实、token或来源片段的错误定位。所谓hallucination在实验中主要由参考答案正确性代理，GSM8K为最终数字答案匹配；推理过程正确与否、非关键附加事实错误、上下文忠实性均不由同一标签充分覆盖。
- **来源：** [精读笔记](notes/important/I076_LapEigvals.md)；[论文页面](https://arxiv.org/abs/2502.17598)

## I077 · How Language Model Hallucinations Can Snowball

- **层级／研究角色：** important／领域实证/现象分析
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 U
- **研究定位：** 错误承诺与隔离验证的行为不一致
- **需核查的条件或限制：** 单类压力测试、CoT总风险/条件风险、图与整数程序真值、宏微聚合及跨论文输入沿用。
- **阅读笔记中的证据片段：** 论文观察到模型先对复杂Yes/No问题做错误承诺，再编造支持理由；把该理由中的局部主张拆出、放入全新会话询问时，同一模型反而常能正确否认。作者称为hallucination snowballing，即错误承诺后出现模型在另一提示下能识别的后续错误。
- **来源：** [精读笔记](notes/important/I077_Hallucination_Snowballing.md)；[论文页面](https://arxiv.org/abs/2305.13534)

## I078 · ICRProbe: Tracking Hidden State Dynamics for Reliable Hallucination Detection in LLMs

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 U
- **研究定位：** 残差更新—注意力投影散度的跨层监督探针
- **需核查的条件或限制：** 机制可识别性、公式/示例对齐、探索性方向选择、均值曲线稳定性、跨域失败和因果token位置控制。
- **阅读笔记中的证据片段：** 方法不直接把某层高维隐藏向量送入探针，而计算各层更新方向与注意力分布的差异，每层得到一个数，组成长度L的特征，训练小MLP预测回答正确性。需要层间hidden states和attention，属于白盒监督探针；reference-free指推断时不需外部参照，不代表监督标签没有外部事实依据。
- **来源：** [精读笔记](notes/important/I078_ICR_Probe.md)；[论文页面](https://aclanthology.org/2025.acl-long.880/)

## I079 · INSIDE: LLMs' Internal States Retain the Power of Hallucination Detection

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 T
- **研究定位：** 白盒多采样内部表示及log-det谱评分
- **需核查的条件或限制：** 测试时激活裁剪、Gram/高斯熵条件、代理标签/阈值及稳定错边界。
- **阅读笔记中的证据片段：** INSIDE希望利用解码前的隐藏表示估计多次生成的语义分散，避免仅从token概率或解码文本重建意义。它提出EigenScore，并在生成阶段裁剪倒数第二层的极端激活，以减少过度一致的错误采样。
- **来源：** [精读笔记](notes/important/I079_INSIDE.md)；[论文页面](https://arxiv.org/abs/2402.03744)

## I080 · Joint Evaluation of Answer and Reasoning Consistency for Hallucination Detection in Large Reasoning Models

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 T
- **研究定位：** 推理/答案联合采样一致性
- **需核查的条件或限制：** 忠实压缩、辅助模型白盒访问、最终答案金标与过程真值区别、熵代理与尺度、过滤覆盖/长度混杂及LFS资源对齐。
- **阅读笔记中的证据片段：** RACE认为只看答案采样一致性会漏掉不同错误推理殊途同归的情况，因此联合考察推理、答案及二者关系。主回答greedy，另采5条高温输出，针对主回答给一个连续风险分数。
- **来源：** [精读笔记](notes/important/I080_RACE.md)；[论文页面](https://arxiv.org/abs/2506.04832)

## I081 · Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 无
- **研究定位：** 自报置信及后校准
- **需核查的条件或限制：** 有限采样、语言概率映射、语义裁判、交叉拟合及选择性AUC口径。
- **阅读笔记中的证据片段：** 作者关注经人类反馈训练的模型：RLHF可能把概率集中到被偏好的回答，使条件概率不再反映经验正确率。论文提出不需要为置信表达专门微调，而用提示让模型输出“答案及正确概率”或“likely”等语言置信词，并比较多候选、分阶段、CoT及后校准。
- **来源：** [精读笔记](notes/important/I081_Just_Ask_for_Calibration.md)；[论文页面](https://arxiv.org/abs/2305.14975)

## I082 · Kernel Language Entropy: Fine-grained Uncertainty Quantification for LLMs from Semantic Similarities

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 T
- **研究定位：** 语义图核及von Neumann谱熵
- **需核查的条件或限制：** SE推广条件、默认/监督调参、模型子组与检验、AUARC口径、边权和裁判调用链。
- **阅读笔记中的证据片段：** 语义熵把生成文本分成意义等价类，同类内部合并，不同类之间一律视为分开。本篇认为这种处理过于粗：两条答案虽然不完全相互蕴含，也可能高度相关，例如一个答案较简略、另一个增加解释。KLE将回答间或簇间关系编码成核矩阵，再用von Neumann entropy衡量分散。
- **来源：** [精读笔记](notes/important/I082_Kernel_Language_Entropy.md)；[论文页面](https://arxiv.org/abs/2405.20003)

## I083 · Language Models (Mostly) Know What They Know

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 无
- **研究定位：** 候选自评与生成前成功率预测
- **需核查的条件或限制：** 可见选项校准、全模型监督、有限采样软标签/majority目标、域外校准、提示响应及模型特有自知。
- **阅读笔记中的证据片段：** P(True)给定问题Q和一个具体候选答案a，问“该答案是否正确”，读取True/False选项概率。它评价外部任务事实，候选可以来自自己或其他模型。因为模型没有可靠的token来源标志，行为上未必知道候选是不是自己先前写的；self-evaluation不应被解释为读取内省记忆。
- **来源：** [精读笔记](notes/important/I083_PTrue_PIK.md)；[论文页面](https://arxiv.org/abs/2207.05221)

## I084 · MARS: Meaning-Aware Response Scoring for Uncertainty Estimation in Generative LLMs

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 无
- **研究定位：** BEM伪标签蒸馏的短语重要性加权
- **需核查的条件或限制：** 概率归一、权重操作顺序、数据身份和专门领域协议。
- **阅读笔记中的证据片段：** 长度归一似然将每个token视为等重要，但一个回答中只有部分词直接回答问题。MARS以问题为条件识别重要短语，提升这些词的概率在最终分数中的权重，并与普通长度归一分数各混合一半。它是替换既有概率型UE方法内部评分的模块，不是独立外部证据核验器。
- **来源：** [精读笔记](notes/important/I084_MARS.md)；[论文页面](https://aclanthology.org/2024.acl-long.419/)

## I085 · On Hallucination and Predictive Uncertainty in Conditional Language Generation

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 E
- **研究定位：** 条件生成token不确定性与集成分解
- **需核查的条件或限制：** UABS干预、对象/动作/表格参照及事实性—信息性权衡。
- **阅读笔记中的证据片段：** 幻觉定义为生成内容不被输入支持；输入是图像或结构化表格。它测来源忠实性，不是相对于整个现实世界的事实真假。图像对象可能现实存在但不在图中，仍属这里的幻觉；表格外真实但没有支持的内容也不能无条件视为忠实。
- **来源：** [精读笔记](notes/important/I085_Hallucination_Predictive_Uncertainty.md)；[论文页面](https://aclanthology.org/2021.eacl-main.236/)

## I086 · QAFactEval: Improved QA-Based Factual Consistency Evaluation for Summarization

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 E；次类 T
- **研究定位：** QA部件优化和可答性
- **需核查的条件或限制：** 监督语义匹配、QA/NLI融合、修改版基准及相关性层级。
- **阅读笔记中的证据片段：** 既有论文因基线、输入粒度和数据不同给出相反优劣结论。本篇把QA事实评估拆为答案选择、问题生成、问答、答案匹配，加上摘要回环过滤与来源不可答惩罚，逐部件比较，试图给QA路线更充分调优。
- **来源：** [精读笔记](notes/important/I086_QAFactEval.md)；[论文页面](https://arxiv.org/abs/2112.08542)

## I087 · Quantifying Uncertainty in Answers from any Language Model and Enhancing their Trustworthiness

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 J
- **研究定位：** 采样一致性与离散反思联合置信
- **需核查的条件或限制：** 答案重选、评审置信、人工分流及删除评价样本的选择偏差。
- **阅读笔记中的证据片段：** BSDetector为给定问题x及具体答案y输出confidence C(x,y)，不必改变最初生成答案；另可用它从多候选中挑选答案，或评估“裁判给出的评审意见是否可信”。这三种应用的输入/金标不同，不能将一个AUROC直接当另外两项提升的证据。
- **来源：** [精读笔记](notes/important/I087_BSDetector.md)；[论文页面](https://aclanthology.org/2024.acl-long.283/)

## I088 · SAC3: Reliable Hallucination Detection in Black-Box Language Models via Semantic-aware Cross-check Consistency

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 J
- **研究定位：** 黑盒跨问题/跨模型一致性
- **需核查的条件或限制：** 语义漂移、验证者相关错误、单类检出率和采样成本。
- **阅读笔记中的证据片段：** 自采样一致性可与正确性相关，但同一模型可能稳定犯错，正确原回答也可能被高温错误样本反对。论文提出question-level/model-level两种失败来源，用问题改写与额外模型增加交叉检查。
- **来源：** [精读笔记](notes/important/I088_SAC3.md)；[论文页面](https://arxiv.org/abs/2311.01740)

## I090 · Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 U
- **研究定位：** 内部状态弱监督探针与采样教师压缩
- **需核查的条件或限制：** 在线/离线成本、teacher fidelity/事实检测双目标、跨任务协议和模型选择监督。
- **阅读笔记中的证据片段：** 语义熵需要对同一问题生成约10个回答，再判定意义等价类。SEP在训练时承担这些成本，以问题和单次中心回答的隐藏状态预测“高/低语义熵”；部署时只用一次回答及线性分类器。
- **来源：** [精读笔记](notes/important/I090_Semantic_Entropy_Probes.md)；[论文页面](https://arxiv.org/abs/2406.15927)

## I091 · Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 无
- **研究定位：** 含义空间不确定性
- **需核查的条件或限制：** 概率估计、采样/聚类、QA金标、排名/校准区别及论文与旧源码差异。
- **阅读笔记中的证据片段：** 问题是：自由生成中，同一意思可能有许多表述，如何估计模型对答案“含义”的不确定性？普通序列熵会把表达方式的多样性也当成不确定性。“Paris”“It’s Paris”不应像“Paris”“Rome”那样被视为不同答案意义。
- **来源：** [精读笔记](notes/important/I091_Semantic_Uncertainty.md)；[论文页面](https://arxiv.org/abs/2302.09664)

## I092 · SummaC: Re-Visiting NLI-based Models for Inconsistency Detection in Summarization

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 E
- **研究定位：** NLI输入粒度与直方图聚合
- **需核查的条件或限制：** 多数据集元评估、标签标准化、目标阈值与文章共享。
- **阅读笔记中的证据片段：** 标准NLI训练主要是句对，直接把完整长文章和整个摘要放进去，会遭遇长度、稀释、跨句整合等分布差异。SummaC把来源切成M块、摘要切成N块，计算全部M×N句对的entailment/contradiction/neutral概率，再聚合判断摘要来源一致性。
- **来源：** [精读笔记](notes/important/I092_SummaC.md)；[论文页面](https://arxiv.org/abs/2111.09525)

## I093 · The Curious Case of Hallucinatory (Un)answerability: Finding Truths in the Hidden States of Over-Confident Large Language Models

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 U
- **研究定位：** 上下文可答性与拒答识别
- **需核查的条件或限制：** 提示/beam干预、早期隐藏状态探针、概念擦除、类比例及可答内容保留代价。
- **阅读笔记中的证据片段：** 研究对象是阅读理解：给定问题及段落，段落是否提供足够信息作答。模型可能凭预训练知识答出真实答案，但段落不支持时仍应拒答；反过来，段落包含正确答案也不保证模型生成正确。该概念不同于I094的世界真假、I090的输出语义分散及闭卷QA的正确性。
- **来源：** [精读笔记](notes/important/I093_Hallucinatory_Unanswerability.md)；[论文页面](https://aclanthology.org/2023.emnlp-main.220/)

## I094 · The Internal State of an LLM Knows When It's Lying

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 T；次类 U
- **研究定位：** 外部正确性监督的内部状态MLP探针
- **需核查的条件或限制：** 留主题泛化、合成真假数据、目标阈值校准、长度混杂与自知解释边界。
- **阅读笔记中的证据片段：** SAPLMA（Statement Accuracy Prediction based on Language Model Activations）用一条陈述最后token的隐藏激活，训练真假分类器。它同时测试外部提供的句子与OPT自己生成的句子，研究是否存在可跨主题读出的事实性相关信号。
- **来源：** [精读笔记](notes/important/I094_Internal_State_Knows.md)；[论文页面](https://arxiv.org/abs/2304.13734)

## I095 · TrueTeacher: Learning Factual Consistency Evaluation with Large Language Models

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 J
- **研究定位：** LLM监督数据与学生蒸馏
- **需核查的条件或限制：** 生成器/来源域分离、人评分层抽样、结构标签噪声与多语迁移。
- **阅读笔记中的证据片段：** 目标是来源条件的整摘要事实一致性，包含矛盾和未被支持的内容，不评价开放世界真值或任务信息覆盖。论文把传统NLI与摘要分布失配作为动机：单句NLI训练不充分涵盖长来源、抽象摘要与实际模型错误。
- **来源：** [精读笔记](notes/important/I095_TrueTeacher.md)；[论文页面](https://arxiv.org/abs/2305.11171)

## I096 · Uncertainty Quantification for Language Models: A Suite of Black-Box, White-Box, LLM Judge, and Ensemble Scorers

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 U；次类 J;T
- **研究定位：** 作者把幻觉定义为回应中任何非事实内容，操作上却用“答案对标准答案是否正确”的二值标签；六个都是数学、选择、短答QA，不能代表复合长文中的逐论断非事实。正类h=1是错误/幻觉，置信分数0–1越高越可能正确，低于阈值判幻觉；论文训练/评估的标签由标准答案离线得到，部署打分不看标准答案。数学只取输出前导整数与gold比较，字母选择题只接受独立A–E；短答若生成文本包含任何可接受答案子串即记正确。这些规则会把“正确关键词+错误否定/背景”的回答判对，也可能拒绝语义等价表达；因此是格式化QA近似gold，不是人工事实标注。
- **需核查的条件或限制：** 本文没有跨数据集/模型的已调权重迁移测试，作者明确限于同域。所有模型来自商业API，版本、token logprob支持和时间变化会影响白盒/裁判分数；原文开放源码不是开放完整API实验。标签是自动格式判题，短答子串可导致false correct。NLI跨长句可能将矛盾局部淹没；稳定地重复错误也可高NSN。5折按题目而非所有候选独立划分需在代码复核，避免同题候选泄漏。该研究描述的方法应用于高风险情境的说法仅是动机，没有临床/金融/法律真实任务测试。筛选可能系统排除某些群体的正确答案，作者也建议分层审计。
- **阅读笔记中的证据片段：** 作者把幻觉定义为回应中任何非事实内容，操作上却用“答案对标准答案是否正确”的二值标签；六个都是数学、选择、短答QA，不能代表复合长文中的逐论断非事实。正类h=1是错误/幻觉，置信分数0–1越高越可能正确，低于阈值判幻觉；论文训练/评估的标签由标准答案离线得到，部署打分不看标准答案。数学只取输出前导整数与gold比较，字母选择题只接受独立A–E；短答若生成文本包含任何可接受答案子串即记正确。这些规则会把“正确关键词+错误否定/背景”的回答判对，也可能拒绝语义等价表达；因此是格式化QA近似gold，不是人工事实标注。
- **来源：** [精读笔记](notes/important/I096_UQLM_Suite.md)；[论文页面](https://arxiv.org/abs/2504.19254)

## I097 · Chainpoll: A high efficacy method for LLM hallucination detection

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 J；次类 U
- **研究定位：** 回应级二分类：开放域为关于现实世界的错误陈述；封闭域为背离给定上下文，二者本质不同。ChainPoll用gpt-3.5-turbo读提示、原模型输出与相关参考文档（Adherence），按精心设计的详细CoT步骤先解释后判“是否有幻觉”；通常独立调用5次，yes比例是幻觉排序分数（高分更可能错），不是经校准的概率。Correctness提示检查开放域，Adherence提示检查来源忠实性。PDF7列表误把Adherence说成“detect open-domain”，但下一句明说Adherence用closed-domain提示，按定义与表4、图1一致应判为笔误。论文声称详细CoT可供用户解释，但解释的流畅性、因果忠实性和证据正确性没有独立人工验证；作者注释承认CoT未必反映真实推理。
- **需核查的条件或限制：** 见原笔记；本卡未自动抽出限制段落。
- **阅读笔记中的证据片段：** 回应级二分类：开放域为关于现实世界的错误陈述；封闭域为背离给定上下文，二者本质不同。ChainPoll用gpt-3.5-turbo读提示、原模型输出与相关参考文档（Adherence），按精心设计的详细CoT步骤先解释后判“是否有幻觉”；通常独立调用5次，yes比例是幻觉排序分数（高分更可能错），不是经校准的概率。Correctness提示检查开放域，Adherence提示检查来源忠实性。PDF7列表误把Adherence说成“detect open-domain”，但下一句明说Adherence用closed-domain提示，按定义与表4、图1一致应判为笔误。论文声称详细CoT可供用户解释，但解释的流畅性、因果忠实性和证据正确性没有独立人工验证；作者注释承认CoT未必反映真实推理。
- **来源：** [精读笔记](notes/important/I097_ChainPoll.md)；[论文页面](https://arxiv.org/abs/2310.18344)

## I100 · G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment

- **层级／研究角色：** important／评价方法
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 J；次类 H
- **研究定位：** LLM多维裁判
- **需核查的条件或限制：** 任务步骤、评分采样、解析失败、文章内相关与LLM文本偏好。
- **阅读笔记中的证据片段：** 核心问题是开放生成文本的多维质量评价，不是单独的新幻觉数据集。G-Eval用LLM产生任务评价步骤，再以填表方式输出评分；其中consistency/groundedness才直接涉及来源事实支持，coherence、fluency、relevance、engagingness不能全部叫幻觉检测。
- **来源：** [精读笔记](notes/important/I100_G_Eval.md)；[论文页面](https://arxiv.org/abs/2303.16634)

## I101 · Human-like Summarization Evaluation with ChatGPT

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 J；次类 H
- **研究定位：** LLM模拟四类人类摘要评价协议
- **需核查的条件或限制：** 来源支持/覆盖/偏好分界、prompt敏感、专家参照自包含、NaN覆盖、解释真实性与历史成本。
- **阅读笔记中的证据片段：** 把人类标注指令改成ChatGPT提示，让同一个API执行四种协议：1–5多维打分、两摘要偏好、SCU覆盖、句子来源支持判断。贡献是灵活的自然语言评价接口及早期元评价，不是发明新的通用幻觉定义，也不是四协议测同一东西。
- **来源：** [精读笔记](notes/important/I101_Humanlike_Summarization_Evaluation.md)；[论文页面](https://arxiv.org/abs/2304.02554)

## I102 · Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena

- **层级／研究角色：** important／元评估/审计
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 —；次类 J;H
- **研究定位：** 开放式多轮助手的人类偏好代理裁判
- **需核查的条件或限制：** S1/S2条件分母、投票/题级聚合、独立参考与候选锚定、位置/冗长偏差、反馈说服效应、生成格式及模型训练风格/知识分离。
- **阅读笔记中的证据片段：** 本文研究开放式多轮聊天助手的helpfulness/human preference，不是专门来源一致性检测。默认rubric综合helpfulness、relevance、accuracy、depth、creativity、detail；一个总分混合多个维度。正文第9页明确承认主要忽略safety，准确性等维度没有分开。
- **来源：** [精读笔记](notes/important/I102_MTBench_Chatbot_Arena_Judges.md)；[论文页面](https://arxiv.org/abs/2306.05685)

## I103 · LLMs as Factual Reasoners: Insights from Existing Benchmarks and Beyond

- **层级／研究角色：** important／元评估/审计
- **评价对象：** 来源忠实性
- **技术：** 主类 —；次类 J;E
- **研究定位：** 十域局部编辑事实一致性基准与LLM裁判元评价
- **需核查的条件或限制：** 边界过滤、条件解释质量、种子聚类/Oracle信息、合成编辑偏差、原文分组划分及论文/发布版本差异。
- **阅读笔记中的证据片段：** 本篇主要贡献是LLM事实一致性裁判的元评价与基准设计，不是一个新的通用幻觉概率公式。全文有三条证据链：在可控FactCC合成错误上比较不同提示和模型；检查AggreFact/DialSummEval的标签与任务定义；设计人工核验种子、模型局部编辑、人工重标的SummEdits十域基准。
- **来源：** [精读笔记](notes/important/I103_SummEdits_Factual_Reasoners.md)；[论文页面](https://arxiv.org/abs/2305.14540)

## I104 · LM vs LM: Detecting Factual Errors via Cross Examination

- **层级／研究角色：** important／评价方法
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 J；次类 U
- **研究定位：** 动态交叉询问的黑盒声明检测
- **需核查的条件或限制：** 矛盾错端识别、单类合成错误、substring标签粒度、不明确默认拒绝、投票/追问预算混杂与正式版指标对齐。
- **阅读笔记中的证据片段：** 输入是模型EXAMINEE生成的事实声明C，另一个角色EXAMINER提问、汇总答案，最后判C correct/incorrect。两个角色可用同一个模型、不同prompt；并不要求是两个独立训练的系统。主要任务是闭卷QA/事实补全产生的回答声明，无必需参考文档或实时检索。
- **来源：** [精读笔记](notes/important/I104_LM_vs_LM.md)；[论文页面](https://arxiv.org/abs/2305.13281)

## I105 · Large Language Models are not Fair Evaluators

- **层级／研究角色：** important／元评估/审计
- **评价对象：** 跨目标或概念研究
- **技术：** 主类 —；次类 J;H
- **研究定位：** 裁判位置偏差
- **需核查的条件或限制：** 交换校准、采样分歧与人工介入、偏好/事实性区别和解析后不平衡。
- **阅读笔记中的证据片段：** 本文研究同一对回答仅改变展示位置就改变优劣判断，fairness指位置不变性，不是人口群体公平或世界事实真值。评判综合helpfulness、relevance、accuracy、detail，胜负标签并非专门的幻觉标签。用于本综述应放在LLM裁判可靠性/协议偏差，不把其胜率直接当事实错误率。
- **来源：** [精读笔记](notes/important/I105_FairEval.md)；[论文页面](https://arxiv.org/abs/2305.17926)

## I106 · Lynx: An Open Source Hallucination Evaluation Model

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 J;E
- **研究定位：** 合成扰动与标签条件解释蒸馏的RAG来源一致性裁判
- **需核查的条件或限制：** 任务粒度/忠实性界线、类不平衡、格式/长度捷径、宏微聚合、候选身份、缓存复算、格式解析与后续训练版本重叠。
- **阅读笔记中的证据片段：** 输入为question、context/document、candidate answer，输出解释REASONING和二元SCORE PASS/FAIL。所谓reference-free指推理时不需要人工gold answer，仍需要指定来源文档；训练却使用gold答案/标签及教师解释，不是无监督或无外部监督方法。
- **来源：** [精读笔记](notes/important/I106_Lynx_HaluBench.md)；[论文页面](https://arxiv.org/abs/2407.08488)

## I107 · The Illusion of Progress: Re-evaluating Hallucination Detection in LLMs

- **层级／研究角色：** important／元评估/审计
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 T;J;H
- **研究定位：** QA检测伪金标与指标元评估
- **需核查的条件或限制：** 分歧人核的选择条件、拒答合并、长度/格式混杂、谱形状、百分比分母和平均次序、重复不变性及提示因果识别。
- **阅读笔记中的证据片段：** 论文不主要提出新裁判，而是审计检测器的评价标签。若把ROUGE-L F1≥.3当答案正确、低于阈值当幻觉，那么一个擅长识别长答案的检测器可能看起来很好；换更语义化的正确性标签后，原有AUROC排序会变。这属于元评估，应该连接综述的“定义—标注—分数可比性”主线。
- **来源：** [精读笔记](notes/important/I107_Illusion_of_Progress.md)；[论文页面](https://aclanthology.org/2025.emnlp-main.1761/)

## I108 · Why Does ChatGPT Fall Short in Providing Truthful Answers?

- **层级／研究角色：** important／领域实证/现象分析
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 H;E
- **研究定位：** 开放域QA失败主题与知识诊断
- **需核查的条件或限制：** 记忆存在性/提示可答性、证据粒度Oracle条件、实体消歧/背景泄漏、substring判分、合理拒答与分母/配对统计识别。
- **阅读笔记中的证据片段：** 论文在开放域问答上问“模型为什么答错”，先将输出错误分类，再用补证据、实体背景和分解追问测试可能缺陷。它既涉及输出正确性评估，也涉及根据行为推断能力原因。应放在“定义/标注口径与诊断性评价”以及“知识与推理来源”部分，不能当作已经验证的通用幻觉检测器。
- **来源：** [精读笔记](notes/important/I108_Why_ChatGPT_Falls_Short_Truthful_Answers.md)；[论文页面](https://arxiv.org/abs/2304.10513)

## I109 · Detecting and Mitigating Hallucinations in Multilingual Summarisation

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 E
- **研究定位：** 多语银标教师蒸馏
- **需核查的条件或限制：** 翻译噪声、来源划分、跨语刻度、人评池化混杂和指标驱动损失加权。
- **阅读笔记中的证据片段：** 已有英文来源一致性指标通常依赖英文NLI、QA、依存句法或实体模型。直接把同样架构推广到低资源语言，需要额外标注与工具；把每次待评摘要翻回英语则持续付出翻译费用，并引入新噪声。作者用英语多教师指标生成银标，翻译训练对，再训练目标语言分类器mFACT，使后续评估不用逐次翻译。
- **来源：** [精读笔记](notes/important/I109_mFACT_Multilingual_Summarisation.md)；[论文页面](https://arxiv.org/abs/2305.13632)

## I110 · Evaluating Hallucinations in Chinese Large Language Models

- **层级／研究角色：** important／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 J;H
- **研究定位：** 原生中文对抗世界知识QA
- **需核查的条件或限制：** 误导/知识划分、参考与拒答口径、GPT4投票、缓存版本/分母和对齐/检索因果边界。
- **阅读笔记中的证据片段：** HalluQA是原生中文对抗式开放QA集，不是英文问题机械翻译，也不是给来源让裁判识别不支持span的RAG数据。450题覆盖中文历史、文学、习俗、社会现象等，分Misleading、Misleading-hard、Knowledge，目标同时包含诱导性错误信念和细粒度知识错误。它的价值是把中文背景、模型阶段差异、假前提/刻板印象/虚实混淆和知识缺口放入统一测试，并发布生成与裁判缓存。
- **来源：** [精读笔记](notes/important/I110_HalluQA_Chinese_LLMs.md)；[论文页面](https://arxiv.org/abs/2310.03368)

## I111 · HalOmi: A Manually Annotated Benchmark for Multilingual Hallucination and Omission Detection in Machine Translation

- **层级／研究角色：** important／基准/数据
- **评价对象：** 来源忠实性
- **技术：** 主类 —；次类 H;T
- **研究定位：** 多语MT专业人工细粒度病理基准
- **需核查的条件或限制：** 幻觉/误译/遗漏区别、自然与扰动排名迁移、贡献/长度聚合、来源分组和版本/分母审计。
- **阅读笔记中的证据片段：** 本文研究条件生成中的来源无关译文内容与来源信息遗漏，不是开放QA世界知识真伪。它将18翻译方向、自然错误、专业人工句级/词级标注和可获取的生成模型放在一起，使低资源迁移、内部检测器与细粒度解释可被真正评估。
- **来源：** [精读笔记](notes/important/I111_HalOmi_Multilingual_MT.md)；[论文页面](https://arxiv.org/abs/2305.11746)

## I112 · Hallucinations in Large Multilingual Translation Models

- **层级／研究角色：** important／领域实证/现象分析
- **评价对象：** 来源忠实性
- **技术：** 主类 —；次类 H
- **研究定位：** 跨资源/方向/领域的自然与扰动幻觉分析
- **需核查的条件或限制：** ALTI/TNG校准、共同候选分母、模型规模交互、条件fallback、有限人验/抽取与公开缓存样本身份审计。
- **阅读笔记中的证据片段：** 过去MT幻觉检测常研究单一高资源双语、小模型、人工扰动；本研究扩展到不同资源层级、语言方向、领域和模型规模，比较传统多语NMT与提示式LLM。重要贡献是揭示“平均质量提高”“参数变大”“幻觉减少”并非处处等价，并把检测接到fallback系统。
- **来源：** [精读笔记](notes/important/I112_Large_Multilingual_Translation_Hallucinations.md)；[论文页面](https://arxiv.org/abs/2303.16104)

## I113 · Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models

- **层级／研究角色：** important／领域实证/现象分析
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 H;E
- **研究定位：** 从SCOTUS、联邦上诉法院USCOA、地区法院USDC判例各抽5000个，按年份/巡回区/州—年份分层，以CAP、SCDB、ACDB、国会推翻列表及Shepard’s等元数据建oracle。总14任务：低复杂度存在、法院、引注、判决撰写法官；中等为维持/推翻、原文引句、被引用权威、推翻年份；高等为两个案例法理一致性、案情、程序姿态、后续程序、核心法律问题、中心裁判要旨。前9个有表格金标：引注由eyecite解析，法官名模糊匹配，引句须在多数意见中，权威只看是否引用不看正负效力；推翻年份仅279个已推翻最高法院案，法理一致性仅5000对最高法院案（2839同意、2161不同意），Shepard’s代码粗化也会损失语义。法院题给了含报告集的引注，已泄露法院层级，但不泄露具体上诉巡回或地区庭。测试零样本/三示例，总80万查询。前9任务温度0，明确拒答计非幻觉，所以错误率并非在已作答样本中的错误条件概率。
- **需核查的条件或限制：** Matthew Dahl、Varun Magesh、Mirac Suzgun、Daniel E. Ho，Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models，Journal of Legal Analysis 2024，所存arXiv:2401.01301v2共80页（正文1–40、参考41–54、附录55–80）；逐页核对任务表、三层法院结果、反事实/校准附表、100例人工一致性及提示模板。官方reglab复现代码已固定在620734a1ccb84efc6827635ac76a2fb6504b2f64并打包qa/I113official；作者另公开Harvard Dataverse复现数据和HuggingFace基准。HF仓库总约430MB、两CS…
- **阅读笔记中的证据片段：** 从SCOTUS、联邦上诉法院USCOA、地区法院USDC判例各抽5000个，按年份/巡回区/州—年份分层，以CAP、SCDB、ACDB、国会推翻列表及Shepard’s等元数据建oracle。总14任务：低复杂度存在、法院、引注、判决撰写法官；中等为维持/推翻、原文引句、被引用权威、推翻年份；高等为两个案例法理一致性、案情、程序姿态、后续程序、核心法律问题、中心裁判要旨。前9个有表格金标：引注由eyecite解析，法官名模糊匹配，引句须在多数意见中，权威只看是否引用不看正负效力；推翻年份仅279个已推翻最高法院案，法理一致性仅5000对最高法院案（2839同意、2161不同意），Shepard’s代码粗化也会损失语义。法院题给了含报告集的引注，已泄露法院层级，但不泄露具体上诉巡回或地区庭。测试零样本/三示例，总80万查询。前9任务温度0，明确拒答计非幻觉，所以错误率并非在已作答样本中的错误条件概率。
- **来源：** [精读笔记](notes/important/I113_Large_Legal_Fictions.md)；[论文页面](https://arxiv.org/abs/2401.01301)

## I114 · Looking for a Needle in a Haystack: A Comprehensive Study of Hallucinations in Neural Machine Translation

- **层级／研究角色：** important／基准/数据
- **评价对象：** 来源忠实性
- **技术：** 主类 —；次类 H;T
- **研究定位：** 自然NMT严重脱离的尾部检测元评估
- **需核查的条件或限制：** 概率/质量差异、多标签互斥映射、选择分母、MC重排与修复误改成本。
- **阅读笔记中的证据片段：** 当MT模型大多数译文都可接受时，找出少量严重来源脱离译文比识别普通低质量更困难。作者反对只在噪声/域外/模型扰动放大病例上验证探测器，转向没有人工扰动的域内模型，人工细标错误，再比较既有启发式、质量指标、概率和MC不确定性。
- **来源：** [精读笔记](notes/important/I114_Needle_Haystack_NMT.md)；[论文页面](https://aclanthology.org/2023.eacl-main.75/)

## I115 · Med-HALT: Medical Domain Hallucination Test for Large Language Models

- **层级／研究角色：** important／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 J;H
- **研究定位：** 医学错误建议/不可答与文献记忆基准
- **需核查的条件或限制：** 恒定拒答基线、标识符真值、语义/格式分离、归一化/异常分母、指令微调交互及真实/伪造构造审计。
- **阅读笔记中的证据片段：** 论文提出医学领域七任务，试图区分reasoning hallucination和memory hallucination，强调信息不足时不要编造。价值是将“被错误建议带偏”“没有合适答案”“虚构问题仍硬答”“编造文献标识”放进可自动运行的测试体系，而非只测常规医学选择题。
- **来源：** [精读笔记](notes/important/I115_Med_HALT.md)；[论文页面](https://arxiv.org/abs/2307.15343)

## I116 · MedHallu: A Comprehensive Benchmark for Detecting Medical Hallucinations in Large Language Models

- **层级／研究角色：** important／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 J;H
- **研究定位：** 医学合成答案判别与裁判相对难度
- **需核查的条件或限制：** oracle上下文、非等价/遗漏构念、过滤家族偏差、长度捷径、NotSure条件覆盖率、parser/随机配对及表格均值审计。
- **阅读笔记中的证据片段：** 给问题Q和一个答案A，输出0=事实、1=幻觉；另有提供相关原文K以及允许2=Not Sure设置。数据每条包含正确答案和合成错误答案，评估脚本随机选其中一个。与I115 Med-HALT的模型自己选择/回忆答案不同，这里评估判别能力，不代表模型在自然使用中的生成幻觉率。
- **来源：** [精读笔记](notes/important/I116_MedHallu.md)；[论文页面](https://arxiv.org/abs/2502.14302)

## I117 · MultiHal: Multilingual Dataset for Knowledge-Graph Grounded Evaluation of LLM Hallucinations

- **层级／研究角色：** important／基准/数据
- **评价对象：** 外部事实性/正确性
- **技术：** 主类 —；次类 E;J;H
- **研究定位：** 多语KG证据注入与生成事实性
- **需核查的条件或限制：** 答案知情路径、关系支持/时效、问题与路径加权、参考集合、翻译审核、裁判/相关/误差条及公开缓存数值核验。
- **阅读笔记中的证据片段：** MultiHal把七个英文事实性/QA基准映射到Wikidata路径，形成多语言、至多二跳的知识注入测试。比较同一问题无路径QA与有路径KG-RAG，主要验证模型在给定结构支持时能否生成更接近参考的答案。它并非天然带全部生成幻觉span的检测金标，也没有直接比较多种真实检索器。
- **来源：** [精读笔记](notes/important/I117_MultiHal.md)；[论文页面](https://arxiv.org/abs/2505.14101)

## I118 · Optimal Transport for Unsupervised Hallucination Detection in Neural Machine Translation

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 无
- **研究定位：** 内部attention边际异常与非参数参考库
- **需核查的条件或限制：** TV/位置W1几何、门控尺度、真实数组/标签版本、误报口径及跨模型/多语适配。
- **阅读笔记中的证据片段：** 作者的假设是：无关译文的cross-attention分布应偏离正常译文，因此把检测当anomaly detection，以OT距离量化。三方法为Wass-to-Unif、Wass-to-Data、门控Wass-Combo。目标是运行时不需要当前输入的人工参考，也不训练专门人工幻觉分类器。
- **来源：** [精读笔记](notes/important/I118_Optimal_Transport_Attention.md)；[论文页面](https://arxiv.org/abs/2212.09631)

## I119 · When Models Lie, We Learn: Multilingual Span-Level Hallucination Detection with PsiloQA

- **层级／研究角色：** important／评价方法
- **评价对象：** 来源忠实性
- **技术：** 主类 T；次类 H
- **研究定位：** 多语QA自然生成错误的LLM银标跨度监督
- **需核查的条件或限制：** 来源/问题划分、标记文字到字符坐标、AP方向/空集/宏平均、多语训练量、源码重复权重/缺context和成本版本审计。
- **阅读笔记中的证据片段：** 序列级幻觉检测只回答“这段回答是否有问题”，不能定位最小错误内容。PsiloQA研究大规模、多语言、span级监督能否自动构造，及这种监督能否训练更强的跨语言检测器。主要资源贡献是14语言Wikipedia QA、自然生成错误、GPT-4o跨度标注；方法贡献主要是统一比较UQ、LLM标注和编码器微调，而不是提出一种全新幻觉定义或独立验证所有世界事实的算法。
- **来源：** [精读笔记](notes/important/I119_PsiloQA.md)；[论文页面](https://arxiv.org/abs/2510.04849)
