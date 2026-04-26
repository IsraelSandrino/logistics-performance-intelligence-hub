-- =========================================================
-- Logistics Performance Intelligence Hub
-- Script: create_tables.sql
-- Objetivo: Criar tabelas dimensionais e fato no Supabase(PostgreSQL)
-- =========================================================

SET search_path TO public;

DROP TABLE IF EXISTS fact_deliveries CASCADE;
DROP TABLE IF EXISTS dim_orders CASCADE;
DROP TABLE IF EXISTS dim_routes CASCADE;
DROP TABLE IF EXISTS dim_hubs CASCADE;
DROP TABLE IF EXISTS dim_carriers CASCADE;

-- =========================
-- DIM: Transportadoras
-- =========================
CREATE TABLE dim_carriers (
    carrier_id VARCHAR(20) PRIMARY KEY,
    carrier_name VARCHAR(100) NOT NULL,
    carrier_type VARCHAR(50),
    service_level VARCHAR(50),
    region_coverage VARCHAR(100)
);

-- =========================
-- DIM: Hubs Logísticos
-- =========================
CREATE TABLE dim_hubs (
    hub_id VARCHAR(20) PRIMARY KEY,
    hub_name VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state CHAR(2) NOT NULL,
    region VARCHAR(50) NOT NULL
);

-- =========================
-- DIM: Rotas
-- =========================
CREATE TABLE dim_routes (
    route_id VARCHAR(20) PRIMARY KEY,
    origin_hub_id VARCHAR(20) NOT NULL,
    destination_city VARCHAR(100) NOT NULL,
    destination_state CHAR(2) NOT NULL,
    destination_region VARCHAR(50) NOT NULL,
    distance_km NUMERIC(10,2),
    route_type VARCHAR(50),

    CONSTRAINT fk_routes_origin_hub
        FOREIGN KEY (origin_hub_id)
        REFERENCES dim_hubs(hub_id)
);

-- =========================
-- DIM: Pedidos
-- =========================
CREATE TABLE dim_orders (
    order_id VARCHAR(30) PRIMARY KEY,
    customer_id VARCHAR(30),
    order_date DATE NOT NULL,
    promised_delivery_date DATE NOT NULL,
    order_value NUMERIC(12,2),
    product_category VARCHAR(100),
    marketplace_channel VARCHAR(50)
);

-- =========================
-- FACT: Entregas
-- =========================
CREATE TABLE fact_deliveries (
    delivery_id VARCHAR(30) PRIMARY KEY,
    order_id VARCHAR(30) NOT NULL,
    route_id VARCHAR(20) NOT NULL,
    carrier_id VARCHAR(20) NOT NULL,

    shipped_date DATE NOT NULL,
    delivered_date DATE,
    delivery_status VARCHAR(50) NOT NULL,

    sla_days INTEGER,
    actual_delivery_days INTEGER,
    delay_days INTEGER,

    shipping_cost NUMERIC(12,2),
    additional_cost NUMERIC(12,2),
    total_cost NUMERIC(12,2),

    is_late BOOLEAN,
    is_failed BOOLEAN,

    failed_reason VARCHAR(100),
    failed_reason_category VARCHAR(100),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_deliveries_order
        FOREIGN KEY (order_id)
        REFERENCES dim_orders(order_id),

    CONSTRAINT fk_deliveries_route
        FOREIGN KEY (route_id)
        REFERENCES dim_routes(route_id),

    CONSTRAINT fk_deliveries_carrier
        FOREIGN KEY (carrier_id)
        REFERENCES dim_carriers(carrier_id)
);

-- =========================
-- Índices para análise
-- =========================
CREATE INDEX idx_fact_deliveries_order_id
ON fact_deliveries(order_id);

CREATE INDEX idx_fact_deliveries_route_id
ON fact_deliveries(route_id);

CREATE INDEX idx_fact_deliveries_carrier_id
ON fact_deliveries(carrier_id);

CREATE INDEX idx_fact_deliveries_status
ON fact_deliveries(delivery_status);

CREATE INDEX idx_fact_deliveries_delivered_date
ON fact_deliveries(delivered_date);

CREATE INDEX idx_fact_deliveries_is_late
ON fact_deliveries(is_late);

CREATE INDEX idx_fact_deliveries_is_failed
ON fact_deliveries(is_failed);