# I059 Self-Checker：模块化事实核查与BingCheck的标注、检索瓶颈

## 来源与核验范围

Miaoran Li、Baolin Peng、Michel Galley、Jianfeng Gao、Zhu Zhang，*Self-Checker: Plug-and-Play Modules for Fact-Checking with Large Language Models*，Findings of NAACL 2024；本地 arXiv:2305.14623v2（2024-04-01），PDF19页，逐页阅读正文、表1–9、附录提示与数据例。[正式出版页](https://aclanthology.org/2024.findings-naacl.12/)；[作者仓库](https://github.com/Miaoranmmm/SelfChecker)固定commit `d33157db37c4475ae1b9a1df4907e7368b35e995`，本地`Reading_Notes/qa/I059_official/I059_sanitized.zip`和`provenance.json`。仓库中34字节`subscription_key.txt`疑似凭据，已从本地ZIP剔除；只静态读源码，未运行Azure、Bing或CUDA评测，论文分数没有独立重现。

## 研究对象、模块及定义（PDF1–3、13–15）

框架以policy agent依次调用claim processor、query generator、Bing/Wikipedia检索、evidence seeker、verdict counselor。BingCheck的四类为supported、partially supported、refuted、not supported。操作上，任何证据矛盾即refuted；无矛盾且至少一条支持则supported；只证实一部分则partially；无支持/反驳才not supported（PDF5）。这仍是**给定检索证据的支持关系**，没有外部独立世界真值保证。尤其“至少一条支持”忽略其他未取到的矛盾证据；实际做法是每claim Bing top3，然后抽证据句。

附录提示强调“复制证据原句”“部分不支持要保守”，但主文脑病毒例子显示模型把证据只证实`1986`及两兄弟误读为也证实精确日期`19 January 1986`（PDF8）。因此分解、证据选择、推断每步都可能错；中间产物可观察不自动意味着可解释性或真值可靠。长文本先抽check-worthy claims，未被抽出的事实不进入分母，响应级准确率会漏看这种遗漏。

## BingCheck构造与质量（PDF4–6、17–18）

ChatGPT模拟好奇用户，Bing Chat生成396条长答，平均391.5 token；人工辅助抽出3840个可核验claim，平均9.7/答、26.3 token/claim。作者使用Self-Checker先给候选claim、证据、标签，再由一名合格MTurk工人修改；之后每条由三人多数投票评审。评审认为381/396回复的claim集合全面且可核，94% claim的证据适当、96% verdict相对标注证据正确。**评审是对由系统预选的候选标注作质量检查**，不能证明未检索到的事实全部覆盖，也不能将96%理解为真实世界标签精度；没有报告每项独立从头标注的一致性、每类错误矩阵或标注者专业核查范围。预填候选可能锚定工人，训练/评测同流程还会造成自动系统与“金标”相关。

表2的`55.0`证据句/response、`6.2`/claim只对三种有证据标签计算，不能当全体平均检索负担。附录个案包含“first artificial heart”多重时间/类别叙述（PDF17–18）；一个页面片段若只写`first permanent`，不能自动支持泛称`first`。这是适合做粒度和限定词压力测试的典型例子。

## 主要结果与口径（PDF7–9）

BingCheck表4**response级**准确率：standard19.4、CoT15.7、ReAct21.0、Self-Checker63.4%；证据句F1 45.0、precision30.5、recall86.1。高recall来自选很多证据，precision较低；不能只报召回当作核查质量。相比ReAct的42.4点提升成立于作者特定提示、检索、长度和API调用设置；没有成本相等对照或多次seed区间。标准/CoT倾向直接支持文本是弱基线，但并非所有无检索方法都必然如此。

FEVER表5，Self-Checker accuracy56.7、严格FEVER score47.9、证据F1 47.5（P75.3/R34.7）；BEVERS accuracy80.2、FEVER77.7，差23.5/29.8点。表5 Verify-and-Edit的53.9 accuracy使用Google搜索，知识源不同；不应把53.9与56.7当全受控同源对比。WiCE表6 Self-Checker label F1 47.7、accuracy71.5，证据F1 60.5（P71.4/R52.5）；微调T5-3B F1 65.3、accuracy77.1，证据F1 67.4。三数据集指标分别为response准确率、FEVER联合证据得分、WiCE类别F1，不能横向排序系统“幻觉能力”。

## 金标消融的真正含义（PDF8–9、19）

BingCheck表7从全流程63.4，给gold claims64.3，另给gold docs仍64.3，给gold evidence sentences67.2；最多只增3.8点，留下verdict瓶颈。*但这些并非独立模块贡献的严格估计*：金标替换会改变下游输入分布，且标注证据由本系统初选后人工修正。查询/检索“不是主要瓶颈”的推断只在这个小数据与top3搜索快照成立。

附录FEVER全test表8与主表5不是同一规模：无金标FEVER score51.3/accuracy62.7；gold docs64.1/72.8；gold句score81.20。不能把主表47.9与附录81.20直接算同一样本提升。WiCE表9出现不同消融行：不分解（无gold）F1约35.6、accuracy35.8、证据F1 23.5；分解相关行F1 64.4、accuracy68.4、证据F1 42.1；带gold evidence有78.7等。PDF提取后表格列/行复杂，综述引用精确配对前需复核版面；较稳妥结论是分解和oracle证据明显改终点，而verdict仍有错误。论文对“primary bottleneck”的归因须限于对应gold条件与数据集。

## 官方仓库静态审计与复现边界

固定版本ZIP约121.9 MB、462个保留成员；`bingcheck/`有401个JSON，而论文记396条，需要按样本ID核对额外文件性质与实验筛选。README把`get_data_and_resources.sh`误写成`get_data.sh`，预处理脚本列表亦与实际清单不一致；“Evaluate Results”三项均写`evaluate_fever.py`，但仓库分别有BingCheck/WiCE脚本，按README照跑会错。`experiment_bingcheck.py`当前源码`TEMPERATURE=0`、Azure`text003`，论文PDF7称temperature `.2`，版本/设置不符；需锁定论文实际执行提交与配置，不能把当前代码输出视为论文原实验。

`evaluate_bingcheck.py`的证据分数使用MiniLM句向量余弦阈值`.8`匹配，而正文说与gold句计算F1，未清楚交代语义匹配细则。源码将每response的claim标签按`refuted`优先、再`partially supported`、混合`not supported`→partially、其余→supported聚合；漏抽claim仍可能被标为supported。代码`evidence_macro_precision`对空预测集合返回1，`evidence_macro_recall`在空矩阵也返回1，需检查实际调用中空列表行为和指标偏差；`evidence_similarity`固定`.to('cuda')`，CPU不能直接复现。`experiment_bingcheck.py`对选证据调用两次模型（分析、再抽句），逐claim verdict又两次，长回答至少数十次API调用，论文只定性谈高成本，未给总token/延时。

## 作者限制与可执行研究问题（PDF10）

作者承认过时证据可误判、混杂来源未经筛选、多次LLM调用高成本、prompt敏感和人工标签主观。可进一步做：

1. 独立从原长答双人抽claim，统计系统候选遗漏率、错误拆分率，并报告response级覆盖与claim级微平均性能。
2. 对Bing top3逐条记录发布日期、来源可靠性、互相矛盾，比较带时点/来源筛选、无筛选两政策。
3. 固定同一检索结果和API token预算，替换单一模块，进行配对消融；报告调用数、成本、P/R与最坏子群。
4. 做“部分支持”最小对：精确日期、数字、否定、限定词、`first` vs `first permanent`，评估过度支持率。
5. 区分自动候选锚定的人类修正标注与独立人工核实金标；公开逐类混淆、一致性与额外5个JSON的来源。
6. 对No-evidence或API失败明确拒答，不把默认`支持`作为安全回退；审计检索与选句异常路径。

## 综述定位

本篇是**可观察的模块化长答事实核查管线和新数据集**，优势在长答claim拆解与中间结果，实证Self-Checker BingCheck response准确63.4优于其prompt基线，仍受低证据精度、verdict过度支持、数据标注锚定与调用成本限制。接I048程序规划、I046时点web检索、I053多证据充分性、I058答案扩展确认偏差、C07 FActScore原子事实评价；不可将FEVER、WiCE与BingCheck不同指标拼成统一排行榜。
