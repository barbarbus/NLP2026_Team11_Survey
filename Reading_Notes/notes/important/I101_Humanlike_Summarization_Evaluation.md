# I101 Human-like Summarization Evaluation with ChatGPT

## 来源、阅读及独立核查范围

Mingqi Gao、Jie Ruan、Renliang Sun、Xunjian Yin、Shiping Yang、Xiaojun Wan，arXiv:2304.02554v1，2023-04-05。原文：https://arxiv.org/abs/2304.02554 。本地9页；正文1–7页全部读完，7–9页参考文献定位，无另附实质附录。渲染并目视4/5/7页的主表、专家比较、解释与无效响应表。

检查作者页面 https://xunjianyin.github.io/papers/chatgpt-summarization-evaluation.html 及原文，未建立本实验原始ChatGPT回复、解析器与预测分数的官方仓库位置。已保存的SummEval官方人标、QAGS官方发布数据来自先前I037/I062核查，本次重用其原文件、记录哈希；不把基准数据当本篇作者预测。

独立脚本`sources/audit_humanlike.py`已运行，证据`qa/I101_audit/independent_audit.json`：用1600条SummEval原始人标重算含自身/排除自身参照的Spearman，核算QAGS多数基线、印刷accuracy差值、无效比例可能分母及历史成本。未调用ChatGPT，未执行作者代码或声称重现LLM相关系数。

## 1. 贡献与任务定位：统一交互形式，评价对象仍不同

把人类标注指令改成ChatGPT提示，让同一个API执行四种协议：1–5多维打分、两摘要偏好、SCU覆盖、句子来源支持判断。贡献是灵活的自然语言评价接口及早期元评价，不是发明新的通用幻觉定义，也不是四协议测同一东西。

Likert维度含consistency/faithfulness、relevance、fluency、coherence；总体质量相关性不能等同事实性检测。TLDR偏好允许综合考虑内容和风格；Pyramid覆盖率测摘要包含参照信息，不核验额外添加的事实；QAGS才直接给article与summary sentence判supported。综述应把事实性结果与一般NLG质量结果分别引用。

“human-like”指模拟人类标注格式，不代表达到人类推理机制、无偏判断或自动替代领域专家。不同数据和输入访问（原文/参照SCUs）也使结果不能合并成一个幻觉分数。

## 2. 四协议的输入、输出和标注单位（第2–3页）

**Likert，SummEval/Newsroom。** 原文+摘要一次请求四维1–5分。SummEval在无定义基线里把consistency改叫faithfulness，希望减少歧义；Newsroom四维为relevance/informativeness/fluency/coherence，不含独立事实维度。后续加定义提示又用consistency，所以变化不只增加字数，还涉及术语与任务解释。

**TLDR pairwise。** 原文+两摘要，要求只答Summary0/1、不解释。对照自动指标用各自评分决定胜者。没有显式tie选项、顺序交换或位置偏差消融；不能把整体偏好准确率当某条摘要是否有幻觉。与I105 FairEval相连，候选顺序是未控制因素。

**REALSumm Pyramid。** 摘要+已从reference提取的SCUs（最多16个），每单元Yes/No是否可由摘要推出。SCU来自人工参照，未自动构建全金字塔，也不是无需参考的评价。漏掉重要内容与新增错误内容不同：一个摘要可能覆盖所有SCU且另编一句，覆盖仍高。

**QAGS句子支持。** article+单summary sentence，Yes/No。真值相对来源，不是独立世界事实；需要明示是否按原始标注多数票、逐票或子句聚合。DAE/FactCC为对照，但其原始机制不同，尤其DAE依存弧与本文句子分类接口的归一需要源码确认。

## 3. 生成、解析、评价协议与复现缺口

固定gpt-3.5-turbo-0301，temperature=0、max_tokens=256，其余默认。该设置降低采样随机性，不保证历史API后端跨时间完全相同，更不能把这一旧快照结果直接当现行模型结论。

“simple rules”提取评分/标签，无法提取就NaN。未给完整解析器、超出1–5值处理、多次评分/解释矛盾的优先级、截断重试、NaN在不同相关/accuracy里的删除方式。256token一口气输出四维加解释也可能截断，原始回复未取得，不能归因所有无效为模型不能评价。

Likert报sample/system/dataset三级Spearman，但原文未精确定义聚合顺序。常见做法是每文章内相关后平均、系统均分间相关、全部摘要池相关；**这里只是候选解释**，不能未经代码就强行映射。不同文章/系统共享样本，独立性与bootstrap单位应按原文分组。

