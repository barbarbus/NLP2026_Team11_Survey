# I100 · G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment

Yang Liu、Dan Iter、Yichong Xu、Shuohang Wang、Ruochen Xu、Chenguang Zhu。资料库arXiv:2303.16634v3，2023-05-23，11页。https://arxiv.org/abs/2303.16634 。

## 阅读和证据范围

细读正文1–8页与全部附录10–11页；参考文献不计被引论文已读。目视第4页Table 1、第6页Table 2/Figure 2、第7页Table 3。官方 https://github.com/nlpyang/geval 固定commit `6f84404ce4503d2ba0cde0293c5d402ecf2976a8`，ZIP及provenance在 `../../qa/I100_official/`。阅读README、gpt4_eval.py、meta_eval_summeval.py、consistency/fluency提示，独立解析四份公开响应文件并重算相关性。

脚本 `../../sources/audit_geval.py`、结果 `../../qa/I100_official/response_audit.json`。由于环境无SciPy，本次独立实现平均秩Spearman、Pearson及处理并列的Kendall tau-b，未执行作者脚本。没有调用API或新生成评分，缓存复算不等于历史模型完整复现。

## 1. 研究问题与综述定位

核心问题是开放生成文本的多维质量评价，不是单独的新幻觉数据集。G-Eval用LLM产生任务评价步骤，再以填表方式输出评分；其中consistency/groundedness才直接涉及来源事实支持，coherence、fluency、relevance、engagingness不能全部叫幻觉检测。

reference-free指不需要人工目标答案，不代表不需要source或知识。摘要一致性输入原文，对话groundedness输入对应事实；fluency提示则只给摘要。应按维度分别记录资源，而非给整个方法一个统一“无证据”标签。

它与GPTScore不同：后者用候选文本生成似然，G-Eval生成评价标签。与I065同属直接LLM裁判，但有预生成步骤与多次采样评分；与I095蒸馏不同，它部署时仍需LLM裁判推理。

## 2. Auto-CoT究竟是什么

先把Task Introduction、Evaluation Criteria交给LLM生成Evaluation Steps，然后将该步骤与每个待评文本一起输入。这个CoT更接近任务级操作清单，不等于每条实例都输出并验证了完整推理链。公开提示文件保存固定步骤，评价输出又要求scores ONLY，不能声称每个分数附有可核实的解释。

步骤可帮助细化rubric，也可能偏离目标：coherence步骤要求覆盖文章关键点，部分混入relevance。论文Figure 1还出现“1到10、最低1最高5”的冲突，正文/附录示例是1–5；不能按示意图误写所有量表1–10。Fluency官方文件为1–3且没有Evaluation Steps，不能笼统宣称所有维度都用了完全同样的CoT结构。

对话engagingness附录既要求brief explanation又在表单要求scores ONLY，潜在格式冲突需要实际输出审计。本次没有取得全对话响应，不推断其失败率。

## 3. 概率加权评分及有限采样

原式score=Σ p(si)si，意在减少单整数集中和并列。若p只指选定数字token概率而非归一到合法分数集合，应说明非法token质量怎么处理；论文称normalization，但式子本身没有额外分母，不擅自补成不同公式。

论文GPT-3.5是text-davinci-003、temperature0；GPT-4当时无输出token概率，所以n20、temperature1、top_p1采样20次估计分布。GPT-4实现不是读取真实完整logits；若20个输出都为合法分数，频率加权等于20个数字均值。

20次均值对整数1–5仍是.05网格，不是数学上任意连续精度。假设独立且范围1–5，均值标准误上界2/√20≈.447；这是保守数学界，不是作者实际误差估计。多次采样同时增加推理预算，和单次整数的对比不只改变“概率”，也改变计算量与方差。

输出均分不是无幻觉概率，4分不意味着80%事实正确；温度变换还改变标签分布。要测风险需要独立校准、阈值、coverage和错误严重度，本文相关性不足以直接提供这些保证。

## 4. 数据与相关性层级

SummEval评四维，来源CNN/DM；Topical-Chat评naturalness/coherence/engagingness/groundedness；QAGS评CNN/DM与XSum摘要一致性。三类benchmark覆盖两任务，不是三个独立开放域事实核查场景。

官方meta_eval按doc_id分组，在同文章多个候选间计算Pearson/Spearman/Kendall，再对有效文章等权平均；若人评分或模型分在组内恒定则跳过。这个“summary-level”实际是文章内候选排序平均，不是1600行pooled相关，也不同于I037系统均分Kendall。本文表格未充分展开这个分母，源码补充了关键协议。

一致性天花板文章可能因人评全同而被排除，模型全部打同分也导致剔除；不同方法可能有不同有效文章集合，横比须共同完整文章或显式报告coverage。不能把不定义相关的组当自动正确，也不能只从较高条件相关推断总体评价都可靠。

## 5. 原论文主要结果与限定

Table 1 G-Eval4四维Spearman .582/.507/.455/.547，平均.514；UniEval平均.474，绝对+.040。摘要中.514是四个相关系数的平均，不是所有摘要的单一相关、更不是51.4%accuracy。G-Eval3.5平均.401，低于UniEval，不支持所有LLM都优于专用模型。

去CoT平均Spearman .500，去Probs .502，完整.514；改进.014/.012不附充分多种子或配对CI，不能只靠数值称稳定显著。去Probs Kendall平均.446反高于完整.418，作者认为并列导致；但并列本身是量表性质，tau-b有显式修正，不能凭不同方向就宣布不符合论点的统计量“不公平”。应报并列比例、共同样本、多个秩指标与人工比较。

