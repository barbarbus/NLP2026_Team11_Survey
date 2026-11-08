# 精读后研究地图（当前124篇）

这份地图给全部124篇已形成详细笔记的论文定位。16篇核心均已有正文细读笔记，但各篇附录/补充材料/复现待办尚未全部清零。类别可以交叉，不将方法硬分成互斥流派。

- I001 Factuality Survey：主类事实性/来源支持/相关性的概念边界及分解—检索—验证中间评价；次类二手综述证据、输出协议身份、开放世界识别、粒度/顺序/宏微及错误先验。
- I002 PHD/RV：主类黑盒整段实体反向问答/特征匹配自检；次类any-error目标与百分比容错、实体去名/substring/别名、全阳性子集及阈值先验、缓存复算、热门度代理和多角色知识相关性。
- I004 BAMBOO：主类长文来源条件的句子/摘要级二元支持性判断；次类**Yes/非幻觉正类**与反向指标、合成扰动/缺证据、格式评分、长度/指令/证据位置/检索成本及多任务分母。
- I006 ENOKI：主类文本锚定OpenIE事实的claim核验与span投影；次类三元组遗漏/递进多计、neutral并入冲突、教师自动标注、Span Coverage F1单字符满分反例、来源聚类/阈值/后端成本及数据版本。
- I011 FreshLLMs/FreshQA：主类时间敏感的开放域问答和宽松/严格双模式评价；次类错误前提、附加事实与拒答、FreshEval人机一致口径、搜索证据/答框/提示长度混杂、动态金标与历史API版本。
- I012 FACTOR：主类受控事实集合上的白盒LM四选一似然排序测验；次类五类扰动/NLI与语言模型过滤、真假候选标签污染、知识与表层捷径、检索证据、成对与四选一指标区别及开放生成筛选/neutral分母。
- I013 HALoGEN：主类九场景生成事实与拒答的跨域基准；次类来源/世界参照混合、每回答宏原子错误率与微率、空原子分母、程序/索引/LLM核验器覆盖、真值单类推理、引用存在与支持区别、训练语料A/B/C归因强度及资源计数审计。
- I014 HalluLens：主类训练语料/输入一致性定义与动态外在幻觉测验；次类Wikipedia训练代理、动态题的金标质量、拒答—条件错误—总体正确三分母、LongWiki检索/裁判误差及F1聚合、虚构实体存在性、药域全拒答、裁判提示与现存解析代码口径。
- I016 Embedding Distance：主类关键词嵌入/类内距离KDE的响应分类代理；次类截止日期即真假标签的模型身份混淆、同题重采样、成对距离伪重复、KDE概率/超参选择、附录反例、跨数据集基线不可比和增长百分比算术。

- I008 FactCHD：主类复杂推理合成问答检测与标签条件解释监督；次类阳性F1/格式覆盖、词面解释元评价、知识信息预算、多角色错误相关性、label/reason身份及训练测试完整重复。

- I102 MT-Bench/Arena：主类开放式多轮助手的人类偏好代理裁判；次类S1/S2条件分母、投票/题级聚合、独立参考与候选锚定、位置/冗长偏差、反馈说服效应、生成格式及模型训练风格/知识分离。

- I107 Illusion of Progress：主类QA检测伪金标与指标元评估；次类分歧人核的选择条件、拒答合并、长度/格式混杂、谱形状、百分比分母和平均次序、重复不变性及提示因果识别。

- I106 Lynx/HaluBench：主类合成扰动与标签条件解释蒸馏的RAG来源一致性裁判；次类任务粒度/忠实性界线、类不平衡、格式/长度捷径、宏微聚合、候选身份、缓存复算、格式解析与后续训练版本重叠。
- I108 Truthful Answers：主类开放域QA失败主题与知识诊断；次类记忆存在性/提示可答性、证据粒度Oracle条件、实体消歧/背景泄漏、substring判分、合理拒答与分母/配对统计识别。

- I103 SummEdits：主类十域局部编辑事实一致性基准与LLM裁判元评价；次类边界过滤、条件解释质量、种子聚类/Oracle信息、合成编辑偏差、原文分组划分及论文/发布版本差异。

- I104 LM vs LM：主类动态交叉询问的黑盒声明检测；次类矛盾错端识别、单类合成错误、substring标签粒度、不明确默认拒绝、投票/追问预算混杂与正式版指标对齐。

- I083 P(True)/P(IK)：主类候选自评与生成前成功率预测；次类可见选项校准、全模型监督、有限采样软标签/majority目标、域外校准、提示响应及模型特有自知。
- I101 Human-like Summarization Evaluation：主类LLM模拟四类人类摘要评价协议；次类来源支持/覆盖/偏好分界、prompt敏感、专家参照自包含、NaN覆盖、解释真实性与历史成本。

