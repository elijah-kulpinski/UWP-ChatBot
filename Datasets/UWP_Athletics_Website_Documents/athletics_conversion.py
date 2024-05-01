import json

def convert_json_format(input_filepath, output_filepath):
    # Load the original JSON data
    with open(input_filepath, 'r') as input_file:
        original_data = json.load(input_file)

    # Container for the converted data
    converted_data = []

    # Iterate over each website and page in the original data
    for website, pages in original_data['content'].items():
        for page, texts in pages.items():
            # Generate a synthetic prompt for each page
            prompt_base = f"Synthetic prompt for {page}"
            for text_entry in texts:
                # For each text entry, create a new structure with "prompt" and "response"
                converted_entry = {
                    "prompt": prompt_base,
                    "response": text_entry["text"]
                }
                converted_data.append(converted_entry)

    # Write the converted data to a new JSON file
    with open(output_filepath, 'w') as output_file:
        json.dump(converted_data, output_file, indent=2)

# Example usage
input_filepath = 'paragraphs-small.json'
output_filepath = 'athletics_paragraphs.json'
convert_json_format(input_filepath, output_filepath)
