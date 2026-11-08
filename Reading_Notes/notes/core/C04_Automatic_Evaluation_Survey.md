# C04 · A Survey of Automatic Hallucination Evaluation on Natural Language Generation

Siya Qi, Lin Gui, Yulan He, Zheng Yuan；https://arxiv.org/abs/2404.12041 。本地v4（2025-10-20）46页，检索范围截至2025年7月。

## 阅读范围与核查状态

已读正文第1–20页、附录A/B/C第39–46页，含检索筛选、四象限案例、105方法元信息和资源链接；第20–39页主要参考文献，不因列入综述就计作原始论文已读。已目视核验第2页概念图、第40页PRISMA和实验设置、第41页四案例表、第43页方法表。已与本组C07–C13原文证据对照；未运行四个检测器或重建全部105条编码。

## 1. 为何是本组最直接的核心综述

本文专注text-only Automatic Hallucination Evaluation（AHE），排除纯人工评价、缓解技术及多模态系统，覆盖pre/post-LLM方法。相比C01–C03，更贴近我们的选题“评估方法”，包括证据获取、比较机制、内部信号、LLM裁判及应用限制。应借鉴其问题拆解，而非将本组综述写成其105方法清单的改述。

两个中心目标是Source Faithfulness（SF）和World Factuality（WF）。第2页四象限给出来源自身错误时的权衡：忠实复述可世界错误，修正来源可违反严格源支持，源外新增可世界真实或不实。这里的SF误差是相对于输入关系，而WF关系依外部事实判定，两者不是互斥类别；也不能从一个分数可靠恢复另一个分数。

## 2. 检索方法、统计分母和纳入范围

第3页称遵循PRISMA，DBLP为主、另查ACL和ICLR/ICML/NeurIPS/AAAI，2020-01至2025-07；以hallucination/factuality/faithfulness组合evaluation/assessment/measurement/benchmark/dataset检索标题元数据，去重后标题摘要筛选、再全文资格检查。

附录A第39–40页：数据库223→去重58→165，另排除27→138，排缓解5、多模态61→72；其他来源106+24+17=147，均取回且资格阶段无剔除；72+147=219。算术与最终219吻合。不能把219篇纳入研究与105种评价方法混为一个分母；前者含背景/资源与相关工作，后者用于方法统计。

摘要77.1%方法针对LLM与105分母相符（81/105≈77.14%）；第4页46.7%有新数据约为49/105。此处只是整数比例一致性，不是独立核查81/49行编码。其他来源全部纳入、跨来源去重和手工补查的完整清单尚未重建；遵循PRISMA的自述不自动证明无遗漏或无筛选偏差。

## 3. 基准分类的贡献及不要混淆的东西

任务特定→通用事实性→应用→元评估→自动数据生成（第4–10页）。细化长文、非英语、医学法律、代码工具与角色行为，提示幻觉不仅是短事实QA。元评估关注检测器本身，对照SummEval、SummaC、AggreFact、TRUE、FELM；应与直接测生成模型分开。

Table1/2同时混有完整任务数据集、人工错误标注子集和元评估整合集，Size单位包括article、summary、pair、entity、dialogue、claim；原始规模不能直接当独立标注数量。例如RAGTruth表写2.97k样本，对应约2965个input，而实际17790条模型response；FActScore6.5k可能对应扩展500实体×13模型生成，不等于183实体的人工主实验；C07/C12笔记已给出处。

数据生成的“真实感”不是已验证真实错误率。合成替换可过易、带生成器风格、误把正确改写标假，自动生成还可能自验证循环；需要独立人工核查和跨生成器测试。动态基准也只是降低陈旧和污染风险，不能保证不泄漏或来源一直正确。

SimpleQA第7页表给2k prompts，而C03给4326题，需读其原始论文与版本确认；本文虽列链接，不能用“更新更晚”自动判一个规模为真。Table2的法律数据745k等大数字也需要核查单位、原问题与模型采样倍数，不应用于本组未验证的统计图。

## 4. 方法分类：管线拆分很有用，三个范式并非独立轴

