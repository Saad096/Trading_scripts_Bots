import pandas as pd
import glob

# Specify the path to the directory containing the CSV files
csv_dir = 'C:\\Users\\PF-Enterprises\\Desktop\\Scripting_By_Saad_Alam\\Bugged product Scrapped files\\'

# Get a list of all CSV files in the directory
csv_files = glob.glob(csv_dir + '\\*.xlsx')

# Initialize an empty list to store the data from all CSV files
data = []

# Iterate over each CSV file
for file in csv_files:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_excel(file)
    # Append the data from the DataFrame to the list
    data.append(df)

# Concatenate the data from all DataFrames into a single DataFrame
merged_data = pd.concat(data, ignore_index=True)

# Specify the output file path for the merged data
output_file = 'C:\\Users\\PF-Enterprises\\Desktop\\Scripting_By_Saad_Alam\\CSV_merged.xlsx'

# Save the merged data to a CSV file
merged_data.to_excel(output_file, index=False)
