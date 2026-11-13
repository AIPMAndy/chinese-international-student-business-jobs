-- 教学模拟。将 funnel.csv 导入同名表；数字列须为 INTEGER/REAL。
-- 每行是月度客户分组汇总，不是用户明细。
SELECT month,
       SUM(eligible_users) AS eligible_users,
       SUM(converted_users) AS converted_users,
       1.0 * SUM(converted_users) / NULLIF(SUM(eligible_users), 0) AS conversion_rate,
       SUM(revenue_cu) AS revenue_cu,
       1.0 * SUM(revenue_cu) / NULLIF(SUM(converted_users), 0) AS revenue_per_buyer
FROM funnel
GROUP BY month
ORDER BY month;

SELECT month, segment,
       1.0 * converted_users / NULLIF(eligible_users, 0) AS conversion_rate
FROM funnel
ORDER BY month, segment;

-- cohorts.csv 中空白 retained 表示窗口未成熟，不能补成 0。
SELECT cohort_month,
       CASE WHEN d30_eligible > 0
            THEN 1.0 * d30_retained / d30_eligible END AS d30_retention,
       CASE WHEN d60_eligible > 0
            THEN 1.0 * d60_retained / d60_eligible END AS d60_retention
FROM cohorts
ORDER BY cohort_month;