- I080 RACE：主类推理/答案联合采样一致性；次类忠实压缩、辅助模型白盒访问、最终答案金标与过程真值区别、熵代理与尺度、过滤覆盖/长度混杂及LFS资源对齐。

- I078 ICR Probe：主类残差更新—注意力投影散度的跨层监督探针；次类机制可识别性、公式/示例对齐、探索性方向选择、均值曲线稳定性、跨域失败和因果token位置控制。

- I077 Hallucination Snowballing：主类错误承诺与隔离验证的行为不一致；次类单类压力测试、CoT总风险/条件风险、图与整数程序真值、宏微聚合及跨论文输入沿用。

- I076 LapEigvals：主类单生成注意力谱的白盒监督探针；次类因果三角矩阵、非标准拉普拉斯解释、混合正确性标签/拒答过滤、提示与长度、跨集迁移和选参协议。

- I093 Hallucinatory (Un)answerability：主类上下文可答性与拒答识别；次类提示/beam干预、早期隐藏状态探针、概念擦除、类比例及可答内容保留代价。

- I094 SAPLMA：主类外部正确性监督的内部状态MLP探针；次类留主题泛化、合成真假数据、目标阈值校准、长度混杂与自知解释边界。

- I090 Semantic Entropy Probes：主类内部状态弱监督探针与采样教师压缩；次类在线/离线成本、teacher fidelity/事实检测双目标、跨任务协议和模型选择监督。

- I079 INSIDE：主类白盒多采样内部表示及log-det谱评分；次类测试时激活裁剪、Gram/高斯熵条件、代理标签/阈值及稳定错边界。

- I082 KLE：主类语义图核及von Neumann谱熵；次类SE推广条件、默认/监督调参、模型子组与检验、AUARC口径、边权和裁判调用链。

- I075 Generating with Confidence：主类黑盒采样语义图及答案级置信；次类输入不确定性、谱/度数/偏心度、风险覆盖、校准与方向性源码差异。

- C01 NLG Survey：主类跨任务历史与定义；次类IE/QA/NLI/LM方法谱系、来源外真实与任务差异。
- C02 LLM Taxonomy：主类LLM事实性/忠实性和成因；次类RAG失败分解、检测与基准。
- C03 Siren’s Song：主类三种参照冲突和生成/识别能力；次类生命周期、不确定性和跨语言。
- C04 AHE Survey：主类自动评估管线；次类SF/WF四象限、检索证据、元评估、实际部署。

