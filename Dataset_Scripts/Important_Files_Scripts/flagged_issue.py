"""
Author: Aaron Antreassian
Date: 04/28/2024

This script will remove the flagged entries from a JSON file and assumes you have already done manual review on the flagged entries
to ensure they are all duplicates.

The operations performed by the script are as follows:
1. Loads data from a specified JSON file, which is expected to contain multiple entries, each potentially flagged for removal.
2. Filters out any entries where the 'Flagged' key is set to True, keeping only those entries that are unflagged.
3. Writes the cleaned data back to the file, overwriting the old data. This step ensures that all changes 
   are immediately reflected in the dataset, preserving storage space and simplifying data management.
4. Provides a straightforward and automated way to clean datasets, which is essential for users managing large datasets 
   or datasets that frequently require updating and cleaning.

Libraries used:
- json: For loading and writing JSON-formatted data.
"""

import json

def remove_flagged_items(input_filename):
    # Load the JSON data from the file
    with open(input_filename, 'r') as file:
        data = json.load(file)

    # Filter out items that are flagged
    unflagged_items = [item for item in data if not item.get("Flagged", False)]

    # Save the modified data back to the original file
    with open(input_filename, 'w') as file:
        json.dump(unflagged_items, file, indent=4)

# Example usage
remove_flagged_items('hopefully_final.json')
