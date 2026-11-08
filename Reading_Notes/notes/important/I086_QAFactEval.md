# I086 · QAFactEval: Improved QA-Based Factual Consistency Evaluation for Summarization

Alexander R. Fabbri, Chien-Sheng Wu, Wenhao Liu, Caiming Xiong；NAACL2022（官方README）。细读PDF为arXiv:2112.08542v2，2022-04-29，15页；https://arxiv.org/abs/2112.08542 。官方代码 https://github.com/salesforce/QAFactEval 。

## 阅读与审计范围

正文1–9页、附录12–15页全部细读，目视第6页消融、第7页主表及示例、第13页数据/过滤规则。官方源码固定commit `01177f11cc05f8b3e75511a0cfa54bac19324d09`，静态阅读README、qafacteval.py、lerc_quip.py、setup.py、qaeval/changes；独立AST与比例核算见 `../../qa/I086_official/static_audit.json`，脚本 `../../sources/audit_qafacteval_static.py`。未运行下载代码、安装依赖、下载或加载大模型；没有原始逐例打分文件，未复算主表模型性能。

## 1. 研究问题：QA与NLI排名是否取决于部件选择

既有论文因基线、输入粒度和数据不同给出相反优劣结论。本篇把QA事实评估拆为答案选择、问题生成、问答、答案匹配，加上摘要回环过滤与来源不可答惩罚，逐部件比较，试图给QA路线更充分调优。

目标仍是来源一致性，不是世界真实性。它主要判断生成摘要的内容是否受来源支持，问题从摘要来；从来源问问题则更容易混入relevance/recall。作者反对把相关维度混成事实一致性，但这不表示任务质量不需要recall，只是应分别报告。

最重要贡献不是“QA终于普遍赢NLI”，而是展示部件和可答性判定对指标效果的显著影响，并显示两路线有可学习的互补性。结论需保留英语新闻和目标开发集调优条件。

## 2. 最佳管线的细节

答案选择：spaCy名词短语chunks最佳；比较NER、Max NP、ALL。NER平均约3个候选，其余平均超过10个，性能下降可能来自覆盖不足。NP并不保证所有否定、因果、关系、量词、时间条件都问到；更大覆盖还会增加冗余、费用和噪声。

QG：BART-large用QA2D训练，输入摘要和指定答案生成问题。最佳模型的问题平均约17token，其他约10；新unigram20%对比T5-SQuAD47%，较长且更复制摘要的问题使QA更容易定位。流畅/自然QG质量与事实核验效用不是同一目标：看起来更自然的MixQG不一定带来更高一致性评价。

QA：Electra-large默认；比较Electra-base、MADE、T5与UnifiedQA。来源文档回答，用问题和候选答案作为匹配上下文。摘要端同一QA先做IsAnsweredSumm，若不能从摘要回答就删题；附录还要求候选span与摘要端QA答案F1至少约.60。

来源端IsAnsweredInput判断无法回答时，把该题所有overlap分数设0，即Answerability Penalty；能答才计算匹配。不能将“摘要端不可答删题”与“来源端不可答置零”混同，否则会把错误内容对应的问题全部过滤掉，虚高分数。

答案匹配默认LERC(QuIP)：MOCHA约40k人工QA输出评分训练的1–5相似度模型，用RoBERTa-large、QuIP问答预训练初始化，输入问题、摘要指定答案、来源QA答案和上下文，输出学习匹配分数。它是监督式语义匹配器，不是无监督公式，也不等于直接世界真值分类。

最终对通过摘要过滤的问题平均；LERC原尺度不是自然校准的0–1事实概率，不能把原始lerc_quip得分当成置信百分比。过滤后题数、零可用题、失败回退和问题覆盖均影响可解释性，应随分数记录。

## 3. 学习式QA+NLI组合

SCConv将来源—摘要句对的NLI支持分数直方图映射到句级支持，再聚合。QAFactEval-NLI还把QA每题分数的K维向量变成H-bin直方图，经单层映射得到QA汇总，与NLI分数拼接，经线性层判整体一致性。

