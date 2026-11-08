# 124篇文献的技术分类（16 core + 108 important）

## 分类原则

主类沿用计划书的五条评价技术线：H 人工评价、E 参考/证据核验、T 判别器/蕴含/内部表征、U 自一致性/不确定性、J LLM 裁判。T 类包含训练探针、NLI 评价器，以及基于内部表征/注意力的异常判别；它们的监督要求另见逐篇笔记。
每篇最多一个**技术主类**，可以有多个技术次类。`—`表示论文的主要贡献是基准、综述、元评估或现象分析，不能仅凭论文使用了某种基线就说它提出了该方法。
另用“研究角色”和“评价对象”两个正交轴防止概念混淆。特别是来源忠实性不等于世界事实性；论文标题中的“hallucination”也不自动意味着相同的标注构念。
分类依据是逐篇阅读笔记及原文；技术次类只记录重要交叉，不能理解为该论文覆盖该类全部方法。

## 总览

共 124 篇：core 16 篇、important 108 篇。技术主类：H 人工评价 2 篇；E 参考/证据核验 20 篇；T 判别器/蕴含/内部表征 27 篇；U 自一致性/不确定性 27 篇；J LLM 裁判 8 篇；— 无单一方法主类 40 篇。
技术次类（可重叠）：H 35 篇；E 32 篇；T 26 篇；U 15 篇；J 41 篇。主类与次类不能直接相加当作互斥论文数。
研究角色：综述/概念 9 篇；基准/数据 20 篇；评价方法 80 篇；元评估/审计 8 篇；领域实证/现象分析 7 篇。

## 五类技术的判断标准

- **H 人工评价**：人工定义、标注、评分和人际一致性；人工标签用作基准金标时仅记为次类。
- **E 参考/证据核验**：将输出拆为声明、实体、关系或问答，依据源文、检索证据或知识图谱判断支持性。
- **T 判别器/蕴含/内部表征**：使用训练的事实性判别器、NLI 模型，或隐藏状态与注意力等内部特征建立检测分数。
- **U 自一致性/不确定性**：跨采样语义一致性、置信度、概率、熵、校准以及动态拒答风险。
- **J LLM 裁判**：让通用大模型依据提示、评分规则或交叉询问判定事实性或忠实性。

## 16篇核心论文速查

- [C01](notes/core/C01_NLG_Hallucination_Survey.md) Survey of Hallucination in Natural Language Generation — 综述/概念；技术主类 —，次类 无。
- [C02](notes/core/C02_LLM_Hallucination_Taxonomy.md) A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions — 综述/概念；技术主类 —，次类 无。
- [C03](notes/core/C03_Sirens_Song.md) Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models — 综述/概念；技术主类 —，次类 无。
- [C04](notes/core/C04_Automatic_Evaluation_Survey.md) A Survey of Automatic Hallucination Evaluation on Natural Language Generation — 综述/概念；技术主类 —，次类 无。
- [C05](notes/core/C05_TruthfulQA.md) TruthfulQA: Measuring How Models Mimic Human Falsehoods — 基准/数据；技术主类 —，次类 T;J;H。
- [C06](notes/core/C06_HaluEval.md) HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models — 基准/数据；技术主类 —，次类 H;J。
- [C07](notes/core/C07_FActScore.md) FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation — 评价方法；技术主类 E，次类 J。
- [C08](notes/core/C08_SelfCheckGPT.md) SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models — 评价方法；技术主类 U，次类 T;J。
- [C09](notes/core/C09_AlignScore.md) AlignScore: Evaluating Factual Consistency with a Unified Alignment Function — 评价方法；技术主类 T，次类 E。
- [C10](notes/core/C10_Semantic_Entropy.md) Detecting hallucinations in large language models using semantic entropy — 评价方法；技术主类 U，次类 无。
- [C11](notes/core/C11_TRUE.md) TRUE: Re-evaluating Factual Consistency Evaluation — 元评估/审计；技术主类 —，次类 E;T。
- [C12](notes/core/C12_RAGTruth.md) RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models — 基准/数据；技术主类 —，次类 T;H。
- [C13](notes/core/C13_FELM.md) FELM: Benchmarking Factuality Evaluation of Large Language Models — 基准/数据；技术主类 —，次类 E;J;H。
- [C14](notes/core/C14_Human_Evaluation_Survey.md) Do My Eyes Deceive Me? A Survey of Human Evaluations of Hallucinations in NLG — 综述/概念；技术主类 H，次类 J。
- [C15](notes/core/C15_Hallucination_Audit.md) An Audit on the Perspectives and Challenges of Hallucinations in NLP — 综述/概念；技术主类 —，次类 无。
- [C16](notes/core/C16_Defining_Hallucination.md) The Pitfalls of Defining Hallucination — 综述/概念；技术主类 —，次类 无。

