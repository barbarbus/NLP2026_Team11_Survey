# I080 Joint Evaluation of Answer and Reasoning Consistency for Hallucination Detection in Large Reasoning Models

## 来源、版本与实际完成范围

Changyue Wang、Weihang Su、Qingyao Ai、Yiqun Liu，采用本地arXiv:2506.04832v2（2025-11-15），20页。原文：https://arxiv.org/abs/2506.04832 。实质正文1–10页、附录13–20页已全部读完，10–13页参考文献定位；渲染并目视7/9/18页主表、消融、权重及提取器分析。

官方 https://github.com/bebr2/RACE ，固定commit `6e9daba1ed87265bd264c5c045fecacfbaaa92fe`，保存6885137字节仓库ZIP、带行号源码、AST及资源清单。归档内5个输出文件是LFS指针，不把指针当数据；本次另取得并逐一核对指针SHA256/大小的4个实际JSON：judge 315983字节，main result 59752018字节，summary 3829887字节，summary samples 15804023字节。5采样的原始长输出约309.6MB未下载，其压缩CoT已核查。

源码阅读覆盖RACE.py评分、生成/提取/main/eval管线、训练数据与SFT、提示和运行脚本；未运行下载代码或加载模型。`sources/audit_race.py`独立解析输入/训练/发布输出，检验对齐/计数/精确问题重合，复算表格、长度诊断AUROC和公式反例；`fetch_race_lfs.py`及`inspect_race_resources.py`保存资源证据。详见`qa/I080_official/`。未做完整GPU推断、NLI/NER或RACE AUROC复现。

## 1. 先澄清评价目标：使用推理链，不等于给推理链真值打分

RACE认为只看答案采样一致性会漏掉不同错误推理殊途同归的情况，因此联合考察推理、答案及二者关系。主回答greedy，另采5条高温输出，针对主回答给一个连续风险分数。

但第4.1节明确最终判定对象是**主答案A_main是否有事实错误**；金标裁判也比较question、reference和answer，未给全部推理步骤单独标真伪。因此主AUROC证明的是“推理链信号能否改善最终答案错误排序”，不能直接证明“最终答案正确而推理错误”的独立检测率，更不等于错误推理定位/完整过程监督。

这与I077的局部解释主张验证、I093的可答性、I078内部更新特征不同。综述应分列：信号输入覆盖推理链，金标对象仍是最终答案。论文的“fine-grained”主要指多类信号，不是已全面测量逐步事实准确性。

## 2. 访问条件与系统成本组成

目标生成器可以是黑盒，只需可见推理R及答案A；普通CoT模型用提示分开Thought/Answer；普通direct输出设R=A=O。主要LRMs为DS-R1蒸馏7B/8B/14B、Qwen3-14B、GLM-Z1-9B、QwQ-32B、DeepSeek-R1，后者走官方API；另有Qwen2.5-14B direct/CoT两设置。

整个检测系统还需要8B CoT extractor，访问其内部注意力和完整logit分布；还需DeBERTa NLI、MiniLM embeddings及spaCy NER。因此“黑盒”只修饰被评价生成器，不表示检测系统只需调用一个文本API。训练提取器也用了合成监督：无目标任务新微调/无外部检索，不等于无训练或零额外模型成本。

发布提取器地址：https://huggingface.co/bebr2/RACE-CoT-Extractor-Llama-8B 。本次保存来源与使用路径，没有下载多GB权重，更没有对模型行为作未执行的复现声明。

## 3. 推理提取器：保留错误也可以叫“忠实”（第4–5页，附录A）

目标C=f(Q,A,R)，提取支撑**模型自己最终答案**的最简推理。训练池从2WikiMultihopQA的12576题出发，DS-Distill-Qwen7B生成R/A，Qwen2.5-32B生成6条压缩候选。详细过滤为：用Q+C再答得到A_i，保留与原模型A_R一致者；取最短一半，再选步骤最少者；每步相对原R的NLI entailment都>.9才保留。

