-- DIMENSIONS

\copy dim_carriers FROM 'data/raw/dim_carriers.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

\copy dim_hubs FROM 'data/raw/dim_hubs.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

\copy dim_routes FROM 'data/raw/dim_routes.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');

\copy dim_orders FROM 'data/raw/dim_orders.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');


-- FACT

\copy fact_deliveries FROM 'data/raw/fact_deliveries.csv' WITH (FORMAT csv, HEADER true, DELIMITER ',', ENCODING 'UTF8');