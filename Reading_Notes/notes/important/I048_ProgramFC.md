# I048 ProgramFC：显式程序改善多跳核验，但“可解释”仍取决于解析器和子模块

## 来源、版本与核验范围

Liangming Pan、Xiaobao Wu、Xinyuan Lu、Anh Tuan Luu、William Yang Wang、Min-Yen Kan、Preslav Nakov，*Fact-Checking Complex Claims with Program-Guided Reasoning*，ACL 2023，arXiv:2305.12744v1（2023-05-22）。本地PDF共22页，正文、限制、baseline细节、程序/错误样例及全部prompts逐页阅读；目视核对PDF6表1、PDF7图4–5、PDF8表2–3、PDF15模型说明与PDF17错误例。

作者当前[官方仓库](https://github.com/mbzuai-nlp/ProgramFC)main保存为`Hallucination_Evaluation_Library/code/I048_ProgramFC_main.zip`（13,311,402字节），ZIP完整性通过。静态审计program generator/executor、QA、BM25与评价脚本，并直接统计包内HOVER/FEVEROUS-S claims。没有调用已退役的Codex/text-davinci-003或运行FLAN-T5/Pyserini，故表1–3未做模型级复现。

## 方法核心：规划与执行分离

ProgramFC把复杂claim变成受控程序，只有三个函数：

- `Question(q)`：求中间实体/数值/日期；
- `Verify(c)`：核验一个较简单claim并返回Boolean；
- `Predict(expr)`：对之前的Boolean做AND/OR/NOT得到最终标签。

Codex `code-davinci-002`看20个人工(claim, program)示例后，以temperature .7生成N个候选程序；执行时FLAN-T5回答问题/做二元核验，gold设置读人工证据，open-book对每个步骤用BM25检索，closed-book只用参数知识。N=5时对五个程序的最终标签多数票。

这一结构的真正优势是**中间变量可替换、查询可迭代、模块可交换**。例如先问Interstellar导演，再核验Christopher Nolan出生地；原claim没有“Christopher Nolan”，一步检索难以构造这一query。它与自由CoT不同：执行结果确实沿程序流动，原则上可定位planner、retriever、QA/verifier或logic错误。

但程序只是高层解释。`Verify`内部仍是黑盒FLAN-T5，程序不显示它用了哪条证据、是否正确蕴含；可读性不自动等于证据充分性或因果忠实性。

## 数据与当前公开文件审计

论文用私有test不可得的validation作评价：HOVER 4000条，2-hop1126、3-hop1835、4-hop1039；FEVEROUS-S仅保留纯sentence evidence共2962。当前ZIP计数完全对应。HOVER dev标签严格2000 supports/2000 refutes；FEVEROUS-S为1411/1551。训练分别18,171和26,928，标签并不平衡。

当前HOVER文件存在重复surface claims：train 18,171行只有18,054 unique claims，116个重复组/233行，其中8组同文本标签冲突；dev 4000行只有3982 unique，18组重复，其中1组同文本一真一假。dev冲突例“Changchun is more populous...”有两个ID与不同evidence/相反标签。Gold-evidence模型可依证据区分，open/closed系统只凭相同claim生成query/程序，原则上无法稳定同时答对。统计显著性应按unique claim聚类，且应明确相同claim因不同gold evidence为何能有相反标签。

train与dev之间未见exact claim/id重叠；FEVEROUS-S四个集合内均无exact claim重复。论文使用validation做最终报告，缺少独立公开test；prompt、解析器或模型大小若根据这些结果调过，会产生validation overfitting风险。

## 表1：7/8最佳属实，但提升高度依赖设置

Macro-F1：ProgramFC N=5在8个gold/open设置中7个最高；唯一例外是HOVER 2-hop gold，75.65低于DeBERTaV3-NLI 77.22。主要结果：

- HOVER2：75.65 gold / 70.30 open；
- HOVER3：68.48 / 63.43；
- HOVER4：66.75 / 57.74；
- FEVEROUS-S：92.69 / 68.06。

Open-book相对gold分别下降5.35、5.05、9.01、24.63点，说明FEVEROUS-S最大瓶颈是检索/结构化表信息被排除，而不是最终逻辑。不能只用gold结果描述真实RAG能力。

“few-shot”也须谨慎：所有方法只新增20个in-domain例，但RoBERTa/DeBERTa/MULTIVERS已在FEVER、NLI等数十万监督例上训练，Codex/FLAN也有大规模预训练/指令训练。它是20-shot域适配，不是总监督相等。

表1没有置信区间。BERT/LisT5用10 seeds平均，其他大型模型与20-example prompt看起来是单配置；不同方法的不确定性不对称。应对demonstration选择、顺序、program采样、子模块生成和retrieval同时做层级bootstrap。

## “分解优于一步”与百分比口径

N=5相对直接FLAN-T5的绝对F1增量：gold为1.96、2.82、8.67、1.88，平均3.83点；open为1.28、3.20、2.32、4.33，平均2.78点。论文的“6.0%/4.5%”是约相对增幅，不是百分点。

4-hop gold的14.9%来自`(66.75-58.08)/58.08`；open所称6.7%更接近N=1的`(59.16-55.42)/55.42`，而N=5只有4.2%。正文在不同设置似乎选取不同N版本，引用时应直接给原始F1。

ProgramFC对小sub-task模型尤其有效：4-hop中FLAN-small端到端48.59，ProgramFC+small62.46；接近端到端FLAN-XXL63.39。但这不是“80M系统对11B系统”：规划器仍是大型Codex，且多次调用检索和80M模块。论文也承认总时间约端到端FLAN的4–5倍。

## N=5投票不是稳定单调收益

N=5减N=1的8项增量为1.55、.94、2.35、2.80、1.06、**-1.42**、.92、.26，全部平均约1.06点；若只平均7个正增量约1.41，才接近正文“1.5%”。HOVER4 open从59.16降至57.74，说明多数采样可把共享planner偏差放大。

五个程序来自同一模型、同prompt，非独立验证。应报告program文本/步骤多样性、错误相关、投票margin和调用成本；比较best-of-N需要oracle，majority-of-N则必须包括退化项，不能只报正向平均。

## 迭代检索的证据与口径（PDF7）

图5的recall@10：one-step→ProgramFC为HOVER2 73.18→77.13、HOVER3 51.33→59.17、HOVER4 36.43→49.93、FEVEROUS-S76.25→85.65。HOVER4相对增幅`(49.93-36.43)/36.43=37.1%`，正文口径正确；绝对增量13.50点。程序能用中间答案构造新query，机制可信。

不过ProgramFC多步骤各检索，最终再从所有结果取top10；一步基线只有一次query，比较没有固定检索调用/候选预算。优势同时来自分解与更多查询。应画相同总BM25调用、top-k和latency预算下的recall，并报告最终答案对gold evidence recall的条件性能。

当前README执行命令`num_retrieved=5`，论文主实验说baselines top10，图5又汇总所有步骤后取top10；代码对每步直接追加top-k结果，未见跨query全局score校准。当前复现配置与论文检索评估需另行对齐。

## 错误分析只条件于“已经答错”的300例

作者从HOVER最终错误中每hop抽100条。P(syntax/semantic/execution | final wrong)：syntax均0；semantic为29%、38%、77%；其中4-hop structure error57%；execution error为71%、62%、23%。这说明随着hop增加，错误重心从子模块转到program结构。

这些比例不是全体程序错误率：只看最终错例会漏掉“错误程序碰巧答对”，也不能由2-hop的71% execution error推出71%的所有程序正确。没有报告标注人数、agreement、抽样seed和N=1/N=5哪种程序。更完整设计应对正确/错误预测都抽样，分别标program semantics、每步证据、函数输出与最终逻辑。

论文称300例无syntax error，但当前执行器对很多异常实行随机fallback；“可解析”也可能只是宽松parser接受，而非语法/逻辑正确。

## Closed-book结果：参数知识仍接近随机，ProgramFC并非普遍最好

ProgramFC closed-book为HOVER2/3/4 54.27/54.18/52.88、FEVEROUS59.66；InstructGPT CoT为57.20/53.66/51.83/61.05。ProgramFC只在HOVER3/4最好，2-hop和FEVEROUS由CoT更高。HOVER平衡，50附近确实接近随机；这支持复杂事实核验需要外部知识，而非仅靠更漂亮的推理格式。

不同模型规模、API家族和prompt不统一；ProgramFC还串联Codex与FLAN，不能将差异单独归因symbolic program。应做同一planner/solver下program vs free-CoT、同调用预算与同temperature比较。

## 当前源码暴露的执行语义与复现风险

官方README说明论文结果主要用已退役`code-davinci-002`，当前代码改用`text-davinci-003`。README给出的N=1新结果与论文相近但不同，例如HOVER2 gold75.03 vs论文74.10、open70.55 vs69.36。模型迁移结果不能当原表复现；而text-davinci-003如今也不可稳定重跑。

更关键的是当前`program_execution.py`：

1. 文档宣称Predict支持AND/OR/NOT，`derive_final_answer`实际只按字符串`" and "`切分。OR/NOT无法按声明语义执行；论文附录恰有正确程序应为`not(fact1 and fact2)`的例子。
2. 找不到逻辑变量时只报警但保持`final_label=True`，缺失argument会偏向SUPPORTED；parse/execution异常和无法映射的verifier回答则用未设seed的随机True/False。
3. 多程序最终`true_count > false_count`才SUPPORT，否则REFUTE；平票、空program或None占位都偏REFUTE。生成API失败会留下少于N个program，分母未审计。
4. verifier只接受精确`true/false/yes/no/it's impossible to say`，其中“impossible to say”被硬映射False；unknown不等于refuted。其他输出随机，结果非确定。
5. generator批请求失败后逐条重试，再失败只打印，不记录失败状态；最终文件仍包含样本但program数可变。
6. program parser用宽松regex和字符串替换；若FINAL不是最后一步，循环后`final_answer`可被后续命令重置为None。

因此当前源码不能忠实执行论文所宣称的完整逻辑语言，正式表可能来自不同内部版本。需实现AST白名单解释器、三值逻辑、显式错误状态和deterministic seed，并发布论文时raw programs/results。

## Prompt与模型说明的细节问题

FEVEROUS-S的20-shot prompt中Alfredo Cornejo Cuevas同一claim出现两次、程序略有不同，实际unique demonstration少于20且对该结构加权。HOVER prompt也含拼写/模板错误（如`predict`大小写、转义异常），parser宽松度可能影响结果。

Appendix A.3写“FLAN-T5-XXL 3B”，但标准命名和Figure4均是XL=3B、XXL=11B；当前代码默认`flan-t5-xl`。论文表1实际应理解为XL 3B，引用需纠正命名而非照抄“XXL 3B”。

代码MIT许可；仓库含处理后的claims但完整Wikipedia索引需另构建。当前HOVER重复/冲突claim计数应加入任何复现实验报告。

## 可进一步开展的实验

1. **严格AST执行器：**解析Question/Verify/Predict，完整实现AND/OR/NOT、括号和三值UNKNOWN；所有错误单列而非随机/默认真。
2. **固定预算：**ProgramFC、CoT、Self-Ask用相同LLM tokens、BM25调用数、候选段和wall-clock，画性能—成本曲线。
3. **逐阶段oracle：**gold program、gold intermediate answer、gold evidence、gold verifier分别替换，估计planner/retriever/QA/logic条件误差。
4. **全体解释审计：**正确与错误预测都抽样，标program completeness、每步支持、反事实删除后的prediction change；给annotator agreement。
5. **多程序相关性：**按program结构cluster后投票，比较随机5条、五个近重复和跨planner ensemble；报告margin与有效样本量。
6. **重复claim处理：**HOVER按claim cluster评价，解释相同文本相反标签；open/closed条件下将不可识别的evidence-conditioned标签冲突单列。
7. **隐式推理与自然claim：**针对时间不可能、常识桥接、数量比较及真实政治claim构造测试，验证作者已承认的implicit decomposition缺口。
8. **版本迁移：**用当前可用开源planner重生成并固定raw programs；与论文Codex和仓库text-davinci-003结果做同样本配对比较。

## 对综述可使用的结论

ProgramFC提供了很有价值的“planner—tools—logic”事实核验范式：在7/8 few-shot设置领先，迭代query尤其改善深层证据召回，且错误分析显示4-hop主要难在program结构。它适合作为幻觉评估中“将复杂回答拆成可执行核验计划”的方法依据。但性能来自大型planner、多个子调用和更多检索预算；N=5并非单调有效，4-hop open反而下降。当前公开执行器只真正实现AND并用随机/默认策略处理异常，与论文宣称的逻辑库不一致；解释也只在最终错例上审计。高质量复现必须保存raw program、严格执行语义、显式UNKNOWN并逐阶段追踪错误。