## 分类清单

### H · 人工评价（2篇）

格式：ID〔core/important；研究角色；评价对象；次类〕标题。每条链接通向对应精读笔记。

- [C14](notes/core/C14_Human_Evaluation_Survey.md)〔core；综述/概念；跨目标或概念研究；次类 J〕Do My Eyes Deceive Me? A Survey of Human Evaluations of Hallucinations in NLG
- [I037](notes/important/I037_SummEval.md)〔important；元评估/审计；来源忠实性；次类 E;T;J〕SummEval: Re-evaluating Summarization Evaluation

### E · 参考/证据核验（20篇）

格式：ID〔core/important；研究角色；评价对象；次类〕标题。每条链接通向对应精读笔记。

- [C07](notes/core/C07_FActScore.md)〔core；评价方法；外部事实性/正确性；次类 J〕FActScore: Fine-grained Atomic Evaluation of Factual Precision in Long Form Text Generation
- [I005](notes/important/I005_ETF.md)〔important；评价方法；来源忠实性；次类 J;H〕ETF: An Entity Tracing Framework for Hallucination Detection in Code Summaries
- [I006](notes/important/I006_ENOKI.md)〔important；评价方法；来源忠实性；次类 T;J〕Enoki: Efficient Multi-Level Hallucination Detection
- [I015](notes/important/I015_EntFA_Factual_Hallucination.md)〔important；评价方法；来源忠实性；次类 H〕Hallucinated but Factual! Inspecting the Factuality of Hallucinations in Abstractive Summarization
- [I029](notes/important/I029_CONNER_Beyond_Factuality.md)〔important；评价方法；外部事实性/正确性；次类 J〕Beyond Factuality: A Comprehensive Evaluation of Large Language Models as Knowledge Generators
- [I032](notes/important/I032_FACTOOL.md)〔important；评价方法；外部事实性/正确性；次类 J〕FacTool: Factuality Detection in Generative AI -- A Tool Augmented Framework for Multi-Task and Multi-Domain Scenarios
- [I041](notes/important/I041_Correctness_and_Faithfulness_QA.md)〔important；评价方法；跨目标或概念研究；次类 J;H〕Evaluating Correctness and Faithfulness of Instruction-Following Models for Question Answering
- [I042](notes/important/I042_FEQA.md)〔important；评价方法；来源忠实性；次类 无〕FEQA: A Question Answering Evaluation Framework for Faithfulness Assessment in Abstractive Summarization
- [I043](notes/important/I043_QuestEval.md)〔important；评价方法；来源忠实性；次类 T〕QuestEval: Summarization Asks for Fact-based Evaluation
- [I046](notes/important/I046_Complex_Claim_Verification_with_Evidence_Retrieved_in_the_Wild.md)〔important；评价方法；外部事实性/正确性；次类 J〕Complex Claim Verification with Evidence Retrieved in the Wild
- [I047](notes/important/I047_FACTKG.md)〔important；评价方法；外部事实性/正确性；次类 T〕FactKG: Fact Verification via Reasoning on Knowledge Graphs
- [I048](notes/important/I048_ProgramFC.md)〔important；评价方法；外部事实性/正确性；次类 J〕Fact-Checking Complex Claims with Program-Guided Reasoning
- [I050](notes/important/I050_GraphEval.md)〔important；评价方法；外部事实性/正确性；次类 J〕GraphEval: A Knowledge-Graph Based LLM Hallucination Evaluation Framework
- [I054](notes/important/I054_Q_Squared.md)〔important；评价方法；来源忠实性；次类 T〕Q2: Evaluating Factual Consistency in Knowledge-Grounded Dialogues via Question Generation and Question Answering
- [I057](notes/important/I057_RAGAs.md)〔important；评价方法；来源忠实性；次类 J〕RAGAs: Automated Evaluation of Retrieval Augmented Generation
- [I058](notes/important/I058_Retrieving_Supporting_Evidence_for_LLMs_Generated_Answers.md)〔important；评价方法；外部事实性/正确性；次类 J〕Retrieving Supporting Evidence for LLMs Generated Answers
- [I059](notes/important/I059_Self_Checker.md)〔important；评价方法；外部事实性/正确性；次类 J〕Self-Checker: Plug-and-Play Modules for Fact-Checking with Large Language Models
- [I062](notes/important/I062_QAGS.md)〔important；评价方法；来源忠实性；次类 无〕Asking and Answering Questions to Evaluate the Factual Consistency of Summaries
- [I072](notes/important/I072_Entity_Level_Consistency.md)〔important；评价方法；来源忠实性；次类 无〕Entity-level Factual Consistency of Abstractive Text Summarization
- [I086](notes/important/I086_QAFactEval.md)〔important；评价方法；来源忠实性；次类 T〕QAFactEval: Improved QA-Based Factual Consistency Evaluation for Summarization

