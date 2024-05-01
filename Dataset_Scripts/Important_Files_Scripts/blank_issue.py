"""
Author: Aaron Antreassian
Date: 04/28/2024

This script is designed to enhance data quality within a JSON dataset by ensuring that all entries contain 
valid text in the 'question' field. This is crucial in contexts where the data is used for training machine learning 
models, particularly for our chatbot, where the presence of meaningful input data directly influences model performance.

The script performs the following operations:
1. Loads data from a specified JSON file, which is expected to contain a list of entries with a 'question' key.
2. Filters the data to exclude any entries where the 'question' field is empty or contains only whitespace.
3. Writes the cleaned data back to the same JSON file, ensuring that only entries with valid questions are retained.
4. Outputs a confirmation message indicating the completion of the cleaning process and the file to which clean data has been saved.

"""

import json

def clean_questions(json_file_path):
    # Read the JSON data from the provided file path
    with open(json_file_path, "r") as file:
        data = json.load(file)
    
    # Filter out entries with no text in the 'question' field
    cleaned_data = [entry for entry in data if entry.get('question', '').strip()]
    
    # Write the cleaned data back to the same file, preserving other data structures and formatting
    with open(json_file_path, "w") as file:
        json.dump(cleaned_data, file, indent=4)
    
    # Notify user of completion and file path to the cleaned data
    print(f"Cleaned data has been saved back to {json_file_path}.")

# Specify the path to the JSON file to clean. Replace 'augmented_data.json' with the actual file path if different.
json_file_path = 'augmented_data.json'
clean_questions(json_file_path)