本次用官方SummEval确定100文章×16系统=1600摘要、每摘要3专家。下面重算明确命名为“pooled-summary”和“按系统均分”，不冒充作者未说明的所有三级算法。Newsroom/TLDR/REALSumm各子集实际条数、类别数及预测文件未建立，不从原数据全集规模推本实验分母。

## 4. 主表：SummEval领先与Newsroom失败要并列（第4页）

SummEval表1四维×三级共12列，ChatGPT均比列出的传统指标高。事实consistency的sample/system/dataset为.435/.833/.425；其中sample领先最佳BARTScore-cnn .367约.068，system领先BARTScore_s_h .800约.033。相关系数.833不是83.3%事实判对率。

Newsroom表2中ChatGPT各列落后两个source→hypothesis BARTScore版本，例如coherence sample .484，BARTScore_s_h .679、cnn版.653；fluency system .607对.964/.893。其排名不能描述为“只落后一个指标”，更不能由SummEval单集概括LLM裁判普遍最优。

准确率表：TLDR .6178对最佳BARTScore_h_r .6151，增.27个百分点；REALSumm .6436对DAE .6304，增1.32点；QAGS-CNN .8488对.8459，增.29点；QAGS-XSUM .7573对.6360，增12.13点。只有最后一项差距明显大。没有逐例配对预测、CI/显著性，不把.27/.29点写成稳健领先。

本次按QAGS官方原始数据“每句>半数yes”规则得CNN714句、支持531（74.37%多数基线），XSUM239句、支持116（48.54%，多数类51.46%）。这是明确规则下的基准结构核查，不能证明I101用了完全相同子集/票聚合；不据此擅自把论文accuracy乘714/239恢复整数混淆矩阵。

SCU和TLDR也必须报告多数/随机基线、每类precision/recall才能判断偏置。尤其Pyramid SCU有多少Yes未给，64.36%不自动比总说Yes强。

## 5. Prompt敏感性：详细指令反而破坏系统排序

表6加入定义（def）有些sample/pooled关联改善，例如consistency .435→.471、dataset .425→.479；fluency三项反而降，system .889→.606。定义不是无条件提升。

加定义+步骤，consistency system .833→−.149（差−.982），relevance .901→−.079（差−.980），fluency .889→.016。仅system role提示也使consistency .833→.007。相同模型/数据对文字形式高度敏感，支持固定并报告完整prompt；不能把“让模型扮人类+逐步看原文”当保证更可靠。

system correlation基于少量系统聚合通常比全1600点更敏感，但本文没有给失败系统、分数均值、有效项变化与置信区间。不能把相关翻转简单归因为prompt一定“理解反了”，也不能归因为仅1%NaN而已经证明；需原分数/解析/同样本比较来分离。

无定义时fluency/coherence两评分池相关.960，加定义后.843，下降.117。维度分离可能有所改善，却不是它们各自与人类更一致的充分条件；事实维度与语言流畅度仍可受同一次四维评分的halo效应影响，未做逐维独立请求对照。

## 6. 人类参照的自包含偏差：原数据上的独立重算

表6专家与“三专家平均”相关，均值包含被比较者自己。LLM则没参与人类平均，双方参照不对称。即使3个独立零均值同方差随机评分，单个X与(X+Y+Z)/3的Pearson相关也为1/√3≈.57735，与另两人均值相关为0；这是数学例子，不是假定真实专家随机。

重用官方1600人标，按发布expert_annotations列表槽位计算Spearman（不能独立确认槽位与命名专家始终一致）：

- consistency slot0 pooled含自身.901532，leave-one-out .759062；slot1 .881022→.762664；slot2 .796464→.758824。
- relevance slot0 .816065→.562216，slot1 .822787→.567816，slot2 .747073→.499898。
- fluency slot1 .876155→.610486；其system .843267→.721119。
- coherence slot1 .913239→.748759；其他槽位也下降，完整数值保存在JSON。

含自身pooled/system值与表6多项三位小数接近，支持其参照效应确实在该发布数据上存在；不是仅理论猜想。不过**不能把新的leave-one-out专家值直接与论文原LLM值比较**：LLM也应对同一个“其他两人平均”重新计算，当前缺LLM分数做不到。因此不据此宣布“专家优势消失”或“LLM超人”。

