# 金融与会计案例｜可打印输入数据

**教学模拟 · 可打印输入数据。** 本页仅整理原始输入，不提供计算答案。金额、人数、记录和假设均不是客户成果。与本案例题面及其口径说明配合使用。版本日期：2026-11-13。

## A1. 预算与实际驱动因素

原始文件：[pnl-inputs.csv](pnl-inputs.csv)。适用于 FP&A 主案例，同一完整月、同一产品；金额为人民币元，数量为件。`scenario` 的 `budget` 为预算，`actual` 为实际。

| 输入项目 | 预算 | 实际 |
| --- | --- | --- |
| 销量（件） | 10,000 | 11,000 |
| 单价（元／件） | 100 | 96 |
| 单位变动成本（元／件） | 60 | 62 |
| 固定经营费用（元） | 180,000 | 200,000 |
| 折旧（元） | 20,000 | 20,000 |
| 利息（元） | 10,000 | 12,000 |


字段依次为 `units`、`price_cny`、`variable_cost_cny`、`fixed_opex_cny`、`depreciation_cny`、`interest_cny`。经营费用不含另列的折旧与利息。

## A2. 与现金桥相关的余额

原始文件：[working-capital.csv](working-capital.csv)。金额为人民币元。不是完整资产负债表。

| 科目 | 月初 | 月末 |
| --- | --- | --- |
| 应收账款 | 200,000 | 356,000 |
| 存货 | 300,000 | 348,000 |
| 应付账款 | 150,000 | 220,000 |
| 应计经营费用 | 40,000 | 60,000 |


数据字典：`account` 为科目；`opening_cny` 为月初余额，`closing_cny` 为月末余额。科目依次对应 `accounts_receivable`、`inventory`、`accounts_payable`、`accrued_operating_expenses`。

## A3. 实际现金收支

原始文件：[cash-flows.csv](cash-flows.csv)。金额为人民币元。金额均按正值记录，方向由 `direction` 指定；期初余额不是本期流入。

| 项目 | 金额 | 方向 |
| --- | --- | --- |
| 期初现金 | 100,000 | 期初余额 |
| 客户回款 | 900,000 | 流入 |
| 采购付款 | 660,000 | 流出 |
| 经营付款 | 180,000 | 流出 |
| 利息付现 | 12,000 | 流出 |
| 资本开支 | 40,000 | 流出 |
| 新增借款 | 0 | 流入 |
| 偿还本金 | 0 | 流出 |
| 分红 | 0 | 流出 |


数据字典：`item` 为现金项目；`amount_cny` 为金额。`opening_balance` 表示期初余额，`inflow` 为流入，`outflow` 为流出。项目依次为 `opening_cash`、`customer_collections`、`supplier_payments`、`operating_payments`、`interest_paid`、`capital_expenditure`、`new_borrowing`、`principal_repayment`、`dividends`。上述三表的 `data_type` 均为 `synthetic`。

## B. 核算与审计：六条原始记录

原始文件：[invoice-sample.csv](invoice-sample.csv)。此组金额独立于 A，不可混入 FP&A 主案例。金额为人民币元。每条 `row_id` 是独立原始记录，不按发票号先行去重。

| 记录号 | 发票号 | 供应商 | 采购单 |
| --- | --- | --- | --- |
| R1 | I001 | V001 | P001 |
| R2 | I002 | V002 | P002 |
| R3 | I003 | V003 | P003 |
| R4 | I003 | V003 | P003 |
| R5 | I004 | V004 | P004 |
| R6 | I005 | V005 | P005 |


| 记录号 | 发票日期 | 接收日期 | 记账日期 |
| --- | --- | --- | --- |
| R1 | 2026-09-27 | 2026-09-28 | 2026-09-29 |
| R2 | 2026-09-29 | 2026-10-02 | 2026-09-30 |
| R3 | 2026-09-20 | 2026-09-21 | 2026-09-22 |
| R4 | 2026-09-20 | 2026-09-21 | 2026-09-22 |
| R5 | 2026-09-26 | 2026-09-27 | 2026-09-30 |
| R6 | 2026-09-30 | 2026-09-30 | 2026-10-02 |


| 记录号 | 金额（元） | 银行后缀 |
| --- | --- | --- |
| R1 | 10,000 | 1234 |
| R2 | 18,000 | 5678 |
| R3 | 12,000 | 1111 |
| R4 | 12,000 | 1111 |
| R5 | 25,000 | 9999 |
| R6 | 9,000 | 2222 |


字段对应：`row_id`、`invoice_id`、`vendor_id`、`po_id`；三类日期分别为 `invoice_date`、`received_date`、`posting_date`；金额为 `amount_cny`；四位银行后缀为 `bank_suffix`，不是完整账号。`data_type` 为 `synthetic`。检查截止日、接收证据、原银行后缀及本题费用确认规则见 B 题面。

## C. 信用练习：未来 30 天预测

原始文件：[credit-forecast.csv](credit-forecast.csv)。金额为人民币元；`base_cny` 为基准，`downside_cny` 为下行。`data_type` 为 `synthetic_assumption`，均非已实现结果。

| 项目 | 基准 | 下行 |
| --- | --- | --- |
| 期初现金 | 108,000 | 108,000 |
| 客户回款 | 800,000 | 720,000 |
| 采购付款 | 640,000 | 640,000 |
| 经营付款 | 180,000 | 180,000 |
| 利息 | 12,000 | 12,000 |
| 现有债务到期本金 | 20,000 | 20,000 |
| 资本开支 | 0 | 0 |
| 最低现金缓冲 | 80,000 | 80,000 |


`item` 依次对应 `opening_cash`、`customer_collections`、`supplier_payments`、`operating_payments`、`interest`、`existing_debt_principal_due`、`capital_expenditure`、`minimum_cash_buffer`。最低缓冲是题设要求，不是现金支出。其余预测范围与忽略项见 C 题面。

## D. 公司研究：可比与目标公司

原始文件：[valuation-comps.csv](valuation-comps.csv)。收入、企业价值、净债务单位为百万元人民币；普通股单位为百万股。以下 “—” 对应 CSV 空值，不代表零。

| 公司 | 收入 | 企业价值 |
| --- | --- | --- |
| Peer_A | 100 | 300 |
| Peer_B | 120 | 480 |
| Peer_C | 80 | 400 |
| Target | 50 | — |


| 公司 | 净债务 | 普通股（百万股） |
| --- | --- | --- |
| Peer_A | — | — |
| Peer_B | — | — |
| Peer_C | — | — |
| Target | 8 | 10 |


数据字典：`company` 为公司代号，`Peer_A/B/C` 为三个可比，`Target` 为目标；其余字段为 `revenue_cny_million`、`enterprise_value_cny_million`、`net_debt_cny_million`、`shares_million`。`data_type` 为 `synthetic`。Target 的企业价值为待计算项；可比公司的净债务和股数未提供。统一期间与其他价值调整条件见 D 题面。
