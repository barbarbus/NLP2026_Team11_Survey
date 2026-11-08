# 第三十九阶段：内部注意力新颖性需排除词面与标签筛选捷径

I051全文22页、实质附录和官方源码固定快照已审计。完成108/124（核心16、重要92），余16。详见`notes/important/I051_TOHA.md`。

TOHA的0阶拓扑量等价于prompt内部距离归零后的最小生成森林边权和，需100个有标注probe选头和头数；“training-free”不等于主结果零标签。CoQA/SQuAD标签先用ROUGE-L极端阈值筛选，再由GPT-4o审核，评价分布被选择。各任务差异显著：Mistral CoQA `.89`、SQuAD `.96`，但CNN/DM `.60`；Llama3.1 CoQA `.84`低于20次SelfCheck `.95`。全流程加速小于只算检测阶段7倍。迁移p>.05不能证明等效。当前官方配置`n_max=6`与论文10不一致。

待研究：source级split、全自然输出标签重审、保持词面和长度的事实最小对、头选择nested validation、构图对称化、跨域非劣检验和长context成本曲线。
