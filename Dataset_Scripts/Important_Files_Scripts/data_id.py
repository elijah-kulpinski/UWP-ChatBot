"""
Author: Aaron Antreassian
Date: 04/28/2024

This script generates unique codes for each prompt-response pair in a JSON dataset using SHA-256 hashing.
The unique code is derived from hashing the concatenation of the prompt and response texts and taking the
first 5 characters of the hash. This code can serve as an identifier for each pair, which is useful for 
tracking and referencing them in a larger dataset.

Steps performed:
1. Load a dataset from a JSON file.
2. For each prompt-response pair, concatenate the texts, hash the concatenated string, and generate a unique code.
3. Add the unique code to the corresponding dictionary in the dataset.
4. Save the updated dataset back to the JSON file with the unique codes included.

Libraries used:
- json: For loading and saving JSON-formatted data.
- hashlib: For creating hash digests of strings, which are used here to generate unique identifiers.
"""

import json
import hashlib

def generate_code(prompt, response):
    # Concatenate prompt and response
    text = prompt + response
    # Hash the concatenated text using SHA-256
    hashed_text = hashlib.sha256(text.encode()).hexdigest()
    # Take the first 5 characters of the hashed text as the code
    code = hashed_text[:5]
    return code

# Load JSON data from file
with open('path_to_input.json', 'r') as file:  # Replace 'path_to_input.json' with the actual file path
    data = json.load(file)

# Generate unique codes for each prompt-response pair and add them to the JSON data
for pair in data:
    prompt = pair['prompt']
    response = pair['response']
    code = generate_code(prompt, response)
    pair['code'] = code

# Write the updated JSON data back to the file
with open('path_to_output.json', 'w') as file:  # Replace 'path_to_output.json' with the desired output file path
    json.dump(data, file, indent=4)

print("Codes added to JSON file successfully.")