Table 2 Topical-Chat实际表头r/ρ、正文也说Pearson/Spearman，caption却写Spearman/Kendall；以表头读，勿误引.575为Spearman。G-Eval4平均r .575、ρ .588，3.5为.574/.585，几乎相同；UniEval coherence Pearson .602高于G-Eval4 .594，3.5 engagingness/groundedness还高于4。不能写4在所有维度最佳。

Table 3 QAGS：G-Eval4 CNN Pearson .631低于BARTScore .735、UniEval .682；XSum .558高于UniEval .461，平均.599。Spearman CNN .685、XSum .537。总体收益更大来自抽象XSum，但不能只用两个域证明抽象性是唯一因果因素。QAGS原标注、来源增强协议与模型/版本需对齐I062记录。

“GPT4比3.5好说明模型更大”只是作者解释，训练数据、对齐、接口、温度/采样均不同，且GPT4架构参数未在本文独立控制，不能作单变量规模因果结论。

## 6. 官方代码版本和输出解析

当前gpt4_eval默认gpt-4-0613、temperature2，而论文2023-05版本写temperature1。不能用现代码设置覆盖历史论文事实，也不能把历史实验表直接当当前默认复现。每条prompt放system role、max_tokens5、n20；截断与模型格式行为会影响评分。

异常时含limit则等待重试，其他异常忽略该例且计数；输出文件只写成功例，未必完整覆盖输入。因此要核对保存行数和缺失机制，不能只信脚本跑完。README示例--prompt与代码--prompt_fp名称不完全一致，复现应按实际参数。

parse_output正则 `^ ?([\d\.]+)`只接受起始至多一个空格的数字串，非匹配直接0，不是合法量表内最低分。换行、两空格、"Score: 4"都可被判0；解析失败被当质量差，与真实评分混淆。应保留validity，比较严格原解析与经过人工规则确认的宽松解析，不能默默修后仍称原成绩。

## 7. 本次对已发布四份响应的实际复算

各维1600行、100文章、每行20响应，共每维32000响应。Coherence与relevance无原解析失败；consistency159个失败（约.497%响应）、fluency7个失败。例包括换行开头Possible score、两空格后2，以及截断/表情文本。以上是独立遍历公开输出计数，没有API调用。

沿原规则零填后，各维有效文章100/96/98/100。文章内平均Spearman约.571067/.500666/.505785/.563621；平均Kendall .462578/.419867/.455399/.452915。pooled Spearman约.571723/.504700/.469571/.589804。具体完整值、hash保存在审计JSON。

这些数值不完全等于论文表1的.582/.507/.455/.547，特别fluency不同。只证明当前发布响应+所读元评估逻辑与表格不能逐项对上，可能版本/模型/解析/输入差异；未取历史全部commit，不能声称论文造假或已严格复现。现有响应仍是有价值的可审计证据。

每例20次分数聚合沿原脚本sum/len；文章均值用独立统计实现，相关计算未调用作者脚本。当前重算不冒称二进制逐位一致，完整精确值以审计JSON为准。

## 8. 偏好LLM文本实验的证据强度

按人类偏好将人写/GPT3.5摘要对分为human好、LLM好、相当三组，再用G-Eval4打分。Figure 2三组LLM均分都较高，包括人类偏好human的组。这里“always”只描述组均值，不是每条都偏好LLM。

作者明确原人类判断Krippendorff alpha .07很低；分组本身不稳、长度/风格/信息量可能不同，所以结果提示偏好风险，不是已经隔离“认出同家族文本而自我偏爱”的因果机制。判分者GPT4、生成者GPT3.5，也不是同一模型直接评价自己的输出。

使用其分数作奖励可能强化偏好是合理风险假说，本文没有实际训练奖励模型后证明自我强化。后续应做内容等价风格改写、长度匹配、盲来源标签、多家族评委与高一致性人评，分离作者识别、风格偏好、真实质量差异。

## 9. 已提出并推进的研究问题

问题A：.514是否代表强幻觉检测？已确认它是多维平均、文章内相关，consistency另有.507；没有AUROC、阈值风险与跨度定位证据。需在同事实错误金标上报检测和校准，不能凭总体质量相关取代。

问题B：probabilities提升来自什么？已厘清GPT4的20次频率均值与3.5 token概率不是同一估计；应固定采样预算比较众数、均值、单次、多温度和非法输出策略，另评重复运行方差。本次只重算缓存，不虚构新采样。

问题C：相关性剔除哪些困难文章？本次实查有效文章分母，后续按各方法共同文章重算，并把常数预测的无法区分作为独立覆盖失败报告，不让剔除难例隐性抬高排名。

问题D：提示是否严格测目标？Coherence混覆盖、fluency无步骤、对话解释/仅数字指令冲突已定位；应固定专家rubric、使用最小错误/遗漏/流畅改写对照，检验评价目标漂移，与I065/I043连接。

## 10. 综述接口与待办

对应C04评估方法框架、C14人类一致性与报告、C16测量有效性；和I037共用SummEval参照，I065是直接LLM评价对比，I095提供以LLM标签蒸馏降低部署成本的替代路线。综述可写G-Eval通过任务步骤和评分分布改善部分人评相关，但对采样、解析、相关聚合和模型偏好敏感，不将它称通用真实性概率。

待补：原历史API/代码版本、完整3.5概率归一化、Topical/QAGS原始输出、偏好实验逐例数据；共同文章与解析敏感性、原加法并列处理及配对置信区间。本轮未运行模型，全任务目标继续。

程子晨参与全部统筹，其余成员按定义/rubric、方法、统计、复现归档对接；建议不计作成员已执行署名。
