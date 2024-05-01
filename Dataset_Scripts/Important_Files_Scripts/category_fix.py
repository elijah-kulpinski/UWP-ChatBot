"""
Author: Aaron Antreassian
Date: 04/28/2024

This script is used for changing all of the rogue categories to the 5 specified ones we want.
The OpenAI API sometimes likes to give random categories that are not in the 5 we want so this script does a
pretty good job at getting them to the 5 we want.

The script operates by:
1. Loading a dataset from a specified input JSON file.
2. Iterating over each item in the dataset to modify the category names based on a predefined dictionary of replacements.
3. Counting the occurrences of each category post-modification to provide insights into data distribution.
4. Saving the modified dataset to a new JSON file.
5. Printing the counts of each category for verification and analysis.

Libraries used:
- json: For loading and writing JSON-formatted data.
- collections.Counter: For efficiently counting occurrences of categories.
"""

import json
from collections import Counter

def modify_and_count_phrases_categories(input_filename, output_filename):
    with open(input_filename, 'r') as file:
        data = json.load(file)

    paragraph_categories_count = Counter()
    question_categories_count = Counter()

    # Define mappings for category keywords and their replacements. Make sure to play around with these as the key words may not grab all of the rogue categories
    category_replacements = {
        "Athletics": "Arts and Athletics",
        "About Us": "About Us",
        "Campus Life": "Campus Life",
        "Admissions": "Admissions and Aid",
        "Academics": "Academics",
        "Art": "Arts and Athletics",
        "Language": "Arts and Athletics",
    }

    for item in data:
        categories = item["category"].split(" | ")
        
        # Replace the entire category based on presence of keywords
        new_categories = []
        for category in categories:
            replaced = False
            for keyword, replacement in category_replacements.items():
                if keyword in category:
                    new_categories.append(replacement)
                    replaced = True
                    break
            if not replaced:
                new_categories.append(category)  # Keep the original category if no keyword match
        
        # Update the category field with the new values
        item["category"] = " | ".join(new_categories)

        # Count the updated categories
        paragraph_categories_count.update([new_categories[0]])
        if len(new_categories) > 1:
            question_categories_count.update([new_categories[1]])
        else:
            question_categories_count.update([new_categories[0]])

    # Save the modified data to a new file
    with open(output_filename, 'w') as file:
        json.dump(data, file, indent=4)

    # Print the categories count for verification
    print("Paragraph Categories Count:", paragraph_categories_count)
    print("Question Categories Count:", question_categories_count)

# Example usage
modify_and_count_phrases_categories('real_final_dataset.json', 'maybe_final.json')
