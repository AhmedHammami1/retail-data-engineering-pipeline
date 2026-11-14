# Retail Data Engineering Pipeline & Data Warehouse

## 1. Project Overview

This project aims to design and implement an end-to-end Data Engineering pipeline using real-world retail transaction data.

The project uses the Online Retail II dataset from the UCI Machine Learning Repository. The objective is to extract, explore, clean, transform, and load retail transaction data into a PostgreSQL Data Warehouse.

The final solution will use Python for ETL operations, PostgreSQL for data storage, Docker for containerization, and Git/GitHub for version control and project documentation.

## 2. Project Objectives

The main objectives are:

- Build an end-to-end ETL pipeline.
- Work with a real-world transactional dataset.
- Identify and handle data quality issues.
- Design a dimensional Data Warehouse using a Star Schema.
- Store structured data in PostgreSQL.
- Perform analytical SQL queries.
- Containerize the application using Docker.
- Implement testing and document the complete workflow.

## 3. Technologies and Tools

| Technology | Purpose |
|---|---|
| Python 3.11.9 | ETL development |
| Pandas | Data manipulation and analysis |
| Openpyxl | Reading Excel files |
| PostgreSQL 18.7 | Data Warehouse |
| SQL | Database operations and analytics |
| Docker | Application containerization |
| Docker Compose | Managing application services |
| Git | Version control |
| GitHub | Project hosting |
| Visual Studio Code | Development environment |

## 4. Development Environment Setup

### 4.1 Python Installation

Python 3.11.9 was installed and verified.

Command:

```powershell
python --version
```

### 4.2 Virtual Environment

A Python virtual environment was created to isolate project dependencies.

Command:

```powershell
python -m venv venv
```

Activation:

```powershell
.\venv\Scripts\Activate.ps1
```

The virtual environment ensures that project libraries do not interfere with other Python installations.

### 4.3 Git Configuration

Git was installed and configured.

The project repository was initialized using:

```powershell
git init
git branch -M main
```

A `.gitignore` file was created to exclude unnecessary files, including:

- Python virtual environments.
- Python cache files.
- Environment variables and secrets.
- Log files.
- IDE configuration files.

The initial project structure was committed and pushed to GitHub.

GitHub repository:

https://github.com/AhmedHammami1/retail-data-engineering-pipeline

### 4.4 PostgreSQL Configuration

PostgreSQL 18.7 was installed and its Windows service was verified.

The PostgreSQL command-line tool (`psql`) was configured in the Windows PATH.

The database connection was tested using:

```powershell
psql -U postgres -h localhost -p 5432 -d postgres
```

Connection details:

- Database: postgres
- User: postgres
- Host: localhost
- Port: 5432

A dedicated project database was created:

```sql
CREATE DATABASE retail_dw;
```

Connection to the project database:

```sql
\c retail_dw
```

The connection was verified successfully using:

```sql
\conninfo
SELECT version();
```

### 4.5 Docker Configuration

Docker Desktop was installed.

The Docker Engine was verified using:

```powershell
docker ps
```

The command successfully returned the container list, confirming that the Docker Engine was accessible.

### 4.6 Python Dependencies

The following libraries were installed inside the virtual environment:

```powershell
python -m pip install pandas openpyxl
```

Installed versions:

- Pandas: 3.1.1
- Openpyxl: 3.1.5
- NumPy: 2.4.6

Dependencies were exported into `requirements.txt`:

```powershell
python -m pip freeze > requirements.txt
```

## 5. Dataset Selection

### 5.1 Dataset Information

The selected dataset is Online Retail II, provided by the UCI Machine Learning Repository.

Official source:

https://archive.ics.uci.edu/dataset/502/online+retail+ii

The dataset contains real transactional records from a UK-based online retailer.

The Excel workbook contains two worksheets:

- Year 2009-2010
- Year 2010-2011

The original file is stored in:

`data/raw/online_retail_II.xlsx`

The original dataset is preserved without modification.

### 5.2 Dataset Attributes

The dataset contains eight columns:

| Column | Description |
|---|---|
| Invoice | Invoice identifier |
| StockCode | Product identifier |
| Description | Product description |
| Quantity | Number of products purchased |
| InvoiceDate | Transaction date and time |
| Price | Unit price |
| Customer ID | Customer identifier |
| Country | Customer country |

## 6. Data Exploration

### 6.1 Python Exploration Script

The first exploration script was created at:

`src/extraction/explore_data.py`

The script uses Pandas to:

