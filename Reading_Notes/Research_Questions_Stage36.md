# 第三十六阶段：KG一致性需要开放世界、否定量词与版本化数据审计

I047全文15页、完整附录、五张关键页及当前官方源码已审计。当前完成105/124（核心16、重要89），剩余19。详见`notes/important/I047_FACTKG.md`。

## 核心发现

FACTKG论文版108,674条，五类推理与三类风格；GEAR图证据accuracy77.65，较最佳claim-only BERT65.20高12.45点，但Multi-hop68.84反低于BERT70.06。结果支持多数合成类型利用图信息，不代表真实世界事实核验已解决。

标签实质是DBpedia 2015闭世界一致性。实体四跳外和缺边不证明现实为假；“I imagined P”被标为P反面不成立；multi-hop否定还混淆`¬∃path`与`∃nonmatching path`。结构问句被当二值claim，也应拆为presupposition satisfaction。

README承认当前数据修错后baseline可能与论文不同。源码test DataLoader `drop_last=True`会漏尾批；`best_param=model.state_dict()`未deepcopy；fallback用未统一seed的Python随机；train/dev用gold Evidence而test用预测relation/hop；Flan当前生成+子串解析与论文token概率描述不同。当前数据Drive不可访问，历史表未重算。

## 后续综合问题

- 对修正版pickle做计数、重复、跨split实体/关系/source graph和历史diff审计。
- 将缺边改为UNKNOWN，REFUTED要求显式互斥或反证。
- 用一阶逻辑执行negation、conjunction和多路径，区分`¬∃`与`∃¬`。
- 把embedded truth、utterance truth和presupposition satisfaction分开。
- 同一fact的written/colloquial成对评价，避免跨测试集难度比较。
- 报relation/hop/path recall及gold/shuffled/wrong evidence因果消融。
- 用自然LLM生成错误检验模板KG检测器的跨分布能力。
