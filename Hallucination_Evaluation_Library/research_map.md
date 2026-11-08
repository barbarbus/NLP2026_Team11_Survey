# 文献研究地图与阅读安排

整理日期：2026-11-06。核心论文 16 篇，核心之外的重要论文 108 篇。所有计入数量的论文均已保存可解析PDF。

分类与“对应核心”表示本项目的概念组织关系，并非已验证的直接引用或继承关系。重要论文是推荐候选池，不表示已完成全文精读，也不表示每篇都必须写入最终8页报告。预印本与已发表版本须在最终引用前再次统一。

## 核心阅读顺序

先读 C01–C04 建立全景，结合 C15–C16 明确“事实性、忠实性、无支持信息”的区别；再读 C05–C06 和 C13 了解基准；随后比较 C07–C10 的不同方法；以 C11、C14 检查评价方法自身是否可靠，最后用 C12 连接RAG场景。

### C01 Survey of Hallucination in Natural Language Generation
历史基础：NLG幻觉定义、任务边界与早期指标。
[原始页面](https://arxiv.org/abs/2202.03629) · [本地PDF](papers/core/C01_Survey_of_Hallucination_in_Natural_Language_Generation.pdf)

### C02 A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions
LLM全景框架：事实性/忠实性、检测方法和基准分类。
[原始页面](https://arxiv.org/abs/2311.05232) · [本地PDF](papers/core/C02_A_Survey_on_Hallucination_in_Large_Language_Models_Principles_Taxonomy_Challenges_and_Open_Questions.pdf)

### C03 Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models
补充全景视角，交叉核对分类，而非照搬现成综述。
[原始页面](https://arxiv.org/abs/2309.01219) · [本地PDF](papers/core/C03_Siren_s_Song_in_the_AI_Ocean_A_Survey_on_Hallucination_in_Large_Language_Models.pdf)

### C04 A Survey of Automatic Hallucination Evaluation on Natural Language Generation
最贴近本选题的自动评估综述；重点比较我们的分类维度与现有综述的差异。
[原始页面](https://arxiv.org/abs/2404.12041) · [本地PDF](papers/core/C04_A_Survey_of_Automatic_Hallucination_Evaluation_on_Natural_Language_Generation.pdf)

### C05 TruthfulQA: Measuring How Models Mimic Human Falsehoods
真实性基准：常见误解与开放问答；不能等同所有形式的幻觉。
[原始页面](https://arxiv.org/abs/2109.07958) · [本地PDF](papers/core/C05_TruthfulQA_Measuring_How_Models_Mimic_Human_Falsehoods.pdf)

### C06 HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models
幻觉识别基准：考察合成错误与自然错误的分布差异。
[原始页面](https://arxiv.org/abs/2305.11747) · [本地PDF](papers/core/C06_HaluEval_A_Large_Scale_Hallucination_Evaluation_Benchmark_for_Large_Language_Models.pdf)

### C07 FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation
原子事实核验：研究事实分解、证据检索和事实精确率的局限。
[原始页面](https://arxiv.org/abs/2305.14251) · [本地PDF](papers/core/C07_FActScore_Fine_grained_Atomic_Evaluation_of_Factual_Precision_in_Long_Form_Text_Generation.pdf)

### C08 SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models
黑箱采样一致性：研究无需外部证据时的检测及多次采样成本。
[原始页面](https://arxiv.org/abs/2303.08896) · [本地PDF](papers/core/C08_SelfCheckGPT_Zero_Resource_Black_Box_Hallucination_Detection_for_Generative_Large_Language_Models.pdf)

### C09 AlignScore: Evaluating Factual Consistency with a Unified Alignment Function
统一对齐函数：比较蕴含/训练型指标与LLM裁判。
[原始页面](https://arxiv.org/abs/2305.16739) · [本地PDF](papers/core/C09_AlignScore_Evaluating_Factual_Consistency_with_a_Unified_Alignment_Function.pdf)

### C10 Detecting hallucinations in large language models using semantic entropy
语义熵：区分语义不确定性与词面变化，讨论自信错误的边界。
[原始页面](https://www.nature.com/articles/s41586-024-07421-0) · [本地PDF](papers/core/C10_Detecting_hallucinations_in_large_language_models_using_semantic_entropy.pdf)

### C11 TRUE: Re-evaluating Factual Consistency Evaluation
跨任务元评估：关注自动指标和人工标注的对齐，而非单一排行榜。
[原始页面](https://arxiv.org/abs/2204.04991) · [本地PDF](papers/core/C11_TRUE_Re_evaluating_Factual_Consistency_Evaluation.pdf)

### C12 RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models
RAG细粒度标注：区分证据忠实性、无依据内容和事实错误。
[原始页面](https://arxiv.org/abs/2401.00396) · [本地PDF](papers/core/C12_RAGTruth_A_Hallucination_Corpus_for_Developing_Trustworthy_Retrieval_Augmented_Language_Models.pdf)

### C13 FELM: Benchmarking Factuality Evaluation of Large Language Models
事实评价器的基准：区分被评价模型与评价器自身的能力。
[原始页面](https://arxiv.org/abs/2310.00741) · [本地PDF](papers/core/C13_FELM_Benchmarking_Factuality_Evaluation_of_Large_Language_Models.pdf)

### C14 Do My Eyes Deceive Me? A Survey of Human Evaluations of Hallucinations in NLG
人工评价协议：标注指南、标注者信息和一致性报告。
[原始页面](https://aclanthology.org/2025.inlg-main.4/) · [本地PDF](papers/core/C14_Do_My_Eyes_Deceive_Me_A_Survey_of_Human_Evaluations_of_Hallucinations_in_NLG.pdf)

### C15 An Audit on the Perspectives and Challenges of Hallucinations in NLP
术语审计：追踪不同论文对幻觉定义的不一致。
[原始页面](https://aclanthology.org/2024.emnlp-main.375/) · [本地PDF](papers/core/C15_An_Audit_on_the_Perspectives_and_Challenges_of_Hallucinations_in_NLP.pdf)

### C16 The Pitfalls of Defining Hallucination
定义反思：为什么不能把无支持、虚假、遗漏等概念混为一谈。
[原始页面](https://aclanthology.org/2024.cl-2.10/) · [本地PDF](papers/core/C16_The_Pitfalls_of_Defining_Hallucination.pdf)

## 重要论文如何围绕核心论文展开

### 定义、术语与综述框架（1篇）

- **I001 Factuality of Large Language Models: A Survey** — 对应核心：C01;C02;C03;C04;C15;C16；负责人：范一鸣 / 程子晨。梳理术语、边界和综述分类；不把综述替代原始实验论文。 [PDF](papers/important/I001_Factuality_of_Large_Language_Models_A_Survey.pdf) / [来源](https://aclanthology.org/2024.emnlp-main.1088/)

### 评估数据集与基准（23篇）

- **I002 A New Benchmark and Reverse Validation Method for Passage-level Hallucination Detection** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I002_A_New_Benchmark_and_Reverse_Validation_Method_for_Passage_level_Hallucination_Detection.pdf) / [来源](https://arxiv.org/abs/2310.06498)
- **I003 A Token-level Reference-free Hallucination Detection Benchmark for Free-form Text Generation** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I003_A_Token_level_Reference_free_Hallucination_Detection_Benchmark_for_Free_form_Text_Generation.pdf) / [来源](https://arxiv.org/abs/2104.08704)
- **I004 BAMBOO: A Comprehensive Benchmark for Evaluating Long Text Modeling Capacities of Large Language Models** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I004_BAMBOO_A_Comprehensive_Benchmark_for_Evaluating_Long_Text_Modeling_Capacities_of_Large_Language_Mode.pdf) / [来源](https://arxiv.org/abs/2309.13345)
- **I005 ETF: An Entity Tracing Framework for Hallucination Detection in Code Summaries** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I005_ETF_An_Entity_Tracing_Framework_for_Hallucination_Detection_in_Code_Summaries.pdf) / [来源](https://arxiv.org/abs/2410.14748)
- **I006 Enoki: Efficient Multi-Level Hallucination Detection** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I006_Enoki_Efficient_Multi_Level_Hallucination_Detection.pdf) / [来源](https://arxiv.org/abs/2609.00581)
- **I007 FRANK: A Benchmark for Factuality Metrics** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I007_FRANK_A_Benchmark_for_Factuality_Metrics.pdf) / [来源](https://aclanthology.org/2021.naacl-main.383/)
- **I008 FactCHD: Benchmarking Fact-Conflicting Hallucination Detection** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I008_FactCHD_Benchmarking_Fact_Conflicting_Hallucination_Detection.pdf) / [来源](https://arxiv.org/abs/2310.12086)
- **I010 Fine-grained Hallucination Detection and Editing for Language Models** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I010_Fine_grained_Hallucination_Detection_and_Editing_for_Language_Models.pdf) / [来源](https://arxiv.org/abs/2401.06855)
- **I011 FreshLLMs: Refreshing Large Language Models with Search Engine Augmentation** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I011_FreshLLMs_Refreshing_Large_Language_Models_with_Search_Engine_Augmentation.pdf) / [来源](https://arxiv.org/abs/2310.03214)
- **I012 Generating Benchmarks for Factuality Evaluation of Language Models** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I012_Generating_Benchmarks_for_Factuality_Evaluation_of_Language_Models.pdf) / [来源](https://arxiv.org/abs/2307.06908)
- **I013 HALoGEN: Fantastic LLM Hallucinations and Where to Find Them** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I013_HALoGEN_Fantastic_LLM_Hallucinations_and_Where_to_Find_Them.pdf) / [来源](https://aclanthology.org/2025.acl-long.71/)
- **I014 HalluLens: LLM Hallucination Benchmark** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I014_HalluLens_LLM_Hallucination_Benchmark.pdf) / [来源](https://aclanthology.org/2025.acl-long.1176/)
- **I015 Hallucinated but Factual! Inspecting the Factuality of Hallucinations in Abstractive Summarization** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I015_Hallucinated_but_Factual_Inspecting_the_Factuality_of_Hallucinations_in_Abstractive_Summarization.pdf) / [来源](https://aclanthology.org/2022.acl-long.236/)
- **I016 Hallucination Detection: A Probabilistic Framework Using Embeddings Distance Analysis** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I016_Hallucination_Detection_A_Probabilistic_Framework_Using_Embeddings_Distance_Analysis.pdf) / [来源](https://arxiv.org/abs/2502.08663)
- **I017 Halo: Estimation and Reduction of Hallucinations in Open-Source Weak Large Language Models** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I017_Halo_Estimation_and_Reduction_of_Hallucinations_in_Open_Source_Weak_Large_Language_Models.pdf) / [来源](https://arxiv.org/abs/2308.11764)
- **I018 Language Models Hallucinate, but May Excel at Fact Verification** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I018_Language_Models_Hallucinate_but_May_Excel_at_Fact_Verification.pdf) / [来源](https://aclanthology.org/2024.naacl-long.62/)
- **I019 Learning to Reason for Hallucination Span Detection** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I019_Learning_to_Reason_for_Hallucination_Span_Detection.pdf) / [来源](https://arxiv.org/abs/2510.02173)
- **I020 Monitoring Decoding: Mitigating Hallucination via Evaluating the Factuality of Partial Response during Generation** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I020_Monitoring_Decoding_Mitigating_Hallucination_via_Evaluating_the_Factuality_of_Partial_Response_durin.pdf) / [来源](https://arxiv.org/abs/2503.03106)
- **I021 RealTime QA: What's the Answer Right Now?** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I021_RealTime_QA_What_s_the_Answer_Right_Now.pdf) / [来源](https://arxiv.org/abs/2207.13332)
- **I022 Self-contradictory Hallucinations of Large Language Models: Evaluation, Detection and Mitigation** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I022_Self_contradictory_Hallucinations_of_Large_Language_Models_Evaluation_Detection_and_Mitigation.pdf) / [来源](https://arxiv.org/abs/2305.15852)
- **I023 Teaching with Lies: Curriculum DPO on Synthetic Negatives for Hallucination Detection** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I023_Teaching_with_Lies_Curriculum_DPO_on_Synthetic_Negatives_for_Hallucination_Detection.pdf) / [来源](https://arxiv.org/abs/2505.17558)
- **I024 The Dawn After the Dark: An Empirical Study on Factuality Hallucination in Large Language Models** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I024_The_Dawn_After_the_Dark_An_Empirical_Study_on_Factuality_Hallucination_in_Large_Language_Models.pdf) / [来源](https://aclanthology.org/2024.acl-long.586/)
- **I026 FactCheckmate: Preemptively Detecting and Mitigating Hallucinations in LMs** — 对应核心：C05;C06;C12;C13；负责人：李瑾 / 程子晨。比较标注粒度、错误覆盖、数据构造与污染风险。 [PDF](papers/important/I026_FactCheckmate_Preemptively_Detecting_and_Mitigating_Hallucinations_in_LMs.pdf) / [来源](https://arxiv.org/abs/2410.02899)

### 事实一致性、分类与蕴含指标（11篇）

- **I027 Adversarial NLI for Factual Correctness in Text Summarisation Models** — 对应核心：C07;C09;C11；负责人：李瑾 / 张磊 / 程子晨。比较细粒度事实性、蕴含/分类指标及摘要评价的历史基础。 [PDF](papers/important/I027_Adversarial_NLI_for_Factual_Correctness_in_Text_Summarisation_Models.pdf) / [来源](https://arxiv.org/abs/2005.11739)
- **I029 Beyond Factuality: A Comprehensive Evaluation of Large Language Models as Knowledge Generators** — 对应核心：C07;C09;C11；负责人：李瑾 / 张磊 / 程子晨。比较细粒度事实性、蕴含/分类指标及摘要评价的历史基础。 [PDF](papers/important/I029_Beyond_Factuality_A_Comprehensive_Evaluation_of_Large_Language_Models_as_Knowledge_Generators.pdf) / [来源](https://arxiv.org/abs/2310.07289)
- **I031 Evaluating Factuality in Generation with Dependency-level Entailment** — 对应核心：C07;C09;C11；负责人：李瑾 / 程子晨。蕴含/分类型事实一致性指标：比较粒度、训练信号和跨任务元评估。 [PDF](papers/important/I031_Evaluating_Factuality_in_Generation_with_Dependency_level_Entailment.pdf) / [来源](https://aclanthology.org/2020.findings-emnlp.322/)
- **I032 FacTool: Factuality Detection in Generative AI -- A Tool Augmented Framework for Multi-Task and Multi-Domain Scenarios** — 对应核心：C07;C09;C11；负责人：李瑾 / 张磊 / 程子晨。比较细粒度事实性、蕴含/分类指标及摘要评价的历史基础。 [PDF](papers/important/I032_FacTool_Factuality_Detection_in_Generative_AI_A_Tool_Augmented_Framework_for_Multi_Task_and_Multi_Do.pdf) / [来源](https://arxiv.org/abs/2307.13528)
- **I035 On Faithfulness and Factuality in Abstractive Summarization** — 对应核心：C07;C09;C11；负责人：李瑾 / 张磊 / 程子晨。比较细粒度事实性、蕴含/分类指标及摘要评价的历史基础。 [PDF](papers/important/I035_On_Faithfulness_and_Factuality_in_Abstractive_Summarization.pdf) / [来源](https://arxiv.org/abs/2005.00661)
- **I036 Ranking Generated Summaries by Correctness: An Interesting but Challenging Application for Natural Language Inference** — 对应核心：C07;C09;C11；负责人：李瑾 / 张磊 / 程子晨。比较细粒度事实性、蕴含/分类指标及摘要评价的历史基础。 [PDF](papers/important/I036_Ranking_Generated_Summaries_by_Correctness_An_Interesting_but_Challenging_Application_for_Natural_La.pdf) / [来源](https://aclanthology.org/P19-1213/)
- **I072 Entity-level Factual Consistency of Abstractive Text Summarization** — 对应核心：C07;C09;C11；负责人：李瑾 / 程子晨。蕴含/分类型事实一致性指标：比较粒度、训练信号和跨任务元评估。 [PDF](papers/important/I072_Entity_level_Factual_Consistency_of_Abstractive_Text_Summarization.pdf) / [来源](https://aclanthology.org/2021.eacl-main.235/)
- **I073 Evaluating the Factual Consistency of Abstractive Text Summarization** — 对应核心：C07;C09;C11；负责人：李瑾 / 程子晨。蕴含/分类型事实一致性指标：比较粒度、训练信号和跨任务元评估。 [PDF](papers/important/I073_Evaluating_the_Factual_Consistency_of_Abstractive_Text_Summarization.pdf) / [来源](https://arxiv.org/abs/1910.12840)
- **I074 Fast and Accurate Factual Inconsistency Detection Over Long Documents** — 对应核心：C07;C09;C11；负责人：李瑾 / 程子晨。蕴含/分类型事实一致性指标：比较粒度、训练信号和跨任务元评估。 [PDF](papers/important/I074_Fast_and_Accurate_Factual_Inconsistency_Detection_Over_Long_Documents.pdf) / [来源](https://arxiv.org/abs/2310.13189)
- **I092 SummaC: Re-Visiting NLI-based Models for Inconsistency Detection in Summarization** — 对应核心：C07;C09;C11；负责人：李瑾 / 程子晨。蕴含/分类型事实一致性指标：比较粒度、训练信号和跨任务元评估。 [PDF](papers/important/I092_SummaC_Re_Visiting_NLI_based_Models_for_Inconsistency_Detection_in_Summarization.pdf) / [来源](https://arxiv.org/abs/2111.09525)
- **I095 TrueTeacher: Learning Factual Consistency Evaluation with Large Language Models** — 对应核心：C07;C09;C11；负责人：李瑾 / 程子晨。蕴含/分类型事实一致性指标：比较粒度、训练信号和跨任务元评估。 [PDF](papers/important/I095_TrueTeacher_Learning_Factual_Consistency_Evaluation_with_Large_Language_Models.pdf) / [来源](https://arxiv.org/abs/2305.11171)

### 问答式事实评估（7篇）

- **I040 Do We Know What We Don’t Know? Studying Unanswerable Questions beyond SQuAD 2.0** — 对应核心：C09;C11；负责人：李瑾 / 程子晨。比较问答式核验和基准；分析问题生成及答案匹配误差。 [PDF](papers/important/I040_Do_We_Know_What_We_Don_t_Know_Studying_Unanswerable_Questions_beyond_SQuAD_2_0.pdf) / [来源](https://aclanthology.org/2021.findings-emnlp.385/)
- **I041 Evaluating Correctness and Faithfulness of Instruction-Following Models for Question Answering** — 对应核心：C09;C11；负责人：李瑾 / 程子晨。比较问答式核验和基准；分析问题生成及答案匹配误差。 [PDF](papers/important/I041_Evaluating_Correctness_and_Faithfulness_of_Instruction_Following_Models_for_Question_Answering.pdf) / [来源](https://arxiv.org/abs/2307.16877)
- **I042 FEQA: A Question Answering Evaluation Framework for Faithfulness Assessment in Abstractive Summarization** — 对应核心：C09;C11；负责人：李瑾 / 程子晨。问答式事实核验：比较问题覆盖率、答案匹配误差和人工一致性。 [PDF](papers/important/I042_FEQA_A_Question_Answering_Evaluation_Framework_for_Faithfulness_Assessment_in_Abstractive_Summarizat.pdf) / [来源](https://aclanthology.org/2020.acl-main.454/)
- **I043 QuestEval: Summarization Asks for Fact-based Evaluation** — 对应核心：C09;C11；负责人：李瑾 / 程子晨。问答式事实核验：比较问题覆盖率、答案匹配误差和人工一致性。 [PDF](papers/important/I043_QuestEval_Summarization_Asks_for_Fact_based_Evaluation.pdf) / [来源](https://arxiv.org/abs/2103.12693)
- **I054 Q2: Evaluating Factual Consistency in Knowledge-Grounded Dialogues via Question Generation and Question Answering** — 对应核心：C09;C11；负责人：李瑾 / 程子晨。问答式事实核验：比较问题覆盖率、答案匹配误差和人工一致性。 [PDF](papers/important/I054_Q2_Evaluating_Factual_Consistency_in_Knowledge_Grounded_Dialogues_via_Question_Generation_and_Questi.pdf) / [来源](https://aclanthology.org/2021.emnlp-main.619/)
- **I062 Asking and Answering Questions to Evaluate the Factual Consistency of Summaries** — 对应核心：C09;C11；负责人：李瑾 / 程子晨。问答式事实核验：比较问题覆盖率、答案匹配误差和人工一致性。 [PDF](papers/important/I062_Asking_and_Answering_Questions_to_Evaluate_the_Factual_Consistency_of_Summaries.pdf) / [来源](https://aclanthology.org/2020.acl-main.450/)
- **I086 QAFactEval: Improved QA-Based Factual Consistency Evaluation for Summarization** — 对应核心：C09;C11；负责人：李瑾 / 程子晨。问答式事实核验：比较问题覆盖率、答案匹配误差和人工一致性。 [PDF](papers/important/I086_QAFactEval_Improved_QA_Based_Factual_Consistency_Evaluation_for_Summarization.pdf) / [来源](https://arxiv.org/abs/2112.08542)

### 外部证据核验与RAG忠实性（13篇）

- **I044 ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I044_ARES_An_Automated_Evaluation_Framework_for_Retrieval_Augmented_Generation_Systems.pdf) / [来源](https://aclanthology.org/2024.naacl-long.20/)
- **I045 Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I045_Can_LLMs_Express_Their_Uncertainty_An_Empirical_Evaluation_of_Confidence_Elicitation_in_LLMs.pdf) / [来源](https://arxiv.org/abs/2306.13063)
- **I046 Complex Claim Verification with Evidence Retrieved in the Wild** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I046_Complex_Claim_Verification_with_Evidence_Retrieved_in_the_Wild.pdf) / [来源](https://arxiv.org/abs/2305.11859)
- **I047 FactKG: Fact Verification via Reasoning on Knowledge Graphs** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I047_FactKG_Fact_Verification_via_Reasoning_on_Knowledge_Graphs.pdf) / [来源](https://arxiv.org/abs/2305.06590)
- **I048 Fact-Checking Complex Claims with Program-Guided Reasoning** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I048_Fact_Checking_Complex_Claims_with_Program_Guided_Reasoning.pdf) / [来源](https://arxiv.org/abs/2305.12744)
- **I050 GraphEval: A Knowledge-Graph Based LLM Hallucination Evaluation Framework** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I050_GraphEval_A_Knowledge_Graph_Based_LLM_Hallucination_Evaluation_Framework.pdf) / [来源](https://arxiv.org/abs/2407.10793)
- **I051 Hallucination Detection in LLMs with Topological Divergence on Attention Graphs** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I051_Hallucination_Detection_in_LLMs_with_Topological_Divergence_on_Attention_Graphs.pdf) / [来源](https://aclanthology.org/2026.acl-long.704/)
- **I052 INTRYGUE: Induction-Aware Entropy Gating for Reliable RAG Uncertainty Estimation** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I052_INTRYGUE_Induction_Aware_Entropy_Gating_for_Reliable_RAG_Uncertainty_Estimation.pdf) / [来源](https://arxiv.org/abs/2603.21607)
- **I053 InteGround: On the Evaluation of Verification and Retrieval Planning in Integrative Grounding** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I053_InteGround_On_the_Evaluation_of_Verification_and_Retrieval_Planning_in_Integrative_Grounding.pdf) / [来源](https://aclanthology.org/2025.findings-emnlp.732/)
- **I055 QuCo-RAG: Quantifying Uncertainty from the Pre-training Corpus for Dynamic Retrieval-Augmented Generation** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I055_QuCo_RAG_Quantifying_Uncertainty_from_the_Pre_training_Corpus_for_Dynamic_Retrieval_Augmented_Genera.pdf) / [来源](https://arxiv.org/abs/2512.19134)
- **I057 RAGAs: Automated Evaluation of Retrieval Augmented Generation** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I057_RAGAs_Automated_Evaluation_of_Retrieval_Augmented_Generation.pdf) / [来源](https://aclanthology.org/2024.eacl-demo.16/)
- **I058 Retrieving Supporting Evidence for LLMs Generated Answers** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I058_Retrieving_Supporting_Evidence_for_LLMs_Generated_Answers.pdf) / [来源](https://arxiv.org/abs/2306.13781)
- **I059 Self-Checker: Plug-and-Play Modules for Fact-Checking with Large Language Models** — 对应核心：C07;C09;C12；负责人：李瑾 / 程子晨。比较外部证据、检索质量与事实验证；关注忠实性和事实性是否分开。 [PDF](papers/important/I059_Self_Checker_Plug_and_Play_Modules_for_Fact_Checking_with_Large_Language_Models.pdf) / [来源](https://arxiv.org/abs/2305.14623)

### 自洽性、不确定性与内部信号（28篇）

- **I060 A Probabilistic Framework for LLM Hallucination Detection via Belief Tree Propagation** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I060_A_Probabilistic_Framework_for_LLM_Hallucination_Detection_via_Belief_Tree_Propagation.pdf) / [来源](https://aclanthology.org/2025.naacl-long.158/)
- **I061 A Stitch in Time Saves Nine: Detecting and Mitigating Hallucinations of LLMs by Validating Low-Confidence Generation** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I061_A_Stitch_in_Time_Saves_Nine_Detecting_and_Mitigating_Hallucinations_of_LLMs_by_Validating_Low_Confid.pdf) / [来源](https://arxiv.org/abs/2307.03987)
- **I063 Attention Satisfies: A Constraint-Satisfaction Lens on Factual Errors of Language Models** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I063_Attention_Satisfies_A_Constraint_Satisfaction_Lens_on_Factual_Errors_of_Language_Models.pdf) / [来源](https://arxiv.org/abs/2309.15098)
- **I064 Bold Claims or Self-Doubt? Factuality Hallucination Type Detection via Belief State** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I064_Bold_Claims_or_Self_Doubt_Factuality_Hallucination_Type_Detection_via_Belief_State.pdf) / [来源](https://aclanthology.org/2025.findings-emnlp.527/)
- **I066 Contextualized Sequence Likelihood: Enhanced Confidence Scores for Natural Language Generation** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I066_Contextualized_Sequence_Likelihood_Enhanced_Confidence_Scores_for_Natural_Language_Generation.pdf) / [来源](https://arxiv.org/abs/2406.01806)
- **I067 DRIFT: Detecting Representational Inconsistencies for Factual Truthfulness** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I067_DRIFT_Detecting_Representational_Inconsistencies_for_Factual_Truthfulness.pdf) / [来源](https://arxiv.org/abs/2601.14210)
- **I068 Distinguishing Ignorance from Error in LLM Hallucinations** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I068_Distinguishing_Ignorance_from_Error_in_LLM_Hallucinations.pdf) / [来源](https://arxiv.org/abs/2410.22071)
- **I069 Do Androids Know They're Only Dreaming of Electric Sheep?** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I069_Do_Androids_Know_They_re_Only_Dreaming_of_Electric_Sheep.pdf) / [来源](https://arxiv.org/abs/2312.17249)
- **I070 Do Language Models Know When They're Hallucinating References?** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I070_Do_Language_Models_Know_When_They_re_Hallucinating_References.pdf) / [来源](https://arxiv.org/abs/2305.18248)
- **I071 Do Not Design, Learn: A Trainable Scoring Function for Uncertainty Estimation in Generative LLMs** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I071_Do_Not_Design_Learn_A_Trainable_Scoring_Function_for_Uncertainty_Estimation_in_Generative_LLMs.pdf) / [来源](https://arxiv.org/abs/2406.11278)
- **I075 Generating with Confidence: Uncertainty Quantification for Black-box Large Language Models** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I075_Generating_with_Confidence_Uncertainty_Quantification_for_Black_box_Large_Language_Models.pdf) / [来源](https://arxiv.org/abs/2305.19187)
- **I076 Hallucination Detection in LLMs Using Spectral Features of Attention Maps** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I076_Hallucination_Detection_in_LLMs_Using_Spectral_Features_of_Attention_Maps.pdf) / [来源](https://arxiv.org/abs/2502.17598)
- **I077 How Language Model Hallucinations Can Snowball** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I077_How_Language_Model_Hallucinations_Can_Snowball.pdf) / [来源](https://arxiv.org/abs/2305.13534)
- **I078 ICRProbe: Tracking Hidden State Dynamics for Reliable Hallucination Detection in LLMs** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I078_ICRProbe_Tracking_Hidden_State_Dynamics_for_Reliable_Hallucination_Detection_in_LLMs.pdf) / [来源](https://aclanthology.org/2025.acl-long.880/)
- **I079 INSIDE: LLMs' Internal States Retain the Power of Hallucination Detection** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I079_INSIDE_LLMs_Internal_States_Retain_the_Power_of_Hallucination_Detection.pdf) / [来源](https://arxiv.org/abs/2402.03744)
- **I080 Joint Evaluation of Answer and Reasoning Consistency for Hallucination Detection in Large Reasoning Models** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I080_Joint_Evaluation_of_Answer_and_Reasoning_Consistency_for_Hallucination_Detection_in_Large_Reasoning_.pdf) / [来源](https://arxiv.org/abs/2506.04832)
- **I081 Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I081_Just_Ask_for_Calibration_Strategies_for_Eliciting_Calibrated_Confidence_Scores_from_Language_Models_.pdf) / [来源](https://arxiv.org/abs/2305.14975)
- **I082 Kernel Language Entropy: Fine-grained Uncertainty Quantification for LLMs from Semantic Similarities** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I082_Kernel_Language_Entropy_Fine_grained_Uncertainty_Quantification_for_LLMs_from_Semantic_Similarities.pdf) / [来源](https://arxiv.org/abs/2405.20003)
- **I083 Language Models (Mostly) Know What They Know** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I083_Language_Models_Mostly_Know_What_They_Know.pdf) / [来源](https://arxiv.org/abs/2207.05221)
- **I084 MARS: Meaning-Aware Response Scoring for Uncertainty Estimation in Generative LLMs** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I084_MARS_Meaning_Aware_Response_Scoring_for_Uncertainty_Estimation_in_Generative_LLMs.pdf) / [来源](https://aclanthology.org/2024.acl-long.419/)
- **I085 On Hallucination and Predictive Uncertainty in Conditional Language Generation** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I085_On_Hallucination_and_Predictive_Uncertainty_in_Conditional_Language_Generation.pdf) / [来源](https://aclanthology.org/2021.eacl-main.236/)
- **I087 Quantifying Uncertainty in Answers from any Language Model and Enhancing their Trustworthiness** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I087_Quantifying_Uncertainty_in_Answers_from_any_Language_Model_and_Enhancing_their_Trustworthiness.pdf) / [来源](https://aclanthology.org/2024.acl-long.283/)
- **I088 SAC3: Reliable Hallucination Detection in Black-Box Language Models via Semantic-aware Cross-check Consistency** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I088_SAC3_Reliable_Hallucination_Detection_in_Black_Box_Language_Models_via_Semantic_aware_Cross_check_Co.pdf) / [来源](https://arxiv.org/abs/2311.01740)
- **I090 Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I090_Semantic_Entropy_Probes_Robust_and_Cheap_Hallucination_Detection_in_LLMs.pdf) / [来源](https://arxiv.org/abs/2406.15927)
- **I091 Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I091_Semantic_Uncertainty_Linguistic_Invariances_for_Uncertainty_Estimation_in_Natural_Language_Generatio.pdf) / [来源](https://arxiv.org/abs/2302.09664)
- **I093 The Curious Case of Hallucinatory (Un)answerability: Finding Truths in the Hidden States of Over-Confident Large Language Models** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I093_The_Curious_Case_of_Hallucinatory_Un_answerability_Finding_Truths_in_the_Hidden_States_of_Over_Confi.pdf) / [来源](https://aclanthology.org/2023.emnlp-main.220/)
- **I094 The Internal State of an LLM Knows When It's Lying** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I094_The_Internal_State_of_an_LLM_Knows_When_It_s_Lying.pdf) / [来源](https://arxiv.org/abs/2304.13734)
- **I096 Uncertainty Quantification for Language Models: A Suite of Black-Box, White-Box, LLM Judge, and Ensemble Scorers** — 对应核心：C08;C10；负责人：杨桑多杰 / 程子晨。围绕自洽性和语义熵分析不确定性信号；注意自洽不代表事实正确。 [PDF](papers/important/I096_Uncertainty_Quantification_for_Language_Models_A_Suite_of_Black_Box_White_Box_LLM_Judge_and_Ensemble.pdf) / [来源](https://arxiv.org/abs/2504.19254)

### LLM裁判、人工评价与元评估（14篇）

- **I033 LLM-based NLG Evaluation: Current Status and Challenges** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。自动评估与人工判断一致性、评价协议和裁判偏差。 [PDF](papers/important/I033_LLM_based_NLG_Evaluation_Current_Status_and_Challenges.pdf) / [来源](https://aclanthology.org/2025.cl-2.9/)
- **I034 Multi-Dimensional Evaluation of Text Summarization with In-Context Learning** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。自动评估与人工判断一致性、评价协议和裁判偏差。 [PDF](papers/important/I034_Multi_Dimensional_Evaluation_of_Text_Summarization_with_In_Context_Learning.pdf) / [来源](https://arxiv.org/abs/2306.01200)
- **I037 SummEval: Re-evaluating Summarization Evaluation** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。自动评估与人工判断一致性、评价协议和裁判偏差。 [PDF](papers/important/I037_SummEval_Re_evaluating_Summarization_Evaluation.pdf) / [来源](https://aclanthology.org/2021.tacl-1.24/)
- **I065 ChatGPT as a Factual Inconsistency Evaluator for Text Summarization** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。自动评估与人工判断一致性、评价协议和裁判偏差。 [PDF](papers/important/I065_ChatGPT_as_a_Factual_Inconsistency_Evaluator_for_Text_Summarization.pdf) / [来源](https://arxiv.org/abs/2303.15621)
- **I097 Chainpoll: A high efficacy method for LLM hallucination detection** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。考察裁判偏差、人工一致性和跨模型元评估；不直接比较异构数据集分数。 [PDF](papers/important/I097_Chainpoll_A_high_efficacy_method_for_LLM_hallucination_detection.pdf) / [来源](https://arxiv.org/abs/2310.18344)
- **I100 G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。考察裁判偏差、人工一致性和跨模型元评估；不直接比较异构数据集分数。 [PDF](papers/important/I100_G_Eval_NLG_Evaluation_using_GPT_4_with_Better_Human_Alignment.pdf) / [来源](https://arxiv.org/abs/2303.16634)
- **I101 Human-like Summarization Evaluation with ChatGPT** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。考察裁判偏差、人工一致性和跨模型元评估；不直接比较异构数据集分数。 [PDF](papers/important/I101_Human_like_Summarization_Evaluation_with_ChatGPT.pdf) / [来源](https://arxiv.org/abs/2304.02554)
- **I102 Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。考察裁判偏差、人工一致性和跨模型元评估；不直接比较异构数据集分数。 [PDF](papers/important/I102_Judging_LLM_as_a_Judge_with_MT_Bench_and_Chatbot_Arena.pdf) / [来源](https://arxiv.org/abs/2306.05685)
- **I103 LLMs as Factual Reasoners: Insights from Existing Benchmarks and Beyond** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。考察裁判偏差、人工一致性和跨模型元评估；不直接比较异构数据集分数。 [PDF](papers/important/I103_LLMs_as_Factual_Reasoners_Insights_from_Existing_Benchmarks_and_Beyond.pdf) / [来源](https://arxiv.org/abs/2305.14540)
- **I104 LM vs LM: Detecting Factual Errors via Cross Examination** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。考察裁判偏差、人工一致性和跨模型元评估；不直接比较异构数据集分数。 [PDF](papers/important/I104_LM_vs_LM_Detecting_Factual_Errors_via_Cross_Examination.pdf) / [来源](https://arxiv.org/abs/2305.13281)
- **I105 Large Language Models are not Fair Evaluators** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。考察裁判偏差、人工一致性和跨模型元评估；不直接比较异构数据集分数。 [PDF](papers/important/I105_Large_Language_Models_are_not_Fair_Evaluators.pdf) / [来源](https://arxiv.org/abs/2305.17926)
- **I106 Lynx: An Open Source Hallucination Evaluation Model** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。考察裁判偏差、人工一致性和跨模型元评估；不直接比较异构数据集分数。 [PDF](papers/important/I106_Lynx_An_Open_Source_Hallucination_Evaluation_Model.pdf) / [来源](https://arxiv.org/abs/2407.08488)
- **I107 The Illusion of Progress: Re-evaluating Hallucination Detection in LLMs** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。考察裁判偏差、人工一致性和跨模型元评估；不直接比较异构数据集分数。 [PDF](papers/important/I107_The_Illusion_of_Progress_Re_evaluating_Hallucination_Detection_in_LLMs.pdf) / [来源](https://aclanthology.org/2025.emnlp-main.1761/)
- **I108 Why Does ChatGPT Fall Short in Providing Truthful Answers?** — 对应核心：C11;C14；负责人：杨桑多杰 / 张磊 / 程子晨。考察裁判偏差、人工一致性和跨模型元评估；不直接比较异构数据集分数。 [PDF](papers/important/I108_Why_Does_ChatGPT_Fall_Short_in_Providing_Truthful_Answers.pdf) / [来源](https://arxiv.org/abs/2304.10513)

### 中文、多语言与领域泛化（11篇）

- **I109 Detecting and Mitigating Hallucinations in Multilingual Summarisation** — 对应核心：C05;C06;C13；负责人：李瑾 / 张磊 / 程子晨。检验评估在中文、多语言或专业领域的适用边界。 [PDF](papers/important/I109_Detecting_and_Mitigating_Hallucinations_in_Multilingual_Summarisation.pdf) / [来源](https://arxiv.org/abs/2305.13632)
- **I110 Evaluating Hallucinations in Chinese Large Language Models** — 对应核心：C05;C06;C13；负责人：李瑾 / 张磊 / 程子晨。检验评估在中文、多语言或专业领域的适用边界。 [PDF](papers/important/I110_Evaluating_Hallucinations_in_Chinese_Large_Language_Models.pdf) / [来源](https://arxiv.org/abs/2310.03368)
- **I111 HalOmi: A Manually Annotated Benchmark for Multilingual Hallucination and Omission Detection in Machine Translation** — 对应核心：C05;C06;C13；负责人：李瑾 / 张磊 / 程子晨。检验评估在中文、多语言或专业领域的适用边界。 [PDF](papers/important/I111_HalOmi_A_Manually_Annotated_Benchmark_for_Multilingual_Hallucination_and_Omission_Detection_in_Machi.pdf) / [来源](https://arxiv.org/abs/2305.11746)
- **I112 Hallucinations in Large Multilingual Translation Models** — 对应核心：C05;C06;C13；负责人：李瑾 / 张磊 / 程子晨。检验评估在中文、多语言或专业领域的适用边界。 [PDF](papers/important/I112_Hallucinations_in_Large_Multilingual_Translation_Models.pdf) / [来源](https://arxiv.org/abs/2303.16104)
- **I113 Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models** — 对应核心：C05;C06;C13；负责人：李瑾 / 张磊 / 程子晨。检验评估在中文、多语言或专业领域的适用边界。 [PDF](papers/important/I113_Large_Legal_Fictions_Profiling_Legal_Hallucinations_in_Large_Language_Models.pdf) / [来源](https://arxiv.org/abs/2401.01301)
- **I114 Looking for a Needle in a Haystack: A Comprehensive Study of Hallucinations in Neural Machine Translation** — 对应核心：C05;C06;C13；负责人：李瑾 / 张磊 / 程子晨。检验评估在中文、多语言或专业领域的适用边界。 [PDF](papers/important/I114_Looking_for_a_Needle_in_a_Haystack_A_Comprehensive_Study_of_Hallucinations_in_Neural_Machine_Transla.pdf) / [来源](https://aclanthology.org/2023.eacl-main.75/)
- **I115 Med-HALT: Medical Domain Hallucination Test for Large Language Models** — 对应核心：C05;C06;C13；负责人：李瑾 / 张磊 / 程子晨。检验评估在中文、多语言或专业领域的适用边界。 [PDF](papers/important/I115_Med_HALT_Medical_Domain_Hallucination_Test_for_Large_Language_Models.pdf) / [来源](https://arxiv.org/abs/2307.15343)
- **I116 MedHallu: A Comprehensive Benchmark for Detecting Medical Hallucinations in Large Language Models** — 对应核心：C05;C06;C13；负责人：李瑾 / 张磊 / 程子晨。检验评估在中文、多语言或专业领域的适用边界。 [PDF](papers/important/I116_MedHallu_A_Comprehensive_Benchmark_for_Detecting_Medical_Hallucinations_in_Large_Language_Models.pdf) / [来源](https://arxiv.org/abs/2502.14302)
- **I117 MultiHal: Multilingual Dataset for Knowledge-Graph Grounded Evaluation of LLM Hallucinations** — 对应核心：C05;C06;C13；负责人：李瑾 / 张磊 / 程子晨。检验评估在中文、多语言或专业领域的适用边界。 [PDF](papers/important/I117_MultiHal_Multilingual_Dataset_for_Knowledge_Graph_Grounded_Evaluation_of_LLM_Hallucinations.pdf) / [来源](https://arxiv.org/abs/2505.14101)
- **I118 Optimal Transport for Unsupervised Hallucination Detection in Neural Machine Translation** — 对应核心：C05;C06;C13；负责人：李瑾 / 张磊 / 程子晨。检验评估在中文、多语言或专业领域的适用边界。 [PDF](papers/important/I118_Optimal_Transport_for_Unsupervised_Hallucination_Detection_in_Neural_Machine_Translation.pdf) / [来源](https://arxiv.org/abs/2212.09631)
- **I119 When Models Lie, We Learn: Multilingual Span-Level Hallucination Detection with PsiloQA** — 对应核心：C05;C06;C13；负责人：李瑾 / 张磊 / 程子晨。检验评估在中文、多语言或专业领域的适用边界。 [PDF](papers/important/I119_When_Models_Lie_We_Learn_Multilingual_Span_Level_Hallucination_Detection_with_PsiloQA.pdf) / [来源](https://arxiv.org/abs/2510.04849)

## 全体成员的交付标准

程子晨参与并负责所有研究方面，组织分类讨论、证据核查和总稿整合。每位成员先从其负责方向选择4–6篇精读，再扩展阅读；所有结论必须记录论文页码、实验条件和证据。每篇阅读笔记应包括：定义、任务、粒度、证据来源、方法机制、基准、人工一致性、泛化性、成本、局限及可复现资源。未读出的信息写“未报告/待确认”，不要据标题补造结论。

源码用于理解方法和按需复现实验，Track A不要求训练全部模型。源码快照均未运行，不包含额外模型权重和外部数据下载；依赖与许可证以各原仓库为准。