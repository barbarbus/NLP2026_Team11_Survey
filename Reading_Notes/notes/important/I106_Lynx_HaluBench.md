# I106 Lynx: An Open Source Hallucination Evaluation Model

## 来源、版本与实际核查范围

Selvan Sunitha Ravi、Bartosz Mielczarek、Anand Kannappan、Douwe Kiela、Rebecca Qian，2024。原文 https://arxiv.org/abs/2407.08488 ，本库13页为**v2，2024-07-22**。正文1–8页实质内容、附录A/B第11–13页全部读完，8–10页文献定位；目视第3/7/13页，确认首图、主结果与追加训练/格式表。以下数字均明确区分论文、当前公开数据和历史预测缓存。

原仓库 https://github.com/patronus-ai/Lynx-hallucination-detection 固定提交`241fc162cf5e76a01138128a97b34bdb2b343bee`，ZIP SHA256 `a796660ab5f85c9efe538fc9d91f4c1f9a6bbfb2a5b090936088cc033776881b`。已读两份推理Python、70B/8B训练YAML、四份推理YAML及mcli/vLLM说明，没有运行完整推理/训练或上传结果。独立审计仅隔离执行两个纯正则解析辅助函数，输入为人工构造字符串；其余为数据读取、静态接口及算术检查。

HaluBench全量原作者数据 https://huggingface.co/datasets/PatronusAI/HaluBench ，固定`5966a87929f51c204ab3cbef986b449495cc97b6`，Parquet7512526字节，SHA256 `c7e9cf966085ffae88d2947744418a05a26ea94380c35c238b9fc12ecb874cdc`，存`qa/I106_data/`。70B原作者model card/metadata已存；8B名称以数据卡实际链接`PatronusAI/Llama-3-Patronus-Lynx-8B-Instruct`核查，旧猜测短名401不能解释为所有8B资源私有。未下载巨大权重或调用GPU。

另发现并固定下载原作者6域Lynx-70B预测缓存、GPT-4o的DROP/CovidQA缓存、后续`lynx-train-v0.1/v0.2/v0.4`数据；各commit/hash在`qa/I106_releases/provenance.json`，不与论文原2400训练例混认。独立脚本`audit_lynx.py`、`audit_lynx_releases.py`及两个fetch脚本已保存；结果分别为`qa/I106_lynx_audit.json`、`qa/I106_released_prediction_audit.json`。Parquet读取依赖pyarrow，本机只装在作业目录`.reading_deps`，不改系统环境。没有把离线缓存复算写成重新生成模型实验。

## 1. 测量对象：来源支持，不是世界真伪

输入为question、context/document、candidate answer，输出解释REASONING和二元SCORE PASS/FAIL。所谓reference-free指推理时不需要人工gold answer，**仍需要指定来源文档**；训练却使用gold答案/标签及教师解释，不是无监督或无外部监督方法。

第3.1节明确：不评检索context与query是否相关；只要回答与context一致，即使回答问题不正确/检索不相关，也算faithful。世界知识与来源冲突时，按来源判。因而这是RAG生成的来源一致性评估部件，不是完整RAG质量、客观事实核查、检索质量或回答帮助性指标。原文intrinsic/extrinsic术语分界与其它综述不一定相同，写作时用具体参照解释，避免只贴词。

**定义内部张力：** 首图将“两个例子都是植物”判FAIL，理由是问题期望genus层级，plants太宽。文档实际上支持它们都是植物，这更像I108的specificity/回答任务不充分；与“错误回答但来源支持也算faithful”的第3.1节不完全一致。短答案在question中补全语义时，问题当然重要；但明确完整句的来源支持与回答粒度应该拆开，不应用单个示例证明任意任务正确性都属于faithfulness。后续公开v0.4训练提示还明确支持“irrelevant to question但被context支持”为FAITHFUL，进一步说明需锁定rubric版本。

可构造文档Alice赢2020、Bob赢2021，问2021赢家，答完整句“Alice赢2020”：来源支持成立，但未回答目标。一个统一PASS/FAIL若未明确评哪个，会把评估器分歧误叫推理能力差。与I044 ARES/I057 RAGAs的多维拆分相连：faithfulness、answer relevance、context relevance应分报。

## 2. 数据构造：领域真实，错误多为合成

HaluBench含六来源：HaluEval QA10000，RAGTruth QA900，以及FinanceBench/DROP/CovidQA/PubMedQA各1000。四个原QA集本来有gold答案，作者各选500原例作PASS，另500经GPT-4o在temperature0做细微语义扰动作FAIL；原/扰动不是必然来自同一组500配对题。第5页称additionally sampled500，不能自动把1000样本当500对反事实。

