# I078 ICR Probe: Tracking Hidden State Dynamics for Reliable Hallucination Detection in LLMs

## 来源、版本和实际核查范围

Zhenliang Zhang、Xinyu Hu、Huixuan Zhang、Junzhe Zhang、Xiaojun Wan，ACL2025长文，17986–18002。正式原文：https://aclanthology.org/2025.acl-long.880/ 。本地17页；正文1–9页、附录11–17页全部实质内容已读，9–11页参考文献定位；目视渲染7/13/17页的迁移热图、top-k表/算法及跨模型迁移表。

官方仓库：https://github.com/XavierZhang2002/ICR_Probe ，固定commit `40ec490e762cadbac6bcefdc24a8f0d5974e8448`，保存1499288字节ZIP、SHA256和文件清单，见`qa/I078_official/`。完整阅读4个实质Python源文件、README和7个notebook单元的源码，保存带行号文本、AST及去掉图片输出的notebook内容。未执行下载代码、pyc、模型或torch加载。

独立脚本 `sources/audit_icr.py` 做标准库JSD/熵/标准化反例、参数数目、主表与迁移矩阵、层/样本消融验算；`sources/inspect_icr_resources.py`提取源码与AST。仓库没有生成数据、裁判标签、划分、特征缓存、模型checkpoint或主表全流程。下文把论文公式、公开示例实现及尚未建立的对应关系分开。

## 1. 任务定位：单回答的监督白盒检测

方法不直接把某层高维隐藏向量送入探针，而计算各层更新方向与注意力分布的差异，每层得到一个数，组成长度L的特征，训练小MLP预测回答正确性。需要层间hidden states和attention，属于白盒监督探针；reference-free指推断时不需外部参照，不代表监督标签没有外部事实依据。

评价主要是英语QA回答的二分类AUROC，不是原子事实定位、来源引用核验或真实性完整分级。文章泛称hallucination的范围较宽，但标签构造说明不够细，无法确认错数字、拒答、格式失败、部分正确等如何一一计分。因此本篇提供内部动力学特征有效性的证据，不能作为所有幻觉定义下统一正确性的保证。

与I094 SAPLMA相比，监督输入从单点隐藏表示变为跨层低维统计；与I090 SEP相比，目标不是明确蒸馏多采样语义熵；与I076相比，利用的不是注意力列质量的三角谱，而是更新向量与token方向的投影分布。

## 2. 论文公式和各项含义（第2–5页、算法1）

串行attention/FFN残差块简化为：`x_i^l=x_i^(l−1)+a_i^l+m_i^l`，其中a为attention输出，m为在attention后状态上计算的FFN输出。更新`Δx=x^l−x^(l−1)=a+m`。实际pre-norm、最后层归一等结构细节需对齐模型hook，简式未展开它们。

对第i个token，先平均各头的QK缩放logits并softmax，得到注意力分布。再把Δx投到各token隐藏方向：`p_ij=(Δx_i^l)^T x_j^l / ||x_j^l||`，对投影向量softmax成分布。按注意力选top-k token，计算两分布Jensen–Shannon divergence，作为ICR score。

低ICR解释为更新与注意力一致、attention主导；高ICR解释为FFN注入新知识、更新偏离attention。对回答token逐层求均值，得到L维特征。MLP结构`L→128→64→32→1`，各隐层BatchNorm、LeakyReLU(α=.01)、dropout=.3，输出sigmoid。

正文说输出“非幻觉概率”，算法2却定义y=1为hallucinated并返回“幻觉概率”；notebook把result_type=1当correct、0当wrong。AUROC若标签与分数同时反向可保持数值，但部署阈值解释相反，不能不核对就直接使用。

算法1先在全部token上softmax再截取top-k，两截后向量一般各自不再和为1，未明确再次归一；标准JSD需要概率分布。算法2则写logistic regression、SGD和线性θ公式，正文/附录实际为多层MLP与Adam。这些是文档间实质差异，复现须确定采用哪个版本。

