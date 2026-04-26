-- Operational risk score by route
-- Base: vw_logistics_performance
-- Critério usado: Score = atraso % * 45% + falha % * 35% + atraso médio ponderado * 20%

WITH route_metrics AS (
    SELECT
        route_id,
        route_destination_city,
        destination_state,
        region,
        route_type,
        COUNT(*) AS total_deliveries,
        SUM(CASE WHEN is_late THEN 1 ELSE 0 END) AS late_deliveries,
        SUM(CASE WHEN is_failed THEN 1 ELSE 0 END) AS failed_deliveries,
        ROUND(AVG(delay_days), 2) AS avg_delay_days,
        ROUND(AVG(total_cost), 2) AS avg_delivery_cost,
        ROUND(SUM(total_cost), 2) AS total_route_cost,
        ROUND(
            SUM(CASE WHEN is_late THEN 1 ELSE 0 END)::numeric 
            / NULLIF(COUNT(*), 0) * 100,
            2
        ) AS late_rate_percent,
        ROUND(
            SUM(CASE WHEN is_failed THEN 1 ELSE 0 END)::numeric 
            / NULLIF(COUNT(*), 0) * 100,
            2
        ) AS failed_rate_percent
    FROM vw_logistics_performance
    GROUP BY
        route_id,
        route_destination_city,
        destination_state,
        region,
        route_type
),

risk_score AS (
    SELECT
        *,
        ROUND(
            LEAST(
                100,
                (
                    late_rate_percent * 0.45
                    + failed_rate_percent * 0.35
                    + avg_delay_days * 10 * 0.20
                )
            ),
            2
        ) AS operational_risk_score
    FROM route_metrics
)

SELECT
    route_id,
    route_destination_city,
    destination_state,
    region,
    route_type,
    total_deliveries,
    late_deliveries,
    failed_deliveries,
    late_rate_percent,
    failed_rate_percent,
    avg_delay_days,
    avg_delivery_cost,
    total_route_cost,
    operational_risk_score,
    CASE
        WHEN operational_risk_score >= 70 THEN 'Alto risco'
        WHEN operational_risk_score >= 40 THEN 'Risco médio'
        ELSE 'Baixo risco'
    END AS risk_level
FROM risk_score
ORDER BY operational_risk_score DESC;