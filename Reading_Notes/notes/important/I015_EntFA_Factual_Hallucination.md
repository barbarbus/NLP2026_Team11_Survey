# I015 · Hallucinated but Factual! Inspecting the Factuality of Hallucinations in Abstractive Summarization

Meng Cao, Yue Dong, Jackie Chi Kit Cheung，ACL2022，3340–3354；https://aclanthology.org/2022.acl-long.236/ （以资料库PDF题名为核验对象）。本地15页PDF。源码 https://github.com/mcao516/EntFA 。

## 阅读与核查范围

已细读正文第1–9页和全部附录第12–15页；第9–11页主要参考文献。目视核验第6、7、9页Tables3–8。下载官方固定commit `e6f857ddf0ba43a7bc5e6e0b40cfaada99f79583`，独立清点train/test JSON，静态阅读train_knn.py、evaluation.py及概率/输入构造utils.py。未执行作者代码、加载pickle、下载大型checkpoint或训练模型。独立批次缩放反例已运行，但不是原模型性能复现。

## 1. 研究问题及对综述的作用

摘要中来源未明确支持的实体不一定现实错误；正确背景信息可改善理解，例如将只有姓的Juncker补全姓名与职务。作者提出ENTFA，分别判断entity是否由来源支持、是否世界真实；并用分类器作离线RL奖励减少非事实实体。本文是C01/C04“factual hallucination”讨论的原始实证来源，应优先引用，而非只复述综述概念。

范围限制很重要：研究的是XSum/BART生成摘要中的实体及其属性，不是任意长文全事实核验；关系、否定、因果、数值计算和跨句含义可能未被NER完整覆盖。已包含的人名地名日期数值，不意味着同时评估所有关系真值。

## 2. 标签定义与人评设计

标注先看实体在“所生成语境”里能否由来源直接推出；能则Non-hallucinated，不能则查Wikipedia/Google判断Factual hallucination或Non-factual hallucination。实体在来源出现但被放到错误语境归Intrinsic hallucination（第3–5页）。多属性实体分开标，NER漏提由人补齐。

关键边界：找不到网上证据证明或反驳，也标Non-factual，而不是Unknown。故“非事实”混合已证伪和未核实，不能直接等同客观错误；搜索覆盖、时效和核验者能力影响标签。Intrinsic55个随后从主实验排除，这会使实体重合特征在剩余任务特别有效；不能推广为对来源实体关系误用也已可靠识别。

XENT由800篇BART摘要、2838个实体组成。作者两人加三名研究生；10对先pilot并讨论；按指南标注，报酬20美元/小时，伦理审批已报告。800实体重叠子集Fleissκ=.809、四类对多数类agreementμ=.931（第5、12页）。κ不是对所有实体全重标，也不保证网上真值正确。

Table3：Nonhall1921、Factual hal441、Nonfactual421、Intrinsic55，总2838。源外两类441/(441+421)=51.16%事实；若含intrinsic，441/(441+421+55)=48.09%。所以“超过一半幻觉实体为真”须限定排除intrinsic的源外集合，不能说所有类型一概超过半数。约30%实体不支持也只是特定BART/XSum样本，不是所有LLM发生率。

## 3. 先验/后验特征并非已校准的真值概率

给定summary中实体e，ck为去掉e后的其余上下文，包含右侧文字。Prior来自预训练masked LM：P_MLM(e|ck)；posterior来自以source+masked summary微调的CMLM：P_CMLM(e|ck,S)。多token实体按自回归概率连乘。两个模型本身不同，不能把它们当同一联合分布严格贝叶斯更新，也不是输出“世界为真”的后验概率。

假设非事实实体在加source后仍缺证据，所以prior/posterior都较低；但背景事实可由训练知识补足，即便来源没写也有高posterior。特征另加大小写无关的字面实体重合，KNN做两种二分类：hallucinated vs not，factual vs nonfactual。KNN虽不需要梯度优化仍依赖有标签实例、特征标准化和邻居数，是监督方法，不能因作者称no training就列为完全无监督。

实体概率乘积会受token数量/词频影响，生僻真名可能低分，常见错误可能高分；需要按长度和实体类型分层。完整summary左右语境可能提高可预测性，也可能使模型沿错误叙事补出错误实体，不能从高概率逻辑保证正确。替代CLM只看左文，CMLM利用右文；比较时输入信息量与目标分布不同。

