# I084 · MARS: Meaning-Aware Response Scoring for Uncertainty Estimation in Generative LLMs

Yavuz Faruk Bakman、Duygu Nur Yaldiz、Baturalp Buyukates、Chenyang Tao、Dimitrios Dimitriadis、Salman Avestimehr。ACL 2024长文，7752–7767，本地正式PDF16页。原文 https://aclanthology.org/2024.acl-long.419/ 。不要与同缩写的其他评价指标混淆。

## 阅读与独立核查范围

细读正文1–10页实质内容、附录A–C（12–16页）；参考文献不计其被引论文已读。目视第6页概率解释、第8页Tables 1–3、第14页Algorithm 1及训练细节、第15页成本与标注提示。官方源码由作者页面/原文确认，https://github.com/Ybakman/LLM_Uncertainty 固定commit `264a349fb7c723937048f771a2f3af15c50719cd`，ZIP/provenance保存于 `../../qa/I084_official/`。

静态读README、生成/清理/似然/聚类/不确定性/结果代码，以及importance_model_training两脚本；独立JSON解析发布的medical_dataset.json。脚本 `../../sources/audit_mars.py`，完整算术/源码hash/数据计数在independent_audit.json，逐行源码副本同目录。没有运行作者脚本、下载/反序列化pth模型，未调用付费裁判；Drive模型链接仅记录，不冒称完成模型复现。

## 1. 任务定位与核心主张

长度归一似然将每个token视为等重要，但一个回答中只有部分词直接回答问题。MARS以问题为条件识别重要短语，提升这些词的概率在最终分数中的权重，并与普通长度归一分数各混合一半。它是替换既有概率型UE方法内部评分的模块，不是独立外部证据核验器。

它评价closed-book、closed-ended英语QA的模型回答正确性；没有来源文档忠实性标注，也不逐条定位长答案幻觉。主生成器不重新微调，但新增110M importance模型需要训练。“unsupervised methodology”仅指重要性伪标签来自既有模型而非新招募人工标签，不等于无监督组件、无需训练或没有训练数据。

与I066 CSL同属token重要性加权，但MARS使用独立小模型/BEM删除伪标签及短语结构；CSL使用生成器attention加验证标签选头。不能只因两者都叫meaning/context aware就视为同一实现或相同访问预算。

## 2. 评分公式与概率解释边界

原始答案s长度L，token条件概率p_l，长度归一评分为Π_l p_l^(1/L)。MARS改为Π_l p_l^w_l，其中w_l=1/(2L)+u_l/2；u_l非负且和1。log MARS=.5×平均token logp+.5×重要性加权logp，分数仍为几何平均型评分。

如果u均匀，则退回长度归一；混入一半均匀分使非重要词也不会完全被忽略，但并不保证附带错误信息一定被检测。词的重要性来自删除对BEM等价判决的影响，不是对真实事实错误的直接验证。

作者第3页明确长度归一不构成归一概率分布，这点应保留。MARS也没有天然使所有可能答案概率和为1。exp后的值在0–1并不足以证明是正确性概率；用其替代熵公式时是经验代理分数，需要区分理论熵与实现。

三个被增强基线分别为：中心答案的负长度归一分（Confidence）、多个采样答案平均负log分（Entropy）、按意义聚类后不同簇log质量负均值（SE）。高不确定性预测错误，AUROC阳性在源码为1−correct；与I066高confidence预测正确须统一符号。

固定代码get_uncertainty.py沿用I091旧仓库的簇logsumexp后按不同簇平均负log、加常量5；不同于I066的负logmeanexp，也不是严格Shannon熵。相同名称的SE不能仅凭表头认为公式完全一致。

## 3. 重要性伪标签、短语与蒸馏模型

BEM本来输入问题、参考答案、候选答案来测QA答案等价；这里把原生成回答本身当reference，逐一删除短语作为candidate，以1−BEM输出衡量重要性。目标题的真实金标不是MARS推理的必要输入，不能把此过程写成“每次需正确答案”。但BEM仍是经过监督训练的外部模型，原生成若错误，它也不会因此自动变真。

