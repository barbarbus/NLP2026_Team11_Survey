# 第三十八阶段：结构化原子化必须同时验证覆盖率、聚合校准和纠错独立性

I050全文12页、全部prompt和六张关键页已审计。当前完成107/124（核心16、重要91），剩余17。详见`notes/important/I050_GraphEval.md`。

## 核心发现

GraphEval用Claude 2把回答转为自由文本三元组，再由NLI逐triple对完整context核验；任一概率>.5就判整段不一致。它本质是claim decomposition接口，并未对context建图或做图推理。

表2九格的简单平均增量是4.84点；按1600/235/239样本量加权才是论文所报6.2点。8/9格不降，HHEM在QAGS-X由75.5降75.2。论文未说明SE=1.3的独立单位。输出越长通常triple越多，max聚合会机械提高至少一次误报概率，因此“长文本收益”需与多重检验/长度效应拆开。

论文没有人工测KG抽取的事实覆盖和scope保真，故“系统检查所有信息”未获支持。Claude 2用默认temperature 1且无seed/重复、raw completion或parser，严格复现受限。

GraphCorrect的27个ROUGE格全更接近原文，只能证明局部编辑较保守。所谓修复率由同一GraphEval框架先选错再验收，存在循环自评、选择偏差和检测器规避；两项QAGS-X设置还不如Direct Prompt。作者在discussion承认需要人工评价。

## 后续综合问题

- 建立atomic proposition+span金标，测triple覆盖、scope/negation/quantity/coreference保真。
- 同NLI/调用预算比较句切分、OpenIE、LLM claims和KG，隔离“图结构”贡献。
- 按词数/triple数校准max规则，比较noisy-OR、top-k与FDR控制。
- 多seed重抽KG，测集合Jaccard、标签翻转、解析失败和版本漂移。
- 用blind人工/异构裁判独立评价修复，记录正确被改坏、删除逃逸和新引入错误。
- 多triple修复测试顺序冲突，联合报告正确性、信息保存、语言质量和成本。
- 扩展到QA、RAG、长文、数值/时间/否定和多语言，验证domain-general声明。