## 4. MENT转换及泛化证据边界

将Maynez摘要级/跨度标签映射到实体：factual summary中的实体视为真；nonfactual summary中落在extrinsic span的实体假定不真；再排除来源出现的实体，减少整句跨度导致的误标（第5–6页）。作者明确承认转换噪声，语义真实不能由“落在span”保证；这不是独立重新人工核验的实体金标。

XENT训练→MENT测试改善说明一定的数据迁移能力，但仍来自XSum体系并受标签转换规则影响，不能称跨领域、跨语言或现代LLM通用性。30%测试样本的表述应结合发布文件看实际是文档层拆分，而非先假定实体随机切分；下文已检查相同source是否重叠。

## 5. 实验结果：把两个任务与三种评价口径分开

Table4第6页：hallucination accuracy92.93、macro-F191.73，与简单overlap完全相同；factuality accuracy90.95、macro-F181.82，高于Zhou基线85.76/75.07。不能把81.82说成全部幻觉检出F1，也不能说本法在hallucination任务严格胜过全部基线。论文结论“outperforms”需以实际表格限定。

Table5 MENT factuality78.48 accuracy、60.23 macro-F1；绝对F1明显低于XENT。论文报告10-fold cross-validated paired t-test p<3.27e−5，但本组未获得预测重算、检查fold分组、选择超参数和多重比较，不自行提升统计结论的外推范围。

Table6第7页：FRANK的partial Pearson .183（p<1e−8），Wang数据PCC .268，优于该表引用基线，但相关强度绝对值有限；统计显著不等于高度相关或可部署。不同列是偏相关与普通PCC，且基线数值从原论文引用，未统一重跑。摘要级分数为所有实体factual-class置信的最小值，回答越含更多实体越可能被单个低分拉低，需分析长度影响及零实体情况。

Table8消融：去posterior使factuality F181.82→70.30（−11.52个百分点）；去prior80.12、去overlap77.18。hallucination去overlap91.73→74.83（−16.90），显示源支持任务主要依赖重合；这与排除intrinsic后样本结构一致，不证明字面重合在完整幻觉范围足够。

附录Table10三分类采用leave-one-out：nonhall F195.05、factual hallucination70.88、nonfactual62.89，不能将leave-one-out直接与Table4测试集二分类对比。Figure8单信号AUC：MLM.62、CMLM_XSum.91、CLM_XSum.88；这是实体概率判事实的ROC，不是全部KNN整体性能，也不是.91 accuracy。

## 6. RL应用：有收益信号，但部分由自己的指标打分

对标注为nonfactual的实体token给−r_nfe，其余用MLE posterior概率奖励；用Pang–He离线RL近似importance weight，参考摘要作为行为轨迹，不等于从环境探索获得无偏奖励。γ=1、30000更新、slow policy Polyak=.01，CMLM训练15000步、4×32GB V100（第4、12–13页）。这些是作者成本，不是本组已运行。

Table7：MLE R145.1/DAE34.6/ENTFA factual82.8；r=2时R144.6、DAE37.3、factual90.1，r=4时R143.0、DAE40.8、factual92.5。事实性提升伴ROUGE下降，需权衡。与loss-trunc c=.7的R142.7/DAE38.8相比r=4略好，但与所有设置不能笼统说质量各方面都最佳。

ENTFA既作reward又作评估，可能有指标利用；FEQA/DAE是额外来源忠实指标，不是独立完整世界事实金标。Novel unigrams/bigrams及ENFS说明不是纯复制，但不能证明每个源外实体真实，也不能单凭它们排除更隐蔽的reward hacking。附录噪声实验部分样本量随噪声量变大，固定50k区域与100k点应分开，不把整个趋势都解释为只改变噪声率。

## 7. 已实际完成的官方数据审计

官方快照ZIP和provenance保存在../../qa/I015_official/，未见LICENSE文件，不标注为任意可再发布许可；代码内部pickle未加载。

audit_entfa_data.py独立解析JSON：

- train460篇、1632实体：nonhall1093、factual270、nonfactual230、intrinsic39。
- test240篇、843实体：nonhall583、factual118、nonfactual134、intrinsic8。
- 合计700篇2475实体，与论文800/2838不相同；不能未经证据猜测缺失100篇是validation或其他特定原因。
- train/test各source完全重复数为0、跨集合精确source重叠0；只支持没有完全相同source，不排除近重复/相同事件/预训练见题。
- SHA与全部计数见count_audit.json。脚本train_knn.py只映射前三标签，Intrinsic跳过；与论文排除该类一致。

