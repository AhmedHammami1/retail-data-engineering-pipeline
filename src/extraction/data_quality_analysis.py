
import pandas as pd

file_path = "data/raw/online_retail_II.xlsx"

# Read both worksheets
df_2009 = pd.read_excel(file_path, sheet_name="Year 2009-2010")
df_2010 = pd.read_excel(file_path, sheet_name="Year 2010-2011")

# Combine the worksheets
df = pd.concat([df_2009, df_2010], ignore_index=True)

# Analyze duplicates
duplicate_count = df.duplicated().sum()

print("Total rows:", len(df))
print("Number of duplicate rows:", duplicate_count)

print("\nFirst 10 duplicate records:")
print(df[df.duplicated(keep=False)].head(10))

# Investigate duplicate groups

duplicate_rows = df[df.duplicated(keep=False)]

duplicate_groups = (
    df.groupby(list(df.columns), dropna=False)
      .size()
      .reset_index(name="Occurrences")
)

duplicate_groups = duplicate_groups[
    duplicate_groups["Occurrences"] > 1
]

print("\n===== DUPLICATE INVESTIGATION =====")

print("Rows involved in duplicate groups:", len(duplicate_rows))

print("Number of duplicate groups:", len(duplicate_groups))

print(
    "Extra duplicate occurrences:",
    (duplicate_groups["Occurrences"] - 1).sum()
)

print("\nTop 10 most repeated records:")
print(
    duplicate_groups
    .sort_values("Occurrences", ascending=False)
    .head(10)
)

# Analyze cancellations and negative quantities

# Invoices beginning with C
cancelled = df[
    df["Invoice"].astype(str).str.startswith("C")
]

# Transactions with negative quantities
negative_quantity = df[df["Quantity"] < 0]

# Transactions with zero quantities
zero_quantity = df[df["Quantity"] == 0]

print("\n===== CANCELLATION ANALYSIS =====")

print("Cancelled invoice rows:", len(cancelled))

print("Unique cancelled invoices:", cancelled["Invoice"].nunique())

print("\n===== QUANTITY ANALYSIS =====")

print("Negative quantity rows:", len(negative_quantity))

print("Zero quantity rows:", len(zero_quantity))

print("\nExamples of cancelled transactions:")
print(cancelled.head())

print("\nExamples of negative quantities:")
print(negative_quantity.head())

# Analyze prices
negative_prices = df[df["Price"] < 0]
zero_prices = df[df["Price"] == 0]

# Negative quantities without a cancellation invoice
negative_without_c = df[
    (df["Quantity"] < 0) &
    (~df["Invoice"].astype(str).str.startswith("C"))
]

print("\n===== PRICE ANALYSIS =====")

print("Negative prices:", len(negative_prices))
print("Zero prices:", len(zero_prices))

print("\nExamples of negative prices:")
print(negative_prices.head())

print("\n===== NEGATIVE QUANTITY WITHOUT CANCELLATION PREFIX =====")

print("Number of rows:", len(negative_without_c))

print("\nExamples:")
print(negative_without_c.head(10))

# Investigate zero-price transactions

zero_price_df = df[df["Price"] == 0]

print("\n===== ZERO PRICE INVESTIGATION =====")

print("Number of zero-price rows:", len(zero_price_df))

print("\nMost frequent descriptions:")
print(zero_price_df["Description"].value_counts(dropna=False).head(20))

print("\nMost frequent stock codes:")
print(zero_price_df["StockCode"].value_counts().head(20))

print("\nQuantity statistics:")
print(zero_price_df["Quantity"].describe())

print("\nExamples of zero-price transactions:")
print(zero_price_df.head(15))
# Investigate zero-price transactions with a Customer ID
zero_price_with_customer = zero_price_df[
    zero_price_df["Customer ID"].notna()
]

print("\n===== ZERO-PRICE TRANSACTIONS WITH CUSTOMER IDs =====")

print("Number of rows:", len(zero_price_with_customer))

print("\nDescriptions:")
print(
    zero_price_with_customer["Description"]
    .value_counts(dropna=False)
)

print("\nQuantity classification:")
print(
    zero_price_with_customer["Quantity"].apply(
        lambda q: "Negative" if q < 0 else "Positive" if q > 0 else "Zero"
    ).value_counts()
)

print("\nExamples:")
print(zero_price_with_customer.to_string(index=False))

