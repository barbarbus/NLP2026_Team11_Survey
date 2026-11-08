# I053 InteGround：多证据充分性验证与检索规划的四域对照

## 版本与核查范围

Jiayang Cheng等，*INTEGROUND: On the Evaluation of Verification and Retrieval Planning in Integrative Grounding*，Findings of EMNLP 2025，13587–13602，PDF16页。逐页读正文、附录、表1–13及图1–3；官方[仓库](https://github.com/HKUST-KnowComp/InteGround)固定commit `4a13e122d4d8dc1cbed6702fd82fdbe931073fa9`（1,011,307字节ZIP及SHA256/清单见`Reading_Notes/qa/I053_official/`）。只做源码静态核查，未调用Bedrock/API或运行完整模型，论文表格未复现。

## 任务定义与指标

给命题ϕ、候选知识库K，找证据子集Σ使Σ蕴含ϕ或¬ϕ；可回答“蕴含/矛盾/都不能证明”。本文实际核验实验折成`Entailment`与`Not entailment`两类，负类包含证据缺失，不等同现实命题为假（PDF2–5）。规划实验取K内候选排名，主要看Recall@5，即前五证据覆盖gold条目的比例；这不同于是否找齐**所有必要证据**，更不同于最终推理正确率。附录直接检索另给F1@5和Acc@5（PDF12–13），不能互换。

## 数据组成及构念风险（PDF3–4、9）

共1625命题：EntailmentBank340（平均gold4.5、K25），WiCE285（2.8、85.2），HotpotQA500（3.4、42.7），MuSiQue500（3.4、20）。EB从test任务2抽叶节点；WiCE仅保留supported、排除单证据、每claim只取第一个gold evidence group；QA从validation取至少三证据问题，再用LLM把问答变命题。不同域候选数量、证据单位、文本长度和来源差别很大（PDF12表8）。

WiCE明知多组合法证据，却只标第一组，其他足够支持的集合可能被错标“证据不完整”。Hotpot文章标题附到句子末、MuSiQue段落附标题，证据粒度不同；QA的LLM转换可能改变原问题量词/答案关系，未见独立等价率标注。KB候选是预构造、有限且含gold，并非开放网路检索；所谓跨域泛化限定于这四种构造设置。

## 核验实验：四种证据条件与真实结论（PDF4–6）

每题构造四套：完整gold，gold+随机distractor，gold的严格子集，混合候选但不满足与gold的集合包含。前两套标正，后两套标负。表3每个条件的百分比是**该条件准确率**，不是总体accuracy；表4是正类Entailment precision/recall/F1。

EntailmentBank中Llama3.1-8B完整/冗余正确95.9/95.9，但证据不全条件仅18.8；Claude3 Sonnet99.7/99.4、证据不全16.8；GPT-4o97.4/97.1、证据不全34.4。NLI-xlarge完整87.1、不全79.4，表现更保守。这支持LLM在科学常识命题上用参数知识补齐缺失证据的解释，但未用知识编辑/新颖事实反事实隔离“参数记忆”；也可能是负例标签错、证据可替代、prompt诱发过度推断。WiCE GPT-4o不全85.3、NLI高96.1/97.5，说明现象强度因域而变。MuSiQue Llama8B完整仅40.0，不能把该模型描述为普遍强验证者。

冗余证据相对gold整体影响较小，但并非绝对稳健：MuSiQue NLI-xxlarge完整43.6、冗余26.6，-17.0点；WiCE GPT-4o68.4→63.5，-4.9点。混合条件标负常容易拒绝，可能因随机distractor的表面分布与gold不同。

表4的NLI precision高如WiCE96.5/96.9，但recall只有53.3/43.9；Claude3.5 Sonnet WiCE precision96.0、recall41.6。单报precision会掩盖大量漏证。将NLI输出送入LLM prompt（图2）会提高缺失/无关拒绝率却伤完整/冗余召回，是阈值取舍而非无成本改良。GPT-4o结构化/CoT prompt在EB F1从76.9升81.4/80.1，却WiCE从75.4降63.5/66.4（表12），说明“让模型逐步检查”有域依赖的保守化效果。

## 规划实验与数字核查（PDF6–8）

四检索器BM25、MiniLM、mE5、ST5；三个LLM planner产计划，方式为query expansion、atomic/proposition拆分、premise abduction。表6是跨LLM的Recall@5均值：

- EntailmentBank BM25 no plan64.4，fact65.8，premise abduction**56.3**；WiCE BM25 no plan61.1，四规划均降，abduction52.4。
- HotpotQA BM25 no plan67.5、abduction70.8；MuSiQue BM25 no plan60.9、abduction67.7。
- MuSiQue mE5 no plan65.2、query expansion74.2、abduction73.7；此格query expansion最佳。Hotpot mE5 no plan80.1、abduction79.7，轻微下降。

因此“premise abduction一致改善”若意为所有域/检索器，不受表6支持；WiCE的四检索器均下降，EB只3/4上升（BM25大跌）。按16个域×检索器格数，abduction相对no-plan改善9格、下降7格；平均增量需区分不同候选库与模型权重，不能由单一格推整体因果。Query expansion同样不是“一律有害”：MuSiQue四检索器全部改善，Hotpot MiniLM也69.5→73.9。

反思规划图3需按同一检索预算解读。第二轮看第一轮top结果、再生成3–5 query，额外LLM与检索调用；若没有同预算随机/迭代基线，“self-reflection改善”不能归因于反思内容本身。当前正文说多计划拼接为query，附录又说Borda合并多个ranking；源码同时保存拼接后检索与逐query检索两分支。引用结果时必须指明表/图到底采用哪一融合分支，公开PDF没把映射说清。

## 源码复现风险

仓库只有25项，无论文原始完整缓存/标注结果；README要求用户自行实现`utils.py/get_llm_response()`，因此并非开箱即复现。`run_verification.py`固定seed20240627，完整、冗余、约半数gold的缺失、混合集各生成一条。混合集最多重抽10次，但超过次数仍接受最后结果，未显式assert集合条件；多合法证据组只取第一组。负类构造是基于ID集合规则，不是逐实例的逻辑非蕴含人工验证。

`run_history_aware_planning_individual.py`包含原作者绝对路径`/home/ubuntu/EventGrounding/...`，并对LLM JSON用`eval(get_dict(res))`解析；离开原环境会失败，解析未知输出也不安全。代码固定部分检索器注释，README未提供一键运行的API实现。每个正式表格的模型版本、prompt、原始计划和召回输出都应固定后才能复算。

## 可进一步研究的问题

1. 为每题人工/多裁判标注所有充分证据组合，复算“不完整”负例的真实非蕴含率。
2. 同命题替换实体/年份生成模型不可能凭参数知识补齐的反事实，再比LLM/NLI缺证误报。
3. 把Recall@5与`all-gold@5`、最终蕴含正确率联报，按gold条数和K规模分层。
4. 对每规划固定query数、总检索次数、LLM tokens和召回候选预算；加入第二轮无反思、随机query和oracle缺证提示。
5. 区分concat/Borda融合，发布每一模型×检索器×域的run级分数和配对区间。
6. 核查QA→命题等价率，以及WiCE多gold组、EB叶证据的充分性。
7. 修复LLM函数、绝对路径和JSON解析，提供缓存计划与评价脚本，使表6/图3可重放。

## 对综述可使用的结论

InteGround把复杂事实核验拆成“找到多条互依证据”和“判断证据合起来是否充分”，用四种证据条件揭示给定证据缺失时LLM过度蕴含的风险。检索规划效果高度依域、候选库与检索器；abduction在Hotpot/MuSiQue多格有效，却在WiCE全部四格退化，反思还增加第二轮预算。它是评价RAG幻觉的证据完整性与规划误差链的重要参考，不能把有限gold集合规则等同真实世界的证明或否证。