### T · 判别器/蕴含/内部表征（27篇）

格式：ID〔core/important；研究角色；评价对象；次类〕标题。每条链接通向对应精读笔记。

- [C09](notes/core/C09_AlignScore.md)〔core；评价方法；来源忠实性；次类 E〕AlignScore: Evaluating Factual Consistency with a Unified Alignment Function
- [I016](notes/important/I016_Embedding_Distance.md)〔important；评价方法；外部事实性/正确性；次类 U〕Hallucination Detection: A Probabilistic Framework Using Embeddings Distance Analysis
- [I017](notes/important/I017_HALO_HaloCheck.md)〔important；评价方法；外部事实性/正确性；次类 U〕Halo: Estimation and Reduction of Hallucinations in Open-Source Weak Large Language Models
- [I019](notes/important/I019_RL4HS.md)〔important；评价方法；外部事实性/正确性；次类 J〕Learning to Reason for Hallucination Span Detection
- [I023](notes/important/I023_Teaching_with_Lies.md)〔important；评价方法；外部事实性/正确性；次类 J〕Teaching with Lies: Curriculum DPO on Synthetic Negatives for Hallucination Detection
- [I026](notes/important/I026_FACTCHECKMATE.md)〔important；评价方法；外部事实性/正确性；次类 U〕FactCheckmate: Preemptively Detecting and Mitigating Hallucinations in LMs
- [I027](notes/important/I027_Adversarial_NLI.md)〔important；评价方法；来源忠实性；次类 E〕Adversarial NLI for Factual Correctness in Text Summarisation Models
- [I031](notes/important/I031_Dependency_Arc_Entailment.md)〔important；评价方法；来源忠实性；次类 E〕Evaluating Factuality in Generation with Dependency-level Entailment
- [I036](notes/important/I036_NLI_Summary_Ranking.md)〔important；元评估/审计；来源忠实性；次类 E;H〕Ranking Generated Summaries by Correctness: An Interesting but Challenging Application for Natural Language Inference
- [I044](notes/important/I044_ARES.md)〔important；评价方法；来源忠实性；次类 E;J;H〕ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems
- [I051](notes/important/I051_TOHA.md)〔important；评价方法；外部事实性/正确性；次类 U〕Hallucination Detection in LLMs with Topological Divergence on Attention Graphs
- [I063](notes/important/I063_Attention_Satisfies.md)〔important；评价方法；外部事实性/正确性；次类 无〕Attention Satisfies: A Constraint-Satisfaction Lens on Factual Errors of Language Models
- [I067](notes/important/I067_DRIFT.md)〔important；评价方法；外部事实性/正确性；次类 U〕DRIFT: Detecting Representational Inconsistencies for Factual Truthfulness
- [I069](notes/important/I069_Do_Androids_Know.md)〔important；评价方法；外部事实性/正确性；次类 U〕Do Androids Know They're Only Dreaming of Electric Sheep?
- [I073](notes/important/I073_FactCC.md)〔important；评价方法；来源忠实性；次类 E〕Evaluating the Factual Consistency of Abstractive Text Summarization
- [I074](notes/important/I074_SCALE_Long_Documents.md)〔important；评价方法；来源忠实性；次类 E〕Fast and Accurate Factual Inconsistency Detection Over Long Documents
- [I076](notes/important/I076_LapEigvals.md)〔important；评价方法；外部事实性/正确性；次类 U〕Hallucination Detection in LLMs Using Spectral Features of Attention Maps
- [I078](notes/important/I078_ICR_Probe.md)〔important；评价方法；外部事实性/正确性；次类 U〕ICRProbe: Tracking Hidden State Dynamics for Reliable Hallucination Detection in LLMs
- [I090](notes/important/I090_Semantic_Entropy_Probes.md)〔important；评价方法；外部事实性/正确性；次类 U〕Semantic Entropy Probes: Robust and Cheap Hallucination Detection in LLMs
- [I092](notes/important/I092_SummaC.md)〔important；评价方法；来源忠实性；次类 E〕SummaC: Re-Visiting NLI-based Models for Inconsistency Detection in Summarization
- [I093](notes/important/I093_Hallucinatory_Unanswerability.md)〔important；评价方法；外部事实性/正确性；次类 U〕The Curious Case of Hallucinatory (Un)answerability: Finding Truths in the Hidden States of Over-Confident Large Language Models
- [I094](notes/important/I094_Internal_State_Knows.md)〔important；评价方法；外部事实性/正确性；次类 U〕The Internal State of an LLM Knows When It's Lying
- [I095](notes/important/I095_TrueTeacher.md)〔important；评价方法；来源忠实性；次类 J〕TrueTeacher: Learning Factual Consistency Evaluation with Large Language Models
- [I106](notes/important/I106_Lynx_HaluBench.md)〔important；评价方法；来源忠实性；次类 J;E〕Lynx: An Open Source Hallucination Evaluation Model
- [I109](notes/important/I109_mFACT_Multilingual_Summarisation.md)〔important；评价方法；来源忠实性；次类 E〕Detecting and Mitigating Hallucinations in Multilingual Summarisation
- [I118](notes/important/I118_Optimal_Transport_Attention.md)〔important；评价方法；来源忠实性；次类 无〕Optimal Transport for Unsupervised Hallucination Detection in Neural Machine Translation
- [I119](notes/important/I119_PsiloQA.md)〔important；评价方法；来源忠实性；次类 H〕When Models Lie, We Learn: Multilingual Span-Level Hallucination Detection with PsiloQA

