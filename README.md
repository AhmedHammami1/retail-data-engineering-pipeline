# Retail Data Engineering Pipeline & Data Warehouse

An end-to-end data engineering project that transforms raw retail transaction data into an analytical PostgreSQL Data Warehouse using Python, SQL, and Docker.

## Overview

This project implements an ETL (Extract, Transform, Load) pipeline using the **UCI Online Retail II dataset**, which contains more than one million retail transaction records collected between December 2009 and December 2011.

The pipeline extracts data from Excel, performs data cleaning and transformation, stores intermediate datasets in Parquet format, and loads the results into a PostgreSQL Data Warehouse designed using a **Star Schema**.

SQL analytical queries are then used to explore sales performance, product revenue, customer behavior, geographical markets, and cancellations.

The complete pipeline is also containerized using Docker and Docker Compose.

## Project Objectives

- Build an end-to-end ETL pipeline.
- Process and clean a large retail dataset using Python.
- Store intermediate datasets efficiently using Parquet.
- Design and implement a dimensional Data Warehouse.
- Apply Star Schema modeling principles.
- Automate data loading into PostgreSQL.
- Perform analytical SQL queries to extract business insights.
- Containerize the application using Docker Compose.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | ETL pipeline development |
| Pandas | Data manipulation and cleaning |
| PyArrow | Parquet data processing |
| PostgreSQL 18 | Data Warehouse |
| SQL | Database modeling and analytics |
| psycopg2 | Python–PostgreSQL connectivity |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| Git & GitHub | Version control |
| VS Code | Development environment |

## Dataset

