# I111 HalOmi: A Manually Annotated Benchmark for Multilingual Hallucination and Omission Detection in Machine Translation

## 来源、版本、阅读与执行边界

David Dale、Elena Voita、Janice Lam、Prangthip Hansanti、Christophe Ropers、Elahe Kalbassi、Cynthia Gao、Loïc Barrault、Marta R. Costa-jussà，FAIR Meta。EMNLP2023，638–653，DOI10.18653/v1/2023.emnlp-main.42，正式页 https://aclanthology.org/2023.emnlp-main.42/ 。本库arXiv:2305.11746v2，2023-12-06，共16页。正文1–9、实质附录12–16全部阅读；9–12页参考文献只定位。目视1/3/5/6/8/14/15/16页，核实定义图、ALTI矩阵聚合方向、完整检测热图、自然/扰动对比和词级案例。

另下载正式16页PDF至`qa/I111_published.pdf`，SHA256 `a2c17a688b429d9853a0ecc7528dffa7248c5e72d255fa8b8945e8d361698edc`。逐页提取文字比较主要为会议页脚、页码、数学空格，方法和表格实质相同。以下页码指PDF物理页，印刷页=637+物理页。

官方代码 https://github.com/facebookresearch/stopes/tree/main/demo/halomi ，固定stopes commit `a4e75e8cb5b8eed629ac0056f301d32d8f194db2`，3,686,623字节ZIP存`qa/I111_official/`。阅读HalOmi README、evaluation_utils、reproduce_evaluation、compute_detection_scores及共享ALTI聚合/get_loss函数；没有运行下载模型、翻译或检测器前向程序。

实际下载官方 `https://dl.fbaipublicfiles.com/nllb/halomi_release_v2.zip`，19,881,020字节，SHA256 `e62bbbd286a443224e1754b3554082aaae7c3e3788eef6a02a155223d3195987`，存`qa/I111_data/`及provenance。读取四份主TSV：core、full、source_tokens、target_tokens；ZIP内额外notebook checkpoint备份未当额外样本。数据是句子/标注/历史预测分数，不是本次新模型输出。

独立脚本`sources/audit_halomi.py`，输出`qa/I111_halomi_audit.json`。执行全部句级缓存分数复算、掩码/row_id/标签检查、纯函数隔离、ALTI均值恒等式与反例。只从AST隔离无模型的pair与ALTI聚合函数；没有fit词级联合logistic regression，也没有重跑MT、外部编码器或注意力收集。本文结果、真实缓存复算、静态/数学推论和后续实验分开记录。

## 1. 为什么这篇对LLM幻觉评价综述重要

本文研究条件生成中的**来源无关译文内容**与**来源信息遗漏**，不是开放QA世界知识真伪。它将18翻译方向、自然错误、专业人工句级/词级标注和可获取的生成模型放在一起，使低资源迁移、内部检测器与细粒度解释可被真正评估。

与I110 HalluQA形成测量目标对照：HalluQA把不流畅和多数拒答也算幻觉，而HalOmi专门排除乱码、错误语言等不可理解译文，并区分普通误译、无关幻觉和遗漏。因此两个“hallucination rate”不能横向当同一随机变量。与I109 mFACT相比，HalOmi是人工MT错误标签，不是英语指标翻译银标；不过本集也经过检测器偏向抽样，不能当总体自然发生率。

“语言多”“译文自然生成”“生成模型公开”是不同优点；本工作只用单个NLLB600M模型，明确未满足多模型/多架构泛化。不能由18方向推出对所有decoder-only LLM翻译、RAG或摘要都已验证。

## 2. 幻觉、误译和遗漏的操作定义（第3页图2）

幻觉为目标词与来源找不到合理对应的新增无关信息；遗漏为来源信息未进入译文。对目标错误词，标注者依次问：是否与某来源词同常见语义类、是否存在语义联系、是否能解释这种联系；均否才标幻觉。于是某些实体/数值/时间被误译但仍与来源概念相关，可能归普通mistranslation，不一定纳入幻觉。

