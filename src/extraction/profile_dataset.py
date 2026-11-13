
import pandas as pd

# 1. Load both worksheets
file_path = "data/raw/online_retail_II.xlsx"

df_2009 = pd.read_excel(file_path, sheet_name="Year 2009-2010")
df_2010 = pd.read_excel(file_path, sheet_name="Year 2010-2011")

# 2. Combine both datasets
df = pd.concat([df_2009, df_2010], ignore_index=True)

print("===== GENERAL DATASET PROFILE =====")

# 3. Dataset dimensions
print("\nDataset shape:", df.shape)

# 4. Date range
print("\n===== DATE RANGE =====")
print("First transaction:", df["InvoiceDate"].min())
print("Last transaction:", df["InvoiceDate"].max())

# 5. Unique business entities
print("\n===== UNIQUE VALUES =====")
print("Unique invoices:", df["Invoice"].nunique())
print("Unique products:", df["StockCode"].nunique())
print("Unique customers:", df["Customer ID"].nunique())
print("Unique countries:", df["Country"].nunique())

# 6. Quantity statistics
print("\n===== QUANTITY STATISTICS =====")
print(df["Quantity"].describe())

# 7. Price statistics
print("\n===== PRICE STATISTICS =====")
print(df["Price"].describe())

# 8. Countries
print("\n===== COUNTRIES =====")
print(df["Country"].value_counts())

print("\nDataset profiling completed.")