可改进协议是固定独立裁决人组、每一裁判都对相同不含自己的金标，或对人/机分别使用leave-one-out并明确不同参考带来的方差。比较单人、三人平均与模型还应包含标注者不确定性，避免将任何一组均值当无噪声真值。

## 7. 无效响应的分母、覆盖与选择偏差

表9比例base0、def .0003、def+ins .0106、sys .0013；对应拒评、不按要求评、另写摘要、续写等例子。最高1.06%，可读作格式完成率较高，但不等于评价正确率99%。

独立舍入枚举：若分母1600整请求，.0106可能17条、.0013可能2条，但**没有整数条数能四舍五入得到.0003**；若分母6400维度评分，.0003可为2个维度、.0106可为68、.0013可为8。它提示请求级与维度级invalid不能混用；当前不选某个分母当既成事实。

NaN如何进入表6相关性未说明。若各prompt删掉不同困难摘要，比较性能还会变样本构成；应在共同有效集、全请求故障计分、覆盖率三个口径分别报告。独立例子90对/100有效、另10无效，valid-only accuracy .9，但全请求成功率90/110=.81818；该例只解释分母，不是本篇真实计数。

## 8. 解释一致性不等于解释正确

表7同一错误体育摘要获低分，ChatGPT给与分数方向相符的解释；更详细prompt能把fluency/coherence理由分开。作者也明确解释未必正确，需要进一步测试。

只有少量选例，没有完整随机抽样数、逐主张证据定位、解释正确/完整/因果忠实的定量标注。原长article还未在表内展示，本次不凭模型的自称替其核实“第83分钟替补”等具体细节。检测器的解释也可能产生自己的幻觉；低分后合理化解释不能自动作为被评摘要错误的证据。

与I100 G-Eval比较，本篇是直接输出评分/可选解释，未学习自动任务步骤或使用token概率加权等级；与I105 FairEval比较，未做位置交换；与I037 SummEval比较，人标参照需注意expert/crowd和参照内含自身。

## 9. 历史成本与可重复性的准确表述（第6页）

作者按约1000token/摘要、当时每次.002美元、1600条得3.2美元；人类按12美元/小时、整集5小时得60美元，比例18.75，支持其“10–20倍”估算。该假设隐含平均每摘要11.25秒，包含四维、读文章和判断的时间只是作者估计，非测时实验；文章可共享阅读成本，需真实流程验证。

若3名专家同样工时则180美元、56.25倍，是独立条件计算，不是论文实测人工账单。不查询当前API价格，也不把历史3.2美元外推现行模型。重试、解析修正、标注核验和prompt开发均未充分计入。

temperature=0使同快照较可控，但无重复调用方差、版本间比较或完整缓存，不能从参数设置证明绝对可重复，更不能以人际差异直接断言机器评价更准确。可重复地给错分与正确地评估是两个目标。

## 10. 研究问题、得到的回答及综述引用锚点

**Q1：人类式提示是否足以通用事实评价？** 本篇支持多协议可执行及部分数据优势，Newsroom失败、SCU与偏好目标差异和小差值限制泛化。下一步按来源忠实/内容覆盖/偏好分任务，固定金标、覆盖及baseline预算。

**Q2：human gap有多大？** 原参照自包含会抬高专家相关，本次原数据重算已量化，但因无LLM分数无法同参考公平重比。后续取得回复/评分，以独立人标作共同参照，按文章bootstrap比较依赖相关。

**Q3：prompt改变了评判还是解析？** 严格同样本、逐维完整输出、原始回复归档、解析失败单列；将术语faithfulness/consistency、定义、步骤、role、最大长度分别控制，而不是一次混改后归结“CoT无效”。

**Q4：解释可以当证据吗？** 必须对来源逐主张核验，区分分数一致与事实正确；当前表7只证明存在可读解释，没有完整解释可靠性估计。

建议英文表述：*A single ChatGPT snapshot can follow several human summarization-evaluation protocols, but its agreement varies sharply across datasets and prompts. Human-reference self-inclusion, invalid-response handling and the distinction between factual support and overall preference constrain claims of human-level evaluation.*

页码：2–3页协议和prompt；4页表1–5；5页表6/7人机参照和解释；6–7页成本、维度相关与无效响应。已完成全文阅读、目视表格、官方基准数据独立重算；未取得本篇原ChatGPT预测、未复现LLM相关、未解决全部NaN/子集口径。