- C05 TruthfulQA：主类基准与协议；次类训练裁判、拒答/信息性、版本漂移。纠正初筛将其主要放在裁判类的偏重。
- C06 HaluEval：主类合成与人工标注基准；次类识别、提示/证据干预、格式解析、选择偏差。
- C07 FActScore：主类原子事实与证据核验；次类模型整体分数估计、知识源限制与覆盖。
- C08 SelfCheckGPT：主类自采样一致性；次类NLI/LLM裁判、黑盒访问、预算。
- C09 AlignScore：主类训练式语义对齐；次类跨任务NLI、分块聚合、训练测试重叠。
- C10 Semantic Entropy：主类语义不确定性；次类自采样、聚类、拒答与confabulation范围。
- C11 TRUE：主类检测器元评估；次类来源忠实性、样本级AUROC、标签映射。
- C12 RAGTruth：主类RAG来源条件及跨度基准；次类细粒度定位、监督检测、风险覆盖。
- C13 FELM：主类多领域细粒度事实基准；次类声明分解、金标参考与数据版本。
- C14 Human Evaluation Survey：主类人工评价及报告可靠性；次类标注程序、定义与样本选择。
- C15 Audit：主类概念及术语审计；次类社会技术情境、实践者问卷与感知。
- C16 Pitfalls：主类定义与测量有效性；次类双向蕴含、遗漏、语用、任务适配。
- I015 EntFA：主类实体概率与世界事实性；次类源外真实、标注Unknown映射、KNN监督、指标作奖励及源码缩放。
- I007 FRANK：主类错误分类与元评估；次类生成器混杂、人工标签、官方修正和共同样本相关重算。
- I031 DAE：主类依存关系蕴含；次类弱监督、局部判断/整体聚合差距、单句来源、排序基准冲突样本。
- I035 Maynez：主类忠实性/真实性双轴与XSum人工标注；次类参考导语偏差、NLI/QA、标注粒度和分数重算。
- I042 FEQA：主类QA来源核验；次类抽象性、人评筛选、答案匹配、问题覆盖和批量接口顺序。
- I062 QAGS：主类QA双侧答案一致性；次类参考增强证据、题目预算、部件迁移、统计及源码接口可靠性。
- I073 FactCC：主类合成监督来源一致性；次类版本差异、micro-F1与BAcc、span解释、人机协作和抽象性迁移。
- I092 SummaC：主类NLI输入粒度与直方图聚合；次类多数据集元评估、标签标准化、目标阈值与文章共享。
- I086 QAFactEval：主类QA部件优化和可答性；次类监督语义匹配、QA/NLI融合、修改版基准及相关性层级。
- I054 Q²：主类知识对话QA/NLI核验；次类闲聊/人格参照、空题回退、精选标注与模拟系统排序。
- I072 Entity-level：主类实体来源覆盖和训练过滤；次类宽松匹配、空实体、条件测试集、实体计划与关系盲区。
- I043 QuestEval：主类双向QA综合评价；次类可答性/正确性、重要性政策、P/R目标冲突与公式/代码版本漂移。
- I036 NLI Ranking：主类NLI下游元评估与候选重排；次类条件样本、候选预算、句对/全文能力差异及MACE人工标签。
- I027 Adversarial NLI：主类对抗监督与域外排序迁移；次类基线实现差异、小基准重复使用、注意力解释与示例标签核查。
- I065 ChatGPT Evaluator：主类LLM裁判的早期摘要实验；次类提示/解析、A/B位置、域混合相关、解释错误与rubric漂移。
- I040 Unanswerable Beyond SQuAD：主类QA可答性部件的域外可靠性；次类竞争实体、IDK/不确定性区别、辅助NLI训练与公开数据跨度问题。
- I037 SummEval：主类人工评价与指标元评估资源；次类维度混淆、专家修订依赖、系统/实例层级、参考噪声和二值标签敏感性。
- I074 SCALE：主类长来源分块NLI；次类贪心证据检索、校准定义/端点、缓存分数和公开数据版本核查。
- I095 TrueTeacher：主类LLM监督数据与学生蒸馏；次类生成器/来源域分离、人评分层抽样、结构标签噪声与多语迁移。
- I100 G-Eval：主类LLM多维裁判；次类任务步骤、评分采样、解析失败、文章内相关与LLM文本偏好。
- I105 FairEval：主类裁判位置偏差；次类交换校准、采样分歧与人工介入、偏好/事实性区别和解析后不平衡。
- I057 RAGAs：主类RAG多维自动评价；次类来源忠实性、反向问题相关、上下文集中度、分解覆盖和历史版本/格式边界。
- I044 ARES：主类域适配RAG裁判与PPI总体估计；次类合成监督、人工抽样、模拟系统排名和统计覆盖条件。
- I088 SAC³：主类黑盒跨问题/跨模型一致性；次类语义漂移、验证者相关错误、单类检出率和采样成本。
- I091 Semantic Uncertainty：主类含义空间不确定性；次类概率估计、采样/聚类、QA金标、排名/校准区别及论文与旧源码差异。
- I081 Just Ask for Calibration：主类自报置信及后校准；次类有限采样、语言概率映射、语义裁判、交叉拟合及选择性AUC口径。
- I085 Predictive Uncertainty：主类条件生成token不确定性与集成分解；次类UABS干预、对象/动作/表格参照及事实性—信息性权衡。
- I066 CSL：主类内部似然的上下文token加权；次类attention头监督选择、裁判一致子集、采样基线敏感性及语义聚合实现。
- I084 MARS：主类BEM伪标签蒸馏的短语重要性加权；次类概率归一、权重操作顺序、数据身份和专门领域协议。
- I061 A Stitch in Time：主类概率筛查驱动的逐句外部核验/修复；次类误改成本、传播因果、预算及错误前提条件评价。
- I087 BSDetector：主类采样一致性与离散反思联合置信；次类答案重选、评审置信、人工分流及删除评价样本的选择偏差。

- I109 mFACT：主类多语银标教师蒸馏；次类翻译噪声、来源划分、跨语刻度、人评池化混杂和指标驱动损失加权。
- I110 HalluQA：主类原生中文对抗世界知识QA；次类误导/知识划分、参考与拒答口径、GPT4投票、缓存版本/分母和对齐/检索因果边界。
- I111 HalOmi：主类多语MT专业人工细粒度病理基准；次类幻觉/误译/遗漏区别、自然与扰动排名迁移、贡献/长度聚合、来源分组和版本/分母审计。
- I114 Needle in a Haystack：主类自然NMT严重脱离的尾部检测元评估；次类概率/质量差异、多标签互斥映射、选择分母、MC重排与修复误改成本。
- I118 OT Attention：主类内部attention边际异常与非参数参考库；次类TV/位置W1几何、门控尺度、真实数组/标签版本、误报口径及跨模型/多语适配。

- I112 Large Multilingual MT：主类跨资源/方向/领域的自然与扰动幻觉分析；次类ALTI/TNG校准、共同候选分母、模型规模交互、条件fallback、有限人验/抽取与公开缓存样本身份审计。

- I115 Med-HALT：主类医学错误建议/不可答与文献记忆基准；次类恒定拒答基线、标识符真值、语义/格式分离、归一化/异常分母、指令微调交互及真实/伪造构造审计。

