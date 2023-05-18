# import pandas as pd
#
# # Load the first Excel file into a pandas DataFrame
# df1 = pd.read_excel('Seasonailty.xlsx')
#
# # Load the second Excel file into a pandas DataFrame
# df2 = pd.read_excel('Categories List.xlsx')
#
# # Merge the two DataFrames based on the Product Name and CropName columns
# merged_df = pd.merge(df1, df2, left_on='CropName', right_on='Product Name', how='inner')
#
# # Select only the necessary columns
# final_df = merged_df[['CropName', 'Country', 'CropProcess', 'variety', 'region', 'HarvestMonths', 'category']]
#
# # Save the final DataFrame to a new Excel file
# final_df.to_excel('final_file.xlsx', index=False)
import pandas as pd

file1 = pd.read_excel('Seasonailty.xlsx')
file2 = pd.read_excel('Categories List.xlsx')
# Yahan rename krdia cropname ko
file1 = file1.rename(columns={'CropName': 'Product Name'})
# left_on right_on ki jaga just on
merged_data = file1.merge(file2, on='Product Name', how='inner')
# Yahan remove krdien jin products ki category ni mili
merged_data = merged_data.dropna(subset=['category'])
final_data = merged_data[['Product Name', 'Country', 'variety', 'category']]
final_data.to_excel('merged_data.xlsx', index=False)