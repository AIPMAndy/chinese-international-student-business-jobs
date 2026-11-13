# 运营与供应链案例｜可打印输入数据

**教学模拟 · 可打印输入数据。** 本页仅整理原始输入，不提供计算答案。金额、人数、记录和假设均不是客户成果。与本案例题面及其口径说明配合使用。版本日期：2026-11-13。

## 1. 库存与费用约束

原始文件：[assumptions.csv](assumptions.csv)。金额为虚构货币 CU，数量为件。

| 参数 | 值 | 单位 |
| --- | --- | --- |
| 初始库存 | 120 | 件 |
| 到货后、需求前仓容 | 220 | 件 |
| 销售单价 | 30 | CU／件 |
| 周持有费 | 1 | CU／期末库存件／周 |


字段 `parameter` 依次为 `initial_inventory`、`warehouse_capacity_before_demand`、`sale_price`、`weekly_holding_cost`；`value` 为值，`unit` 为单位。仓容检查时点与持有费口径见题面。

## 2. 逐周需求

原始文件：[demand.csv](demand.csv)。`base` 为基本情景，`high` 为高需求情景；`week` 为周次，`demand_units` 为需求件数。

| 周次 | 基本需求（件） | 高需求（件） |
| --- | --- | --- |
| 1 | 80 | 80 |
| 2 | 100 | 100 |
| 3 | 140 | 180 |
| 4 | 100 | 120 |


## 3. 已承诺到货

原始文件：[scheduled_receipts.csv](scheduled_receipts.csv)。

| 到货周 | 件数 | 费用处理 |
| --- | --- | --- |
| 2 | 50 | 已承诺且各方案相同 |


字段为 `arrive_week`、`quantity_units`、`cost_treatment`；费用处理原值 `already_committed_common_sunk_cost`，按题面不重复计入方案新增采购费。

## 4. 可选采购机会

原始文件：[supply_options.csv](supply_options.csv)。同一采购机会在下面两表中按字段分块，不能将其视为两个不同下单机会。

| 采购机会 | 下单周 | 到货周 |
| --- | --- | --- |
| 正常采购 | 1 | 3 |
| 早期加急 | 1 | 2 |
| 后期加急 | 3 | 4 |


| 采购机会 | 最大数量（件） | 批量（件） | 单价（CU／件） |
| --- | --- | --- | --- |
| 正常采购 | 200 | 50 | 12 |
| 早期加急 | 100 | 25 | 17 |
| 后期加急 | 100 | 25 | 17 |


数据字典：`option` 的 `regular` 为正常采购，`expedite_early` 为早期加急，`expedite_late` 为后期加急；下单/到货周为 `order_week`、`arrive_week`；数量上限为 `max_quantity`，批量为 `lot_size`，单价为 `unit_cost_cu`。是否下单及件数由你决定，各项允许不下单。

本页不列参考采购数量。纸上交付可按“周次、期初、到货、需求、销售、缺货、期末”另画滚动表；可编辑空白表见 [purchase_plan_template.csv](purchase_plan_template.csv)。