不能把“来源不能蕴涵的所有事实错误”直接等同该标签。比如同类实体替换在严格factual consistency中可构成严重错误，在此可能仍属于误译。这是定义收窄带来的标签边界，不是某一套概念天然正确；综述应统一说明不同benchmark测什么。

句级四档无/少量词级/部分/全部，严重度主要按错误词数：1–2词、至少3词但不全、近全（允许1–2词例外），按指南避免重叠。一个否定词或剂量词可能比三个无关修饰词语义后果更严重，数词严重度不自动等于危害程度。作者第8页明确讨论按词数分级与语义不充分性的区别。

来源和译文分别有omit/hall span，以<<< >>>包围，并转字符掩码。幻觉与遗漏可同时存在，统计图优先把同时两种错误归幻觉；这只是互斥显示约定，不表示遗漏标签消失。遗漏检测专门限制在**无幻觉子集**，从而避免用最容易的全无关译文充高遗漏检出率，但也改变目标总体。

乱码/错误语言被排除，作者理由是它们明显坏、无需来源可识别，而流畅的无关内容更能误导用户。这种划分有研究价值，但部署时仍需单独识别被排除病例，不能用此基准总体成绩保证完整系统可靠性。

## 3. 18方向、来源与采样：自然生成不等于自然频率

高资源：英语分别与阿拉伯语、普通话、德语、俄语、西语互译，10方向；低资源：英语分别与克什米尔语Devanagari、Manipuri Bengali、Yoruba Latin互译，6方向；额外西语↔Yoruba为NLLB训练中无直接配对的zero-shot，2方向。总共9种语言、18方向，不是18种语言或18无方向pair。

来源为FLORES200 dev及Wiki讨论/Jigsaw评论。英俄西用Jigsaw，汉阿德用Wikipedia讨论，低资源并非每个方向都有同样域。正式NLLB200 distilled600M，beam5，禁止UNK、重复4gram，最大长度3×来源token+5；这是论文版本设置，不应替换成任意HF默认解码。

候选先由多种检测器评分：ChrF++/COMET有参考仅用FLORES，其余COMET-QE、Seq-logprob、LASER3、LaBSE、双向XNLI、ALTI+等。每方向/来源同时均匀抽样、按检测器quantile偏向抽样、取最差。这样富集少见错误，兼顾正常样本，但评价集分布仍与参与选择的代理分数相关。

应区分“生成时无人工扰动”与“评价时未筛选总体”。本集自然译文经选择后25.62%被标有幻觉，不代表NLLB对全部日常输入25.62%发生幻觉；语言间来源和筛选比例也不同，不能只由错误频率推断语言本身造成差异。

若某方法参与筛选，可能更容易/更难地显露自身错误模式，并影响相对评价；此处不是简单断言选择必然抬高所有方法。最小核查是分别报告uniform/biased/worst、FLORES/Wiki，以及原生成池抽样权重或独立随机外测。本次实际计数已保留各方向×来源×selection，但没有原完整生成池和抽样概率，无法恢复总体基率。

## 4. 专业标注和postprocessing（第12页附录A）

每语言两位专业译者，一人标、一人复核；通常有2–3年经验，曾参与FLORES或具相关专业经历。15项资格测试含3 full、4 partial、2 word-level hallucination、5 mistranslation、1不可理解，门槛96%；可一次反馈后重试，仍不通过需换人。

96%如何由15项多粒度标注计算，正文未充分解释，不能简化成“每题准确率≥96%所以最多错0题”。一标一复核也不等同独立双盲标注，未给初始独立κ、复核改变比例或争议仲裁原票，不能凭专业资历保证无噪声。

过滤不可理解译文、括号不平衡、span与原文本明显不匹配等，最终每方向144–197句。此过程改善格式一致性，却对难以标记的错误存在选择效应。两个数据版本的修复说明应与最终模型结论一并记录。

## 5. 实际数据总量、分布与结构核查

core2,865条，full5,247条=自然2,865+扰动2,382。自然来源FLORES1,854、Wiki1,011；uniform747、biased1,125、worst993。自然每方向144–197，与正文范围吻合；自然没有同方向同来源同译文精确重复，扰动有1条重复。

