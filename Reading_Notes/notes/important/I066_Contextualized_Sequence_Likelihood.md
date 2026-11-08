# I066 · Contextualized Sequence Likelihood: Enhanced Confidence Scores for Natural Language Generation

Zhen Lin、Shubhendu Trivedi、Jimeng Sun。资料库为arXiv:2406.01806v1，2024-06-03，16页。https://arxiv.org/abs/2406.01806 。以下不把该预印本自动替换为未经核准的后续发表版。

## 阅读和核查范围

正文1–8页、附录A–E（11页末至16页）已细读，9–11页参考文献不计引用论文已读。目视第7页Tables 2–4、第13页标签阈值及附录说明、第15页Table 8与可靠性图。固定官方 https://github.com/zlin7/ContextSL commit `44f37173ccaa89849d20683570d0b5d4e68f0a1e`，保存ZIP/provenance。

静态阅读README、pipeline/summ.py、uq.py、eval_uq.py、dataeval/load_worker.py、utils/nlg.py、scripts/human_eval.py与main_latex.ipynb代码单元；解析仓库人工标注XLSX的XML，不运行公式或作者程序。人工表可读导出720行在 `../../qa/I066_official/human_annotation_rows.json`，独立核查在independent_audit.json，辅助脚本为 `../../sources/inspect_csl_annotations.py` 和 `../../sources/audit_csl.py`。只用独立标准库算术、XML/AST解析，没有模型调用、远程任务队列、pickle反序列化。

README另给Google Drive预测/cache资源链接，已记录但未下载全部大缓存；不能声称已复现九个模型×数据设定表格。当前代码快照也未被证明与论文实验的具体提交完全一致。

## 1. 方法测什么、为什么提出

作者区分uncertainty与confidence：前者针对输入下的预测分布，后者还依赖具体生成答案。CSL为具体答案打可信排序分，核心问题是序列概率混合了正确性、措辞习惯、语法和非关键内容；不同问题对同一句话的关键token要求不同。

例如问何时登月时日期比人名更直接回答问题，问谁同行时人名更重要。CSL用生成器自身注意力给原始答案token log概率加权，主要目标是正确/错误答案排名；不检索外部事实，不输出经证据核验的真假概率。与I085的整个下一token分布熵不同，这里把特定答案中已生成token的重要性纳入评分。

## 2. 公式及访问条件

基线SL=Σ_i ell_i，ell_i是生成token的log-softmax概率，不是未经归一的raw logit。归一SL=Σell_i/n。CSL用另一个判断提示让模型关注原答案，提取提示最后一个token对答案位置的attention a_i，限定答案span内归一为w_i=a_i/Σ_j a_j，再计算C_CSL=Σ_i w_i ell_i。

它是加权log概率，exp后为加权几何均值。即使w非负、和1，也不意味着对全部答案形成归一概率分布，更不直接等于“答案正确概率”。因此放入SE替换原似然时，应明确是实用分数替换，不将严格概率语义自动继承。

注意力来自“判断答案是否回答问题，回复Y/N”的额外prompt，但CSL不使用最后实际Y/N判决，只用attention。CoQA在该prompt可带来源段落/对话历史；不是用金标答案当必要评分输入。附录示例中包含已知对错的few-shot演示，这和目标题金标无关。

CSL-Next省略判断提示，读取原生成完成后下一token位置对答案的attention。两者均需token概率、attention矩阵及位置对齐，属于白盒/内部访问，不适合只返回文本的闭源API直接照搬。推理不必额外训练生成模型，但选择attention head需要目标正确性标签。

模型多头不能全部等权：验证集给每个head计算其加权分对正确标签的AUROC，选top10，平均这些头的权重/分数。这个选择是监督式元参数选择，不能称“完全无标签”。多头平均旨在减少只选最好头的抽样噪声；是否普遍降低噪声还需更多域/模型检验。

## 3. 对式3序列排序主张的独立检查

第3页讨论top-p/top-k时称截断后序列分布P′(s|x)仍与原始token概率乘积全局成比例、保留排序。这一般不成立：每个前缀留下的概率质量不同，其归一常数依赖路径，不能抽成单个与s无关的常数。