作者以Flair phrase chunking识别短语，避免将子词或紧密关联的姓名拆开；再用温度τ=.01的softmax突出重要项。最后训练BERT-base-uncased衍生的110M模型，同时预测Begin/Inside Phrase和重要性。生成器推理时每答案只需该小模型一遍forward，不再逐短语调用BEM。

训练问题名义上为TriviaQA train69192+NQ train87925，共157117；输入四个7B生成器，若全部成功并保留，名义QA对上限628468。实际过滤、重复、空输出等未取得完整训练标签，因此这不是已审计的数据行数。四个7B主评模型也参与产生importance训练响应，13B是额外生成器迁移，不能称所有测试生成器都完全未见。

训练1epoch、lr5e−5、batch32，短语分类与重要性损失等权。论文称后者NLL；源码fine_tune_bert_v1.py用BCEWithLogitsLoss，参考软目标并输出sigmoid，须保留实现细节。其2%随机行holdout可能包含同题不同生成器输出，未见问题级group split，所以低validation loss不能直接证明新问题/新领域泛化。

Table 6分类train/val .0275/.0205、scoring .1957/.1901，只是训练目标损失，不是人工重要性准确率，也不是QA幻觉检测成绩。源码使用标准BERT token classification三logit（前二分块、第三重要性）；论文“双FC”与具体模块实现需要按版本说明，不夸大为完全不同架构。

## 4. 已核出的权重顺序差异

正文说先得短语重要性，再等分给短语内token。Algorithm 1字面是先把(1−o_k)/|h_k|赋给每token，最后对全部token softmax。两种非线性操作不等价，且τ=.01时差异可能很大。

独立例：两短语原重要性.6/.4，长度2/1。按伪代码先除长度再softmax，token权重约(.0000454,.0000454,.999909)，几乎全给第二短语；按先短语softmax再等分，约(.5,.5,.000000002)，几乎全给第一短语。此例说明需核准操作顺序，不代表论文实际预测样本。

源码训练标签只在phrase首词保留原1−BEM，其他位置-100，然后对保留位置softmax；推理从预测短语起点取sigmoid分，按短语归一，似然代码对每短语内部token负log概率平均，再按短语重要性加权，另混入整体token均值。这个路径更接近正文短语系数/内部平均，不能照Algorithm 1字面断言运行采用先除后softmax。

医学run另有代码分支：归一短语重要性再以τ=.001做一次softmax尖化，一般QA没有此步。因而医学结果不只是“原模块不变、换了数据域”；如果讨论迁移必须列出这个特殊设置。重要性BERT输入max_length512，超长问题+回答截断及短语/token对齐的失败边界仍待原输出验证。

## 5. 第4节概率解释的独立审查

作者用意义变量Y=g(s,x)，将所有可能问题/序列的非归一分数求和作全局Z，归一后定义意义概率，称Z只是共同常量不影响排序。这在有限、固定、Z存在的候选全集上成立，但不自动得到经验正确率校准。

第一，若按每问题条件归一，Z(x)一般随输入变，不再是跨问题常量；独立例原分.9/.8、相应Z10/1，归一后.09/.8，排序可翻转。若坚持全局联合问题—回答空间，还需要说明问题分布/支撑集，而非只写所有x求和。

第二，自由长度序列空间下几何平均分的全局和可能发散。独立构造：每步两个普通token各.25、EOS .5，原自回归分布几乎必然终止；含n个普通token再EOS的每条原概率为.5×.25^n，长度归一分为该概率^(1/(n+1))，随n趋向.25而非0，同时有2^n条序列。各长度分数和n=0/1/2/5/10约.5/.707/1.260/8.980/272.651，故无限求和发散。实际有max length时空间有限，不能用该例否定有限实现；它指出理论叙述需要有限支撑条件。

第三，归一成分布、对正确/错误排序、概率校准是三项性质。不能只根据AUROC变好就说Y已更准确校准，也不能从“class probability”类比推出某分数代表答案真值。第6页“B distinct meanings”均匀平均也应与保重复按意义分布采样的MC均值区分，承接I091待查点。

## 6. 数据、生成与标签协议

