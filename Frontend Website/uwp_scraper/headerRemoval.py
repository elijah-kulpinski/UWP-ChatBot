"""
This script defines a function to read a JSON file, remove lines containing a specific phrase, and update the JSON file.
The example usage demonstrates how to remove lines with a specified phrase from a cleaned JSON file.

Usage:
- Replace 'json_file_path' with the path to your cleaned JSON file.
- Replace 'phrase_to_remove' with the desired phrase to remove.
- Run the script to remove lines with the specified phrase.
"""

# Import the json module for working with JSON data
import json

# Define a function to remove lines containing a specific phrase from a JSON file
def remove_lines_with_phrase(json_file_path, phrase):
    # Open the JSON file for reading
    with open(json_file_path, 'r') as file:
        # Load the JSON data from the file
        data = json.load(file)

    # Calculate the total number of lines before the removal operation
    total_lines_before = sum(len(entry.get("body_content", [])) for entry in data)

    # Iterate through each entry in the data and remove lines containing the specified phrase
    for entry in data:
        if "body_content" in entry:
            entry["body_content"] = [line for line in entry["body_content"] if phrase not in line]

    # Calculate the total number of lines after the removal operation
    total_lines_after = sum(len(entry.get("body_content", [])) for entry in data)

    # Open the same JSON file for writing
    with open(json_file_path, 'w') as file:
        # Dump the modified data back to the JSON file with an indentation of 2 spaces
        json.dump(data, file, indent=2)

    # Print the total number of lines before and after the removal operation
    print(f'Total lines before: {total_lines_before}')
    print(f'Total lines after: {total_lines_after}')

# Example usage
# Specify the path to the JSON file and the phrase to be removed
json_file_path = '/Users/aaronantreassian/Documents/tmp/cleanedJson.json'
phrase_to_remove = 'Tour Guides Virtual'

# Call the function with the specified JSON file path and phrase
remove_lines_with_phrase(json_file_path, phrase_to_remove)
