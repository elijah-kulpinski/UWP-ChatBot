"""
Author: Aaron Antreassian
Date: 04/28/2024

This script is designed to selectively flag entries in a JSON dataset based on a specific question category. 
It's needed for dataset balancing which is an important part of the LLM finwetuning process.

Operations performed by the script:
1. Loads a dataset from a JSON file which contains entries, each with a 'category' key among others.
2. Filters these entries to find those matching a specified target question category.
3. Randomly flags a specified number of these filtered entries, marking them for special attention.
4. Saves the modified data back to the JSON file, ensuring that the changes are retained.

This process not only aids in data management but also ensures that specific data subsets receive the appropriate
attention needed for particular purposes.

Libraries used:
- json: For handling JSON-formatted data.
- random: For selecting a random subset of entries to flag.
"""

import json
import random

def flag_items_specific_question_category(input_filename, target_question_category, num_to_flag):
    with open(input_filename, 'r') as file:
        data = json.load(file)

    # Extract and filter items where the question category matches the target
    filtered_items = []
    for item in data:
        categories = item["category"].split(" | ")
        if len(categories) > 1 and categories[1].strip() == target_question_category:
            filtered_items.append(item)

    # Check if there are enough items to flag, if not, flag as many as possible
    num_to_flag = min(num_to_flag, len(filtered_items))

    # Randomly select items to flag
    items_to_flag = random.sample(filtered_items, num_to_flag) if num_to_flag > 0 else []

    # Set the "Flagged" field of these selected items to True
    for item in items_to_flag:
        item["Flagged"] = True

    # Save the modified data back to the original file
    with open(input_filename, 'w') as file:
        json.dump(data, file, indent=4)

# Example usage
flag_items_specific_question_category('hopefully_final.json', "Campus Life", 762)