主评三组：NQ validation3610；TriviaQA validation子集8000；论文称WebQA并引Chang2022多模态WebQA，称train+test共6642。官方generate_answers.py实际load_dataset('web_questions') train/test合并，且Table 7三个示例均与WebQuestions页面示例对应。这是数据身份/引用冲突，应在综述中写清，不能称做了多模态WebQA验证。

进一步核看主来源 https://huggingface.co/datasets/stanfordnlp/web_questions （2026-11-06）：卡片简介也写6642，但split表train3778/test2032、页面总行数5810，二者内部不一致；当前代码组合应以真实载入数据为准，历史实验确切N仍缺原日志。不能直接把5810覆盖论文所有表格，也不能继续无保留写6642为已核分母。

模型Llama2-7B/base及chat、Mistral7B、Falcon7B-instruct、Llama2-13B，单模型不集成。主表采样5次、温度.5，中心答案greedy；同一2-shot问答演示。EOS句点限制回答长段落，容易影响缩写/多句答案，I066正指出类似旧管线截断问题；此处没有逐例重构，不能断言具体丢了多少答案。

标签一般由gpt-3.5-turbo相对问题和参考答案判断correct/false。源码只精确接受lower()后的correct/correct.和false/false.，未strip；格式不符回退BEM×100，而get_results以gpt_score>90为正确。遇多个参考取max；所以实际标签可能混合GPT与BEM，含格式/回退政策，不能无条件称全部人工金标。

没有原始判决缓存，无法计数回退比例、标签可靠性或替代裁判敏感性。BEM既产生importance伪标签又作格式失败的正确性回退，可能有相关误差；这是有明确代码路径的待测风险，不是已证明造成优势的因果结论。

清理脚本还检查ASCII：中心答案含非ASCII字符就不进入结果；任一采样答案含非ASCII也丢弃整条sample，而不是只清掉那个字符。例如含重音姓名的英语回答也可能触发，不只非英语句子。故最终评价分母还受生成器/随机采样/Unicode影响，8000等原始题数不能自动当作各方法实际评分样本数。未取得过滤日志，不报告虚构的丢弃比例。

## 7. 主表与消融的独立算术

Table 1五模型×三数据×三方法共45组MARS对基线比较全部正向。独立逐格录入复算Confidence提升范围.42–5.80个AUROC百分点，Entropy .87–6.24，SE .16–1.51；15格宏平均提升分别2.8487/3.1987/.7107点。宏平均只是这些表格条件的算术摘要，不是合并全部样本的AUROC或普适效应。

例如TriviaQA/Llama13B Confidence68.19→73.99，Entropy69.04→74.95，SE79.49→81.00。不能说“作答正确率增加5.8%”，这是检测排序指标变化。所有主表只single run，作者因成本未重复；“universally/significant”应限定为所报告格子的方向一致，没有置信区间/重复数据不额外宣称统计显著。

Table 2 TriviaQA短语优于token：Llama7B Confidence72.53→75.06、Entropy74.46→75.94、SE81.55→82.22；Mistral75.31→77.97、77.58→78.51、83.25→83.63。它支持该设置中phrase方案较好，但分块、伪标签、tokenizer等同时参与，不能单凭表格证明所有token方法均忽略语义依赖。

Table 3 equal/max-uncertain相近，min-uncertain较差；注意max在Entropy上反而更高：Llama77.11 vs75.94、Mistral79.22 vs78.51，Confidence则分模型不同。这反驳“等分每格最优”的过强说法，支持选择不确定子词有时重要。Shakespeare分词例是机制说明，不保证所有分词都如此。

Figure 4温度/样本数消融只有两模型TriviaQA，报告MARS优势大体稳定；不能据此推断所有领域的最佳temperature或无限采样单调变好。温度对表达多样性、错误及聚类可靠性的作用，应与I091/I066一起讨论。

## 8. 医学子集：资源版本和评价边界

论文称医疗专业人员协助从MedMCQA选415道能脱离多选项回答的题，用AdaptLLM medicine-chat和GPT-4评正确。该实验说明一个专门子集上的方法测试，不是临床安全验证，也不是医生实际用例的风险控制证明。

