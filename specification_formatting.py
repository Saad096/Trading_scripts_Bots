import pandas as pd
import re

# Read the CSV file
data = pd.read_csv("Final_Specification_for_PB - issue Specs.csv")
# List of attributes for Short specs
short_attributes = ["Size", "Shape", "Skin Color", "Flesh Color", "Texture", "Weight"]

# List of attributes for Long specs (extracted from the provided example)
long_attributes = [
    "Size", "Shape", "Skin Color", "Flesh Color", "Texture", "Weight", "Scientific name",
    "Origin", "TSS value", "Acidity", "Taste", "Seed", "Ripening Season", "Nutritional Value", "Shelf life"
]

# Function to format the attributes correctly
def format_attributes(specs, attributes):
    formatted_specs = specs
    for attr in attributes:
        # Find the attribute in the string
        index = formatted_specs.lower().find(attr.lower())
        if index == -1:
            continue

        # Insert a colon if it's missing after the attribute
        if index + len(attr) >= len(formatted_specs) or formatted_specs[index + len(attr)] != ':':
            formatted_specs = formatted_specs[:index + len(attr)] + ':' + formatted_specs[index + len(attr):]

        # Insert a comma if it's missing before the attribute (and it's not the first attribute)
        if index > 0 and formatted_specs[index - 1] != ' ' and formatted_specs[index - 1] != ',':
            formatted_specs = formatted_specs[:index] + ',' + formatted_specs[index:]

    return formatted_specs

# Format the attributes for each row in the 'Short specs' and 'Long specs' columns
data['Short specs'] = data['Short specs'].apply(lambda x: format_attributes(x, short_attributes))
data['Long Specs'] = data['Long Specs'].apply(lambda x: format_attributes(x, long_attributes))

# Save the formatted data to a new CSV file
data.to_csv("formatted_csv_file.csv", index=False)