## 8. 源码发现与独立反例研究

train_knn.py的build_classifier按训练特征各列std缩放后fit，但infernece函数又按整个测试批次的std重新缩放。evaluation.py同样重新估std，而保存pickle只有classifier，无训练scaler。这样训练/推理坐标体系可能不同，同一输入得分依赖其他测试样本的分布；这是分布级使用测试输入，不是使用测试标签泄漏，不能把两者混称。

已运行probe_entfa_batch_scaling.py：构造合法[0,1]二维概率特征，训练点(0,0)、(.2,.2)，训练缩放后(0,0)、(2,2)。固定查询(.1,.1)，与(.5,.5)组成批次时缩放为(.5,.5)，最近训练点0；换伴随点(.12,.12)则缩放为(10,10)，最近点1。证明批次缩放原则上会改变最近邻判断。此例是2维、1近邻解释实验，不是原3维k30模型的准确率复现，不能据此说论文F1下降多少或结果失效。

其他静态差异：build_classifier(n=30)函数实际硬编码n_neighbors=30，参数n未使用；论文MENT/图示k20不能仅调用此参数复现。README命令用--train-path而argparse定义--train_path等，下划线版本需对照实际脚本；不应承诺照抄README即可运行。get_probability确实按token概率相乘，支持长度敏感性分析。无实体时evaluation会追加空样本，但最后汇总按entity数，不能解释为无实体回答自动事实正确；异常AssertionError时某样本不追加，应报失败覆盖率。

这些问题尚未修改作者资源；保留原ZIP不变以便复核。若后续复现，应另建适配目录，保存训练scaler、冻结数据版本、分别报告原实现与修正版，避免静默修复后仍称原样复现。

## 9. 研究问题及下一步验证

Q1：未知被当假会怎样？已有指南明确此映射。可将未找到证据的实体重标Unknown，再比较三类/二类表现，特别检查新近/长尾实体；未开展人工重标。

Q2：高posterior是否只是常见名与实体长度？源码乘积支持潜在长度效应，但未做实证分层。可按token数、训练频率、实体类型匹配真假样本，加入length/frequency baseline并测增益；不能从原散点直接证明模型学到了真实性。

Q3：RL提升是否对独立世界真值成立？需在各生成系统分层盲抽实体、独立搜索判真，并测关系/非实体错误；不把ENTFA奖励分数自增当最终证明。当前FEQA/DAE提供部分异源指标佐证，但范围仍有限。

Q4：缩放修正有多少影响？已给原则性反例，待冻结特征和预测后用同一训练scaler重计k20/k30结果，按文档配对bootstrap。现未下载checkpoint或计算原特征，不报告量化影响。

Q5：加入intrinsic后模型是否仍好？排除39/8等实体的代码已确认，需重构完整标签任务并加入换关系/错语境案例，测重合baseline误导；尚未做模型运行。

## 10. 研究地图位置

对应核心C01/C04的SF/WF边界、C02事实性/忠实性、C07证据与聚合、C10概率信号、C14人评可靠性、C16输入蕴含。主类“实体概率与世界事实性”，次类“源外真实标注、原始人评数据、指标作奖励”。适合在综述解释支持性≠真实性及probability≠truth，并作为代码/数据可重复性问题的具体案例。

英文概括：EntFA separates source-unsupported but factual entities from non-factual entities using masked-language-model probabilities and lexical overlap. Its evidence is limited to entity-level summarization, with intrinsic errors excluded, and its reported gains require careful separation of classification, correlation, and reward-based generation results.

## 未完成事项

后续交叉核查补充：I007 FRANK官方在2021-07-20修正BERTScore结果，更新版必须区分reference与article输入；独立重算BERTScore P Art的分组控制Pearson约.271，reference P约.158。因此本笔记保留EntFA所引用/报告的历史对比值，但不能据其弱相关数字概括所有BERTScore版本。I035整摘要真假与本篇实体真假单位不同，其“大多数幻觉不真实”也不能与这里实体层51.16%直接作相反结论。详见I007/I035笔记及第四阶段综合。

checkpoint、原特征、预测和源码运行未复现；数据缺失100篇原因、标注Unknown重计、近重复和模型训练污染未查；附录图中非主数字未全目视核验。以上不计为已完成实验。
