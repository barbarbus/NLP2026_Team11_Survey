# I092 · SummaC: Re-Visiting NLI-based Models for Inconsistency Detection in Summarization

Philippe Laban, Tobias Schnabel, Paul N. Bennett, Marti A. Hearst。细读版本arXiv:2111.09525v1，2021-11-18，16页；正式书目信息为TACL2022，10:163–177（官方README引用）。原版本 https://arxiv.org/abs/2111.09525 ，官方代码 https://github.com/tingofurro/summac 。

## 阅读、核验与边界

已读正文1–11页及全部附录15–16页；参考文献不视作引用论文已读。目视Tables 2–5、A2（第8–10、16页）。官方代码使用资料库固定commit `c1f3da93cd074c24d8033eb27a88b5a7cc5c08fa`，读README、benchmark.py、model_summac.py、utils_scorer.py、utils_scoring.py及Main Results notebook的代码单元，不执行其中任何单元，也不加载.bin。独立从I035原标注和FRANK JSON重建标签/划分，审计 `../../qa/I092_official/label_audit.json`，脚本 `../../sources/audit_summac_labels.py`。

## 1. 研究问题：NLI失败是能力还是输入粒度失配

标准NLI训练主要是句对，直接把完整长文章和整个摘要放进去，会遭遇长度、稀释、跨句整合等分布差异。SummaC把来源切成M块、摘要切成N块，计算全部M×N句对的entailment/contradiction/neutral概率，再聚合判断摘要来源一致性。

作者明确把来源外真实背景也算inconsistent；这是source faithfulness，不是现实真实性。它与C16“需要符合任务”的规范判断不同，也不证明所有正确背景都应当删除。

Figure 1的长文NLI .91与局部第三句无支持是示例动机，不能以一个案例证明所有文档级NLI都差。真正支持是多模型/粒度消融，同时也要保留MNLI+VitaminC全文粒度已经较强的例外。

## 2. 两种聚合到底做什么

ZS：对每个摘要句，在来源所有句中取最大支持概率，再对摘要句取均值。例中max向量.98/.99/.04，整体.67；去掉第三句后.985。它编码“每个输出句至少一个来源句支持”，无法可靠处理必须综合多句才能证明的单句，也可能因某个误高NLI分而误接受。均值能稀释少数严重错，与I031弧均值问题相似。

Conv：每个摘要句的来源支持分数列形成H-bin直方图，以一层学习映射得到句分，再平均。论文H=50，使用FactCC合成数据10000对、交叉熵、Adam、batch32、lr.01，开发集选参数。它不只是选最佳证据，而利用整个分布；也丢掉来源句次序与具体句身份，因此不能直接进行跨句逻辑组合。

论文称end-to-end训练需理解为后续聚合模型训练：当前代码NLI推理在no_grad、转numpy并用np.histogram离散化，不是反向微调整个NLI编码器。所谓仅H参数/轻量主要是聚合器，不包括大型ALBERT等预训练NLI模型与其原训练资源。

直方图用count而非density归一化，来源句数量会改变总计数，故长度可能影响分数分布。是否模型学会利用长度而不是一致性，需要控制相同内容/长度实验，本次未跑该实验。可解释性也弱于ZS的argmax证据对。

## 3. 六数据集标准化及标签语义

Table 1 valid/test：CGS1281/400、XSumFaith1250/1250、Polytope634/634、FactCC931/503、SummEval850/850、FRANK671/1575。原任务不同：CGS排序拆为正负独立分类；XSum合并intrinsic/extrinsic；Polytope只保留accuracy错误、忽略三类流畅性问题；FactCC作者标注；SummEval Likert变二元；FRANK多错误类型变二元。

“统一二分类”只是统一接口，不能使原标签定义完全相同。Polytope准确性中遗漏/重复是否应算幻觉尤其需任务化；单一总体标签可能混合来源不支持、信息遗漏和表达问题。人工IAA来自各数据、标签转换不一定保留原可靠性；Table 1不同κ也不能当成无条件可比质量。