## 3. “信息贡献”解释能否成立？

ICR是分布差异，不是直接量出的FFN/attention贡献比例。attention权重还要乘value、跨头拼接和输出投影；相同注意力分布不保证相同输出方向。FFN依赖attention后的状态，也可放大、抵消或旋转已有信号。不能从“低JSD”唯一推出FFN没有加入知识。

独立代数反例：固定端点、注意力及`Δx=(1,0)`，其分解可以是a=(1,0),m=(0,0)，也可以是a=(0,0),m=(1,0)。以A及总Δx构造的ICR相同，但模块向量贡献完全相反。注意力为零输出仍可有非零权重，例如value/output map为零；本反例说明观测量不足以普遍识别分解，不是对真实网络进行了干预。

“MHSA只搬运上下文，FFN独占参数知识”也过于绝对：MHSA的Q/K/V/O本身是学习参数，FFN输入依赖上下文。该叙述可作为机制启发，不是严格功能隔离定理。当前检测消融和分布图支持有用关联；没有attention/FFN消融、activation patching或随机等范数干预来验证score对实际模块贡献的因果忠实性。

与I076的“图瓶颈”解释一样，应把**预测效果**和**机制有效性**分成两个评价目标：良好的AUROC并不自动证明命名中的Information Contribution被定量测准。

## 4. 公开ICR函数与论文计算的关键差异

**输入注意力及预处理。** 示例接收生成缓存的attentions，重建完整序列矩阵。常见生成API给softmax后的权重；代码没有重新从Q/K重建logits，也没有证据其输入是论文算法要求的raw logits。平均“每头权重”和“每头logits后softmax”不可互换，调用方需要明确。

**上下文遮罩。** `set_other_attn_scores_to_zero`只保留user_prompt区间内彼此的注意力、response区间内彼此的注意力；对response行，所有prompt列都被置0。因此不能把该公开实现描述为完整保留回答对问题/证据的注意力。特征只截output token，且生成缓存最后预测token的hidden state通常未被处理；需提供输入边界和token对齐才能确认逐token对应。

**投影层索引。** 代码以`output_hidden_states[layer+1]−output_hidden_states[layer]`算更新，但向`origin_hidden_states[layer]`的token方向投影；公式(6)写的是更新后x^l。由缓存索引可见公开代码使用前一端点，不应直接宣称逐式相同。某些模型最后hidden state可能已final norm，尚需实际hook/库版本对齐。

**标准化后再softmax。** `js_divergence(p,q)`分别执行`(v−mean)/max(std,1e−8)`，然后softmax、自然对数KL。论文没有这个z-score步骤。它不仅数值稳定，还使正仿射缩放不变、去除幅度信息。独立例子p=[0,1],q=[0,2]，仅softmax后JSD=.0183056，而代码式标准化后JSD=0；因此两种版本确实是不同特征。

**top-p覆盖top-k。** README同时给top_k=20、top_p=.1；函数实际随后用`int(top_p*总序列长)`覆盖k。总长100时选择10而非20，这里的top_p是位置比例，并非累计概率nucleus。若要实现论文固定20，必须清楚设置top_p=None；本次仅核查，未修改作者归档源码。

**head选择。** README注释说induction-head参数最终版本不用，示例却use_induction_head=True；函数按注意力偏度/熵选头，不足时取至少H//8个头。使用全部头需明确False，不能直接把Quick Start当成主表配置。

**因果位置风险。** prompt列和未来列被置0，早期回答token可能少于k个非零可见回答位置。topk没有限制索引≤当前token，零分并列可能选到未来位置，而投影端可访问重建后的完整隐藏缓存。现有代码未给因果索引保护；是否实际选中未来位置、影响多少尚未在真实张量上测量，不能写成已量化的泄漏。后续须截断可见位置再top-k，另外处理短回答和空回答边界。

