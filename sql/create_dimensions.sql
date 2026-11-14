
-- ==========================================
-- Retail Data Warehouse
-- 02 - Create dimension tables
-- ==========================================

CREATE TABLE IF NOT EXISTS dw.dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_number INTEGER NOT NULL,
    month_number INTEGER NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    quarter_number INTEGER NOT NULL,
    year_number INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS dw.dim_product (
    product_key SERIAL PRIMARY KEY,
    stock_code VARCHAR(20) NOT NULL,
    description TEXT,
    UNIQUE (stock_code, description)
);

CREATE TABLE IF NOT EXISTS dw.dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id BIGINT UNIQUE
);

CREATE TABLE IF NOT EXISTS dw.dim_country (
    country_key SERIAL PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL UNIQUE
);
