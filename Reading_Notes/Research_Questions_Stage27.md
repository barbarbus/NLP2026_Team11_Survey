# 第二十七阶段：HaluEval2.0的裁判提示、有效回答分母与“micro”名称

I024 ACL2024 21页正文/全部附录与官方仓库`metric.py`/`judge.py`已读。当前96/124（核心16、重要80），剩余28；完整证据见`notes/important/I024_Dawn_After_Dark.md`。

## 关键发现

基准8770题由三次ChatGPT回答BERTScore低相似筛出，绝对幻觉率面向困难题而非自然问题分布。每回答至多抽五事实，只把GPT-4判FALSE当错。可靠性实验报91.5–94.7%“匹配率”，没有假事实的precision/recall。

PDF16表10事实核验示例把两条罗斯福事实标FALSE，但“纠正”与原命题相同；滑铁卢第三句标FALSE却给另一事实作纠正。静态`metric.py`先删无judge/无事实样本，MaHR分母是**有效被抽事实回答**；MiHR是逐回答错误比例的平均，不是pooled facts的micro。`judge.py`解析不足时补UNKNOWN，会压低FALSE率。现行master未固定为原论文提交。

多项“缓解”结果非全域一致：检索使ChatGPT生医MaHR`48.75→23.98`但金融MiHR`13.55→15.25`；RLHF使Alpaca科学MiHR`13.15→13.83`；few-shot CoT让ChatGPT教育MiHR`17.19→25.22`。PDF7表4与PDF9表7的Llama2 top-p科学列不一致。

## 待实验

固定原始预测和论文提交，统计各组过滤/拒答/UNKNOWN/事实数，重写正确few-shot后只重跑裁判，以人工分层标签评估误差；多策略比较正确事实量、回答完整性和时点，而非仅MaHR下降。
