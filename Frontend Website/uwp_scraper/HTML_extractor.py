"""
This script defines functions to extract plain text content from HTML and CFM files.
It reads files from a specified directory, extracts the text, and saves it in JSON files.

Usage:
- Replace 'files_directory' with the path to the directory containing HTML and CFM files.
- Replace 'output_directory' with the desired directory for the output JSON files.
- Run the script to extract text from HTML and CFM files.
"""

# Import necessary libraries
import os
from bs4 import BeautifulSoup
import json

# Function to extract plain text from HTML or CFM files
def extract_body_from_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Determine file type based on extension
            if file_path.endswith('.html'):
                # Use BeautifulSoup to parse HTML
                soup = BeautifulSoup(file, 'html.parser')
            elif file_path.endswith('.cfm'):
                # Assuming ColdFusion files have similar structure to HTML, was necesarry for uwp website
                soup = BeautifulSoup(file, 'html.parser')
            else:
                # Unsupported file type
                return None

            # Extract plain text without HTML tags
            body_text = soup.text
            return body_text
    except Exception as e:
        # Log the error instead of just returning a message
        print(f"Error processing {file_path}: {e}")
        return None

# Function to save content to a JSON file
def save_to_json(content, output_file_path):
    try:
        # Split content into lines with 10 words per line
        lines = [' '.join(content.split()[i:i+10]) for i in range(0, len(content.split()), 10)]

        data = {
            "body_content": lines
        }
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            # Dump the data to a JSON file with indentation
            json.dump(data, output_file, ensure_ascii=False, indent=4)
        return None
    except Exception as e:
        return f"Error saving to {output_file_path}: {e}"

# Directory containing HTML and CFM files
files_directory = "/Users/aaronantreassian/uwp_web_clone/www.uwp.edu"

# Output directory for JSON files
output_directory = "/Users/aaronantreassian/Documents/tmp/Text_Extracted"

# Ensure the output directory exists, create it if necessary
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Iterate through files in the specified directory and its subdirectories
for root, dirnames, filenames in os.walk(files_directory):
    for filename in filenames:
        file_path = os.path.join(root, filename)
        
        # Extract the body content from the file
        extracted_body = extract_body_from_file(file_path)
        
        # If content is successfully extracted, save it to a JSON file
        if extracted_body:
            # Include the relative path in the JSON filename
            relative_path = os.path.relpath(file_path, files_directory)
            output_file_path = os.path.join(output_directory, f"{relative_path.replace(os.path.sep, '_')}.json")
            
            # Save the extracted content to the JSON file
            save_to_json(extracted_body, output_file_path)
            
            # Print the processed filename
            print('Filename: {}'.format(file_path))
