import pandas as pd

# Define the input file path
input_csv_path = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\2_cleaned_data.csv"

# Read the input CSV file
df = pd.read_csv(input_csv_path)

# Function to extract and clean the second number from the Price column
def extract_second_price(price):
    try:
        # Split the price by space and return the second part
        price_parts = price.split()
        
        if len(price_parts) == 2:
            # Clean the second part by removing dots and converting to float
            clean_price = price_parts[1]# Remove dot characters
            return float(clean_price)  # Convert the cleaned string to float
        
        # If there's no space or invalid format, return None
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
