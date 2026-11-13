import pandas as pd

# Path to the original dataset
file_path = "data/raw/online_retail_II.xlsx"
# Read the second worksheet
df = pd.read_excel(file_path, sheet_name=1)
print("info about the second sheet")
# Display basic information
print("\nFirst 5 rows:")
print(df.head())

print("\nDataset dimensions:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())