- I116 MedHallu：主类医学合成答案判别与裁判相对难度；次类oracle上下文、非等价/遗漏构念、过滤家族偏差、长度捷径、NotSure条件覆盖率、parser/随机配对及表格均值审计。

- I117 MultiHal：主类多语KG证据注入与生成事实性；次类答案知情路径、关系支持/时效、问题与路径加权、参考集合、翻译审核、裁判/相关/误差条及公开缓存数值核验。

- I119 PsiloQA：主类多语QA自然生成错误的LLM银标跨度监督；次类来源/问题划分、标记文字到字符坐标、AP方向/空集/宏平均、多语训练量、源码重复权重/缺context和成本版本审计。

- I010 FAVA：主类开放域六类细粒度事实性与检索编辑的合成监督；次类不可核实/主观构念、句级类型与span区别、批次/多标分母、标签可逆性、宏平均身份、检索配置/信息保留及公开代码复现缺口。

- I019 RL4HS：主类字符跨度结果奖励的任务专门推理训练；次类gold最佳候选、宏奖励/字符微指标、类别mask/标准化、解释忠实性、质量筛选、STD约束与二元/定位及重训/迁移区别。

- I003 HADES：主类已知词/短语目标的无原文推理二元判别；次类有原文人核、扰动/主动选样、前缀/双向权限、共识选择、词子词索引、概率特征身份、Brier及隐藏测试复现边界。

- C12补核：已完成实质附录/正式版阅读，实际来源隔离和全部span坐标检查；研究重点增加标签政策翻转、质量分母、预测对齐和正式表格边际一致性。原预测复现待办仍保留。

组织正文时建议依次讨论：定义与测量目标→数据和人工标签→方法机制→元评估与可比性→开放问题。该顺序为当前证据支持的写作组织建议，待全部论文读完再修订，不代表最终综述已经写完。

- I005 ETF：主类代码来源条件的实体—描述句核验；次类AST/NER覆盖、函数版本、unknown外部依赖、entity与summary宏指标及any-error聚合。全CSV审计尚待下载。

- I017 HALO：主类黑盒多答句级蕴含一致性；次类SummaC有向算子与对称性断言、NBA人标相关和标注单位、知识注入的实体/事实泄漏、教师阈值调用成本、简答/CoT反向量化结果与一致错答盲点。原HALOCHECK最终实现及原始人标待核。

- I018 Language Models Hallucinate, but May Excel at Fact Verification：主类有检索证据的指令模型事实裁判与人工元评估；次类生成任务段落保留分母、无证≠虚假、答案词软概率/硬标签接口、检索/对抗证据质量、真句比例与any-error聚合、共指/数词迁移及SciFact训练污染。公开原始行/源码待固定提交复核。

- I020 Monitoring Decoding：主类强参考模型概率比监测的局部token重解码；次类论文加权和/现行代码乘积的版本差异、70B专家信息/成本权限、Top-N候选覆盖、任务真值/裁判差异、延迟吞吐不自洽、重采样token比例错列及直接专家基线。发表提交与模型运行待核。

- I021 RealTime QA：主类动态时点问答与检索新鲜度评价；次类公告/证据/提交/评分四时钟、英语周级测验、GCS不足五篇旧Wiki补齐、NOTA选项替换/拒答口径、六周错误分析与全年EM分母差异、日期消融例外及固定金标下延后检索的时间锚错位。历史仓库快照与基线重算待核。

- I022 Self-contradictory Hallucinations：主类同关系抽样触发的二句逻辑矛盾及迭代消冲突；次类原文内部矛盾/跨次采样区别、冲突不判定原句孰真、缺证算假标注、正确事实误删和句数式informativeness、两种SelfCheck比较目标、QA仅阳性人核下界与API token成本。原标注/旧模型复现待核。
# Stage 26：I023 Teaching with Lies

I023 → **检测器训练、合成负例筛选、课程DPO与评估协议一致性**。MiniCheck过滤`p<.25`并升序用剩余较难负例；与C08/I017采样一致性指标、I013原子事实裁判分属不同方法维度。其图2训练偏好是正确答案>幻觉答案，但二分类检测输入/输出未写全；正文与附录在难度术语、4/25轮、主表/消融F1存在冲突。重要表1平均F1`.612→.756`是两数据集macro均值，相对+23.53%，GPT-4o`.799`仍更高。详见`notes/important/I023_Teaching_with_Lies.md`和`Research_Questions_Stage26.md`。
# Stage 27：I024 HaluEval 2.0

I024 → **五域困难问答基准、GPT-4事实抽取/判断、逐回答幻觉率、训练/检索/解码因素实验**。8770题由三次低BERTScore相似筛选；最多抽五事实，FALSE计错。论文`MiHR`实际逐回答错误占比平均；公开`metric.py`过滤无事实回答，`judge.py`解析不足补UNKNOWN。PDF16裁判few-shot把相同罗斯福事实判FALSE并“纠正”为自身，是主表风险。与C08/I022无证据自检、I021动态问答、I013原子验证、I023检测器训练区分评价对象。详见`notes/important/I024_Dawn_After_Dark.md`和`Research_Questions_Stage27.md`。
# Stage 28：I026 FACTCHECKMATE

