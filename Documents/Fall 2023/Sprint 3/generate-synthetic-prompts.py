from openai import OpenAI
import json

client = OpenAI(
    api_key="openai-api-key-here",
)

# Load paragraphs about the school from a JSON file
with open('instruction_dataset_snip.json', 'r') as file:
    paragraphs = json.load(file)

# Generate synthetic prompt-response pairs using ChatGPT 3.5
generated_pairs = []

print("Processing paragraphs...")
for paragraph in paragraphs:
    # Check if paragraph is a string or dictionary and access the text content
    paragraph_text = paragraph['response']  # Assuming each entry in the JSON file has a 'response' key

    # Instruct GPT-3.5 to generate a user-like query and a response based on the paragraph
    instruction = f"Based on the following information, generate a user-like query and an appropriate response:\n\n{paragraph_text[:500]}..." if len(paragraph_text) > 500 else f"Based on the following information, generate a user-like query and an appropriate response:\n\n{paragraph_text}"

    # Use ChatGPT to generate the prompt-response pair
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": instruction}],
        model="gpt-3.5-turbo",
    )

    # Extract the model-generated prompt-response pair
    generated_pair = chat_completion.choices[0].message.content

    print(f"Generated pair based on paragraph: {paragraph_text[:50]}...")
    generated_pairs.append(generated_pair)

# Save generated pairs to a new file
with open('generated_pairs.json', 'w') as output_file:
    json.dump(generated_pairs, output_file, indent=2)

print("Generated prompt-response pairs saved to generated_pairs.json")