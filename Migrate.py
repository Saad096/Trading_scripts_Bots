import pandas as pd
import mysql.connector
from difflib import SequenceMatcher

# Read the Excel file
file_path = 'CitiesList.xlsx'
sheet_name = 'Sheet2'
df = pd.read_excel(file_path, sheet_name=sheet_name, engine='openpyxl')
print ("Reading cities file")
# Connect to the source MySQL database
src_config = {
    'host':"Bazils-MacBook-Air.local",
    'user':"root",
    'password':"Tazah@1234",
    'database':"Tazah_Raw"
}
src_conn = mysql.connector.connect(**src_config)

# Fetch data from the source SQL table
sql_query = "SELECT CountryName, CityName, ProductName,variety,CurrencyUnit, Hscode, PriceDate, Price FROM products"
src_data = pd.read_sql(sql_query, src_conn)
print ("Src DB Loaded and connected")

# Connect to the destination MySQL database
dst_config = {
    'user': 'root',
    'password': 'Tazah@1234',
    'host': 'Bazils-MacBook-Air.local',
    'database': 'Tazah_main'
}
dst_conn = mysql.connector.connect(**dst_config)
print ("Dest DB Loaded and connected")
# Create a table in the destination database
# create_table_query = """CREATE TABLE your_destination_table_name (
#                             city_id INT PRIMARY KEY,
#                             city_name VARCHAR(255),
#                             country_name VARCHAR(255)
#                         )"""
cursor = dst_conn.cursor()
# cursor.execute(create_table_query)
# dst_conn.commit()

# Calculate the similarity index and update city names
def similarity(a, b):
    return SequenceMatcher(None, a, b).ratio()

threshold = 0.8

updated_data = src_data.copy()

for index, row in df.iterrows():
    excel_city = row['Cities']
    excel_country = row['Country']
    for db_index, db_row in src_data.iterrows():
        db_city = db_row['CityName']
        db_country = db_row['CountryName']

        if excel_country == db_country:
            sim_index = similarity(excel_city, db_city)
            if sim_index > threshold:
                # Update the city name in the updated_data DataFrame
                updated_data.loc[db_index, 'CityName'] = excel_city

print ("Temp Data uploaded")

# Insert the updated data into the destination database
for index, row in updated_data.iterrows():
    insert_query = f"INSERT INTO products (CountryName,State,CityName,Hscode,category,ProductName,CurrencyUnit,PriceDate, AveragePrice, MaxPrice,MinPrice) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (row['CountryName'], row['CityName'], row['CityName'],row['Hscode'],row['variety'],row['ProductName'],row['CurrencyUnit'],row['PriceDate'],row['Price'],row['Price'],row['Price']))
    dst_conn.commit()
    

print("DB updated")

# Close the database connections
cursor.close()
src_conn.close()
dst_conn.close()