- Read the Excel workbook.
- Display available worksheets.
- Load the first worksheet.
- Display the first five records.
- Inspect dataset dimensions.
- Display column names and data types.
- Count missing values.

The second worksheet was explored separately.

### 6.2 First Worksheet: Year 2009-2010

Dataset dimensions:

- Rows: 525,461
- Columns: 8

Missing values:

| Column | Missing values |
|---|---:|
| Invoice | 0 |
| StockCode | 0 |
| Description | 2,928 |
| Quantity | 0 |
| InvoiceDate | 0 |
| Price | 0 |
| Customer ID | 107,927 |
| Country | 0 |

### 6.3 Second Worksheet: Year 2010-2011

Dataset dimensions:

- Rows: 541,910
- Columns: 8

Missing values:

| Column | Missing values |
|---|---:|
| Invoice | 0 |
| StockCode | 0 |
| Description | 1,454 |
| Quantity | 0 |
| InvoiceDate | 0 |
| Price | 0 |
| Customer ID | 135,080 |
| Country | 0 |

### 6.4 Data Type Analysis

Both worksheets have the same column names and compatible data types.

| Column | Data type |
|---|---|
| Invoice | object |
| StockCode | object |
| Description | object |
| Quantity | int64 |
| InvoiceDate | datetime64 |
| Price | float64 |
| Customer ID | float64 |
| Country | str |

This compatibility allows the two worksheets to be combined vertically.

### 6.5 Initial Data Quality Observations

The exploration identified two columns containing missing values:

**Customer ID**

A significant number of transactions do not have an associated customer identifier.

These records should not automatically be deleted because they may still be useful for sales analysis.

**Description**

Some product descriptions are missing. We will investigate whether the missing descriptions can be recovered using the corresponding StockCode.

No records have been removed at this stage.

## 7. Dataset Integration

### 7.1 Combining the Worksheets

The two worksheets were loaded into separate Pandas DataFrames:

- `df_2009`: Year 2009-2010
- `df_2010`: Year 2010-2011

The `pd.concat()` function was used to combine the DataFrames vertically.

Implementation:

```python
df = pd.concat(
    [df_2009, df_2010],
    ignore_index=True
)
```

The `ignore_index=True` parameter creates a new continuous index for the combined DataFrame.
### 7.2 Verified Combined Dataset Results

The concatenation operation was successfully executed using Pandas.

The actual output confirmed the following dimensions:

`(1,067,371, 8)`

| Source | Rows |
|---|---:|
| Year 2009-2010 | 525,461 |
| Year 2010-2011 | 541,910 |
| **Combined dataset** | **1,067,371** |

The combined DataFrame contains all eight original columns.

The first records belong to the 2009-2010 worksheet, while the last records belong to the 2010-2011 worksheet.

The combined dataset contains:

| Column | Missing values |
|---|---:|
| Invoice | 0 |
| StockCode | 0 |
| Description | 4,382 |
| Quantity | 0 |
| InvoiceDate | 0 |
| Price | 0 |
| Customer ID | 243,007 |
| Country | 0 |

No records were deleted during concatenation.

**Result:** Both worksheets were successfully integrated into one DataFrame, preserving all 1,067,371 records.



### 7.3 Important Data Engineering Decision

At this stage, concatenation is performed without deleting or modifying records.

The original dataset remains preserved in `data/raw/`.

Data cleaning and transformation will be performed in subsequent ETL stages.

## 8. Current Project Status

Completed activities:

- [x] Development environment setup.
- [x] Python virtual environment creation.
- [x] Git and GitHub configuration.
- [x] PostgreSQL installation and configuration.
- [x] Creation of the `retail_dw` database.
- [x] Docker installation and engine verification.
- [x] Installation of Pandas and Openpyxl.
- [x] Dataset download.
- [x] Exploration of both Excel worksheets.
- [x] Identification of initial missing values.
- [x] Combination of both worksheets.

Upcoming activities:

- [ ] Verify the combined DataFrame.
- [ ] Analyze duplicate records.
- [ ] Investigate cancellations and returns.
- [ ] Analyze invalid quantities and prices.
- [ ] Define data cleaning rules.
- [ ] Implement data transformation.
- [ ] Design the Data Warehouse.
- [ ] Load data into PostgreSQL.
- [ ] Develop analytical SQL queries.
- [ ] Containerize

## 8. Data Quality Analysis

### 8.1 Duplicate Records Detection

The first data quality check focused on identifying exact duplicate records.

The following Pandas command was used:

