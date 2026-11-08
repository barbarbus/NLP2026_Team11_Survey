# I033 LLM-based NLG Evaluation：LLM裁判的四类路线与“谁来评估评估器”问题

## 来源、版本与阅读边界

Mingqi Gao、Xinyu Hu、Xunjian Yin、Jie Ruan、Xiao Pu、Xiaojun Wan，*[LLM-based NLG Evaluation: Current Status and Challenges](https://doi.org/10.1162/coli_a_00561)*，《Computational Linguistics》51(2)，2025，页661–687。资料库PDF共27页：PDF1–20为摘要、正文、结论与致谢，PDF20–27为完整参考文献；全部逐页阅读。目视核对PDF3图1、PDF12表2、PDF19表4，保存于`Reading_Notes/qa/I033_p3.png`、`I033_p12.png`、`I033_p19.png`。投稿日2024-11-26、修回2025-02-24、接收2025-03-14；作者称文献检索截止2024年6月，但定稿补入若干2025工作，因此“检索截止”和最终引用集不是同一个时间截面。

本文是综述，不提出新的幻觉检测器，也没有发布一个统一实验数据集。它对我们最有价值的作用，是把**作为评价工具的LLM**分为四条技术路线，并集中列出裁判偏差、可复现性和人机协作问题。它的对象是NLG评价，范围包括翻译、摘要、故事、对话、data-to-text、简化、改写、语法纠错和创作；明确排除广义“LLM能力评测”、评价数据集/benchmark综述和指标统计分析。因此它只能作为“幻觉评价器的上位方法论”，不能替代专门的幻觉定义、事实证据与错误类型综述。

## 文献搜集方法与覆盖范围的可信边界（PDF1–3）

作者称以Google Scholar关键词检索、截止2024年6月，纳入约100项工作；因为方向自2023年兴起，包含大量arXiv。正文没有给出可复现的完整检索式、检索日期、命中数、去重、纳排标准、双人筛选或排除清单，也没有PRISMA式流程。所谓“about 100”更像叙述性综述而非系统综述样本。参考文献又包含InteractEval、Zouhar等2025工作，以及2024年6月后的论文，说明接收前做过补录，但没有说明补录规则。我们可以引用其分类与代表工作，不应把“约100篇”写成穷尽性证据。

作者以“模型参数超过10亿”为LLM边界，这是一项操作性约定，不是能力阈值。文章强调LLM评价跨任务通用，故不按任务逐类综述；代价是同一个“consistency/factuality”在摘要、RAG、开放问答中的参照对象不同，容易被上位分类抹平。我们的综述必须继续保留**世界真值、输入忠实性、检索上下文支持、内部一致性、引用正确性**等评价对象，而不能只按“用了哪种LLM方式”组织。

## 四类方法不是互斥的算法族，而是LLM介入位置（PDF2–5、12–18）

图1给出四类：

1. **LLM-derived metrics**：读取LLM embedding或token概率，再经固定公式得到分数；包括embedding相似和概率/概率变化。
2. **Prompting LLMs**：用自然语言rubric直接让现成LLM打分、比较、排序、回答是非或标错误。
3. **Fine-tuning LLMs**：以评价标签/批评文本微调专用裁判。
4. **Human–LLM collaborative evaluation**：人制定/修订标准或最终复核，或LLM为人产生测试、预标错误、批评与审计线索。

这四类按“如何使用LLM”划分，实际可叠加：RAGAS先让LLM反向生成问题、再用embedding；G-Eval用prompt并读取离散评分概率；Prometheus的训练标签由GPT-4 prompt生成；COEVAL又调用LLM裁判但加人工checklist和复核。因此它适合作为**系统组件分类**，不宜当作每篇论文只有一个互斥标签。幻觉评价的更完整二维表应同时标注：评价对象/参照源、判定粒度、证据获取、裁判实现、人类介入、输出类型与元评估协议。

## 路线一：embedding与概率衍生指标（PDF3–5）

RAGAS answer relevance例：给问题`q`和回答`Y`，让LLM依据`Y`反向生成多个可能问题`q_i`，再算这些问题与原问题embedding余弦的平均。这个分数测“回答像是在回答什么问题”，并不直接验证回答事实。反向问题生成漏掉错误细节时，相似度仍可能很高；embedding模型和生成器共同成为隐藏评价器。

GPTScore把“高质量文本在给定context和quality instruction下应有更高生成似然”形式化为`sum_i log P(y_i | y_<i, X, I, theta)`。原式是token log-probability总和，若不同候选长度不同，未归一化会天然偏好更短文本；后续引用或实现是否使用平均对数似然必须单独核查。概率高只表示符合模型分布，不等于世界事实真；训练语料中的流行误解、模板与风格会进入评分。FFLM和DeltaScore比较加入一致/扰动信息前后的概率变化，能减少绝对似然混杂，但结论依赖扰动是否只改变目标属性。

作者总结优势是语义能力强于表面n-gram；风险是攻击鲁棒性、计算成本与社会偏差。闭源API通常不给embedding内部状态或完整logits，衍生指标不可用或只能依赖厂商接口。这里还缺少幻觉评价特别重要的风险：模型概率未经校准、模型自身知识过时、低概率新事实与高概率陈词滥调被混淆，以及token级信号如何聚合成claim/response分数。

## 路线二：提示式LLM裁判的五个设计轴（PDF5–11）

作者没有只列prompt模板，而是拆成五个元素：评价方法、任务指令、输入内容、评价标准、角色/交互。这一分解可直接用于我们的论文编码表。

### 评价输出

- **scoring**：Likert或0–100绝对分；方便汇总但尺度锚点、压缩、高分偏置和跨运行可比性成问题。
- **comparison**：二选一；中型FlanT5/LLaMA2有工作发现优于绝对打分，但产生位置偏差，且只能给相对偏好。
- **ranking**：一次排多个输出；上下文候选集变化会改变名次，列表顺序和长度增大负担。
- **Boolean QA**：Yes/No事实/忠实判定；适配二元标签，却强迫“不确定/证据不足”落入真假并受正类方向影响。
- **error analysis**：按MQM或预定义错误类别定位span；信息更细，但类别覆盖、span边界与多标签聚合需要独立验证。

### 指令、解释与示例

清晰、接近人工指南的直接指令通常较好；要求分析/解释有时提高与人评相关，但解释本身仍需人工评价，不能把流畅理由当忠实证据。one-shot不稳定地优于zero-shot，迭代更新demonstrations可能改善性能，但会引入验证集适配。早期模型可能拒绝或输出不可解析格式；作者称强模型上“基本不存在”，这一判断过强：结构化输出仍会受内容安全、长上下文、JSON转义、API版本与截断影响，所有实验仍应报告解析失败、重试和缺失值政策。

### 输入、rubric与交互

来源忠实性需要source，开放世界事实性需要外部知识；仅给目标文本只能测自洽/常识代理。某些翻译实验发现GPT-4无参考也胜过旧参考指标，不能推出所有任务“无需reference”，因为模型可能调用记忆而非证据。criteria可由人提供、LLM生成/去歧义/拆分，chain-of-aspects先打相关维度再给最终分；标准本身若由被评生态的LLM产生，会把其价值偏好写进真值。

交互包括chain（分析→排名→打分、问题生成→回答、事件抽取→核验）、network（辩论、branch-solve-merge、不同角色）和不同模型peer examination。增加agent数量不等于增加独立证据：同家族模型、相同训练语料和共同prompt可能高度相关；多数票只能降低近似独立误差。跨模型讨论还可能让正确的少数观点被高置信错误同化。

## 提示式裁判的已知偏差及其对幻觉评价的含义（PDF11）

文章集中列出：A/B位置偏差、偏好冗长回答、自偏好、style over substance、无reference时接受与对话历史冲突的回答、对对抗扰动不稳、在高质量摘要区间与人相关降低、非拉丁语言高分偏置、跨数据集/criteria/人类文本来源的大幅方差，以及闭源模型更新导致不可复现。

这些风险不是一张总相关系数能消除。用于幻觉检测时至少要做：双序交换或随机化；控制长度/格式；分别报告模型生成文本与人写文本；包含有证、反证、证据不足三类；按语言、领域、错误难度和质量区间分层；保存完整prompt、模型快照、temperature、日期与解析策略；在claim级报告混淆矩阵和校准，而非只报总体Pearson/Spearman。若被评模型和裁判同源，还应单列self/family bias。

## 路线三：微调专用裁判的监督来源问题（PDF12–15）

表2列出PandaLM 300K、Prometheus 100K、Prometheus2 200K、Shepherd 1317、TIGERScore 48K、INSTRUCTSCORE 40K、AUTO-J 4,396、CritiqueLLM 9,332、JudgeLM 100K、Themis 67K、Self-Taught 20K、CompassJudger-1 900K。除Shepherd社区人工数据、Themis混合人/GPT-4、Self-Taught用LLaMA-3-70B自标和Compass混合来源外，多数关键标签来自GPT-4；训练小裁判因此更接近“蒸馏GPT-4评价政策”，不自动等于蒸馏人类真值。

表3显示方法在scoring/comparison/MQM、reason/error、criteria显式/隐式/统一、是否需reference上差异很大。作者称这些专用模型通常少于14B、成本低、可复现且可接近GPT-4；但模型权重开放并不保证数据、筛选、prompt和训练过程可复现。更新foundation model往往需要重训，且“更强base必然更强judge”只是直觉，不是本文实验。

减少位置偏差的训练对交换、随机删除reference、类别/长度平衡、偏好优化和自迭代都是合理干预，但每项可能改变目标：无reference训练提升接口灵活性，也可能让模型以内部记忆代替证据；self-training可能放大已有偏差；GPT-4为中间输出提供error annotation可能造成教师闭环。AUTO-J、CritiqueLLM在criteria/reference灵活性上与Prometheus/JudgeLM/Compass的结果不一致，恰好说明“一个裁判覆盖所有rubric、参考条件和输出模式”存在capacity与data coverage冲突。

## 路线四：人机协作不是无条件的“最高性能类”（PDF15–17）

人指导LLM：COEVAL由人设计checklist，LLM初评/解释，再由人修订；约20% LLM分数仍被修改，是保留人监督的重要直接证据。InteractEval融合人和LLM think-aloud属性。HMCEval把样本分配给人或机器，文中转述其99% accuracy、约一半人工工作量，但跨任务泛化、分配器标签和成本须回到原论文核验。

LLM辅助人：AdaTest让模型生成测试、人反馈迭代，报告bug发现提高5–10倍；翻译预填error spans可减少标注时间；AdaTest++用于协作审计；LLM critique帮助人识别复杂输出缺陷。这一范式对幻觉评价的意义在于把LLM定位成**高召回候选证据/错误建议器**，人保留裁决，而不是让LLM直接成为不可质疑gold。

作者列出效率、互补和准确性优势，也承认prompt敏感、置信校准差、仍需人监督、协作过程难解释。更应补充：人可能锚定于LLM预标、自动化偏误；复核20%不代表其余80%正确；只把低置信样本交人会因裁判过度自信漏掉系统错；成本比较要包含培训、争议仲裁和界面时间。

## 表4数值复核与不可直接比较性（PDF18–19）

表4把SummEval的四维相关系数并排：BERTScore总体`.231`、BARTScore`.329`；GPTScore各模型`.324–.436`；G-Eval GPT-3.5`.409`、GPT-4`.523`；开源prompt Phi-4`.451`、LLaMA-3.1-70B`.427`、Qwen-2.5-72B`.497`；fine-tuned INSTRUCTSCORE`.258`、Prometheus2`.336`、Themis`.553`、TIGERScore`.384`、CompassJudger-1`.411`；InteractEval GPT-4两次`.714/.725`。Overall均为四列简单算术平均，抽查吻合，例如G-Eval GPT-4 `(0.582+0.507+0.455+0.548)/4=.523`，Themis为`.55275≈.553`。

但表头只写“performance”，未在表内标明Pearson/Spearman/Kendall、summary-level/system-level、prompt、采样、数据子集、reference条件和统计区间；数值来自Fu、Hu、Chu等不同来源，并非本文统一重跑。InteractEval“1st/2nd”结果也显示重复运行有波动，却没有置信区间。模型代际从旧BERT到2025 Qwen/Phi，训练数据可能含SummEval或相关评价资料。故从该表推导的总排序“人机协作 > 微调≈提示 > 衍生”是**跨研究描述性比较**，不能当受控消融或方法类型因果效应。

作者同时给出四个序关系：flexibility为协作>prompt>fine-tune>derived；reproducibility为derived≈prompt>fine-tune>collaboration；performance为collaboration>fine-tune≈prompt>derived；cost为derived≈开源prompt<fine-tune≈闭源prompt<collaboration。它们是经验判断，且存在内部张力：闭源prompt因模型弃用会不可复现；derived若依赖闭源embedding/logits同样会漂移；fine-tune一次性训练成本与大规模API长期调用要按样本量求break-even；协作成本随人介入比例变化，不能固定排最后。

## 未来方向与我们应吸收的研究设计（PDF18–20）

作者主张统一benchmark：覆盖多NLG任务和多评价方法、更新到现代LLM输出、扩大高质量人评规模。对幻觉评价应更进一步：统一不等于混成单分，必须保留参照源、错误类型与粒度；以文章/问题/来源分组划分训练测试；同时测判别、定位、解释、校准和选择性风险；公开模型输出而非只公开分数。

低资源语言方面，作者提醒非拉丁语言评价偏差，建议语言微调。仅翻译英文benchmark不足，因为实体音译、文化知识、形态、脚本、检索覆盖和人类rubric都会改变。新任务如科学评审还涉及可核实性、引用支持、时点与专业不确定性，不能照搬摘要consistency。

人机协作方面，关键问题不是“是否加人”，而是：哪些样本交给人、LLM显示什么证据、如何避免锚定、如何记录修改、怎样用争议反哺校准。可设计三臂对照：纯人、纯LLM、人+LLM；随机是否显示预判/解释；同时测准确性、时间、主观负担、automation bias和错误类型。

## 由本文提出并研究的问题

1. **LLM裁判到底是指标还是标注者？** 若输出固定可复算分数，可作为metric；若prompt、模型版本和采样改变判断，它更像有系统偏差的annotator。应套用人工标注质量框架：盲化、重复、inter-rater agreement、adjudication、calibration与漂移监测。
2. **“与人相关”是否足够证明能检测幻觉？** 不够。相关可能由长度、流畅度或系统质量排序驱动；需要claim级错误挑战集、对抗最小对、真/假/未知三类、分层混淆矩阵和人工证据审计。
3. **专用judge何时优于通用GPT-4？** 假设优势来自rubric对齐、开放权重、低成本；风险是教师偏差与任务窄化。须在固定base/数据预算下比较人标、GPT标、混合标，并做跨domain/语言/模型代际测试。
4. **多裁判投票能否可靠降错？** 只有误差近似独立才明显有效。应测pairwise residual correlation、同家族/异家族组合、共享证据与独立检索，并把多数票与基于历史可靠性的加权/stacking比较。
5. **协作中哪些样本必须升级给人？** 不能只靠裁判自报置信。应结合模型间分歧、证据冲突、检索coverage、OOD、长上下文、关键领域风险，建立选择性预测曲线，报告人工预算—风险而非一个accuracy。
6. **如何保证纵向可复现？** 保存完整输入、输出、logprob、prompt、模型与API版本/日期、解码、解析失败和费用；定期用固定锚样本测漂移。闭源服务更新后，旧分数不能与新分数无说明拼接。

## 对综述写作的直接用法

本文可作为“LLM-as-a-judge及其上位分类”的核心支撑：幻觉评价器可由embedding/概率衍生、直接提示、监督微调或人机协作实现；输出又可为打分、成对比较、排序、二元判断或错误定位。引用其结果时必须同时写明：四类会重叠；表4是跨论文描述性汇总；GPT-4合成标签使微调裁判继承教师政策；人机协作的优势依赖任务分配和人工复核；任何裁判都需要对偏差、鲁棒性、校准、解析失败、语言和版本漂移做元评估。

**一句话结论：** I033提供了有用的LLM评价器组件图谱，但它最重要的启示不是“用更强LLM即可替代人评”，而是LLM裁判本身就是一个需要独立证据、分层元评估和持续漂移监测的测量工具。
