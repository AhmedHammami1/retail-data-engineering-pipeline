
import pandas as pd
from pathlib import Path


def extract_data():
    # 1. Locate the project directory
    project_root = Path(__file__).resolve().parents[2]

    # 2. Define source and destination paths
    file_path = project_root / "data" / "raw" / "online_retail_II.xlsx"
    output_path = project_root / "data" / "processed" / "retail_extracted.parquet"

    # 3. Read both Excel worksheets
    print("Reading Excel worksheets...")

    df_2009 = pd.read_excel(
        file_path,
        sheet_name="Year 2009-2010"
    )

    df_2010 = pd.read_excel(
        file_path,
        sheet_name="Year 2010-2011"
    )

    # 4. Combine both DataFrames
    df = pd.concat(
        [df_2009, df_2010],
        ignore_index=True
    )
    df["Invoice"] = df["Invoice"].astype("string")
    df["StockCode"] = df["StockCode"].astype("string")
    df["Description"] = df["Description"].astype("string")

    print("Extraction completed!")
    print("Dataset shape:", df.shape)

    # 5. Save the extracted dataset as Parquet
    df.to_parquet(output_path, index=False)

    print("Extracted dataset saved successfully!")
    print("Output file:", output_path)
    print("File exists:", output_path.exists())
    print("File size (MB):", round(output_path.stat().st_size / (1024 * 1024), 2))
    return df


if __name__ == "__main__":
    df = extract_data()
