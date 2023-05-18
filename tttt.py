import pandas as pd

# Load the two CSV files into pandas dataframes
df1 = pd.read_csv('fruit.csv')
df2 = pd.read_csv('C:\\Users\\PF-Enterprises\\Desktop\\Scripting_By_Saad_Alam\\varities\\fruits_varieties.csv')

# Create a list of unique values in the Name column of the first dataframe
unique_names = df1['Name'].unique().tolist()

# Create a new dataframe with the Product name and Varieties columns from the second dataframe
new_df = df2[['Unnamed: 0','Product name', 'Varieties']].copy()

# Loop through the list of unique values and check if each value is in the Product name column of the new dataframe
missing_names = []
for name in unique_names:
    if not new_df['Product name'].isin([name]).any():
        # If the value is not in the Product name column, add it to the list of missing names
        missing_names.append(name)

# Create a new dataframe with the missing names
missing_df = pd.DataFrame({'Product name': missing_names, 'Varieties': ''})

# Concatenate the new dataframe with the original dataframe
new_df = pd.concat([new_df, missing_df])

# Save the updated dataframe to a new CSV file
new_df.to_csv('verified_product_varieties1.csv', index=False)

