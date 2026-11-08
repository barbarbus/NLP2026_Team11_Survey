# I041 Correctness and Faithfulness QA：答案满足需求与受给定知识支持是两条不同轴

## 来源、版本与核验范围

Vaibhav Adlakha、Parishad BehnamGhader、Xing Han Lu、Nicholas Meade、Siva Reddy，*Evaluating Correctness and Faithfulness of Instruction-Following Models for Question Answering*，TACL 12 (2024): 681–699，DOI `10.1162/tacl_a_00667`。本地arXiv:2307.16877v2（2024-04-17）PDF共18页，正文、附录A–C、完整参考逐页阅读；目视核对PDF7表3、PDF8表4、PDF10表5、PDF11表6、PDF13表7。

静态审计作者[官方instruct-qa仓库](https://github.com/McGill-NLP/instruct-qa)当前main及公开人工标注。源码保存为`Hallucination_Evaluation_Library/code/I041_instruct_qa_main.zip`（68,696字节），人工标注为`I041_human_eval_annotations.tar.gz`（21,053字节），两包均通过目录读取。检查Recall/K-Precision规范化、LLM judge解析、公开样本数、标签和worker details；没有下载庞大的全模型响应/索引，也没有重跑旧GPT-3.5/4或生成模型，不能声称复现表4–7。

## 最重要的概念贡献：correctness ≠ faithfulness（PDF1–4、8–9）

作者把RAG/给段落QA拆成：

- **correctness w.r.t. information need**：回答是否满足问题所需事实。只评价直接回答问题的部分，额外信息在此维度不扣分。
- **faithfulness w.r.t. provided knowledge**：回答中的所有信息是否可从给定段落直接得到或推断。真实但段落未支持的附加事实也算不忠实。
- **answer abstinence**：无相关证据时是否拒答、有相关证据时是否不误拒。

Figure1的One Direction例很清楚：参考答案London, England；回答增加“Mullingar, Ireland”。回答满足信息需求，correctness为Yes；新增事实可能世界上正确，却不在给定knowledge中，所以仅partially faithful。对我们的综述，这比笼统“幻觉”更精确：**外部正确性**与**来源归因/上下文忠实性**必须分报，低faithfulness不自动等于世界事实错误。

但“correctness只看直接相关部分”的人工定义与自动Recall不完全一致：Recall无法判断哪部分直接相关，也不惩罚额外矛盾。faithfulness则要求全回答受支持，是all-claims性质；长回答更容易出现至少一个不支持细节。两轴还受到回答长度的相反偏好：Recall偏爱冗长覆盖，K-Precision可能偏爱短、抽取式措辞。

## 数据、模型、检索条件与比较公平性（PDF3–4、8）

三数据集均来自Wikipedia：NQ验证集3610题、平均答案2.16词；HotpotQA 7405题、2.46词；TopiOCQA 2514题、10.98词。模型为Flan-T5-11B、Alpaca-7B、GPT-3.5-turbo、Llama-2-7B-chat。Flan训练明确包含NQ和HotpotQA，故这两项不是纯未见任务；GPT-3.5训练数据不透明。TopiOCQA在作者判断中更接近未见任务，但“发布日期晚于知识截止”不能排除相似Wikipedia内容或后续服务更新。

instruction models获得NQ/Hotpot各8段、TopiOCQA 4段，受上下文限制；FiD-220M基线按默认获得NQ100段、TopiOCQA50段、Hotpot最多18段。比较的是**整套retriever+reader与不同证据预算**，不是只比较生成器。更多段落既提高gold coverage也增加噪声，因此方向不必单调；仍应报告相同retrieval set的受控比较及oracle-gold条件。

生成统一用top-p `.95`、temperature `.95`、seed0，开放模型max500 tokens，GPT-3.5不设max。只跑一个seed且高温，会把采样方差混入模型差异；不同max又影响冗长、Recall和K-Precision。没有给API模型快照和调用日期的长期可复现保障。

## Correctness人工元评估：条件样本、重复问题与不平衡（PDF5–7）

只抽**gold passage已被检索到**的题，排除了retriever失败。每数据集100个问题×4模型=1200响应；每条向标注者显示问题/历史、参考答案和匿名响应，不显示passage。4名NLP研究生，每条声称双标，分歧取第三人多数；agreement92.42%、Fleiss κ=.764。

公开包核验：三个数据集各400行但各只有100个unique question id，说明四模型共享相同问题；行级相关把同题四响应当独立，会低估聚类不确定性。标签为961 `correct`、210 `incorrect`、29 `refuse-to-answer`，论文把后二者合并成239个Human=0。正类占80.08%，没有按数据集/模型报告混淆矩阵或置信区间。

公开`details`中1109条有2个worker记录，91条只有1个；看不到任何3条记录。可能发布包只保留部分原始标注/最终共识，或后续导出结构改变，但与“每条双标、分歧第三标”字面不一致。不能用当前包独立复算论文κ，须固定论文时数据版本或向作者确认。

## Recall为什么相关高，以及它测不到什么（PDF5–8、源码）

Recall对每个参考答案做SQuAD式规范化：小写、去标点、去`a/an/the`、空格切词；用Counter多重集交集除参考token数，多参考取最大。严格Recall要求规范化参考字符串完整出现在回答。它不惩罚回答额外token。

这正好修复“答案更详细”的主要假阴性：448/1200个Human-correct且F1≤.3案例中，Figure3称60.81%为More Elaborate Answers，另有open-ended、参考不完整、枚举等。但Recall也会给“Paris is not the capital”与“Paris”很高分，给同时列出正确和错误候选的回答满分；论文局限承认否定问题。多参考取最大还可能用一个短alias轻易命中。

表2：Human=1时EM均值.22、F1.45、Recall.85、GPT4 .89；Human=0时分别0、.10、.23、.13。正文先说以`.5`阈值F1在正确响应上“39% accuracy”，意味着61% false negatives；下一页却写“F1 has 39% false negative rate”。两句矛盾，不能同时引用。EM正确响应命中22%与78% FN是一致的。

表3把相关乘100：EM Spearman/Kendall均27.326；F1 47.341/40.164；Recall 60.048/55.622；BEM53.704/43.868；GPT3.5-Eval61.353；GPT4-Eval67.474。LLM judge和human均为二元，故两种秩相关列相同。相关在同1200条上选择“最佳廉价metric”，无外部验证集；问题和模型输出重复聚类，无CI/显著性比较。更应做question-cluster bootstrap、leave-one-model-out和leave-one-dataset-out，检查Recall优势是否由某模型的verbosity/style驱动。

## 表4不能直接证明instruction model比FiD更正确（PDF8）

Recall：NQ FiD54.45、GPT-3.5 57.98、Llama2 59.28；Hotpot FiD60.55、GPT66.77、Llama69.75、Flan71.28；TopiOCQA FiD61.64、GPT67.39、Llama61.40。论文说GPT-3.5超过FiD`6.48%/10.27%/9.33%`，这是相对增幅：绝对只高3.53/6.22/5.75个百分点。Llama在TopiOCQA“matching”是61.40 vs61.64的近似。

Recall的元评估只在gold retrieved条件做，而表4包含全检索流程，分布改变；FiD答案短、instruction答案长，Recall天然更容易在长文本里出现参考token。额外事实即使错误也不扣分，故这些表值支持“reference-token coverage更高”，不能单独支持“完整回答更正确”。最有力的验证应在表4各模型分层抽样人评完整事实，并同时控制长度/检索coverage。

Appendix B说明Hotpot task-specific multi-hop DPR对四instruction模型均最好；这证明检索器重要，也进一步说明表4是pipeline结果。BM25甚至普遍胜过普通DPR，不能把差异全归于LLM推理能力。

## Faithfulness元评估：gold也会被标不相关，partial被二值压平（PDF9–10）

每数据集50题×4模型=600响应，给question、model response、gold passage；先标passage relevant，再标fully/partially/not at all。正文称过滤不相关后剩544，agreement86.33%、κ=.7057；再把fully=1，partial与not at all均=0计算相关。

当前公开包却有560 `is_passage_relevant=true`、40 false，不是544。560中477 completely、51 partially、32 not-from-passage，比例85.18%/9.11%/5.71%，与论文85.3/9/5.7非常接近；可能论文/公开包版本发生变化。三个数据集仍各50 unique id、四模型共享；公开details中521条有2 worker、79条只有1个，没有第三标。元评估分母和原始标注结构必须版本化。

把partial与完全不支持都映射0适合“全响应是否完全受支持”，但丢失错误严重程度。85%正类高度不平衡；单个不支持数字即可与完全胡编同标签。应同时报三分类/ordinal agreement、unsupported-claim比例、span定位与response-all-supported。

## K-Precision实现、相关性与可投机性（PDF9–12、源码）

K-Precision把所有evidence段拼接，按同一SQuAD规范化，计算response token中也在evidence多重集里的比例。它是非对称的，避免长知识被K-F1的低recall惩罚；但“对knowledge长度不变”说法只在公式分母不含knowledge长度，机会重叠仍随段落变长而增加。规范化只去冠词，其他英语功能词保留，会产生无语义支持的公共token重叠；合法同义改写会降分，复制source会升分。

表5：K-F1相关为负`-10.266/-8.397`，K-Precision`49.849/43.384`，K-BERTScore precision`23.083/18.866`，Q²约`28.7/24–25`，GPT3.5 critic`23.851`，GPT4 critic`54.995`。GPT4只比K-Precision高约5.15 Spearman点，仍属中度；没有配对区间，不能确定“close second”的统计含义。

源码K-Precision++会从response删除所有在query中出现的token；若删完则直接返回1.0。这一空集合政策可给只复述问题的回答满分，虽其总体相关低于普通K-Precision。LLM judge若回复不是精确yes/no只打印警告，之后凡文本含`yes`就记1，否则0；例如解释里出现“not … yes”可能误解析。API异常递归无限重试，没有版本/失败分母审计。

## 无关知识与拒答：1001名段落不是真正人工反证（PDF10–11）

作者把“第1000名之后第一段”当作related but irrelevant，未报告人工验证；低rank不保证不含答案，也可能与问题完全不相关，不能代表难负例或冲突证据。Instr.v2明确要求无答案时回复“I don't know”，PIR用该短语和若干同义表达命中率；它主要测prompt compliance+absence判断，未给语义拒答classifier的误判率。

表6：GPT-3.5在无关段PIR NQ/Hotpot/TopiO为98.4/98.2/88.2，但给**gold passage**仍误拒47.4/25.5/31.8；Llama2误拒57.8/61.5/52.4。Alpaca几乎从不拒答。高PIR不能单独当好faithfulness，因为always-IDK即可满分；必须与gold下false abstention共同看，最好画coverage-risk/ROC并包含部分证据与冲突证据。

K-Precision relevant gold时Flan94.0/92.1/86.4最高，GPT/Llama约65–81。它可能同时反映Flan更抽取、更短、更接近段落措辞，不能直接推出其claim-level支持率最高。人工元评估需按model分层，特别做leave-Flan-out，确认相关不是“模型风格识别”。

## 真实检索表7中faithfulness升高是指标定义的机械效应（PDF12–13）

作者对retrieved passages算K-Precision；Instr.v2时把字符串`I don't know.`**额外视为一条retrieved passage**，因此拒答的token自然全匹配、K-Precision满分。论文明确承认always-IDK会获得最佳K-Precision而PG最差。故GPT-3.5 NQ K-Precision从81.50升96.27主要不能解释为更有证据的回答，可能只是更多拒答；同表PG从2.18升39.01。

PG只在gold passage确实被检索的子集计算：NQ36.79%、Hotpot79.28%、TopiO62.25。其余题中拒答可能合理也可能漏答，未构造完整应该答/不该答真值。Instr.v2下GPT-3.5 Recall NQ57.98→34.10、Hotpot66.77→40.08、Topi67.39→46.76；Llama也显著下降。

论文称GPT正确性平均降37.26%、Llama降29.37%、Llama faithfulness降12.33%，均是先按各任务算**相对百分比下降再平均**，不是百分点：例如GPT NQ绝对降23.88点、相对41.19%。综述引用须注明口径。

## 进一步研究问题与可复现实验设计

1. **二维真值矩阵：**每个atomic claim分别标world-correct、supported-by-context、contradicted、unknown，再聚合回答；保留“正确但未归因”与“有来源但来源错误”。
2. **长度匹配与对抗最小对：**对同答案加正确附加句、错误附加句、否定、候选列表和source原文复制，观察Recall/K-Precision能否区分；按回答长度配对模型。
3. **外部验证元评估：**按question cluster拆分，不让四模型同题跨折；leave-one-model/domain-out，三分类faithfulness和claim/span指标并报；bootstrap按question而非行。
4. **拒答作为选择性预测：**构造answerable、unanswerable、partial evidence、conflicting evidence四类；报告coverage-risk、answerable false abstention、unanswerable hallucination和效用成本，禁止把IDK加入evidence后单报K-Precision。
5. **受控reader比较：**所有模型给同样passages/同gold coverage和相近输出长度；FiD与instruction模型都做人评，分离retriever、reader、verbosity贡献。
6. **版本与数据发布：**固定模型/API日期、responses、人工原始双标/第三标、论文时annotation revision；解释正文544与公开560、单worker details的差异。

**综述可用结论：**本文最可靠的贡献是把QA的“满足信息需求”“由给定知识支持”“该拒答时拒答”分开，并提供1200 correctness与600 faithfulness的人评框架。Recall (`ρ=.600`)和K-Precision (`ρ=.498`)是廉价强基线，但分别奖励冗长覆盖和词面复制；它们不能单独支撑instruction模型比FiD更正确或Flan最忠实。GPT-4 judge相关最高但也只有correctness`.675`、faithfulness`.550`，说明评价器本身仍需审计。
