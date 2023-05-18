import mysql.connector
import csv

# Connect to the database
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword",
  database="Tazah_main"
)

# Fetch all data from the products table
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM products")
result = mycursor.fetchall()

# Write the data to a CSV file
with open('products.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # Write header row
    writer.writerow([i[0] for i in mycursor.description])
    # Write data rows
    writer.writerows(result)

# Close the database connection
mycursor.close()
mydb.close()
