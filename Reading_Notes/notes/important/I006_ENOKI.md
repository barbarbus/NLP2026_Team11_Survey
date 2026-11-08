# I006 ENOKI：文本锚定开放信息抽取与多粒度幻觉检测

## 版本、逐页范围和证据来源

Elisei Rykov、Timur Ionov、Nikolay Ivanov、Maksim Savkin、Maksim Makarenko、Alexander Panchenko、Vasily Konovalov、Julia Belikova，**ENOKI: Efficient Multi-Level Hallucination Detection**，[arXiv:2609.00581](https://arxiv.org/abs/2609.00581)，本地PDF v2 2026-09-04，22页。**已逐页读1–9正文/限制、12–22附录A–L，10–11参考文献作相关工作定位**；目视PDF1/2/5/6/8/14/15/22页的图、公式、主表及附录表。图1是示意而非真实模型运行，官方README也如此注明。无正式会议版可据现有资料断言。官方[仓库](https://github.com/s-nlp/Enoki)、[EnokiQA数据卡](https://huggingface.co/datasets/s-nlp/EnokiQA)及公开`evaluation/span_metrics.py`网页已核查；**没有本地固定commit/完整源码ZIP/208MB数据下载、没有运行模型或全量数据审计**。当前网络沙盒阻止Python外连、GitHub连接器传输失败，故对当前网页源码的陈述一律注明版本未锁定。单独的人工抽查、公式反例和表格算术也不当成主实验复现。

## 1. 研究对象及“多粒度”的准确含义（PDF1–4，图1–3）

输入是参考context与模型生成answer，目标同时输出可核验的事实单位、每单位是否由来源支持、以及answer中的错误字符span。ENOKI把回答按spaCy切句，抽取与回答词面锚定的OpenIE三元组(subject,predicate,object)，把每个三元组言语化成假设，经NLI式验证；不被来源蕴涵的三元组将其object或递进新信息delta投影回原回答字符位置。因此它绕过“先完全自由改写原子命题、再把错误命题反向对齐字符串”的独立对齐步骤，但**仍依赖抽取器产生准确字符span、分组和映射**；称“无需单独claim-to-span alignment模块”不能简化成“无需对齐”。

图1将“Lucien Tesnière生于Montpellier, 1893”拆成生年与出生地两个关系，前者被来源支持、后者不支持；它表明一个全句No标签无法告诉编辑者错在地名。图3从“cultivated in China”递进到“northern China”，先验证较粗命题，再验证更具体命题，新增的`northern`是候选错误delta。前提是两个命题按包含关系同义延展，且上一级验证可靠；多处错误、非嵌套改写、跨句指代会破坏这种局部推断。正文限制部分PDF9页也承认这些情形。

NLI对每个长context按验证器最大输入窗口切块，相邻块重叠一句，对同一fact取**最大蕴涵分数**（PDF4页）。这相当于存在一个单块可支持的假设；适合某一段能完整证明的事实。若支持需跨块联结（例如两个远段共同证明比较或关系链），逐块最大可能全部不够；若任一块出现表面相似但局部时间条件相反，最大值可能掩盖另一块冲突。这样是**证据聚合假设**，不是把整篇长文的逻辑合起来验证。应单独测试跨块事实与互相矛盾来源；仅加大输入窗未必解决证据选择与时间规范化。

“hallucination”在该框架中是相对于给定context的**非蕴涵**：NLI输出neutral+contradiction概率>0.5即报错（PDF6页）。缺证据与明确反证被合并；这对严格RAG来源忠实性合理，对开放世界事实真假则不等价。某fact真实但维基文章未提及可被报“不支持”，不可写成世界为假。每句只检查**已抽出的**事实；无抽取→无检测，而非证明全句正确。表中句级、实体级、span级结果也各有不同gold对象，不可直接相加或比较数值高低。

## 2. 三种抽取后端与训练目标（PDF4–5、12、17–18、20–21）

**ENOKI-LLM**沿CycleOIE prompt，增加递进参数片段、复合参数分解和前后修饰递进示例。附录J原prompt要求显性SPO、被动主动并存、归因与被归因内容分开；附录K递进prompt举“former basketball player”抽`player`→`basketball player`→`former basketball player`。它还把“joined on March 15, 2021”拆为对March、15、2021各自的`joined on`三元组，明确**不**抽完整日期。这会失去日/月/年的组合约束：单独月日年成立或看似成立，不能证明原完整日期正确；`joined on 15`在无月份时语义也不完整。可用“加入日变但月份年同”的例子验证：所有分裂fact需能识别哪一维错，然而对组合型日期的整体合法性和对应关系无法保证。这是从prompt推导的潜在失败，非运行结果。

**ENOKI-RULE**用spaCy `en_core_web_trf`依存树和35规则，不需训练LLM。附录H给预处理、分句分从句、规则触发、head到span塑形、完整性过滤、(s,p,o,prep)词形化去重、输出；每条规则候选受统一spanshape和接受门控制。Stage1在OpenIE6/LSOIE合计5,063个gold三元组的子集上，从空规则发展到16条，评分S=triple F1+0.25×predicate覆盖率，且需ΔS>0。Stage2在名为`EnokiQA-val`的58k句上再添19条、两种随机seed各2000句门控，要求ΔS>0且ΔPrecision≥−.0075，最终35条，分七簇。此开发过程是有标注和代理提出候选的**数据驱动规则设计**，不能把“inference training-free”误写成“开发完全无监督/无验证集”。附录H称Stage2 `EnokiQA-val` 58k句，与正文ENOKIQA dev1995条/5474句不易直接对上，可能是另行构造的规则开发划分；需要脚本/manifest明确是否使用测试源、标签以及独立性，不能自行等同。

**ENOKI-ENCODER**保留OpenIE6式固定深度词级网格，换ModernBERT-large，提出用Hungarian二分匹配代替按行顺序对齐的CE：先算各预测行与金标行的CE矩阵、最小匹配，再对匹配行训练（PDF5及附录A）。这样避免同一集合不同排列被罚。仅当最大深度足够且金标三元组都正确，置换不变性能解决行号噪声；没抽出的关系不会因匹配自动恢复。训练取ENOKIQA dev1995条生成5474句、36865个**ENOKI-LLM教师三元组**，句级随机5%验证，深度14覆盖95%；权重初始化ModernBERT-large，学习率2e−5、batch32（附录C）。开发集被用于抽取器蒸馏和深度选参，不能又当独立外部评估集。由于同一回答及维基文章含多句，随机句级train/val可能共享文章和答案风格，验证loss不能证明跨源泛化；实际跨集仍看独立benchmark。附录A表5显示Hungarian对MuSHROOM/RAGTruth/PsiloQA Span Coverage F1分别41.02→46.96、27.25→34.84、61.14→65.51，支持该同一训练设置下有益；不单独证明此设计对所有抽取任务更好。

## 3. EnokiQA：样本数、教师标签与人工检验（PDF5–6、18–19、22）

英文Wikipedia段落给GPT-OSS-120B生成**需多句、至少五项细节**的事实问题，滤掉答案泄漏、非独立/难以来源回答问题；原问题10926→筛选6774。七个指令模型**无context**回答，提示禁止说没有上下文/请求澄清、要求单段、温度.9（附录I），有意提高知识缺口暴露与幻觉；这不是自然用户RAG请求分布。全维基文章随后作为验证来源，另经回答相关性/长度/近重复过滤。问题生成时只看段落、验证看整篇，来源预算改变需清晰记录。

训练19594条**未标注QA-context**，dev/test各1995**自动标注**，合计有标签3990；dev/test每个七生成器285条。附录L平均answer字符train5525/dev5636/test5727、context13035/13942/15816；dev/test每答案教师抽取平均250.6/246.8个递进三元组，median231/226；作者所谓平均hallucination rate 77.8%/76.0%是**教师抽出的三元组中，Qwen验证器判neutral/contradiction的比例**，非“76%回答含幻觉”、非世界真实错误率，也不等于原子事实真实错误比例：同一错误可跨宽度多次计数。应报告按唯一语义事实/句/回答聚合的比例，并以人工样本校准。

dev/test金标由**同框架的ENOKI-LLM GPT-OSS-120B**抽三元组、Qwen3.5-9B NLI判别、投影成span。用于训练ENCODER是教师蒸馏；若再用EnokiQA自动标签评价某方法，和教师的一致性可能被误当人工事实准确性。主表实验使用其他benchmark作外测，这一界线较清楚；然而EnokiQA本身“双粒度人工金标”并不成立。两人独立标100条test，字符级κ=.580、raw≈.80；相对裁决人标，自动sentenceF1=.867、spanF1=.569（PDF6）。只有100回答、且前者/后者不同粒度与不同分母，不能把.867说成全3990条标签“准确率”；没有报告按生成器/流行度分层置信区间。数据卡当前只显示**dev/test**3990行、208MB；论文训练19594不在该HF数据卡列出的可加载split里，可能另在repo，需查发布位置再声称全量可复现。

附录L还有**test1995条仅285个不同Wikipedia context**，恰好1995=285×7，提示每一来源对应七生成器回答（需逐条ID验证）。即便只据聚类统计也不能把1995行视为完全独立文章；比较模型及显著性应按来源/问题聚类，注意跨dev/test是否有文章重合未公布。dev1081个、train2226个unique context，同样不可从单独数量推断划分隔离。

## 4. 指标及其重要盲点：Span Coverage F1（PDF13–14；当前网页源码）

作者指出粗标注可能圈完整短语/句，而真正错误只在一个词。附录E以MuSHROOM中的世纪数字/庞贝壁画及RAGTruth中把“伏击”写成“Waze”为例；精确匹配会因预测太窄而罚分。提出的Span Coverage指标定义：一个预测span **完全包含于至少一gold span**即记precision成功；一个gold span**包含至少一个预测span**即记recall成功；两者调和，跨样本micro汇总。两边均空按perfect-match。这个指标测的是**落入标注范围/命中每个粗区**，并不度量预测覆盖了多少错误字符，也不保证那个局部字符确为错误。

独立数学反例：gold=[10,100]，该区内实际只有[70,74]是错。预测[12,12]一个本身无错的字符，仍满足包含关系，单样本P=R=F1=1。若预测[70,74]也得1，指标无法区分真正精准定位与“圈内随便猜一个字”。若一个gold含两个相隔错误，预测只命中其一同样得满recall；若同一错误被预测成多个内部细片，每片precision都得1。若多个gold高度嵌套，单个预测可同时满足多gold recall。不能因此断言论文表3模型真的用这种投机策略；这是**指标构造的识别边界**，需对真实输出做span长度/位置/嵌套敏感性分析，并配字符级IoU、exact-boundary、最小错误人工评估。

附录E声称代码边界为**闭区间**`[s,e]`，而当前仓库`evaluation/span_metrics.py`文档明说依赖外部`mycelium-scorer`且使用**半开区间**`[start,end)`；数据卡示例也用半开。代码默认`min_pred_len=1`、`delta=0`、`empty_is_perfect=True`。这可能是论文表述/当前发布版本的差异；不能在未固定依赖版本和表3原始预测前判定印刷结果被边界off-by-one污染，但方法复现必须精确统一坐标约定。当前仓库是外部库代理，不可把公式与当前wrapper当成完整评分实现。对空-空如何在micro分母加权也需读`mycelium`内部实现，不能仅凭公式猜。

span benchmark按训练子集最大化Span Coverage F1选阈值；MuSHROOM无标注train则用.5（PDF7）。各任务阈值预算不同，MuSHROOM分数不能直接同RAGTruth/PsiloQA公平排序；且maximizing同一指标容易偏爱过窄span。句级所有明确NLI方法固定.5，指标为macroF1/AUROC。HalluEntity是预分割实体/谓词/短语单元，指标AUROC/AUPRC，不能把AUPRC55.09解读为55.09%实体正确率；AUPRC还依正类率/单位定义。

## 5. 结果逐表核对：何处领先、何处不领先（PDF6–8、12、15–16）

HalluEntity表2：ENOKI-LLM AUROC79.70/AUPRC55.09；最高**外部**AUPRC基线MinIE39.77，差15.32**百分点**（非相对15.3%）；GPT-5.2零样本AUROC77.63/AUPRC36.63。LLM非递进prompt自消融78.11/54.78，递进只+1.59 AUROC、+.31 AUPRC，不能把15.3pp增益归因于递进prompt本身。Rule76.41/46.81、Encoder70.47/44.25，不是同样达到55.09。附录B替GPT-5.4抽取为81.55/56.99，比GPT-OSS+1.85/+1.90；仅HalluEntity一个表，不足以证明抽取子问题普遍“容易”。

span表3（**Span Coverage F1**）：MuSHROOM ENOKI-LLM52.07、最高外部MinIE44.12，+7.95pp；PsiloQA ENOKI-LLM71.15、MinIE64.06，+7.09pp；RAGTruth ENOKI-LLM37.32，RAGTruth微调Qwen3-8B**42.20**、haldetect41.54，故不能说本方法三集通胜。并且ENOKI-LLM**不递进**在RAGTruth41.35 > 递进37.32（−4.03pp）；MuSHROOM41.90→52.07、PsiloQA65.34→71.15则有益，跨数据集机制不一。表8把NLI改Qwen3.5-9B：MuSHROOM52.07→54.22、RAGTruth37.32→42.98、PsiloQA71.15→70.36，说明验证器选型有影响；Qwen也用于EnokiQA教师标注，不能把差异全归抽取器。

句级附录F表9：ENOKI-LLM FactCheck-Bench F1 59.64、ANAH-250 56.41、RAGTruth-250 76.42。前两远低于不用分解的NLI基线67.44、74.80，也低于Claimify GPT-5.2的72.71、65.56；RAGTruth-250虽高于RefChecker76.31仅.11pp，缺方差无法判稳健胜。表9各基线抽取模型/检测访问不同，论文没有统一“同型号相同预算”的全方法消融。正文说句级“competitive”比“全优”准确。表4可选FastCoref使RAGTruth span27.87→30.92、ANAH句63.78→64.98，HalluEntity AUROC76.41→75.83、PsiloQA65.73→65.50，不可默认coref有益。

效率附录G表10/11按每句：FactCheck-Bench ENOKI-LLM11.12秒、Rule.11、Encoder.13，约101倍/85.5倍；RAGTruth分别7.88、.09、.09，约87.6倍。正文图4写Encoder RAGTruth .13秒与附录表11 .09秒，可能是不同报告设置，须查计时环境/表别而非合并为唯一时间。逐方法输入模型大小不同、OpenAI兼容API网络时延/批处理不同；表10 ENOKI-LLM的FLOPs .05×10^16与其11.12秒并不逻辑矛盾，FLOPs≈2PT粗算只是一个代理，等待/调度也计时。表11同后端FLOPs3.51×10^16，反映任务prompt长度/调用配置，可比价格与吞吐还需模型部署、缓存、批处理和成本明细；“两数量级”只对这些历史测量的一些比较成立。

## 6. 与已读论文的交叉问题、待核和可执行研究

1. **三种粒度如何一一映射？** 对同一回答从三元组→字符span→句级标签同步记录遗漏、重复、不可定位、跨句指代；对照RAGTruth的原字符span与FactCHD的回答级标签，统一清楚**语义事实、提取条目、标注跨度、最终评分单位**四层。特别是EnokiQA每答案约250条增量三元组，不能把计数当250独立事实。
2. **验证器与教师一致性。** 用独立NLI模型及人工三分类裁判对同一批事实重判entail/neutral/contradict，考察`neutral+contradiction>.5`与世界真假/来源支持的关系；对dev/test教师标签评价同族方法时报告教师偏差。注意公开100人工样本只衡量那批回答的总体，须按实体流行度/七生成器/answer长度分层。
3. **Span Coverage指标压力测试。** 对MuSHROOM/PsiloQA/RAGTruth原gold，用预测每个gold的首字符、随机内部字符、人工最小错误span、原完整gold四种纯数学基线比较coverage、IoU、exactF1；单字符基线可能有高coverage但无需模型。分析空-空micro处理、闭/半开边界和`min_pred_len`；取得依赖包源码固定版本后再称动态复现。
4. **证据聚合与长文。** 标记一个事实要两个chunk联合才能支持、不同chunk互相矛盾、以及不同时间的陈述；比较max entail、证据组合和全局判定，测错误类型及成本。不能把“读到整篇文章的每个chunk”自动当综合推理。
5. **资源独立性。** 下载并pin仓库/EnokiQA两分割，核对train19594发布位置、dev/test文章重叠、test285源文章七生成器的精确配对、rule开发58k句与测试集的源隔离、原始预测/阈值/随机种子。现网络限制未完成，未制造模拟数据来冒充。

**可用于综述的定位：** ENOKI以回答字符锚定的递进OpenIE事实串联claim核验和span投影，在HalluEntity及MuSHROOM/PsiloQA的指定指标上强，但RAGTruth span和多个句级集有外部方法领先；其“非蕴涵=幻觉”、自动教师标签与包含型Span Coverage F1决定了成绩的解释范围。建议和I004的Yes正类F1、I008的NON-FACTUAL正类F1、C12的字符跨度F1并列讲清评价对象和分母。
