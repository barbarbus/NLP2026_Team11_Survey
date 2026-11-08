# I032 FACTOOL：工具增强事实核验的四种任务并不共享同一个“事实性”

## 来源、阅读边界与资源状态

I-Chun Chern、Steffi Chern、Shiqi Chen、Weizhe Yuan、Kehua Feng、Chunting Zhou、Junxian He、Graham Neubig、Pengfei Liu，*[FacTool: Factuality Detection in Generative AI — A Tool Augmented Framework for Multi-Task and Multi-Domain Scenarios](https://arxiv.org/abs/2307.13528)*。本地arXiv:2307.13528v2（2023-07-26）PDF共25页：1–12页全部正文、13–15页参考、16–25页完整提示和成功/失败案例逐页读；目视核对PDF8表3–4、PDF9表5、PDF12表6、PDF20/22/25失败案例。作者[FACTOOL仓库](https://github.com/GAIR-NLP/factool)当前README、支持任务、依赖和输出结构静态查看；仓库已有97次提交且后来继续加入Halu-J，未将当前main当作论文时固定实现。检索还确认论文后来以COLM 2025会议版发表；本笔记的实验数字和页码严格对应资料库中的v2，若综述引用正式版须另核改动。未调用旧GPT/Serper/Scholar API或执行不受信代码，本次没有声称重现表5。

## 五阶段框架和四种“事实性”的不可互换性（PDF1–6）

统一流水线是：从生成响应抽claims→每claim生成工具查询→调用工具→收集证据→让规则/LLM判断agreement。统一的是**软件接口**，四任务的真值对象并不统一：

- KB-QA：小于15词、消解指代的ACU，以Google Search/Serper snippets作证据，再由ChatGPT/GPT-4判断世界知识支持。
- 代码：整段code block为一个claim；LLM生成3个测试输入和3个候选解，候选解在测试输入上的多数输出成为pseudo-gold，待测程序匹配全部伪测试才算True。
- 数学：只抽取已知实数间的显式算术式，LLM改写成Python比较；任一算术式False则响应False。
- 文献综述：只抽`(paper title, year, authors)`，以题名搜Google Scholar第一条，题名/年份不区分大小写exact match，作者用LLM判断是否为检索作者子集。

因此“multi-task factuality”包含世界事实支持、有限测试功能正确、局部算术相等和引文元数据存在四个不同判据。代码通过合成测试不等于对所有输入满足规格；数学每步算对不等于建模/推理正确；引文元数据正确不等于综述对论文内容、相关性和结论描述正确。综述应把FACTOOL视为**任务适配的工具编排框架**，不能把四项F1当同一事实性量尺做平均。

## Claim抽取的“精确率/召回率”实际测量（PDF5、8、16–18）

KB提示要求“extract every claim”、每claim<15词且self-contained，但few-shot示例主动抽取大量**嵌套、重复**命题：同一网球句被拆成“6-1,6-4”和“6-1,6-4 on Saturday”；“last photos”和“last 34 photos”并列；“reaches final”和“for first time”再并列。一个细节错误会让父子claims同时失败，响应级“任一错”概率和claim数随拆法改变。提示称要resolve coreference，示例后两条仍用`Berdych`而非完整姓名，规则执行不完全一致。

RoSE 100个参考摘要/527个人工ACU用于抽取评估。论文不是一一匹配后计算集合precision/recall：对机器claim取与任一gold的**最大文本相似度**再平均，反向类似列为recall；一个gold可被多个重复机器claim反复匹配，也没有对遗漏/冗余做离散惩罚。表4 ChatGPT ROUGE-1 P/R/F1 `.7770/.8285/.7836`，注意`.7836`也不是普通调和均值：`2*.777*.8285/(.777+.8285)≈.8020`；GPT-4 ROUGE-1 P/R`.7394/.8758`的调和约`.8019`而表给`.7860`。很可能是逐样本先算F1再平均，不能由汇总P/R复算；必须称“基于最大相似的平均分”，不等同claim边界检出P/R。BERTScore ChatGPT/GPT-4 F1几乎相同`.7174/.7175`，不足以证明“抽出所有可核事实”。更应人工评估原子性、完备性、去重、指代正确率。

## 数据、正类和分母（PDF7–9）

表3：KB FactPrompts 50响应`23 factual:27 nonfactual`、233 claims`177:56`；HumanEval 164响应/claim`109:55`；GSM-Hard 100响应`47:53`、284 claims`246:38`；科学综述100响应`10:90`、186 claims`33:153`。RoSE 100/527仅用于抽取。GSM-Hard只抽最终答案为正的100题，以避“负苹果”等不合逻辑样本，这是人为条件化的子集；不能代表完整GSM-Hard。科学提示由作者self-instruct生成，且只有10%响应全真，极端类不平衡使accuracy很容易被多数类影响。

表5中R/P/F1以**factual=True为正类**，不是以hallucination/error为正类。可从整数反推：科学响应100条仅10正，GPT-4 FACTOOL recall90%=9/10、precision100%=9/9、accuracy99%=99/100；即判9个True、91个False。KB GPT-4 FACTOOL在23个True中TP14（14/23=60.87% recall），总判True16（14/16=87.5% precision），TN25，故accuracy(14+25)/50=78%。数学响应TP45/47=95.74%，预测True65所以P=45/65=69.23%，TN33/53，accuracy78%。这些整数组合与表完全吻合。

论文称self-check“prone to false positive and less sensitive in detecting errors”，实际是它更常输出True，故对**factual正类**precision低、对**错误负类**特异度低。若读者把“错误检测”当正类，会误读R/P。综述应同时给error为正类的sensitivity/specificity或混淆矩阵。论文没有置信区间/多次API抽样；50或100响应下若差几例，F1可显著变化。

## 表5逐任务结果与真正支持的结论（PDF8–12）

GPT-4 FACTOOL claim/response F1：KB `.8909/.7179`、code `.9211/.9211`、math `.9897/.8036`、scientific `.9524/.9474`。与GPT-4 3-shot self-check响应F1分别`.5714/.8526/.7059/.2154`；工具在这四个小型测试上整体更高，科学元数据检索优势最大。KB中ChatGPT FACTOOL响应F1`.5263`，反而低于ChatGPT zero-shot self-check`.5490`，论文承认给足证据后判断仍可能推理错。表5没有显著性检验、运行成本、API失败率或无结果coverage；当年GPT-3.5/4结构化JSON经常失败并**重新运行无效样本**，表8脚注承认。若只保留成功格式的重试结果，会改变成本与失败分布，复现实验须报告每阶段重试数。

response=True定义为全部claims True。claims越多，响应全真概率机械下降；代码一claim所以claim/response完全相同，KB/数学/科学多claim则response F1显著不同。跨任务响应F1不能直接比较。科学任务响应10正/90负，99% accuracy与94.74 F1看似极高，主要说明Google Scholar首条+严格metadata很会识别这个构造集中的虚构引用，不验证科学内容。KB Search snippets可能复制同源错误、缺时点和出处质量；“multiple evidences”可能只是重复同一snippet，PDF20 fortune cookie示例就出现两条完全重复证据。

## 三个工具模块的独立失败机制（PDF10–11、20–25）

**KB证据不等于裁决：**PDF20 ChatGPT把“现代fortune cookie在美国发明”标False，但它援引Makoto Hagiwara在San Francisco制作，推理自身反而支持美国起源；把“Sotomayor是女性最高法院大法官”标False只因没额外提“首位拉丁裔”，把**不完整**错当命题虚假。PDF23 GPT-4对`Jupiter less dense than Saturn`读到Jupiter1.33、Saturn.687仍判True，是比较方向错误。对Jupiter1.33 vs1.326却把作者gold True判False，显示精度/舍入规则不稳定。PDF20 `Everydays sold for $69m`被标False因证据$69.3m，虽然另一snippet正说$69m；精度容差和年份/“当前最高”时点没有预先定义。

**代码伪金会共错：**3个候选解来自同一模型，错误相关而非独立。PDF22 HumanEval/36题要统计数字7**出现次数**，ChatGPT多数候选只按含7的整数计一次，候选与待测代码同错，于是将真实失败代码判True；GPT-4候选恰生成正确计数才判False。PDF24 HumanEval/79所有候选和目标都忘了0应输出`db0db`，三合成测试包含0却多数伪金为`dbdb`，错误无法发现。测试集覆盖、候选多样性和模型相关性才是关键，不能把多数票叫可靠oracle。

**数学只查局部算术：**PDF25长题错误地把“每第二只杯子折扣”建模为未知x并最后令x等总数，但列出的算术恒等式都能在某个x下成立，于是工具漏掉整题推理错；作者明确承认。rounding例`60444034/12=5037002.83`按常见两位小数可接受，却用1e-9严格比较判False。抽取提示本称“不包含变量”，失败案例claims却包含`x`并甚至把字符串`5x==5x`判True，说明实现/提示没有可靠执行规则。Math claim F1`.9897`与response F1`.8036`的巨大差距正反映局部算术易、全局解题难。

**科学检索只查身份证：**PDF25真实MDMA论文因题名规范化/缩写判错，真实GPT-2报告因作者匹配判错。论文用标题第一条exact match，标题变体、预印本/会议年份、et al.、重名都会误报。反之，真实存在但与综述论点无关或被曲解的论文仍判True。

## “现代聊天机器人排行榜”不宜作为黄金结论（PDF12–13）

Exp-III仅60 prompts：KB30、code10、math10、science10。用上述GPT-4 FACTOOL当“gold evaluator”，却其响应F1在KB仅71.79、数学80.36；没有在排行榜这60条上人工复核。GPT-4既被评又担任查询/裁判，可能有同模型风格、知识或自偏好优势。表6响应准确率GPT-4`43.33%=26/60`、ChatGPT`36.67%=22/60`、Claude`26.67%=16/60`、Bard`33.33%=20/60`、Vicuna`21.67%=13/60`，每一题就是1.67百分点，无置信区间，4–6题即可改变相邻排名。

“weighted claim-level accuracy”不是按实际claims pooled，也不是自然使用分布：人为权重KB 3/6、其余各1/6，对每域claim accuracy取加权平均。实际KB响应平均claims更高，且模型回答长度GPT-4 196.83、ChatGPT144.05、Claude208.70、Bard263.77、Vicuna207.13；全claim正确的response accuracy强受长度影响。30:10:10:10权重来自“KB最常见”直觉而非使用日志。故可报告“在作者60提示、作者权重和FACTOOL代理裁判下GPT-4最高”，不能写“GPT-4事实准确率75.60%”作为一般模型属性。

## 复现与进一步研究问题

1. **固定正类与全混淆矩阵：**从论文时commit/保存预测逐任务重建TP/FP/FN/TN，分别以factual和error为正类报precision/recall、specificity、balanced accuracy、置信区间；分开claim、response和无解析结果，不让“error detector”的文字与True正类指标混淆。
2. **逐阶段消融和coverage：**人工gold claims→gold queries→gold evidence→gold agreement逐个替换，量化抽取漏检、检索缺证、证据冲突、裁判推理错各占多少；报告API失败/重试、Search/Scholar无结果率、token/美元/延迟。Search证据保存URL、时间、去重与来源信誉。
3. **代码oracle升级：**与HumanEval原始隐藏tests比较；扩大property-based/boundary tests，引入不同模型/符号执行生成oracle，测候选解错误相关性。特别固定/复现36、64、79，验证同错多数票的漏检率。
4. **数学区分计算与推理：**claims至少分方程建模、代数变形、算术和最终答案，符号变量用CAS/约束检查；预先规定舍入容差、单位和有效位。用PDF25 Kylar例测试是否能指出“x取值/计价逻辑”而非只验证局部等式。
5. **引文与KB时点：**文献题名规范化、DOI/作者ID/预印本版本；再核论文是否支持综述中的具体claim。KB用支持/反证/缺证三类和时间戳，禁止把缺少额外细节判False。
6. **排行榜独立人评：**对60题及更大分层集匿名人评，裁判模型与被评模型分离；匹配长度/claim数并按真实任务分布加权，报告每题paired bootstrap。当前只完成PDF和官方README审计，没有把当前仓库运行结果冒充原表复现。

**综述可用结论：**FACTOOL清楚展示了claim抽取、工具查询和证据裁决的可组合架构；在作者构造集上，GPT-4版对KB/代码/数学/引文的响应级factual-class F1为71.79/92.11/80.36/94.74，整体超过自检。该结果证明任务专用外部工具很有价值，却不证明一个统一事实性判据跨四任务成立；工具oracle、claim粒度、正类方向、回答长度及把代理裁判当黄金排名都必须单独审计。
