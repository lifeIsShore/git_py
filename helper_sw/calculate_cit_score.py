import pandas as pd

# Define the input file path
input_csv_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\combined_data.csv"

# Read the input CSV file
df = pd.read_csv(input_csv_path)

# Extract only the 'Price' and 'city_id' columns
df_filtered = df[['Price', 'city_id']]

# Define the output file path
output_csv_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\1_filtered_data.csv"

# Save the filtered data to a new CSV file
df_filtered.to_csv(output_csv_path, index=False)

print(f"Filtered data has been saved to: {output_csv_path}")
