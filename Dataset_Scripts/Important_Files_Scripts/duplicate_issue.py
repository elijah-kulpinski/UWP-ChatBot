"""
Author: Aaron Antreassian
Date: 04/28/2024

In case any of the JSON files being used get different field names.
Use this script to rename the field names and clean up the dataset by removing unnecessary fields.

The script operates as follows:
1. Loads a JSON dataset from a file, which contains a list of entries, each potentially marked as a duplicate.
2. Iterates over each entry in the dataset, checking for the presence of the "Is Duplicate" field.
3. If found and true, updates the entry with a new "Is_Duplicate" key and removes the old "Is Duplicate" key.
4. Saves the corrected dataset to a new file to preserve the original data for comparison or backup purposes.
5. Notifies the user upon successful completion of the operation.

This renaming and cleanup help in maintaining the integrity and usability of the dataset, particularly when the dataset 
is used by different systems or software that require specific data formatting.

Libraries used:
- json: For loading and saving JSON-formatted data.
"""

import json

# Load the JSON data from the file
with open('athletics_output.json', 'r') as file:
    data = json.load(file)

# Iterate through each object and modify "Is_Duplicate" as needed
for item in data:
    # Check if "Is Duplicate" field exists and is True
    if item.get("Is Duplicate") == True:
        item["Is_Duplicate"] = True
        del item["Is Duplicate"]  # Remove the "Is Duplicate" field

# Write the modified data back to a new JSON file (or the original, if preferred)
with open('athletics_output_revised.json', 'w') as file:
    json.dump(data, file, indent=4)

print("The JSON file has been successfully modified and saved.")
