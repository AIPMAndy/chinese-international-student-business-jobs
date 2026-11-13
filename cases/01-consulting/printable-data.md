# 咨询案例｜可打印输入数据

**教学模拟 · 可打印输入数据。** 本页仅整理原始输入，不提供计算答案。金额、人数、记录和假设均不是客户成果。与本案例题面及其口径说明配合使用。版本日期：2026-11-13。

## 1. 渠道订单与单均收入

原始文件：[channel-data.csv](channel-data.csv)。单位：订单为单；金额为人民币元。`baseline` 对应上期，`current` 对应本期；`dine_in` 为堂食，`delivery` 为平台外卖。各行 `data_type` 均为 `synthetic`。

| 期间／渠道 | 订单数 | 单均收入 |
| --- | --- | --- |
| 上期／堂食 | 12,000 | 40 |
| 上期／平台外卖 | 8,000 | 40 |
| 本期／堂食 | 10,000 | 40 |
| 本期／平台外卖 | 10,000 | 40 |


字段：订单数对应 `orders`；单均收入对应 `revenue_per_order_cny`。下表使用同一组期间与渠道，不能把两表重复计为新增订单。

| 期间／渠道 | 单均食材费 | 单均包装费 | 佣金比例 |
| --- | --- | --- | --- |
| 上期／堂食 | 14 | 0 | 0 |
| 上期／平台外卖 | 14 | 2 | 0.2 |
| 本期／堂食 | 15 | 0 | 0 |
| 本期／平台外卖 | 15 | 2 | 0.25 |


字段：食材费为 `food_cost_per_order_cny`；包装费为 `packaging_per_order_cny`；佣金为 `commission_rate`，按渠道收入计提，0.2 表示 20%。

## 2. 月固定费用

原始文件：[fixed-costs.csv](fixed-costs.csv)。金额为人民币元／月。各行 `data_type` 均为 `synthetic`。

| 费用项目 | 上期 | 本期 |
| --- | --- | --- |
| 人工 | 170,000 | 190,000 |
| 租金 | 100,000 | 100,000 |
| 其他固定费 | 30,000 | 30,000 |


字段依次为 `labor_cny`、`rent_cny`、`other_fixed_cost_cny`；期间仍由 `period` 标识。

## 3. 方案参数

原始文件：[options.csv](options.csv)。均为待验证预测输入，`data_type` 为 `synthetic_assumption`。方案 A、B、C 的适用范围、组合条件及服务限制以题面为准。

| 方案 | 参数 | 值 | 单位 |
| --- | --- | --- | --- |
| A | 外卖转自提订单 | 2,000 | 单／月 |
| A | 额外自提能力上限 | 2,500 | 单／月 |
| A | 自提单均包装费 | 2 | 元／单 |
| A | 自提佣金比例 | 0 | 比例，0 至 1 |
| A | 推广费 | 5,000 | 元／月 |
| B | 单均食材节省 | 1 | 元／单 |
| B | 新增质检费 | 2,000 | 元／月 |
| C | 人工节省 | 12,000 | 元／月 |
| C | 一次培训费 | 3,000 | 元，仅首月 |


数据字典：`option_id` 为方案；`parameter` 为参数名；`value` 为输入值；`unit` 为单位。参数中文依次对应 `delivery_to_pickup_orders`、`max_pickup_capacity`、`pickup_packaging`、`pickup_commission`、`promotion`、`food_saving`、`quality_cost`、`labor_saving`、`one_time_training`。

作答时先保留这些输入，再另建计算区；本页不含收入、贡献、利润桥或方案收益。
