"""
This is a great script for removing the meta data from the extracted file text. 
This script will take a json file as input, parse the file, and remove the non readable text.
There may be some issues with new lines or other languages.
"""

# Import the json module for working with JSON data
import json

# Define a function to remove Unicode characters and newline symbols from a nested structure (dict, list, string)
def remove_unicode_and_newline(data):
    # If the data is a dictionary, apply the function to each key-value pair
    if isinstance(data, dict):
        return {key: remove_unicode_and_newline(value) for key, value in data.items()}
    # If the data is a list, apply the function to each item in the list
    elif isinstance(data, list):
        return [remove_unicode_and_newline(item) for item in data]
    # If the data is a string, remove Unicode characters and newline symbols
    elif isinstance(data, str):
        # Remove Unicode characters by only including characters with ordinal values less than 128
        cleaned_str = ''.join(char for char in data if ord(char) < 128)
        
        # Remove newline symbols ('\n') from the string
        cleaned_str = cleaned_str.replace('\n', '')

        return cleaned_str
    # If the data is neither a dictionary, list, nor string, return it unchanged
    else:
        return data

# Define a function to read a JSON file, process its content using the removal function, and write the cleaned data to a new file
def process_and_write_to_file(input_file_path, output_file_path):
    # Open the input JSON file for reading
    with open(input_file_path, 'r', encoding='utf-8') as file:
        # Load the JSON data from the file
        json_data = json.load(file)

    # Apply the remove_unicode_and_newline function to the loaded JSON data
    cleaned_data = remove_unicode_and_newline(json_data)

    # Open the output file for writing
    with open(output_file_path, 'w', encoding='utf-8') as file:
        # Dump the cleaned data to the output file in JSON format
        json.dump(cleaned_data, file, ensure_ascii=False, indent=2)

# Check if the script is being run as the main module
if __name__ == "__main__":
    # Replace these paths with the actual paths to your input and output JSON files
    input_file_path = "/Users/aaronantreassian/Documents/tmp/cleanerOutput.json"
    output_file_path = "/Users/aaronantreassian/Documents/tmp/cleanedJson.json"

    # Call the processing function with the specified input and output file paths
    process_and_write_to_file(input_file_path, output_file_path)
