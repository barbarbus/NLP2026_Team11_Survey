# C02 · A Survey on Hallucination in Large Language Models: Principles, Taxonomy, Challenges, and Open Questions

Lei Huang等，ACM TOIS，DOI10.1145/3703155；https://arxiv.org/abs/2311.05232 。本地arXiv v2（2024-11-19）58页，页脚January2024不能替代实际版本日期。

## 阅读与核查范围

已细读正文第1–34页，包含定义、成因、检测/基准、缓解、RAG失败和未来讨论。第34–58页为参考文献，不将其中被引研究计作已读。已渲染并目视核查第6、17页案例表与基准表。本文没有自己的统一模型实验；本笔记对C05/C06/C08/C13条目进行了已读原始论文交叉核验，无新的模型运行。

## 1. 贡献定位

本文将LLM幻觉分为factuality与faithfulness，按data/training/inference梳理成因及缓解，并单独详细分析RAG。这是组织框架贡献，不是发明一种可计算、已验证完备且互斥的误差分类。它面向开放LLM及信息检索应用，比C01早期任务分节更关注知识边界和端到端检索系统。

第3页比较旧综述时称Ji等不讨论LLM，但本地C01 v7已新增完整LLM章节，说明综述间的比较同样受引用版本限制。最终相关工作应比较具体版本，不能机械复述该优劣关系。

## 2. 事实性与忠实性的细分

事实性：factual contradiction又分entity-error与relation-error；factual fabrication分unverifiability与overclaim。忠实性：instruction inconsistency、context inconsistency、logical inconsistency（第5–7页）。指令不一致特指非恶意指令的非预期偏离，不将遵循安全约束的拒答一律称为幻觉。

这个体系有助于说明“答错事实”“答非所问”“来源冲突”“推理自相矛盾”分别是什么，但不同轴仍可重叠：一个数字同时与来源和世界事实矛盾；推理链内部不一致也可导致事实错误。需要多标签或主次定义，不应强行将每个错误归入唯一叶节点。

“不可核验”与“完全不存在”被同列unverifiability并非认识论同义：查不到证据可能是证据覆盖不足。Overclaim缺少广泛共识也不总是已经证伪。本文给出具体示例，但没有独立标注研究验证这些标签边界和IAA。与C16结合，应给每个标签明示参照世界、来源、用户任务及背景公理。

第6页算术例子写2x+3=11，先得2x=8，后误得x=3；第7页文字却将“x=4”称作与推理不一致。x=4实际为正确解，故存在解释文字错误，不能将该句当成逻辑金标。简单代入可验证：2×4+3=11，2×3+3=9。本笔记不将此编辑问题推广为作者分类整体无效。

第6、8页Edison等历史归属例子带有关系粒度和表述限定，“credited with”“sole inventor”“improved”并不等价。本组若使用这些例子，必须按原任务和可靠历史来源另核，不把综述案例当作不需要证据的世界事实标签。

## 3. 成因框架的作用与限制

Data：错误信息/社会偏差、长尾/新近知识边界、低质量alignment数据。Training：因果语言建模、长短依赖/注意、exposure bias，SFT能力与知识边界错配，RLHF偏好中的sycophancy。Inference：采样、局部上下文过度依赖、softmax表达限制、推理失败（第7–12页）。

这三个阶段不是独立可加的因果变量：SFT新知识与训练数据重叠，推理时错误可能源于预训练信息不足。章节将“相关”“可能”“理论限制”和“已干预实验”放在同一框架下，引用时须回到原论文区分。Temperature升高改变分布是真的，但其对各任务幻觉的单调关系仍要实验验证；softmax低秩瓶颈也不自动证明某回答为何错误。

第11页把激活探针联系到internal belief，第34页又明确指出探针泛化不充分、belief解释仍在争论。本组应以行为可预测信号或潜在表征说明，不能从探针高准确率断言模型“明知故犯”。类似地Reversal Curse中的反向检索需看关系是否可逆、对象是否唯一，不能把任意“A is B”概括成标准逻辑必有“B is A”。

第9–10页以版权敏感知识不可获得解释知识缺口。这里只能说数据访问/许可可能限制覆盖；没有训练语料审计就不能断言某本受版权保护作品必不在训练集，更不能仅由版权状态推出模型对它没有知识。本文的概念例子不是本组核实的当代训练事实或法律结论。