### U · 自一致性/不确定性（27篇）

格式：ID〔core/important；研究角色；评价对象；次类〕标题。每条链接通向对应精读笔记。

- [C08](notes/core/C08_SelfCheckGPT.md)〔core；评价方法；外部事实性/正确性；次类 T;J〕SelfCheckGPT: Zero-Resource Black-Box Hallucination Detection for Generative Large Language Models
- [C10](notes/core/C10_Semantic_Entropy.md)〔core；评价方法；外部事实性/正确性；次类 无〕Detecting hallucinations in large language models using semantic entropy
- [I002](notes/important/I002_PHD_Reverse_Validation.md)〔important；评价方法；外部事实性/正确性；次类 E〕A New Benchmark and Reverse Validation Method for Passage-level Hallucination Detection
- [I020](notes/important/I020_Monitoring_Decoding.md)〔important；评价方法；外部事实性/正确性；次类 J;E〕Monitoring Decoding: Mitigating Hallucination via Evaluating the Factuality of Partial Response during Generation
- [I022](notes/important/I022_Self_Contradictory_Hallucinations.md)〔important；评价方法；外部事实性/正确性；次类 J〕Self-contradictory Hallucinations of Large Language Models: Evaluation, Detection and Mitigation
- [I045](notes/important/I045_Can_LLMs_Express_Their_Uncertainty.md)〔important；评价方法；外部事实性/正确性；次类 无〕Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs
- [I052](notes/important/I052_INTRYGUE.md)〔important；评价方法；跨目标或概念研究；次类 E〕INTRYGUE: Induction-Aware Entropy Gating for Reliable RAG Uncertainty Estimation
- [I055](notes/important/I055_QuCo_RAG.md)〔important；评价方法；跨目标或概念研究；次类 E〕QuCo-RAG: Quantifying Uncertainty from the Pre-training Corpus for Dynamic Retrieval-Augmented Generation
- [I060](notes/important/I060_BTProp.md)〔important；评价方法；外部事实性/正确性；次类 E〕A Probabilistic Framework for LLM Hallucination Detection via Belief Tree Propagation
- [I061](notes/important/I061_Stitch_in_Time.md)〔important；评价方法；外部事实性/正确性；次类 E〕A Stitch in Time Saves Nine: Detecting and Mitigating Hallucinations of LLMs by Validating Low-Confidence Generation
- [I064](notes/important/I064_Bold_Claims_or_Self_Doubt.md)〔important；评价方法；外部事实性/正确性；次类 T〕Bold Claims or Self-Doubt? Factuality Hallucination Type Detection via Belief State
- [I066](notes/important/I066_Contextualized_Sequence_Likelihood.md)〔important；评价方法；外部事实性/正确性；次类 E〕Contextualized Sequence Likelihood: Enhanced Confidence Scores for Natural Language Generation
- [I068](notes/important/I068_Distinguishing_Ignorance_from_Error.md)〔important；领域实证/现象分析；外部事实性/正确性；次类 T〕Distinguishing Ignorance from Error in LLM Hallucinations
- [I070](notes/important/I070_Hallucinating_References.md)〔important；评价方法；外部事实性/正确性；次类 T〕Do Language Models Know When They're Hallucinating References?
- [I071](notes/important/I071_LARS.md)〔important；评价方法；外部事实性/正确性；次类 T〕Do Not Design, Learn: A Trainable Scoring Function for Uncertainty Estimation in Generative LLMs
- [I075](notes/important/I075_Generating_with_Confidence.md)〔important；评价方法；外部事实性/正确性；次类 无〕Generating with Confidence: Uncertainty Quantification for Black-box Large Language Models
- [I079](notes/important/I079_INSIDE.md)〔important；评价方法；外部事实性/正确性；次类 T〕INSIDE: LLMs' Internal States Retain the Power of Hallucination Detection
- [I080](notes/important/I080_RACE.md)〔important；评价方法；外部事实性/正确性；次类 T〕Joint Evaluation of Answer and Reasoning Consistency for Hallucination Detection in Large Reasoning Models
- [I081](notes/important/I081_Just_Ask_for_Calibration.md)〔important；评价方法；外部事实性/正确性；次类 无〕Just Ask for Calibration: Strategies for Eliciting Calibrated Confidence Scores from Language Models Fine-Tuned with Human Feedback
- [I082](notes/important/I082_Kernel_Language_Entropy.md)〔important；评价方法；外部事实性/正确性；次类 T〕Kernel Language Entropy: Fine-grained Uncertainty Quantification for LLMs from Semantic Similarities
- [I083](notes/important/I083_PTrue_PIK.md)〔important；评价方法；外部事实性/正确性；次类 无〕Language Models (Mostly) Know What They Know
- [I084](notes/important/I084_MARS.md)〔important；评价方法；外部事实性/正确性；次类 无〕MARS: Meaning-Aware Response Scoring for Uncertainty Estimation in Generative LLMs
- [I085](notes/important/I085_Hallucination_Predictive_Uncertainty.md)〔important；评价方法；外部事实性/正确性；次类 E〕On Hallucination and Predictive Uncertainty in Conditional Language Generation
- [I087](notes/important/I087_BSDetector.md)〔important；评价方法；外部事实性/正确性；次类 J〕Quantifying Uncertainty in Answers from any Language Model and Enhancing their Trustworthiness
- [I088](notes/important/I088_SAC3.md)〔important；评价方法；外部事实性/正确性；次类 J〕SAC3: Reliable Hallucination Detection in Black-Box Language Models via Semantic-aware Cross-check Consistency
- [I091](notes/important/I091_Semantic_Uncertainty.md)〔important；评价方法；外部事实性/正确性；次类 无〕Semantic Uncertainty: Linguistic Invariances for Uncertainty Estimation in Natural Language Generation
- [I096](notes/important/I096_UQLM_Suite.md)〔important；评价方法；外部事实性/正确性；次类 J;T〕Uncertainty Quantification for Language Models: A Suite of Black-Box, White-Box, LLM Judge, and Ensemble Scorers

