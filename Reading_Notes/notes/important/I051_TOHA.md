# I051 TOHA：注意力图最小生成森林能筛查上下文不忠实，但标签筛选与统计独立性限制结论

## 来源与核验

Alexandra Bazarova等，*Hallucination Detection in LLMs with Topological Divergence on Attention Graphs*，ACL 2026 long paper，页15449–15470，PDF22页。逐页阅读方法、主结果、全部实质附录、表1–20、图1–10与风险说明。官方[TOHA仓库](https://github.com/sb-ai-lab/TOHA)固定为commit `d15709d005a9db0de22df4d81a2c56f97c27ee89`，源码ZIP 5,878,527字节及SHA256/文件清单保存于`Reading_Notes/qa/I051_official/`。只做静态检查，未运行7B/13B模型，故模型AUROC不能称独立复现。

## 目标、输入和几何定义（PDF1–4、17–18）

目标是RAG/给定context下的**回答级任一幻觉**二分类，主要是忠实性而非开放域世界事实。白盒读取生成模型各层各头attention；闭源API不可直接用。每个头把attention `w_ij`转为伪距离`1-w_ij`，把prompt token集合P内部边距离置零，求把回答token集合R接到P上的最小生成森林权重和，并除以`|R|`。该量等于修改后0阶persistent homology条形码有限区间长度和，记作`MTop-Div_G(R,P)`。较大值被解释为回答相对prompt更“新”，倾向幻觉。

注意力是有方向、受因果mask与softmax归一化影响的；把它当无向距离并不自动满足对称性或三角不等式。正文称“complete undirected graph”，但没有细致说明对上/下三角如何对称化；这需依源码确认。0阶拓扑在这里与MST等价，不能笼统概括为高阶洞结构。附录证明界`0≤MTop-Div≤|R|`及权重扰动ε下变化≤`ε|R|`，只是数值稳定，不证明语义事实稳定。

正文从MST长度可作几何散布代理推出“信息新颖性”，再用新颖性推测幻觉：这是**启发式桥接**，不是信息论等价或事实性定理。正确回答必然引入新组合和同义改写，错误回答也可以大量复制；需在同词面重叠和长度下检验因果关联。

## 头选择和监督量（PDF4–5）

对每个头计算100条验证样本上幻觉与忠实的平均归一化距离差`Δ_head`，降序选头；对前N头取平均score，并在**同一验证集**选AUROC最高的N，正文N最多10。测试集为各数据集25%，5次不同拆分。此法不训练权重，但需要真实标签选头和N；“training-free”不能解释为零监督。N的选择在同一100例上反复优化存在小样本赢家偏差，且1024头中挑最大差值又一层多重选择。应另留nested validation或跨数据集预定头。

当前源码`config/evaluation/default.yaml`为`seed:42,k:5,test_size:.25,val_size:100`。然而`config/method/mtopdiv.yaml`及`MTopDiv` dataclass默认`n_max:6`，与正文Nmax=10不一致；`config/mtopdiv.yaml`默认Llama3.1-8B、CoQA，不能直接视作所有论文表格复现实验配置。`fit_hyperparameters`在验证集按Δ排序并逐N在同一集算AUROC；`predict_score`在unsupervised模式取各选头绝对值平均。函数名unsupervised仍依赖有标注验证集，除非另走top-4复制头变体。

## 数据与标签构造（PDF18–21）

MS MARCO与CNN/DM来自RAGTruth；CoQA、SQuAD、XSum另生成。后者标签主要由GPT-4o产生，少量人工标注用于核查。CoQA/SQuAD先以reference答案筛选：ROUGE-L=1当忠实；ROUGE-L≤.3且无任何reference子串才进入潜在幻觉池，由GPT-4o确认。中间区域被排除。XSum直接GPT-4o判断。作者又为了平衡/干净筛选不同模型的样本，实际评价是**被阈值和裁判筛过的模型条件分布**，不能推断自然RAG全分布检出率。

这种ROUGE极端筛选尤其有词面捷径：错误但包含reference子串的长回答可能被留在忠实/剔除边界，正确同义短答却可能送裁判；模型长度分布也不同（图9各域/模型中位数3–54词）。这些因素会影响attention新颖性。人工由三名团队成员各标约100例，最终只取全体一致样本为gold；表19两人accuracy均值.807、Pearson .628，不代表争议样本性能。GPT-4o对该共识子集的CoQA/SQuAD准确约.808/.854（表18不同prompt均值），尚有约15–19%错误；没有XSum同等人工验证。N/A解析、参考答案质量和按passage/source隔离未充分报告。

表20例如Mistral CoQA 776/776、SQuAD 311/389、XSum301/448（幻觉/忠实），不能假定所有集合平衡或同样本跨模型配对。对同一来源passage的多个问答做实例随机拆分可能造成source泄漏，须按source分组检验。

## 主要AUROC与真正的例外（PDF6–9、13）

表1 Mistral的TOHA在MS MARCO/CNN/DM/CoQA/SQuAD/XSum分别`.76/.60/.89/.96/.66`；Llama2-7B为`.65/.56/.90/.87/.68`；13B为`.67/.56/.92/.88/.66`。性能强弱高度依任务：CNN/DM近随机，CoQA/SQuAD较高。表2 Llama3.1 CoQA `.84`低于单次SelfCheck `.91`、20次`.95`，Qwen XSum `.69`与SelfCheck单次`.69`持平、20次`.72`更差；故“始终SOTA”不成立。

正文举Mistral MS MARCO 11.7%和Llama2 CoQA 21.6%提升，须说明相对哪一基线、按相对百分比还是绝对点。对Mistral MS MARCO，TOHA .76比max entropy .68高.08点、相对11.76%；对Llama2 CoQA，TOHA .90比semantic entropy .76高.14点、相对18.42%，若比perplexity .74则+21.62%。这是选择不同参照的相对百分比，不是跨设置统一提升。

表6–7将采样法增至20额外生成，Mistral CoQA SelfCheck .93 > TOHA .89；Mistral XSum .71 > .66，Llama3.1 CoQA .95 > .84，Qwen CoQA .75 < .79、SQuAD .77持平、XSum .72 > .69。增加预算改变排名，论文称“most”可以，但不能说全域领先。

HotpotQA表3 Mistral `.71±.08`与SelfCheck/semantic entropy `.70`差距远小于波动；Llama2-13B `.80±.03`优于下一个`.70±.04`。称HotpotQA“in the wild”仍是构造的多跳benchmark，不代表实时网络分布。表8在整个RAGTruth上TOHA仅比ReDEEP高.02/.03，且只列两种Llama模型。

## 几何与注意力消融（PDF7–8、13–15）

把prompt内边置零优于完整图MST：Mistral CoQA `.90` vs `.75`、MS MARCO `.65` vs `.38`；Llama2 CoQA `.89` vs `.60`、MS MARCO `.76` vs `.37`（表4）。这支持针对P/R边界的特征设计，但完整MST未做方向反转的AUC和长度/边数匹配，不能唯一归因于“拓扑”。

表9用所有层/头特征训练L1分类器，MTop-Div在Mistral MS MARCO/CoQA `.86/.98`，Llama2 `.75/.96`，高于其他注意力特征；这不是主方法少标签平均10头设置。表10同选择器比较LookBack attention ratio，Llama2 CoQA `.90` vs `.76`、XSum `.68` vs `.59`；方法特征有效但选择器仍可过拟合100例。

作者称“hallucination-aware”头与复制行为相连，图6 Mistral十个高频头仅4个在copy rank前25，Llama2七个仅2个，确有交集但不能说大多数。图5的首token注意力也可能是attention sink/位置效应，不证明该头检测事实矛盾。理想反事实应交换正确/错误事实但保持模板、长度、复制率，检验头的响应变化。

零标签top-4 copy heads变体表5在Llama2 CoQA `.89`、MS MARCO `.62`，Mistral CoQA `.77`、MS MARCO `.66`。Mistral CoQA较监督TOHA `.89`低.12；“完全无标注”是特定变体，不能拿监督TOHA主表性能替代。top copy heads的识别仍需模型内可观察干预或预计算。

## 统计、迁移与成本（PDF5、7、15–16）

表12 Wilcoxon-Holm给TOHA相对8基线p≤.0016，表13平均rank1.67；但把模型×数据集×5次拆分当独立配对若没有按模型/数据集聚类，会伪增样本量。表12中极小p值大量相同，应公开原始run级分数、配对单元和检验脚本。整体显著并不表示每个数据集显著，特别是Hotpot Mistral和CNN/DM。

迁移图3c Mistral跨五域的矩阵存在明显退化，例如以SQuAD头选CoQA仅.71、同域.96；以MS MARCO头选CoQA .86、同域CoQA .89，表现不一。表14只对CNN/DM、XSum做独立两样本t检验，p>.05仅表示未拒绝零差异，不能“确认等效/无迁移损失”；同模型/相同test样本本应配对，且5次拆分小、功效弱。需预定非劣界并做配对置信区间。

图4a在16条MS MARCO上response generation约69秒，max entropy再2秒，TOHA再10.5秒，SelfCheck单次额外生成约73.6秒。TOHA检测阶段约7倍快于单次SelfCheck，但全流程约79.5秒 vs 142.6秒只有1.8倍；若生成原答是既有沉没成本，可比较增量10.5/73.6约7倍。论文“通常10–20次因此70倍”是线性外推，未直接量出批处理、KV cache与多采样吞吐；读取全attention矩阵仍有内存和平方长度成本，图中不含长文/生产负载。

## 研究问题与可执行核查

1. 按source/article而非回答行划分，审计同一context跨train/probe/test泄漏；保存各split的source hash。
2. 保留全部自然输出（包括ROUGE中间区、N/A、三人不一致）重新评估AUROC/AUPRC和不同错误率，量化筛选收益。
3. 构造最小对立样本：只替换事实实体/数词，保持token长度、复制率和prompt结构；另用正确同义改写检验新颖性与事实性的解耦。
4. 分层回归控制回答长度、首token attention、词面重叠、拒答、任务和模型，再测MTop-Div增量。
5. 对头选择采用nested validation、跨domain预选/冻结，并绘制100例选择下的多seed头稳定性与真实迁移损失。
6. 比较有向/无向构图、三角对称化、边定义、纯MST和token copying分数；验证零阶拓扑的独立贡献。
7. 公开配对run结果，以dataset/model为cluster做多层bootstrap；跨域非劣检验须设实际界。
8. 实测长度扩展的峰值显存、token吞吐和批量推断成本，区分原答生成与检测增量。
9. 审计论文Nmax10与仓库n_max6、默认模型/数据及标签处理版本，固定配置后才尝试复现。

## 综述可用结论

TOHA显示，模型内部attention的prompt–response几何边界可用少量标注挑选高信号头，在CoQA、SQuAD以及部分RAGTruth设置上取得强AUROC，并比多次采样的检测阶段节省时间。它属于白盒、响应级、给定上下文忠实性筛查。论文标签以reference极端筛选和GPT-4o为主，存在自然分布选择与词面捷径；跨域/统计结论不能扩大成稳定事实检验。公开代码的选头上限也与论文不符，应保留版本差异。
