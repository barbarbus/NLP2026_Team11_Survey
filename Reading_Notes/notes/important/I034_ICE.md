# I034 ICE：四个示例可校准摘要裁判，但相关性、分布与同源偏好限制了“SOTA”结论

## 来源、版本与核验范围

Sameer Jain、Vaishakh Keshava、Swarnashree Mysore Sathyendra、Patrick Fernandes、Pengfei Liu、Graham Neubig、Chunting Zhou，*Multi-Dimensional Evaluation of Text Summarization with In-Context Learning*，Findings of ACL 2023，ACL Anthology 2023.findings-acl.537，DOI `10.18653/v1/2023.findings-acl.537`，正式版页8487–8495。本地为arXiv:2306.01200v1（2023-06-01）紧凑排版PDF共7页，正文、参考和附录A–E全部逐页阅读；目视核对PDF3表1、PDF4图2–4、PDF5表2，保存于`Reading_Notes/qa/I034_p3.png`、`I034_p4.png`、`I034_p5.png`。

同时静态审计作者[官方ICE仓库](https://github.com/JainSameer06/ICE)当前main：仓库只有3次提交，README仍写“Detailed steps to reuse and reproduce be added soon”；检查`task_prompts.json`、运行脚本、`src/inContextEvaluator.py`、预处理示例和1536条公开缓存预测。官方main压缩包已完整保存为`Hallucination_Evaluation_Library/code/I034_ICE_main.zip`（12,760,631字节，压缩目录可正常列出）。未调用已停用的`text-davinci-003`，没有把缓存审计冒充重新运行模型。

## 问题设定：多维评价中只有consistency直接对应幻觉（PDF1–2）

ICE用同一个LLM和少量`(输入、摘要、人工分数)`示例分别预测四维0–1分：

- consistency：摘要细节是否准确复现source事实；prompt包含全文source。
- relevance：是否覆盖重要信息；默认prompt包含人工reference，不包含source。
- fluency：单句语法与书写质量；只给摘要。
- coherence：句间组织和整体结构；只给摘要。

因此本文对我们的主线贡献是**source-conditioned摘要忠实性裁判**，不是开放世界事实核验。流畅、连贯、相关不应被合成一个“幻觉分”；一个完全流畅且覆盖重点的摘要仍可含事实错。relevance以单篇reference为目标，还可能把reference遗漏/措辞偏好带入分数。

方法的“learning-free”仅指不更新模型参数；它仍使用SummEval专家标签作为四个in-context监督点，且每个测试prompt都调用175B的`text-davinci-003`。更准确的表述是**无梯度、每次推断时少样本监督**，不是无监督或无训练数据。

## Prompt、示例选择与数据隔离（PDF2、7）

默认四个示例是GPT-3上下文窗口能容纳consistency全文prompt的上限。作者先从SummEval的100篇CNN/DM文章选4篇，每篇有16个系统摘要，形成64个候选；最后每篇选一个摘要，共4个demonstrations。为防source重叠，将这4篇的全部64摘要从测试移除，余1536条测试。这一点比随机拆摘要更严格，避免同一新闻文章的其他系统摘要同时出现在示例和测试。

两种选法：

- uniform：每篇文章的16个摘要均匀随机选一个，示例分数近似原数据分布。
- stratified：把0–1分成四桶，每桶取一个且来自不同文章；若某桶无人，则从随机已有桶补一个。所谓stratified并不保证始终覆盖四桶，fallback会破坏原定义。

示例池与测试仍来自同一benchmark、同一专家rubric、同一CNN/DM域；这是benchmark内校准，不证明跨数据集、跨领域或跨标签尺度泛化。四篇文章先如何随机选、主表用哪个seed、四维是否分别换摘要，正文信息有限；仓库需要结合运行脚本固定。作者只检验source文章不重叠，未讨论同一16个摘要生成系统在示例与测试中共享导致的system-style泄漏。

## 表1：哪些数字真正达到最好（PDF3）

测试为1536摘要，报告summary-level Spearman `ρ`和Kendall `τ`，对照CTC、BARTScore、UniEval：

- coherence：ICE uniform `.476/.388`，低于UniEval `.591/.424`；stratified`.497/.387`，仍低。
- consistency：uniform`.486/.466`，高于UniEval`.433/.348`和CTC`.425/.340`；stratified仅`.298/.263`，明显崩落。
- fluency：uniform`.366/.328`、stratified`.397/.348`，均低于UniEval`.445/.349`；stratified的τ`.348`与UniEval`.349`几乎相同但不是最好。
- relevance：uniform`.467/.384`，stratified`.485/.396`；ρ仍低于CTC`.495`，但τ分别超过CTC`.364`与UniEval`.343`。

所以“relevance和factual consistency达到SOTA”只有在**consistency两指标、relevance的Kendall τ**上成立；relevance Spearman并非最好。论文显著性附录只比较uniform ICE与UniEval：1000次bootstrap，每次抽80%测试，称Kendall τ下consistency和relevance、Spearman下consistency在`.05`显著，relevance Spearman不确定。它没有与relevance Spearman最强的CTC直接做显著性比较，也没有多重比较校正。

bootstrap描述没有说明按文章还是按摘要抽样。1536摘要来自96篇文章、每篇16个系统输出；若把摘要当独立单位，重复抽样忽略同article相关性，区间会过窄。应使用article-cluster bootstrap，或同时按文章与系统做分层/双向重采样。

## 分布实验实际说明“模仿标签先验”，不等于校准（PDF3–4）

SummEval consistency和fluency严重靠近高分。uniform示例也多为高分，使预测分布靠近人工分布；stratified故意展示低分，consistency预测被拉到中部，ρ从`.486`掉到`.298`。这支持ICL裁判会吸收示例的**标签分布先验**，却不能仅凭直方图称“calibrated”：预测分布和真值边际相似，不表示条件意义上`predicted .8`的样本有对应质量，也不表示逐样本误差小。

作者承认uniform在低概率低分区域可能没有示例，那里校准差，但仍推荐uniform，因为总体排序稳定。这会牺牲我们最关心的少数幻觉/严重不忠实样本：一个指标在大量近满分摘要上相关较高，未必能召回低分尾部。应分数段报告MAE、严重错误召回、risk-coverage和reliability curve，而非只看rank correlation。

图3只在200条成本控制子集上比较3组示例。目视图中consistency约`.59/.59/.50`，最大差接近9点，fluency约`.41/.41/.36`约5点；正文称最大“about 7 points”只是近似且未给数表/区间。3个seed不足以支持“robust to selection”的强结论。

图4同样只用200条：coherence从1示例约`.36`到2个`.51`后基本持平；relevance从`.32`到`.51–.55`；consistency从`.54`到2个`.67`，随后降至4个约`.59`；fluency约`.40–.45`波动。不是“示例越多越好”，更像2个已捕获大部分任务/尺度信息，后续收益依维度与所选样本而变。四例上限又是旧4K上下文模型的工程约束，不应推广到现代长上下文judge。

## 官方实现揭示的解析与确定性问题

`task_prompts.json`确实存有自然语言定义：consistency要求0–1且准确复现source，relevance称“capture important information from a reference text”。但仓库提供的`run.sh`与`runall.sh`均传入`--exclude_description`，所以相应运行不会把这些定义放入prompt；模型主要从四个例子、字段名`Consistency:`等推断任务。论文把方法描述为“natural language prompt”，读者很容易误以为主结果使用完整rubric。若不关闭定义，coherence提示又写“summary of given text”，而实际构造时不提供source，措辞和输入不完全一致。

`inContextEvaluator.py`固定`text-davinci-003`、temperature 0、`logprobs=5`。类构造器给`num_candidates=3`默认值，解析函数也确实只会读取`response["choices"][0]["text"]`；但CLI将该参数设为required，发布运行脚本明确传`--num_candidates 1`，所以不能把“三候选只读一个”归因于论文主运行。真正可确认的是logprobs没有参与最后分数，且temperature 0不保证远程API版本长期确定。

分数解析用正则`\d*\.?\d+`取第一段数字，再转float；没有验证0≤score≤1、没有处理无数字/科学计数/解释中先出现别的数字，也没有记录解析失败。API异常可重试至20次，达到阈值直接退出整个运行；timeout异常日志引用未定义变量`i`，该路径可能再触发错误。仓库README缺依赖版本、完整复现命令和论文commit/tag；当前main只能算作者资源快照，不是已验证的一键复现包。

相关计算直接对1536个预测与`expert_*_mean`调用SciPy`spearmanr`和`kendalltau`；SciPy默认Kendall tau-b会处理大量并列分，但论文仅写Kendall-Tau。实现不验证示例/测试重叠，只信任预处理文件。发布脚本又传`--sample --sample_size 100`，但当前`getTestData`只读整个JSON，`sample/sample_size`没有在该路径实际抽样；主结果应以缓存文件的1536条为准，而不能从参数名推断只评100条。

缓存静态审计得到非常离散的输出：coherence 17个不同值；consistency仅4个值，`1.0`有1326/1536（86.33%）、`.8`有200、`.9`有8、`.5`仅2；fluency 14值，其中`1.0`671、`.93`525；relevance 9值，其中`.83`836、`.93`189。全部在0–1内，但这是成功解析后缓存，不能说明失败回复不存在。尤其consistency几乎只会输出`.8/1.0`，排名相关`.486/.466`并不等于能给低事实性摘要提供有分辨率的严重程度分数。后续复现应固定这些原API响应/预测，而不是尝试用同名但已退役模型重跑。

## 表2：GPT-3摘要实验只证明系统均值排序一致（PDF5、7）

从Goyal等500篇CNN文章取100篇；GPT-3、BRIO、T0各一摘要，即300摘要，3名标注者按1–5给四维分。附录只有一句“使用SummEval指南”，没有标注者背景、培训、盲化、系统顺序、报酬、agreement、争议裁决或置信区间。

人评系统均值：GPT-3 overall `4.80` > BRIO `4.65` > T0 `4.27`。ICE均值也同序：`.937 > .929 > .904`，且四个维度各自同序。这个结果只说明**三个系统的aggregate ordering相同**；论文没有报告300条样本级相关、pairwise agreement、系统差异显著性或每篇文章上是否选对。consistency `.996/.993/.981`、fluency`.994/.993/.985`高度饱和，GPT-3与BRIO只差`.003/.001`，不能凭排序宣称精确对齐。

裁判`text-davinci-003`本身属于GPT-3家族，被评对象也有GPT-3摘要；GPT-3居首可能部分来自self/family preference、风格熟悉度或训练分布，而非更准确识别事实。实验没有更换异构judge、匿名风格、长度匹配或人工最小对，无法排除这一替代解释。

ROUGE-L只有overall列，给GPT-3/BRIO/T0 `22.09/28.20/26.63`，排序与人不同。BARTScore固定使用source→hyp一个版本，故四维数字完全相同：`-1.25/-0.71/-.96`；它本就不是四个独立维度的prompted metric。用ICE四个不同prompt与同一BARTScore复制四列比较，对“多维识别能力”并不对称。

作者解释传统指标奖赏模仿reference，而GPT-3零样本不模仿reference；这一解释对ROUGE合理，对source→hyp BARTScore不完全等价。ICE的relevance本身也使用reference，并非全程reference-free。更保守的结论是：在这个100文章三系统小样本上，ICE的系统均值排序恰与人评一致，而ROUGE/BARTScore没有。

## 局限、与幻觉综述的关系及研究问题

论文承认只做摘要、部分分析因费用用200样本、依赖175B外部模型。还应增加：闭源模型退役使原实验不可重跑；示例来自测试benchmark同分布；标签分布严重偏斜；prompt输出解析脆弱；只测相关不测事实错误定位；系统均值实验可能self-bias；没有成本、延迟、失败率。

1. **ICL示例是在教rubric还是教分数先验？** 做label-shuffle、错误分数、只保留输入/只保留标签、跨数据集示例实验；比较相同summary在不同示例分布下的分数移动。
2. **尾部幻觉检测是否被总体相关掩盖？** 以人工consistency阈值构造严重错正类，报告PR-AUC、recall@budget、分数段MAE和article-cluster置信区间。
3. **reference relevance与source faithfulness能否解耦？** 对同一摘要分别给source、reference、二者和冲突reference，观察是否把reference遗漏当不相关、把reference自身错误当真。
4. **同源judge偏好有多大？** 交叉使用GPT、Claude、开源异构judge评GPT/BRIO/T0，控制长度和风格；人评文本去系统标识，检查judge×generator交互。
5. **数值打分是否需要解释/证据？** 要求先定位unsupported span和source证据再打分，与直接首数字比较；记录格式失败、越界、重试与token成本，并验证解释是否忠实。
6. **示例选择应优化什么？** uniform保留先验、stratified覆盖尾部，可用混合策略：一部分按真实分布，一部分覆盖罕见错误；目标用尾部风险或校准，而非只优化总体Spearman。

**综述可用结论：** ICE证明旧GPT-3在仅四个SummEval专家示例下即可产生与人评中度相关的多维摘要分数；uniform consistency达到`ρ=.486, τ=.466`，relevance仅τ最好。示例分布会显著改变预测，尤其consistency由uniform`.486/.466`降至stratified`.298/.263`。它支持“ICL可充当低样本source-faithfulness judge”，但不支持“无需标注”“稳健跨域”或“GPT-3摘要已获可靠人类级评价”。