**Source:** [UCI Machine Learning Repository – Online Retail II](https://archive.ics.uci.edu/dataset/502/online+retail+ii)

The dataset contains transactions from a UK-based online retail company between December 2009 and December 2011.

It consists of two Excel worksheets:

- `Year 2009-2010`
- `Year 2010-2011`

After combining both worksheets, the original dataset contains:

- **1,067,371 transaction rows**
- **8 original columns**

The main attributes include invoice identifiers, product codes, descriptions, quantities, invoice dates, prices, customer identifiers, and countries.

## Project Architecture

```text
                  Online Retail II
                    Excel Dataset
                         |
                         v
                 1. DATA EXTRACTION
                    Python / Pandas
                         |
                         v
                 Extracted Parquet Data
                         |
                         v
               2. DATA TRANSFORMATION
                Cleaning and Validation
                         |
                         v
                  Cleaned Parquet Data
                         |
                         v
                  3. DATA LOADING
                  Python / psycopg2
                         |
                         v
                PostgreSQL Data Warehouse
                         |
                         v
                     Star Schema
                         |
                         v
                  SQL ANALYTICS
                         |
                         v
                  Business Insights

       Docker Compose orchestrates the ETL
              application and database.
```

## Data Warehouse Design

The Data Warehouse follows a **Star Schema** architecture, separating descriptive information into dimension tables and transactional measurements into a central fact table.

### Dimension Tables

| Table | Description |
|---|---|
| `dim_date` | Date attributes: day, month, quarter, and year |
| `dim_product` | Product codes and descriptions |
| `dim_customer` | Customer identifiers, including an unknown customer member |
| `dim_country` | Unique country information |

### Fact Table

`fact_sales` stores transaction-level information and references all four dimensions.

It contains:

- Date, product, customer, and country foreign keys.
- Invoice identifier and timestamp.
- Quantity and unit price.
- Transaction line amount.
- Cancellation and data quality flags.

**Fact table grain:** One product transaction line within one invoice.

### Measures and Data Quality Flags

- `quantity`
- `unit_price`
- `line_amount`
- `is_cancelled`
- `is_zero_price`
- `is_negative_price`
- `is_customer_unknown`

Missing customer identifiers are preserved and represented through a dedicated unknown customer dimension member.

## ETL Pipeline

### 1. Extraction

The extraction process:

- Reads both worksheets from the original Excel dataset.
- Combines them into one DataFrame.
- Standardizes selected column data types.
- Exports the extracted dataset to Parquet format.

Output: `data/processed/retail_extracted.parquet`

### 2. Transformation

The transformation process:

- Removes exact duplicate records.
- Recovers eligible missing product descriptions.
- Preserves missing customer identifiers.
- Identifies cancelled transactions.
- Identifies zero-price and negative-price records.
- Creates data quality flags.
- Exports the cleaned dataset to Parquet format.

Output: `data/processed/retail_cleaned.parquet`

**Cleaning results:**

| Metric | Result |
|---|---:|
| Original transaction rows | 1,067,371 |
| Duplicate records removed | 34,335 |
| Final cleaned rows | 1,033,036 |
| Final columns | 12 |

### 3. Loading

Python and `psycopg2` are used to load the transformed data into PostgreSQL.

The loading process populates the four dimension tables and the central fact table. Fact records are inserted in batches to handle the large dataset efficiently.

## Data Warehouse Results

The completed warehouse contains:

| Table | Records |
|---|---:|
| `dim_date` | 604 |
| `dim_product` | 7,405 |
| `dim_customer` | 5,943 |
| `dim_country` | 43 |
| `fact_sales` | 1,033,036 |

**ETL validation:** All 1,033,036 cleaned transaction rows were successfully loaded into `fact_sales`.

## SQL Analytics and Business Insights

Six analytical SQL queries were implemented to explore the retail data.

### 1. Monthly Sales Performance

November 2011 recorded the highest monthly revenue:

**1,503,866.78**

November was also the strongest observed month in 2010.

### 2. Top Products by Revenue

The highest-revenue entries included:

| Product / Entry | Revenue |
|---|---:|
| Manual | 339,226.24 |
| Regency Cake Stand 3 Tier | 330,590.32 |
| DOTCOM Postage | 309,854.11 |

*Note: Some high-revenue entries represent operational or service codes rather than conventional products.*

### 3. Revenue by Country

The United Kingdom was the leading market, generating:

**17,251,519.96**

Other important markets included Ireland, the Netherlands, Germany, and France.

### 4. Top Customers

Customer `18102` generated the highest recorded revenue:

**580,987.04**

### 5. Cancellation Analysis

- Cancelled transaction lines: **19,104**
- Highest monthly cancellation percentage: **2.81%**
- Highest cancellation percentage recorded in: **May 2010**

### 6. Data Quality Analysis

| Indicator | Rows |
|---|---:|
| Total transaction rows | 1,033,036 |
| Cancelled rows | 19,104 |
| Zero-price rows | 6,014 |
| Negative-price rows | 5 |
| Unknown customer rows | 235,151 |

These indicators help identify data quality issues while preserving relevant transaction records for analysis.

## Project Structure

```text
retail-data-engineering-pipeline/
│
├── config/
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── warehouse/
│
├── docs/
│   └── PROJECT_DOCUMENTATION.md
│
├── logs/
├── notebooks/
│
├── sql/
│   ├── create_schema.sql
│   ├── create_dimensions.sql
│   ├── create_fact_table.sql
│   └── analytics_queries.sql
│
├── src/
│   ├── extraction/
│   │   └── extract_data.py
│   ├── transformation/
│   │   └── clean_data.py
│   └── loading/
│       └── load_warehouse.py
│
├── tests/
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Installation and Execution

### Option 1: Run Locally

#### 1. Clone the repository

```bash
git clone https://github.com/AhmedHammami1/retail-data-engineering-pipeline.git
cd retail-data-engineering-pipeline
```

#### 2. Create and activate a virtual environment

For Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Configure PostgreSQL

Create a PostgreSQL database named `retail_dw`:

```sql
CREATE DATABASE retail_dw;
```

Create a local `.env` file in the project root:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_dw
DB_USER=postgres
DB_PASSWORD=your_password
```

Do not commit `.env` to GitHub.

Connect to the database and execute the SQL scripts in this order:

```bash
psql -U postgres -d retail_dw
```

```sql
\i sql/create_schema.sql
\i sql/create_dimensions.sql
\i sql/create_fact_table.sql
```

#### 5. Prepare the dataset

Download the Online Retail II Excel file from the UCI repository and place it here:

```text
data/raw/online_retail_II.xlsx
```

#### 6. Execute the ETL pipeline

Run the scripts in the following order:

```bash
python src/extraction/extract_data.py
python src/transformation/clean_data.py
python src/loading/load_warehouse.py
```

#### 7. Execute analytical queries

Connect to PostgreSQL:

```bash
psql -U postgres -d retail_dw
```

Execute:

```sql
\i sql/analytics_queries.sql
```

### Option 2: Run with Docker

The project is containerized using Docker Compose, which manages the Python ETL application and PostgreSQL database.

#### Prerequisites

- Docker Desktop
- Docker Compose
- UCI Online Retail II dataset

#### 1. Configure the environment

Place the Excel dataset in:

```text
data/raw/online_retail_II.xlsx
```

Create a `.env` file in the project root with the database credentials:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_dw
DB_USER=postgres
DB_PASSWORD=your_password
```

Docker Compose overrides the ETL container's database host with the internal service name `database`.

#### 2. Build and start PostgreSQL

```bash
docker compose up --build -d database
```

#### 3. Initialize the Data Warehouse

Execute the SQL scripts in order:

```powershell
Get-Content .\sql\create_schema.sql | docker compose exec -T database psql -U postgres -d retail_dw

Get-Content .\sql\create_dimensions.sql | docker compose exec -T database psql -U postgres -d retail_dw

Get-Content .\sql\create_fact_table.sql | docker compose exec -T database psql -U postgres -d retail_dw
```

#### 4. Run the ETL pipeline

```bash
docker compose up etl
```

The ETL container extracts, transforms, and loads the dataset into the PostgreSQL container.

#### 5. Verify the results

Check the containers:

```bash
docker compose ps -a
```

View ETL logs:

```bash
docker compose logs etl
```

Verify the number of loaded transactions:

```bash
docker compose exec database psql -U postgres -d retail_dw -c "SELECT COUNT(*) FROM dw.fact_sales;"
```

Expected result:

```text
1033036
```

#### 6. Stop the containers

```bash
docker compose down
```

PostgreSQL data is stored in a persistent Docker volume and is preserved when containers are stopped or removed.

**Warning:** `docker compose down -v` removes the persistent volume and deletes the Docker database data.

## Data Storage and Version Control

- The original Excel dataset is stored locally and is not committed to Git.
- Generated Parquet files are excluded from version control.
- Database credentials are stored in `.env`.
- `.gitignore` excludes sensitive configuration, virtual environments, and generated data.
- `.dockerignore` excludes unnecessary files from the Docker build context.

## Future Improvements

- Implement incremental data loading.
- Add automated pipeline scheduling.
- Develop an interactive dashboard using Power BI or another BI tool.
- Expand automated testing and data validation.
- Introduce workflow orchestration tools such as Apache Airflow.

## Author

**Ahmed Hammami**

- GitHub: [AhmedHammami1](https://github.com/AhmedHammami1)

## Project Status

 — Successfully implemented and validated:

- Data extraction and transformation.
- PostgreSQL Star Schema Data Warehouse.
- Python-based ETL loading pipeline.
- Six analytical SQL queries.
- Docker containerization using Docker Compose.

The complete pipeline has been executed successfully, with **1,033,036 transaction records** loaded and validated in the PostgreSQL Data Warehouse.