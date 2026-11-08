# I045 Can LLMs Express Their Uncertainty?：置信度校准不等于错误可分辨性

## 来源、版本与阅读范围

Miao Xiong、Zhiyuan Hu、Xinyang Lu、Yifei Li、Jie Fu、Junxian He、Bryan Hooi，*Can LLMs Express Their Uncertainty? An Empirical Evaluation of Confidence Elicitation in LLMs*，ICLR 2024，arXiv:2306.13063v2（2024-03-17）。本地PDF共29页，正文、参考文献、证明、完整实验附录与prompt逐页阅读；目视核对PDF7表2、PDF8表3、PDF9表4、PDF17–18表5–7及PDF23表13。

作者当前[官方仓库](https://github.com/MiaoXiong2320/llm-uncertainty)保存为`Hallucination_Evaluation_Library/code/I045_llm_uncertainty_main.zip`（786,333字节），通过压缩包目录检查并静态审计指标和聚合脚本。当前仓库只有极少提交，未见论文输出缓存或固定数据快照，未重跑GPT-3/3.5/4、Vicuna或LLaMA 2，故以下表值是论文审读而非模型实验复现。

## 研究问题与对幻觉综述的准确定位

论文问的是：只有黑盒文本接口时，LLM能否给自己的固定答案输出有意义的置信度？它把方法拆成三层：

1. **Prompting**：Vanilla、Chain-of-Thought、Self-Probing、Multi-Step与Top-K，让模型直接报0–100置信度或多个候选及概率。
2. **Sampling**：Self-Random、Prompt Paraphrase与Misleading Hints，多次查询得到答案变化。
3. **Aggregation**：Consistency、Avg-Conf与Pair-Rank，把多答的频率、口头置信度或候选排序变成最终答案与置信度。

评价又明确拆为：**calibration**（置信度数值与经验正确率是否匹配，ECE）和**failure prediction**（能否把正确、错误回答排序分开，AUROC/AUPRC）。这对幻觉检测很重要：置信度可以作为错误风险信号，但本文只在短答案/选择题上以exact correctness作为标签，没有标注开放生成中的事实claim、无来源陈述、矛盾、严重度或span。因此它是“幻觉风险估计的近邻证据”，不是开放域幻觉检测器本身。

## 数据、模型与实验单位

八个数据集覆盖五类任务：GSM8K和SVAMP（算术）、BIG-Bench Date Understanding与Object Counting、StrategyQA（常识）、Sports Understanding、MMLU Professional Law与Business Ethics。模型为GPT-3、GPT-3.5、GPT-4、Vicuna-13B、LLaMA-2-70B-Chat。

任务被约束为唯一数值或有限选项，答案由字符串/选项相等判定。这使Consistency较干净，却避开开放文本的同义表达、部分正确、多claim与长回答“任一claim错”问题。数据集样本量、是否完整测试集/抽样及每个API调用的确切模型快照没有在主实验表旁充分给出；模型规模、指令训练、RLHF、闭源API版本和基准能力共同变化，所以“模型能力/规模提升导致不确定性更好”只能视为跨模型观察，不能作单因素因果结论。

## 五种prompt策略究竟测什么

- **Vanilla**直接要求答案与置信度，最接近口头自评，但数字可能是语言风格而非概率信念。
- **CoT**先推理再报置信度；它同时改变答案正确率、文本长度与信心，不能仅解释为更好的后处理校准。
- **Self-Probing**在下一轮让模型反思先前答案；第二轮看到自己的答案，可能测自我一致性、说服效应和对既有立场的承诺。
- **Multi-Step**逐步报置信度并取乘积。乘积隐含步骤条件独立/概率可乘及步骤划分可靠；步骤越多乘积机械越小，长度与任务难度混淆。
- **Top-K**要求多个候选和各自概率。模型不一定给出归一分布，数值可能不和为100；Pair-Rank丢弃数值只取次序，Avg-Conf则依赖数值尺度。

论文附录的“confident GPT/cautious GPT”人格提示只使汇总指标轻微变化（表7：accuracy .7103/.6983，ECE .2741/.2812，AUROC .5679/.5946），没有显著检验；不能把口头谨慎直接等同真实校准。

## Vanilla结论：ECE改善与错误识别必须分开（PDF6–8）

表2（数值均×100）中，平均ECE从GPT-3的52.0、Vicuna46.1、LLaMA2 43.6、GPT-3.5 37.7降到GPT-4 18.0；平均AUROC为51.3、52.5、56.4、55.1、62.7。整体支持更强模型往往更好，但并不严格单调：LLaMA2平均AUROC 56.4高于GPT-3.5的55.1。GPT-4仍只有.627 AUROC，离可靠筛错较远。

表2的类别方向必须按源码解释：`y_true=correct`、`y_confs=confidence`，PR-P是正确类的AP，PR-N通过`1-y_true, 1-y_confs`把错误类当正类。因此GPT-4平均PR-P 78.4、PR-N 34.2；论文正文把AUPRC-Negative与筛错联系才合理。AP强依赖类别先验，GPT-4高PR-P部分来自较高正确率，跨模型/任务不可脱离prevalence直接比较。

最重要的反例是PDF8明确给出：GPT-4在GSM8K用CoT准确率93.6%，几乎每题都报100%，ECE却仅.064。数值校准看似优秀，原因只是准确率接近饱和置信度；它几乎不提供实例级失败排序。故**低ECE不等于模型知道自己何时错**。反过来，好的AUROC也不保证数值能解释成概率。综述必须并列报告calibration、discrimination与selective risk，而不能只选最好的一项。

## 多答采样的主结果及其边界（PDF8、21–22）

GPT-3.5、M=5时，表3五数据集平均：Self-Random+Consistency ECE .187、AUROC .730；Misleading+Consistency .173/.696；Prompt paraphrase .243/.692；单答CoT .250/.564；单答Top-K .178/.652。GSM8K最醒目，Self-Random AUROC .927，相比CoT .548，表明答案稳定性在算术上是强烈风险信号。

但采样响应来自同一模型与同一问题，强相关，不能按五个独立模型理解。Self-Random temperature=.7改变生成分布；口头置信度方法多用temperature=0，方法比较同时改变了解码。Misleading Hints测到的不仅认识不确定性，还包括模型的暗示敏感性；提示可能正确、错误、强弱不同。Appendix B.6分弱声明、强声明、外部来源，但提示真实性和影响没有被独立标注。

Figure7将M从1扩至13，边际收益趋缓；附录另称某研究将candidate set设为4，而主表M=5。需要把“原始回答是否计入M”“hint数量”和“总查询次数”统一，才能准确比较成本。每题5或13次API调用还使性能—费用—延迟成为核心维度，论文只给原则性讨论，没有等预算比较。

Consistency将最高频答案的频率作为置信度。对固定选项合理，但多数一致可能是稳定错误；训练数据中的共同偏见不会因多次采样消失。开放生成若用exact string会把同义正确答案当分歧，若用语义聚类又引入阈值和嵌入模型，本文没有处理。

## 三种聚合公式与表4的正确读法

Consistency是候选答案的频率。Avg-Conf的式(2)不是普通“该答案置信度均值”，而是匹配该答案的置信度之和除以**所有采样置信度之和**；它是口头信心加权的答案份额。源码`vis_aggregated_conf.py`与此一致。若所有置信度相等，它退化为Consistency；若口头数字跨采样不可比较，权重也失去概率含义。

Pair-Rank依据Top-K中两候选先后关系学习类别分布。表4在GPT-4、Top-K+Self-Random、六数据集上：

- ECE均值：Consistency .120、Avg-Conf .148、Pair-Rank .069；Pair-Rank最低。
- AUROC均值：Consistency .669、Avg-Conf .669、Pair-Rank .676；Pair-Rank均值略高。
- Avg-Conf在Law、Date、Sport、Strategy、Ethics五个数据集AUROC最高，但GSM8K只有.410，远低于Consistency .844和Pair-Rank .803，故“5/6胜出”与“宏平均不胜”可同时成立。

表头“Mean & Var”中的±值没有清晰说明是何种重复随机实验的方差/标准差；六列本身差异远大于所列数值。表中每种聚合还可能选择不同最终答案，所以AUROC变化既来自confidence排序，也来自base accuracy变化；严格比较应固定同一最终答案，只替换置信度，再另报joint decision效果。

## 表13与主表存在未解释数值冲突

PDF23表13把GPT-3.5五数据集汇总后，Self-Random+Avg-Conf平均ECE .148、AUROC .745；Misleading+Avg-Conf .142/.702，支持“口头置信度与答案分布组合优于只看Consistency”。但Top-K的GSM8K在表13为ECE 39.8、AUROC59.9；PDF8表3和PDF20表10却为ECE19.6、AUROC58.5。仅ECE相差20.2点，并会把五域平均从约20.6推到24.6。正文未解释是否不同run、样本、prompt或版本，引用Top-K平均时应标注该冲突，不能把表13当无条件复现主表。

## 白盒基线并非在所有指标、所有任务都胜（PDF9、17–18）

作者比较GPT-3的sequence probability、长度归一sequence probability、key-token probability与黑盒verbalized confidence。Top-K表5中，白盒AUROC往往较高：GSM8K verbalized .5405而三白盒约.6929–.7061；StrategyQA .5034而token .6061。但ECE不统一：Business Ethics verbalized .1820优于所有白盒；GSM8K raw seq-prob ECE .0773虽低而其accuracy仅.1152，仍可能是低概率与低正确率的机械匹配。

CoT表6也有反例：Date token-prob AUROC .4027，低于verbalized .5036；各白盒方法跨任务互有胜负。摘要所称平均AUROC约`.522→.605`可作总体观察，不能简化为“白盒全面更好”。此外白盒概率受答案长度、tokenization及生成路径影响，与“答案正确概率”不是同一随机变量。

## 当前官方源码审计：可复现性与实现语义

`utils/compute_metrics.py`确认：accuracy为正确比例；AUROC以正确为正；PR-P为正确AP；PR-N把错误和`1-confidence`作为正类；ECE用`netcal.metrics.ECE(n_bins=10)`。论文未在主文显著说明10等宽/库默认分箱，ECE对分箱数、空bin和样本量敏感，需固定实现版本。

`vis_aggregated_conf.py`的Consistency取众数频率；Avg-Conf按上述全局置信度份额；Multi-Step直接连乘各步数值。代码还有以下风险：

1. 输出CSV表头写到`auroc,auprc_p,auprc_n`，实际行在AUROC后额外写`aurc`，导致从该列起整体错位；若后处理按表头读取，会把AURC误当PR-P、PR-P误当PR-N。
2. `vis_aggregated_conf_top_k.py`在正式计算前保留`pdb.set_trace()`，且定义`search_vis_answers_top_k(result_dict, task_type)`却以额外`num_ensemble=`参数调用，当前脚本会先停在调试器，继续后再触发`TypeError`，不能原样复现Pair-Rank表。
3. Pair-Rank代码从Python `set`建立类别索引、随机初始化参数且未设seed；类别顺序和优化起点不固定。论文描述类似pairwise概率拟合，代码损失却是`-sum(rank_matrix * ratio)`而不是常见的负对数似然`-sum(rank*log ratio)`，应以发布实现为准并解释这一差异。
4. Pair-Rank只优化1000步SGD，无收敛检查；Top-K候选集合若缺失某选项，其概率空间只覆盖出现过的答案。不同run可能得到不同值。
5. 仓库没有论文使用的完整模型响应、结果CSV与环境锁定；静态审计能确认定义，不能验证表2–13的数值生成链。

这些问题不自动否定论文表值——论文作者可能用过更早的内部版本——但当前仓库不足以让第三方一键复现。综述中应把“正式报告结果”与“当前代码可执行性”分栏。

## 统计与测量层面的关键问题

1. **ECE不是proper scoring rule且受accuracy影响。** 应补Brier score/NLL、reliability diagram、adaptive/classwise ECE，给bootstrap区间。
2. **AUROC不反映部署阈值和错误稀有度。** 应报错误类AUPRC、risk-coverage/AURC及目标coverage下风险；源码虽计算AURC，主表未系统使用，CSV还错列。
3. **AP不可跨prevalence裸比较。** 正确率不同会改变PR-P/PR-N基线；至少给随机基线和normalized AP。
4. **宏平均掩盖异质性。** 表4 Avg-Conf的5/6局部胜利被GSM8K反转；应同时报dataset macro、样本micro和分任务层级模型。
5. **没有成对不确定性。** 同一题被多方法评价，适合question-level paired bootstrap/DeLong或层级bootstrap，而不是只报点估计。
6. **答案与confidence共同改变。** prompting/sampling/aggregation既改预测又改分数，应拆成fixed-answer uncertainty quality与joint system utility。
7. **暗示/采样不是独立重复。** 需要测同题相关、有效样本量和不同随机seed；M增加的收益应按总tokens/API成本比较。

## 可直接推进的研究问题与实验

1. **校准—筛错—选择性预测三联评估：**统一报ECE/Brier/NLL、AUROC/错误AP、AURC与80/90/95% coverage风险，防止“93.6%准确+全100置信”的假优秀。
2. **固定答案消融：**先生成一次答案，再让不同方法只估该答案confidence；另做允许改答案版本，分离估计质量与纠错收益。
3. **稳定错误压力测试：**构造常见错误、训练记忆错误、错误前提和同一错误释义，检验Consistency是否高置信地确认共同偏见。
4. **开放文本语义聚类：**exact、规范化、NLI双向蕴含和claim-level聚类并报敏感性；把“措辞变化”与“事实变化”分开。
5. **Multi-Step长度控制：**相同推理人为切成不同步骤，测试乘积是否仅因步骤数下降；改用条件概率或log-score并校准。
6. **Pair-Rank可复现修复：**去断点、修函数调用/CSV表头、固定类别顺序与seed，明确使用ratio还是log-likelihood，发布raw responses和环境后重算表4。
7. **等预算曲线：**以总调用、tokens、延迟和费用为横轴比较M=1…13；与小型外部验证器、检索证据核验做相同预算对照。
8. **从短答案迁移到幻觉：**把confidence下沉到atomic claim，分别标世界真实性、上下文支持和不可核验；回答级风险用最大claim风险、错误claim比例和严重度聚合。

## 对综述可使用的结论

本文最可靠的价值不是证明某一方法普遍最好，而是把黑盒不确定性估计组织成prompt—sampling—aggregation，并用校准和失败预测揭示两种能力不等价。多答一致性在算术等任务显著改善筛错，口头置信度可为聚合补充信息；但方法、任务和指标之间高度异质，没有稳定赢家。尤其应引用GPT-4/GSM8K“近乎全100%置信、accuracy93.6%、ECE.064却难以筛错”的例子，说明低ECE可能来自高准确率而非实例级自知。当前源码确认10-bin ECE和类别方向，同时暴露Pair-Rank脚本不可直接运行及CSV错列，正式表值仍需基于固定responses的独立重算。
