# 第三十五阶段：真实事实核查必须同时约束证据时间、来源、覆盖与摘要忠实性

I046全文19页、全部实质附录、六张关键页及当前官方源码已审计。当前完成104/124（核心16、重要88），剩余20。详见`notes/important/I046_Complex_Claim_Verification_with_Evidence_Retrieved_in_the_Wild.md`。

## 核心发现

无约束检索测试Acc49.0，排除事后网页与fact-check站后仅33.0；claim-only为25.5。MultiFC中82.7% claims至少检到一个排除站点，说明常见web检索评价存在强烈事后答案泄漏。generated subquestions胜原claim，但也用了10问而gold平均3问，尚未匹配查询预算。

few-shot摘要单对faithful/minor为89%，仍有11% major/wrong；聚合到4摘要/claim后50条中12条至少一处严重错。更忠实few-shot摘要的answerable/partial覆盖为64.0%，反低于zero-shot的70.2%，说明模型可用幻觉提高表面完整性。严格全部subquestions answerable仅6/50，宽松无完全unanswerable也仅14/50。

源码与论文配置不完全一致：top-4 vs默认top-5、zero-shot vs默认few-shot；README有文件名/命令拼写问题，无时间检索终检检查错字段，且源码含应撤销的硬编码API凭据。正文与附录还把faithfulness/comprehensiveness招募人数15/17对调。官方数据包当前不可访问，表值未独立重算。

## 后续综合问题

- 建立冻结网页快照与live-search双轨，核对首次发布时间和版本，而非仅信URL元数据。
- generated/gold/claim按相同query、页数、tokens和成本比较。
- 以subquestion覆盖×atomic-claim支持二维评价，禁止把参数知识补写算coverage。
- raw/extractive/abstractive/oracle在相同251-token预算下分离压缩与生成收益。
- 增设“证据不足/不可核查”，报告选择性风险和人工追加检索收益。
- 追踪检索→抓取→BM25→摘要→裁决的条件错误传播，并做真实人机协作实验。
