# 第四十八阶段：问前风险探针与实际路由差距

I067全文11页及附录核对完成。当前117/124（核心16、重要101），余7。详见`notes/important/I067_DRIFT.md`。答案token模式12格中10格最佳，question-only并非全优；所谓Qwen NQ+13点仅与Halo question特征比，若比Halo answer则更低。TriviaQA留存80%准确91.6%是拒答曲线，尚无真实fallback路由实验；`<.1%`与零延迟缺端到端实测。方法用一次答案的GPT-4o正确性监督，与通用幻觉真值有距离。后续需固定layer独立验证、按实体/模板拆分、审计judge及真实路由成本。
