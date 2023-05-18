import csv

# Input and output file paths
input_file_path = 'scraped_db_data.csv' # Replace with the path to your input CSV file
output_file_path = 'city_map_generated.csv' # Replace with the desired path for the output CSV file

# Set to keep track of unique combinations of CityName, State, and CountryName
unique_combinations = set()

# Read input CSV file and write unique combinations to output CSV file
with open(input_file_path, 'r', newline='', errors="ignore") as input_file, open(output_file_path, 'w', newline='') as output_file:
    reader = csv.DictReader(input_file)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    for row in reader:
        city_name = row['CityName']
        state = row['State']
        country_name = row['CountryName']
        combination = f"{city_name},{state},{country_name}"
        if combination not in unique_combinations:
            writer.writerow(row)
            unique_combinations.add(combination)

print("Unique combinations written to output CSV file.")