I026 → **白盒输入隐状态预判、EM代理标签、一次性激活干预**。预判“幻觉”来自短答案EM错答；真正未见模型跨架构表13近随机，见过三模型联合训练表2约71%。fθ定义为幻觉概率却以`≤.3`触发并选最高概率候选，gφ训练/推断隐藏状态时点文面不一致。图4摘要34.4%指GPT-4o两答案偏好赢率差，不能当绝对事实正确率。与I023检测器训练、I024生成后裁判、C08采样自检分属不同运行阶段。详见`notes/important/I026_FACTCHECKMATE.md`和`Research_Questions_Stage28.md`。
# Stage 29：I029 CONNER

I029 → **中间知识k的六维评价与最终答案a的有效性分离**。NLI逐维max/min使事实支持/中立/反证并非一律互斥归一，表2 FLAN few-shot三列和为108.55%；式7有效性NLI的文字与数学顺序相反。NQ中DPR事实支持97.78%却最终有效36.86%，LLaMA94.20%/42.00%，是来源/相关性等混杂的观察；LLM事实分与最终有效性的Somers相关NQ.15、WoW.24仍显著。接I024最终答案评判、I021时点证据、I013原子核真，详见`notes/important/I029_CONNER_Beyond_Factuality.md`和`Research_Questions_Stage29.md`。
# Stage 30：I032 FACTOOL

I032 → **工具增强、跨任务claim/query/evidence/judge流水线**。四任务真值分别为网络证据、合成测试、局部算术、引文元数据；表5以factual=True为正类，不能按幻觉正类读。附录显示代码同错多数票、数学局部对/全局错、KB把缺少额外信息当False。GPT-4版响应F1 KB71.79/code92.11/math80.36/scientific94.74；其60题排行榜又把该代理当gold，须降级。接I013原子核验、I024 GPT裁判、I029中间知识六维，详见`notes/important/I032_FACTOOL.md`和`Research_Questions_Stage30.md`。

# Stage 31：I033 LLM-based NLG Evaluation

I033 → **LLM评价器上位分类与judge元评估**。四类为embedding/概率衍生、直接提示、专用微调、人机协作，实际可组合；提示裁判再拆输出方式、指令、输入证据、rubric与交互。表4的SummEval Overall为四维均值，但数值来自不同论文、协议未统一、无区间，不能据此因果断言“协作>微调≈提示>衍生”。多数微调judge以GPT-4合成标签训练，应理解为教师评价政策蒸馏；位置、长度、风格、自偏好、语言和版本漂移必须独立审计。接C14人工评价、C16测量有效性、I024/I032 GPT事实裁判、I100 G-Eval、I105 FairEval，详见`notes/important/I033_LLM_based_NLG_Evaluation.md`和`Research_Questions_Stage31.md`。

# Stage 32：I034 ICE

I034 → **少样本数值裁判、示例分布先验与摘要多维评价**。4篇示例文章与1536测试摘要按source隔离，但同benchmark/rubric/系统风格仍共享；uniform consistency`ρ=.486, τ=.466`最好，relevance只在τ最好。stratified consistency降至`.298/.263`，说明ICL同时学习标签分布；缓存consistency仅4个预测值且1326/1536为1.0。三系统GPT-3/BRIO/T0只验证系统均值排序，且GPT-3 judge有同家族偏好风险。发布脚本只请求1候选并关闭rubric，首数字正则不验范围。接I037 SummEval、I065早期ChatGPT裁判、I100 G-Eval、I105位置偏差及I033上位分类，详见`notes/important/I034_ICE.md`和`Research_Questions_Stage32.md`。

# Stage 33：I041 Correctness and Faithfulness QA

I041 → **信息需求正确性、给定知识忠实性与拒答三分评价**。1200 correctness行来自每域100题×4模型，问题重复；Recall相关`.600`但奖励冗长。Faithfulness正文称544而当前公开包有560 relevant，K-Precision相关`.498`但奖励词面复制；partial被并入负类。GPT-3.5胜FiD的百分比是相对增幅；Instr.v2又把`I don't know`加入evidence，使拒答K-Precision机械满分，须与gold误拒和coverage-risk联报。接I029中间知识多维、I040不可答、I054 Q²、I057 RAGAS、I044 ARES及C12 RAGTruth，详见`notes/important/I041_Correctness_and_Faithfulness_QA.md`和`Research_Questions_Stage33.md`。

# Stage 34：I045 Can LLMs Express Their Uncertainty?

