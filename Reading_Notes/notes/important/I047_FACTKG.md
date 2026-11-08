# I047 FACTKG：知识图谱一致性、合成反事实与真实世界真伪不能混为一谈

## 来源、版本与核验范围

Jiho Kim、Sungjin Park、Yeonsu Kwon、Yohan Jo、James Thorne、Edward Choi，*FACTKG: Fact Verification via Reasoning on Knowledge Graphs*，ACL 2023，arXiv:2305.06590v2（2023-05-19）。本地PDF共15页，正文、完整附录A–F、模板、否定标注与GEAR公式逐页阅读；目视核对PDF3构造图、PDF6表2、PDF8表3–4、PDF13表5–6、PDF15表10–12。

作者当前[官方仓库](https://github.com/jiho283/FactKG)main保存为`Hallucination_Evaluation_Library/code/I047_FactKG_main.zip`（29,293字节），目录与源码通过静态审计。仓库README明确说“修正数据中的一些错误后，baseline可能与论文不同”；公开数据位于Google Drive且当前环境无法访问，故未重算当前数据规模、标签、重叠或表3。以下区分论文时108,674条版本与当前修正版。

## 正确定位：它测的是文本—固定KG一致性

FACTKG从WebNLG 2020的文本—RDF对和DBpedia 2015构造108,674条英文claim，标签SUPPORTED/REFUTED，覆盖One-hop、Conjunction、Existence、Multi-hop、Negation。其优势是可把证据表示成明确关系路径，适合研究结构化事实核验和图推理。

但标签的精确含义是“claim能否由指定版本DBpedia及生成规则满足”，不是无条件世界真值：

- DBpedia缺边可能是知识库不完整，不证明现实中为假。
- DBpedia 2015已过时，时间变化事实会与今天不同。
- 实体替换/NLI过滤得到的是合成反事实，语言和错误分布不同于LLM自然幻觉。
- KG路径能解释系统检到了什么，仍不保证KG本身正确、完整或语义粒度合适。

因此它可用于综述中的**结构化外部验证/图推理基准**，不能作为开放生成事实正确性的唯一证据。

## 数据构成、规模与split

论文表2共108,674：One-hop19,530、Conjunction37,097、Existence9,172、Multi-hop27,262、Negation15,613；风格为written34,462、模型转口语64,788、presupposition9,424。按8:1:1分train/dev/test，声称不同split的triples互斥。

Triple-disjoint比随机claim划分严格，但不保证entity、relation、template、WebNLG source graph或同一实体邻域互斥；模型仍可从重复实体、关系组合和生成模板迁移。claim作为pickle dictionary key，若修正版含相同文本的重复样本会被覆盖；必须以当前文件计数，而不能直接沿用论文总数。

测试集只提供entity set，不提供gold relation sequences；训练/dev提供Evidence。关系与hop预测器从claim+entity学习，再在完整DBpedia搜索路径。该设置同时测语言解析、关系/跳数预测、图搜索和最终判别，错误来源需分阶段报。

## 五类claim的构造与各自标签风险

### One-hop：替换不等于现实反证

SUPPORTED来自单triple WebNLG句。REFUTED通过entity或relation substitution：替换实体须与原claim所有实体图距离>4，并与原句双向MNLI判为contradiction；替换关系从相同head/tail类型组随机选并套模板。

“图上四跳之外”只说明DBpedia局部不相连，不证明替换事实为假；NLI只判断新旧句互相冲突，不核验新句现实真值。论文抽1000条、两名研究生共同判99.4% refuted，说明样本精度较高，但没有按生成方式/关系/实体频率分层，也没有给κ、各自判断与6个失败例。剩余0.6%按108k放大仍可能数百条；当前README又承认后续修错，必须版本化标签。

Relation group很粗，例如person→person把child、successor、parent、spouse、vicePresident、primeMinister放在同组；替换后语法可能通顺但事实可偶然成立。模板词形与关系名也可能留下标签线索。

### Conjunction：all-facts语义与部分反事实

多triple WebNLG句作为SUPPORTED；替换一个实体生成REFUTED。逻辑上任一合取项假则整体假，但模型可能依靠局部怪异实体或固定替换位置，而不执行全合取。更合理的诊断应区分0/1/多项错误、哪一项被替换，并测试错误位置和claim长度。

### Existence：开放世界尤其敏感

从`{head, relation}`或`{tail, relation}`生成“X had a parent/company”等模板，只保留22个关系。SUPPORTED只需存在某tail/head；REFUTED用相同实体类型但不同关系。对不完整KG，关系不存在是unknown而非false；existence任务把开放世界强行闭合，模型的“正确”只针对DBpedia快照。

### Multi-hop：类型替换与路径存在

从conjunction中把中间实体替换成type name，例如“船由一家位于Papenburg的公司建造”。DBpedia一个实体有多type，作者把每个type插入句子，用GPT2-large perplexity最低者。这个选择优化语言自然度，不保证类型是语义上最具体/正确；预训练GPT2偏好也进入数据构造。

REFUTED再用entity substitution。路径推理定义为存在某中间节点满足关系链；多个路径、类型层级和KG缺边会改变标签。表3中GEAR Multi-hop68.84反低于claim-only BERT70.06，说明检索噪声抵消图证据，不支持“所有复杂推理都受益于KG”。

### Negation：scope和量词是最大标签风险

One-hop每原句生成100个opposite候选，要求实体保留、含否定词、双向NLI contradiction，再反转标签。Conjunction/Multi-hop用GPT-J 6B和16个ICL例在不同位置加negation，根据替换位置制定规则。

自然语言否定并非简单逐边翻转。对“X was not built by a company in New York”，通常语义是`¬∃company(builder(X,c) ∧ location(c,NY))`；作者的路径说明可能按“存在一家建造公司且地点不是NY”即`∃c(builder ∧ location≠NY)`处理。两者在多建造商情形不等价。Table12把三类句留给PATHCHECK，却没有形式语义说明量词范围如何唯一决定；这使模型可能学习生成规则而不是自然语言逻辑。

Table10/11的“双重not”句如“was not built by Samsung, not in Papenburg”也有强scope歧义。应将每条negation编译为显式逻辑式，按所有匹配路径求值，并由语义标注者验证，而非只按生成位置翻标签。

## 口语转换与presupposition并不都保真

模型式转换用Wizard of Wikipedia训练FLAN-T5-large，以temperature20、500 candidates再过滤：edit distance≥6、保留verbs/entities、原句→生成句NLI entail且反向不contradict，最后AFLITE选样。平均500中仅41.2存活。高强度筛选制造了“通过特定NLI/NER/parser”的条件分布，未必代表真实口语。

测试集全部模型式口语claim由3名研究生复核，只保留至少2人判“All facts preserved”；此前9.8%被至少2人判“Loss of important information”。train/dev并未说明接受同等全量人审，导致test比训练口语更干净，并形成质量选择分布。Appendix E又说总计9名研究生参与survey，与主文“test每条3人”可兼容，但未给每人负载和agreement。

Presupposition三类尤其值得警惕：

- factive模板“I realized/remembered P”通常预设P，可沿用原标签，但“I explained/emphasized P”并非严格factive。
- non-factive模板“I imagined P / I wish P / If only P”被直接标为原P的反面。`imagine P`并不蕴含`¬P`，愿望也可针对已部分成立事实；这是系统性标签规则而非真值逻辑。
- structural模板把“When was X related to Y?”这类question本身当claim，并以其presupposition判真伪。问句没有普通二值真值，把presupposition satisfaction当claim truth需明确单独任务，不能和陈述句accuracy混合。

这三类会让模型通过“I imagined/If only/When”词面推标签。应报告template-only、去实体和打乱KG基线，并把presupposition satisfaction独立评价。

## Baseline与图证据效果的正确读法（PDF7–8）

Claim-only：BERT65.20、BlueBERT59.93、Flan-T5 zero-shot62.70，majority51.35。GEAR with evidence77.65，比最佳BERT高12.45点；One-hop83.23、Conjunction77.68、Existence81.61、Negation79.41，均明显高于claim-only对应最佳，但Multi-hop68.84低于BERT70.06。

这些结果支持“当前pipeline在多数合成reasoning类型利用图信息”，不能证明图推理本身达到77.65：GEAR还看到claim文本，关系/hop分类器在合成训练集监督下学习模板，检索失败时随机选路径，最终BERT可利用两侧artifact。需要claim-only、evidence-only、shuffled evidence、gold relation/hop、gold path、random path的完整阶梯消融。

Claim-only BERT显著超多数类，作者归因Wikipedia预训练知识或生成pattern。BlueBERT仍59.93，已表明没有Wikipedia预训练也能用模板/替换artifact；BERT与BlueBERT的tokenizer、预训练域和优化差异也不只“是否见过Wikipedia”，不能用二者差额精确量化记忆知识。

Flan-T5论文说比较输出`True/False` token probability；当前源码实际`model.generate`后以大小写`true/false/yes/no`子串解析，并要求正反词不同时出现。说明正式描述与当前实现不一致，且“not true”“No, it is true”等输出可能被错判/不计正确。

论文只报accuracy，无seed方差、置信区间、SUPPORT/REFUTE分层、按style×reasoning交叉结果或检索recall。多数类51.35说明轻度不平衡；应至少报balanced accuracy、MCC、各类F1和path recall。

## Cross-style结果不能证明口语训练带来一般化

表4：BERT W→W71.75、W→C63.85、C→C68.10、C→W69.43；GEAR81.00、75.43、80.81、78.80。跨style都低于相同测试style对应训练（W→C低于C→C；C→W低于W→W），实际上存在domain shift。作者强调C→W高于C→C，但两列测试集不同，难度不可直接比较；不能据此因果断言“口语多样性改善泛化”。

测试口语经过人工只留完全保真，written与colloquial样本量、reasoning mix、label比例可能不同。应在同一underlying fact生成written/colloquial配对测试，以paired accuracy和prediction consistency评价style robustness。

## 图“可解释性”仍需忠实性评价

Appendix表5展示两条正确和一条错误案例，路径可读，但“可视化一条检索路径”不等于路径是模型决策原因。GEAR把所有路径文本化并经BERT/Transformer聚合，注意力/展示路径可能是事后选择。解释评价应测：删除展示路径是否改变预测、只保留路径能否保持预测、路径是否真满足claim逻辑、错误预测时路径错误还是聚合错误。

KG可提供规范证据链是优势；但随机fallback path、错误relation/hop和无关路径会使“解释”失真。特别是REFUTED需要明确反证：缺少支持路径不等于存在反证路径。

## 当前官方源码审计

1. README明确当前数据纠错后baseline可能不同，因此论文表3是历史版本结果；没有release tag/变更清单时不可用当前数据声称复现论文表。
2. 当前代码固定若干torch seed，但Python `random.choice`用于fallback路径而未统一seed；图检索结果可随运行变化。
3. GEAR classifier的train/dev/test DataLoader均`drop_last=True`，会静默排除每个split不足32的尾部样本；总accuracy和type accuracy分母不是完整文件，除非样本数恰好整除32。
4. `best_param = model.state_dict()`没有`deepcopy`；PyTorch state dict张量通常引用当前参数，后续训练会继续改变它，最终`load_state_dict(best_param)`可能加载停止时参数而非真正dev最佳epoch。
5. test关系候选来自top-3 predictor，再对候选按预测hop取permutations；train/dev却直接使用gold Evidence检索，存在明显oracle-train/predicted-test exposure gap。
6. 训练/dev预处理对Evidence path原地`sort`，关系集合再经`set`，顺序不稳定；候选搜索在无连接时随机选分支，复现需固定Python/hash seed并保存路径缓存。
7. 当前Flan脚本与论文的token probability叙述不同；仓库README还默认`flan-t5-xl`，论文表写Flan-T5未在表中标规模，正文亦不够醒目。
8. 代码按CC BY-NC-SA 4.0发布，适合课程研究打包，但须保留署名、非商业及相同方式共享条件。

## 可进一步开展的问题与实验

1. **当前修正版数据审计：**下载三个pickle，报告实际计数、标签/style/reasoning交叉表、重复claim、实体/关系/source graph跨split重叠，并与108,674历史版diff。
2. **三值开放世界标签：**SUPPORTED/REFUTED/UNKNOWN；REFUTED必须有互斥关系或显式反证，单纯缺边归UNKNOWN。
3. **形式语义否定：**把claim编译为一阶逻辑，区分`¬∃`与`∃¬`、合取scope和多路径；对Table10–12做穷举KG反例。
4. **Presupposition单独任务：**区分utterance truth、embedded proposition truth和presupposition satisfaction；禁止`imagine P⇒¬P`捷径。
5. **配对style评估：**同一事实的written与colloquial成对，只改风格；报告prediction flip、paired McNemar与实体/关系保持率。
6. **证据因果消融：**claim-only、KG-only、shuffled/wrong path、gold relation/hop、gold path与retrieved path；报告各阶段recall和最终conditional accuracy。
7. **解释忠实性：**路径sufficiency/comprehensiveness、删除测试、逻辑执行正确率与human可理解性分开。
8. **自然LLM幻觉迁移：**用真实模型生成claim而非模板替换，映射到KG后人工处理实体链接、时效、KG缺失和多claim；测FACTKG训练的检测器是否跨分布有效。

## 对综述可使用的结论

FACTKG的重要贡献是提供大规模、可分reasoning type的自然语言—KG路径基准，并显示图证据总体将accuracy由最佳claim-only65.20提高到77.65；但Multi-hop反而下降，图检索是关键瓶颈。数据大量依赖模板、NLI过滤、替换和闭世界DBpedia，non-factive presupposition与negation scope存在明确语义风险，故不能把SUPPORTED/REFUTED直接视为现实真/假。当前仓库又承认数据已纠错，且实现存在尾批丢弃、最佳参数引用、随机路径未统一seed等复现问题。综述应把它放在“结构化证据与可执行推理”一节，并与真实web证据、开放世界unknown和自然生成幻觉基准形成对照。