```python
duplicate_count = df.duplicated().sum()
```

The `duplicated()` method identifies rows that have exactly the same values across all columns. The `sum()` method counts duplicate occurrences, excluding the first occurrence of each group.

**Results:**

| Metric | Result |
|---|---:|
| Original dataset rows | 1,067,371 |
| Duplicate occurrences | 34,335 |
| Duplicate percentage | 3.22% |

The duplicate percentage was calculated as:

Duplicate percentage = (34,335 / 1,067,371) × 100

### 8.2 Initial Observations

The inspection of sample duplicate records showed identical transaction attributes, including invoice number, product code, quantity, price, customer identifier, and transaction date.

However, repeated transaction lines must be investigated before removal because they may represent legitimate business activity.

**Data quality decision:** No duplicate records have been deleted at this stage. Further investigation is required before defining the cleaning rules.

### 8.2 Detailed Duplicate Investigation

A deeper analysis was performed to distinguish between duplicate occurrences, rows involved in duplicate groups, and distinct duplicate groups.

The following code was used:

```python
duplicate_rows = df[df.duplicated(keep=False)]

duplicate_groups = (
    df.groupby(list(df.columns), dropna=False)
      .size()
      .reset_index(name="Occurrences")
)

duplicate_groups = duplicate_groups[
    duplicate_groups["Occurrences"] > 1
]
```

**Results:**

| Metric | Result |
|---|---:|
| Total dataset rows | 1,067,371 |
| Rows involved in duplicate groups | 67,242 |
| Distinct duplicate groups | 32,907 |
| Extra duplicate occurrences | 34,335 |

The investigation also identified records repeated multiple times within the same invoice.

For example, one product record appeared 20 times in invoice 555524.

**Interpretation:**

- Rows involved in duplicate groups include both the original occurrence and repeated occurrences.
- Distinct duplicate groups represent the number of unique records appearing more than once.
- Extra duplicate occurrences represent the number of additional copies beyond the first occurrence.

**Data quality decision:**

No records have been deleted. The original dataset remains unchanged. Further investigation is required before deciding which records should be removed from the transformed dataset.

### 8.3 Cancellation and Negative Quantity Analysis

The next data quality investigation focused on identifying cancelled invoices and transactions with negative or zero quantities.

#### Cancellation Detection

Invoices beginning with the letter `C` were identified using:

```python
cancelled = df[
    df["Invoice"].astype(str).str.startswith("C")
]
```

Results:

| Metric | Result |
|---|---:|
| Rows with cancelled invoices | 19,494 |
| Unique cancelled invoices | 8,292 |

#### Negative Quantity Detection

Transactions with negative quantities were identified using:

```python
negative_quantity = df[df["Quantity"] < 0]
```

Result: 22,950 rows.

#### Zero Quantity Detection

Transactions with zero quantities were identified using:

```python
zero_quantity = df[df["Quantity"] == 0]
```

Result: 0 rows.

#### Initial Interpretation

The dataset contains 19,494 rows associated with invoices beginning with `C` and 22,950 rows with negative quantities.

The two categories are not identical. There are 3,456 more negative-quantity rows than cancelled-invoice rows.

This indicates that negative quantities must be investigated independently of the invoice prefix.

#### Data Quality Decision

No cancellation or negative-quantity records have been deleted.

Further investigation is required to distinguish cancellations, returns, and other negative-quantity transactions before defining the transformation rules.

### 8.4 Price and Negative Quantity Analysis

This investigation focused on identifying negative prices, zero prices, and negative quantities without a cancellation invoice prefix.

#### Price Analysis

The following conditions were checked:

```python
negative_prices = df[df["Price"] < 0]
zero_prices = df[df["Price"] == 0]
```

Results:

| Metric | Result |
|---|---:|
| Negative price rows | 5 |
| Zero price rows | 6,202 |

The five negative-price records have descriptions such as "Adjust bad debt" and invoice identifiers beginning with "A".

These records appear to represent accounting adjustments rather than ordinary product sales.

Zero-price transactions require further investigation because they may represent free products, samples, promotions, or operational adjustments.

#### Negative Quantities Without Cancellation Prefix

The following filter was used:

```python
negative_without_c = df[
    (df["Quantity"] < 0) &
    (~df["Invoice"].astype(str).str.startswith("C"))
]
```

Result: 3,457 rows.

Examples include descriptions such as:

- short
- lost
- damages
- mixed

These records may represent stock corrections, damaged goods, shortages, or other operational adjustments.

