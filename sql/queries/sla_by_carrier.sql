-- SLA por transportadora
-- Fonte: vw_logistics_performance

SELECT
    carrier_id,
    carrier_name,

    COUNT(*) AS total_deliveries,

    SUM(CASE WHEN is_failed = TRUE THEN 1 ELSE 0 END) AS failed_deliveries,
    SUM(CASE WHEN is_late = TRUE AND is_failed = FALSE THEN 1 ELSE 0 END) AS late_deliveries,
    SUM(CASE WHEN is_on_time = 1 AND is_failed = FALSE THEN 1 ELSE 0 END) AS on_time_deliveries,

    ROUND(
        100.0 * SUM(CASE WHEN is_on_time = TRUE THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS sla_percent,

    ROUND(AVG(actual_delivery_days), 2) AS avg_delivery_days,
    ROUND(AVG(delay_days), 2) AS avg_delay_days,

    ROUND(SUM(total_cost), 2) AS total_logistics_cost,
    ROUND(AVG(total_cost), 2) AS avg_cost_per_delivery

FROM vw_logistics_performance
GROUP BY
    carrier_id,
    carrier_name
ORDER BY
    sla_percent DESC,
    total_deliveries DESC;