主文提到GPT-4o只是可选强模型示例，实际实验是Qwen2.5-32B。主文“correct answer A”也容易被误读成参考gold；附录明确比较的是A_R。该过滤保证的是复述原推理/答案的行为一致性，不校验原推理的世界事实。提示明确要求原推理有错也忠实保留，不能把NLI高蕴含当“事实已验证”。

发布训练JSON有6142条互异问题，包含question/think/final_answer/sum，sum均为非空列表；训练read_data明确只返回前2000条，与主实验2000、2epoch吻合。合成池6142与实际训练2000须分开，不能报告成训练全池或每任务重新标注2000。

独立按NFKC+大小写+空白归一的问题串比较，整个6142池及前2000与发布NQ1800、SQuAD5928、Trivia7993、Hotpot保留6723均**无相同问题串**。这是有利的精确问题去重证据；不排除释义/实体/来源篇章重合、预训练污染，也未覆盖未保留的Hotpot682题，不能扩大为完全无数据泄漏证明。

## 4. 四项分数的含义、方向与单位

**S_CC，推理间一致性。** 主C每步与每条sample C比较NLI contradiction概率，先对sample平均，再按主答案对该step的代理模型attention均值加权。权重跨头/层平均、对答案token和step token取均值，再归一和为1。高分表示主推理更多被样本反驳，非直接被外部证据推翻。

**S_AA，答案不确定性。** 按SINdex使用问答embedding余弦聚类，以簇比例p乘簇内平均相似度，得到p'，计算`−Σp'log p'`。论文将其解释为更细的语义熵，实际实现/概率口径有重要差异，见下节。

**S_CA，推理—答案alignment。** 以主C和Q为上下文，在提取器上teacher-force各sample答案，逐位置计算**整个词表分布的Shannon entropy**，先长度归一再对sample平均。它不是sample答案的负对数似然；当前token虽用于后续前缀，当前步的entropy不使用该token是否被高概率预测。高分表示代理下一词分布更分散。

**S_Coh，内部coherence。** 从主原推理R与压缩C抽NER实体，计算`|E_R−E_C|/|E_R|`。高分是更多原实体被摘要删掉；原实体空时公开代码返0。仅以大小写和去开头the粗略归一，实体别名/同指仍可能被误判。它测压缩遗漏，不是形式逻辑矛盾或事实真伪。

最终相加四项，高分为风险高。主文说最后一项主要为LRM设计，公开calculate_race_score没有模型类型开关，对所有传入R/C都计算，正值就加。ordinary direct也有R=A的摘要实体差异，不能不加说明就假设代码自动关掉该项。

## 5. 信息论动机成立，四个操作量却不是联合熵的等价估计

恒等式 `H(R,A|Q)=H(R|Q)+H(A|Q)−I(R;A|Q)` 本身正确，提取后可考虑C/A。但NLI contradiction并不是H(C|Q)的统计一致估计，entity omission也不是熵分解项。最关键，S_CA是代理条件token entropy的正值，并非负互信息。

若理想化把前三项分别当H(C)、H(A)、H(A|C)，它们相加等于H(C,A)+H(A)，比目标联合熵额外加了H(A)。正确展开负互信息需要H(A|C)−H(A)，不是只加H(A|C)。实际proxy更复杂，更不能以恒等式证明等权和精确估计joint entropy。

独立例子：预测分布[.999,.001]，entropy仅.007907 nats；若被teacher-force的答案偏偏是概率.001的token，NLL为6.907755，明显不兼容却entropy很低。对只有一个token的两个不同答案，在相同前缀处该entropy完全相同。故低S_CA不等于主推理真的蕴含每个答案。

等权数值也不是等贡献：S_CC、S_Coh大致0–1，S_AA和S_CA为自然对数统计、范围随聚类/词表与分布变化。换对数底或模型温度会改变相对权重及排序。文章附录承认量纲差异，但又从较大最优系数推断“更重要”，需谨慎；系数大小不是独立机制贡献。

## 6. SINdex源码：去重、包含主答案与未归一的p'

`calculate_sindex`使用主答案+5个sample，先去首尾空白、空串替成空格，再在clustering_algorithm执行`sorted(set(sequences))`。随后簇频率分母是**不同字符串数**，不是6次采样次数；还把主答案加入了论文文字强调的sample答案空间。

