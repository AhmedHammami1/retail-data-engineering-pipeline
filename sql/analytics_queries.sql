
-- =====================================================
-- RETAIL DATA WAREHOUSE - ANALYTICAL QUERIES
-- =====================================================

-- 1. Monthly sales performance
SELECT
    d.year_number,
    d.month_number,
    d.month_name,
    SUM(f.line_amount) AS total_revenue,
    SUM(f.quantity) AS total_quantity,
    COUNT(DISTINCT f.invoice) AS total_invoices
FROM dw.fact_sales f
JOIN dw.dim_date d ON f.date_key = d.date_key
WHERE f.is_cancelled = FALSE
GROUP BY d.year_number, d.month_number, d.month_name
ORDER BY d.year_number, d.month_number;


-- 2. Top 10 products by revenue
SELECT
    p.stock_code,
    p.description,
    SUM(f.quantity) AS total_quantity,
    SUM(f.line_amount) AS total_revenue
FROM dw.fact_sales f
JOIN dw.dim_product p ON f.product_key = p.product_key
WHERE f.is_cancelled = FALSE
GROUP BY p.stock_code, p.description
ORDER BY total_revenue DESC
LIMIT 10;


-- 3. Top 10 countries by revenue
SELECT
    co.country_name,
    SUM(f.line_amount) AS total_revenue,
    COUNT(DISTINCT f.invoice) AS total_invoices
FROM dw.fact_sales f
JOIN dw.dim_country co ON f.country_key = co.country_key
WHERE f.is_cancelled = FALSE
GROUP BY co.country_name
ORDER BY total_revenue DESC
LIMIT 10;


-- 4. Top 10 customers by revenue
SELECT
    c.customer_id,
    SUM(f.line_amount) AS total_revenue,
    COUNT(DISTINCT f.invoice) AS total_invoices
FROM dw.fact_sales f
JOIN dw.dim_customer c ON f.customer_key = c.customer_key
WHERE f.is_cancelled = FALSE
  AND f.is_customer_unknown = FALSE
GROUP BY c.customer_id
ORDER BY total_revenue DESC
LIMIT 10;


-- 5. Cancellation analysis by month
SELECT
    d.year_number,
    d.month_number,
    COUNT(*) FILTER (WHERE f.is_cancelled = TRUE) AS cancelled_lines,
    COUNT(*) AS total_lines,
    ROUND(
        100.0 * COUNT(*) FILTER (WHERE f.is_cancelled = TRUE)
        / NULLIF(COUNT(*), 0), 2
    ) AS cancellation_percentage
FROM dw.fact_sales f
JOIN dw.dim_date d ON f.date_key = d.date_key
GROUP BY d.year_number, d.month_number
ORDER BY d.year_number, d.month_number;


-- 6. Data quality overview
SELECT
    COUNT(*) AS total_rows,
    COUNT(*) FILTER (WHERE is_cancelled = TRUE) AS cancelled_rows,
    COUNT(*) FILTER (WHERE is_zero_price = TRUE) AS zero_price_rows,
    COUNT(*) FILTER (WHERE is_negative_price = TRUE) AS negative_price_rows,
    COUNT(*) FILTER (WHERE is_customer_unknown = TRUE) AS unknown_customer_rows
FROM dw.fact_sales;
