# 第四十五阶段：信念树概率传播的校准与逻辑边风险

I060全文24页及全部附录提示核对完成。当前114/124（核心16、重要98），余10。详见`notes/important/I060_BTProp.md`。

BTProp用前120个有标签Wikibio样本估计发射概率，还在验证集调改写子节点`.8/.2`，因此不是纯零资源。FELM-Science AUC-PR相对SelfCheckGPT升6.6/8.7点，但Wikibio两个backbone都落后，FactCheckGPT提升1.5–3.4点。测试阈值选择、NLI树边、独立性和改写信心设1都影响解释；Llama提示把需外部核查的unknown当false，图14示例有明显错位。官方仓库固定版本只有README，暂无可复现代码。建议独立校准、人工树边审计、同预算比较及真实概率校准验证。
