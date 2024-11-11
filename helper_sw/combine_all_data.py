import os
import pandas as pd
import glob

def combine_csv_files(input_folder, output_file):
    # Find all CSV files in the input folder matching the batch pattern
    all_files = glob.glob(os.path.join(input_folder, "found_addresses_with_scores_batch_*.csv"))
    # Sort the files by the batch number in their names to ensure the correct order
    all_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
    
    # Combine all files
    combined_df = pd.concat((pd.read_csv(f, encoding="windows-1252") for f in all_files), ignore_index=True)
    
    # Save the combined CSV to the specified output file
    combined_df.to_csv(output_file, index=False, encoding="windows-1252")
    print(f"Combined CSV saved to: {output_file}")

# Define paths
input_folder = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined"
output_file = r"C:\Users\ahmty\Desktop\Python\geo_DSproject_github_clone\git_py\csv_output\combined\will be used\data with geospatial\combined_data.csv"

# Run the function
combine_csv_files(input_folder, output_file)