I045 → **黑盒口头置信度、多答一致性与失败预测**。GPT-4在GSM8K CoT准确93.6%、几乎全报100%，ECE`.064`却缺少筛错力，证明低ECE不等于实例级自知。GPT-3.5 Self-Random+Consistency五域AUROC`.730`，但同模型采样相关且稳定错误仍会高一致。表4 Pair-Rank均值ECE`.069`、AUROC`.676`；Avg-Conf虽5/6域AUROC最高却被GSM8K`.410`反转宏平均。源码确认10-bin ECE和PR类别方向，同时Pair-Rank脚本有断点/参数错误、无seed，CSV漏AURC表头而错列；表13与表3/10的Top-K GSM8K ECE亦冲突。接C08 SelfCheckGPT、I017 HALO、I020 decoding monitor、I026预判检测器及I033评价框架，详见`notes/important/I045_Can_LLMs_Express_Their_Uncertainty.md`和`Research_Questions_Stage34.md`。

# Stage 35：I046 Complex Claim Verification with Evidence Retrieved in the Wild

I046 → **时点受限web证据、复杂claim分解、检索—摘要错误传播**。无约束Acc49.0降到claim前且非fact-check来源33.0，claim-only25.5；MultiFC 82.7% claims至少含排除站点，揭示事后核查泄漏。10个generated subquestions胜原claim，但与平均3个gold问题未匹配预算。few-shot摘要单对11% major/wrong，claim级50条有12条至少一处严重错；更忠实版本覆盖反降，证明幻觉可提高表面comprehensiveness。源码top-5/默认few-shot与论文top-4/主表zero-shot不同，且含终检字段错误、硬编码凭据及README问题。接I021动态时点QA、I029多维知识评价、I032工具核验、I041 correctness/faithfulness、I044 ARES及C12 RAGTruth，详见`notes/important/I046_Complex_Claim_Verification_with_Evidence_Retrieved_in_the_Wild.md`和`Research_Questions_Stage35.md`。

# Stage 36：I047 FACTKG

I047 → **自然语言—KG路径核验、合成反事实与结构化解释**。论文版108,674条；GEAR77.65较BERT65.20高12.45点，但Multi-hop68.84低于BERT70.06。标签是DBpedia2015闭世界一致性，缺边/四跳外不等于现实为假；`imagine P⇒¬P`不成立，否定多跳还混淆`¬∃`与`∃¬`。当前README承认数据已修错；代码会drop尾批、best state未deepcopy、随机fallback未统一seed，Flan实现与论文token概率描述不同。接I032工具事实核验、I046真实web证据、I041两轴忠实性、I029多维知识与结构化KG路线，详见`notes/important/I047_FACTKG.md`和`Research_Questions_Stage36.md`。

# Stage 37：I048 ProgramFC

I048 → **复杂claim程序分解、迭代检索与模块化执行**。N=5在8设置7个最高，但HOVER4 open从N=1 59.16降至57.74，八项平均仅约+1.06点；迭代检索HOVER4 recall@10由36.43升49.93，但query预算更多。错例条件分析显示4-hop semantic program error77%。当前执行器只实现AND，OR/NOT未按声明执行；缺变量默认真、异常随机、平票偏REFUTE。Codex已退役，仓库切text-davinci-003；公开HOVER还有exact重复和相反标签。接I032 FACTOOL工具链、I046真实检索、I045多答一致性、I029分步知识及I047 KG执行，详见`notes/important/I048_ProgramFC.md`和`Research_Questions_Stage37.md`。

# Stage 38：I050 GraphEval

I050 → **自由文本三元组原子化、逐claim NLI与局部纠错**。表2样本量加权提升约6.2点，但九格等权仅4.84，HHEM+QAGS-X还降.3；任一triple过阈值的max规则会随triple数提高误报。论文未人工验证KG覆盖、scope保真或定位解释；Claude 2温度1且无重复。GraphCorrect的ROUGE只证保守编辑，修复率由同一检测器选样并验收，属循环自评，两项QAGS-X还低于Direct。接I013原子事实、I037/SummaC NLI分解、I047 KG核验、I048程序分解及I032工具纠错，详见`notes/important/I050_GraphEval.md`和`Research_Questions_Stage38.md`。

# Stage 39：I051 TOHA

I051 → **白盒注意力拓扑/MST、prompt—回答新颖性及少标注选头**。100个有标注probe选头且同集选N，主表不是真正零监督；CoQA/SQuAD以ROUGE极端筛选再用GPT-4o标注，可能使新颖性学到词面/长度捷径。Mistral CoQA/SQuAD AUROC`.89/.96`，CNN/DM仅`.60`；20次采样SelfCheck多处反超。仓库`n_max=6`与论文10不符，迁移p>.05不足以证明等效。接I118 OT Attention几何、I020 decoding概率、I045置信与I026白盒预判，详见`notes/important/I051_TOHA.md`和`Research_Questions_Stage39.md`。

# Stage 40：I052 INTRYGUE