#### Data Quality Decisions

- Preserve all five negative-price records in the raw dataset.
- Do not automatically delete zero-price transactions.
- Investigate negative quantities without a C invoice prefix separately.
- Exclude accounting adjustments from ordinary sales revenue calculations unless they are modeled separately.
- Preserve the original transaction records for auditability.

No records have been deleted during this investigation.
### 8.5 Zero-Price Transaction Analysis

**Objective:** Investigate transactions whose unit price is equal to zero and determine whether they represent free products, stock adjustments, or other operational records.

**Method:** Filter the combined DataFrame using `Price == 0` and analyze descriptions, stock codes, quantities, and example transactions.

**Results:**

| Metric | Result |
|---|---:|
| Zero-price rows | 6,202 |
| Rows with missing descriptions among zero-price rows | 4,382 |
| Average quantity | -51.73 |
| Minimum quantity | -9,600 |
| Maximum quantity | 12,540 |
| Median quantity | -2 |

Frequently occurring descriptions include `check`, `damages`, `damaged`, `found`, `missing`, `adjustment`, `short`, and `lost`.

**Observations:**

- Several descriptions indicate operational stock adjustments rather than normal commercial sales.
- Zero-price transactions contain both positive and negative quantities.
- All 4,382 missing descriptions in the dataset appear among the 6,202 zero-price transactions. This relationship must be explicitly verified.
- Some transactions may represent free items, samples, stock corrections, or other exceptional operations.

**Preliminary decision:**

- Preserve all zero-price records in the source data.
- Do not automatically delete them.
- Investigate their characteristics before defining transformation and warehouse rules.
- Separate ordinary sales from operational adjustments when designing analytical measures, if the evidence supports this classification.

**Status:** Investigation in progress. No records have been deleted or modified.
### 8.6 Detailed Zero-Price Analysis

Further investigation was conducted on the 6,202 transactions
whose unit price equals zero.

**1. Missing descriptions**

| Metric | Result |
|---|---:|
| Total missing descriptions | 4,382 |
| Missing descriptions with zero price | 4,382 |
| Missing descriptions with non-zero price | 0 |

All missing descriptions are associated with zero-price transactions.
However, not all zero-price transactions have missing descriptions.

**2. Quantity classification**

| Quantity category | Rows |
|---|---:|
| Negative | 3,457 |
| Positive | 2,745 |
| Zero | 0 |

Negative quantities may represent stock removals, losses, or adjustments.
Positive quantities may represent stock corrections or free items.
These interpretations remain provisional.

**3. Cancellation analysis**

All 6,202 zero-price transactions have invoice numbers
that do not start with the cancellation prefix `C`.

**4. Customer identification**

| Customer ID status | Rows |
|---|---:|
| Missing Customer ID | 6,131 |
| Available Customer ID | 71 |

Approximately 98.9% of zero-price transactions have no Customer ID.

**Preliminary conclusion:**

Zero-price transactions contain several different types of records.
They should not automatically be considered ordinary sales or deleted.
Further investigation is required before defining transformation rules.

No source records have been modified or deleted.
### 8.7 Zero-Price Transactions with Customer IDs

A separate investigation was performed on the 71 zero-price
transactions that contain a Customer ID.

**Results:**
- Number of transactions: 71
- All 71 transactions have positive quantities.
- These records contain identifiable products and customer information.
- Some special records were identified, including:
  - TEST001: This is a test product.
  - Manual
  - PADS

**Interpretation:**

These transactions may represent free products, promotional items,
or special operational transactions. Their exact business meaning
cannot be confirmed using the available columns alone.

Test-related records should be flagged during transformation.

**Decision:**

Preserve the original records and classify exceptional transactions
during the transformation phase where sufficient evidence exists.
### 8.8 General Dataset Profiling

**Dataset dimensions:**
- Rows: 1,067,371
- Columns: 8

**Date range:**
- Start: 2009-12-01 07:45:00
- End: 2011-12-09 12:50:00

**Unique business entities:**
- Invoices: 53,628
- Products: 5,305
- Customers: 5,942
- Countries: 43

**Quantity statistics:**
- Mean: 9.94
- Median: 3
- Minimum: -80,995
- Maximum: 80,995

**Price statistics:**
- Mean: 4.65
- Median: 2.10
- Minimum: -53,594.36
- Maximum: 38,970

**Observations:**
- The United Kingdom represents the majority of transactions.
- Quantity and price contain extreme values.
- Negative quantities and prices require appropriate business rules.
- The customer count represents non-null Customer IDs.

