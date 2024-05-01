"""
Author: Aaron Antreassian
Date: 04/28/24

This script is used for splitting the data into a training set and a validation set. 
The validation set is 20% of the original data and is randomly selected from each category. 
The training set is the remaining 80% of the data. The validation set is written to a new JSON file, 
and the original data is overwritten with the training set.
We want to do this for the LLM training as it is important to have a validation and training set to test the model on.
These new datasets are then put into their own Huggingface dataset repos for easy use in the LLM training script.

Note: this script was only used on the second dataset we created so their will only be a training and validation set for the second dataset.

"""

import json
import random

def split_data(original_file, new_file):
    with open(original_file, 'r') as file:
        data = json.load(file)

    new_data = []
    reduced_data = []

    # Create a dictionary to hold entries by category
    category_dict = {}
    for entry in data:
        category = entry['category']
        if category not in category_dict:
            category_dict[category] = []
        category_dict[category].append(entry)

    # Randomly select 20% from each category
    for category, entries in category_dict.items():
        total_items = len(entries)
        indices = list(range(total_items))
        random.shuffle(indices)

        split_index = int(0.2 * total_items)
        new_indices = indices[:split_index]
        remaining_indices = indices[split_index:]

        # Append the selected new data entries and the entries to keep
        new_data.extend(entries[i] for i in new_indices)
        reduced_data.extend(entries[i] for i in remaining_indices)

    # Write the new_data to the new JSON file
    with open(new_file, 'w') as file:
        json.dump(new_data, file, indent=4)

    # Overwrite the original file with the reduced data
    with open(original_file, 'w') as file:
        json.dump(reduced_data, file, indent=4)

# Usage
original_file = 'run1_fix.json'
new_file = 'validate_1.json'
split_data(original_file, new_file)