合成设置在FactCC的50000条自动编辑数据训练聚合器；监督设置再在每个目标基准的validation标注上fine-tune并选阈值，test报告。二者资源不同，79.5的监督组合不能同77.8未在目标人评上训练的QAFactEval当完全同监督条件。

“synthetic/无人工标签”只针对这一聚合阶段；底层QA/QG/LERC/NLI各自依赖监督与预训练资源，不能写整个系统不需要人工标注。

## 4. 数据调整让原SummaC总分失去直接可比性

本篇明确改Polytope：原SummaC将Omission、Addition等当不一致，本篇把相关样本转为一致，认为它们多是抽取、仍受来源支持。判断是否合理仍要看错误定义与实例：如果Addition其实是来源外新事实，不能仅凭“抽取”一概合理；本次未读Polytope原文与工作簿，不替作者证明每条重标正确。

XSF附录缩至996valid+996test，而I092是1250+1250，排除一般factuality/世界知识与非目标标注口径，使用与Koto工作相同子集。I035公开预计算四模型各498共1992，与此数量吻合，但本篇未在已读源码提供完整ID映射，不能只因数量相等就证明完全是同一1992条。

其余CGS1281/400、Poly634/634、FactCC931/503、SummEval850/850、FRANK671/1575。Table 6正类比例明确是validation：Poly87.2%、XSF9.4%、FactCC85.8%。原I092表Poly6.6%是另一标签协议，不能把两者当同基率测得同一指标性能。本文也重新计算基线，不能将74.4→77.8直接称在完全相同测试上提高3.4点。

基准原偶奇拆分共享文章问题仍需核查本篇实际ID；不能从同样split规模直接宣称它已按文章隔离，也不能将I092重建466交集未经重算直接赋给缩小后的XSF。

## 5. 调参协议、消融与局限

部件消融只用validation：随机80%定阈值、剩20%评价，保护test。最佳组合再固定，每次换一个部件。附录承认没跑完整笛卡尔组合，只从初步良好组合搜索，另尝试ALL作次优选择。它说明局部敏感性，不保证全组合全局最优，也未完全隔离交互作用；反复在小验证集搜索仍可能有选择噪声。

Table 2总体77.5为validation消融结果，不是Table 3 test77.8。单部件替换：MaxNP75.7、NER66.4、ALL75.7；QG BART-SQuAD74.3、T5-SQuAD67.0、MixQG-base75.1/large74.9。不能说更大QG永远更好，或问题自然度越高元评估越好。

QA替换Electra-base77.0、MADE77.4、T5-base76.1、UnifiedQA75.7，差较小。但作者固定Electra-large的IsAnsweredInput，故不是完整替换所有QA功能；“QA能力不是瓶颈”只能解释为可答问题上的答案抽取变化在该控制下影响较小。不可答识别恰恰是大瓶颈。

匹配EM68.4、F171.7、IsAnsweredInput73.3、LERC原71.8、LERC-RoBERTa77.3、LERC-QuIP77.5。说明语义匹配预训练/架构显著影响得分，QuIP相对同规模RoBERTa增.2，没有给此差显著性，不夸大QuIP单独贡献。

无摘要过滤73.8、无来源不可答惩罚72.1、两者都无67.4，相对77.5下降3.7/5.4/10.1点。这是验证集受控消融的实证，不能直接称造成现实幻觉减少10.1%。Table 4展示QA来源错拒答仍会误罚忠实例，也说明惩罚机制不能保证所有零分都是真错。

## 6. 测试结果、提升分母及相关性

Table 3六集宏BAcc：QuestEval68.2，QAFactEval77.8，MNLI75.7，ANLI74.4，SCZeroShot72.8，SCConv synthetic74.3；QA+NLI synthetic78.3，supervised79.5。相对前QA68.2提高9.6个百分点，(77.8−68.2)/68.2=14.076%，摘要“14%”是相对提升，不是14个百分点，也不是错误率降低14%。独立算术已保存。