扰动器看question、gold answer、evidence，要求看似合理但与证据不符，输出new_answer/change_made。公式直接给标签1−y，隐含**每个扰动确实翻转真值且原答案确实faithful**；模型生成过程本身不保证。需要独立人核，尤其数学、量纲、问句粒度、合法重述及原gold不足的情形。

“real-world domains”描述金融/医学来源，不表示错误是自然生产流量、自然发生率或真实用户分布。原文第5页说人工标全部FinanceBench in HaluEval，应结合上下文理解为本文FinanceBench部分，而不是HaluEval原本有金融子集；该措辞本身不清。训练与测试共享扰动生成器/格式，域多样性不自动等于错误机制独立。

表1标题为hallucination examples，但CovidQA例问何种test，来源明确提rRT-PCR、回答也rRT-PCR。全量发布中对应`covidqa-1308`为**PASS**。这是论文示例标题与实际样本标签不符，不是目前发现这条数据被误标FAIL；不能因表格标题去改发布标签。医疗内容这里只作历史语料来源支持核对，不作现实诊疗建议。

## 3. 全量基准审计：14900条、聚类与类比例

本次独立读取14900行，字段`id,passage,question,answer,label,source_ds`，无重复ID。四个专业/推理子集各500PASS/500FAIL；HaluEval为4990PASS/5010FAIL；RAGTruth为740PASS/160FAIL。总PASS7730、FAIL7170，恒PASS accuracy=**51.8792%**。论文15k可作近似，但“所有子集平衡”不成立。

RAGTruth恒PASS即**82.2222%**，比Lynx70表内80.2%还高；说明普通accuracy在该子集受类比例影响很大。这不证明模型不会检错，因为其召回/特异度权衡仍未知，应另报balanced accuracy、错误类P/R和混淆矩阵。不能把其它四域的均衡设计套到RAGTruth。

独立原文数：DROP486、PubMed1000、Finance761、RAGTruth150、HaluEval9936、Covid86；原文＋问题组数分别987/1000/1000/150/10000/730。RAGTruth900例实为150个问题的多模型回答；Covid1000例共享86段来源。统计区间和划分必须按来源/问题聚类，不能一律把所有行当独立。跨集合来源级重叠又与完全相同问答三元组重叠不同。

精确(passage,question,answer)重复额外12行（DROP5、RAGTruth7），未发现同三元组相反标签；只是精确重复检查，不等于语义重写/事实重叠不存在。没有模型推理分数时不能由gold标签恢复整个指标排序。

## 4. 人工质控的0.94实际表示什么

四个合成子集各随机50例，共200，人工检查原/扰动答案和理由。表2agreement为DROP.92、Finance.90、Covid.96、PubMed.96；在每域50例下分别46/45/48/48，总187/200=**.935**，四舍五入约.94。

这是作者称“与人工标注一致”的比例，原文未给足多人独立原始标签、Kappa/Alpha或标注者人数/资质/付费细节。**不能把.94写成Cohen κ=.94或双人一致性94%**。针对200子集的检查不能证明14900每条正确，金融全量人工复核应和其余只抽样质控分开。未取得完整原始200人核记录，不伪造重算κ或修正标签。

扰动器提供change_made给教师解释，会增加解释针对预设错误的概率，但也可能使教师围绕预设标签合理化；不是独立盲审证据。后续需要不知道生成目标的人工核验，特别记录“扰动未改变真值”“原答案已错”“粒度/格式导致分歧”。

## 5. Lynx训练：教师蒸馏与机制证据边界

原文训练2400、验证800，训练来自RAGTruth/DROP/Covid/PubMed四任务各600，其中300扰动；金融与HaluEval未列入该训练分布。用GPT-4o生成reasoning：负例额外给gold、change_made并要求解释为什么不faithful，正例要求解释为什么faithful；将解释+标签作assistant监督，微调Llama3-Instruct-8B/70B。

推理只见question/context/answer，不给gold或change_made，所以不是直接测试时泄漏gold。但训练解释包含教师的privileged information，与单纯模型从相同输入自由推理的能力不同。原文没有充分CoT移除/label-only、教师解释打乱/纠错及数据规模对照；因此不能把所有增益因果归于“reasoning chains”而非任务适配、输出格式或数据分布。

