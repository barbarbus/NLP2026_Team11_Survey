# 第三十三阶段：correctness、context faithfulness与abstention必须分报

I041 TACL论文18页、5张关键表、官方源码及公开人工标注已审计。当前完成102/124（核心16、重要86），剩余22。详见`notes/important/I041_Correctness_and_Faithfulness_QA.md`。

## 核心发现

双轴定义很重要：回答可世界正确但不受给定知识支持；附加信息不影响correctness，却影响all-response faithfulness。Recall与K-Precision分别偏好冗长覆盖和词面复制，需与长度、抽取性和claim标签一起解释。

正确性1200行实际是每数据集100题×4模型，问题重复；961 correct、210 incorrect、29 refuse合并为239负。Faithfulness公开包当前有560 relevant而正文写544；477/51/32为完全/部分/不支持，且部分被压成0。公开details还有91/79条仅一名worker，与双标叙述不一致。

表4 GPT-3.5胜FiD的6.48/10.27/9.33%是相对增幅，绝对3.53/6.22/5.75点；Recall不惩罚错误附加内容。表7把`I don't know`加入evidence，拒答会机械得到K-Precision满分；必须和gold条件误拒共同报告。

## 后续综合问题

- 建立world correctness × context support的claim级二维标签。
- 问题分组bootstrap与leave-model/domain-out，避免同题四响应伪独立。
- 用否定、矛盾附加句、source复制、同义改写测试Recall/K-Precision。
- 将拒答评价改为answerable/partial/conflict/unanswerable的coverage-risk。
- 固定论文时公开标注版本，解释544/560和单worker记录。
