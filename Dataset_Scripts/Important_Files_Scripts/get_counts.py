"""
Author: Aaron Antreassian
Date: 04/28/2024

This script is used to count the categories of the paragraphs and questions in the JSON dataset.
This was a super important script for this project and I used it quite frequently to make sure the data was balanced.

The script performs the following steps:
1. Loads data from a specified JSON file, which contains entries each with a 'category' field formatted as "Paragraph Category | Question Category".
2. Iterates through each entry to count occurrences of each category type separately using counters.
3. Calculates the total number of paragraph and question entries for summary statistics.
4. Prints the total counts and individual category counts for both paragraph and question types.

Libraries used:
- json: For loading JSON-formatted data.
- collections.Counter: For efficiently counting occurrences of each category.
"""

import json
from collections import Counter

# Load the JSON data from the file
with open('augmented_data.json', 'r') as file: # Change the file name to your json file
    data = json.load(file)

filtered_data = []
paragraph_categories_count = Counter()
question_categories_count = Counter()

# Filter objects and count categories for duplicates with separate counters
for item in data:
    paragraph_category, question_category = item["category"].split(" | ")
    
    paragraph_categories_count.update([paragraph_category])
    question_categories_count.update([question_category])

# Print the categories count for verification
# Sum the paragraph totals
paragraph_total = sum(paragraph_categories_count.values())

# Sum the question totals
question_total = sum(question_categories_count.values())

print("Paragraph Total:", paragraph_total)
print("Question Total:", question_total)
print("Paragraph Categories Count:", paragraph_categories_count)
print("Question Categories Count:", question_categories_count)