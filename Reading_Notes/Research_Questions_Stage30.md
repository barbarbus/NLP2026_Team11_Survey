# 第三十阶段：工具统一的是流水线，不是真值语义

I032 FACTOOL本地25页正文/完整提示/失败案例及官方仓库README已读。当前99/124（核心16、重要83），剩余25。详细证据见`notes/important/I032_FACTOOL.md`。

## 核心发现

四任务分别测世界事实支持、有限测试代码正确、局部算术正确和引文元数据存在，不能共用一个“事实性”解释。表5以factual=True为正类：科学响应10正/90负下GPT-4 FACTOOL为TP9/TN90/FP0/FN1，才得到99% accuracy、90% recall、100% precision；若把幻觉当正类会把指标方向读反。

claim抽取表4用最大ROUGE/BERTScore的方向平均，重复机器claim可复用同一gold；汇总P/R也不能复算所列F1。KB/数学/科学的response只要任一claim错即False，强受claim数/长度影响。

附录直接展示同错oracle：HumanEval/36、/79的候选解多数与待测代码共享bug；数学Kylar例全部局部算术成立却整体建模错；KB把正确但“不够完整”的Sotomayor命题判False。排行榜仅60题，并用KB响应F171.79、数学80.36的FACTOOL代理当gold；GPT-4 43.33%其实26/60。

## 待执行

固定论文提交和预测，重建正/负双方向混淆矩阵；逐阶段替换gold claim/query/evidence/judge；代码用隐藏/属性测试，数学加入全局方程逻辑，引文检查DOI与论点支持；排行榜独立盲审、匹配claim数并给区间。
