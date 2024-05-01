"""
Author: Aaron Antreassian
Date: 04/28/2024

This script filters a JSON dataset to remove entries marked as duplicates and counts the categories of duplicates 
for both paragraphs and questions. The aim is to maintain a clean dataset by removing entries identified as duplicates 
while analyzing the distribution of categories among these duplicates. This is useful for understanding 
the nature of duplicated content and ensuring data quality in scenarios like data analysis or machine learning where 
duplicate entries could skew results.

The script executes the following steps:
1. Loads a dataset from a specified JSON file.
2. Iterates through each entry to filter out duplicates and to count the categories of duplicates using separate counters.
3. Uses sets to track unique IDs that have already been counted to avoid recounting the same entry.
4. Saves the filtered dataset (without duplicates) to a new JSON file.
5. Outputs the counts of each category for verification and analysis.

Libraries used:
- json: For loading and saving JSON-formatted data.
- collections.Counter: For efficiently counting occurrences of categories.
"""

import json
from collections import Counter

# Load the JSON data from the file
with open('athletics_output_revised.json', 'r') as file:  # Change the file name to your JSON file
    data = json.load(file)

filtered_data = []
paragraph_categories_count = Counter()
question_categories_count = Counter()
unique_ids_counted_for_paragraph = set()  # To ensure each unique ID is counted once for paragraph
unique_ids_counted_for_question = set()  # To ensure each unique ID is counted once for question

# Filter objects and count categories for duplicates with separate counters
for item in data:
    if not item.get("Is_Duplicate"):
        filtered_data.append(item)
    else:
        paragraph_category, question_category = item["category"].split(" | ")
        # Check and update paragraph category count if ID hasn't been counted yet
        if item["ID"] not in unique_ids_counted_for_paragraph:
            paragraph_categories_count.update([paragraph_category])
            unique_ids_counted_for_paragraph.add(item["ID"])
        # Check and update question category count if ID hasn't been counted yet
        if item["ID"] not in unique_ids_counted_for_question:
            question_categories_count.update([question_category])
            unique_ids_counted_for_question.add(item["ID"])

# Write the filtered data to a new JSON file
with open('athletics_output_final.json', 'w') as file:  # Change to your desired destination file name
    json.dump(filtered_data, file, indent=4)

# Print the categories count for verification
print("Paragraph Categories Count:", paragraph_categories_count)
print("Question Categories Count:", question_categories_count)
