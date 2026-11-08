# I008 FactCHD: Benchmarking Fact-Conflicting Hallucination Detection

## 来源、版本与阅读范围

Xiang Chen、Duanzheng Song、Honghao Gui、Chenxi Wang、Ningyu Zhang、Yong Jiang、Fei Huang、Chengfei Lyu、Dan Zhang、Huajun Chen。IJCAI2024，6216–6224，[正式论文](https://www.ijcai.org/proceedings/2024/687)，DOI10.24963/ijcai.2024/687。资料库arXiv:2310.12086v3，2024-05-26，9页；已读1–7全部实质正文，8–9参考定位，无另附实质附录。正式9页逐页文本差异检查，重读6–7，目视3/5/6/7的图、主表及案例。主要方法/数值一致，作者Lyu拼写和版面流动有变化。正式第7页仍有fine-tuning ChatGPT作Manager描述，不因跨页排版误判删去。

正式PDF保存 `qa/I008_published.pdf`，2085729字节，SHA256 `e96dea7af72f56d6e24c71af5e38ceaccce33bbe324fd61ddad667e335864e9e`。官方[源码](https://github.com/zjunlp/FactCHD)固定commit `451b26658c3325293f7cac9b3727cf6574e6d6dd`，ZIP1108995字节，SHA256 `0da40d4c9e9d697bcf3561863d2d26169a26762e9da806e1fa74a784ebb6b307`，在 `qa/I008_official/`。完整读README、评分两个文件、finetune/inference；针对性读生成函数、标签转换、KG采样和解释prompt。未声称逐行读完所有生成工具文件。

按README取得官方[完整数据](https://huggingface.co/datasets/zjunlp/FactCHD)，固定revision `12d00b048630728fc2f8626b678e91658f258bbe`。`qa/I008_data/`保存训练42361059字节、测试5722150字节JSONL及各自SHA/来源provenance。独立 `sources/audit_factchd.py` 检查全部58343条，不执行上游API或模型；结果 `qa/I008_data_audit.json`。以下明确区分论文报告、当前发布资源事实、静态实现推论和待实施实验。未重训模型、未复现主表、未验证所有世界事实。

## 1. 研究问题与在综述中的位置

论文关注给定用户问题Q和模型回答R，判断是否有fact-conflicting hallucination，并生成解释。与只输出一个分数的检测不同，它要求标签和理由；与RAGTruth、FAVA不同，主评价不要求完整错误字符跨度；与TruthfulQA不同，它主要评估检测器对固定问答的判断，不能把检测F1当被检测生成器本身的真确率。

标准检测输入不附生成时gold knowledge/evidence，检测器可依内在知识或自己检索；生成金标解释的ChatGPT却看标签及事实。这构成明确的信息预算不对称。基准将外部世界真确、给定知识支持和推理有效性紧密结合，讨论时仍应区分：知识图谱未收录不等于世界为假，文本无证据不等于反证，数量/集合关系判断错误也不等于实体事实不存在。

其价值是扩展多步关系、比较、集合问题以及解释评价，并提供训练资源和多源检测框架。最稳妥的综述定位为“合成的问答级事实冲突检测与标签条件解释监督”；不能无条件称自然用户流量中的全面幻觉评估。

## 2. 四种推理模式与知识来源（正式2–4页）

Vanilla由文本事实构造问答；其余通过KG形成多跳关系、定量比较、集合运算。Wikidata与PrimeKG提供关系结构，文本来自FEVER、Climate-FEVER、HealthVer、COVID-Fact、SciFact等事实核验资源。作者使用438种关系，希望覆盖普通和专业知识。KG采样包含关系路径、共同属性及交集等，复杂性不是只延长文字。

多跳要求链上每一步成立、实体对齐正确、最后答案满足问题；一个关系正确不能证明整条链。比较要求统一时间、单位和对象集合；数字复制正确而大小关系写反仍错误。集合问题还涉及完整性：列出若干满足条件的对象，并不能证明“所有对象”的全集穷尽。KG开放世界假设尤其限制否定与全集答案的金标可信度。

代码还有 `subgraph_type=all`：`generate_all_subgraph`取BFS关系并加入属性，属于混合图，不宜直接等同语义纯集合运算。当前数据中将set_operation与all的数量相加，恰与论文SET列总数一致，但没有找到完整的发布分类转换，故这里只报告数量对应，不证明原主表每条all都按SET评分。

七领域并不均衡。训练common Wikidata15370、Wikipedia14398、public health9088、COVID7117、medicine4027、science693、climate690；测试相应2109、1961、987、1096、400、190、217。领域分布发生变化，且知识来源与推理模式绑定；领域表现差异可能同时是知识、问题模板及推理类型差异，需交叉分层才能识别。

## 3. 数据生成：已知答案条件下造错误和解释

ChatGPT根据知识构造问题、正确回答和似是而非的错误回答；提示还利用ChatGLM/Alpaca/Vicuna等真实模型错误作为示范，降低明显的纯实体替换。策略包含错误推理、误解问题、过度泛化或具体化等。使用真实错误示范不意味着全量样本是未经干预的自然模型输出，生成器及提示的文风仍可能成为分类线索。

官方 `kg_data_generate.py:684–739` 的 `generate_all_use_chatgpt`明确先以0.7概率选hallucinated_answer并置NON-FACTUAL，否则选correct_answer置FACTUAL，再把标签、问题、答案和knowledge传给ChatGPT生成reason。这里0.7是此函数当前采样参数，不是最终全基准的阳性比例；不能从代码参数强推数据先验。

`KG_GENERATE_DATA`与`KG_GENERATE_DATA_MULTI_HOP`明确告诉教师正确标签，要求基于Evidence解释，甚至禁止在输出使用“evidence”一词。因而gold reason是标签知情的事后解释，不是独立检测器盲判的推理轨迹，也不是模型内部认知过程的忠实记录。解释符合既定标签和解释真正核实事实是两个目标。

文本路径 `text_data_generate.py:385–421` 先把SUPPORTS/REFUTES转为局部变量label的FACTUAL/NON-FACTUAL，传入解释prompt；408行后校验却比较尚未更新的 `data['label']` 与新标签字符串。在预期SUPPORTS/REFUTES输入下两分支均不触发，最后才写回新label。因此该路径的检查不能保证reason首行与新标签一致。KG路径在生成前已写新标签，不能将同一缺陷扩展到所有KG样本。当前资源中确有不一致，但没有逐条生成日志，不能证明所有不一致均由这一分支造成。

## 4. 质量控制及其统计限度

论文描述小样本人工检查、SBERT相似去重及人工过滤；删除相近样本训练1542、测试832，人工再过滤565/258，最终51383训练和6960测试。报告保留测试集的κ=.858，说明所用保留样本、标注协议下有较高一致性，不是生成全流程原始错误率，也不能证明标注者共享的知识误区不存在。

“每模式检查5例且要求95%一致”需要谨慎理解。若每例一个二元质量决策，5例的比例步长为20%，达到95%实际上要求5/5，仍无法估计总体≥95%质量；多人判断同一5例不会变成大量独立问题。应报告抽样单位、标注人数、排除规则、分歧前后κ与逐类误差，而不是只把95%当可靠性保证。

自动生成解释可能出现与标签一致但理由错误，甚至理由内部矛盾。第一条公开训练记录 `1297e6a9-fe7e-11ed-a6c9-fa4faded13a2` 的reason同时给Honshu103000000、Spain43653155，却说前者略小于后者。仅比较其自身数字即可发现矛盾，无需假定这些历史人口数字真的正确。这是解释金标需另行核验的可复查例，不是全数据错误率估计。

## 5. 全量公开数据审计：数量吻合不等于标签及划分吻合

所有记录均有id/label/query/response/reason/type/domain，KG记录有subgraph_type及部分规模字段；当前noe发布不含原始完整证据或来源ID，无法逐条重建原gold evidence或检查来源级隔离。

训练51383，FACTUAL26570、NON-FACTUAL24813；测试6960，FACTUAL3603、NON-FACTUAL3357。模式训练vanilla31986、multihop8209、comparison5691、set4500、all997；测试4451、1013、706、570、220。四模式论文总数可以由set+all合并得到5497/790，但该合并的语义和实验分类仍待原转换脚本确认。

独立规范化reason前缀，训练得到NF25632、F25729、未知22；测试NF3530、F3427、未知3。与结构化label不一致训练855、测试182：训练826个F→NF、7个NF→F、22个F→unknown；测试176/3/3。这里是字段一致性审计，不是855/182条的世界真值自动裁决。例 `common_71082` label为FACTUAL，而reason以NON-FACTUAL开头并论证Wales不是island；训练目标读取哪个字段直接影响评价任务身份。

训练和测试各自没有重复id，但两划分**共享200个id，且这200条全部完整记录逐字段相同**。例如 `99e5101e-ff63-11ed-8891-3af931db02dc` 的电影Rope问题、action回答、NF解释整条重合。共享Q+R有261个不同组合，涉及265测试行；共享问题518个，涉及1586测试行。完整记录重合是当前固定版本可确定的划分污染，不能用“只是同一主题”解释。是否所有历史模型使用这一版本训练仍需作者实验manifest，不能反向假定。

训练Q+R唯一组合45314，其中407组存在不同结构化label；测试6038组，其中70组不同label。相同可见输入给相反标签，意味着QR-only检测器不可能对这些记录同时确定性全对，除非引入隐藏证据/时间或其他任务变量。当前不含原证据，不能排除不同隐藏上下文导致某些合法差异，也不能直接把每组多数标签当修正真值。后续应将冲突组与完全重合组单列敏感性分析，不私改原基准。

## 6. FactCls究竟如何计算：阳性F1与格式覆盖

论文称FactCls为Micro-F1，强调NON-FACTUAL为正类。源码 `evaluate/metrics_plus.py` 实际按正类TP/FP/FN计算F1=2TP/(2TP+FP+FN)。这可称池化阳性F1，但不是所有类别micro-F1（单标签二分类时等于accuracy）。例如gold[NF,F,F]、全预测NF，阳性F1=.5而全类micro-F1=1/3。综述必须明确正类，避免把78.15解释为78.15%准确率。

按当前测试结构化label，全预测NF阳性F1=65.077%；若gold取reason前缀并按源码忽略未知，约67.321%。因此报告zero-shot ChatGPT52.82、ICL61.04时需要同时给恒正基线；这些分数并不自动表示优于简单类先验。因历史gold转换未知，这里是明确条件下的资源基线，不声称已经重新跑赢论文模型。

实现另有重要边界：预测不以识别标签开头时记fail，但对正类gold没有追加FN，对负类也不追加FP；`prediction is None`还会跳过整体计数。独立例gold[NF,NF,F]、pred[NF,UNKNOWN,F]，该TP/FP/FN路径给1.0，若未知阳性按漏检计应为2/3。主表是否受此问题影响，需逐条预测及格式失败率；静态反例本身不证明某模型利用了漏洞。

复现应同时报告总样本、有效输出、格式失败、F1全分母版本、选择性有效样本F1及覆盖率。格式改进和知识改进不可混为一种增益，尤其LLaMA2 zero-shot5.77大幅偏低时。

## 7. ExpMatch：参考措辞匹配不是解释正确性的充分指标

设计将解释分head/body/tail，权重.15/.70/.15；head和tail用ROUGE-L，body用词级F1。它试图弱化标签判断句和结论、强调中间理由，有明确可复用的分解动机。但参考解释来自标签条件教师，词重合评价容易偏爱教师文风，不直接检验事实、逻辑、证据充分性或解释因果忠实性。

源码按字符串`.`切句，U.S.、Dr.、3.5等可被错误分段；≥3片段直接第一句head、最后一句tail、中间body，并不识别语义功能。短输出的head条件同时要求startswith('The')和startswith('the')，逻辑不可满足。剥标签仅支持全大写/全小写前缀，TitleCase可残留。body F1直接空白分词，未像全回答比较那样规范化，大小写和标点会改变得分。

实际ROUGE函数默认measure='r'，即recall，并非自动ROUGE-L F1；分项先跨样本求平均再加权，缺失项的计数规则必须保留。论文脚注说不合输出格式ExpMatch置零，当前evaluate_response路径却未见统一的格式失败清零门控，仍会计算head/body/tail。复算时必须明确跟论文定义还是跟当前代码，不能悄然混合。

独立词袋反例“两个主体交换关系”中，`Alice exceeds Bob`与`Bob exceeds Alice`词级F1=1，关系真值却相反。它证明词袋body不识别论元方向，不证明所有现实解释分数都失效。可加入数字/否定/主体交换最小对、引用证据蕴含、步骤有效性和盲人验作为元评价。

## 8. Triangulator：多源判断的融合及独立性条件

Guardian是FactCHD微调模型；Tool组件调用外部工具/知识；Manager汇总来自不同方向的判断并给最终标签和解释。论文使用社会科学triangulation动机，试图以内部模型、工具证据和管理者减少单源误差。

多个角色不自动构成统计独立证据。标签教师、工具使用者或Manager可能共享ChatGPT家族，Guardian又学习该教师解释，错误高度相关时投票/综合未必降低偏差；Manager的更流畅解释也可能隐藏来源冲突。应测错误相关性、证据重叠率、角色消融、同token预算独立采样以及含错误工具结果时的恢复能力。

正式第6页图5的医疗案例，Manager一方面给NON-FACTUAL，一方面写回答正确、没有fallacies，角色间药品名称也变化。这里仅指出图中文字内部矛盾，不据此提供临床结论或判断药物真实关联。第7页Probst案例最终解释添加检索引文未显示的职业属性，展示性案例不能替代完整证据归因测试。

官方固定仓库未找到完整Triangulator执行入口、Manager训练配置、逐角色调用缓存与成本追踪。正文描述fine-tuning ChatGPT不等于现有开源脚本已覆盖整个框架；原始调用/训练版本需要补齐。两个域外成功案例是质性展示，不是OOD统计泛化测量。

## 9. 主结果与正确的增益分母（正式5–7页）

Table3 ChatGPT zero-shot FactCls52.82/ExpMatch24.03；ICL61.04/41.96；工具增强68.63/42.37。检索有收益，但工具预算、上下文量与训练状态不完全等同，不能把差值全归因某一种检索器。

LLaMA2-7B zero-shot5.77/29.41，ICL30.25/43.02，LoRA74.73/53.71，加Wiki75.86/54.58。LoRA比ICL FactCls+44.48百分点，包含领域适配、标签格式、解释风格等多重因素，不证明模型突然获得同等量的新世界知识。需盲测生成器/问题/来源分割及格式标准化后的差值。

Triangulator78.15/52.52，相对LLaMA2 LoRA+Wiki分类+2.29百分点，但解释−2.06；相对不加Wiki LoRA分类+3.42、解释−1.19。不能写成分类和解释均最佳。集合FactCls80.87较高，但comparison66.27低于Alpaca LoRA69.92，亦不是所有模式均胜。

Alpaca LoRA70.66/54.96，加Wiki71.32/55.07；Vicuna69.58/54.98→70.86/56.28。不同基模型收益不同，有些解释匹配更高；需按指标和预算给结论，不能把单列冠军推广为整体最可靠。

Table5 Alpaca提供gold evidence后分类83.56，相对70.66高12.90百分点。这是oracle知识可用条件，说明信息瓶颈的潜力，不是现实检索系统已达到的增益。不提供query则30.48，下降40.18百分点、相对下降56.86%；“下降40%”应明确百分点。去Q也破坏关系指代和问题意图，不宜只解释为缺少一句额外上下文。

13B相对7B zero-shot63.28 vs23.10，ICL64.70 vs28.34，LoRA72.89 vs70.66。规模效应在未适配状态大，在该微调条件小；不能从两点推普遍规模律。总体F1是池化非线性函数，不应简单平均四类型列强行验证总列；ExpMatch也需知道样本/缺失项权重。

## 10. 训练、推理及评分资源的可复现性边界

finetune.py监督 `data_point['output']`，数据必须先变成instruction/input/output格式；HF公开原始是query/response/label/reason，未找到连接完整公开数据到实验input/output/category的最终转换脚本。仓库确有FEVER claim-evidence格式转换函数，但那是另一中间任务，不能当作FactCHD问答解释全量适配器。故尚不能确定历史训练和评分更信结构化label还是reason前缀。

README和run_alpaca.bash给10epochs、batch240、lr1e-4、cutoff800、LoRA r16/alpha32、3GPU；函数默认3epochs/batch80/lr3e-4/cutoff256/r8/alpha16，不宜混报。脚本指向src/finetune.py而当前文件在仓库根目录，部署要修路径。val_set_size=None分支会用None参与乘法，但示例传2000可避开，不能说所有运行必然失败。

inference只在CUDA分支构造模型；CPU路径不完整。长于1024输入返回空串，与格式失败评价相联系。generation含temperature=.2、top_p=.75、top_k=40、num_beams=4、max_new_tokens256，但未明确do_sample，仅有temperature参数不能证明真的采样。原始运行需保留有效生成配置、截断率和随机种子。

score.py按id建立字典，重复id可能覆盖；缺失id异常分支打印pass却不continue，可能沿用上一轮data或首轮未绑定变量。正式复现应在对齐前assert唯一、全集覆盖和相同candidate身份。此为当前代码静态问题，尚未获得原预测，不能证明主表实际发生错配。

## 11. 由本文提出并研究的问题

问题一：检测提升来自推理还是模板/格式？已有证据是合成paired回答、标签条件reason及zero-shot格式敏感。可行研究是生成器held-out、同Q相反R成对、去掉固定reason句式、长度匹配和格式修正前后F1；当前只完成数据与代码审计，未实施这些模型实验。

问题二：标签本身是什么？全量检查已经量化label/reason不一致、可见QR冲突、完全重复划分。下一步须保存原版，按字段身份构造并行评价，人工核验冲突并检查隐藏来源，不直接多数投票纠错。即使检测器分数变化，也要区分任务定义变化和模型进步。

问题三：解释分高是否真的更正确？关系反转词袋反例、数字内部矛盾及脚注/实现差异已提供否证“高重合必然有效”的证据；尚没有全量盲人验相关性。建议分别报告标签正确率、理由事实支持、推理有效性、引用忠实性和信息完整性，再研究ExpMatch对这些维度的相关，而非合成一个总分遮住冲突。

问题四：多角色为什么有用？主表支持分类边际提升而解释匹配下降；共享教师使独立性前提存疑。应固定模型、检索结果、总调用预算，以单角色多样本和角色融合比较，并测Manager是否识别冲突证据。当前没有工具轨迹和预算，无法识别收益是视角、更多token还是Manager先验。

## 12. 与其他已读论文的对应及可用于综述的表述

与HaluEval对应合成错误和教师风格；FactCHD增加多步推理及解释，但共享合成分布/金标生成风险。与FELM对应细分类错误和外部知识，FELM细粒度标注与本篇问答级标签不能直接横排。与RAGTruth/PsiloQA/RL4HS对应来源条件、标签字段身份和解释监督，FactCHD没有完整span目标；与FAVA对应解释匹配与真实修复质量的分离。

与LM-vs-LM、SAC3对应多次/多角色判断和错误相关性；与SummEdits、Illusion of Progress对应合成标签元评估及指标选择；与QAGS/QAFactEval对应词面/QA代理不能自动保证事实性。可在综述“复杂推理基准”“解释与可追溯评价”“元评价和复现边界”三处交叉引用，不把本文仅列入一个互斥类别。

英文可写：FactCHD extends question–answer hallucination detection with reasoning-oriented synthetic examples and label-conditioned explanations. Its results should be interpreted under explicit knowledge and output-format budgets; lexical explanation agreement and pooled positive-class F1 do not by themselves establish factual or causal validity of the explanations.

## 13. 待办与结论强度

已完成全部实质论文阅读、正式关键图表核对、固定源码阅读、58343记录全量字段/交集审计、公式及解析反例。仍待原实验commit/数据manifest、最终格式转换、Triangulator训练/工具调用与成本、原始模型输出、人工语义复核、源级分割及修订标签敏感性实验。未声称发现了所有事实错误，未声称复现任何模型主表。资源问题是当前固定公开版本的证据，历史成绩受影响范围保持未决。
