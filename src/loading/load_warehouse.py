
import os
from pathlib import Path
from decimal import Decimal
from datetime import date
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv


# =====================================================
# 1. PROJECT CONFIGURATION
# =====================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "retail_cleaned.parquet"
)

load_dotenv(PROJECT_ROOT / ".env")

BATCH_SIZE = 5000


# =====================================================
# 2. DATABASE CONNECTION
# =====================================================

def get_connection():

    connection = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return connection


# =====================================================
# 3. EXTRACT CLEANED DATA
# =====================================================

def load_cleaned_data():

    print("\n===== EXTRACTING DATA =====")

    df = pd.read_parquet(DATA_PATH)

    print("Dataset loaded successfully!")
    print("Rows:", len(df))
    print("Columns:", len(df.columns))

    return df


# =====================================================
# 4. LOAD DATE DIMENSION
# =====================================================

def load_dim_date(df, connection):

    print("\n===== LOADING DIM_DATE =====")

    dates = (
        pd.to_datetime(df["InvoiceDate"])
        .dt.normalize()
        .drop_duplicates()
        .sort_values()
    )

    records = []

    for timestamp in dates:

        current_date = timestamp.date()

        date_key = int(current_date.strftime("%Y%m%d"))

        records.append((
            date_key,
            current_date,
            current_date.day,
            current_date.month,
            current_date.strftime("%B"),
            (current_date.month - 1) // 3 + 1,
            current_date.year
        ))

    with connection.cursor() as cursor:

        execute_values(
            cursor,
            """
            INSERT INTO dw.dim_date (
                date_key,
                full_date,
                day_number,
                month_number,
                month_name,
                quarter_number,
                year_number
            )
            VALUES %s
            ON CONFLICT (date_key) DO NOTHING
            """,
            records
        )

        cursor.execute(
            "SELECT COUNT(*) FROM dw.dim_date"
        )

        total = cursor.fetchone()[0]

    print("Source distinct dates:", len(records))
    print("Total dates in dimension:", total)


# =====================================================
# 5. LOAD PRODUCT DIMENSION
# =====================================================

def load_dim_product(df, connection):

    print("\n===== LOADING DIM_PRODUCT =====")

    products = (
        df[["StockCode", "Description"]]
        .drop_duplicates()
    )

    records = []

    for stock_code, description in products.itertuples(
        index=False, name=None
    ):

        if pd.isna(description):
            description = None

        records.append((
            str(stock_code),
            description,
            str(stock_code),
            description
        ))

    insert_query = """
        INSERT INTO dw.dim_product (
            stock_code,
            description
        )
        SELECT %s, %s
        WHERE NOT EXISTS (
            SELECT 1
            FROM dw.dim_product
            WHERE stock_code = %s
              AND description IS NOT DISTINCT FROM %s
        )
    """

    with connection.cursor() as cursor:

        cursor.executemany(insert_query, records)

        cursor.execute(
            "SELECT COUNT(*) FROM dw.dim_product"
        )

        total = cursor.fetchone()[0]

    print("Source distinct product combinations:", len(products))
    print("Total products in dimension:", total)


# =====================================================
# 6. LOAD CUSTOMER DIMENSION
# =====================================================

def load_dim_customer(df, connection):

    print("\n===== LOADING DIM_CUSTOMER =====")

    customers = (
        df["Customer ID"]
        .dropna()
        .unique()
    )

    records = [
        (int(customer_id),)
        for customer_id in customers
    ]

    with connection.cursor() as cursor:

        execute_values(
            cursor,
            """
            INSERT INTO dw.dim_customer (customer_id)
            VALUES %s
            ON CONFLICT (customer_id) DO NOTHING
            """,
            records
        )

        # Insert one Unknown Customer member
        cursor.execute(
            """
            INSERT INTO dw.dim_customer (customer_id)
            SELECT NULL
            WHERE NOT EXISTS (
                SELECT 1
                FROM dw.dim_customer
                WHERE customer_id IS NULL
            )
            """
        )

        cursor.execute(
            """
            SELECT customer_key
            FROM dw.dim_customer
            WHERE customer_id IS NULL
            """
        )

        unknown_customer_key = cursor.fetchone()[0]

        cursor.execute(
            "SELECT COUNT(*) FROM dw.dim_customer"
        )

        total = cursor.fetchone()[0]

    print("Identified customers in source:", len(records))
    print("Unknown customer key:", unknown_customer_key)
    print("Total customers in dimension:", total)

    return unknown_customer_key