自然hall标签：无2,131、少量225、partial291、full218，合计有幻觉734/2,865=25.6195%。omit标签：无1,790、少量335、partial528、full212，有遗漏1,075/2,865=37.5218%；两率不能相加当互斥错误比例。至少有幻觉的最低方向是英→俄5/146=3.4247%，有遗漏最低英→阿25/144=17.3611%，支持正文约3%/17%的下界描述。

扰动hall：无724、少量129、partial717、full812，有幻觉1,658/2,382=69.6054%；omit无318、少量251、partial1,012、full801。扰动与自然抽样/类别频率不同，不能仅看检测分数变化就归纯机制效应。自然full hallucination有201同时full omission，但仍11个标无omission；标签经验关系不是逻辑恒等。

源端token189,530、其中自然100,164；目标端177,203、其中自然94,341，总366,733条。源端zero_weight10,621、目标10,654为特殊/无字符token，词级评估排除。literal“na”类token源14、目标6，不能让pandas默认把它们读NaN；官方已提示keep_default_na=False。

全5,247句raw/normalized字符掩码长度均与对应文本一致，掩码仅0/1；所有token的row_id在界内，direction/perturbation与full句子一致，label_mask长度=token_weight，token_label均等于字符mask是否含1。结构正确并不证明语义标注完全正确。

发现4条句级与字符标签不一致：row_id937扰动阿→英标small omission但source mask全0；2868自然Yoruba→西语标full hallucination但target mask全0；3965扰动西→Yoruba句级无幻觉但target mask有1；4957自然英→德句级无遗漏但source mask有1。row_id为full.tsv零起始行，非纸面编号。应该回到原标注核实，不能默默替换某层标签或把所有mask自认为金标。

自然存在278组相同源语言+normalized来源文本跨不同目标方向复用，最多4方向；扰动257组、最多8方向。句级检测分开方向，故不自动使其无效；但词级联合模型仅按row_id分组CV时，相关来源可能分布不同fold，不能称来源语义完全隔离或整语言留出。

## 6. 句级评价：有序成对排序及代码的tie边界

句级目标：hall severity排序；hall=none子集的omit severity排序；any pathology取两种severity最大值。指标把不同标签的句对拿出，统计更严重者是否获得更高风险分，方向内计算，再18方向等权宏平均。它不是普通准确率，也不是直接平均每个类别二元AUROC。

多类成对指标的隐含权重与n_i×n_j相关；类别比例改变时，即使每类对排序能力不变，总分也可变。方向宏又不同于把全部2,865句pool到一起的pair指标。用“.83”说83%的译文检测正确或83%的所有token都标对，均不成立。

源码percent_correct_pairs只计严格x1<x2，预测相等不给半分；二元常规AUROC给ties半分。隔离函数反例：标签[0,1]、分数[.5,.5]，源码0，标准AUROC.5；只有一个标签时源码返回0而不是undefined。本文宣称二类等价AUROC需要无预测tie等条件。

实际自然hall主任务所有10分数的跨标签ties均0，故该边界没有改变本次hall成绩；自然omit/any只有XNLI各1个tie，影响很小，不能把数学反例夸大为论文主结论全部失效。随机连续分数期望约.5和恒分数得0也应区别。

扰动数据无幻觉子集中的英→Manipuri没有可比较的不同omit等级；若把它按源码0加入18方向宏，会把分数拉低。排除这一个无可比方向、宏17方向，能重建附录图10的omit数值。无效分母处理必须显式报告，不能一边称18方向一边用0冒充有效检测成绩。

## 7. 内部、外部、灰区方法的机制

Seq-logprob是生成模型对该译文token条件概率的汇总；代码risk `score_log_loss`实为平均负log loss，越高越可疑，不是未取负号的正向高置信概率。低概率可反映稀有但正确文本或域外输入，高概率也可能流畅编造；它是排序信号，不是来源支持证明。

