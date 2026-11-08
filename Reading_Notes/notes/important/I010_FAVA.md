# I010 Fine-grained Hallucination Detection and Editing for Language Models

## 来源、阅读及核查范围

Abhika Mishra、Akari Asai、Vidhisha Balachandran、Yizhong Wang、Yulia Tsvetkov、Graham Neubig、Hannaneh Hajishirzi。COLM 2024；本地arXiv:2401.06855v4（2024-08-12），23页，页眉明确正式会议版本。[作者主页](https://fine-grained-hallucination.github.io/)、[OpenReview正式入口](https://openreview.net/forum?id=dJMTn3QOWO)。已读1–10正文、14–23全部实质附录，10–13参考仅定位；目视2/4/5/6/8/14/15/21/23页，涵盖分类树、生成流程、公式、基准/消融表及人验界面。尝试下载OpenReview PDF返回HTTP403，未声称另一本正式PDF已下载或逐页比较；当前证据以本地明确标COLM的v4为准。

官方 [abhika-m/FAVA](https://github.com/abhika-m/FAVA) 固定 `7ec08c2dcbff016a7b6af93152994600b646f0a5`，ZIP406154字节，SHA256 `d34e3e6468474285dfb3e3c26404df4bf81eee406a3a554615132c55c79fcca0`，保存 `qa/I010_official/`。已读README、utils.py、run_eval/run_baselines/run_fava、process_train_data及generate_train_data控制流/模型选择；未声称逐行读完所有长few-shot prompt及Contriever内部源码。只静态分析，不执行模型、下载代码模块或API。

官方HF [fava-uw/fava-data](https://huggingface.co/datasets/fava-uw/fava-data) 固定 `f4e40415d525b18bcb49ba241f26fd8e12eeb606`，保存README、annotations.json和training.json。训练JSON137320668字节，SHA256 `5f6422b13b48b3f6fdff7bab4698b3702c90154c10cad519047f58600e6536a7`。独立 `sources/audit_fava.py` 读全部460人标行和30073训练行，核查样本身份、重复、标签结构、六类比例、精确文本交集、源码AST语法及论文算术，结果 `qa/I010_data_audit.json`。没有表2/3完整预测缓存，不把数据核验说成FAVA模型性能复现。

## 1. 目标、贡献与综述定位

FAVA同时提出六类幻觉分类、FAVABENCH人标基准和一个检索增强的检测/编辑模型。任务不只判整篇有无错误，而是说明哪里错、是哪一类、可否局部改正。模型以Llama2-Chat7B初始化，用合成错误及带类型的修订目标训练；推理时检索证据，再生成带标签与修改的原文。

综述位置是“开放域细粒度事实性”“合成错误监督”“检索核验与事后编辑”“指标与修复质量”。与PsiloQA的关键区别：FAVA训练误差由受控插入获得，目标是web world knowledge；PsiloQA诱发自然生成错误，再依指定来源/参考标注。两者都含span标签，但FAVA自动主指标实际上降为句子×类型判断，不能把其F1与PsiloQA字符IoU当成同一定位能力。

作者定义幻觉为相对外部世界知识的事实错误或未验证陈述，把世界知识操作化为搜索算法返回的相关web文档。常识、数值和逻辑推理错误明确排除。这是一个有信息边界的可操作定义，不是对所有客观事实的无限访问；“检索未找到”与“世界上不存在”尤其需要区别。

## 2. 六类体系：证据状态不全是已证伪

图2先问能否依据web知识核验；可核验且与证据不冲突是factual，可核验且冲突再分单位：Entity是改一个实体可使句子正确；Relation是关系/动词/介词/形容词等错；Sentence是整句冲突、不能靠短语最小替换解决。剩下分Invented、Subjective、Unverifiable：虚构核心实体、主观无普适真假、客观断言但检索没有直接支持或反驳。

这里“主观”不是“已经虚假”，“unverifiable”更明确可以实际为真。两者被算hallucination，是信息寻求文本的规范选择。对于意见问答、创作或隐私相关陈述，是否应删除要依用户任务，不可直接把此taxonomy当所有场景通用错误定义。实体/关系/句子类别也依编辑粒度：同一错误可能有多种最小修订，边界和类别均存在主观性。

Invented要求核实实体不存在，比“当前top5没证据”更强。在开放世界，很难有限检索证明不存在；检索召回、别名、语言、时效和索引范围都会影响分类。FAVA让人标者搜索web并记录URL，能增加证据覆盖，但仍非逻辑上的完整不存在证明。Fictional entities in creative work明确不在Invented内，不能见小说角色就标。

处理建议与标签分支也有差别：Entity/Relation通常替换短词；整句冲突、虚构可删除；主观/不可核实可标明而不一定断言其假。图2右分支写“highlighted to convey unverifiability”，后文又说应移除部分句子；实际后处理是否删除，必须检查mark/delete标签，不能只由错误名推断最终编辑文本。

## 3. FAVABENCH：问题、回答、标注行的分母

第5页设计200个问题，四来源各50：OpenAssistant经GPT4筛选知识密集问题、No Robots开放QA、作者撰写更需推理和知识的指令、WebNLG模板转换。三个生成器ChatGPT(gpt-3.5-turbo-0301)、Llama2-Chat7B/70B，理论600个回答；每例两人标，论文说收集1010标注passages含早期实验批，最终自动评测902，不能把902都当独立问题或独立回答。

正文招20学生（10本科/10NLP研究生），每例两标，45分钟培训；附录A描述10名CS本科、各60篇。可能涉及不同轮次，但论文没给全批次身份映射，不能替作者自行补出一致的全流程。正文每标约10分钟付$3.5；图6写60条、600分钟、总$200（$20/h），即单条约$3.33。报告成本时要说明不同描述，不能假装是精确统一账单。

目视图5界面可选type、输入改词、highlight span、勾选是否用Wikipedia，或记录web来源；图6要求无法核验时也提交搜索的top10 URL。它不是单凭标注者常识投票。正文称Cohen kappa并报句级75.1%、精确类型60.3%；没有完整双人对应表/计算细节，不能随意把这两数字同时称raw agreement和κ。细类别分歧较大也提示taxonomy并非客观唯一分解。

目前固定HF人工文件实际460行：chatgpt252、llama208；来源WebNLG182、instruction-following140、OpenAssistant138，**无No Robots行**。llama字段没有区分7B/70B，不能据此复原三生成器表。460行仅267个唯一output、150个唯一prompt；按(model,output)也是267组，组大小1/2/3/4/5分别121/110/27/7/2；414个不同(output,annotated)组合，46行与另行两字段完全相同。118输出组有不同标注字符串，符合多标/多批次存在的可能，但没有annotator ID，不能知道每条来自谁、如何仲裁。

因此实际发布既不是460个独立模型响应，也不是论文完整902评测的可直接替身。267去重输出也非按全语义去重的独立事实。公开行上“含任一标签”的比例chatgpt63.095%、llama71.154%；论文59.8/70.2/64.9对应不同生成器和完整样本，不能拿公开子集强行声称完全复现/推翻。

## 4. 人标错误分布的版本问题

正文表1按三生成器给类型分布，Entity42.7/48.6/55.7%；正文总体Entity48.3%，invented14.1%、sentence18.1%。但附录表7是Entity28.4、Relation2、Sentence6.1、Invented3、Subjective20.2、Unverifiable40.3，实体比例和不可核验比例显著不同。可能混有早期批次，论文未明确表7究竟对应哪批，不应合并为统一结论。

实际460行按开标签计1132个类型span：entity487(43.021%)、relation32(2.827%)、contradictory174(15.371%)、invented150(13.251%)、subjective138(12.191%)、unverifiable151(13.339%)；153行无开标签。这里是带重复标注的span计数，不是唯一事实/句子的类型占比。标签严格栈检查460行均配对正确；结构正确不代表事实金标正确。

第2页说除实体外其他类型“over60%”，表1和正文Entity约48%对应非实体约52%，不能直接推出60%；附录Entity28.4对应非实体71.6又属不同统计。综述可以稳妥写“存在多种非实体错误”，不要挑一个未对齐的百分比强化叙述。

## 5. 训练合成：从种子到可逆编辑

第6–7页图4三步：Wikipedia参考经ChatGPT换成文章、博客、tweet等体裁，仍要求只用来源信息；逐类插错，保留此前错误；最后逆转插错时的mark/delete来形成“坏文本→带修订标签的好文本”。训练参考包括原gold加四个Contriever-MSMARCO相关段落，打乱顺序。这个gold-included训练与test只检索top5有分布差异；原参考在候选集合内是构造已知的支持，不是检索器独立找到的证明。

作者称总35074例，约30074 Wikipedia和5000NQ；正文有“30,0074”印刷异常，不能按300074解读。实际公开training.json仅30073例，字段只有prompt/completion，没有NQ来源ID或topic列表；全部prompt恰5个Reference标记。不能确定缺的一例原因，也不能把未发布的5000NQ当已下载。本次按实际全文件核查，非完整原训练重建。

六类实际开标签：entity22090、relation20892、sentence15895、invented15057、subjective14601、unverifiable15423，总103958，约3.46跨度/例。比例21.249/20.097/15.290/14.484/14.045/14.836%，接近表10的21.2/19.9/15.3/14.6/14.1/14.9；“每类约15%”只是很粗的概述，实体/关系明显更高。637例零开标签，标签最多36个；插错类型数与span数不同，一个选中类型可以插多个span。

代码六种类型依次各随机Bernoulli(.5)，没有seed固定；理想独立选择下平均3种、全不选概率1/64=1.5625%，但实际零标签637/30073≈2.118%又受生成失败、实际插入与过滤影响，不能用理论选择直接预测实际跨度分布。生成器源码用未固定日期的gpt-3.5-turbo而论文说明0301，模型漂移影响复现；GPT4给invented/unverifiable，其他用ChatGPT，任务复杂度与生成器质量绑定。

训练30073个prompt/input均唯一；按公开 `Text:` 段和人工output做空白规范后的精确文本交集0，completion与人工annotated精确交集0。这仅排除这种逐字重叠，不排除文章、实体、事实、模板或预训练污染；公开训练没有明文原文章ID，尚未做可靠文章隔离。不得由0精确交集宣称完全无泄漏。

## 6. 实际标签与合成质量核查

独立用只识别六类+mark/delete的严格栈检查，训练631/30073（约2.10%）有不配对/交叉/缺关闭标签。例18的Robert J.外层entity未在局部关闭；例30多个relation缺闭合；例38末段relation也缺闭合。这些是语法结构问题，不是人工事实判错，也不保证导致训练崩溃：模型可以学习不规则目标，但检测解析与编辑应用将更难。

公开 `swap_error_tags` 还有确定的代码问题：将 `</contradictory>` 替换成 `</delete><contradictory>`，最后是新的开标签。当前发布很多contradictory标签又是正常闭合，故不能断言此版本代码原样生成了所有公开训练样本，更不能把全部631归因这个单一bug。需要实际生成/后处理版本和原中间文件才能追溯。

人验50合成例，iterative validity1.66/2、quality1.36/2，one-shot1.1/.9；差+.56和+.46分，不是83%和68%的直接正确率，更不是每个错误独立正确的概率。评分0指不足一半符合、1至少一半、2全部符合，是粗有序量表。人验支持逐步插错较好，不证明每条种子原文事实完美或所有插错真实可见。

风格改写也可能自行引入主观、时间词或新事实；若这些没有标签，训练gold便不完整。Wikipedia多体裁有助扩大表面风格，仍不等真实模型错误分布。平衡合成类与自然极少类之间的先验差异，会改变precision和阈值；这正是与PsiloQA自然错误比较有价值之处。

## 7. 训练与检索设置

Llama2-Chat7B初始化，标准自回归loss预测带标签编辑文本；表11 BFloat16、2epochs、weight decay0、warmup.03、lr2e−5、max sequence2048、batch128，4×A40、Open-Instruct训练。输入参考很长，2048是否裁掉目标/证据及其比例未报告，本次未下载模型tokenizer去重算，不把字符长度等同token。

推理Contriever-MSMARCO检索Wikipedia top5，论文说Wikipedia January2023，开放web的人标世界知识可比它更新/更广。README提供的是DPR Wikipedia psgs_w100与预生成embedding下载指引，并不自动证明正好同January2023快照；没有下载巨大索引，本次不声称复原检索环境。训练原gold+四相关段落、检测top5、编辑entity匹配+四retrieval再rerank/order，是不同配置，不可用一个“RAG”词抹平。

基线ChatGPT/GPT4提示六类与demonstrations；Rt+ChatGPT补top5。第8页明确因成本**没有retrieval+GPT4基线**，摘要“outperforms retrieval-augmented ChatGPT and GPT4”不能读成两者都有检索。白盒13B格式差被未纳入主要检测比较，也是一种基线选择边界。

## 8. 自动检测到底测什么：公式、宏平均与对齐

第4–5页因span主观，自动评估改为每句每类是否存在，最后六类F1宏平均。若gold把句子中的A实体标错，预测却把同句另一个正确B实体标错，只要同类标签存在仍算句级命中；它无法证明精确边界或具体错误解释正确。类型多标签可共存，不能写六分类互斥accuracy。

式1印刷分子是 `sum 1[pred==gold]`，把TN也计入，而分母仍预测positive或goldpositive。字面会产生precision>1：gold=pred=[1,0,0]给3/1=3；常规定义应为TP。源码run_detection在“gold含类”和“pred含类”的各条件内判断，意图近似正确TP/positive；但不执行此有外部依赖的函数，也不证明论文原表实际用了印刷错误。

更严重的是式2六类等权F1与表2Avg不一致。独立算六个已印F1的均值：ChatGPT响应上FAVA44.783而Avg48.1；GPT4 27.083而Avg34.2。Llama70B响应上FAVA41.067而Avg47.2，GPT4 29.85而Avg42.5。表12 Llama7B响应上FAVA42.625而OA39.6，GPT4 24.117而OA47.3。差远超一位小数舍入；可能有先逐篇平均、缺类过滤或另一整体指标，但目前文稿与公开汇总代码未完整指明，不能自行选一种机制当事实。

表13/14OA caption又叫“overall accuracy”而标题分别precision/recall；不能把OA统称accuracy、macroF1或microF1。这些指标身份不同，正文说accuracy namelyF1也需翻译成“作者报告的检测F1”，而非真正正确率。仅有边际表不足以恢复逐例汇总和置信区间。

公开run_eval把gold/pred分别分句后取两者最小句数，按索引配对；模型若删一句/合并句子，后面可能错位或被截掉，不是基于原答offset的稳定对齐。最小反例：两句gold标签[0,1]，预测只返回一条干净句，min只评首句，漏掉后一句假阴性。这里是独立结构反例，未声称某个已保存FAVA输出确实如此。

## 9. 结果与边界：强于哪些、不是强于全部

第8页表2印刷Avg：ChatGPT输出FAVA48.1、RtChat24.4、GPT4 34.2；Llama70B输出FAVA47.2、RtChat27.8、GPT4 42.5。48.1−24.4=23.7**个百分点**，正文“23.7%”不宜翻成相对提升23.7%。各类有例外：ChatGPT回答relation FAVA25<ChatGPT28.6，invented16.7<GPT4 22.2；Llama70B relation34.5<GPT4 60；不存在每类全面胜出。

表12 Llama7B印刷OA，GPT4 47.3>FAVA39.6，恰与正文“强于所有”有反例；但按其六类F1重算FAVA反而更高，说明OA定义未明足以影响排名解释。不能默默换成六类均值作为已更正作者最终得分，也不能只引用OA宣布FAVA实际全面失败。必须给两种所见值并保留待查。

表3二元句级F1：ChatGPT回答FAVA79.6、FActScore67.7、RtChat64.8；Llama汇总FAVA80.3、GPT4 74.2、FActScore71.2。高二元F1并不证明细类别或具体span都准；合并六类消除了类型分歧，样本阳性比例和类别边界也与其他基准不同。

表16人验50输出，FAVA检测正确55.7% vs RtChat23.9%，编辑63.5% vs17.2%，分别+31.8和+46.3个百分点；平均检出2.4 vs1.9个/篇。它主要是已提出检测/编辑的正确率，不是全真实错误的recall；“检出更多”又与precision不同。即便优势大，FAVA提出的检测仍约44.3%未被判正确，不能写已接近完美定位。正文一处说依据提供证据，第20页又说extensive web searches，人工协议要保留此范围不明。

## 10. 编辑、检索消融与事实性—信息量

表4传记任务FActScore：ChatGPT66.7→70.0(+3.3pp)，Alpaca13B42.5→51.8(+9.3)，Alpaca7B38.8→43.2(+4.4)。ChatGPT自编辑和RtChat在ChatGPT输出反而58.6/62.7，说明事后编辑会破坏原来正确内容；并非所有RAG修正天然有益。正文编辑模型大小有一处70B，而实验节列13B，不能据此精确归因规模。

FActScore主要核查生成原子事实支持，值提升可能来自删掉不支持内容，而非增加正确知识或完整性；其gamma长度相关配置也不能自动覆盖用户信息需求。独立例：原文两真两假，删去两假即可从.5到1，未新增任何事实；若连有用事实也删，需单独测保留率/回答完整性。推荐配对统计“旧真保留、旧错修复、新错引入、信息损失”，而不是只看一个平均FActScore差。

表18检索消融Alpaca13B：无编辑42.5，top1 44.2，top5 47.0，rerank47.7，+entity50.1，+order51.8。top5比top1是+2.8pp，正文说4.5其实相对无编辑；rerank+0.7；entity比top5+3.1（若比前一步rerank则+2.4）；order比entity+1.7。表5简版最后只到entity50.1，不能与表4最强51.8当同配置。

图7样本10k/20k/30k显示recall/F1随量升，precision20k最高再降，不是所有指标单调增加。无多seed和等质量对照，不能把这条曲线推成普遍规模律。逐类插错的人验优于one-shot，但它同时改变流程、调用次数和成本，不能把收益无条件归为“更强推理”。

## 11. 公开代码可执行性与结果复现限制

AST静态parse发现 `eval/run_baselines.py` 第39行缩进错误；不是依赖版本问题，当前文件不能直接正常解析。run_eval虽然parse通过，但构造reference循环 `prompt +=` 没有本地初始化、最后写 `instance` 未定义；vLLM返回对象未取 `.outputs[0].text` 就交字符串函数；utils里的nlp/np/results_rec/results_prec/error_types无模块内定义，调用方的局部同名量不会自动成为utils全局。run_fava示例还调用未定义parse_args。故README命令不是当前可直接再现实验的完整管线。

baseline接受retrieval开关却构造prompt时直接用每例reference，并未以该flag控制，输入若含reference就可能带来源；对照必须先检查实际文件，而不是仅看命令名称。源码有长文本时截证据到300字符、<50字符输出回退原文等行为，也可能改变覆盖率。没有原运行输出和版本，不声称原论文一定受这些问题影响。

标签清理最多处理10轮delete，且直接strip类别标签不会必然删除subjective/unverifiable内容；是否最终应保留取决于目标标签。swap closing tag问题已另有真实数据检查。建议修复时先做字符串单元示例、输出文本类型检查、稳定原文句/offset映射、缺类/空预测定义和逐记录缓存，再考虑重跑模型。当前未改上游原件、未执行paid API/训练，不把工程修复提案当完成复现。

## 12. 研究问题、独立结果与下一步

**Q1：细粒度生成标签是否等于细粒度评价？** 本文直接给出否定例：输出span、自动句级typepresence。独立同句A/B错位反例证明精确定位不能由句级F1识别。应与PsiloQA字符IoU、HalOmi词级病理、HalluEntity实体身份分列，不做一个统一“fine-grained score”排名。

**Q2：不存在证据是否能识别invented？** 有限检索只能识别当前证据缺失。设计应把retrieval failure、unsupported、contradicted、entity nonexistence、subjective分开，人标记录搜索预算和证据时间。可用扩充索引/检索深度观察Unverifiable→supported/contradicted的转移；本次尚未进行新web事实逐例复核。

**Q3：合成监督学到真实错误，还是学到模板？** 公开30073例类型比例接近文稿，但631结构异常，且全含gold参考。需要held-out文章/生成器、自然错误对照、去掉gold-included优势、统一训练量；精确文本交集0只是一项弱排重。与I119自然错误银标可以形成综述里的互补路线，不宜一方完全取代另一方。

**Q4：目前能否复现排名和人工κ？** 不能完整。公开460人标行缺annotatorID/902全量、llama规模未拆，源码有明显接口/语法问题，表宏平均又不明。已完成全部发布数据审计、表格算术和静态路径研究；还需要原实验commit、逐句预测/原标注关系和聚合脚本。不能以“库里有代码”当复现成功。

**Q5：FActScore增加意味着编辑更有用吗？** 不充分，已有删除提高precision反例和ChatGPT编辑反而下降的真实表证据。应配对评价纠错、误改、保真与任务完整性，记录输入/输出token与检索/裁判调用成本。把检测性能与最终修复效果分成不同证据等级。

综述可用表述：“FAVA将开放域事实性拆成六种可解释类型，以受控合成监督训练检索增强的局部检测与编辑模型，在多个生成器上的检测及传记FActScore取得较强结果。但其自动细粒度指标主要是句子×类型存在性，而非精确跨度；公开版本的样本、聚合和运行管线仍存在复现缺口，且主观/不可核实标签不应直接等同于已证伪事实。”

剩余待办：OpenReview正式PDF可用副本比较；完整902及1010批次的标注身份、仲裁和κ；未公开5000NQ与模型训练命令；全基线预测缓存/精确OA聚合；Contriever快照与tokenizer截断；母语/事实语义逐条核验；真实模型重算。以上均未虚报完成，不影响本篇正文与相关实质附录已经细读的进度身份。
