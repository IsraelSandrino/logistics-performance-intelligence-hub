SELECT
    route_id,
    route_destination_city,
    destination_state,
    route_type,
    region,

    COUNT(*) AS total_deliveries,

    SUM(total_cost) AS total_cost,
    ROUND(AVG(total_cost), 2) AS avg_cost_per_delivery,

    ROUND(SUM(total_cost) / NULLIF(SUM(distance_km), 0), 2) AS cost_per_km,

    ROUND(AVG(distance_km), 2) AS avg_distance_km,

    SUM(CASE WHEN is_late = 1 THEN 1 ELSE 0 END) AS late_deliveries,
    ROUND(
        SUM(CASE WHEN is_late = 1 THEN 1 ELSE 0 END)::decimal / COUNT(*) * 100,
        2
    ) AS late_percent,

    ROUND(AVG(delay_days), 2) AS avg_delay_days

FROM vw_logistics_performance
GROUP BY
    route_id,
    route_destination_city,
    destination_state,
    route_type,
    region
ORDER BY total_cost DESC;