ALTI+传播token贡献，句级ALTI平均每个目标token来自来源的总贡献；ALTIT把同一来源—目标贡献矩阵按每个source token聚合后平均，直觉为来源被使用程度。它们和只看注意力weights的Attn-OT不同，不能把两者都叫“注意力解释”来概括。

外部包括COMET-QE、LaBSE/LASER句嵌入相似、XNLI双向蕴涵乘积、SONAR嵌入上的BLASER2.0-QE。源码XNLI从config.label2id['entailment']取类别并双向计算，比固定第几列有更明确语义。风险列多经取负（COMET用1−score），不能按原论文通常“高分好”的方向重新计算缓存。

Attn-OT比较当前attention与良好译文参考分布，是灰区：虽用内部attention，却需大量外部“好译文”。作者每方向采1M训练句、译后按长度比/损失/LASER各去最差20%，剩约600K；并非完全无训练、低成本的单样本内部检测器。

## 8. ALTI与ALTIT的严格关系：遗漏机制需要更小心解释

共享源码compute_alti_metrics里，令S为保留source列数、T为target行数、C为这些贡献总和：`avg_sc=C/T`，`src_sum_contr_mean=C/S`。因此**ALTIT=ALTI×T/S**（在风险列二者同取负时也成立），这是固定矩阵上的代数恒等，不是经验相关。它不额外保留来源各列贡献的分布。

隔离实际聚合函数：矩阵A两行都是[.3,.3,0]，B两行都是[.2,.2,.2]。A第三来源词完全没被用，B三词都有贡献；两者ALTI均约.6、ALTIT均约.4，但source_min为0与.4。于是“ALTIT高低直接定位哪些来源词遗漏”的强解释不成立；它更多结合总来源依赖与长度比例。该反例不证明指标无用，实际长度比例可能正好是有效遗漏信号。

更直接的机制研究应比较单独T/S、ALTI、二者乘积、source_min/low-contribution比例，并在长度比匹配数据上评估；词级ALTI仍保留更细矩阵信息，不能把句级均值局限外推为全部贡献方法无效。当前没有真实贡献矩阵缓存逐句核数，本次结论来自已读源码和实际纯聚合函数。

README把score_alti_t_mean描述为目标token上的max贡献平均，与源码使用src_sum_contr_mean和论文图4的source聚合不同；复现应以确定函数/列生成过程记录，不能仅按字段说明重写成top_sc_mean。

## 9. 句级真实缓存复算：修正值与论文旧值

官方README坦率记录：v1遗漏检测有错误，后来修正；发表后又发现部分score_log_loss有错，当前保留legacy列重现论文，corrected列用于新数。不能把修正列与旧热图逐格不符都归模型复现失败。

自然hall方向宏：corrected log loss .796786、legacy .791640；ALTI .747689、ALTIT .579903、Attn-OT .533654、COMET-QE .748242、LaBSE .780582、LASER .753988、XNLI .669939、BLASER .825663。与README预期精确小数吻合，原图总体logprob.79对应legacy，而当前修正舍入.80。

自然无幻觉omit：corrected loss .587348、legacy .560904；ALTI .484925、ALTIT .768027、Attn-OT .703135、COMET .587501、LaBSE .718998、LASER .640703、XNLI .646845、BLASER .735587。any pathology：corrected loss .687980、legacy .674489、ALTI .636970、ALTIT .682101、AttnOT .623706、COMET .662633、LaBSE .754149、LASER .709153、XNLI .667526、BLASER .807611。

这些是历史缓存分数与人标签的真实独立重算；没有重新运行生成器或检测器。最优模型在本数据中是BLASER总体hall/any，ALTIT总体omit，但不代表每方向、每任务它们都最佳。

资源组hall：高资源10方向LaBSE .889984、BLASER .885975、corrected loss .881540；低资源6方向BLASER .791390、loss .719597、ALTI .715872、XNLI .479385；zero-shot2方向ALTI .653470、BLASER .626923、loss .604585。故“低资源内部方法优于所有外部”遗漏BLASER例外；“BLASER每方向均最佳”也不成立。高低资源差异还混合具体语言/脚本/域，不能视为单一资源量实验。