正文训练3epoch、LR5e−7、batch256，70B用32H100；附录LionW(.9,.95)、cosine100warmup、norm clip1、FSDP FULL_SHARD/activation checkpoint，推理70B为8H100/vLLM，8B为accelerate，贪心、max_new_tokens600。不能把8B“fraction of cost”当已测的具体端到端美元/延迟比例；没有完整实测成本表。

**配置差异：** 公开70B/8B YAML的global_train_batch_size都是32，而正文256；max_seq_len8000、seed17。若2400例×3epoch、不额外采样/packing，batch256约30更新，batch32为225，warmup100个batch-step含义大不相同。它不证明实际训练错，因为可能有未公开累积/采样配置，但说明模板不能直接等同历史run。模型/数据路径多为HF_USER占位，也没有原2400/800清单与run锁定文件。

## 6. 主表：优势范围、聚合与文字不符

v2表3Lynx70六域accuracy依次88.4/80.2/81.4/86.4/97.5/90.4，总87.4；GPT4o为87.9/84.3/85.3/84.3/95.0/82.1，总86.5。逐域差Lynx−GPT4o为**+0.5/−4.1/−3.9/+2.1/+2.5/+8.3个百分点**。原文说all tasks最高不受表格支持：RAGTruth和FinanceBench明确落后，不能只引用总体领先。

Lynx70总87.4、Llama70 80.1，差**7.3点**，不是正文7.8%；对GPT3.5表内58.7差**28.7点**，不是正文27.6。不要擅自将这些说成relative percent gains；按所印总分直接相减就是百分点。PubMed8.3也为个百分点，不是相对8.3%。

独立按六域宏平均：Lynx70 87.3833→87.4、GPT4o86.4833→86.5，和原表相容；但ClaudeSonnet六域宏**82.5833**而Overall78.8，Haiku宏**78.0667**而Overall69.0，RAGAs宏68.0333而66.9；按发布行数10000/900/1000×4加权也分别83.7644/72.5242/69.5315，不相符。GPT4Turbo宏85.35 vs85.0、GPT3.5宏58.4167 vs58.7也超通常单纯一位数舍入误差。

因此不能假定每行Overall同一公式。Lynx70按全量行数加权约88.0456，若写“全部14900行有87.4%正确”也不严谨；87.4看起来是六任务等权宏平均。需原逐例评分与版本/有效样本解释，不因表存在矛盾就否定全部子集结果。

RAGAs用faithfulness阈值.5，低于才判FAIL；这是人工固定阈值策略，不是其分数天然最优决策点。不同模型有额外JSON适配训练，而基线同prompt零样本不能保证格式错误率相同。本文没有比较ARES含PPI的系统级统计目标，也不能据此推断其实际生产适用性普遍更差。

## 7. 预测缓存复算：能对齐的真复算，不能对齐的停止合并

Lynx6域缓存共14900条响应，含custom_id、模型content、usage等，未包含完整推理输入/gold。公开Lynx输出大量SCORE为未加引号PASS/FAIL，REASONING常为单引号列表，**不是严格合法JSON**。独立使用与v1相近的两阶段正则（先双引号、再未引号）抽SCORE，并保留ERROR，不让格式失败悄悄消失。

**DROP：** 1000个唯一UUID可与基准完全对应；复算FAIL→FAIL427、FAIL→PASS73、PASS→PASS437、PASS→FAIL63，accuracy**86.4%**，重建论文子集分数。GPT4o同1000UUID为440/60/403/97，accuracy**84.3%**，同样吻合。已按同题配对：两者都正确790、都错83、仅Lynx正确74、仅GPT4o正确53，discordant127，精确双侧McNemar p=**.075531**。这只说明该缓存与此检验条件下+2.1点未达常用.05阈值，不证明二者相同，也不替代题/文档聚类与多重比较分析。

**PubMedQA：** 1000唯一ID对应，负例438正确/62错放，正例466正确/34误拒，accuracy**90.4%**吻合。**FinanceBench：** 同1000唯一ID，负443正确/55错放/2解析失败，正356正确/144误拒，accuracy**79.9%**，与论文81.4不同。基准金融标签经过人工修订、缓存/数据可能版本不同；当前证据不足以确定哪批材料用于论文，不把79.9擅自替换成“真正论文成绩”。