## 5. JSD、熵与消融的数学问题（附录A/B.5）

标准JSD为`.5 KL(P||M)+.5 KL(Q||M)`，M=(P+Q)/2。采用自然对数时范围[0,ln2]；采用log2才为[0,1]。公开函数用自然对数，故论文“0至1”的陈述只能作为松界，不能称其自然归一到1或直接把1解释为最大值。

HS ONLY把注意力设uniform，作者反复称`JSD(P,U)`等价于H(P)，这在数学上不成立：P=U时H(P)=ln2而JSD=0；P=[1,0]时H=0而JSD=.215762。`KL(P||U)=log k−H(P)`才有相应关系，也不是JSD。固定维度下与均匀分布的差异可以反映集中度，但不等于原分布熵。

代码中attention_uniform还发生在z-score之前，uniform经标准化与softmax仍uniform；投影则先标准化再softmax。所以HS ONLY衡量的是**变换后投影分布对uniform的JSD**，不能说直接测了原隐藏更新向量的Shannon entropy。NONE没有任何信号给出.5可作常量基线，并不是训练后测得显著机制证据。

## 6. 数据、标签和训练协议：已知条件与缺口

模型Llama-3-8B-Instruct、Qwen2.5-7B-Instruct、Gemma-2-9B-it；数据HaluEval QA、SQuAD、HotpotQA、TriviaQA rc.nocontext。附录每源随机抽10000，80/20训练/测试，名义8000/2000；未提供完整筛选后类数、实例索引、question/article分组或各模型拒答/缺失比例。

“标签来自annotated hallucination datasets”不足以重建SQuAD/Hotpot/Trivia生成回答的gold：它们的原始答案不是每条新生成输出的直接二元标签。notebook读取output_judge.jsonl，说明存在裁判结果，但仓库未给裁判模型/提示/解析规则与文件；HaluEval是使用原真/假答案还是新生成后裁判亦未建立。不能据数据集名称自行补成GPT-4判分、EM或某个F1阈值。

生成温度、提示、最大长度、context提供方式、输入截断、每题采样数和SEP教师构造等关键设置缺乏足够产物。附录称所有baseline设置一致，但无源码/缓存对齐不能独立确认I090 SEP的教师标签、层选择与标准设置是否完整保留。

附录训练50epoch、batch32、Adam lr5e−4，验证loss停滞5epoch减半lr，多次运行平均，但没列种子、次数、误差条或验证集从哪里划出。仓库Config则为100epoch、batch16、lr1e−3、weight_decay1e−5。代码每epoch在val_loader评价并按val_loss保存，没有独立test路径；不能确认论文80/20中的20%是否同时作选择与最终测试，也不能只凭公开脚手架断言发表结果一定泄漏。

## 7. 主表：多数领先而非全胜（第6页表1）

12个模型×数据条件中，ICR胜过SAPLMA/SEP较强者10项；全部基线比较也有明确例外：Qwen/Trivia .7684低于SAPLMA .8225，Llama/Trivia .7325低于SAPLMA .7650。Gemma四任务均领先，例如SQuAD .8142对SAPLMA .7175，增.0967。

独立按12条件等权宏平均：ICR .788267、SAPLMA .763492、SEP .685025。ICR比SAPLMA高.024775（2.4775个百分点），这只是发表AUROC的等权算术汇总，不是原实例合并AUROC、显著性或真实人类标注总体性能。没有输出级预测与CI，.0167等较小差异不能宣称稳定显著。

PPL/LN-Entropy/LLM-Check是不训练的对照，与有8000级标签MLP的监督预算不同。附录Semantic Entropy也有多生成成本：不能只看参数数目推断全面优于所有范式。表7所谓“cross-dataset AUROC”只列每模型四个数据值，未给源→目标矩阵，不宜擅自解释成特定跨域教师转移协议。