独立反例：6次输出A,A,A,A,A,B，经验簇熵H(5/6,1/6)=.450561；去重后A/B各占1/2，得到.693147。它会丢掉多数票强度；“重复样本频率估计生成概率”的解释不再成立。该机制与I091/I082已讨论的采样频率/唯一答案问题相连。

p'_l=p_l×簇内平均余弦后没有重新归一。单簇、p=1、平均相似.8时，标准簇熵应0，公开公式却−.8ln.8=.178515，Σp'=.8。可作为结合分散度的启发式分数，但不是归一概率分布的Shannon entropy。singleton簇的相似度代码补1，避免分母零；论文双重求和/组合数的成对计数约定应以实现的unordered combinations为准。

聚类为按排序后的字符串逐一分给首个满足平均距离阈值的已有簇，不是全局最优或严格等价关系。问题文本也被拼到embedding前，长输出truncation会影响聚类；不同的措辞、长度和排序可以改变簇结构。未重跑embedding，未量化这些因素在作者结果中的份额。

## 7. 实际数据、过滤、金标和发布覆盖率

附录名义池Trivia7993、NQ EfficientQA1800、Hotpot7405闭卷；SQuAD answerable5928提供context做阅读理解。发布输入前三者中NQ/SQuAD/Trivia全量数目已独立核对；SQuAD的context已拼在question字段，不能与I076默认无context的SQuAD直接横比分数。

输出最长2048token，greedy主回答；sample5条、temperature1、top-p .95。缺`</think>`的主回答被过滤；这种因长度未完成/格式失败的输出本身与可靠性相关，不能从保留集AUROC直接推总体风险。不同模型若保留率不同，其条件测试人群也不同。

本次取得的Qwen3/Hotpot主回答、judge、主摘要、sample摘要均6723条，问题串主/摘要/sample摘要按位置全部一致、主问题互异、主回答全非空且均有closing think。相对名义7405题保留90.7900%，差682题；没有原始全部未过滤记录，不把每条缺失都归因为特定截断原因。

33615个sample摘要槽位均每题5个，其中1947个为空（约5.79%），主摘要均非空。空sample C的原因可能包括空最终答案/解析失败，未下载309.6MB原sample输出，尚不能逐条归因；不把“每题有5个槽位”当5条全部成功、可比较的推理。

裁判Qwen2.5-32B在question/reference/answer上比较选项概率：A语义正确，B相关但错误，C无关/无有效回答；非A统称hallucination。因此金标还合并格式、无效回答等。发布llm标签0=3193、1=3530，1为幻觉，错误基率约52.5%；未将拒答独立成类。

judge还含zj字段，0=2552、1=4171，与llm一致79.7858%；README未解释zj，不把它自动称“人工金标”或EM。judge自身无问题/ID，长度与邻接文件一致仍不能独立证明标签逐条语义无错。论文称manual labels证明裁判可靠，但本地附录未给足以复算全部裁判准确率的人工混淆矩阵/一致性产物；也不能把下节的提取器人工评价当裁判人工准确率。

## 8. 发布缓存上的独立长度诊断：提出混杂问题，不替代复现

以公开llm=1为阳性、固定“越长风险越高”，标准库rank AUROC（含tie半分）得到主推理**字符长度**.697505、最终答案字符长度.503977。代码对完美/反向/全tie的小例做基本校验；未用真值选择方向。

这是在同一发布保留队列上的描述性诊断，没有独立训练/测试，也未运行RACE；不能和论文78.41直接当严格配对显著性比较，更不能说RACE效果全来自长度。它提供可检验问题：原推理长、实体多、提取删掉多与答错相关，S_Coh及其他信号可能部分捕捉难题/过度思考。应做长度匹配、增量AUROC、按难度分层及配对CI。

## 9. 主表完整比较与例外（第7页表1）

4数据×9设置共36条件，RACE胜过该行最强已有baseline **34项**；7个LRM×4任务中胜27/28。RACE比raw在36项均高。独立等权宏AUROC=80.1053（百分数尺度），对逐条件最佳baseline平均高2.66194个百分点；这不是合并实例AUROC，也非显著性证明。

