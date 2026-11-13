
import pandas as pd

file_path = "data/raw/online_retail_II.xlsx"

# Read both worksheets
df_2009 = pd.read_excel(
    file_path,
    sheet_name="Year 2009-2010"
)

df_2010 = pd.read_excel(
    file_path,
    sheet_name="Year 2010-2011"
)

# Combine both DataFrames
df = pd.concat(
    [df_2009, df_2010],
    ignore_index=True
)

# Display information
print("Combined dataset dimensions:", df.shape)

print("\nFirst 5 rows:")
print(df.head())

print("\nLast 5 rows:")
print(df.tail())

print("\nMissing values:")
print(df.isnull().sum())
# Verify missing descriptions and zero prices
print("\n===== MISSING DESCRIPTION VERIFICATION =====")

missing_description = df["Description"].isna()
zero_price = df["Price"] == 0

print("Total missing descriptions:", missing_description.sum())

print(
    "Missing descriptions with zero price:",
    (missing_description & zero_price).sum()
)

print(
    "Missing descriptions with non-zero price:",
    (missing_description & ~zero_price).sum()
)

# Classify zero-price transactions by quantity
zero_price_df = df[zero_price].copy()

zero_price_df["Quantity_Category"] = zero_price_df["Quantity"].apply(
    lambda q: "Negative" if q < 0
    else "Positive" if q > 0
    else "Zero"
)

print("\n===== ZERO-PRICE QUANTITY CLASSIFICATION =====")
print(zero_price_df["Quantity_Category"].value_counts())

# Check cancellation invoice prefix
zero_price_df["Is_Cancellation"] = (
    zero_price_df["Invoice"].astype(str).str.startswith("C")
)

print("\n===== ZERO-PRICE CANCELLATION ANALYSIS =====")
print(zero_price_df["Is_Cancellation"].value_counts())

# Customer ID analysis
print("\n===== ZERO-PRICE CUSTOMER ANALYSIS =====")
print("Missing Customer IDs:", zero_price_df["Customer ID"].isna().sum())
print("Available Customer IDs:", zero_price_df["Customer ID"].notna().sum())