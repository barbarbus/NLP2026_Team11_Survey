# I050 GraphEval：把回答拆成自由文本三元组可改善NLI，但覆盖、长度效应与自评纠错仍未证实

## 来源、版本与核验范围

Hannah Sansford、Nicholas Richardson、Hermina Petric Maretic、Juba Nait Saada，*GraphEval: A Knowledge-Graph Based LLM Hallucination Evaluation Framework*，KiL'24（KDD 2024同场workshop），arXiv:2407.10793v1（2024-07-15）。本地PDF共12页，正文、讨论、KG与纠错prompt逐页阅读；目视核对PDF6表2、PDF7表3–4、PDF10–12全部prompt。

未找到作者公开实现或实验数据仓库，因此没有可打包的官方源码；当前文件夹保留论文PDF、逐页全文与证据页。以下数值复算自论文表格，不等于模型级复现。实验依赖Amazon Bedrock上的Claude 2；论文未固定服务端版本、seed或采样轨迹，今天无法严格重建原调用。

## 测量对象与方法边界

GraphEval只评估**closed-domain consistency**：回答是否与给定context一致，不检查context本身是否真实，也不覆盖模型训练知识偏离或开放域事实。流程为：

1. 用Claude 2把待评回答一次性转成自由文本三元组`(entity 1, relation, entity 2)`；不建立实体/关系类型、属性或统一ontology。
2. 将每个三元组分别作为hypothesis，与完整context一起交给现成NLI事实一致性模型，得到“含幻觉”概率。
3. 任一三元组概率大于0.5，就把整个回答判为不一致，同时返回触发的三元组。

它更准确的定位是**LLM claim decomposition + NLI aggregation**，而不是传统意义上的知识图谱推理：图没有对context建模，没有路径搜索、约束推理或实体链接；“KG”主要提供结构化原子化接口。优点是同一NLI不再一次吞入整段回答，能返回疑似错误的命题单位；但其有效性取决于抽取完整性、三元组语义保真、NLI校准和响应级聚合四层。

## 数据、标签与可推广性

三个数据集全部是英文摘要一致性：SummEval 1600例，consistent比例33.2%，回答/context平均63/359词；QAGS-C 235例、48.1%、49/383词；QAGS-X 239例、48.5%、18/318词。SummEval把人工consistency分数5判正、低于5全判负；这是一种极端二值化，会把轻微局部问题与严重事实错误合并。QAGS标签同样是回答级“所有句子均一致”口径。

论文宣称方法可容易扩展到QA、commonsense等领域，但实证只有摘要。三数据集还共享新闻摘要任务、相近长度与NLI熟悉的蕴含形式，不能据此证明跨领域、长文、RAG对话、多语言或开放域能力。尤其QAGS-X仅18词，作者观察收益接近零；这既可能支持“长回答更需分解”，也可能暴露三元组化损失短句中的修饰和关系细节。

## 表2主结果与独立复算

Balanced accuracy（SummEval/QAGS-C/QAGS-X）：

