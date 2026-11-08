# I097 ChainPoll：多次裁判投票、双类幻觉和RealHall基准

## 来源与阅读范围

Robert Friel、Atindriyo Sanyal，*ChainPoll: A High Efficacy Method for LLM Hallucination Detection*，arXiv:2310.18344v1（2023-10），本地PDF21页；逐页读方法、四数据集、ROC/PR图、全部附表、标注与排除理由。论文来自Galileo，描述其产品研究；全文未给公开官方数据/代码URL，资料包仅保留PDF及全文，不把产品实现当已取得的可复现源码。文内摘要称“11%/23%”须注意其参照与定义，不能等同百分点提升。

## 任务、算法及两套判据（PDF2–8）

回应级二分类：开放域为关于现实世界的错误陈述；封闭域为背离给定上下文，二者本质不同。ChainPoll用`gpt-3.5-turbo`读提示、原模型输出与相关参考文档（Adherence），按精心设计的详细CoT步骤先解释后判“是否有幻觉”；**通常独立调用5次**，`yes`比例是幻觉排序分数（高分更可能错），不是经校准的概率。Correctness提示检查开放域，Adherence提示检查来源忠实性。PDF7列表误把Adherence说成“detect open-domain”，但下一句明说Adherence用closed-domain提示，按定义与表4、图1一致应判为笔误。论文声称详细CoT可供用户解释，但解释的流畅性、因果忠实性和证据正确性没有独立人工验证；作者注释承认CoT未必反映真实推理。

## RealHall构造与标注（PDF4–6、15–18）

四集均以当时ChatGPT/gpt-3.5-turbo自然生成回应为核心：封闭域COVID-QA+检索（250k段语料建向量库，问题取top4，RAG式上下文）、DROP（文本内多事实离散推理）；开放域Open Assistant仅对话树首轮提示、TriviaQA去参考文档当闭卷事实问答。数据选择以“困难、现实、多样”为目标，排除多数旧摘要和人工合成幻觉集。值得注意的反例：HaluEval QA人为幻觉答平均66字符、自然“clean”仅14字符，长度捷径足以混淆检测；NarrativeQA存在原摘要找不到答案的病题，作者发现GPT4给ChatGPT答案8%错、给原gold答案12%错。可是RealHall仍仅四个选定域，代表性是作者的判断，不代表覆盖所有真实产品任务。

金标来源混合：Open Assistant早期有人类标；COVID-QA和TriviaQA用**GPT-4单独打标签**；DROP用bag-of-words F1，任何`F1>0`就判无幻觉（`F1=0`判有）。最后规则很宽：答中碰到一个正确词也可能判“无幻觉”，与文章开头“任何错误陈述”不一致。论文说GPT-4和人类分歧不比人类彼此多，但没有给人数、样本量、κ或类别条件统计，不能据此当高可信金标。GPT-3.5作为生成和裁判，不是完全独立的外部专家；GPT-4标注并未用于实时检测，但可能把评测对GPT风格偏好带入。

## 对照与关键数值（PDF3、8–11、19–21）

汇总四集AUROC ChainPoll`.781`、SelfCheck-BERTScore`.673`、SelfCheck-NGram`.644`、G-Eval`.579`、最大pseudo-entropy`.550`、GPTScore`.524`。若以`.781−.5`为机会校正优势，与`.673−.5`之比约1.62，表5的“质量百分比”使用这种扣随机基线口径，不能读成一般准确率。分集：开放域OpenAssistant `.697`（去详细CoT`.629`，SelfCheck-BERTScore`.555`），TriviaQA `.847`（去CoT`.818`，SelfCheck`.784`）；封闭域COVID-QA `.785`（去CoT`.707`，TRUE NLI`.727`），DROP `.794`（去CoT仅`.537`，SelfCheck-NGram`.722`、TRUE`.459`）。DROP的巨大差值显示特定详细提示对离散推理重要，也可能是提示定制/标签F1规则耦合，应跨模型和重新人工标注验证。正文仅报告AUROC，PR曲线图有展示但无AUPRC/置信区间；无重复运行标准差、阈值P/R或校准分析，不能确定差距在抽样扰动下稳定。

对照的模型/提示并非完全等成本：ChainPoll 5次GPT-3.5；SelfCheck原型20次生成并用BERTScore，G-Eval也用20次采样；GPTScore用`text-curie-001`算似然；TRUE用公开相近而非完全同训练混合的NLI模型。作者改写G-Eval/GPTScore原始任务专用提示以适应RealHall，这合理但可能影响原法表现；不能把所有差距归功于“详细CoT”或证明最廉价，因为未给统一token量、API报价和端到端延迟。其“低于GPT-4成本”对应2023价格，不是今天固定事实。自称解释可直接给用户，但理由若引用错误文本同样危险。

## 附录发现与待复核（PDF17–20）

在旧SummEval，GPTScore与单纯perplexity的Spearman分别`.460/.458`，ChainPoll-Adherence`.427`，显示不同数据分布下排名会反转。作者解释为旧摘要模型多输出不连贯文本，现代模型的似然轻易捕捉风格质量，未必识别细致事实错误。这是合理的数据混杂解释，但未做严格控制旧/新模型、长度、流畅度的反事实验证。Pseudo-entropy只见API top5/6概率、用已见概率归一化作权重但在log项保留原概率；附录排版公式有符号/文字矛盾（称“更低的entropy”却意图呈现更高不确定性），不应直接照抄为可复现公式；更要防止把pseudo-entropy当完整词表Shannon熵。

## 后续问题与综述位置

1. 公开RealHall每例提示、上下文、输出、标注者及裁判原始五次输出；人工双盲复核GPT4和DROP `F1>0`标签。
2. 固定生成/裁判调用token数、价格与时延，比较详细CoT、直接布尔、简短解释、NLI/外部检索与5次投票。
3. 使用不同家族裁判和不同年代生成模型交叉评估，减轻GPT来源耦合。
4. 报AUPRC、分类阈值、校准、风险覆盖曲线、bootstrap区间，并按错误类型/回答长度分层。
5. 逐句/claim检验CoT理由与实际证据的对应，而非仅把理由当说服性文本。

综述归于**LLM裁判多采样投票与基准选择偏差**。与I096的数值裁判/线性集成、I070直接/间接自询、C12 RAGTruth的人工span标签作比较，保持开放域真实性和给定来源忠实性分轴。
