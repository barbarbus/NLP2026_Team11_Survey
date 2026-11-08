# 第四十四阶段：模块化事实核查的抽取、证据与裁决误差

I059全文19页、附录表及作者仓库静态核验完成。当前113/124（核心16、重要97），余11。详见`notes/important/I059_Self_Checker.md`。

BingCheck有396条Bing Chat长答、3840个claim。Self-Checker response准确63.4%，证据句P30.5/R86.1/F1 45.0；FEVER score47.9 vs BEVERS77.7，WiCE verdict F1 47.7 vs T5-3B65.3。用系统输出预填人工标注有锚定风险。官方仓库目前401个数据JSON，README脚本名/评测命令错误，BingCheck温度0与论文.2不符；本地已剔除疑似凭据文件。关键问题是：独立抽claim的遗漏、部分支持的过度判定、时点/来源筛选、同成本模块消融，以及“证据一致”与现实真值分轴。
