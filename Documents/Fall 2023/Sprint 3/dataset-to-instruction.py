import json

# Read body content and file URLs from your dataset
with open('website-body-contents.json', 'r') as file:
    data = json.load(file)

prompt_response_pairs = []

# Iterate through each data entry
for entry in data:
    body_content = entry.get("body_content", [])
    file_url = entry.get("file", "")
    
    # Concatenate all paragraphs into a single response
    response = "\n".join(body_content)
    
    # Create a single prompt for the entire entry
    prompt = f"Synthetic prompt for {file_url}"
    prompt_response_pairs.append({"prompt": prompt, "response": response})

# Save the result to instruction_dataset.json
with open('instruction_dataset.json', 'w') as output_file:
    json.dump(prompt_response_pairs, output_file, indent=2)

print("instruction_dataset.json generated.")
