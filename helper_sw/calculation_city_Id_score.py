import pandas as pd

# Define the input file path
input_csv_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\4_filtered_data_without_outliers.csv"

# Read the input CSV file
df = pd.read_csv(input_csv_path)

# Group by 'city_id' and calculate the mean of 'Price_cleaned'
df_grouped = df.groupby('city_id')['Price_cleaned'].mean().reset_index()

# Rename the columns for clarity
df_grouped.columns = ['city_id', 'Price_cleaned_mean']

# Round the 'Price_cleaned_mean' to 3 decimal places
df_grouped['Price_cleaned_mean'] = df_grouped['Price_cleaned_mean'].round(3)

# Drop duplicates to ensure one entry per city_id
df_grouped = df_grouped.drop_duplicates(subset='city_id')

# Define the output file path with a different name
output_csv_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\5_cleaned_data_with_unique_city_id_and_mean.csv"

# Save the grouped and cleaned data to a new CSV file
df_grouped.to_csv(output_csv_path, index=False)

print(f"Data with unique city_id and Price_cleaned_mean has been saved to: {output_csv_path}")
