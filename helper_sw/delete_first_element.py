import pandas as pd

# Define the input file path
input_csv_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\2_cleaned_data.csv"

# Read the input CSV file
df = pd.read_csv(input_csv_path)

# Function to extract the second number from the Price column
def extract_second_price(price):
    try:
        # Split the price by space and return the second part
        price_parts = price.split()
        
        if len(price_parts) == 2:
            # Return the second part after cleaning
            clean_price = price_parts[1].replace('.', '').replace(',', '.')
            return clean_price  # Return the second part as a string for the updated Price column
        
        # If there's no space, return None to indicate invalid entry
        return None
        
    except Exception:
        return None  # If there's any error, return None

# Apply the extract_second_price function to the 'Price' column
df['Price_cleaned'] = df['Price'].apply(lambda x: extract_second_price(str(x)))

# Remove rows where 'Price_cleaned' is None (invalid entries)
df_cleaned = df.dropna(subset=['Price_cleaned'])

# Define the output file path with a different name
output_csv_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\3_ready_for_cal_data.csv"

# Save the cleaned data to a new CSV file
df_cleaned.to_csv(output_csv_path, index=False)

print(f"Cleaned data has been saved to: {output_csv_path}")
