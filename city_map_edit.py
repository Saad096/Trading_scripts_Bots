import csv
import requests

def get_state_name(city_name, username):
    url = f'http://api.geonames.org/searchJSON?name={city_name}&maxRows=1&username={username}'
    response = requests.get(url)
    data = response.json()

    if 'geonames' in data and len(data['geonames']) > 0:
        return data['geonames'][0]['adminName1']
    else:
        return None

# Input and output file paths
input_file_path = 'city_map_generated.csv' # Replace with the path to your output CSV file
output_file_path = 'city_map_edit.csv' # Replace with the desired path for the modified output CSV file

# Geonames username
username = 'bazil786' # Replace with your Geonames username

# Read output CSV file and modify State column
with open(input_file_path, 'r', newline='') as input_file, open(output_file_path, 'w', newline='') as output_file:
    reader = csv.DictReader(input_file)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        city_name = row['CityName']
        state = row['State']
        country_name = row['CountryName']
        if city_name and state and country_name:
            new_state = get_state_name(city_name, username)
            if new_state:
                row['State'] = new_state
        writer.writerow(row)

print("Modified output written to output_modified.csv file.")