- HHEM：66.0/63.5/75.5；+GraphEval：71.5/72.2/75.2，增量+5.5/+8.7/**-0.3**。
- TRUE：61.3/61.8/72.6；+GraphEval：72.4/71.7/73.9，增量+11.1/+9.9/+1.3。
- TrueTeacher：74.9/75.6/79.0；+GraphEval：79.2/78.1/79.6，增量+4.3/+2.5/+.6。

九个模型×数据集格的简单平均增量是4.84点，而非6.2；按各数据集样本数加权为约6.23点，恰好对应论文“average improvement 6.2”。这意味着该平均主要由1600例SummEval支配，而不是三个benchmark等权。按模型做样本量加权，增量约5.19、9.83、3.67点，差异很大。

论文报告SE=1.3，但未说明是对九个格、三个模型、三个数据集还是样本做何种估计；九格共享数据、抽取器和NLI，不能视为九个独立重复。没有seed、bootstrap区间或配对显著性检验。更合适的是按document cluster配对bootstrap，并把Claude抽取重复采样和NLI模型作为层级因素。

结论应限定为：在9个设置中8个balanced accuracy不降、1个下降；收益主要来自SummEval/QAGS-C和较弱的TRUE/HHEM。不能写成“GraphEval总能改善NLI”。

## 长文本收益也可能是max聚合的长度效应

响应级规则是`max_i p(hallucination_i) > .5`。若每个真实三元组有独立假阳性率`q`，含`m`个三元组的回答至少一次误报概率为`1-(1-q)^m`；即使q固定，输出越长、抽出的triple越多，越容易被判错。三元组误差实际相关，但方向不消失。

因此“长回答上GraphEval更有价值”至少混合两种机制：更完整的事实覆盖，以及更多次检验导致的敏感度/假阳性共同增加。Balanced accuracy部分抵消类别不平衡，却不能消除按长度变化的阈值。论文没有报告triple数分布、每triple precision/recall、按长度分箱的TPR/FPR或校准曲线。应比较固定triple数、Bonferroni/FDR、top-k均值、noisy-OR和长度条件阈值。

## “系统检查全部信息”的关键证据缺失

KG prompt要求识别实体、共指和关系，并强调“all information”进入图；四个few-shot例均为干净百科句。作者承认抽取阶段会信息损失，却没有人工标注抽取recall/precision。以下信息尤其难稳定装进二实体一关系：

- 否定、模态、传闻/归因、条件句和比较范围；
- 数量、单位、时间区间、事件角色及多元关系；
- 限定词、程度、副词、集合/全称量词；
- 跨句因果、共指、并列与嵌套主张；
- 非命名实体的一元属性和“没有发生”的事实。

Prompt还说不要把“related information”拆成多个triple，因为可能改变意义；这与原子化核验的目标存在张力。例4把“意大利病例是中国3.6倍”整段塞进relation，说明三元组可能只是句子切片而非规范语义结构。若遗漏一个错误事实，后续NLI永远无机会检测；若拆错scope，NLI可对一个不存在于原文的命题作准确但无关的判断。

解释性也只达到“返回自由文本triple”。论文没有验证triple能否稳定映射回原回答span、用户能否理解、定位precision/recall或解释是否忠实。抽取器自己生成了错误triple时，显示它并不等于解释原模型错误。

## 基线是否公平：收益可能来自更短hypothesis

Raw NLI把整段摘要与context比较；GraphEval让同一模型逐个读较短triple。改善可来自：

1. 真正的结构化共指与事实覆盖；
2. 简单的句子/claim拆分，缓解长hypothesis分布外问题；
3. 多次调用后使用any-error聚合，提高敏感度；
4. Claude 2在重述时规范化或补全语义。

论文提到SummaC和FActScore，却没有在相同NLI、相同拆分数和相同调用预算下比较sentence split、LLM atomic claims、SRL/OpenIE或滑窗NLI。因此实验不能把增量特异地归因于“knowledge graph”。对context不送入Claude确实减少一次昂贵LLM输入，但每个triple仍需一次NLI；TRUE/TrueTeacher各需45.5GB，长回答的总延迟和GPU吞吐没有报告。“only one LLM call”不是总计算成本低的证明。

## Claude 2配置带来的稳定性与版本问题

所有需要LLM的实验使用Claude 2，Amazon Bedrock默认`temperature=1, top_p=1, top_k=250`。这是高随机配置，论文却未报告重复次数、抽取一致率、无效Python列表率、解析修复或空KG处理。相同回答可生成不同triple集合，随后任何triple过阈值都会改变最终标签。

Prompt要求在`<python>`标签内返回列表、三字符串、括号/引号完全匹配，但无公开parser，无法知道格式错误怎样处理。模型/API版本也未固定到可重放快照。高质量复现应缓存全部raw completion、解析状态和triple顺序，并至少在temperature 0与多seed下报告响应级一致率。

## GraphCorrect机制与两阶段错误传播

GraphCorrect先对每个被判错的triple调用Claude 2，让它根据context生成“corrected triple”；再调用Claude 2，把旧triple在原回答中替换为新triple，要求不改其他内容。对多个错误triple如何排序、重叠替换或处理前一次修改改变后续上下文，论文没有给出算法细节。

第二步虽然看不到grounding context，但同时看到旧/新triple和完整回答，仍可能无法定位、改错span、破坏语法、遗漏隐含事实或增删其他内容。论文“防止添加/丢失信息”的表述过强；prompt约束不是保证。第一步若检测是假阳性，就会主动篡改正确回答；若纠正triple自身错误，第二步会把新错误写回文本。

## 表3只证明保守编辑，不证明事实正确

GraphCorrect相对Direct Prompt的ROUGE-1/2/L在27个格全部更高，例如HHEM+SummEval的R1 .915 vs .827，QAGS-X .821 vs .649。这说明输出与原文更相似，符合局部替换设计；但原文恰含被认为是幻觉的内容，高相似既可能是优点，也可能代表没有充分纠正。ROUGE不能区分保留正确内容、保留错误内容或用同义词修复造成的低重合。

真正需要同时测：人工事实正确率、正确span保存率、误改率、遗漏错误率、编辑距离和fluency。仅报告原文相似度不能支持“while maintaining information”或“effective correction”。

## 表4是同一检测器的循环自评

流程先用某个`NLI + GraphEval`挑出疑似错误输出，纠正后再用**同一个框架**判是否修好。所谓“percentage of believed corrected hallucinations”不是独立正确率：选择偏差使样本条件于原检测器为正，纠正文本也可能通过删掉、改写或让KG抽取器漏掉主张来逃过检测。

GraphCorrect相对Direct在7/9格更高，但TRUE+QAGS-X为66.7 vs 70.8、TrueTeacher+QAGS-X为69.3 vs 71.1，均更差。最高也只有69.5%，不能笼统写“绝大多数都成功修正”而不附代理定义。作者在discussion明确承认应该人工评估；这一承认应优先于摘要/结论的强表述。

独立验证应让blind人工标注者或不同架构裁判检查原文、修改后文本和证据；同时保留“仍错误/已正确/正确被改坏/信息删除/无法判断”五类，而不是只看检测器翻转。

## 可进一步开展的实验

1. **抽取覆盖金标：**人工把回答标成atomic propositions与span，测triple precision/recall、scope、negation、quantity和coreference保真。
2. **拆分因素消融：**同一NLI与调用预算下比较raw response、sentence、OpenIE、LLM claims和GraphEval，识别KG的独立贡献。
3. **长度校准：**按triple数和词数报告TPR/FPR/ECE，比较max、noisy-OR、top-k、FDR及长度条件阈值。
4. **稳定性：**Claude temperature 0及多个seed重复抽取，报告KG集合Jaccard、最终标签翻转率、无效格式率与成本。
5. **跨域：**加入QA、长文、RAG对话、数值/时间/否定、多语言及开放域检索；按领域重新校准而非直接沿用.5。
6. **解释有效性：**评估返回triple到原span的定位、人类查错时间、误导率，以及删除该triple是否真正改变判定。
7. **独立纠错评价：**blind人工和异构裁判评价正确性、完整性、误改、删除与语言质量；检测器不得同时负责选样和验收。
8. **顺序与冲突：**多triple修复比较并行、顺序、联合编辑，记录相互覆盖和新引入错误。
9. **成本前沿：**报告Claude tokens、NLI次数、显存、wall-clock和单位正确检测/修复成本，与轻量claim split及强LLM judge比较。

## 对综述可使用的结论

GraphEval代表“先结构化原子化、再逐claim核验”的重要路线。在三项摘要基准上，它使三个NLI模型的样本量加权balanced accuracy平均提高约6.2点，且能返回疑似错误triple；但九格等权平均仅4.84点，HHEM在QAGS-X还下降.3。论文没有验证KG抽取覆盖、定位解释或跨域泛化，max聚合还引入triple数量/输出长度效应。

GraphCorrect展示了利用定位结果做局部修复的工程思路，但ROUGE只证明更保守地编辑，表4又由同一检测器选错并验收，不能当真实修复率。综述中应把它作为“结构化分解改善NLI接口”的有希望证据，而不是“KG已系统检查所有事实并可靠纠错”的定论。