**Conclusion:**

Initial dataset exploration and profiling are complete.
The dataset is sufficiently understood to begin developing
the ETL pipeline. No source records have been modified.
### 8.9 Data Extraction and Parquet Export

The two Excel worksheets were successfully extracted and combined.

- Total rows: 1,067,371
- Total columns: 8
- Output format: Parquet
- Output path: data/processed/retail_extracted.parquet

The following columns were standardized as strings:
- Invoice
- StockCode
- Description

This was necessary because these columns contained mixed Python types,
which prevented PyArrow from exporting them consistently.

The original Excel dataset remains unchanged.

**Status:** Extraction and Parquet export completed successfully.
### 9.1 Exact Duplicate Removal

**Objective:** Identify and remove exact duplicate transaction records.

**Initial dataset:** 1,067,371 rows.

**Results:**
- Exact duplicate occurrences: 34,335
- Rows after duplicate removal: 1,033,036
- Rows removed: 34,335
- Removal rate: approximately 3.22%

**Method:**

Pandas `duplicated()` was used to identify exact duplicates.
`drop_duplicates()` retained the first occurrence of each
identical record.

**Decision:**

Only exact duplicates across all eight columns were removed.
Records sharing an invoice number or product code were preserved
when their other values differed.

The original extracted Parquet dataset remains unchanged.
### 9.2 Missing Description Investigation

After duplicate removal, 4,275 rows had missing descriptions.

All these rows had a unit price of zero.

The StockCode consistency analysis produced:

| Metric | Result |
|---|---:|
| StockCodes with one known description | 3,718 |
| StockCodes with multiple descriptions | 1,232 |
| StockCodes in missing-description rows | 2,451 |
| Missing StockCodes with a known description | 2,096 |
| Missing StockCodes with exactly one description | 1,616 |

**Preliminary cleaning strategy:**

- Recover descriptions for the 1,616 StockCodes with exactly one known description.
- Preserve missing descriptions for the 480 ambiguous StockCodes.
- Preserve missing descriptions for the 355 StockCodes without a known description.

No missing descriptions have been modified yet.
### 9.3 Description Recovery

A description recovery operation was performed using StockCode.

**Results:**

| Metric | Result |
|---|---:|
| Missing descriptions before recovery | 4,275 |
| Recovered descriptions | 2,974 |
| Remaining missing descriptions | 1,301 |
| Recovery rate | 69.54% |

**Method:**

A mapping was created between StockCode and its known description.
Descriptions were recovered only when a StockCode had exactly one
distinct known description.

**Validation:**
- 1,301 missing descriptions remain.
- All remaining missing descriptions have Price = 0.
- No missing descriptions with non-zero prices remain.

**Decision:**

Ambiguous and unavailable descriptions were preserved as missing.
No transaction rows were deleted during this operation.
### 9.4 Customer ID Investigation

After duplicate removal, 235,151 transactions had missing Customer IDs,
representing 22.76% of the cleaned dataset.

**Cancellation analysis:**

| Invoice type | Rows |
|---|---:|
| Non-cancellation invoices | 234,437 |
| Cancellation invoices | 714 |

**Quantity statistics:**
- Mean: 1.51
- Median: 1
- Minimum: -9,600
- Maximum: 10,200

**Price statistics:**
- Mean: 7.71
- Median: 3.29
- Minimum: -53,594.36
- Maximum: 25,111.09

**Cleaning decision:**

Missing Customer IDs will be preserved.

Customer identities cannot be reliably reconstructed from the
available information. Removing these records would result in
a loss of 22.76% of the cleaned dataset.

During warehouse loading, unidentified customers may be represented
by a dedicated Unknown Customer dimension member.

The original missing values will remain unchanged in the staging data.
### 9.5 Cancellation Records Analysis

**Objective:** Analyze invoices identified as cancellations before deciding how to handle them during data cleaning.

**Results after exact duplicate removal:**

| Indicator | Result |
|---|---:|
| Cancellation rows | 19,104 |
| Unique cancelled invoices | 8,292 |
| Average quantity | -24.96 |
| Median quantity | -2 |
| Minimum quantity | -80,995 |
| Maximum quantity | 1 |
| Median unit price | 2.95 |

**Observations:**

- Cancellation records are identified by an invoice number beginning with `C`.
- Most cancellation records have negative quantities.
- The maximum quantity is positive (1), so not every cancellation row has a negative quantity.
- Unit prices are generally positive.
- Cancellation records represent potentially important transaction information and should not automatically be treated as invalid data.

