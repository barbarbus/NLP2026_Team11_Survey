# I071 LARS：学习式回答评分与不确定性排序

## 文献、核验范围、源码

Duygu Nur Yaldiz等，*Do Not Design, Learn: A Trainable Scoring Function for Uncertainty Estimation in Generative LLMs*，arXiv:2406.11278v3（2025-02-12），本地PDF23页；阅读方法、主表1–5、OOD表7–10/15、多语言表14、训练和提示附录。论文列出[专用LARS仓库](https://github.com/duygunuryldz/LARS)及[TruthTorchLM](https://github.com/Ybakman/TruthTorchLM)；均下载固定提交至`qa/I071_official`。前者截至本次获取只有README/LICENSE，没有可执行实现；后者为通用真值工具库，有算法代码，但不能据此断言完全复现论文的训练/数据处理。

## 问题与方法（PDF1–4）

问题不是检索证据核查，而是为封闭式QA/算术题模型的**回答正确性排序**提供不确定性分数。传统sequence probability是逐token条件概率连乘，长回答自然偏低；LNS取几何平均，MARS/TokenSAR对重要词赋权。但词义交互、实体类型概率偏置及跨语言工具可用性使固定权重不充分。论文的日期/人名例子说明同等答对率可有不同token概率，但那是描述性证据，未证明全部增益来自消除该偏置。

LARS输入问题x、回答token序列s和各token生成概率p，用RoBERTa-base(125M)+二分类头，以GPT-3.5-turbo对生成回答相对gold的正确/错误标签做BCE监督。把校准集概率分布按分位数切k箱（附录最佳通常k=8），每个概率转为互斥few-hot向量，缩放后插在对应回答token后，形成`问题—词—概率向量—...`序列；优于简单相加的实验配置，但序列长度翻倍并受RoBERTa上下文限制。训练5轮、AdamW 5e-6、batch8；超过5轮观察过拟合。**评分函数输出是监督正确性logit/分数，不是原生成模型序列概率**，代入Entropy/SE公式时是启发式替换，因此称作概率估计/校准需另验绝对概率可靠性。

## 数据、标签与评价（PDF4–6、18、21–23）

五生成模型：Llama2-7B/13B-chat、Llama3-8B-instruct、Mistral7B-instruct、Gemma7B-it。TriviaQA和NaturalQA训练各随机约1.3万问题、每问题采6个含贪婪输出，去重约6万QA对；GSM8K全训练约8千题。各模型/数据集通常另训LARS；这使方法依赖大规模**模型和任务相关的校准集**，与无监督LNS/MARS/TokenSAR并非同等标注成本。测试TriviaQA约9千、NaturalQA约3500、WebQA约6000（合并其训练+验证拆分作OOD测）、GSM8K约1000。实际模型正确性及训练标签均由GPT-3.5-turbo对gold与生成回答判定，不能当无误人工真值；需要审查教师偏差与题库泄漏。每问题UE估计采5个生成；Confidence只用贪婪输出，Entropy/SE等多采样，成本不能只比RoBERTa一次前向。论文报AUROC和PRR；AUROC是排序，不代表概率校准。正文称AUROC“对类别不平衡敏感”需谨慎：在固定正负条件分布下理论AUROC不直接由患病率决定，经验方差、任务混合才会变。

## 主结果（PDF5–8）

TriviaQA Llama2-7B：Confidence AUROC LNS`.697`、MARS`.751`、TokenSAR`.747`、LARS`.851`；PRR LARS`.760` vs MARS`.576`。SE下LARS`.849` vs LNS`.795`、TokenSAR`.796`。Gemma7B TriviaQA Confidence LARS`.819` vs TokenSAR`.688`，但不同模型绝对分数不能直接解释为“Gemma更易检测”。NaturalQA Llama3-8B Confidence `.812` vs LNS`.697`、TokenSAR`.717`。这些结果支持同域监督下排序提升；“up to 16% AUROC”应按论文所指比较口径，不与绝对百分点混说。表1 Llama3 TriviaQA无监督Eccentricity`.853`、LARS Confidence`.872`，两者调用和训练资源不同。

WebQA OOD Confidence Llama2-7B `.715` vs最佳TokenSAR`.664`，Llama3-8B `.713` vs`.656`。但**GSM8K算术领域转移失效显著**：Llama3-8B同域LARS Confidence`.836`，TriviaQA+NaturalQA训练的OOD LARS`.684`，低于TokenSAR`.719`及p(True)`.797`；Llama2-7B同域`.720` vs OOD`.603`。论文正文有“仍超过其他评分函数，除Llama3-8B”的限定，不能只报告平均成功。数学答案的数字语义使句向量一致性方法也弱，改变问题类型就需要重新训练/标定。

跨模型表3/15：在TriviaQA，Llama3目标模型用本身校准的Confidence`.874`，用Llama2-7B校准`.836`，用Mistral`.833`；表15 Gemma目标用其本身`.8311`，用Llama3`.7830`。迁移通常保留部分收益，却非完全模型无关。跨语言表4：Llama3 TriviaQA Entropy LARS 英`.864`、土`.814`、德`.827`、西`.835`，均高于TokenSAR`.793/.720/.758/.750`；这些数据来自Googletrans翻译原题、对目标语言提示、同语言重新标注/训练，**不是英语训练的零样本跨语泛化**，也非原生低资源语料。翻译质量与GPT判题可能引入共性误差。

## 消融及推断边界（PDF7–9、17–20）

TriviaQA Llama2-7B Confidence只文本`.750`、只概率`.721`、两者`.851`，表明两种输入互补；但“只概率”是两层MLP，架构也变，消融并不纯粹隔离信息。去问题`.832` vs全输入`.851`；简单句向量+概率MLP仅`.666`。附录以Llama3-8B/70B教师生成噪声标签训LARS得`.809/.837` vs直接问教师`.635/.746`，但所谓“without labeled data”其实仍使用教师伪标签与训练成本。序列插入概率词对长答案不适用；难解释哪些实体/词交互使正确性提升。所有主要评价限于简短答案与算术，不能直接扩展到长文多事实、给定来源忠实性、引用真实性。论文没有给ECE、Brier、可靠性图或真实风险覆盖点，因此“calibrated”只能按排序表现理解，不能证明数值概率已校准。未见多随机种子置信区间及人工判题抽查率，细小提升的稳健性仍待验。

## 后续研究问题及综述位置

1. 以人工双标小样本审计GPT-3.5教师在别名、数值近似、否定、时间问题上的误标，并报告噪声修正后的AUROC/PRR。
2. 固定总标注、采样、计算、延迟预算，对监督LARS、无监督LNS/MARS/TokenSAR和纯文本RoBERTa公平比较。
3. 以ECE/Brier、校准曲线、不同风险阈值下错误率和选择性回答收益检验绝对“置信度”。
4. 模型/题型/语言跨域时是更新几层、重算概率分箱、还是全量重训？区分答案实体类型变化与模型概率尺度变化。
5. 对长文/多论断输出做claim级或span级LARS，解决RoBERTa上下文、token对齐和复合答案标签问题。
6. 用原生多语问题及不同语言人工金标重复实验，排除翻译题和同一教师打标签的偏差。

综述归于**白盒可用token概率的监督不确定性评分**，连接I075置信度、I079内部态、I059黑盒一致性；与I070的黑盒书目检测在输入可观测性、监督成本和标签目标上分开。
