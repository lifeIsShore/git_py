import pandas as pd
import numpy as np
import csv

# File paths
input_csv_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\combined_data.csv"
output_full_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\data_with_city_score.csv"
output_city_score_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\city_scores.csv"

# Read the CSV with error handling for skipped lines and BOM handling
try:
    df = pd.read_csv(
        input_csv_path,
        delimiter=";",
        encoding="utf-8-sig",  # Handles BOM if present
        quoting=csv.QUOTE_NONE,
        on_bad_lines="warn"  # Skips lines with problems and logs them
    )
except Exception as e:
    print(f"Error reading the CSV file: {e}")
    raise

# Debug: Print the column names to check for issues with 'Price' column
print("Column names in the CSV:", df.columns)

# Strip any extra spaces from the column names
df.columns = df.columns.str.strip()

# Check if 'Price' column exists
if 'Price' not in df.columns:
    print("The 'Price' column is missing or misnamed. Available columns are:")
    print(df.columns)

# If the column exists, proceed to extract the price per square meter (m²)
if 'Price' in df.columns:
    df['price_per_m2'] = df['Price'].str.split().str[1].str.replace('.', '').str.replace(',', '.').astype(float)

    # Group by 'city_id' and calculate the mean price per m², then take the log
    city_scores = df.groupby('city_id')['price_per_m2'].mean().apply(np.log).reset_index()
    city_scores.rename(columns={'price_per_m2': 'city_score'}, inplace=True)

    # Merge city scores back into the main DataFrame
    df = df.merge(city_scores, on='city_id', how='left')

    # Save the full DataFrame with city scores included
    df.to_csv(output_full_path, index=False, encoding="windows-1252")

    # Save the city scores to a separate CSV
    city_scores.to_csv(output_city_score_path, index=False, encoding="windows-1252")

    print("Processing completed successfully. Files saved to specified output paths.")
else:
    print("The 'Price' column is not available in the CSV file.")