独立两步反例：root概率A=.4/B=.35/C=.25，top-p=.7留下A/B、质量.75；A之后token x=.8、另一个=.2，B之后x=.95、另一个=.05，同阈值均只留下x。两路径末尾立即终止。原始P(Ax)=.32、P(Bx)=.3325，后者更高；截断重归一P′(Ax)=.4/.75=.5333，P′(Bx)=.35/.75=.4667，前者更高，发生排序逆转。

这否定的是一般的全局比例/保序推导，不是对本篇数据全部结果的否定。若评分使用原始未截断模型log概率，它依然是该原始模型下的正确似然，但与“实际采样器分布”的概率需要分开。后续阅读不能把“序列似然”“采样频率”“正确性概率”三者混写。

## 4. 数据、生成与验证划分

CoQA dev7983题，open-book且历史带参考答案；TriviaQA rc.nocontext validation去重9960题，closed-book；NQ validation3610题，closed-book。每次随机1000题作head选择/验证，其余测试，重复10种随机划分。名义余量6983/8960/2610，但实际评价还会删除空输出、裁判不一致等，不能未经日志将名义余量当最终分母。

模型为LLaMA2-13B、Mistral7B、Gemma7B；README指明Mistral-7B-v0.1和相应base模型名，不能当作所有chat版本的结果。主要评价greedy答案，采样基线另温度.5取5个额外答案；附录改为1.0并测试3/5额外生成。作者修改停止规则避免“Dr.”中的句点截断答案，实际响应版本与I091旧管线不可假定相同。

TriviaQA用1-shot示例；NQ用5-shot训练题；CoQA含参考历史，和自由对话累计模型自身错误不同。每次随机划分测试集高度重叠；±为10划分均值/标准差，不是10个完全独立生成实验，也不是每例误差或95%区间。

main_latex notebook确认主要表配置curve='auroc'、setting='mlga~neg_mlgc'、num_gens5、temp.5、acc_name='moe'及seed0–9。Notebook使用paired=True的汇总显著性，pval=.01作格式标记；有重叠划分这一依赖时，应谨慎解释极小p值，不能把每个被重复测试的题视为新独立观测。是否采用更细致的按题bootstrap仍需追查，当前不笼统宣称全部显著性无效。

## 5. 自动正确性不是双裁判多数票

作者用LLaMA2-70B和gpt-3.5-turbo-0125给答案相对参考的分数；人工样本上选择阈值，LLaMA≥.2、GPT≥.6为正确。关键acc_agree只保留二者二元判断一致的答案，不一致设NaN，并非“任一说真就真”“两个都说真才真，否则假”或第三裁判多数票。

源码summ.py get_acc('moe|acc')复制LLaMA标签，对与GPT不同的位置赋NaN；eval_uq再dropna。故主结论条件于自动裁判一致的子集，疑难/争议答案被选择性排除。这能提高标签可信性，但同时改变评价对象；应报告保留覆盖率及被删组特征。

人评阈值来自9个model×dataset各80例，总720。scripts/human_eval.py实际每设定40个中心greedy答案与40个第一采样答案，不仅greedy；两次选题集合可能重叠，不应说720个独立问题。人工参考和上下文用于判答案正确，未给充分标注者间一致性统计。

原表独立解析确认720行、每数据240、每模型240、每组合80；human_eval=1有538、0有162、.5有19、.8有1，即700条明确二元标签、20条非二元/模糊。CoQA其中一条两自动分数缺失。剔非二元并只用完整分数时699例。

按公开阈值独立复算：CoQA双裁判一致222/235，覆盖94.47%，其中218正确对人评，一致率98.198%；NQ196/226，覆盖86.73%，180正确对人评，一致率91.837%；Trivia226/238，覆盖94.96%，222正确对人评，一致率98.230%。总保留644/699。这些覆盖是人工抽样内结果，不是全测试集保留率。