**HaluEval：** 缓存10000响应有**2516条重复custom_id额外记录**，当前基准ID却唯一。仅把`halueval_`改`halueval-`会将同题不同候选答案混合，产生约50%的伪分数；已在脚本明确标为无效候选join诊断，**不作为复现结果**。检查例：同一ID缓存解释批评“Father of Philadelphia Folk Music”，当前基准候选却为“Grandfather...”，说明ID不是完整候选身份。要补原输入/答案内容或复合ID后才能计分。

**CovidQA：** 两个模型缓存各1000条、各有265条重复ID额外记录；发布基准区分`covidqa-1806`与`covidqa-1806-perturbed`，缓存只留1806等，ID不含候选极性。把它强行连到原例会错配。GPT4o缓存自己含label，可直接复算**95.0%**，不依赖错误ID合并；Lynx缓存无gold，在未证明与GPT序列/极性完全配对前不抄标签，暂不报97.5复现。

**RAGTruth：** 缓存custom_id0..899是局部索引，当前基准用原样本ID如11904；没有原索引映射，不把行序默认当对应关系。不能由现有缓存直接重构80.2混淆矩阵。所有资源均已保留，缺口具体到候选身份，不笼统写“作者未开源输出”。

## 8. 后续训练集的重叠：必须写清版本归属

官方HF组织还公开Dec2024的lynx-train-v0.1（5540train/1147validation）、v0.2（4640/1047）、v0.4（5287train）。它们样本量、prompt的HIGHLIGHTS字段及发布日期与Jul2024论文2400/800不同，**不是已确定的原论文训练集**。

独立将prompt中的question/document或context/answer全部提取，归一空白后比对三元组：v0.1/v0.2各有**27条训练行**与当前HaluBench完全相同、各27验证行相同；两版各有54个训练–验证共同唯一三元组。v0.4有**72条训练行**与HaluBench三元组重合。来源文档重叠更多，分别train889/889/362行、v0.1/v0.2验证316行。报告的是训练行数，不能混成不同测试题/不同文档数；样例行号与test ID已存。

这些发现说明**今天拿后续官方训练文件直接重训再在HaluBench测，不能声称严格独立测试**；并不足以指认论文原训练或公布权重一定见过相同测试例。应要求原run的数据manifest，必要时重建按文档/问题/候选三层隔离的训练集，并同时保留后续版本研究记录。不要把后续公开增加的数据视为原论文已做留域泛化的证据。

## 9. 源码接口与分母：可访问不等于一键历史复现

v1读取`messages,_id,LABEL`，HaluBench原发布是`passage,question,answer,id,label,source_ds`，需要明确适配；不能直接load原基准就运行。v1先创建model对象，但pipeline又传字符串model_name_or_path，可重复加载，分布式每进程device="cuda"未明确rank与已有model复用，不是已经实测的显存/性能故障。

v2 YAML传`--test_ds_path`，Python argparse只定义`--hf_ds_path`，原样命令会参数不匹配；提供的资源是需要修订配置的模板。v2按用户content未经chat模板token数<4000筛输入，随后才加chat格式，600/2000输出预算与8000上限需另核；它会删除长上下文，报告accuracy须连同保留比例，不能把删掉样本当全基准表现。没有统计本次实际删多少，因为未用对应tokenizer重跑。

v2生成未显式设do_sample=False，真实默认要看模型generation_config；不能由函数调用本身保证论文greedy。返回包含prompt的全序列，再用硬编码文本split后索引[1]取生成，模板不匹配就会IndexError；宜直接切去input token长度。还未显式add_generation_prompt，实际聊天模板如何处理需版本固定。

v2 SCORE只接受双引号，v1有未引号fallback。独立把官方缓存内容输入同规则检查：Lynx每域**全部被quoted-only规则判ERROR**，v1型fallback能恢复几乎所有（金融2条未解析）。这是确定的规则/缓存不兼容，不意味着论文使用v2得了0%；相反提示要锁定论文实际解析路径，不能复制任一新版代码就宣布论文复现失败。

纯regex不会验证JSON结构：小写pass提出来仍与PASS不等；单引号键无法提；同文本两SCORE选第一个而非最后结论。独立人工字符串测试已保存。推理结束token耗尽、格式失败、无法判定应单报，而非随意算事实错误或删除。程序有push_to_hub副作用，本次未运行主程序或上传任何结果。

## 10. 附加训练与格式适应的证据

附录B.3在看到RAGTruth较基座下降后加2k该域训练样本，RAGTruth80.2→85.8，Overall87.4→87.8（+.4点），其它域DROP86.4→85.3、Covid97.5→96.9、PubMed90.4→88.8下降。它显示任务混合权衡，而非“加训练样本所有指标更好”。追加选择是看过该测试域结果后做的开发决策，严格结论需另独立确认集；不等同数据内容已经泄漏。