论文对无原划分的三个集采用偶数行valid、奇数行test；这保留类别与生成器分布，却不保证相同来源文章隔离。阈值/参数可能在相同文章其他生成器摘要上调节，所以它不等价于完全新文章泛化。

主指标BAcc=.5(TPR+TNR)，对每集在validation选不同阈值，六集不加权平均；AUROC为次指标。阈值无需测试集标签，但需要目标集开发标注；ZS无训练聚合参数不意味着最终二分类完全零目标数据。宏平均不是把所有文档pool后算一次，也不是按数据量加权。

## 4. 主结果、速度与显著性

Table 2 BAcc整体：NER56.8、MNLI-doc61.3、FactCC-CLS62.8、DAE64.2、FEQA58.7、QuestEval69.4、ZS72.1、Conv74.4。五个百分点指74.4−69.4的绝对差，不是相对提升5%。

Conv分集64.7/66.4/62.7/89.5/81.7/81.6；并非每集第一：CGS ZS70.4更高，Polytope QuestEval70.3更高，FRANK QuestEval82.1略高于Conv81.6且作者称差异不显著。不能写“六集全面最优”。FactCC-CLS在这里是RoBERTa-base重新训练版本，不是I073原BERT FactCC checkpoint；DAE是默认单句来源路线，长来源适配限制需注明。

附录AUROC整体Conv77.8、ZS74.3、QuestEval73.6；Conv在FactCC92.2但CGS67.6低于ZS73.1。BAcc74.4与AUROC77.8不是同一分数，不能与C09的后来跨任务结果无条件比较。

吞吐测固定FactCC503例、平均33.2句、单Quadro RTX8000：Conv433文档/分钟、ZS435、FEQA33.9、QuestEval22.7、DAE755、MNLI-doc6200、FactCC-CLS13900。说明相较当时QAG较快但比单次分类慢；不能当今天硬件/API延迟预测。复杂度仍近似随M×N句对增长，“不同单位难以直接比较”不意味着不能说明该伸缩规律。

正文声称bootstrap并Bonferroni校正。发布notebook实际对索引shuffle、截取70%无放回子样本100次，按各模型边际区间是否分离比较，不是通常有放回bootstrap，也非同一重采样索引下差值的配对bootstrap；未按文章聚类。其引用模块utils_summac_benchmark等在当前ZIP还没有同名文件，不能保证当前notebook可直接重跑。应把论文报告的显著性与当前可核源码范围分开，不假称已重新验证星号。

当前benchmark.evaluate会在传入cut上直接choose_best_threshold；若对test对象调用便利用test标签调阈值。utils_scorer的from_score_to_pred同样在当前dataset选择阈值。正文要求validation选阈值，复现需显式验证并转移阈值，而不能照任一便捷接口把test最优值当符合论文协议。本次没用此接口运行模型，也不能据此断言原实验一定泄漏。

## 5. 消融限定了哪些结论

模型Table 3：旧decomposable attention SNLI仅ZS56.9/Conv56.4；现代模型和MNLI/VitC更强，最佳ALBERT-xlarge MNLI+VitC72.1/74.4。表用“BERT Base/Large”泛指规模，实际附录包含DeBERTa、RoBERTa、ALBERT，不能误写所有都是BERT结构。

Table 4默认VitC+MNLI单E74.4，加入E+C74.0略低；ANLI/MNLI加入矛盾有小增益，不是所有模型越多NLI类别越好。neutral在部分模型弱，不能等同来源外真实的通用检测器。

Table 5 MNLI全文–全文56.4，句–句ZS70.3/Conv73.0，两句–句Conv73.5；VitC+MNLI全文–全文ZS72.1，句–句ZS72.1/Conv74.4，两句–句Conv74.7。粒度改善对MNLI尤其显著，VitC全文模型本身已强。句–句不是绝对最佳，两个来源句可稍好，也未提供该.3差的显著性。

当前split_2sents是滑窗1–2、2–3、3–4……，正文是非重叠1–2、3–4……，需固定版本/规则。不能把这两个分块方案当成同一配置复现。

附录A1先来源max再摘要mean最佳72.1；min/max组合差。这个经验最优不保证严重错句风险最低，仍需报告句级错误存在性与平均支持两个目标。

