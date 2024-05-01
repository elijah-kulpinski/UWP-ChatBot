from openai import OpenAI
import json

client = OpenAI(
    api_key="openai-api-key-here", # Add API key here
)

# Load paragraphs about the school from a JSON file
with open('instruction_dataset_snip.json', 'r') as file:
    paragraphs = json.load(file)

def classify_paragraph_gpt(paragraph_text):
    instruction = "Classify this paragraph into one and only one of the following categories based on the content of the paragraph and where you may find this information on a University website: Campus Life, Academics, Admissions and Aid, Athletics and Art, or About Us. You must use one of the categories I mentioned. Here's the paragraph:\n\n" + paragraph_text
    try:
        category_choice = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": instruction}]
        )
        return category_choice.choices[0].message.content.strip()
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Error"

# Generate synthetic prompt-response pairs and classify paragraphs
generated_pairs = []

print("Processing paragraphs...")
for paragraph in paragraphs:
    paragraph_text = paragraph['response']  # Assuming each entry in the JSON file has a 'response' key
    
    # Classify the paragraph
    # category = classify_paragraph_gpt(paragraph_text)

    instruction = f"Based on the following information, generate a user-like question and an appropriate answer:\n\n{paragraph_text[:500]}..." if len(paragraph_text) > 500 else f"Based on the following information, generate a user-like question and generate an appropriate answer:\n\n{paragraph_text}"

    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": instruction}],
        model="gpt-3.5-turbo",
    )

    generated_pair = chat_completion.choices[0].message.content.strip()

    # Assuming the format "Question: [question text] Answer: [answer text]"
    if "Question:" in generated_pair and "Answer:" in generated_pair:
        parts = generated_pair.split("Answer:")
        question = parts[0].replace("Question:", "").strip()
        answer = parts[1].strip()
    else:
        question = "Could not extract question"
        answer = "Could not extract answer"
    
    paragraph_category = classify_paragraph_gpt(paragraph_text)
    question_category = classify_paragraph_gpt(question)
    category = paragraph_category + " | " + question_category

    print(f"Generated question based on paragraph: {paragraph_text[:50]}... | Category: {category}")
    generated_pairs.append({"question": question, "answer": answer, "category": category})

# Save generated pairs and their categories to a new file
with open('generated_pairs_with_categories.json', 'w') as output_file:
    json.dump(generated_pairs, output_file, indent=2)

print("Generated prompt-response qa pairs with categories saved to generated_pairs_with_categories.json")

