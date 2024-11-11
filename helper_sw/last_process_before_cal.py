import pandas as pd

# Define the input file path
input_csv_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\1_filtered_data.csv"

# Read the input CSV file
df = pd.read_csv(input_csv_path)

# Function to clean the Price column
def clean_price(price):
    try:
        # Split the price by space and get the second part if available
        price_parts = price.split()
        
        if len(price_parts) == 2:
            # Get the second part and clean it
            clean_price = price_parts[1].replace('.', '').replace(',', '.')
            return float(clean_price)  # Convert to float
            
        # If there's no space, it's a single number or invalid
        return None
        
    except Exception:
        return None  # If there's any error, return None to mark it for removal

# Apply the clean_price function to the 'Price' column
df['Cleaned_Price'] = df['Price'].apply(lambda x: clean_price(str(x)))

# Remove rows where Cleaned_Price is None (invalid or single value)
df_cleaned = df.dropna(subset=['Cleaned_Price'])

# Keep only the columns 'Price' and 'city_id'
df_cleaned = df_cleaned[['Price', 'city_id']]

# Define the output file path
output_csv_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\2_cleaned_data.csv"

# Save the cleaned data to a new CSV file
df_cleaned.to_csv(output_csv_path, index=False)

print(f"Cleaned data has been saved to: {output_csv_path}")
