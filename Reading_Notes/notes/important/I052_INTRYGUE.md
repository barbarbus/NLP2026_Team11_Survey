# I052 INTRYGUE：用归纳头的注意力汇聚门控熵，机制证据与筛查泛化仍需分层验证

## 来源、版本与核验

Alexandra Kuleshova、Andrei Volodichev、Daria Kotova、Alexey Zaytsev，*INTRYGUE: Induction-Aware Entropy Gating for Reliable RAG Uncertainty Estimation*。本地为arXiv:2603.21607v3（2026-08-31），PDF19页；另核对[EMNLP 2026正式条目](https://aclanthology.org/2026.emnlp-main.2236/)（50891–50909）。正文、表1–10、图1–14、机制实验、标签与实现附录逐页阅读。作者[官方仓库](https://github.com/kuleshovaai/intrygue)固定在commit `49586338e62e6782743a50c73e8913582db4acbf`，237,999字节ZIP、SHA256与清单见`Reading_Notes/qa/I052_official/`。未运行六个4B–13B模型；以下是纸面复算与源码静态核查。

## 评价目标和机制假设（PDF1–5）

评价对象是给定检索文本的**回答级任一不忠实内容**，不是客观世界真值；假文档被忠实复述会得到低风险，作者在限制与风险部分明确承认（PDF10、16）。白盒要求获得生成时注意力和每token logits。

作者提出两条相反路径：归纳头通过从context复制模式帮助正确答案、降低预测熵；同时它可能激活最后一层的“熵神经元”，通过最终LayerNorm/RMSNorm分母使logits平坦，部分抵消熵降低。归纳头在重复随机序列上按正确偏移的attention质量排序；“熵神经元”按输出向量范数大、unembedding投影方差低确定。

SinkRate把回答token各行对某prompt/回答历史列的attention累加，按该列可被多少回答token看到作归一，再取最大列值；较高值解释为注意力集中到无用汇聚token、归纳复制较弱。对每个样本求前k归纳头的SinkRate集合S，以及生成token熵集合E，门控分数`f(S)×g(E)`。长回答版`min(S)×max(E)`，短答版`mean(S)×mean(E)`；高SinkRate保留熵，低值下调熵。无外部裁判、无额外生成，但须白盒前向和可能较贵的attention矩阵。

这个乘积并不是经过概率校准的“不正确概率”：`min(S)`受头数影响，`max(E)`受长度和词表概率分布影响，低SinkRate的正确复制与错误复制同样会压低分数。归纳头是机制代理，不直接验证被复制事实是否蕴含于可信证据。

## 机制实验：哪一层是因果、哪一层仍属解释（PDF3–5、14）

图2 MaxEntropy在MS MARCO/XSum四模型AUROC约.62–.66，分布重叠，说明单一熵信号弱。图4四个设置SinkRate单独预测AUROC `.67–.73`，Mann–Whitney p<1e−4；这只是关联，且不同样本长度、问答难度、词面复制可能共同变化。

图3a–b在CoQA中先选择**已答对且SinkRate最低三分位**样本，再mean-ablate前五归纳头：NLL和熵比随机五头更升，支持这些头对这一条件子集答案概率有因果作用。但效应是对条件样本与模型干预，不证明所有RAG正确答案都靠复制，也不直接证明最终语义答案翻错比例。随机头与归纳头的层位/范数是否匹配也需核。

图3c–f的SinkRate与前15个低LogitVar神经元最大激活负相关，支持共激活关联。图5a消融归纳头后神经元激活范数下降；图5b消融30个熵神经元后预测熵下降。它们分别支持两条局部干预链，却未给出同一token上严格的“归纳头→神经元→熵→最终误报”中介分解。要证明第二条解释造成误报，需要在固定正确答案和prompt的同一样本上做神经元路径patching、重新测检测FPR，并控制其他隐藏状态变化。附录图9–10变化组件数仍见同方向，增强稳健性但不补中介证明。

图6四象限很有信息：Llama2 CoQA中熵判错、SinkRate判对的284条，熵准确仅23.8%、SinkRate76.2%；Qwen相应135条，熵40.7%、SinkRate60.0%。但两条阈值都在同一validation集按F1选择，四象限解释是条件在代理预测上的后验结果，不可当成独立的因果纠错率。相反象限也存在：Llama2的57条熵52.6%对、SinkRate47.4%，Qwen的66条熵80.3%对、SinkRate19.7%，门控可能恶化特定子群。

## 数据、标注和分母（PDF12–14）

四任务：RAGTruth MS MARCO长QA、CNN/DM摘要；作者自行生成的CoQA对话QA、XSum摘要。后两者生成温度1，并用GPT-4o判响应级幻觉；各模型CoQA 661–1525条、XSum650–750条，幻觉率CoQA14.6–34.7%、XSum24.3–39.4%（表3），不存在统一平衡先验。图4/表1–2的AUROC是回答级排序，不给固定阈值下的precision/recall或风险覆盖。

CoQA回答中位数2–5词，而RAGTruth MS MARCO为93–168词、CNN/DM77–90词；XSum32.5–55词（表4）。因此min/max相对mean的提升可能部分来自极值随长度变化，不必全部归因于机制。CoQA约8.2–12.7%为yes/no类回答（表8）；在该子群，INTRYGUE相对LN-Entropy误报率反升：Mistral `.40 vs .38`、Llama3.1 `.43 vs .31`，是复制机制不适用的明确反例。

100条CoQA由三名组内成员人标，pairwise agreement均值accuracy .807、Pearson .628；只用三人一致子集当GPT裁判的gold，GPT-4o五prompt平均准确.808（表5–6）。这不能推断全体争议样本的准确性，更无XSum人工同等验证。作者另让Gemini 3.1 Pro Preview重标Gemma CoQA的703条，与原GPT标签641一致、62不一致（91%一致）；表7 INTRYGUEmean AUROC均为.76、min-max .73→.71。两位模型裁判的高一致不是人工事实真值，且仅一个模型×任务。

## 主表复算与限定（PDF6–8、16）

RAGTruth表1：MS MARCO三模型min-max `.77/.72/.73`，相对MaxEntropy `.67/.65/.62`分别高.10/.07/.11点；CNN/DM `.69/.60/.60`，其中Llama2-7B的mean `.62`比min-max `.60`高，Llama2-13B多基线也在`.62`，故“长文总应min-max”有例外。Mistral MS MARCO max-prob `.75`是强基线，.77对.75仅+.02点，结果波动±.03/±.04。

CoQA表2 mean六模型 `.82/.79/.81/.81/.80/.76`；Mistral LN-Entropy `.83`更高，Llama3.1 LN-Entropy `.81`持平而Semantic Entropy `.82`更高。XSum min-max六模型 `.73/.66/.63/.66/.68/.62`；Qwen ReDeEP `.69`更高，Gemma ReDeEP与Semantic Entropy `.62`持平。论文“多数设置具竞争力”合理，不能说每项最佳。

表10仅选六格与单独SinkRate/MaxEntropy比，乘积每格较二者高，支持信号互补。但未比较更简单的加权线性和、双特征逻辑回归（同验证量）、条件重标定，也未测独立信息贡献。图7、13、14未见非线性门控稳定收益，说明直接乘积足够实用，不证明它在所有标定目标上最优。

附录表9 dynamic以验证集长度阈值切换两版：Mistral MS MARCO `.84`高于固定min-max `.77`，但Llama2-13B CNN/DM `.57`低于`.60`，Llama2-7B XSum `.64`低于`.66`；“matches or closely approaches”须含这些反例。更严重的是表9 XSum的Llama2-13B min-max写`.73±.04`，主表2相同格为`.63±.05`，而dynamic `.63`；可能是排印错误，但不能擅自替换，应固定原始结果并请求作者/源码验证。

图8的20个Qwen XSum样本：LN-Entropy2.38s、INTRYGUE2.56s、Semantic Entropy69.78s。差0.18s是在特定硬件/样本规模下；完整attention的显存和长输入平方成本未展示。五次随机拆分、40/40/20 train/val/test（PDF16）会在不同折上复用样本，std不是独立总体置信区间。应按source分组且配对bootstrap。

## 官方源码静态审计与复现边界

`config/evaluation/default.yaml`：seed42、k5、val_size.5；外层`KFold3`用`StratifiedGroupKFold`按context分测试集（若传groups），更好地控制同context跨测试泄漏；但训练/验证由普通`train_test_split(... stratify=y)`分开，**不按context分组**，验证的头数选择可看到同一context的训练行。必须核实运行入口确实传groups，不能仅凭类存在断言所有表都分组。

`config/method/intrygue.yaml`默认sink=min、entropy=max、`n_heads_max:null`；`fit_hyperparameters`在有标签val上逐个头数算AUROC，选最高；故主表是验证调参，正文“training-free”仅指不拟合权重。固定k=5变体的图6a部分支持可零标签部署，但不可用调参主表代替固定k绩效。

`get_score`显式要求完整attention与logits，分数按响应token熵计算；源码先对prompt末token位置开mask，再把answer mask最后两个**数组位置**设0，注释称去除最后非EOS预测。若右填充样本较长，末两数组位置可能是padding而非真实末token；若回答极短，mask可能为空，mean会除零、max为`-inf`。应以原始token id/attention_mask的真实长度做单元测试，对CoQA 2–5词短答尤其重要。是否实际触发取决于批处理/tokenizer，未运行不能报既成错误率。

README明确当前预计算标注CSV尚未发布（仍写“camera-ready later”），论文AUROC与标签差异无法从仓库直接重算；附带的是框架、配置和生成/标注脚本。源码快照可静态复核公式和split，但不能当完整数据复现包。

## 后续研究问题

1. 同token反事实path patching测“归纳头→熵神经元→熵→误报”中介效应，并以匹配层/范数随机头做控制。
2. 在正确改写、反事实复制、伪证据与含冲突证据条件下，测低SinkRate是否会压低真实错误的警报。
3. 长度匹配和source-group条件下比较min/max、mean、加权和与校准回归；报告按回答词数/yes-no类型的FPR。
4. 重标全部自然回答的争议子集，以blind人工评估GPT/Gemini标签一致与裁判偏差；分别报告CoQA/XSum。
5. 核对表9 XSum Llama2-13B `.73`与主表`.63`的原始预测文件；公开每折AUROC及confidence interval。
6. 固定k=5与验证选k分别报告，保证“无需标签部署”的结论用固定k的独立测试值支持。
7. 审计入口是否传context groups，训练/验证也按source分，防止调参泄漏；短回答mask做极端长度单测。
8. 测完整attention获取的峰值显存、输入长度/回答长度成本和批量吞吐，比较只算logits的熵。

## 综述可用结论

INTRYGUE是白盒RAG忠实性预警的一种低额外生成成本方法：用复制相关头的SinkRate修正模型token熵，跨四任务六模型多格优于单独熵，且消融表明相关头和神经元影响预测分布。现有证据尚未把整个机制链的中介效应闭合；正确但不复制的简短推理甚至出现更高误报。主表调过头数、CoQA/XSum主要靠模型裁判、部分表格数值冲突且公开仓库缺原始标注数据，综述应注明这些条件。