自然omit高资源ALTIT .778306、BLASER .792617，低资源ALTIT .728329、BLASER .663864，zero-shot ALTIT .835723、BLASER .665604；总体结论应带分组，不能用某一德英方向替代多语结论。

## 10. Attention-OT：负结果、复现缺口和成本

表2八种注意力OT变体hall均约.49–.55；最好也接近机会。去EOS改善某些变体、不改善其他，omission可到.71。作者观察大约75%attention指向EOS，讨论EOS隐状态范数较小可能影响weights解释；去掉EOS后仍不解决hall判别。

附录B比正文脚注更细：原Wass-to-Unif可重现，Wass-to-Data/Combo约低2个百分点，参考数据选取不同且原文无完整code/training data。应写“部分变体复现接近，部分有差异”，不能说全方法完全精确复现。

当前README说明AttnOT参考分布未发布，产生历史分数时未固定随机种子，今日有固定seed接口仍不保证逐分数相同。因而评价已存列可以重现，重新生成AttnOT列并非完全可复现。本次不下载/执行任何pickle参考文件，也未运行模型收集注意力。

此负结果说明特定attention异常模式对NLLB多语自然病例不稳，不能证明所有attention特征、所有attribution或所有架构都毫无价值；与其他内部状态检测论文比较时要明确模型/层、任务和分布。

## 11. 自然与人工扰动：可直接复算的排名逆转

扰动把所有encoder–decoder attention层输出乘α=.3，作者用该设置匹配平均序列损失，使生成更脱离来源但仍流畅。它是干预生成器内部，不是简单对自然译文做少量事实编辑，也不是现实用户一定触发的故障机制。

缓存复算hall：自然legacy loss .791640>ALTI .747689；扰动legacy loss .722985<ALTI .827157，排名逆转。corrected loss自然.796786/扰动.722592也保留逆转。因此“在扰动上ALTI胜过概率”不能直接外推自然错误。

扰动omit排除无可比英→Manipuri后，legacy loss .603233、ALTI .512729、ALTIT .622435、AttnOT .648676、COMET .582082、LaBSE .610703、LASER .587784、XNLI .687738，按2位舍入与图10 .60/.51/.62/.65/.58/.61/.59/.69吻合。若错误加入那一个零分方向，XNLI变.64953、ALTIT .58786，会造出伪“无法复现”。这是实际分母诊断，不是另外训练。

附录图12在按病理类型/来源/方向下采样匹配后仍有排名差异；图注写Word-level，但正文和列内容讨论的是sentence-level自然/扰动比较，不能照图注误认词级AUROC。本次未取得原匹配抽样索引、未复现具体匹配子集，只确认完整缓存的逆转及论文受控思路，不能称重建图12逐格数据。

## 12. 词级任务、组合模型和局限（第7–8、15–16页）

目标侧每词是否hallucinated，来源侧每词是否omitted；SacreBLEU tokenizer分词，中文按字符，其他按空白/标点规则。NLLB子词分数到词时取最坏值，字符mask任一1使词标正。中文“一个词”与其他语言形态词并不等价，词级单位不是跨语天然同尺度。

四特征：token log loss、与空来源条件logprob对比的contrastive分数、ALTI来源总贡献、来源最大贡献。遗漏对源/目标交换，内部模型仍需支持反向语言方向；这不同于仅把同一attention矩阵简单转置的普通无参数词对齐。

联合logistic regression用所有语言pool，3折GroupKFold按sentence row_id分组，避免同一句子token跨fold；并非leave-one-language-out，也不是独立来源语义切分。单特征时代码用全数据fit一个logistic，不做CV，理由是单调变换不影响排序；若学到负系数会反转方向，符号选择仍用标签，有限样本/域分组解释要谨慎。

图7显示hall总体logprob/contrastive约.70/.70，ALTI sum/max .78/.68，联合.84；omit .78/.73/.78/.76、联合.83。当前README的脚本期待omit联合.84，可能反映修正/库/版本差异，**本次未重fit联合模型**，不声称已解决这1点差异。

