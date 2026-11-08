# I005 ETF: An Entity Tracing Framework for Hallucination Detection in Code Summaries

## 来源、版本及核查范围

Kishan Maharaj、Vitobha Munigala、Srikanth Tamilselvam、Prince Kumar、Sayandeep Sen、Palanivel Kodeswaran、Abhijit Mishra、Pushpak Bhattacharyya。ACL2025，30639–30652，[正式来源](https://aclanthology.org/2025.acl-long.1480/)，DOI10.18653/v1/2025.acl-long.1480。库中arXiv:2410.14748v4，2025-09-06，14页；已读1–10全部实质正文、11–14完整提示/实验/NER/规则/标注附录，参考只定位相关条目。正式14页逐页文本差异核查，主要为空白、页码和表格提取分隔；目视正式2/7/13页流程、主表、分布及附录表。正式PDF908599字节，SHA256 `043158fce81030dc146ad50c0938620625b440b27d6465813b93fd204aaa3d4c`，存 `qa/I005_published.pdf`。

官方[仓库](https://github.com/kishanmaharaj/hallucination-in-code-summarisation)固定commit `e1fba184f38d0b751e5d1bdf770a663d361923d9`，ZIP19597字节，存 `qa/I005_official/`。已读4份notebook全部code cell、string_helper/javalang_helper和NER prompt；未执行下载源码或模型。独立 `sources/audit_etf.py`保存正则反例、分母及聚合计算至 `qa/I005_audit.json`。

作者[CodeSumEval](https://huggingface.co/datasets/kishanmaharaj/ETF-CodeSumEval)页面显示411行；页面样例表明每行嵌套entity-sentence标签。已写 `sources/fetch_etf_data.py`，但执行下载时自动审批因用量上限未完成审核，**下载没有执行**。本篇已形成详细正文/附录笔记，但全量CSV审计仍待办，不能将页面行数当全数据核查。未复现模型主表。

## 1. 任务与核心贡献

本文评估Java代码摘要是否忠实说明给定代码，属于来源条件的事实一致性，不是检查生成代码可否编译，也不是评价摘要的完整性、简洁性或代码自身是否正确。真实程序中的函数名、注释可能误导模型，因此“摘要看起来合理”不足以证明与实现一致。

贡献是CodeSumEval人工基准、四类错误因素taxonomy，以及实体追踪框架ETF。主流程：静态解析源代码实体；LLM抽摘要实体并过滤未真实出现者；匹配两端实体；未映射实体视为extrinsic；已映射实体与相关描述句形成tuple，由LLM核验intent；任一错误使整摘要判幻觉。

这把来源、摘要和局部描述连接起来，增加了可以检查的中间层。但AST实体存在不是程序语义证明，局部描述都通过也不保证全局控制流、顺序、条件和副作用正确；不应采用正文“验证全部功能”的过强表述。

## 2. 数据单位、采样和标注（第3–4页及附录E）

从CodeXGLUE Java取600片段，每段用7个生成器，理论4200摘要，再因平均每篇标注≥30分钟随机裁至约10%。报告411摘要、9933 entity-level tuples。正文一处写“441 summaries”，与Table1及多处411不一致，原清单待全CSV核查，不自行将441算成第二个已证实版本。

表1摘要130幻觉/281无幻觉，比例31.63%/68.37%；tuple CORRECT9024、INCORRECT303、IRRELEVANT606，加总9933。去人工IRRELEVANT后9327，错误303/9327≈3.25%，非常不平衡。9933不是独立代码片段、也未必是独立实体：同实体在不同句子可反复形成tuple，约24.17 tuple/摘要。

8位Java专家，至少CS硕士、平均4年以上经验；4354 tuples来自222摘要有两组独立标注，κ=.72，分歧由两位meta-annotator解决。双标约43.83% tuple，不能把κ当整个所有语料的准确率。人验先纠正NER，再判断entity-sentence CORRECT/INCORRECT/IRRELEVANT，最后评GOOD/FAIR/POOR；第二阶段依据反馈形成四类因素再回标。

GOOD说明文字一方面“almost no hallucination”，一方面“completely correct”，操作边界需要明确。作者观察FAIR/POOR平均1.33个实体错，再取阈值1，属于经验动机，不是从平均值数学推出最优阈值。漏信息与错误不同，故本数据不直接测摘要是否充分覆盖实现。

## 3. 四类因素及因果结论强度（第4–9页）

HC1 identifier name bias含变量/函数/库名：getJobID实际return -1，摘要却描述数据库查询；HC2知识不足含代码本身和缺外部实现；HC3复杂度含长度、词法、逻辑；HC4自然语言上下文含陈旧注释/日志。图3给13.2%、30.3%、52.1%、4.4%，合计100%。

图中是人工归因的类别分布，正文同时说name bias与知识不足常重叠；若按多标签计数归一，不是互斥错误概率。原始标签分母未全核查，不能把52.1%称所有LLM幻觉由复杂度导致的因果比例。要验证名称因素，需保持程序语义不变的重命名对照；验证注释因素，需正确/错误/删除注释同代码配对。

首例int16说明名称/概念与Java内建类型的混淆，但ColumnInt16也可能是合法用户类；“16-bit column概念”与“Java primitive int16”应分清，不能只见词形就判整句错。外部方法未给实现时，真实语义可能不可识别，应保留unknown条件，避免把常识推断一律当已证伪。

HC3 Redis案例中summary称success=false时归还broken resource，代码catch还检查jedis!=null；核查重点应是条件是否完整，而不单看归还方法名。HC4展示注释模式与实际regex不同，也提醒代码本身、作者解释及摘要应分开逐项核对。

## 4. 框架方法及覆盖风险（第6–7页）

代码端通过javalang lexer/AST取类、函数、变量、类型、值等；摘要端用带code/NL tagset及一个示例的LLM NER。过滤器旨在删掉NER捏造的实体，但过滤越严格也越可能丢合法形态变化、术语别名及短变量。未映射实体直接判extrinsic可能将合法库别名、类型通称和必要推论误报。

intent context最终选择规则抽取摘要中提实体的句子；附录D称LLM抽句会编造、改写或遗漏原句，因此偏好字符串。这个设计保护原文本身份，但代词、省略、跨句关系、camelCase与分词变化会漏掉真正解释。语义错误也可能不含命名实体，例如“该函数从不抛出异常”，实体先行机制可能没有覆盖。

验证prompt以完整代码和局部相关句要求CORRECT/INCORRECT/IRRELEVANT，测试时把模型IRRELEVANT视为INCORRECT，但人工IRRELEVANT先删除。这种不对称会惩罚无关预测，评价条件仍是人工认定相关的tuple；必须区分oracle实体/句子条件的核验与端到端NER+映射+核验。

working-memory理论和7±2/3–4对象被用作局部到整体设计的动机，本文没有人类注视实验或LLM认知测量，不构成方法因果有效性的证据。局部核查更多调用、更长总上下文也可能解释收益，需要同预算分解消融。

## 5. 摘要级73%与实体级61%（第7页Table2）

表明确macro P/R/F1。GPT4-Omni direct摘要F1 .28→ETF .73，+45百分点；Gemini .42→.64，Mixtral .45→.61，Llama3.1-70B .38→.54，Llama3-8B .26→.50，Mistral .24→.41。所有所列摘要F1提高，但并非所有单项提高，如Llama3-8B macro precision .59→.51。

实体级GPT4-Omni P.59/R.69/F1.61，Gemini .58/.62/.60；其余F1 .39/.56/.48/.49。正文在Entity-Intent Verification段引用.73/.64，实际取自上方Instance Level；摘要73%也指摘要级，而非9933个实体全局73%正确。

macro F1不等于对macro P/R作一次调和平均，故不以该差异直接断言表错；类不平衡下恒CORRECT的二类宏F1约.4917，恒无幻觉摘要宏F1约.4061。它们可作分布基线，但原评价过滤/标签实现与全数据未取得，不能宣称已按同样本正式复算并胜过某模型。

一个正确摘要中若有50个独立tuple，每个误报率1%，any-error聚合的误报概率1−.99^50≈39.5%。真实tuple彼此相关，此为独立假设示例，不是ETF实测误报率。它说明摘要级指标依赖长度/实体数，需按代码、摘要长度和tuple量分层，并按代码聚类给区间。

## 6. NER评价和代理教师（附录C，12–13页）

人工数据上GPT4o Jaccard .81、类型F1 .92；Gemini1.5 Flash .64/.92。这两个指标测实体集合覆盖与类型匹配，不是人类整体事实性相关系数。正文称“strong correlation”，但表没有Pearson/Spearman，不能写成相关系数.92。

开放模型NER在600代码的摘要上用GPT预测作gold；这测教师一致性，不是独立事实标注。Llama3-70B JS .5981、类型F1 .90、fabricated .15%；Codellama7B JS .4586、F1 .84、fabricated **35.68%**，正式表图已确认，不能因文本粘连“0.8435.68”误读为5.68%。

Table3 mapped最高88.44%并不等于事实正确率88.44%；一个实体名字能在代码找到，也可被错误解释。Summary length单位未在表明示，不擅自改叫token；七个生成器的摘要长度和实体数不同，mapping比例也不与summary-level幻觉率同义。

## 7. 实际源码：两套抽取、正则和缺失流程

utils/javalang_helper.py对片段包dummy class，遍历ClassDeclaration/MethodDeclaration/VariableDeclarator/Literal/Import/ReferenceType；没有显式处理FormalParameter、MethodInvocation、MemberReference、BasicType。notebook中的另一版identify_entities却处理这些节点，因此库函数与notebook实体覆盖不一致。当前缺完整历史manifest，不能确定哪套生成原实验数据。

utils/string_helper只用 `\b + re.escape(entity) + \b`，并无显式括号/数组/反引号规范化。独立同规则检验：foo()、values[]在后面跟空格时末尾非word到空格非word无边界，匹配失败；PreparedStatement与prepared statement形态不相等也漏；普通x可匹配。这是明确输入反例，不证明所有真实tuple都受影响。

Intent notebook把summary.lower后分句，但mapped entity是否统一小写需上游确认；遍历每entity每句，调用gpt-4o、max_tokens100且未设temperature，和附录temperature.3/max_new_tokens4000不同。后者可能描述另一步生成设置，不直接认定全部运行配置错误，但应分阶段列参。

notebook还引用未发布args模块和saved_data输入，含eval解析字符串而非安全字面解析；update_file_name返回新名但调用未赋值，后面仍用旧名。源码可说明实验思路，却不是下载后直接完整复现主表的成品。未找到全部匹配/过滤/宏指标计算与原预测缓存，本次没有运行这些上游notebook。

## 8. 提示、成本和泛化

生成prompt明确要求输入输出、business purpose、详细功能，这会鼓励超出片段的信息推测；对真实业务目的缺上下文的代码尤其如此。direct baseline也要求列错误实体/相关句，而非最简单二元判别，因此ETF收益同时含输出协议和分解差异，需同预算、同标签解析对照。

作者报告A100-SXM4-80GB单/多卡及多种生成/核验模型，Limitations明确多次LLM调用带来实时部署困难，未报告统一端到端延迟、API费用、失败率或吞吐。可按每摘要实体×相关句数估调用量，但缺全CSV与日志不造具体成本。

只测Java/CodeXGLUE及指定生成器，不能推广为Python/COBOL/Perl均有效；AST解析可用性、外部依赖、重载、回调及异常语义都改变任务。实体别名、creative summary误报是作者明确失败案例；计划用fuzzy/embedding、文档检索、多agent只是未来方向。

## 9. 可研究问题与跨篇对应

问题一是实体覆盖如何约束最终定位：需要完整NER、映射、相关句和核验各步召回，不能只报oracle tuple分类。与I001管线误差、C07原子分解、I002条件抽取后的实体可逆性共享命题身份问题。

问题二是未定义外部函数如何标真：可以将同名API的两个实现放不同仓库，保持局部片段一致而全程序语义不同，证明局部输入无法总确定真实功能。应把source-supported、contradicted、unknown分开，而非以名称猜测或简单未映射判错。

问题三是定位是否等于span检测：本文输出entity-sentence，不报告字符边界F1；与C12/RL4HS的全span覆盖不可横排名次。与FAVA同样需要分开局部错误标签和整体质量，与FactCHD一样需要核验解释/证据是否真正支持结论。

问题四是复杂度与错误因果：重命名、改注释、等价控制流变换及增加无关代码的配对试验，可分别识别词面、长度和逻辑因素；当前只有类别分析及本地实现反例，没有跑这些模型实验。

英文可用：ETF grounds code-summary evaluation in entity–description correspondences, but entity presence and local intent verification do not by themselves establish complete program-semantic faithfulness. Evaluation should distinguish tuple classification, end-to-end coverage and summary-level aggregation.

## 10. 尚未完成的核查

待下载固定HF全CSV，核验9933/411、唯一代码/模型分组、重复tuple及跨摘要相关性、标签与taxonomy字段、主表宏平均及实际原预测。待确认抽取函数版本、所有mapping/过滤/评分实现、格式失败、原实体召回和真实费用。当前审批用量问题只阻止新增下载，不抹去已完成正文/附录与本地源码工作；全量数据结论不得提前补写。