## 8. 跨集迁移：百分点、例外与图注边界（图4，表9–10）

图4对应Gemma，ICR同域4项均值.8247，12个异域单元均值.738558，下降.086142，即8.6142**个百分点**；相对原值下降10.4452%。SAPLMA下降.101808（10.1808点），SEP .116667（11.6667点）。正文写8.61%/10.18%/11.67%，其算式对应绝对点差，不应翻译成相对降幅。

Gemma最低跨域ICR为Trivia→Halu .6629，但不是每格都胜SAPLMA：Halu→Trivia .6967<.7047，Trivia→Halu .6629<.7186。因此“异域全胜”需改成宏平均优势。热图共享色标.6–.9又会截断低于.6的SEP值，读格内数值比只看颜色更可靠。

附录Qwen最低Hotpot→Trivia .6387，Llama最低SQuAD→Trivia .5658，另Hotpot→Trivia .5933。附录文字声称两者全部超过.6，以及把表9称Gemma，与表头/数字矛盾。应按Qwen、Llama实表记录，不将正文“≥.66”外推所有模型。

独立均值：Qwen ID .7765→OOD .714342（降6.2158点），Llama .7636→.685375（降7.8225点）。这些是同一生成器上的跨数据源训练/测试，不是一个探针跨模型即用；层数变化导致L维输入改变。平均层曲线相近也不能证明特征与所有数据伪迹独立。

## 9. 消融与解释性：具体支持到哪一步

**attention增益，表2。** 完整对HS ONLY在Gemma四任务均高，支持注意力与变换后的更新统计有互补预测信息；没有attention-only项，也没有维数/范数相配的模块真贡献探针，不能推成已测准FFN知识注入。

**层组，表3。** 去中层在SQuAD/Hotpot/Trivia损失最大，分别.0560/.0988/.0804；Halu却去深层损失.1151，大于去中层.0662。应说多任务中层重要，同时保留Halu深层反例。文字早层0–13、中层15–28、深层29–41漏了14层，需索引确认。删特征并重训度量的是预测可用性，不是删生成器模块导致的幻觉变化。

**k，表5。** k20通常较好，Trivia k30 .8005稍高于k20 .8001；SQuAD k20→30从.8142降.8005，降.0137（1.37点），不符合文字“所有任务变化小于.5%”。Halu k20比ALL .8289高.0147，应说1.47点。选择k和网络结构是否用独立开发集、是否报告全部候选需核查。

**架构，表6。** 列hidden layers1–5，性能.6410/.7398/.7889/.8000/.8006；但`L→128→64→32→1`是3个隐层、4个线性层。文字称4 hidden layers与实际定义不一致。更深的.8006与.8000差.0006，没有方差不宜夸大最优性。

**规模，表8。** Qwen14B/3B分别对SAPLMA平均高3.9325/3.7850点，对SEP高9.01/10.785点，与文中近似相符。但这是分别适配/训练各模型的结果，不证明同一探针尺度不变；生成错误分布也随模型变。

## 10. notebook图的实际统计含义

稳定性ribbon先计算每数据集跨样本的平均层曲线，再对四条数据集均值曲线求总体std，画±1.5×std，并删最后一层`[:-1]`。因此窄阴影表示这四个数据源**均值曲线接近**，不是每条回答的score低方差，也不是标准误/95%CI。它无法直接证明每个错误类别或部署域稳定。

逐层AUROC先以correct=1计算，再逐层取`max(AUC,1−AUC)`，随后展示峰值层。该图允许每层用同一套真值选择方向且选择最高层，是描述性可分性，不是固定单向无监督检测在独立测试上的承诺性能。它不等于主表MLP也用了该翻转；目前未找到主表评分管线，不能把notebook行为套到所有结果。

密度/直方图选择layer11并标AUROC≈.77，仍依赖上述选择。应对选层/方向设独立开发集，再测新样本；若只展示关联，就明确属于探索性分析。