最坏子词聚合可能偏向长词。独立算例：若每子词误报概率.1且独立，“任一误报算整词误报”，1子词为.1、10子词1−.9^10=.651322。这是合成例，不是实测错误率；说明比较语言/词形时需按词长、子词数报告coverage和false positive。

图13人工挑选英西案例显示logprob容易突出词/句开头，ALTI可能在词尾低贡献；它们兼有合理检测和结构性位置倾向。热力图可解释分数，却不是证明模型生成幻觉的心理/因果机制。需要扰动/控制位置和重要事实独立测试。

## 13. 已研究问题与进一步验证设计

问题A：误译与幻觉界线是否跨benchmark一致？指南实际收窄到无合理来源对应，而非全部错信息。后续在同一候选上双标“任意事实不一致/误译/无关新增/遗漏”，提供映射和争议样本，不把不同指标排行当彼此否定。本次已定位定义差别，没有给全数据新增人工语义标签。

问题B：ALTIT是不是提供全新遗漏信息？代数与隔离聚合函数证明句级两均值仅差T/S；coverage矩阵反例已运行。后续比较长度比基线、长度匹配、source_min和贡献稀疏性，检验实际收益来自何种信号。保留其词级信息，不作过宽否定。

问题C：稀有自然错误的部署风险能否由AUC推断？目前有检测器富集、乱码排除和低资源混合。若真实基率.001、TPR.8、FPR.01，precision=.0008/(.0008+.00999)=.074143，只约7.4%；这是先验漂移算例，非本文实测性能。需要随机真实流量、低FPR区间、PR-AUC、成本/风险coverage，不能把.83成对分数当83%报警可信率。

问题D：多语言pool会不会泄漏相关来源？已确认278自然来源组跨方向，按row_id CV不能消除。后续按原来源ID/文本语义group、leave-direction和leave-language-out，比较联合模型泛化；不能仅从278这个数断言已导致具体提升多少。

问题E：发布标签/版本能否支持严格复现？实际发现4句级—mask冲突，corrected/legacy差、perturbed无可比方向和词级联合期望差。后续先回原标注仲裁，保留版本映射与排除清单，再重算，不能自动拿某层覆盖另一层。

问题F：人工与自然错误是否同分布？真实hall排名逆转已复算，图12匹配思路支持不能只归类别率。需要多种干预强度、自然源域、不同生成模型，并按相同声明/长度/类型匹配，而不把单α=.3干预当全部synthetic data都无价值。

## 14. 复现资料与综述可用结论

固定仓库提供句级分数生成和句/词级缓存评价程序。全word-level预测列的生成流水线本次未定位：搜索当前ZIP的.py/.ipynb，contrastive字段仅出现于reproduce_evaluation；这不妨碍读取已存分数，但不能说当前目录能从零无缺口生成全部token TSV。NLLB权重、fairseq nllb分支、词典、SentencePiece、外部检测器和AttnOT参考数据是另一层依赖。

README记录本数据/代码主体CC-BY-NC4.0，FLORES/Wiki/Jigsaw来源有各自CC-BY-SA条款，资料包保留上游LICENSE和说明，不将其重标为本组原创。本文专业译者公平报酬只作作者报告，不虚构具体金额。

综述建议：HalOmi以同一公开MT模型的18方向自然译文和专业细粒度标注，揭示单语言结论、人工诱发错误和注意力异常检测的迁移局限；句级与词级、幻觉与遗漏需要分开评价。低资源外部指标表现取决于覆盖，BLASER是重要例外；其数据富集、小规模、单生成模型和严重度定义限制总体风险外推。

关联：I109的翻译银标需用原生人工错误验证；I110的世界知识/拒答标准不可与此混同；DAE/FactCC/SummaC等来源一致性工作可比较定义与粒度；内部概率/attention类论文需用自然、多语、来源分组测试检验迁移。本文不支持“所有MT错误都为幻觉”“所有内部方法胜外部”“跨语方法已有18种语言零样本泛化”“自然发生率25.62%”“联合词级模型本次全部重训复现”等过强表述。
