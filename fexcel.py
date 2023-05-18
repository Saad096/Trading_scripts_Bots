import os
import pandas as pd

# Directory containing the Excel files
directory = r'C:\Users\PF-Enterprises\Documents\vegetables'

# Output file name
output_file = 'Category_wise_data_with_variety_of_vegetables.xlsx'

# Initialize an empty dataframe to store the merged data
merged_data = pd.DataFrame(columns=['Category', 'HScode', 'Product Name', 'Variety'])

# Loop through all the files in the directory
for filename in os.listdir(directory):
    if filename.endswith('.xlsx'):
        # Read the Excel file into a dataframe
        file_path = os.path.join(directory, filename)
        df = pd.read_excel(file_path)

        # Check if column names are matching and rename if necessary
        if 'Hscode' in df.columns:
            df.rename(columns={'Hscode': 'HScode'}, inplace=True)
        if 'ProductName' in df.columns:
            df.rename(columns={'ProductName': 'Product Name'}, inplace=True)
        if 'variety' in df.columns:
            df.rename(columns={'variety': 'Variety'}, inplace=True)

        # Add 'Category' column with value 'Fruits'
        df['Category'] = 'Vegetable'

        # Merge the data into the merged_data dataframe
        merged_data = pd.concat([merged_data, df], ignore_index=True)

# Drop duplicates based on the 'Variety' column
merged_data.drop_duplicates(subset='Variety', inplace=True)

# Reset the index
merged_data.reset_index(drop=True, inplace=True)

# Write the merged data to the output file
merged_data.to_excel(output_file, index=False)

print(f'Success! Merged data has been saved to {output_file}.')