# =====================================================
# 7. LOAD COUNTRY DIMENSION
# =====================================================

def load_dim_country(df, connection):

    print("\n===== LOADING DIM_COUNTRY =====")

    countries = df["Country"].dropna().unique()

    records = [
        (str(country),)
        for country in countries
    ]

    with connection.cursor() as cursor:

        execute_values(
            cursor,
            """
            INSERT INTO dw.dim_country (country_name)
            VALUES %s
            ON CONFLICT (country_name) DO NOTHING
            """,
            records
        )

        cursor.execute(
            "SELECT COUNT(*) FROM dw.dim_country"
        )

        total = cursor.fetchone()[0]

    print("Distinct countries in source:", len(records))
    print("Total countries in dimension:", total)


# =====================================================
# 8. RETRIEVE DIMENSION KEYS
# =====================================================

def get_dimension_mappings(connection):

    print("\n===== RETRIEVING DIMENSION KEYS =====")

    mappings = {}

    with connection.cursor() as cursor:

        # Date mapping
        cursor.execute(
            """
            SELECT date_key, full_date
            FROM dw.dim_date
            """
        )

        mappings["dates"] = {
            row[1]: row[0]
            for row in cursor.fetchall()
        }

        # Product mapping
        cursor.execute(
            """
            SELECT product_key, stock_code, description
            FROM dw.dim_product
            """
        )

        mappings["products"] = {
            (row[1], row[2]): row[0]
            for row in cursor.fetchall()
        }

        # Customer mapping
        cursor.execute(
            """
            SELECT customer_key, customer_id
            FROM dw.dim_customer
            """
        )

        mappings["customers"] = {
            row[1]: row[0]
            for row in cursor.fetchall()
            if row[1] is not None
        }

        # Unknown customer mapping
        cursor.execute(
            """
            SELECT customer_key
            FROM dw.dim_customer
            WHERE customer_id IS NULL
            """
        )

        mappings["unknown_customer"] = cursor.fetchone()[0]

        # Country mapping
        cursor.execute(
            """
            SELECT country_key, country_name
            FROM dw.dim_country
            """
        )

        mappings["countries"] = {
            row[1]: row[0]
            for row in cursor.fetchall()
        }

    print("Date keys retrieved:", len(mappings["dates"]))
    print("Product keys retrieved:", len(mappings["products"]))
    print("Customer keys retrieved:", len(mappings["customers"]))
    print("Country keys retrieved:", len(mappings["countries"]))
    print("Unknown customer key:", mappings["unknown_customer"])

    return mappings


# =====================================================
# 9. LOAD FACT TABLE
# =====================================================

