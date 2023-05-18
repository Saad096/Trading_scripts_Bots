import os
import glob
import pandas as pd

# Set the folder path containing the CSV files
folder_path = 'varities'

# Get a list of all CSV files in the folder
csv_files = glob.glob(os.path.join(folder_path, '*.csv'))

# Initialize an empty DataFrame to store the concatenated data
concatenated_data = pd.DataFrame()

# Loop through the CSV files and concatenate their data
for file in csv_files:
    # Read the CSV file into a DataFrame
    data = pd.read_csv(file)

    # Concatenate the data into the concatenated_data DataFrame
    concatenated_data = pd.concat([concatenated_data, data], ignore_index=True)

# Save the concatenated data to a new CSV file called 'fruits_varieties.csv'
output_file = os.path.join(folder_path, 'fruits_varieties.csv')
concatenated_data.to_csv(output_file, index=False)

print("Data from all CSV files has been concatenated into 'fruits_varieties.csv'")
