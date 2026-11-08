# 第三十二阶段：ICL裁判学习的不只是rubric，还有标签分布

I034 ICE本地7页正文/附录、三页关键图表及官方仓库实现已审计。当前完成101/124（核心16、重要85），剩余23。详细证据见`notes/important/I034_ICE.md`。

## 核心发现

ICE用4个SummEval专家示例让`text-davinci-003`输出0–1多维分。4篇示例文章的全部64摘要从测试删除，避免同source泄漏；但示例/测试仍共享benchmark、领域、rubric和系统风格。

表1中uniform consistency的`ρ=.486, τ=.466`确实最好；relevance只有τ`.384`最好，ρ`.467`低于CTC`.495`。stratified consistency降至`.298/.263`，表明示例标签先验会拉动预测。200条、3个seed的最大波动目视接近9点，不能强称稳健。

GPT-3/BRIO/T0实验只在三个系统均值上与人排序一致，无样本相关/显著性；judge与GPT-3输出同家族，有self-bias替代解释。发布脚本实际只请求1个completion并关闭文字rubric；解析以正则取第一段数字且不验0–1。缓存consistency仅4个预测值，1326/1536为1.0，严重饱和；旧模型已经退役，当前README仍无完整复现说明。官方main源码包已保存到资料库。

## 后续综合问题

- 区分ICL在学习rubric、分数尺度和benchmark先验中的贡献。
- 用article-cluster bootstrap、尾部PR-AUC/召回与分段校准替代单一相关。
- 混合真实分布示例与罕见错误覆盖，不让uniform忽略严重幻觉尾部。
- 交叉judge×generator家族并控制长度/风格，测self/family preference。
- 让judge定位unsupported span和source证据后评分，同时审计解析失败与越界。