## 4. 检测方法：需要拆开的三个问题

第一，输出相对什么是真？第二，可用什么证据？第三，如何做判定？本文先按factuality/faithfulness分，再列机制，部分交叉不能避免。

### 4.1 世界事实性检测（第12–14页）

Fact-checking先fact extraction，再fact verification。External retrieval包括FActScore、工具、问题+回答查询扩展；Internal checking包括CoVe、p(True)和直接LLM判断。内部检查不是外部事实数据库，可能稳定复述同一错误；它与多样采样并非互斥。

Uncertainty分internal states与behavior。前者用token概率/熵、概念熟悉度、内部表征，依赖白盒或概率访问；后者用自述、重复采样、间接询问、LMvLM交叉质询，适合黑盒。黑盒不等于无模型成本、零资源不等于无额外训练模型；C08实际使用20样本及NLI/Prompt比较器，C10还需语义聚类。

低概率不是“必假”，一致也不是“必真”；应检测随机confabulation与稳定误解的差异。本文的框架主要组织方法，不给各类一个统一控制条件下的可靠性排序。

### 4.2 来源忠实性检测（第14–16页）

Fact-based测n-gram、实体、关系；Classifier-based包括NLI和合成错误训练；QA-based依赖答案选择→问题生成→来源回答→答案相似；Uncertainty-based用概率/深度集成/dropout等；LLM judge给来源、输出和指南，输出二值或Likert。

指令遵循与逻辑一致虽然属于本文忠实性定义，许多所列指标实际上主要检验context support，未证明能同样检查所有非恶意指令、输出格式或因果合理性。综述需单独标注方法的实际覆盖范围；模型家族或“LLM judge”名称不能替代输入资料与打分规则。

NLI在源支持方向工作，长文分句/依赖弧/对抗微调各解决不同问题；QA各组件可能限制上限；实体匹配无法判关系；LLM裁判可能受解释、长度、语气和训练熟题影响。判断解释应在原论文元评估中验证，不因生成了理由就当作可信证据。

## 5. 基准表的价值及已读原论文交叉核验

第16–19页区分generation evaluation与detector evaluation，方向正确：前者测生成模型输出，后者测已有回答的判定。Table4还列语言、数据量、手工输入、任务、指标，适合建立比较表初稿，但数据量的单位不统一：问题、响应、句子、段落混用，必须另列unit。

对已读资料的核对发现：

- TruthfulQA817为旧版问题数，与固定官方当前790题不同；其生成、MC1、MC2及后来二选一协议也应分列。表中的Acc和LLM judge是任务相关指标，不是可互换结果。
- SelfCheckGPT-WikiBio1908是238篇生成传记中的句子数；原始论文的主要句子检测结果使用AUC-PR、传记层面使用相关系数，Table4笼统写AUROC不足以代表原始主实验。模型标签是在世界事实性下人工核查，表中只勾faithfulness需要说明其所指，不应据此改写原论文评估目标。
- HaluEval30000是三个任务的配对记录、5000是论文一般问答；最终识别随机取正确/错误候选，固定官方一般数据现为4507条。表中“Manual=否”仅指输入题目是否手写，不是说没有人工标签。
- FELM表中3948和正文817来自某段历史文字；C13已独立发现同一论文Table2为847/4425、官方数据快照847/4426。不能重复817/3948作为无版本限定的统一规模。
- HaluEval2.0表内五域1535+1125+1409+1701+3000=8770，算术吻合正文；这只是表格内部求和，不是已经核查该新基准数据或读过其原论文。

这些核对不意味着所有其他条目有误，未读原文条目均需后续确认。特别是AUROC/AUC-PR、单实例accuracy与整体生成率必须分开；把它们合为“accuracy”会破坏比较。

## 6. 缓解章节与评估综述如何衔接

Data类包括过滤、去重、模型编辑、RAG；Training类涉及架构/目标、alignment数据与sycophancy；Inference类涉及factual-nucleus、ITI、DoLa、CoVe、自反思、CAD、faithfulness discriminator、符号推理（第19–26页）。