## 11. 参数、计算成本及公开接口可复现性

独立按线性bias与BatchNorm affine参数计，MLP共`128L+10945`：L28为14529，L32为15041，L42为16321。16K是近似量；按十进制16000和16Ki=16384含义不同，不能从“L<42”无条件推导严格少于16000。BN running buffers另算存储、不算可训练参数。

小探针不等于小总成本：要缓存多层hidden/attention，重建序列注意力矩阵，并对各回答token取top-k投影。attention存储随序列长平方增长；投影约O(L·T_answer·k·d)，还含读注意力/筛选成本。作者600–800 GPU小时是多轮全部实验预算，不是每条在线检测耗时。没有与baseline等硬件、等生成长度的延迟/峰值显存对比，不能用16K/110K参数比例当运行提速比例。

README明确训练段仅示意。静态接口检查确认：构造函数要求额外model参数，示例没传，且构造后又self.model=None；setup_data调用`_load_data`和`_create_data_loaders`，类内均未定义；验证读取config.halu_threshold但Config无此字段。阈值Precision/Recall用该字段，F1却用round输出（约.5），若两阈值不同又是不同操作点。保存最佳模型后没有独立测试/加载流程。

这些说明公开包需补齐，不能直接运行得到表1；不等于论文原内部实验从未运行。没有擅自修改归档以掩盖问题，也没有浪费GPU执行缺失的管线。

## 12. token级案例与“解释”的边界

表4有3个手选回答：错误hectares .04、Vietnam .19，正确Cree .55；标点、空白和数字子token分数不一致。它们说明句级特征可在某些关键词上低分，但没有token真值全集、span边界、精确率/召回/F1或全样本抽样协议。

句级平均特征训练后直接把单token特征送同一MLP，本身改变了输入分布。非线性意味着`MLP(mean f_i)`一般不等于`mean MLP(f_i)`；不能把句级概率严格分解成每token贡献，也不能把低分token必然称为错误事实。案例用于提出局部检测问题，不能当已验证高质量定位器。

## 13. 研究问题、可用论点及后续核验

**Q1：ICR测到的究竟是什么？** 目前更稳妥是“跨层更新—注意力分布差异特征”；标准化与投影索引改变了其量纲/语义。应分别实现论文版本、公开版本，在固定标签/划分下对照，单独改变z-score、head、mask、层端点、k/p及归一，再报告机制主张。

**Q2：何时能称模块贡献？** 对真实a/m输出取向量范数、与总更新的点积贡献及抵消量，加入模块patch/ablation和等范数随机控制，检验ICR是否追踪这些量；当前代数不可识别反例说明仅A+端点不足以作通用识别。

**Q3：能否部署为单次实时告警？** 要先明确最后token对齐和因果top-k，解决零分并列/未来缓存风险；预注册阈值，报告类比例、拒答、短回答、覆盖、延迟和显存。当前图例与缺失接口不能证明开箱即用。

**Q4：跨域优势是否稳定？** 保留Trivia例外、全源→目标矩阵及低于.6项；源域选参，目标测试不能参与符号/层/k选择。共享问题、文章分组切分、多种子与paired CI需要原始数据。缺标签规则尤其阻止判断是知识错误、格式还是裁判偏差迁移。

综述可用英文表述：*ICR Probe compresses cross-layer hidden-state updates into attention–projection divergence features and trains a small supervised classifier. Its reported in-domain gains coexist with transfer failures, while the interpretation as module-wise information contribution requires additional causal validation and implementation alignment.*

页码锚点：3–5页定义/探针；6页表1；7页图4与表2；8页层与token案例；13–15页算法/训练/k/熵消融；16–17页规模及迁移补充。已完成全文/附录细读、公开源码/7单元审阅、标准库验算；尚未完成GPU复现、原始标签审计或发表管线对齐。