Reference-based：证据获取＋比较；reference-free：内部状态/一致性；LLM-based：强模型裁判/交叉验证（第10–15页）。本文也承认LLM judge既可有reference也可没有，SelfCheckGPT Prompt也是LLM判自采样一致性，故三组交叉。我们应把“证据来自哪里”与“谁/怎样判定”分成独立维度。

证据获取SF：整篇输入、定位句、QG-QA、atomic claims、semantic graphs、层次结构。WF：指定知识库、LLM参数知识、online search。二者可联合。把LLM当KB有循环核验风险；搜索需要query、覆盖、来源可信/时效和证据整合，不能因为有网址就视为世界真值。

比较可词面EM/F1、关系匹配、答案分布距离、NLI、图/弧蕴含、合成任务微调、多指标集成。分解会影响事实的上下文完整性和覆盖；提取出少数易核查claim获得高支持率，可能掩盖困难内容遗漏。问答方法会受问题生成、答案选择、answerability和对比器限制；源支持蕴含方向应明确。

Reference-free一致性、重构、自采样协方差特征及语义熵，是风险代理而非真实性充分证据。第13页“幻觉是随机且不稳定”的表述只适合部分confabulation；C05已显示共享误解，C10也明确方法不处理所有稳定错误。重构原问题成功说明相关/可逆程度，不能保证回答所有断言真实。

内部信号包括logprob、attention、embedding、gradient、FFN、relevance propagation等，不同访问条件和训练监督需单列。Semantic entropy依赖语义聚类，linear probe预测熵又是另一层近似；不能把所有内部得分都称校准概率。

LLM judge可输出二分类、Likert、跨度、理由，交叉质询则是交互核验。理由可方便人工审阅，但不证明真实机制；CoT可增加表面自信，第14页承认它甚至可能遮蔽不确定线索。工具集成OpenFactCheck之类应评组件与端到端，不能只以框架开放就判它可靠。

## 5. 监督、粒度、成本：从作者建议转成可测要求

第16页认为没有普遍最优粒度，需随任务从token/entity/span/claim/sentence/document选择。细粒度便于定位却可丢跨句语用；完整回答分数又掩盖局部危险事实。应报告判断单位和聚合规则两项，特别明确macro平均、micro计数和any-error。

监督不能仅按是否为目标幻觉数据训练二分：SelfCheckGPT不训练生成器却使用已训练BERTScore/QA/NLI/LLM比较器，采样20次并非天然“快且便宜”；本文称unsupervised/source-grounded是高层简化，应以C08具体访问与费用为准。监督方法可能域外失败，但没有充分证据说所有监督方法必然不泛化；需要原文的跨域/生成器测试。

对齐人类标签要有清晰定义、重叠标注、训练与IAA，C14补足本篇宏观建议的执行细节。第16页把LLM teacher称“性能上限”，要精确解释：若只按teacher标签评分，无法在该评分中发现teacher错误；这不等于学生对独立真实金标永远不可能更好，去噪、外部证据或归纳偏置可改变真实准确率。本文没有证明一般性的teacher上限定理。

延迟、费用、专门知识和严重性需要共同衡量，但“高风险领域”应落实到标签和代价函数而非只写背景。不能从本文泛称某大模型适合批处理推断当前API价格/延迟；本组未测产品实时性能。

## 6. 附录B四案例实验：真实有新实验，但证据范围很小

作者从XEnt/FactCollect选四种SF/WF组合，比较WeCheck、SelfCheckGPT、HaluEval、FacTool。GPT方法统一用GPT-3.5-turbo；SelfCheckGPT用zero-shot prompt判一致性，HaluEval提供示例，FacTool适配KBQA检验摘要且用online search；全部二值输出（第40页）。因此不能当作原生任务、相同证据和相同预算的公平全比较。

第41页Table3已目视记录，列顺序为WeCheck/SelfCheckGPT/HaluEval/FacTool，TRUE表示判正确：

- SF且WF：TRUE/TRUE/TRUE/FALSE。
- SF但WFE（来源与摘要均Chris Betts）：FALSE/TRUE/TRUE/FALSE。
- SFE但WF（来源Marl Park，摘要Cardiff）：TRUE/FALSE/TRUE/TRUE。
- SFE且WFE（Ballymena）：FALSE/TRUE/TRUE/FALSE。