def load_fact_sales(df, connection, mappings):

    print("\n===== LOADING FACT_SALES =====")

    # Clear previous fact rows to make a complete reload safe
    with connection.cursor() as cursor:

        cursor.execute(
            "TRUNCATE TABLE dw.fact_sales RESTART IDENTITY"
        )

    insert_query = """
        INSERT INTO dw.fact_sales (
            date_key,
            product_key,
            customer_key,
            country_key,
            invoice,
            invoice_date,
            quantity,
            unit_price,
            line_amount,
            is_cancelled,
            is_zero_price,
            is_negative_price,
            is_customer_unknown
        )
        VALUES %s
    """

    date_map = mappings["dates"]
    product_map = mappings["products"]
    customer_map = mappings["customers"]
    country_map = mappings["countries"]

    unknown_customer_key = mappings["unknown_customer"]

    # Read source columns in the required order
    source_columns = [
        "Invoice",
        "StockCode",
        "Description",
        "InvoiceDate",
        "Customer ID",
        "Country",
        "Quantity",
        "Price",
        "IsCancelled",
        "IsZeroPrice",
        "IsNegativePrice",
        "IsCustomerUnknown"
    ]

    total_loaded = 0
    batch = []

    with connection.cursor() as cursor:

        for row in df[source_columns].itertuples(
            index=False, name=None
        ):

            (
                invoice,
                stock_code,
                description,
                invoice_date,
                customer_id,
                country,
                quantity,
                price,
                is_cancelled,
                is_zero_price,
                is_negative_price,
                is_customer_unknown
            ) = row

            # Resolve date key
            transaction_date = invoice_date.date()
            date_key = date_map[transaction_date]

            # Resolve product key
            if pd.isna(description):
                description = None

            product_key = product_map[
                (str(stock_code), description)
            ]

            # Resolve customer key
            if pd.isna(customer_id):
                customer_key = unknown_customer_key
            else:
                customer_key = customer_map[int(customer_id)]

            # Resolve country key
            country_key = country_map[country]

            # Convert monetary values to Decimal
            unit_price = Decimal(str(price)).quantize(
                Decimal("0.01")
            )

            line_amount = (
                unit_price * int(quantity)
            ).quantize(Decimal("0.01"))

            batch.append((
                date_key,
                product_key,
                customer_key,
                country_key,
                str(invoice),
                invoice_date.to_pydatetime(),
                int(quantity),
                unit_price,
                line_amount,
                bool(is_cancelled),
                bool(is_zero_price),
                bool(is_negative_price),
                bool(is_customer_unknown)
            ))

            # Insert records in batches
            if len(batch) >= BATCH_SIZE:

                execute_values(
                    cursor,
                    insert_query,
                    batch,
                    page_size=BATCH_SIZE
                )

                total_loaded += len(batch)
                batch.clear()

                print(
                    "Fact rows loaded:",
                    total_loaded
                )

        # Insert remaining records
        if batch:

            execute_values(
                cursor,
                insert_query,
                batch,
                page_size=BATCH_SIZE
            )

            total_loaded += len(batch)

    print("\nTotal fact rows loaded:", total_loaded)


# =====================================================
# 10. VALIDATE WAREHOUSE
# =====================================================

def validate_warehouse(df, connection):

    print("\n===== WAREHOUSE VALIDATION =====")

    tables = [
        "dim_date",
        "dim_product",
        "dim_customer",
        "dim_country",
        "fact_sales"
    ]

    with connection.cursor() as cursor:

        for table in tables:

            cursor.execute(
                f"SELECT COUNT(*) FROM dw.{table}"
            )

            count = cursor.fetchone()[0]

            print(f"{table}: {count:,} rows")

        cursor.execute(
            """
            SELECT
                COUNT(*) AS total_rows,
                SUM(quantity) AS total_quantity,
                SUM(line_amount) AS total_amount,
                COUNT(*) FILTER (WHERE is_cancelled) AS cancellations,
                COUNT(*) FILTER (WHERE is_customer_unknown) AS unknown_customers
            FROM dw.fact_sales
            """
        )

        result = cursor.fetchone()

        print("\nFact table statistics:")
        print("Total transactions:", result[0])
        print("Total quantity:", result[1])
        print("Total line amount:", result[2])
        print("Cancellation rows:", result[3])
        print("Unknown customer rows:", result[4])

    print("\nExpected source rows:", len(df))


# =====================================================
# 11. MAIN ETL EXECUTION
# =====================================================

def main():

    connection = None

    try:

        # Extract
        df = load_cleaned_data()

        # Connect
        connection = get_connection()

        print("\nPostgreSQL connection successful!")

        # Load dimensions
        load_dim_date(df, connection)

        load_dim_product(df, connection)

        load_dim_customer(df, connection)

        load_dim_country(df, connection)

        # Retrieve foreign keys
        mappings = get_dimension_mappings(connection)

        # Load fact table
        load_fact_sales(df, connection, mappings)

        # Validate
        validate_warehouse(df, connection)

        # Commit all operations
        connection.commit()

        print("\n====================================")
        print("ETL PIPELINE COMPLETED SUCCESSFULLY!")
        print("====================================")

    except Exception as error:

        if connection is not None:
            connection.rollback()

        print("\nETL PIPELINE FAILED!")
        print("Error:", error)

        raise

    finally:

        if connection is not None:
            connection.close()

            print("\nDatabase connection closed.")


if __name__ == "__main__":
    main()
