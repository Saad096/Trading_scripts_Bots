import pandas as pd

# Load the CSV file
df = pd.read_csv('raw_products (1).csv')

# Get the number of rows in the DataFrame
nrows = df.shape[0]

# Calculate the number of rows in each quarter
quarter_size = nrows // 4

# Split the DataFrame into four equal parts
part_1 = df.iloc[:quarter_size]
part_2 = df.iloc[quarter_size:2*quarter_size]
part_3 = df.iloc[2*quarter_size:3*quarter_size]
part_4 = df.iloc[3*quarter_size:]

# Save each part as a CSV file
part_1.to_csv('product_part_1.csv', index=False)
part_2.to_csv('product_part_2.csv', index=False)
part_3.to_csv('product_part_3.csv', index=False)
part_4.to_csv('product_part_4.csv', index=False)
