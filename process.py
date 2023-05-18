import pandas as pd

# Read the CSV file into a pandas DataFrame
df = pd.read_csv('C:\\Users\\PF-Enterprises\\Downloads\\Final_Product.csv')

# Specify the variety values to filter the data
variety_values = ['Beef Cattle', 'Bullock', 'Hanwoo', 'Kedah Kelantan', 'Aubrac', 'Salers', 'Rouge des près', 'Angus', 'Hereford', 'Wagyu', 'Black Angus', 'Heifer', 'Bull', 'Herefordshire', 'Red Angus', 'Dexter', 'Brahman', 'Shorthorn', 'Charolais', 'Limousin', 'Canterbury Angus', 'Rubia Gallega', 'Wakanui', 'Fiorentina', 'Ox', 'Nelore', 'Chianina', 'Blonde', 'Caledonia Crown', 'Maori Lakes', 'Canterbury', 'Cinta Senese DOP', 'Riverlands Angus', 'Greenstone Creek', 'Riverlands', 'Heifer - Scottona', 'Local Indian Dairy', 'Turina', 'Cow', 'Young Bull', 'Brangus', 'Whole birds', 'Calf', 'Dikbil', 'Bovine', 'Cow and Bull', 'Senepol', 'Brown Swiss Cattle', 'Sanhe', 'Barrosã', 'Red Bororo', 'Mirandesa', 'Crossbreed - Unspecified']


# Filter the data based on the variety values and select the columns you want
filtered_data = df.loc[df['variety'].isin(variety_values), ['category', 'Hscode', 'ProductName']].drop_duplicates()

# Save the filtered data to another CSV file
filtered_data.to_csv('for_process.csv', index=False)