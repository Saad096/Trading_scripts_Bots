import csv

# Input file paths
main_file_path = 'main.csv' # Replace with the path to your main CSV file
output_file_path = 'output.csv' # Replace with the path to your output CSV file

# Read main CSV file and store CityName, State, and CountryName entries in a dictionary
city_data = {}
with open(main_file_path, 'r', newline='') as main_file:
    reader = csv.DictReader(main_file)
    for row in reader:
        city_name = row['CityName']
        state = row['State']
        country_name = row['CountryName']
        key = f"{city_name},{state},{country_name}"
        city_data[key] = row

# Read output CSV file and update State in main CSV file if a match is found
with open(output_file_path, 'r', newline='') as output_file:
    reader = csv.DictReader(output_file)
    for row in reader:
        city_name = row['CityName']
        state = row['State']
        country_name = row['CountryName']
        key = f"{city_name},{state},{country_name}"
        if key in city_data:
            city_data[key]['State'] = row['State']

# Write updated data to a new CSV file
output_file_path = 'main_updated.csv' # Replace with the desired path for the updated main CSV file
with open(output_file_path, 'w', newline='') as output_file:
    fieldnames = city_data[next(iter(city_data))].keys()
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(city_data.values())

print("State values updated in the main file. Updated data written to main_updated.csv file.")