单LLaMA对明确人评CoQA228/235=97.021%、NQ196/226=86.726%、Trivia226/238=94.958%；GPT为221/235=94.043%、194/226=85.841%、230/238=96.639%。大体支持Table 1，CoQA GPT表写94.1而本次明确规则复算约94.0，保留该小差，不强行改数据到吻合。

重要限定：附录B用这批人评选最优阈值，报告的标签一致性也是同批复核，没有看到独立人评holdout。98.2%是“经两裁判一致选择后对人评的准确性”，不能说“所有答案标签98.2%可靠”，更不能说“模型作答正确率98.2%”。模糊题及错误参考被剔除后，可解释性更强但适用范围更窄。

## 6. AUROC、AUARC与后校准

AUROC阳性为答案正确，高CSL高可信；代码用negative confidence u并对-u求ROC，方向与I091高不确定性预测错误相反，数值比较前需统一标签/符号。

AUARC是按低confidence拒绝后保留答案的准确率曲线面积。代码area_under_accuracy_coverage_curve按u升序、计算前缀平均准确率，再用linspace(0,1,n)梯形积分；函数名覆盖/正文拒绝是同一排序视角在轴反转下的表述。这个实现的第一点把单例准确率放在0，而非覆盖1/n，必须在复算时保留；少量样本时端点影响明显。Random列是基础正确率，不是固定.5；Upper Bound按正确标签理想排序，通常也不是100。

可靠性图在附录E经sklearn CalibratedClassifierCV后得到，且小于10例的箱不展示。它不能证明raw CSL已经是校准概率，也不能据未显示的低样本箱推断没有校准误差。拟合/评估隔离、版本默认参数及ECE数值仍需单查calib.py和缓存，本次未重现。

## 7. 主表与附录例外

Table 2 NQ/Mistral：CSL76.65±.43，TokenSAR72.61±.48，SLnorm71.06±.54，分别高4.04/5.59个AUROC百分点；不是QA准确率提高5.59点。Trivia/Mistral CSL90.76、SL88.81；CoQA/LLaMA CSL73.34、TokenSAR72.78，优势大小随任务变化。

CSL不总是数值最高于CSL-Next：CoQA/Gemma为73.30 vs73.64，LLaMA73.34 vs73.36；作者也将近似方法以不显著差异粗体标记。不能将“CSL优于baseline”改写成“每一格严格超过所有方法”。

Table 3 NQ/Mistral Random52.90、CSL AUARC72.25、Upper Bound86.57；CoQA/Gemma Random92.64、CSL96.85、CSL-Next96.90。高基础准确率时AUARC看起来很高，不是所有题都正确96.85%，更不是同为AUROC96.85。

Table 4 SE+CSL主设置各行优于原SE变体，例如NQ/Mistral78.66 vsSEnorm75.71；但Table 8温度1、3个额外生成时CoQA/Gemma75.25低于SEnorm75.42，5个时77.11也低于77.24。差距可能不显著，仍不能说“所有设置一致严格改善”。

更重要的基线敏感性在Table 6：温度1、5个额外生成的CoQA/Gemma Deg76.40，CSL73.07；LLaMA75.73 vs73.46，Mistral74.41 vs71.79。作者附录主动承认Deg可更好，代价更多生成/NLI比较。公平综述应给成本—效果条件，不能只摘主表低温下的胜出。

跨域head迁移Table 5用CoQA选头，再用Trivia/NQ。CSL均高于SLnorm，但CSL-Next有反例：Trivia/Gemma87.43低于88.11；NQ/Gemma74.99低于75.81。跨域结果标准差也更大，例如NQ/Mistral CSL72.71±3.32。该证据支持部分迁移，不是无域适配普遍稳健。

## 8. 注意力解释和资源开销

Figure 2仅一条登月答案换三种问题，1024个head对相关片段attention增大，极小t-test p值说明所展示比较；head共享模型和输入，不能当1024个独立事实实例，亦不证明attention是回答因果依据。Figure 3 NQ/Mistral验证/测试head排名Spearman>.97是同总体切分的稳定性，而非任何领域都不变。

CSL与CSL-Next权重高相关、head跨域和可视化是合理机制支持，但两种分数共享模型、token和标签选择，不是完全独立验证。作者也承认某些token权重难解释，且QA提示需迁移到其他任务。

