import os
import csv

# get all file names in the 'Data' directory
data_files = os.listdir('Data')

# remove the extension (.csv) from each file name
data_files = [os.path.splitext(filename)[0] for filename in data_files]

# open the CSV file and read the Product Name column
with open('Vegetable List - Product.csv', 'r') as csv_file:
    reader = csv.DictReader(csv_file)
    product_names = [row['Product Name'] for row in reader]

# find the product names that are not in the list of data files
missing_product_names = [name for name in product_names if name not in data_files]

# write the missing product names to a new CSV file
with open('missing_products.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Product Name'])
    for name in missing_product_names:
        writer.writerow([name])
