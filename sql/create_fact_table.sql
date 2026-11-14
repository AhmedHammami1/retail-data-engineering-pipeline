
-- ==========================================
-- Retail Data Warehouse
-- Create Fact Sales Table
-- ==========================================

CREATE TABLE IF NOT EXISTS dw.fact_sales (

    -- Primary key
    sales_key BIGSERIAL PRIMARY KEY,

    -- Foreign keys
    date_key INTEGER NOT NULL,
    product_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    country_key INTEGER NOT NULL,

    -- Invoice information
    invoice VARCHAR(20) NOT NULL,
    invoice_date TIMESTAMP NOT NULL,

    -- Measures
    quantity INTEGER NOT NULL,
    unit_price NUMERIC(12, 2) NOT NULL,
    line_amount NUMERIC(18, 2) NOT NULL,

    -- Transaction indicators
    is_cancelled BOOLEAN NOT NULL,
    is_zero_price BOOLEAN NOT NULL,
    is_negative_price BOOLEAN NOT NULL,
    is_customer_unknown BOOLEAN NOT NULL,

    -- Referential integrity
    CONSTRAINT fk_sales_date
        FOREIGN KEY (date_key)
        REFERENCES dw.dim_date(date_key),

    CONSTRAINT fk_sales_product
        FOREIGN KEY (product_key)
        REFERENCES dw.dim_product(product_key),

    CONSTRAINT fk_sales_customer
        FOREIGN KEY (customer_key)
        REFERENCES dw.dim_customer(customer_key),

    CONSTRAINT fk_sales_country
        FOREIGN KEY (country_key)
        REFERENCES dw.dim_country(country_key)
);
