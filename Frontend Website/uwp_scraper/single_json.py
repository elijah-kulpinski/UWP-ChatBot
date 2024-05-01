"""
This script processes a directory containing JSON files, extracts 'body_content' field from each JSON file,
and writes the aggregated data to a single output JSON file.

Usage:
- Replace 'input_directory' with the path to the directory containing JSON files.
- Replace 'output_json_file' with the desired output JSON file path.
- Run the script to aggregate 'body_content' fields from JSON files into a single output file.
"""

import os
import json

def process_directory(input_dir, output_file):
    body_content_list = []

    # Iterate through files in the specified directory and its subdirectories
    for root, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)

                try:
                    # Read each JSON file and extract 'body_content' field
                    with open(file_path, 'r') as json_file:
                        data = json.load(json_file)
                        body_content = data.get("body_content", None)

                        if body_content:
                            body_content_list.append({"file": file_path, "body_content": body_content})
                        else:
                            print(f"No 'body_content' field found in file: {file_path}")

                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON in file {file_path}: {e}")

    # Write the aggregated data to the output JSON file
    with open(output_file, 'w') as output_json:
        json.dump(body_content_list, output_json, indent=2)

if __name__ == "__main__":
    # Specify the input directory and output JSON file path
    input_directory = "/path/to/your/input_directory"
    output_json_file = "output.json"

    # Process the directory and create the output JSON file
    process_directory(input_directory, output_json_file)