例外：QwQ/SQuAD RACE77.40<Semantic Entropy80.33；Qwen2.5 direct/SQuAD85.02<SE85.71、SINdex85.69。不能写“在LRM始终胜所有baseline”。Hotpot/Qwen3为78.41对SINdex75.80；DeepSeek-R1无logits，LNPE/Ptrue/概率SE为空，不把缺失填0比较。

本篇同一数据源也可能因生成器过滤产生不同实际测试分母。没有预测分数缓存、多种子或置信区间，数值接近的优劣不能自动写显著。普通CoT与direct不是只换检测器，生成方式、输出和错误分布也变化，不能把两列AUROC差当推理本身提高事实正确率。

## 10. 消融、权重、提取器评价和训练量

**模块消融，表3。** Hotpot五个模型删除某项通常降低AUROC，S_CC通常贡献大，attention weighting相对均匀权重改善约.2–.55点。但DS14的only S_CC=79.81，略高完整79.73，反驳“每个单项均低于联合”的绝对说法。删某项的平均效益与独立必要性不同，相关信号可能有冗余。

**RACE+，表4。** 前20%样本grid search，后80%test，权重在[0,1]步长.05搜索再归一。它引入目标标签监督，不与固定等权直接作为相同无目标调参预算。表4基线数也与主表略异，应优先做同划分内差值，不能把优化后值减主表值。当最优系数四舍五入和为1.01左右属报告精度，不自行重构准确权重。

**训练vs原模型，表6。** 提取平均84.57–100.49token，对原333.72–418.22减少约74.4%–76.3%；AUROC提升.29/.25/1.01/.50/5.68点，QwQ的5.68不能一概叫slight。短很多说明压缩与成本收益，不证明被删事实都无关。

**标注量，表7。** 100/500/1000/2000/4000条训练，对应79.13/79.46/79.84/79.73/79.62；100→1000仅+.71点，之后不是单调。文章“1000前显著增加”缺少误差条；“1000最优”只在此模型任务的探索表，不建立普适样本复杂度。

**提取忠实性。** 人工看250条、1条不忠实，报告99.6%，覆盖DS7B/8B与NQ/Hotpot。该定义是忠实原R/A、保持核心而非事实真；原推理错误被忠实复述也计好。未给完整多标者一致性、具体样本列表及按模型分层CI。还可能有词义改写/遗漏错误被人工标准忽略，后续宜双盲对照原文。

**采样和阈值。** NQ曲线约11 samples达较高区间，并非样本无限增必涨；主用5降低预算。Hotpot DS8B cluster阈值.9→.95：SINdex74.98→72.79、RACE78.56→78.16，支持该范围内对阈值相对不敏感，不证明全部任务无需选择。

**plug-and-play。** 推理模块加SEU/SCG多数提高；表9 QwQ的SEU原值73.28与表1的76.25不一致，不能按有利的较低baseline夸大收益。该表也未提供所有新组合成本和显著性。

## 11. 效率：论文并行测量与公开串行代码分开

DS8B/NQ随机100问、单80GB GPU，表2greedy30.91秒，main+sample批生成43.28秒，RACE提取2.10秒、评分最慢并行项.82秒，共46.20秒，较greedy增加49.47%；SINdex43.30秒，RACE多2.90秒；SRR47.68秒。

“只多约49%”依赖生成批处理与组件并行、特定模型/长度/硬件。公开README明确当前实现不含batch inference优化，batch_calculate_race是Python逐例循环，calculate_cross_uncertainty再逐sample调用；不能期待直接运行公开脚本就重现论文延迟。检测还需多模型常驻、代理完整attention，内存与部署资源也要计。

提取器训练数据生成、6候选、验证、NLI过滤和8B SFT是离线成本，表2不含。不能只比较原推理SRR与RACE在线分数时长就断言系统总预算更低；也不能把在更大模型部署中“相对可接受”外推到8B单卡边缘场景。

## 12. 公开管线的复现问题和故障默认值

模型加载异常时embedding可退化为384维全1向量，NLI缺失则S_CC返回5，代理/空推理失败可返回10，NER缺失则S_Coh=0。程序可能继续输出看似正常的连续分数，但已不再是论文四项有效信号；需显式记录各项有效性并停止无效评价，不能把常量默认值当真实高风险证据。