独立解析固定仓库medical_dataset.json实际411行、408个不同问题、无空题；比论文415少4行，存在3次重复问题带来的非独立性，暂未判断是否答案有冲突。没有改动原数据，不擅自去重后继续拿论文AUROC作比较。

源码医学裁判为gpt-4-turbo-preview，提示明确用自身医学知识，未提供参考答案；一般QA提供金标，参照方式改变。医学生成也有领域专用多示例提示，且importance权重额外τ=.001尖化，与一般任务统一2-shot叙述不同。必须区分实际分支和论文简述，不能把差异都归因于题目更复杂。

Table 4 Confidence62.41→62.89（+.48点），Entropy59.58→60.33（+.75），SE62.89→64.48（+1.59）；检测能力仍有限。这里SE提升1.59大于主表1.51，作者“up to1.51”对应一般QA主表范围，不应跨表理解为全论文最大值。无临床人评金标/区间，不能从这些数字导出部署保证。

## 9. 成本、局限与论文定位

110M相对7B参数约1.57%、13B约.85%，对应作者称1.5%/.8%的数量级；参数比例不是实际延迟或显存百分比。论文给Table 1约400 A100 GPU小时、伪标签200小时、importance训练7小时，必须区分离线成本和单次推理附加成本。

附录相对TokenSAR约30×“计算效率”来自10token×355M vs110M的粗量级推算，不是统一硬件延迟基准；批量、序列长度、token对齐和模型加载影响实耗。单遍forward不等于复杂度不随句长增长，只是调用次数不随短语数逐次增加。

限制包括英语、闭合答案、短QA、监督组件迁移、分块与BEM判错、稳定错误及不完整标签。不将低不确定性当事实保证；对附带不重要但错误的短语和拒答仍需证据核验/人工评价。

## 10. 提出的问题及已完成研究

问题A：提升来自权重还是训练数据适配？45格正向和短语消融支持评分有效，但四测试生成器也用于importance训练，BEM教师与数据域共享。可固定训练问题/生成器，做leave-one-generator-out及新域评估，再比较原BEM在线权重与蒸馏权重；当前没有原训练数据不能独立完成此消融。

问题B：理论归一能保证校准吗？本轮已给发散和输入相关Z反例，证明需要额外支撑条件/校准评价；不据此否定经验AUROC。后续统一有限候选集、保重复采样、类质量及校准集，再比较Shannon熵、I091簇均值和I066负log均值。

问题C：短语权重顺序会影响什么？独立.6/.4例证明非交换，源码路径已追到softmax目标和phrase内均值；需取得论文实际checkpoint及原样本输出再确定发表结果实现，不能只修伪代码后声称复现了表格。

问题D：医学改善是否是真域泛化？当前数据411/415版本差、裁判无参考、提示和τ变化，故不能把结果当纯domain shift控制。应先固定子集及独立人工事实标签，再在相同模块超参下比较；没有把这项尚未执行的研究写成实证。

问题E：怎样放入综述而不堆数字？以“序列评分中的词语重要性”串联I091的未解决token重要性、I066 attention加权、MARS的BEM蒸馏，再由I081区分排名/校准、C14讨论标签与版本。Table 1用于说明有限设定的方向一致，资源审计用于说明同名指标和数据不能无核查横比。

可用英文论点：“MARS combines uniform token weighting with question-conditioned phrase importance distilled from an answer-equivalence model. Its reported AUROC gains support meaning-aware scoring in the evaluated QA settings, while probabilistic calibration, label validity, and dataset identity require separate scrutiny.”

组内程子晨仍参与理论、源码、数据、比较和写作所有部分；其他成员可依原分工分别承接数据身份/标签复核、权重操作对照、资源成本及综述综合。此为协作接口，未声称成员已执行新训练/人工评审。

已完成全篇实质正文/附录、4页关键证据目视、固定官方代码、医疗数据清点、45组表格算术及独立理论反例。待补原实验commit、importance训练标签/权重、全部原始GPT判决/回退计数、WebQuestions历史实际分母和独立人评；未运行模型，未将这些待办计作复现完成。