Llama2-Chat13B baseline3.3%、finetuned77.8%，附录明确baseline难输出JSON而微调可解析。因此74.5点提升混合**格式遵从与语义决策**，不能全归推理能力跃升。构造100例90例语义正确但仅3例可解析的反例，exact-parse accuracy仍3%，说明两者必须分别报告；这是逻辑演示，不是恢复Llama2真实隐藏决策。

## 11. 已提出并做独立检查的研究问题

### A. 高分是否需要读懂来源？

全量答案字符长度作唯一“越长越像FAIL”分数、正确处理同长度并列，独立AUROC：HaluEval **.970115**、RAGTruth .729316，DROP .528160、Finance .518950、PubMed .488092、Covid .499970。HaluEval PASS平均13.69字符、FAIL66.19；极强长度关联提示基准可存在表面捷径。**这些是ranking AUROC，不是表3accuracy，不能直接声称长度模型97%accuracy打败Lynx88.4。** 也没证明LLM实际使用此捷径。

DROP更具体：500FAIL里**272个答案是Python列表literal**，500PASS中0；仅规则“literal list→FAIL，否则PASS”在全1000上accuracy/BA=**77.2%**。它是看过数据后的诊断，不是预注册留出模型，但确实无需文档事实推理即可获得相当高分。后续应控制答案格式/长度匹配、统一列表/字符串序列化，并检验自然回答迁移，避免让score主要测构造过程。

### B. 同一输入身份如何保证？

本次两个高重复ID缓存证明“ID能连上”不保证是同一candidate。最低manifest应包括source_id、question_id、candidate_id、context/answer哈希、模型版本、label版本。保存所有原始输入后才能处理候选变体、原标修订、对话/长文本截断。已完成重复/对齐和具体错配诊断；未凭推理解释的只言片语给全部错误映射补标签。

### C. 微调增益究竟来自理由、格式还是领域？

需要label-only与reasoning+label同数据、同训练步数、同解析支持；再做教师解释置换/错误解释对照、不同生成器与自然模型输出外测。本文未有这样的全因子消融，现有Llama2表与parser差异支持“至少需拆开”的研究动机，而不是已证明哪项贡献最多。

### D. 医学/金融高准确率能外推真实部署吗？

来源任务、人工gold证据、合成错误与50/50类比，不代表真实低基率/长文/未知检索失败场景。应报告误拒/漏检及代价、置信/拒绝覆盖、时间/语言外测和问题级区间；只做PASS/FAIL本身不产生校准概率。论文不评真实医学/金融决策效果，也没有数据证明生产安全性。

### E. 总分与“第一”如何有可复核含义？

本次宏/加权算术、真缓存子集混淆、DROP配对检验和常量基线表明，必须先确定标签/分母/解析，再讨论排名。模型总分.9点领先不是六域全面领先；部分行聚合不闭合，不能在综述排序榜中直接把它当统一尺度。更稳妥做法是按共同输入、共同输出政策、分域及成组统计报告，而不是只留一个最好总分。

## 12. 综述写法与剩余复现工作

可写：“Lynx通过GPT-4o生成的细微答案扰动及标签条件解释，微调Llama3裁判进行来源一致性判断。HaluBench覆盖六个QA来源；原表70B总体87.4、GPT4o86.5，但RAGTruth/Finance子集并不领先。全量数据与缓存审计还提示类不平衡、答案长度/列表格式捷径、候选ID和版本对齐、格式解析及后续训练重叠等元评估问题。”

不写：不需要任何证据；评客观世界真值；87.4%就是所有14900条micro正确率；每域第一；0.94是κ；Llama2能力从3.3变77.8而无格式影响；原论文已证实训练泄漏；长度AUROC等于准确率；源码/预测未公开；本次重跑70B模型或完整复现原表。

后续依次补原2400/800数据与run；修复输入适配/CLI、生成与解析路径并保留无效输出；获取HaluEval/Covid候选级映射和RAGTruth原索引；核对金融人标/缓存版本；修正整体聚合；自然错误与留生成器/留文档测试；报告聚类区间与代价。当前已读全部实质正文/附录、查模型/数据卡、核实两份推理与配置、遍历基准与后续训练数据、部分缓存复算及诊断；未进行GPU训练/推理，未消除原文与发布材料的全部缺口。