I052 → **归纳头SinkRate门控token熵、RAG白盒忠实性预警**。归纳头/熵神经元干预支持局部机制，但完整误报中介未证；CoQA yes/no子群误报上升。主表验证选k、表9 XSum Llama2-13B `.73`与主表`.63`冲突，dynamic有退化；官方仓库尚缺原始标注CSV。接I051 TOHA复制头、I118 OT Attention、I045自报置信、I085预测不确定性，详见`notes/important/I052_INTRYGUE.md`和`Research_Questions_Stage40.md`。

# Stage 41：I053 InteGround

I053 → **多条证据完整性、证据充分性裁判与检索规划**。四域1625题，EB不全证据上Llama8B/Claude3 Sonnet正确率18.8/16.8%，但基于gold ID构造的负例未人工逐一核非蕴含，WiCE只取第一合法证据组。Premise abduction表6的16格9升7降、WiCE四格全降；Recall@5不等于找齐所有必要证据。反思多一次LLM/检索预算，源码缺数据缓存和API实现。接I048 ProgramFC规划、I046 web证据、I047 KG闭世界与I041忠实性，详见`notes/important/I053_InteGround.md`和`Research_Questions_Stage41.md`。

# Stage 42：I055 QuCo-RAG

I055 → **预训练语料实体频率/零共现驱动的动态检索**。OLMo-2六格EM高最强基线5.3–12.0点，但未固定检索预算；零实体共现不核关系，作者错答条件样本中仅抓47.0–51.9%幻觉句，漏检多数错误关系。0.5B抽取器可能把错误推理结论置空，源码API失败默认不检索；论文token成本只计生成文本，完整部署需4T索引/外部服务。接I053多证据检索、I048迭代查询、I046时点证据、I021新鲜度，详见`notes/important/I055_QuCo_RAG.md`和`Research_Questions_Stage42.md`。

# Stage 43：I058 Retrieving Supporting Evidence for LLMs Generated Answers

I058 → **答案扩展检索、top1证据一致性、自裁判确认偏差**。6,980题神经+reader预测Yes83.8%，只是支持标签分布；各预测类100例人工核验分别80/71/74%，加权约78.8%，并非独立幻觉率。表4数字可重算为84.54%一致，与正文83.2%矛盾。reader可补出证据中没有的数字，检索query又包含待核实答案。接I046真实web时点证据、I053多证据充分性、I041双轴定义与C12证据标注，详见`notes/important/I058_Retrieving_Supporting_Evidence_for_LLMs_Generated_Answers.md`和`Research_Questions_Stage43.md`。

# Stage 44：I059 Self-Checker

I059 → **模块化长答事实核查、BingCheck、人工候选锚定**。396长答/3840 claim，response准确63.4%，证据P30.5/R86.1；FEVER与WiCE距微调强基线仍远。gold消融只小幅提高BingCheck，提示裁决过度支持，但候选标注由系统预填。仓库有401 JSON、README命令错误与实验温度不符，已固定版本并剔除疑似密钥。接I048规划、I046来源时点、I053证据充分、I058确认偏差与C07原子事实，详见`notes/important/I059_Self_Checker.md`和`Research_Questions_Stage44.md`。

# Stage 45：I060 BTProp

I060 → **有标签校准的信念树概率传播、NLI逻辑边、模型内部自检**。FELM-Science AUC-PR比SelfCheckGPT高6.6/8.7点，但Wikibio两backbone均低于SelfCheckGPT；所谓后验依赖Wikibio前120条有标签样本、改写信心设1和逻辑边假设，未验证概率校准。Llama提示把外部数据缺失当false；官方仓库只含README。接I045口头置信度、C08 SelfCheckGPT、I059检索核查与I041两轴定义，详见`notes/important/I060_BTProp.md`和`Research_Questions_Stage45.md`。

# Stage 46：I063 Attention Satisfies

I063 → **白盒约束token注意力、监督探针、部分满足预测**。44,233个结构化查询上SAT-Probe提供与confidence相近且互补的AUROC，需预知约束token、Llama内部注意力和有标签训练。Wikidata流行度与注意力相关，无法由观察图推出因果；早停仅预测可行性，未量端到端拒答。官方数据/代码已固定保存。接I051 TOHA、I052 INTRYGUE、I060信念概率、I045置信与I055频率信号，详见`notes/important/I063_Attention_Satisfies.md`和`Research_Questions_Stage46.md`。

# Stage 47：I064 Bold Claims or Self-Doubt

I064 → **输出重复率极端两型、白盒hidden state分类、选择偏差**。10次抽样把重复10次和少于5次的错误答案分别称OH/UH，中间样本排除，测试OH/UH人为各500；ALCUNA只有UH，近1的分数易误读。Mistral表2 BAFH不及SAR，线上成本不能只报分类器.05秒。接I045置信、I060信念树、C08 SelfCheckGPT、I063探针与I068无知区分，详见`notes/important/I064_Bold_Claims_or_Self_Doubt.md`和`Research_Questions_Stage47.md`。