attention权重路径使用的query切片与entropy的预测位置对齐相同，query包含第一个answer之前的位置并漏最后answer位置；step key的think_start也−1，最后step还拼上Answer分隔符。对“从全部答案token到纯step token的均值attention”解释有索引差异，实际影响尚未跑张量核查。

main/summary/sample按数组位置合并，当前发布摘要问题串零错位是正面核查；eval也只按位置把score配judge，不验证ID。将来新增过滤或重排时应以键校验，不能只确保等长。

`cot_extraction.py`在main中对未初始化的局部sample_dataset执行`+=`；输出写到output_dir根目录，而后续main按dataset/model子目录找；run.sh传裸输出文件名，main里的`os.makedirs(os.path.dirname(...))`得到空串存在报错路径。训练shell调用不存在的train.py而归档为sft_train.py，后者导入dataset而文件为sft_dataset.py。生成逻辑以model_name.endswith('b')判thinking，可能把普通模型名字误分支，sample direct分支又只识别chat而非direct。均为静态可见问题，不代表作者原内部脚本一定如此。

因此本次不运行GPU去“验证”一个明显需对齐的包，也不修改归档掩盖差异。必要修复可另存patch并在统一数据/模型版本下重跑；当前无RACE scores缓存，无法只靠发布文本重算78.41 AUROC。

## 13. 研究问题及得到的实质答案

**Q1：能否验证答案正确但推理错误？** 现有主金标不能直接回答。应人工标原子推理事实/逻辑关系与最终答案，形成四象限（答对/错×推理对/错），特别报告答对但推理错上的检测率，避免只由final-answer标签支持更强过程主张。

**Q2：提取会不会美化或删掉关键错误？** 250例忠实性只提供有限保障。保持错误的prompt和NLI过滤是正面设计，但仍需对原R/C的错误保留率、冗余错误删除、错误改写、主样本不同程度压缩作盲评。与I077相连，后见答案条件下的“支撑链”也可能只是合理化，不保证忠实原计算。

**Q3：四项是否能保持信息论解释？** 当前只能称受信息论启发的heuristic ensemble。频率去重、p'未归一、条件entropy替负MI都有独立反例；应比较频率保留版、归一版、NLL/entailment alignment，并验证改法的排序和成本，而不是仅换术语。

**Q4：entity omission代表真实逻辑问题吗？** 真实有用探索可有4个实体、摘要留1个，得.75；错误抽象推理若NER无实体则得0。应控制原/摘要长度和实体数，增加逻辑步骤标注；缓存中推理长度AUROC .6975表明这是值得做的对照，不证明任一具体模块无效。

**Q5：发布资源足够复现吗？** 已取得四个实际LFS JSON并校验，各6723、对齐良好；三个输入数与文中吻合、训练精确问题重合0，这是可复用证据。仍缺原sample长输出、有效score缓存、完整裁判管线/人工标注、失败样本及优化实现，不能宣称端到端复现完成。

## 14. 可用于综述的论点与证据锚点

第4–6页：推理抽取与四维评分；第7页表1：34/36领先、SQuAD例外；第8页表2：在线时延与批处理条件；第9页表3–4：联合信号及目标标签调权；第14–16页：提取器过滤/判分协议/忠实性；第18页：压缩、采样/训练消融与插拔组合；第20页：答案多数一致但生日理由变化的例子。

建议英文表述：*RACE uses distilled reasoning traces and answer consistency to improve the ranking of final-answer errors. The framework adds useful process-related signals, but its main evaluation does not independently label reasoning correctness, and its information-theoretic interpretation, filtering coverage and auxiliary-model cost require qualification.*

与I077共同支持“最终答案一致不足以覆盖错误解释”；与I091/I082/I088共同强调一致性不是事实真值；与I076/I078共同要求区分检测预测性、机制解释、源码版本及监督预算。当前完成全文附录阅读、固定源码核查、发布资源验证和独立诊断，未执行GPU模型、重标全数据或重现主AUROC。