**Cleaning decision:**

Cancellation records will be preserved. A derived Boolean column named `IsCancelled` will be added to distinguish cancellation invoices from other invoices.

The original invoice identifiers and quantities will remain unchanged. This distinction will be useful when calculating net sales in the data warehouse.
### 9.6 Price Anomalies Analysis

**Objective:** Investigate records with zero or negative unit prices.

**Results after exact duplicate removal:**

| Indicator | Count |
|---|---:|
| Zero prices | 6,014 |
| Negative prices | 5 |

**Negative price observations:**

The five negative-price records have the description `Adjust bad debt`. Their invoice identifiers begin with `A`, and their quantities are positive.

These records appear to represent financial adjustments rather than ordinary product sales.

**Zero price observations:**

Zero-price records include both ordinary product descriptions and operational descriptions such as `damages`, `lost`, and `short`.

Their business meaning cannot be determined reliably from the available columns alone.

**Cleaning decisions:**

- Preserve all five negative-price records.
- Preserve all zero-price records.
- Add Boolean indicators to distinguish these records during analysis.
- Do not automatically classify zero-price records as errors.

### 9.7 Summary of Data Cleaning Decisions

| Data quality issue | Decision |
|---|---|
| Exact duplicates | Remove |
| Missing descriptions | Recover when a StockCode has exactly one known description; preserve the remaining missing values |
| Missing Customer IDs | Preserve |
| Cancellation invoices | Preserve and flag |
| Negative prices | Preserve and flag |
| Zero prices | Preserve and flag |

The objective is to retain valid business information while making unusual records identifiable for subsequent analysis and warehouse modeling.
### 9.8 Transaction Flags Creation

Four Boolean columns were added to the cleaned dataset:

| Column | Purpose |
|---|---|
| `IsCancelled` | Identifies cancellation invoices |
| `IsZeroPrice` | Identifies records with a zero unit price |
| `IsNegativePrice` | Identifies records with a negative unit price |
| `IsCustomerUnknown` | Identifies records with a missing Customer ID |

The flags allow unusual transactions and incomplete customer information to be identified without deleting the corresponding records.

### 9.9 Cleaning Stage Summary

After duplicate removal and description recovery:

- Initial rows: 1,067,371
- Exact duplicate rows removed: 34,335
- Final rows: 1,033,036
- Descriptions recovered: 2,974
- Remaining missing descriptions: 1,301
- Missing Customer IDs: 235,151

The cleaned dataset is intended to be saved as `data/processed/retail_cleaned.parquet`, preserving the original extracted dataset separately.

The saved Parquet file must be reloaded and validated before considering the cleaning stage complete.
### 9.10 Cleaned Dataset Export and Validation

The cleaned dataset was successfully exported to:

`data/processed/retail_cleaned.parquet`

**Export results:**

| Metric | Result |
|---|---:|
| Rows | 1,033,036 |
| Columns | 12 |
| File size | 6.76 MB |
| Missing descriptions | 1,301 |
| Missing Customer IDs | 235,151 |
| Cancellation rows | 19,104 |
| Zero-price rows | 6,014 |
| Negative-price rows | 5 |

The exported Parquet file was reloaded using Pandas to verify that the data was correctly saved and remained readable.

All validation results matched the expected values.

**Conclusion:** The initial data cleaning and validation stage is complete. The extracted dataset remains unchanged, while the cleaned dataset is stored separately for subsequent transformation and warehouse loading.
# 10. Data Warehouse Design

## 10.1 Business Process

The data warehouse focuses on online retail sales transactions. It will support analysis of revenue, product performance, customer behavior, geographical distribution, and cancellations.

## 10.2 Fact Table Grain

The grain of `FactSales` is one product transaction line within an invoice.

Each source row represents a product line and retains its invoice identifier, product information, transaction date, customer information, country, quantity, and unit price.

## 10.3 Star Schema

The proposed warehouse contains one fact table and four dimension tables:

- `FactSales`
- `DimDate`
- `DimProduct`
- `DimCustomer`
- `DimCountry`

## 10.4 Fact Table Measures

- Quantity
- UnitPrice
- LineAmount = Quantity × UnitPrice

The fact table also preserves transaction indicators such as IsCancelled, IsZeroPrice, IsNegativePrice, and IsCustomerUnknown.

## 10.5 Dimension Tables

**DimDate:** Calendar date, day, month, quarter, and year.