### J · LLM 裁判（8篇）

格式：ID〔core/important；研究角色；评价对象；次类〕标题。每条链接通向对应精读笔记。

- [I010](notes/important/I010_FAVA.md)〔important；评价方法；外部事实性/正确性；次类 H〕Fine-grained Hallucination Detection and Editing for Language Models
- [I018](notes/important/I018_LLM_Fact_Verification.md)〔important；评价方法；外部事实性/正确性；次类 E〕Language Models Hallucinate, but May Excel at Fact Verification
- [I034](notes/important/I034_ICE.md)〔important；评价方法；来源忠实性；次类 H〕Multi-Dimensional Evaluation of Text Summarization with In-Context Learning
- [I065](notes/important/I065_ChatGPT_Factual_Inconsistency.md)〔important；评价方法；来源忠实性；次类 H〕ChatGPT as a Factual Inconsistency Evaluator for Text Summarization
- [I097](notes/important/I097_ChainPoll.md)〔important；评价方法；外部事实性/正确性；次类 U〕Chainpoll: A high efficacy method for LLM hallucination detection
- [I100](notes/important/I100_G_Eval.md)〔important；评价方法；跨目标或概念研究；次类 H〕G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment
- [I101](notes/important/I101_Humanlike_Summarization_Evaluation.md)〔important；评价方法；来源忠实性；次类 H〕Human-like Summarization Evaluation with ChatGPT
- [I104](notes/important/I104_LM_vs_LM.md)〔important；评价方法；外部事实性/正确性；次类 U〕LM vs LM: Detecting Factual Errors via Cross Examination

