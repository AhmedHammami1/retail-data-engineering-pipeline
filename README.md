# Retail Data Engineering Pipeline & Data Warehouse

## Project Overview

This project implements an end-to-end Retail Data Engineering Pipeline using the UCI Online Retail II dataset.

The objective is to extract, clean, transform, and load retail transaction data into a PostgreSQL Data Warehouse using a Star Schema architecture.

The project also includes SQL analytical queries to generate business insights about sales performance, products, customers, geographical markets, and cancellations.

## Project Objectives

- Build an end-to-end ETL pipeline.
- Process and clean a large retail dataset.
- Design and implement a relational Data Warehouse.
- Apply Star Schema dimensional modeling.
- Automate data loading into PostgreSQL using Python.
- Perform analytical SQL queries.
- Extract meaningful business insights.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python 3.11 | ETL development |
| Pandas | Data manipulation and cleaning |
| PyArrow | Parquet file processing |
| PostgreSQL 18 | Data Warehouse |
| SQL | Data modeling and analytics |
| psycopg2 | Python–PostgreSQL connection |
| Git & GitHub | Version control |
| Docker | Development environment tooling |
| VS Code | Development environment |

## Dataset

**Source:** UCI Machine Learning Repository

**Dataset:** Online Retail II

https://archive.ics.uci.edu/dataset/502/online+retail+ii

The dataset contains retail transactions collected between December 2009 and December 2011.

It includes two worksheets:
- Year 2009-2010
- Year 2010-2011

The combined dataset contains 1,067,371 transaction rows and 8 original columns.

## Project Architecture

```text
Excel Dataset
     |
     v
Extraction (Python / Pandas)
     |
     v
Raw Extracted Data (Parquet)
     |
     v
Data Cleaning and Transformation
     |
     v
Cleaned Data (Parquet)
     |
     v
ETL Loading (Python / psycopg2)
     |
     v
PostgreSQL Data Warehouse
     |
     v
Star Schema
     |
     v
SQL Analytics and Business Insights
```

## Data Warehouse Design

The Data Warehouse follows a Star Schema architecture.

### Dimension Tables

- **dim_date:** Stores date-related attributes such as day, month, quarter, and year.
- **dim_product:** Stores product codes and descriptions.
- **dim_customer:** Stores customer identifiers and includes an unknown customer member.
- **dim_country:** Stores country information.

### Fact Table

**fact_sales** stores transaction-level information.

It contains:
- Date, product, customer, and country foreign keys.
- Invoice identifier and timestamp.
- Quantity and unit price.
- Line amount.
- Data quality and cancellation flags.

**Fact table grain:** One product transaction line within one invoice.

## ETL Pipeline

### 1. Extraction

- Read both worksheets from the original Excel dataset.
- Combine the worksheets into one dataset.
- Standardize selected column data types.
- Export extracted data into Parquet format.

### 2. Transformation

- Remove exact duplicate records.
- Recover eligible missing product descriptions.
- Preserve missing customer identifiers.
- Identify cancelled transactions.
- Identify zero-price and negative-price records.
- Create data quality flags.

The cleaned dataset contains **1,033,036 rows and 12 columns**.

### 3. Loading

Python and psycopg2 are used to load the transformed data into PostgreSQL.

The loading process populates:
- dim_date
- dim_product
- dim_customer
- dim_country
- fact_sales

## Data Warehouse Results

| Table | Number of Rows |
|---|---:|
| dim_date | 604 |
| dim_product | 7,405 |
| dim_customer | 5,943 |
| dim_country | 43 |
| fact_sales | 1,033,036 |

The ETL pipeline completed successfully, with all 1,033,036 cleaned transaction rows loaded into the fact table.

## SQL Analytics and Business Insights

Six analytical SQL queries were implemented.

### 1. Monthly Sales Performance

November 2011 recorded the highest monthly revenue:

**1,503,866.78**

### 2. Top Products by Revenue

The highest-revenue entries included:
- Manual: 339,226.24
- Regency Cake Stand 3 Tier: 330,590.32
- DOTCOM Postage: 309,854.11

### 3. Revenue by Country

The United Kingdom was the leading market, generating:

**17,251,519.96**

### 4. Top Customers

Customer 18102 generated the highest revenue:

**580,987.04**

### 5. Cancellation Analysis

A total of 19,104 cancelled transaction lines were identified.

The highest monthly cancellation percentage was 2.81%, recorded in May 2010.

### 6. Data Quality Analysis

| Indicator | Rows |
|---|---:|
| Total rows | 1,033,036 |
| Cancelled rows | 19,104 |
| Zero-price rows | 6,014 |
| Negative-price rows | 5 |
| Unknown customer rows | 235,151 |

## Project Structure

```text
retail-data-engineering-pipeline/
│
├── config/
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
│   ├── transformation/
│   │   └── clean_data.py
│   └── loading/
│       └── load_warehouse.py
│
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Execution

### 1. Clone the repository

```bash
git clone https://github.com/AhmedHammami1/retail-data-engineering-pipeline.git
cd retail-data-engineering-pipeline
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

Create a PostgreSQL database named:

```sql
CREATE DATABASE retail_dw;
```

Configure the database connection in a local `.env` file:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=retail_dw
DB_USER=postgres
DB_PASSWORD=your_password
```

Do not commit `.env` to GitHub.

### 5. Prepare the dataset

Download the Online Retail II Excel dataset from the UCI repository and place it at:

```text
data/raw/online_retail_II.xlsx
```

### 6. Execute the ETL scripts

Run the extraction script:

```bash
python src/extraction/extract_data.py
```

Run the transformation script:

```bash
python src/transformation/clean_data.py
```

Run the warehouse loading script:

```bash
python src/loading/load_warehouse.py
```

### 7. Execute analytical SQL queries

Connect to PostgreSQL:

```bash
psql -U postgres -d retail_dw
```

Run:

```sql
\i sql/analytics_queries.sql
```

## Data Storage and Version Control

- The original Excel dataset is kept locally.
- Generated Parquet files are excluded from Git.
- Database credentials are stored in `.env`.
- `.gitignore` prevents sensitive configuration and generated data from being committed.

## Future Improvements

- Add automated pipeline scheduling.
- Implement more comprehensive automated tests.
- Develop an interactive dashboard using Power BI or another BI tool.
- Add incremental data loading.
- Containerize the complete application using Docker.

## Author

**Ahmed Hammami**

GitHub: https://github.com/AhmedHammami1

## Project Status

The extraction, transformation, PostgreSQL warehouse loading, and six analytical SQL queries have been successfully implemented.