**DimProduct:** Product StockCode and description.

**DimCustomer:** Customer identifier.

**DimCountry:** Country name.

Each dimension will use a generated surrogate key as its primary key.

The invoice identifier will be retained directly in FactSales as a degenerate dimension.

## 10.6 Technical Design Decisions

- PostgreSQL will be used as the data warehouse database.
- Monetary values will use NUMERIC types to preserve decimal precision.
- Customer identifiers will be converted to nullable integers.
- Full transaction timestamps will be preserved.
- Missing customer identifiers will be represented by an unknown-customer dimension member.
- Product descriptions will not be arbitrarily selected when a StockCode has multiple descriptions.
- Cancellation and unusual-price records will be preserved.

## 10.7 Dataset Coverage

The transaction date range is December 1, 2009 to December 9, 2011.
## 10.8 PostgreSQL Warehouse Schema Creation

The existing PostgreSQL database `retail_dw` is used to host the data warehouse.

A dedicated schema named `dw` was created to organize warehouse tables separately from other database objects.

The schema will contain:

- `dim_date`
- `dim_product`
- `dim_customer`
- `dim_country`
- `fact_sales`

The schema was created using `CREATE SCHEMA IF NOT EXISTS dw`, making the operation safe to execute more than once.
### 10.9 Dimension Tables Creation

Four dimension tables were designed and created in the `dw` schema:

- `dim_date`: Stores calendar attributes using an integer date key in YYYYMMDD format.
- `dim_product`: Stores product codes and descriptions. Multiple descriptions for a StockCode are allowed.
- `dim_customer`: Stores customer identifiers and supports a dedicated unknown-customer member.
- `dim_country`: Stores unique country names.

Surrogate keys are generated for product, customer, and country dimensions using PostgreSQL SERIAL primary keys.

The date dimension uses a deterministic integer key based on the calendar date.
### 10.10 Fact Table Creation

The central fact table `dw.fact_sales` was created.

**Fact table grain:** One row represents one product transaction line within an invoice.

The table contains:

- A generated primary key: `sales_key`.
- Four foreign keys referencing the dimension tables.
- Invoice identifier and full transaction timestamp.
- Quantity, unit price, and line amount.
- Four Boolean transaction indicators.

Foreign-key constraints enforce referential integrity between the fact table and its dimensions.

The original transaction timestamp is retained alongside the integer date key to preserve time-level information.

Customer records with missing identifiers will be linked to a dedicated unknown-customer dimension member during the loading stage.
### 11.1 Loading Date and Product Dimensions

The Python ETL pipeline successfully populated the first two dimension tables.

**DimDate:**
- Distinct source dates: 604
- Records inserted: 604
- Database total: 604

The date dimension contains one record per distinct calendar date, with attributes including day, month, month name, quarter, and year.

**DimProduct:**
- Distinct StockCode-description combinations: 7,405
- Database total: 7,405

The product dimension preserves distinct StockCode-description combinations, including multiple descriptions for the same StockCode and missing descriptions.

Both loading operations completed successfully, and the database counts matched the source-derived counts.
## 8. SQL Analytics and Business Insights

### 8.1 Objective

After loading the cleaned retail dataset into PostgreSQL, SQL analytical queries were developed to evaluate sales performance, identify important products and customers, analyze geographical markets, and monitor data quality.

The analysis uses the Star Schema composed of four dimension tables and one fact table.

### 8.2 Monthly Sales Performance

The monthly sales analysis calculates:
- Total revenue.
- Total quantity sold.
- Number of distinct invoices.

**Key findings:**
- November 2011 recorded the highest monthly revenue, reaching 1,503,866.78.
- November 2010 also recorded strong performance, with 1,464,293.14 in revenue.
- November was the strongest observed sales month in both years.

These results suggest a possible seasonal sales pattern.

### 8.3 Top 10 Products by Revenue

Products were ranked according to their total revenue.

**Key findings:**
- Manual (M) generated the highest revenue: 339,226.24.
- Regency Cake Stand 3 Tier ranked second: 330,590.32.
- DOTCOM Postage ranked third: 309,854.11.
- White Hanging Heart T-Light Holder recorded the highest quantity among the top ten products, with 94,147 units.

Some highly ranked entries represent operational or service codes rather than ordinary merchandise.

### 8.4 Revenue by Country

The geographical analysis identifies the countries generating the highest revenue.

**Key findings:**
- United Kingdom: 17,251,519.96.
- EIRE: 658,767.31.
- Netherlands: 554,038.09.
- Germany: 425,019.71.
- France: 350,456.09.

