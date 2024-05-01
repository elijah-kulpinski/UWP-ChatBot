"""
Author: Aaron Antreassian
Date: 04/28/2024

This script is designed to augment your dataset of questions by generating multiple rephrased versions of each question
using OpenAI's API. This augmentation helps in expanding the dataset with diverse ways of asking the same question, which
can be beneficial for training models to understand and respond to varied phrasing in natural language processing tasks.

The script performs the following steps:
1. Initializes the OpenAI client with an API key.
2. Defines a function to generate rephrased questions from an original question using the API.
3. Loads a dataset of original questions from a JSON file.
4. Iterates through the dataset, generating rephrased questions for each and marking the original question as a parent entry.
5. Saves the augmented dataset with both original and rephrased questions to a new JSON file.

Key libraries used:
- openai: To interact with the OpenAI API for generating rephrased questions.
- json: For loading and saving data.
- typing: Provides support for type hints which enhance code readability and error-checking in IDEs.
"""

import json
from openai import OpenAI
from typing import List

# Initialize the OpenAI client with your API key
client = OpenAI(api_key="") # Add API Key here

def generate_rephrased_questions(original_question: str) -> List[str]:
    # Specify the number of rephrased questions to generate
    count = 4
    
    # Instruction for the API to rephrase the question
    instruction = f"Please rephrase the following question in {count} different ways, ensuring each version asks the same thing but with different wording:\n\n'{original_question}'"
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[{"role": "system", "content": instruction}],
            model="gpt-3.5-turbo",
        )

        # Process the API response to extract rephrased questions
        rephrased_questions_raw = chat_completion.choices[0].message.content.strip()

        # Splitting based on newline and removing the number and period from the start of each item
        rephrased_questions = [line.split('. ', 1)[1] if '. ' in line else line for line in rephrased_questions_raw.split('\n')]

        return rephrased_questions[:count]

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

# Load the JSON dataset
with open('hopefully_final.json', 'r') as file:
    data = json.load(file)

augmented_data = []  # List to hold all data including augmented items

# Process each item in the dataset
for item in data:
    print(f"Augmenting object with ID = {item['ID']}")

    # Mark the original question as a parent
    item["Parent"] = True
    augmented_data.append(item)

    # Generate rephrased questions (4 for each original question)
    rephrased_questions = generate_rephrased_questions(item["question"])

    # Create and append the rephrased (child) questions to the augmented data list
    for rephrased_question in rephrased_questions:
        child_question = {
            "ID": f"{item['ID']}-{rephrased_questions.index(rephrased_question) + 1}",
            "System Prompt": item["System Prompt"],
            "question": rephrased_question,
            "answer": item["answer"],
            "category": item["category"],
            "Flagged": False,
            "Is_Duplicate": False,
            "child_of": item["ID"],
            "Parent": None
        }
        augmented_data.append(child_question)

# Save all augmented data to a new JSON file in one operation
with open('augmented_data.json', 'w') as outfile:
    json.dump(augmented_data, outfile, indent=4)

print("Augmentation complete and saved to 'augmented_data.json'.")