QAFactEval分集75.1/63.1/79.8/84.1/80.9/83.9，并非每集最好：XSF BertScore-FFCI68.8，PolyDocNLI84.7，FactCC MNLI89.8。QA+NLI监督79.5总体最高，FRANK84.3带99%显著标记；附录只明确总体与FRANK存在对应显著差异，其他集未见显著差。不要将所有主表粗体都当显著。

Table 5为pool实例Pearson；QAFactEval XSF.29、SummEval.61、FRANK-CNN.66/XSUM.32、QAGS-CNN.68/XSUM.44。BARTScore QAGS-CNN.73比它高，XSF FFCI/QuestEval.45更高，说明宏分类胜出不保证每个连续标签相关都最好。

附录Summary-level含义是同一来源文章下跨生成器候选算相关，再跨文章平均，非“全库每摘要一个分数”的普通pool相关。QAGS每来源只一个生成模型，不报该项；不能与I062所叫summary-level Pearson混为同一个计算方式。示例QAFactEval Summary-level Pearson FRANK-CNN.68/XSUM.53，表5instance .66/.32，差异来自聚合。

附录Spearman/Kendall与Pearson不同：SummEval QAFactEval实例Pearson.61，Spearman.43、Kendall.34；不选择性只报最大的数，表格要写清系数类型。它没有FRANK原文那样按生成器组回归残差控制，不能直接比较.66与I007偏相关当方法提升。

## 7. 官方实现、空题及复现待办

qafacteval.py包装外部QAEval，ZIP的qaeval目录只有license与修改说明，主体由未固定版本pip依赖提供；代码固定commit不能冻结整个管线。主README没随包提供论文全部baseline输出与NLI组合训练流程，不能声称已获得完整主表复现材料。

源码get_filter要求摘要端probability>null_probability且F1>0.60；附录写F1<.60才移除，对恰=.60边界不同。独立AST核实严格大于与算术边界，影响规模尚未量化，不夸成主要误差来源。

score_batch_qafacteval明确TODO只用每个source所配summaries中的第一条，其他候选可能被忽略；实际批量评估应一次一候选或修正映射。return_qa_pairs=False时输出结构还依赖外部QAEval版本，不能未经运行宣称所有返回路径可用。

LERC输入串为question<q>reference_answer<r>prediction<c>context，最长512token，尾部来源会被截断；不能假设匹配器已读到所有长文证据。对不可答题直接0；无可用问题时底层平均/回退依赖QAEval，目前未核验，不能自行填为“完美忠实”或“错误”。

本次未执行setup.py（其中还会联网读README），未下载权重、未调用spacy自动安装、未加载归档。运行依赖/model revision/题目缓存和失败分支需要后续固定。

## 8. 研究问题与已形成答案

Q1：QA排名低是否代表路线本身差？部件消融表明QG、过滤、不可答、匹配都能改变10点级结果，不能据FEQA/QAGS早期配置否定整个机制；同样不能据此宣布未来所有QA都优于NLI。

Q2：补足可答性是否比提高生成答案质量更重要？在固定Electra可答性下，换答案模型影响较小；去可答性惩罚大降。这支持分开研究答案抽取和可答判断，而不是一个SQuAD F1代表全部功能。

Q3：为什么题目更流畅却指标更差？作者报告较长复制问题更易QA定位；这可能提高匹配也可能保留错误预设。需独立标注问题预设、事实覆盖与可答性，而非只优化QG自然度。当前消融支持效用与流畅度不等价，未做完整因果分解。

Q4：基准标签改变算不算模型进步？不能只看跨论文总体差；本篇同协议重算基线才是内部有效对照。Polytope标签语义与XSF子集须在综述表中明确，不能在综述中合并原版与修改版分数。

## 9. 综述位置及团队接口

主方面是QA管线部件研究、不可答与语义匹配；次方面为QA/NLI组合、基准有效性、阈值调优、相关性定义和依赖版本。与I042/I062历史管线、I092粒度、I073训练数据、C11元评估、C14报告可靠性直接连接。李瑾负责部件对照，程子晨参与各环节原文核验、资源审计及跨章节综合；以实际贡献记录为准。
