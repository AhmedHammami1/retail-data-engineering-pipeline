
import pandas as pd
from pathlib import Path


def clean_data():

    # 1. Locate project directory
    project_root = Path(__file__).resolve().parents[2]

    # 2. Load extracted dataset
    input_path = (
        project_root / "data" / "processed" / "retail_extracted.parquet"
    )

    df = pd.read_parquet(input_path)

    print("===== INITIAL DATASET =====")
    print("Rows before cleaning:", len(df))

    # 3. Detect exact duplicates
    duplicate_count = df.duplicated().sum()

    print("\n===== DUPLICATE ANALYSIS =====")
    print("Exact duplicate occurrences:", duplicate_count)

    # 4. Remove exact duplicates
    df_cleaned = df.drop_duplicates().copy()

    # 5. Missing values analysis
    print("\n===== MISSING VALUES AFTER DUPLICATE REMOVAL =====")

    missing_values = df_cleaned.isnull().sum()

    print(missing_values)

    print("\nMissing percentage:")
    print((missing_values / len(df_cleaned) * 100).round(2))

    # 6. Investigate missing descriptions
    print("\n===== MISSING DESCRIPTION INVESTIGATION =====")

    missing_desc = df_cleaned[df_cleaned["Description"].isna()]

    print("Rows with missing descriptions:", len(missing_desc))

    print("\nPrice distribution:")
    print(missing_desc["Price"].value_counts(dropna=False))

    print("\nQuantity statistics:")
    print(missing_desc["Quantity"].describe())

    print("\nMost frequent StockCodes:")
    print(missing_desc["StockCode"].value_counts().head(15))

    print("\n===== AFTER DUPLICATE REMOVAL =====")
    print("Rows after cleaning:", len(df_cleaned))
    print("Rows removed:", len(df) - len(df_cleaned))

    # 7. Check StockCode description consistency
    print("\n===== STOCKCODE DESCRIPTION CONSISTENCY =====")

    description_counts = (
        df_cleaned.dropna(subset=["Description"])
        .groupby("StockCode")["Description"]
        .nunique()
    )

    consistent_codes = description_counts[description_counts == 1]
    inconsistent_codes = description_counts[description_counts > 1]

    missing_codes = missing_desc["StockCode"].unique()

    print("Unique StockCodes with one description:", len(consistent_codes))
    print("StockCodes with multiple descriptions:", len(inconsistent_codes))
    print("Missing-description StockCodes:", len(missing_codes))

    print(
        "Missing StockCodes with a known description:",
        sum(code in description_counts.index for code in missing_codes)
    )

    print(
        "Missing StockCodes with exactly one description:",
        sum(code in consistent_codes.index for code in missing_codes)
    )

    # 8. Build mapping of StockCode to its unique description
    description_mapping = (
        df_cleaned.dropna(subset=["Description"])
        .groupby("StockCode")["Description"]
        .agg(lambda x: x.unique()[0] if x.nunique() == 1 else None)
        .dropna()
    )

    # 9. Recover missing descriptions
    missing_before = df_cleaned["Description"].isna().sum()

    df_cleaned["Description"] = df_cleaned["Description"].fillna(
        df_cleaned["StockCode"].map(description_mapping)
    )

    missing_after = df_cleaned["Description"].isna().sum()

    print("\n===== DESCRIPTION RECOVERY =====")
    print("Missing descriptions before:", missing_before)
    print("Descriptions recovered:", missing_before - missing_after)
    print("Missing descriptions remaining:", missing_after)

    # 10. Validate description recovery
    print("\n===== DESCRIPTION RECOVERY VALIDATION =====")

    print("Recovered rows:", missing_before - missing_after)
    print(
        "Remaining missing descriptions:",
        df_cleaned["Description"].isna().sum()
    )

    print(
        "Missing descriptions with non-zero price:",
        (
            df_cleaned["Description"].isna()
            & (df_cleaned["Price"] != 0)
        ).sum()
    )

    print("\nExamples of remaining missing descriptions:")
    print(
        df_cleaned[df_cleaned["Description"].isna()]
        [["StockCode", "Quantity", "Price", "Country"]]
        .head(10)
    )

    # 11. Investigate missing Customer IDs
    print("\n===== CUSTOMER ID INVESTIGATION =====")

    missing_customer = df_cleaned[df_cleaned["Customer ID"].isna()]

    print("Missing Customer IDs:", len(missing_customer))

    print("\nPercentage:")
    print(round(len(missing_customer) / len(df_cleaned) * 100, 2), "%")

    print("\nCancellation analysis:")
    print(
        missing_customer["Invoice"]
        .astype(str)
        .str.startswith("C")
        .value_counts()
    )

    print("\nQuantity statistics:")
    print(missing_customer["Quantity"].describe())

    print("\nPrice statistics:")
    print(missing_customer["Price"].describe())

    # 12. Cancellation analysis
    print("\n===== CANCELLATION ANALYSIS =====")

    cancelled = df_cleaned[
        df_cleaned["Invoice"].astype(str).str.startswith("C")
    ]

    print("Cancellation rows:", len(cancelled))
    print("Unique cancelled invoices:", cancelled["Invoice"].nunique())

    print("\nQuantity statistics:")
    print(cancelled["Quantity"].describe())

    print("\nPrice statistics:")
    print(cancelled["Price"].describe())

    print("\nCancellation price distribution:")
    print(cancelled["Price"].value_counts().head(10))

    # 13. Price anomalies
    print("\n===== PRICE ANOMALIES =====")

    print("Negative prices:", (df_cleaned["Price"] < 0).sum())
    print("Zero prices:", (df_cleaned["Price"] == 0).sum())

    print("\nRows with negative prices:")
    print(
        df_cleaned[df_cleaned["Price"] < 0][
            ["Invoice", "StockCode", "Description", "Quantity", "Price"]
        ].to_string(index=False)
    )

    print("\nExamples of zero-price records:")
    print(
        df_cleaned[df_cleaned["Price"] == 0][
            ["Invoice", "StockCode", "Description", "Quantity", "Customer ID"]
        ].head(10).to_string(index=False)
    )

    # 14. Create transaction flags

    # Identify cancellation invoices
    df_cleaned["IsCancelled"] = (
        df_cleaned["Invoice"].str.startswith("C", na=False)
    )

    # Identify zero prices
    df_cleaned["IsZeroPrice"] = df_cleaned["Price"] == 0

    # Identify negative prices
    df_cleaned["IsNegativePrice"] = df_cleaned["Price"] < 0

    # Identify missing Customer IDs
    df_cleaned["IsCustomerUnknown"] = (
        df_cleaned["Customer ID"].isna()
    )

    print("\n===== TRANSACTION FLAGS VALIDATION =====")

    for column in [
        "IsCancelled",
        "IsZeroPrice",
        "IsNegativePrice",
        "IsCustomerUnknown"
    ]:
        print(f"\n{column}:")
        print(df_cleaned[column].value_counts())

    # 15. Save cleaned dataset
    output_path = (
        project_root / "data" / "processed" / "retail_cleaned.parquet"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    df_cleaned.to_parquet(output_path, index=False)

    print("\n===== CLEANED DATASET SAVED =====")
    print("Output path:", output_path)
    print("Final shape:", df_cleaned.shape)

    print(
        "File size:",
        round(output_path.stat().st_size / (1024 * 1024), 2),
        "MB"
    )

    # 16. Reload saved dataset for validation
    df_check = pd.read_parquet(output_path)

    print("\n===== FINAL VALIDATION =====")
    print("Rows:", len(df_check))
    print("Columns:", len(df_check.columns))
    print("Missing descriptions:", df_check["Description"].isna().sum())
    print("Missing Customer IDs:", df_check["Customer ID"].isna().sum())
    print("Cancelled rows:", df_check["IsCancelled"].sum())
    print("Zero-price rows:", df_check["IsZeroPrice"].sum())
    print("Negative-price rows:", df_check["IsNegativePrice"].sum())

    return df_cleaned


if __name__ == "__main__":
    df_cleaned = clean_data()
