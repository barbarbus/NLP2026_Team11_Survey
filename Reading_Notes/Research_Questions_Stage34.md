# 第三十四阶段：置信度校准、失败排序与选择性风险是三种不同能力

I045 ICLR论文29页、正文与完整附录、六张关键页及当前官方源码已审计。当前完成103/124（核心16、重要87），剩余21。详见`notes/important/I045_Can_LLMs_Express_Their_Uncertainty.md`。

## 核心发现

论文把黑盒置信度方法拆为prompt、sampling、aggregation，并以ECE与AUROC/AUPRC评价。GPT-4在GSM8K CoT准确率93.6%、几乎全报100%，ECE仅.064却难以区分错误，是“低ECE不等于知道何时会错”的直接证据。

GPT-3.5五域中Self-Random+Consistency由单答CoT的平均AUROC`.564`升至`.730`；但同模型采样相关、temperature不同，Consistency也会稳定确认共同错误。表4 Pair-Rank平均ECE`.069`最低、AUROC`.676`最高；Avg-Conf虽在6域中5域AUROC最高，却被GSM8K`.410`拉低到平均`.669`，说明局部胜率、宏平均和任务风险不可互换。

源码确认ECE为10 bins、AUROC/PR-P以正确为正、PR-N以错误为正。当前Top-K/Pair-Rank脚本保留断点且函数调用参数不匹配；Pair-Rank无seed、损失与常见负对数似然不同；结果CSV表头漏AURC导致列错位。论文表值与当前代码可执行性必须分开报告。表13的Top-K GSM8K ECE39.8也与表3/10的19.6冲突。

## 后续综合问题

- 统一报告proper score、校准、错误AP/AUROC和risk-coverage，给成对question bootstrap。
- 固定一次答案只估confidence，分离不确定性估计与答案改变。
- 用稳定错误、错误前提、同义答案与claim级开放文本压力测试一致性。
- 按总tokens/API成本画M=1…13收益，比较检索核验和外部验证器。
- 修复Pair-Rank复现链并发布raw responses；验证ratio损失、seed与候选缺失敏感性。
- 将回答级置信度扩为世界正确性×上下文支持×不可核验的claim级风险。