这16个判定表明不同目标和证据会产生不同标签，且FacTool对第一例可能错；不能据第二例成功说FacTool总可靠、从两例说模型输出不稳定，更不能把4例accuracy当总体性能。单次每例结果不能区分随机不稳定与系统目标不同；若要测稳定性，应对同一输入重复运行并报告方差。

SF与WF互相影响是合理假设，本文没有控制模型先验、来源真假、提示、查询和适配，只靠案例不能确立“无意识影响”的内部因果机制。世界真假标签也依作者引用的证据，本组没有重新检索这四则历史新闻，故不声称已独立验证世界金标。

## 7. 方法表交叉核查：允许当导航，不能替代原文

第42–44页元信息表提供dataset/source/fact definition/task/base-model/method/metric/SF/WF，但字段语义有混用：Based-model包括生成器、裁判或合成数据模型；Metric可能输出分数也可能元评估AUROC/F1；New Dataset未命名时由综述自行赋方法名。这些规则已在第42页解释，不能将人为别名当原论文正式命名。

对已读方法：AlignScore表写22 datasets，但C09主训练是7任务15数据集约4.7M，需区分收集池/实际训练/元评估；Q²表勾WF而不勾SF，原方法是对指定来源的一致性核验，应按原文目标复核；SelfCheckGPT表metric写AUC-PR较C02的AUROC更符合原始主实验，但SF/WF勾选仍不能代替其事实标签定义；FELM847与版本审计更接近，segment数另计。RAGTruth词跨度与input/response数仍需独立列。

第44页将一些主要NLI小模型列入“after LLM”也不意味着都依赖ChatGPT，作者Era规则偏方法生态/能力而非单一参数阈值。105条均属作者划分单元，不等于105个独立同任务可比较检测器。

## 8. 开放问题、我们已能回答什么

Q1：SF与WF可以一个分数同时可靠测吗？本文四象限及C16逻辑分析说明目标不同，C07指定知识库支持又不是全世界真假。应保留双标签，错误来源和世界证据分别获取；当前没有本组实验验证某一个联合score最佳。

Q2：引用材料就是事实证据吗？并不充分。搜索可能返回模型杜撰、自循环或过时材料；来源支持和来源可信需分层评估。可将同一claim配真实/伪造/缺失/冲突证据，固定裁判看判定转移，未运行。

Q3：细粒度必然提升评价吗？本文否认普遍最优粒度。可固定同一回答，比较独立原子/带上下文原子/完整句/完整回答，分别评覆盖、歧义与跨句错误，人工抽检分解是否改变语义。尚未实施。

Q4：教师裁判如何限制元评估？若金标只来自同一个LLM，学生高吻合不能证明真值正确；独立专家/可靠来源的保留测试集可检验teacher与student共同偏差。需隔离teacher生成的训练标签与人工测试标签，现未重训。

Q5：多源一致能否提高可靠性？只有来源相对独立且可信才有意义；若多网页复写同一错误，数量不是独立支持。可按来源溯源聚类、时间和引用链计证据，而不是简单多数票。本文给方向，本组尚未收集溯源网络。

## 9. 对本组最终写作的具体贡献

主类“自动评估方法综述”，次类“SF/WF、证据管线、内部风险信号、应用与元评估”。保留两阶段证据→比较思路，把LLM使用方式移为正交属性，再加入访问权限、监督、单位/聚合、指标、费用和独立金标。相较C01–C03，本篇最贴近方法流程；相较C14–C16，它不替代详细人评程序、术语社会研究或形式逻辑边界。

英文概括：Automatic hallucination evaluation requires separating source faithfulness from world factuality and tracing how evidence is collected, compared, and aggregated. Model-internal proxies and LLM judges provide scalable signals, but their reliability must be established against independent labels under explicit task, cost, and generalization conditions.

## 待核范围

尚未重新编码105方法或核验全部219篇纳入清单；没有重跑四案例、历史新闻真值核验、模型成本测试或证明teacher天花板。多模态仅作为作者未来讨论背景，不扩张本组纯文本工作范围。
