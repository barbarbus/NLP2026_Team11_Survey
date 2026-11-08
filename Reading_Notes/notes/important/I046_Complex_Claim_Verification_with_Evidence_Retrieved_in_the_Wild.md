# I046 Complex Claim Verification with Evidence Retrieved in the Wild：真实检索的核心瓶颈是证据可得性而非最终分类器

## 来源、版本与核验范围

Jifan Chen、Grace Kim、Aniruddh Sriram、Greg Durrett、Eunsol Choi，*Complex Claim Verification with Evidence Retrieved in the Wild*，arXiv:2305.11859v2（2024-06-15）。本地PDF共19页，正文、限制、实验细节、完整人评说明、prompt与ChatGPT附录逐页阅读；目视核对PDF6–9表2–7、PDF14表8及PDF16表9。

作者[官方仓库](https://github.com/jifan-chen/Fact-checking-via-Raw-Evidence)当前main保存为`Hallucination_Evaluation_Library/code/I046_Fact_checking_via_Raw_Evidence_main.zip`（26,314字节），压缩包结构通过检查。静态审计问题生成、Bing检索、时间/站点过滤、BM25二阶段检索、摘要与DeBERTa分类脚本。官方Google Drive数据包在当前环境无法连接，未核对1200条原始记录、网页正文、模型摘要或预测，亦未调用已停用/变更的text-davinci-003与Bing API，因此不能声称复现表2–9。

## 任务为什么比常见“给定证据判真伪”更真实

传统事实核查数据常直接提供人工justification，或允许搜索到声明发布后的事实核查文章；分类器会读到别人已经综合好的结论。本文要求系统只能使用**声明发生时已经存在**、且不来自已知fact-checking站点的原始网页，模拟新声明刚出现时的核查。

完整链条为：复杂claim → 10个二元subquestions → 商业搜索引擎 → 网页抓取 → BM25段落/文档筛选 → 每文档claim-focused summary → 六级veracity分类。这个设计将“生成回答的幻觉评价”扩展为“核验信息从哪里来”的上游问题：若真实证据不可得，最终模型再强也只能拒绝、猜测或用参数知识补写。

研究对象是英语政治声明与PolitiFact六档标签，不是一般开放域生成。PolitiFact标签包含编辑判断和程度权衡，标签不完全等同原子命题的布尔真值；论文也因此把自动分类仅当代理，强调返回证据供人使用。

## 数据、切分与五阶段系统

CLAIM DECOMP含1200条复杂政治声明，train/dev/test为800/200/200。每条有六级标签（pants-on-fire、false、barely-true、half-true、mostly-true、true）、人工justification和既有人标subquestions。

### 1. Claim decomposition

用text-davinci-003和4个few-shot示例，以temperature .7反复采样，最多5次，直到收集10个不同的yes/no问题。问题既覆盖显式事实，也试图覆盖隐含因果与限定条件。源码只以exact string去重，并过滤包含`why/who/which/what/where/when/how`任一子串的问题；它不能合并语义重复，也可能误删单词内部含这些字符串的合法yes/no问题。生成问题多于gold平均3个，因此后续“predicted胜gold”混合了问题质量与查询预算，不是纯质量比较。

### 2. First-stage retrieval

每个subquestion向Bing请求结果，过滤已知fact-checking域名，并用claim日期限定网页时间。理论最多10问题×10文档，过滤去重后平均检索66.7页，成功抓取45.0页；约三分之一因paywall、PDF或反爬不可读。正文Figure2/Appendix表8称一阶段约45文档、70,245词，表1的“# words 1,561”更像每文档均值却表头未注明；45×1,561≈70,245，二者并非总词数冲突，但呈现口径容易误读。

时间约束并不等于真实“发布时已可见”：搜索引擎`freshness`、网页元数据和`htmldate`可能把更新时间当发布日期，旧URL内容也可能后改。源码默认把cutoff加1天，并在二阶段再次以页面时间过滤；需要保存当时网页快照与检索日志才能审计。

### 3. Second-stage retrieval

网页按30词窗口、stride15切片，BM25取top-10 spans，将每段扩展±150词，重叠段合并，再保留top-4文档。信息从约70,245词压至2,710词、7.7文档，摘要后约251词、4文档。此压缩约99.6%，大幅降低成本，也可能丢掉低词面重叠的反证、限定词或跨文档关系。

论文配置top-4文档，当前README命令与源码默认均为top-5；仓库默认与正式表配置不一致。`num=5`参数还与实际`topk_units/topk_docs`并存但用途不直观，复现必须显式传参而不能依赖默认值。

### 4. Claim-focused summarization

text-davinci-003分别摘要每个文档，要求1–2句、不作verdict、不复述文档不支持的claim信息。zero-shot与人工写4例的few-shot比较；后者对不相关文档输出“不相关”。逐文档而非全证据一次摘要，减少模型自己合成裁决，但仍会把参数知识掺入摘要。

当前源码调用temperature .75；摘要不是确定性步骤。论文没有给多次摘要的方差或固定completion ID。仓库默认`use_fewshot=1`，README示例却传`use_fewshot 0`，又与论文默认系统zero-shot-003不同，需以每张表的条件而非README命令为准。

### 5. Veracity classification

DeBERTa-large输入claim+summaries，做六分类。训练25 epochs、max length512、batch32，以dev MAE选最佳；运行5个seed后**选择dev最好的一次**报告test，而非报告5次均值/方差。这会产生模型选择乐观偏差，test点估计没有seed不确定性。claim+raw evidence可能因512截断，故summary的收益同时来自压缩与内容选择，不能只归因“生成摘要更有推理价值”。

## 严格检索使表面性能显著下降，揭示事后答案泄漏（PDF6）

表2测试集：

- 无时间/站点约束：Acc49.0、SoftAcc86.0、Macro-F1 48.5、MAE .68。
- 只排fact-check站：33.5/75.0/33.9/.95。
- 只限claim之前：33.5/72.0/38.0/.98。
- 同时限时且排fact-check：33.0/74.5/34.5/.99。
- Claim-only：25.5/68.0/27.5/1.12；人工justification oracle为57.5/93.0/57.8/.50。

MultiFC的15,379条claim中，82.7%至少检到一个本文排除站点，24.4%检索页来自fact-check站。无约束系统接近oracle，主要可能是搜到声明之后的综合性核查，而非从原始证据独立推理。故RAG事实核查研究若不做时间切分和来源去泄漏，会严重高估真实新声明能力。

严格系统相对claim-only绝对只增7.5 Acc、6.5 SoftAcc、7.0 Macro-F1并降.13 MAE；虽多数显著，却仍只有33%六分类准确。SoftAcc把相邻档位也算正确，74.5%看似很高但容忍一档误差；部署时必须并列exact、MAE和严重错误距离，不能单报SoftAcc。随机/恒定多数类及恒定中间档的SoftAcc基线未给，难判断74.5中多少来自六档有序标签本身。

## 阶段消融：subquestion有用，但“gold不如生成”不能按字面解释（PDF6–7）

默认系统（generated subQs→subQs BM25→zero-shot summary）为33.0 Acc、34.5 Macro-F1。把一阶段查询换为原claim降至24.5/18.0，甚至不如claim-only，说明复杂声明整体搜索难命中各个方面。用gold subquestions只有27.5/28.1；作者解释generated有10个而gold平均3个，实质说明**更大查询预算**可能胜少量gold问题，并未证明生成问题更正确。应把两者都限制为相同问题数、搜索调用与去重URL数。

二阶段用claim、gold subQs或human justification做BM25，Acc31.5/31.5/33.0，差异均不显著；±150词扩展可能使query精度不敏感，也可能因为最终样本200太小。oracle justification未明显胜，不代表它无信息，而是二阶段仅把它当检索query、不是输入分类器。

few-shot摘要Acc35.0、Macro-F136.2，略高于zero-shot33.0/34.5；raw-doc无摘要29.0/26.3，只有部分指标显著。由于raw长文本会被512截断，该消融不能分离“摘要事实选择”“长度压缩”和“生成改写”。应加extractive top-251-word、相同token预算和oracle evidence span三类基线。

## 商业搜索结果变化：URL不稳定但200条测试不足以证明性能稳定

同一query集相隔1周URL Jaccard .48，相隔2个月仅.30；Acc从33.0到33.5再29.5，Macro-F1 34.5→36.8→32.3，差异未显著。URL集合70%变化而指标未显著，可能说明功能冗余，也可能只是test N=200与best-seed噪声造成检验功效不足；“未显著”不能证明等价。

复现还受网页消失、内容更新、搜索排序与API退役影响。最合适的发布物应同时有冻结网页快照、URL/时间戳/抓取失败码、query和live-search track；固定语料评价可复现性，live track评价真实时效性。

## 人评一：few-shot降低单摘要幻觉，但claim级风险仍不低（PDF7–9）

从dev随机抽50 claims、每条4个document-summary，共200对；比较zero-shot-001、zero-shot-003、few-shot-003。标签为Faithful、Minor、Major、Completely Wrong，映射4/3/2/1后多数票；若三人全不同则取数值均值再就近映射。论文未清楚给每item标注人数，Fleiss κ=.30，说明严重度边界分歧明显。

表5：zero-shot-003为66.0% faithful、18.0% minor、16.0% major、0 wrong；few-shot-003为82.5/6.5/8.5/2.5。作者把Faithful+Minor称89%“good enough”，但若证据进入政治事实核查，11% major/wrong不能视为小问题；minor也可能在某些claim上改变关键数值/时间，类别定义依赖“整体印象”而非claim关键原子事实。

表7在claim级采用any-error聚合：50条中28全faithful、10至少minor、12至少major/wrong，即24% claims含严重摘要错误。单摘要89%可用不能直接转译为整套证据安全；四摘要和多claim的家族错误率会上升。应报每100 claims至少一严重错、错误原子数/总原子数、是否影响最终verdict和来源定位。

人评说明还存在内部错位：正文称faithfulness招17人、comprehensiveness 15人；Appendix C.2却说faithfulness资格测试31人后选15、comprehensiveness 28人后选17。未发布原始assignment时无法判断哪组数字正确，也无法复算κ和共识。

## 人评二：覆盖率提高可能来自幻觉补全（PDF8–9）

以161个gold subquestions测summary能否回答：zero-shot-003为47.8% answerable、22.4% partial、29.8% unanswerable；更忠实的few-shot反而为42.9/21.1/36.0。作者合理推断zero-shot看似覆盖更多，部分是它补写了文档没有的信息。

这是本文对幻觉评价最关键的测量警告：**comprehensiveness与faithfulness不可互相替代**。一个摘要可以通过虚构答案提高“可回答率”；另一个完全复制局部证据却遗漏关键反证。必须二维报告support correctness与claim coverage，并在两者均满足时才称可用于核查。

claim级表7：6 fully answerable、8 partially answerable、30 partially unanswerable、6 wholly unanswerable，所以36/50至少有一个问题完全无答案；只有14/50在“all questions answerable or partial”口径下可覆盖。此处把partial视为足以“fully addressed”的文字略宽松，应该另报严格全部answerable（仅6/50）和宽松无完全unanswerable（14/50）。14条宽松可覆盖中1条有严重摘要错，不等于其余13条最终结论一定正确。

## ChatGPT最终裁判反而被摘要拖累（PDF16、表9）

ChatGPT claim-only Acc32.0/Macro-F131.0/MAE1.16，加入summary后24.5/25.7/1.25；DeBERTa则25.5/27.5/1.12升至33.0/34.5/.99。作者推测ChatGPT过度依赖参数知识而没有利用摘要，但没有attention、反事实替换或证据冲突实验，属于解释假设。

ChatGPT先输出0–100分，再按训练集六类比例的percentile把分数映射成标签。这会强制预测边际接近训练标签分布，排序质量、数值校准与离散分类混在一起；也不是普通固定阈值zero-shot分类。需要直接六类prompt、固定阈值、训练比例quantile三种并列，以及证据置乱/相反证据测试。

## 当前官方源码的复现与安全审计

1. 仓库只有代码与Drive链接，没有固定网页语料、LLM completions、人工标注、五seed预测或环境lock；数据链接当前无法访问。
2. README把`generate_subquestions.py`写成与实际文件`generate_sub_questions.py`不同，摘要命令还有`pyhton python`拼写错误，不能直接复制运行。
3. 论文二阶段top-4，README/源码默认top-5；论文默认表用zero-shot，而源码默认few-shot、README示例又显式zero-shot。配置需逐表重建。
4. `evidence_retrieval.py`在无timestamp结果的终检分支仍检查`search_results_timestamp`，会错误报告非时间检索状态。
5. Bing检索器源码含一个硬编码订阅凭据（本笔记不记录具体值），同时也读环境变量；即便凭据已失效，公开仓库也应立即撤销、清理历史并只用环境变量。
6. 页面过滤仅做URL子串域名表，无法覆盖镜像、转载、短链或未列出的事实核查站；“Non-FC”是有限denylist，不是保证无事后核查内容。
7. 分类脚本提供单个seed运行命令；论文五seed择优需外部循环与选择逻辑，仓库未给自动汇总。代码指标含micro-F1（等同单标签accuracy）但论文不报。
8. 当前源码未见LICENSE；第三方可读不等同明确可再分发/修改，打包使用应注明来源而不擅自推定许可。

## 可进一步验证的研究问题

1. **时间有效证据审计：**对每页人工核对首次发布日期、最后修改、内容版本和claim cutoff；比较URL时间过滤与真实Wayback快照。
2. **查询预算匹配：**generated/gold/original claim在相同10 queries、相同返回页数和token成本下比较；评估subquestion factuality、去语境化与覆盖。
3. **coverage × faithfulness二维前沿：**每个gold subquestion标“检到支持/检到反证/仅相关/无证据”，每个summary claim标supported/contradicted/added；禁止把幻觉补全算覆盖。
4. **压缩受控实验：**raw evidence、extractive 251 tokens、abstractive 251 tokens、oracle spans同长度比较，分离截断、检索和生成贡献。
5. **错误传播图：**记录query遗漏、网页抓取失败、BM25丢失、摘要添加/删除、verdict误判；计算每阶段条件失败率及最终错误归因。
6. **选择性核查：**证据不足时输出“不可核查”而不是硬六分类；报告coverage-risk、严重误判与人工追加检索收益。
7. **live/frozen双赛道：**冻结2022语料用于可复现横比，实时搜索用于时效鲁棒性；以等价性界限而非“不显著”判断版本稳定。
8. **人机协作试验：**比较人工单独、系统单独、摘要+URL、摘要+原文四条件的准确率、时间、过度信任和纠错率，而不只问摘要是否看似有用。

## 对综述可使用的结论

本文最可靠的贡献是把现实事实核查中的证据时间泄漏与上游检索瓶颈量化：无约束Acc49.0降到严格时间+站点约束33.0，说明大量既有“web evidence”优势来自事后事实核查页面。生成subquestions明显优于直接搜索复杂claim，但与gold的比较未匹配查询数。few-shot摘要把单文档major/wrong从16%降到11%，claim级仍有24%至少一处严重错；更忠实摘要的subquestion覆盖反而下降，直接展示覆盖与忠实的张力。最终系统应把“找不到足够证据”作为合法输出，并为人类保留原文、时间和来源，而不是让摘要或分类器用参数知识填补空白。