### — · 无单一方法主类（40篇）

格式：ID〔core/important；研究角色；评价对象；次类〕标题。每条链接通向对应精读笔记。

- [C01](notes/core/C01_NLG_Hallucination_Survey.md)〔core；综述/概念；跨目标或概念研究；次类 无〕Survey of Hallucination in Natural Language Generation
- [C02](notes/core/C02_LLM_Hallucination_Taxonomy.md)〔core；综述/概念；跨目标或概念研究；次类 无〕A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions
- [C03](notes/core/C03_Sirens_Song.md)〔core；综述/概念；跨目标或概念研究；次类 无〕Siren's Song in the AI Ocean: A Survey on Hallucination in Large Language Models
- [C04](notes/core/C04_Automatic_Evaluation_Survey.md)〔core；综述/概念；跨目标或概念研究；次类 无〕A Survey of Automatic Hallucination Evaluation on Natural Language Generation
- [C05](notes/core/C05_TruthfulQA.md)〔core；基准/数据；外部事实性/正确性；次类 T;J;H〕TruthfulQA: Measuring How Models Mimic Human Falsehoods
- [C06](notes/core/C06_HaluEval.md)〔core；基准/数据；跨目标或概念研究；次类 H;J〕HaluEval: A Large-Scale Hallucination Evaluation Benchmark for Large Language Models
- [C11](notes/core/C11_TRUE.md)〔core；元评估/审计；来源忠实性；次类 E;T〕TRUE: Re-evaluating Factual Consistency Evaluation
- [C12](notes/core/C12_RAGTruth.md)〔core；基准/数据；来源忠实性；次类 T;H〕RAGTruth: A Hallucination Corpus for Developing Trustworthy Retrieval-Augmented Language Models
- [C13](notes/core/C13_FELM.md)〔core；基准/数据；外部事实性/正确性；次类 E;J;H〕FELM: Benchmarking Factuality Evaluation of Large Language Models
- [C15](notes/core/C15_Hallucination_Audit.md)〔core；综述/概念；跨目标或概念研究；次类 无〕An Audit on the Perspectives and Challenges of Hallucinations in NLP
- [C16](notes/core/C16_Defining_Hallucination.md)〔core；综述/概念；跨目标或概念研究；次类 无〕The Pitfalls of Defining Hallucination
- [I001](notes/important/I001_Factuality_Survey.md)〔important；综述/概念；跨目标或概念研究；次类 无〕Factuality of Large Language Models: A Survey
- [I003](notes/important/I003_HADES.md)〔important；基准/数据；来源忠实性；次类 H;T〕A Token-level Reference-free Hallucination Detection Benchmark for Free-form Text Generation
- [I004](notes/important/I004_BAMBOO.md)〔important；基准/数据；来源忠实性；次类 无〕BAMBOO: A Comprehensive Benchmark for Evaluating Long Text Modeling Capacities of Large Language Models
- [I007](notes/important/I007_FRANK.md)〔important；元评估/审计；来源忠实性；次类 H;E;T〕FRANK: A Benchmark for Factuality Metrics
- [I008](notes/important/I008_FactCHD.md)〔important；基准/数据；外部事实性/正确性；次类 T;J;H〕FactCHD: Benchmarking Fact-Conflicting Hallucination Detection
- [I011](notes/important/I011_FreshLLMs_FreshQA.md)〔important；基准/数据；外部事实性/正确性；次类 E;J;H〕FreshLLMs: Refreshing Large Language Models with Search Engine Augmentation
- [I012](notes/important/I012_FACTOR.md)〔important；基准/数据；外部事实性/正确性；次类 U;E〕Generating Benchmarks for Factuality Evaluation of Language Models
- [I013](notes/important/I013_HALoGEN.md)〔important；基准/数据；外部事实性/正确性；次类 E;J;H〕HALoGEN: Fantastic LLM Hallucinations and Where to Find Them
- [I014](notes/important/I014_HalluLens.md)〔important；基准/数据；外部事实性/正确性；次类 J;H〕HalluLens: LLM Hallucination Benchmark
- [I021](notes/important/I021_RealTime_QA.md)〔important；基准/数据；外部事实性/正确性；次类 无〕RealTime QA: What's the Answer Right Now?
- [I024](notes/important/I024_Dawn_After_Dark.md)〔important；领域实证/现象分析；外部事实性/正确性；次类 无〕The Dawn After the Dark: An Empirical Study on Factuality Hallucination in Large Language Models
- [I033](notes/important/I033_LLM_based_NLG_Evaluation.md)〔important；综述/概念；跨目标或概念研究；次类 无〕LLM-based NLG Evaluation: Current Status and Challenges
- [I035](notes/important/I035_Faithfulness_and_Factuality.md)〔important；领域实证/现象分析；来源忠实性；次类 H;E;T〕On Faithfulness and Factuality in Abstractive Summarization
- [I040](notes/important/I040_Unanswerable_Beyond_SQuAD.md)〔important；基准/数据；外部事实性/正确性；次类 H;T〕Do We Know What We Don’t Know? Studying Unanswerable Questions beyond SQuAD 2.0
- [I053](notes/important/I053_InteGround.md)〔important；基准/数据；跨目标或概念研究；次类 E;J〕InteGround: On the Evaluation of Verification and Retrieval Planning in Integrative Grounding
- [I077](notes/important/I077_Hallucination_Snowballing.md)〔important；领域实证/现象分析；外部事实性/正确性；次类 U〕How Language Model Hallucinations Can Snowball
- [I102](notes/important/I102_MTBench_Chatbot_Arena_Judges.md)〔important；元评估/审计；跨目标或概念研究；次类 J;H〕Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena
- [I103](notes/important/I103_SummEdits_Factual_Reasoners.md)〔important；元评估/审计；来源忠实性；次类 J;E〕LLMs as Factual Reasoners: Insights from Existing Benchmarks and Beyond
- [I105](notes/important/I105_FairEval.md)〔important；元评估/审计；跨目标或概念研究；次类 J;H〕Large Language Models are not Fair Evaluators
- [I107](notes/important/I107_Illusion_of_Progress.md)〔important；元评估/审计；外部事实性/正确性；次类 T;J;H〕The Illusion of Progress: Re-evaluating Hallucination Detection in LLMs
- [I108](notes/important/I108_Why_ChatGPT_Falls_Short_Truthful_Answers.md)〔important；领域实证/现象分析；外部事实性/正确性；次类 H;E〕Why Does ChatGPT Fall Short in Providing Truthful Answers?
- [I110](notes/important/I110_HalluQA_Chinese_LLMs.md)〔important；基准/数据；外部事实性/正确性；次类 J;H〕Evaluating Hallucinations in Chinese Large Language Models
- [I111](notes/important/I111_HalOmi_Multilingual_MT.md)〔important；基准/数据；来源忠实性；次类 H;T〕HalOmi: A Manually Annotated Benchmark for Multilingual Hallucination and Omission Detection in Machine Translation
- [I112](notes/important/I112_Large_Multilingual_Translation_Hallucinations.md)〔important；领域实证/现象分析；来源忠实性；次类 H〕Hallucinations in Large Multilingual Translation Models
- [I113](notes/important/I113_Large_Legal_Fictions.md)〔important；领域实证/现象分析；外部事实性/正确性；次类 H;E〕Large Legal Fictions: Profiling Legal Hallucinations in Large Language Models
- [I114](notes/important/I114_Needle_Haystack_NMT.md)〔important；基准/数据；来源忠实性；次类 H;T〕Looking for a Needle in a Haystack: A Comprehensive Study of Hallucinations in Neural Machine Translation
- [I115](notes/important/I115_Med_HALT.md)〔important；基准/数据；外部事实性/正确性；次类 J;H〕Med-HALT: Medical Domain Hallucination Test for Large Language Models
- [I116](notes/important/I116_MedHallu.md)〔important；基准/数据；外部事实性/正确性；次类 J;H〕MedHallu: A Comprehensive Benchmark for Detecting Medical Hallucinations in Large Language Models
- [I117](notes/important/I117_MultiHal.md)〔important；基准/数据；外部事实性/正确性；次类 E;J;H〕MultiHal: Multilingual Dataset for Knowledge-Graph Grounded Evaluation of LLM Hallucinations

## 使用与边界

- 建议论文正文用“研究角色 × 五类技术 × 评价对象”的三层结构组织综述，而不是把所有基准强行算作方法。
- 主类是为了统计和排版作出的主贡献判定；跨类论文须同时查看“次类”，例如 FActScore（E+J）、SelfCheckGPT（U+T/J）、ARES（T+E/J）。
- 类别是研究地图，不代表复现完成或各论文主张已经由本组独立验证。具体数据、局限与待核查点见对应精读笔记。
