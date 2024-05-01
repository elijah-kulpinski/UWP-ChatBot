"""

This script reads a JSON file, extracts information, and writes it to a text file.
Each entry in the JSON file is formatted in the text file with the file path, body content, and a separator.

Usage:
- Replace 'json_file_path' with the path to your input JSON file.
- Replace 'output_txt_file_path' with the desired output text file path.
- Run the script to convert JSON data to a formatted text file.
"""

import json

# Replace 'your_file.json' with the actual path to your JSON file
json_file_path = '/Users/aaronantreassian/Documents/tmp/cleanedJson.json'

# Replace 'output.txt' with the desired path for your output text file
output_txt_file_path = '/Users/aaronantreassian/Documents/tmp/cleanedData.txt'

# Read the JSON file
with open(json_file_path, 'r') as json_file:
    # Load the JSON data into a Python object
    data = json.load(json_file)

# Create or open a text file for writing
with open(output_txt_file_path, 'w') as txt_file:
    # Iterate through each object in the JSON file
    for entry in data:
        # Write the file path to the text file
        txt_file.write(f"File: {entry['file']}\n\n")

        # Write the body content to the text file
        txt_file.write("Body Content:\n")
        for paragraph in entry['body_content']:
            # Write each paragraph to the text file
            txt_file.write(paragraph + "\n")

        # Add a separator between entries
        txt_file.write("\n" + "="*30 + "\n")
