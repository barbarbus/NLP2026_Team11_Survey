# 第四十一阶段：多证据核验要验证“缺失”标签和规划预算

I053全文16页、实质附录和官方源码静态审计已完成。累计110/124（核心16、重要94），余14。详见`notes/important/I053_InteGround.md`。

四域1625题中，EB缺证条件的Llama8B准确18.8%、Claude3 Sonnet16.8%，支持过度蕴含风险；但WiCE只保留第一gold证据组，负例不一定真正缺证。表6 premise abduction 16格中9升7降，WiCE四检索器均降，不能说普遍改善；query expansion在MuSiQue四格均升。Recall@5是证据条目覆盖，不保证找齐全部必要证据。源码无原始缓存，LLM函数须用户实现，反思脚本含绝对路径和`eval`解析。

后续：多gold组/人工充分性、反事实知识、all-gold@5、统一query与LLM预算、concat与Borda分支核查，以及安全可重放的代码与缓存。