模型编辑应测edit success、locality、generalization及连续编辑副作用；RAG应测retrieval和generation两端；自反思应看未使用外部新证据时的实际改进边界；改变生成器后还要重新评估检测器泛化。本文把缓解与成因对应是有用的假设结构，并不证明每项方法只干预一种成因。

第20页简述RAG“without affecting performance”，第22、26–32页又详细说明噪声检索可降低性能，因此不能将早期概括照抄为无条件保证。同理“plug-and-play不需重训”不等于无推理开销，ITI探针、并行上下文解码、检索/重写和多轮验证都应记录实际成本。

## 7. RAG失败分析最适合转化为评估实验

Retrieval failure（第26–30页）按query/source/retriever拆：是否需要检索、歧义与多跳拆解；来源是否真实/时效/受生成内容污染；分块、embedding及领域迁移。Generation bottleneck（第30–33页）按context awareness与alignment拆：噪声、冲突、lost-in-middle、引用/归因、faithful decoding。

可直接转成测试条件：同一问题使用金标/实际/无关/错误/冲突证据；固定证据内容，仅改位置和长度；分开问世界正确与来源忠实；对引用检查是否支持claim并覆盖所有claim。因检索最优文档而答对，不代表真实部署召回可靠；看到引用也不证明其内容支持或确实影响了生成。

第31页知识冲突讨论值得保留：早期简单实体替换显示模型偏参数记忆，连贯反事实、多证据或不同规模研究却可显示模型偏外部上下文。不能从某一个构造条件宣称LLM总信记忆或总信检索，实验操纵的可置信度影响结论。没有NLI判为可信就能证明来源世界正确的捷径。

Lost-in-middle的RoPE衰减、训练位置分布只是文中解释路径，不能据此断言所有模型同一机制。压缩上下文也可能删掉关键证据或引入抽象摘要错误；需要同时测压缩信息保留与最终事实性，而非只测token减少。

## 8. 未来方向和本组研究问题

Q1：事实性/忠实性是否可用互斥二分？已读C16与C12说明可交叉，本文例子亦如此。可给同一回答多轴标注world-correct、source-supported、instruction-compliant、internally-consistent，报告标签交叉矩阵及各检测器覆盖；尚未新建数据集。

Q2：知识冲突测试是否依赖反事实生成方式？本文第31页已汇集相反倾向。后续原论文需记录替换实体/重写叙事、单证据/多证据、参数答案确认方法，比较同一模型不同构造下偏好；本笔记尚无控制实验，不将方法差异说成已证明全部解释。

Q3：参考基准表是否会传播错误？已实际核对SelfCheckGPT指标、FELM规模、TruthfulQA版本等，说明二手表不能直接做最终事实表。下一步对124篇建立原文证据行，每个数字保留单位、指标、版本和页码，不以论文题名代替证据。

Q4：不确定性能否识别所有事实错误？稳定误解可能低熵，随机语言表述也可能高熵但语义一致。C08/C10已读方法支持区分这两类；需固定采样预算及聚类器测各类错误，未运行新实验。

Q5：RAG的“来源忠实”会不会降低“世界正确”？错误证据条件下逻辑上可能。设计三变量：证据真假、模型参数回答、生成来源引用，分别评估context adherence和world truth，不把拒绝错误来源一律标成不忠实失败。尚待原始知识冲突研究精读。

## 9. 对综述结构的用途

主类“LLM定义与成因框架”，次类“检测/基准分类、RAG评估条件”。可用作背景组织，但最终论文应以原始评估方法的输入/证据/单位/监督/聚合机制建立多轴比较。与C01相比更细化开放LLM及RAG，与C14/C15相比不提供新的人评流程审计或实践者调查。

英文概括：Factuality and faithfulness provide useful evaluation targets, but they intersect and require distinct operational labels. The survey’s RAG failure analysis motivates controlled evaluation of retrieval quality, evidence conflicts, context utilization, attribution, and generation rather than a single end-to-end score.

## 保留事项

未重新统计全部基准或复现缓解实验；未将被引395条文献计作已读；表格其他条目、模型知识边界与激活信号的泛化仍待原论文核验。版权与训练材料覆盖、历史产品能力等只作为作者叙述中的待证假设，不转写为已查实的当前事实。