The United Kingdom is the dominant market in the dataset.

### 8.5 Top 10 Customers

Customers were ranked according to their total revenue, excluding transactions with unknown customer IDs.

**Key findings:**
- Customer 18102 generated the highest revenue: 580,987.04.
- Customer 14646 ranked second: 528,602.52.
- Customer 14911 recorded the highest invoice count among the top ten customers, with 398 invoices.

This analysis helps identify high-value customers and supports customer segmentation strategies.

### 8.6 Cancellation Analysis

Cancellation frequency was analyzed monthly using the following formula:

Cancellation Percentage = (Cancelled Transaction Lines / Total Transaction Lines) × 100

**Key findings:**
- 19,104 cancelled transaction lines were identified.
- May 2010 recorded the highest monthly cancellation percentage: 2.81%.
- November 2011 recorded the lowest monthly cancellation percentage: 1.29%.
- The cancellation percentage remained below 3% in all observed months.

This indicator measures cancelled transaction lines, not cancelled invoices.

### 8.7 Data Quality Overview

The final warehouse contains the following data quality indicators:

| Indicator | Number of Rows |
|---|---:|
| Total transaction rows | 1,033,036 |
| Cancelled rows | 19,104 |
| Zero-price rows | 6,014 |
| Negative-price rows | 5 |
| Unknown customer rows | 235,151 |

Missing customer identifiers represent approximately 22.76% of transaction rows. These records were preserved and associated with a dedicated unknown customer dimension member.

### 8.8 Conclusion

The analytical SQL layer demonstrates that the data warehouse can support business-oriented analysis.

The implemented queries provide insights into:
- Sales evolution over time.
- Product revenue performance.
- Geographical market performance.
- Customer revenue contribution.
- Cancellation trends.
- Data quality indicators.

The warehouse therefore provides a structured foundation for further business intelligence and data visualization.

## 9. Docker Containerization

### 9.1 Objective

The project was containerized using Docker and Docker Compose to provide a reproducible and portable execution environment.

Containerization separates the Python ETL application from the PostgreSQL database while allowing both services to communicate through a Docker network.

### 9.2 Container Architecture

The Docker environment consists of two services:

**1. PostgreSQL Database Container**
- Uses the official PostgreSQL 18 image.
- Hosts the `retail_dw` database.
- Stores warehouse data in a persistent Docker volume.
- Exposes PostgreSQL through port 5433 on the host machine.

**2. Python ETL Container**
- Uses Python 3.11 slim as its base image.
- Installs project dependencies from `requirements.txt`.
- Executes the extraction, cleaning, and loading scripts sequentially.
- Connects to PostgreSQL through the Docker network using the service name `database`.

### 9.3 Docker Files

| File | Responsibility |
|---|---|
| Dockerfile | Builds the Python ETL application image. |
| docker-compose.yml | Defines and orchestrates both services. |
| .dockerignore | Excludes unnecessary files from the build context. |
| .env | Stores database connection configuration. |

### 9.4 Data Persistence and Networking

Docker Compose creates an internal network allowing the Python application to communicate with PostgreSQL.

The ETL application uses `database` as its database hostname and port `5432` inside the Docker network.

A named Docker volume, `postgres_data`, preserves PostgreSQL data when containers are stopped or removed.

The original Excel dataset is mounted into the ETL container as read-only, while processed Parquet files are stored in the project's local data directory.

### 9.5 Execution Workflow

The containerized pipeline follows these steps:

1. Build the Python application image.
2. Start the PostgreSQL database container.
3. Wait for PostgreSQL health checks to succeed.
4. Execute data extraction.
5. Execute data cleaning and transformation.
6. Load dimension tables into PostgreSQL.
7. Load transaction records into the fact table.
8. Validate warehouse record counts and statistics.

### 9.6 Execution Results

The complete ETL pipeline was successfully executed inside Docker.

| Warehouse table | Records |
|---|---:|
| dim_date | 604 |
| dim_product | 7,405 |
| dim_customer | 5,943 |
| dim_country | 43 |
| fact_sales | 1,033,036 |

The final database validation confirmed that all 1,033,036 expected transaction records were successfully loaded.

### 9.7 Conclusion

Docker and Docker Compose successfully containerized the Retail Data Engineering pipeline and PostgreSQL Data Warehouse.

The implementation provides an isolated execution environment, service communication, persistent database storage, and reproducible ETL execution.
