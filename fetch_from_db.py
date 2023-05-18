import mysql.connector
import csv

# Connect to the database
cnx = mysql.connector.connect(user='root', password='Taza@1234', host='localhost', database='Tazah_Main')

# Create a cursor object
cursor = cnx.cursor()

# Execute a SELECT statement to fetch all data from a table
query = "SELECT * FROM products;"
cursor.execute(query)

# Fetch all rows and store them in a list
rows = cursor.fetchall()

# Close the cursor and database connection
cursor.close()
cnx.close()

# Write the data to a CSV file
with open('Bugged_filter_data.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)

    # Write the header row
    header = [i[0] for i in cursor.description]
    writer.writerow(header)

    # Write the data rows
    for row in rows:
        writer.writerow(row)
