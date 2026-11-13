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