# Stage 48：I067 DRIFT

I067 → **问前中层状态有监督正确性预测、拒答与路由设想**。答案模式12格中10格AUROC最高；问前模式Qwen NQ所谓+13点只比同问特征Halo，低于Halo答案模式。TriviaQA拒答20%后留存正确91.6%，但没有真正fallback路由实验；零延时和`.1%`开销缺完整实测。GPT-4o一次答案对参考的判断是标签代理。接I026预生成检测、I063白盒约束、I064两型、I045置信与I053检索fallback，详见`notes/important/I067_DRIFT.md`和`Research_Questions_Stage48.md`。

# Stage 49：I068 Distinguishing Ignorance from Error

I068 → **高知识条件下提示扰动错答、HK+/HK−及模型特定标签**。六次全对后扰动错为HK+，六次未答gold为HK−，中间约5%排除；最高23.52%仅Gemma NQ高知识子集且雪崩错误示范。简单重提示更易修HK+，符合操作定义但不能直接推因果病因。官方WACK代码/数据已固定。接I064重复率分类、I067问前探针、I045置信与I055检索路由，详见`notes/important/I068_Distinguishing_Ignorance_from_Error.md`和`Research_Questions_Stage49.md`。

# Stage 50：I069 Do Androids Know

I069 → **给定来源忠实性的白盒span探针、有机/合成分布差与任务迁移**。10606条有机响应三人最小span标注，Fleiss κ`.39–.55`；同域response F1 `.75/.94/.90`高单专家，但CF span F1仍低专家`.03`。CDM合成训练→有机`.66`，E2E跨任务CDM训练仅`.06` vs自域`.86`，不能推通用真值表征。官方仓库目前404。接I063约束白盒、I051/052注意力、I050定位与C12标注，详见`notes/important/I069_Do_Androids_Know.md`和`Research_Questions_Stage50.md`。

# Stage 51：I070 Hallucinated References

I070 → **伪书目引用的黑盒作者一致性与直接自询**。六模型各1000条ACM主题书目，Bing引号搜索作近似grounding标签；仅GPT-4的100条由四专家核对。GPT-4融合AUC`.927`、ChatGPT`.792`、Llama70B`.702`，但稳定套用相似真书目的作者会高分误判。标签是可检索性代理，不是训练数据或论断真实性；官方代码、结果CSV与专家标注已固定。接I059一致性、I064重复率、I071知识边界及外部引文核验，详见`notes/important/I070_Hallucinating_References.md`和`Research_Questions_Stage51.md`。

# Stage 52：I071 LARS

I071 → **监督学习的token概率聚合与QA错误排序**。RoBERTa用问题、回答及分箱概率做监督评分；TriviaQA Llama2-7B Confidence AUC`.851` vs TokenSAR`.747`，但GSM8K Llama3同域`.836`转QA训练`.684`，且跨语为翻译题另训。依赖GPT教师标签，AUROC不能证明绝对概率校准。专用仓库当前仅README，通用TruthTorchLM仓库已固定；详见`notes/important/I071_LARS.md`和`Research_Questions_Stage52.md`。

# Stage 53：I096 UQLM Suite

I096 → **闭卷QA黑盒/白盒/裁判分数与监督线性集成**。四模型六题集共24组合、每题15候选；同域调权集成20/24 AUROC高于单项，但四个AI2-ARC组合均LNTP最佳。自动标准答案判题含前导整数与短答子串，不能直接当长文事实性真值；0–1归一化不等于概率校准。源码已固定，详见`notes/important/I096_UQLM_Suite.md`和`Research_Questions_Stage53.md`。

# Stage 54：I097 ChainPoll

I097 → **开放域Correctness/来源Adherence的五次GPT-3.5详细推理投票**。RealHall四集平均AUROC`.781`；DROP详细CoT`.794` vs普通CoT`.537`，但COVID/TriviaQA由GPT-4单独打标签、DROP `F1>0`即算正确，限制“金标”解释；没有公开官方代码/数据定位。接I096裁判、I070自询、C12人工span，详见`notes/important/I097_ChainPoll.md`和`Research_Questions_Stage54.md`。

# Stage 55：I113 Large Legal Fictions

I113 → **美国联邦判例开放域知识、假法律前提与重复率校准**。有金标任务汇总GPT4/3.5/PaLM2/Llama2错误率`.58/.69/.72/.88`，但拒答计非幻觉；GPT4地区引注三示例错误`.270`伴随拒答`.729`。高复杂度两答矛盾仅是“配对至少一错”证据，作为**单答**错误率下界存在分母漏洞（一般仅推出单答错误率≥矛盾率/2）。官方复现代码已固定，详见`notes/important/I113_Large_Legal_Fictions.md`和`Research_Questions_Stage55.md`。