CSL额外一遍forward而非生成多个完整答案，通常比采样型方法省，但“close to none”不等于零开销：需保存/访问attention、对齐token、输出矩阵，内存/高效attention内核兼容性也影响实际时间。没有统一硬件/长度实测就不给精确加速倍数；head选择还需1000标签及离线多头计算。

## 9. 源码中语义熵聚合的进一步核查

固定uq.py的_hard_semantic_entropies先对每簇log概率做logsumexp，再对簇结果调用_logmeanexp，最后取负。即U=−log[(Σ_c mass_c)/K]，不是I091旧代码的−K⁻¹Σ_c logmass_c，也不是严格Shannon熵−Σ_c p_c logp_c。get_semantic_entropy确实调用此函数；主notebook的SE相关路径仍需原缓存核对，不将快照等同原实验提交。

独立固定两类质量.9/.1和.5/.5：当前函数都给log2=.693147，而真正熵分别.325083和.693147。固定K和总质量时它不区分类概率不平衡，只受K及总权重影响。这个算例说明术语/实现区别，不据此断言其经验分数必无排序价值。

CSL取exp后本也非归一概率，原语义簇函数又以无矛盾而非严格双蕴含条件分组。因此比较“SE+CSL”要说明具体聚类、分数组合及实现，而不能把I091/C10理想定义的所有性质直接赋给它。本轮静态发现必须在综述审计部分按版本限定陈述。

## 10. 研究问题、正文连接与后续任务

问题A：标签选择是否改变相对排名？双裁判一致子集排除NQ人评样本约13.27%，可能集中于别名/多解/困难题，排名差距有条件性。当前只有720人评表、缺完整CSL缓存，无法独立重算各方法在人工金标与完整题集上的AUROC。可用保留/删除分层审查、全题人工子样本和相同题预算复测，此为待执行设计。

问题B：head筛选是否只是多重挑选？验证与测试分开、10头平均和跨域表提供一定支持，不能直接指控测试泄漏；但1000验证在上千头上选择仍可能不稳。应固定不同校准规模、按主题隔离、冻结头后测新域，并给选择频率和题级置信区间。

问题C：加权到底改进了什么？原始SL、SLnorm、TokenSAR、CSL及Next对照支持token加权有用；要进一步隔离“问题相关性”则应固定验证监督和头数，加入随机权重、打乱问题、人工关键词和不带判断提示等控制。可视化/权重相关不足以证明唯一机制。

问题D：怎样把CSL与I081结合？CSL输出排名分，I081比较直接置信及后校准。需固定同一答案、独立标签、校准集与测试集，再比较AUROC、风险覆盖、ECE/BS，避免某方法重新生成更好答案导致混杂。不能只比较两篇不同基准表里的最高数。

问题E：语义熵不同实现如何公平比较？本轮实际对照发现I091均值log、I066 log均值与理想概率熵三个对象不同。下一步在固定人工意义簇/原概率及样本频数的条件下统一实现，再报告性能/成本；目前只完成静态和算术，未复现模型结果。

综述主类：内部概率与token重要性；次类：attention头选择、语义聚合、裁判标签及选择性预测。接I091时说明对“非关键词概率仍占权重”的补充，接I085说明分布熵与特定回答分的区别，接C14/I100/I081说明标签、评价条件与校准。可用英文论点：“CSL reweights token log-likelihoods using task-conditioned attention and validation-selected heads. Its gains are conditional on the evaluation labels and sampling baselines, and the weighted score requires separate calibration before probabilistic interpretation.”

程子晨继续参与全文、公式、数据、源码、指标及综述写作全环节；其他成员按原计划可接头选择、标注子集、概率聚合和跨方法预算对照。此为后续协作建议，不声称已经执行模型实验。

已完成全部实质正文/附录细读、关键表图核查、官方固定源码、720行人评清点与大部分Table 1独立复算、截断保序/熵聚合反例。未下载完整Drive预测cache，未运行模型；缺最终逐设定评价分母、原始实验revision、独立人评holdout和全部校准复现，待办明确保留。
