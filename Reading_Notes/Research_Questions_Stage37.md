# 第三十七阶段：程序化核验要把planner、retrieval、solver和logic错误逐层分开

I048全文22页、全部附录与prompt、五张关键页、官方源码及公开claims已审计。当前完成106/124（核心16、重要90），剩余18。详见`notes/important/I048_ProgramFC.md`。

## 核心发现

ProgramFC N=5在8个gold/open设置中7个最高，但HOVER2 gold低于DeBERTa。HOVER4 open的N=5还由N=1的59.16降至57.74；八项平均增量约1.06点，不是无条件1.5。迭代检索HOVER4 recall@10从36.43升49.93，相对+37.1%，但用了多次query，预算未匹配。

300例错误分析是条件比例：4-hop最终错例中77% program semantic error、23% execution error，不能当总体程序错误率。80M solver接近11B端到端的比较仍包含大型Codex planner和多次调用。

当前执行器只实现字符串AND，OR/NOT未执行；缺变量默认真，异常/未知回答随机，平票偏REFUTE且无统一seed。论文Codex已退役，仓库迁移text-davinci-003；FLAN“XXL 3B”实际应为XL 3B。当前HOVER dev有18组exact重复claim，1组相反标签；train有116组、8组标签冲突。

## 后续综合问题

- 用AST和三值逻辑完整执行AND/OR/NOT，错误显式计数，禁止随机fallback。
- gold program/answer/evidence/verifier逐层oracle，构建错误传播矩阵。
- 同LLM tokens、检索调用和延迟比较ProgramFC/CoT/Self-Ask。
- 对正确与错误输出都做人评，验证每步证据和删除解释后的因果变化。
- 对程序结构聚类后投票，测N个样本的相关性与有效多样性。
- HOVER按unique claim聚类，单列同文本相反标签与evidence-conditioned不可识别项。
- 用开源planner固定raw programs，做Codex→替代模型版本迁移审计。
