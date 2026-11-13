# 销售与商务拓展案例｜可打印输入数据

**教学模拟 · 可打印输入数据。** 本页仅整理原始输入，不提供计算答案。金额、人数、记录和假设均不是客户成果。与本案例题面及其口径说明配合使用。版本日期：2026-11-13。

## 1. 账户记录

原始文件：[accounts.csv](accounts.csv)。以下中文是原 CSV 文字字段的翻译。账户均虚构；同一账户在三个表中按字段展开。

| 账户 | 行业 | 团队人数 | 需求信号 |
| --- | --- | --- | --- |
| Aster | 批发 | 20 | 人工重复录单 |
| Birch | 软件 | 12 | 希望工资结算自动化 |
| Cedar | 分销 | 40 | 重复订单及手工报表 |
| Dune | 批发 | 15 | 与现供应商讨论续约 |


| 账户 | 沟通对象 | 预算状态 | 时间 |
| --- | --- | --- | --- |
| Aster | 运营经理 | 尚未确认 | 本季度评审 |
| Birch | 未知 | 尚未确认 | 尚无日期 |
| Cedar | 运营与财务 | 已讨论预算范围 | 本季度提案 |
| Dune | 财务负责人 | 预算已确认 | 本季度决策 |


| 账户 | 适配记录 |
| --- | --- |
| Aster | 核心订单流程相符 |
| Birch | 产品不支持工资结算 |
| Cedar | 适配需验证集成 |
| Dune | 谈判中，合同未签 |


数据字典：`account` 为账户；`industry` 为行业；`team_size` 为团队人数；`pain_signal` 为需求信号；`decision_contact` 为当前沟通对象记录；`budget_status` 为预算状态；`timing` 为时间；`fit_note` 为适配记录。沟通对象的审批职责仍按题面进行发现与核实，未知项不补造。

## 2. 未签机会记录

原始文件：[pipeline.csv](pipeline.csv)。金额为年度合同额 CU；概率是题设假设，非历史校准结果。

| 账户 | 年度合同额 | 记录阶段 | 概率假设 |
| --- | --- | --- | --- |
| Aster | 12,000 | 已标合格 | 0.4 |
| Birch | 18,000 | 未合格 | 0 |
| Cedar | 24,000 | 提案 | 0.6 |
| Dune | 10,000 | 谈判 | 0.8 |


| 账户 | 原表合格标记 | 季度 |
| --- | --- | --- |
| Aster | 1 | 2026-Q4 |
| Birch | 0 | 2026-Q4 |
| Cedar | 1 | 2026-Q4 |
| Dune | 1 | 2026-Q4 |


数据字典：`annual_contract_value_cu` 为年度合同额；`stage` 的 `qualified`、`unqualified`、`proposal`、`negotiation` 对应上表阶段；`probability_assumption` 为 0 至 1 的比例；`qualified` 为原表的 1／0 标记，保留供核对；`quarter` 为季度。全部机会尚未签约，不能将记录金额当已实现收入。

## 3. Aster 价值假设与目标口径

原始文件：[value_assumptions.csv](value_assumptions.csv)。本页只列输入；兑现比例不是已经节省的现金。

| 参数 | 输入值 | 单位 |
| --- | --- | --- |
| 使用人数 | 20 | 人 |
| 每人每周手工耗时 | 2 | 小时 |
| 年度工作周数 | 48 | 周 |
| 每小时容量价值 | 25 | CU／小时 |
| 年度订阅费 | 12,000 | CU |
| 一次实施费 | 2,000 | CU |
| 基准兑现比例 | 0.6 | 比例，0 至 1 |
| 保守兑现比例 | 0.2 | 比例，0 至 1 |
| 季度目标：年度合同额 | 100,000 | CU，年度合同额 |


数据字典：`parameter` 为参数名，`value` 为值，`unit` 为单位。参数依次对应 `users`、`manual_hours_per_user_per_week`、`working_weeks`、`hourly_capacity_value`、`annual_subscription`、`one_time_implementation`、`base_realization_rate`、`downside_realization_rate`、`quarter_quota`。年度工作周、容量价值、费用和兑现比例的含义及未计成本，沿用题面。

本页不计算合格管线合计、加权管线、情景价值或推荐会议顺序。