## 6. 独立重建：标签与划分实际有什么变化

XSumFaith当前loader把每个system–article的跨度记录行按hallucination_type取众数，众数NULL则一致；不是先按每位工人形成一个票。一个工人可标多个跨度，行数权重因此不同。用I035已固定原CSV独立重建：2500摘要、row-mode正257，按每工人“没有任何非NULL跨度”再多数票正254，3例标签不同。只有1例工人数为2，其余2499为3。

这说明此处行权重问题有实质但较小的标签敏感性，不能夸称全部10.2%正类都由这一bug造成；原论文20–30%来源忠实与此库10.2%的更大差异还涉及三人一致/词跨度聚合及Gold等口径，尚未全部重建。

最重要的已验证划分问题：按当前原CSV分组顺序偶/奇切分，各1250例，valid485个唯一bbcid、test481个，交集466篇。它不是训练文本泄漏的直接证明，而是目标开发/测试共享大量文章的确定事实，限制“全新文章”泛化与独立样本假设。后续应按文章分组重划分再选阈值，并报告变化；本次没有重跑NLI或宣称其数值损失。

FRANK正文说“多数标注者认为整个摘要无错”，当前loader是先每句至少两票NoE，再要求所有句都满足。这两个操作不可交换。独立对2246摘要重建：句级多数后全句通过752，先每工人全摘要无错再多数722，30例标签不同。若每句是不同两人同意正确，整体可能没有两位始终认为全篇正确。需在综述注明标签聚合路径，而非只写majority vote。

SummEval正文写三人全部5分才正，当前loader是严格多数给5。Polytope正文说只五类accuracy，当前overall_label按任意已记录错误判负，需检验原表是否记录流畅类后才能量化影响。未下载该工作簿、不伪造其影响规模。对这些差异，本次不能确定是后续代码改变还是原文简述，均按固定版本报告。

## 7. 当前发布模型不等于原文默认

论文等宽50-bin与主要单E，README示例默认Conv用percentile边界23个bin；代码默认构造又可能是三个NLI模型而README只vitc。ZS默认granularity paragraph且use_con=True，正文主方法为句级E-only max–mean。使用者须显式设置参数，不把默认API输出当作主表配置。

模型最多保留来源100句；过滤字符数≤10的句子；Conv最多10个摘要句，其余切掉，未处理成可见错误；每对输入最长500token。长回答和极短事实句可能受覆盖影响。当前Conv有Linear(full_size,1)及Linear(3,2)，也不只是严格50个训练参数。

缓存与HF模型只指定名字未固定模型revision；固定源码仍不等于冻结完整权重/数据。score端模型结果没有在本次运行，已有.bin也未反序列化。XSum加载器还调用trust_remote_code，未经检查不运行下载脚本。

## 8. 提出并研究的问题

Q1：NLI是否“根本不适合”事实评估？多粒度实证反驳这种笼统断言，但更合适输入不等于完成世界核验/多跳推理。I073正式版和I031也显示任务与模型选择重要，应作机制解释而非路线二选一。

Q2：标签标准化只改格式吗？不是。独立重建确认XSum3例、FRANK30例对操作顺序敏感，SummEval规则亦有文字/代码差异。计分对象在元评估前就被改变，综述应记录完整标签映射。

Q3：偶奇划分能衡量新文章吗？独立计数466篇共享文章，答案是否定的；可以测试同类文章分布下不同生成输出，但不能据此声称文章隔离。下一步按bbcid分组实验仍待做。

Q4：74.4%证明上线可靠了吗？没有。是六新闻基准宏BAcc，带目标集阈值选择，且部分子集差。部署需固定阈值、错误代价、风险覆盖和证据长度，不拿整体均值替代实际风险。

## 9. 综述位置及团队接口

主方面为NLI粒度对齐与元评估基准，次方面为聚合、阈值、人评映射、切分依赖和成本。联系C09分块、C11 TRUE、I007 FRANK、I035原XSum、I073合成数据、I031关系粒度、I042/I062 QA比较。李瑾汇总机制和指标表，程子晨参与所有证据/源码审计和跨章节综合；后续按实际工作记录贡献。
