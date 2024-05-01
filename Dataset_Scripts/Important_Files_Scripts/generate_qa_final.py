
"""
Author: Aaron Antreassian
Date: 04/28/2024

This script automates the process of generating question-answer pairs from provided paragraphs,
classifying the content, and identifying similarities between generated questions to ensure uniqueness.
It leverages the OpenAI API for content classification and question generation, employs TF-IDF for text vectorization,
and uses cosine similarity to find similar text entries. This approach helps in creating a categorized dataset of 
QA pairs, which can be useful for training models or for providing structured educational content.

Libraries and tools used:
- openai: To interact with the OpenAI API for generating responses and classifying text.
- json: For loading and saving data.
- scikit-learn's TfidfVectorizer and cosine_similarity: For text vectorization and similarity comparison.
- transformers' AutoTokenizer: For advanced text tokenization not used in this script but included for potential future use.

The workflow includes:
1. Loading data from a JSON file.
2. Generating question-answer pairs using OpenAI's API.
3. Classifying paragraphs and questions into predefined categories.
4. Identifying similar questions to ensure no duplicates are in the dataset.
"""


# Import necessary libraries
from openai import OpenAI  # For interacting with OpenAI's API
import json  # For loading and saving data in JSON format
from sklearn.feature_extraction.text import TfidfVectorizer  # For converting text to TF-IDF vectors
from sklearn.metrics.pairwise import cosine_similarity  # For computing similarity between vectors
# from transformers import AutoTokenizer # For tokenizing text to ChatML format

# Initialize the OpenAI client with an API key for authentication
client = OpenAI(
    api_key="" # Add API key here
)

# Load paragraphs from a JSON file into the 'paragraphs' variable
with open('full_question_generation.json', 'r') as file:
    paragraphs = json.load(file)

# Initialize the TF-IDF Vectorizer for later use in transforming texts to feature vectors
vectorizer = TfidfVectorizer()

# Define a function to compute cosine similarity between two text inputs
def compute_cosine_similarity(text1, text2):
    # Vectorize the input texts and compute TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform([text1, text2])
    # Compute and return the cosine similarity between the two vectors
    return cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]

# Define a function to classify a given paragraph text into predefined categories using OpenAI's API
def classify_paragraph_gpt(paragraph_text):
    # Prepare the instruction for classification
    instruction = "Analyze and then classify this paragraph into one and only one of the following categories that best describes its content: \"Campus Life\", \"Academics\", \"Admissions and Aid\", \"Athletics and Art\", or \"About Us\". You must use one of the categories I mentioned and the category may not exceed more than 3 words. Here's the paragraph:'\n\n{paragraph_text[100:4000]}..." if len(paragraph_text) > 500 else f"Analyze and then classify this paragraph into one and only one of the following categories: Campus Life, Academics, Admissions and Aid, Athletics and Art, or About Us. You must use one of the categories I mentioned and the category may not exceed than 3 words. Here's the paragraph:'.\n\n{paragraph_text[150:4000]}"
    try:
        # Make an API call to classify the paragraph and return the classification result
        category_choice = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": instruction}]
        )
        return category_choice.choices[0].message.content.strip()
    except Exception as e:
        # Handle any errors during the API call and return an error message
        print(f"An error occurred: {e}")

def classify_question_gpt(question_text, paragraph_category):
    # Adjust the instruction to include the paragraph category for context
    instruction = (
        f"Given that the related paragraph falls under the \"{paragraph_category}\" category, "
        f"analyze and then classify this question into one and only one of the following categories "
        f"that best describes its content: \"Campus Life\", \"Academics\", \"Admissions and Aid\", "
        f"\"Athletics and Art\", or \"About Us\". You must use one of the categories I mentioned "
        f"and the category may not exceed more than 3 words. Here's the question:'.\n\n{question_text}"
    )

    try:
        # Make an API call to classify the question and return the classification result
        category_choice = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Consider using the most appropriate model version
            messages=[{"role": "system", "content": instruction}]
        )
        return category_choice.choices[0].message.content.strip()
    except Exception as e:
        # Handle any errors during the API call and return an error message
        print(f"An error occurred: {e}")


# Initialize variables for processing and storing data
generated_pairs = []

# Create a list to store the flagged prompts
flagged_prompts = []

paragraph_category_count = {}

question_category_count = {}

paragraph_counter = 1  # Initialize a counter for paragraphs

system_prompt = "You are an expert assistant helping a student with a question about your university."

#Duplicate variables to be used in the cosine similarity check
flagged = False

is_duplicate = False

print("Processing paragraphs...")
# Iterate through each paragraph to process it
for paragraph in paragraphs:
    paragraph_text = paragraph['response']
    
    # Generate a question-answer pair based on the paragraph text
    instruction = f"Please read the following information and generate a simple user-like question and an appropriate answer about the given information. Make sure the question closely relates to the content of the given informtation. Make sure to only include the question and the answer. The question should start with 'Question:' and the answer should start with 'Answer:'\n\n{paragraph_text[100:4000]}..." if len(paragraph_text) > 4000 else f"Please Analyze the following information and generate a simple user-like question and an appropriate answer about the given information. Try not to focus too much on financial aid questions unless the given information is about it. The question should start with 'Question:' and the answer should start with 'Answer:'\n\n{paragraph_text}" # paragraph length should start after 100 characters for uwp website content
    chat_completion = client.chat.completions.create(
        messages=[{"role": "system", "content": instruction}],
        model="gpt-3.5-turbo",
    )

    generated_pair = chat_completion.choices[0].message.content.strip()

    # Extract question and answer from the generated pair
    if "Question:" in generated_pair and "Answer:" in generated_pair:
        parts = generated_pair.split("Answer:")
        question = parts[0].replace("Question:", "").strip()
        answer = parts[1].strip()
    else:
        # Handle cases where extraction fails
        question = "Could not extract question"
        answer = "Could not extract answer"
    
    
    # Classify the paragraph and question into categories
    paragraph_category = classify_paragraph_gpt(paragraph_text)
    question_category = classify_question_gpt(question, paragraph_category)
    category = paragraph_category + " | " + question_category

    # Update category counts for paragraphs and questions
    if paragraph_category in paragraph_category_count:
        paragraph_category_count[paragraph_category] += 1
    else:
        paragraph_category_count[paragraph_category] = 1

    if question_category in question_category_count:
        question_category_count[question_category] += 1
    else:
        question_category_count[question_category] = 1

    # Print the generated question and its category
    print(f"Generated question based on paragraph: {paragraph_text[:50]}... | Category: {category}")
    
    
    # Store the generated pair with additional information
    generated_pairs.append({"ID": paragraph.pop('code'), "System Prompt": system_prompt, "question": question, "answer": answer, "category": category, "Flagged": flagged, "Is_Duplicate": is_duplicate })

    # with open('generated_dataset_final.json', 'w') as output_file:
    #     json.dump(generated_pairs, output_file, indent=2)

    # Increment the paragraph counter
    paragraph_counter += 1

# Vectorize all questions for similarity comparison
questions = [pair["question"] for pair in generated_pairs]
tfidf_matrix = vectorizer.fit_transform(questions)

# Calculate cosine similarity between all question pairs to find duplicates or similar questions
similarities = cosine_similarity(tfidf_matrix)
similarity_threshold = 0.9  # Threshold for considering questions as similar

# Iterate through similarities to identify and report similar questions
for i in range(len(similarities)):
    for j in range(i + 1, len(similarities)):  # Avoid repeating pairs and self-comparison
        if similarities[i, j] > similarity_threshold:
            # Report similar questions
            print(f"Questions {i + 1} and {j + 1} are very similar with a cosine similarity of {similarities[i, j]}.")

            # Update boolean values if similar questions are found
            generated_pairs[i]["Flagged"] = True
            generated_pairs[j]["Flagged"] = True
            generated_pairs[i]["Is_Duplicate"] = True
            generated_pairs[j]["Is_Duplicate"] = True

            # Get the information of the similar questions
            ID1 = generated_pairs[i]["ID"]
            question1 = generated_pairs[i]["question"]
            answer1 = generated_pairs[i]["answer"]
            category1 = generated_pairs[i]["category"]
            ID2 = generated_pairs[j]["ID"]
            paragraph1 = paragraphs[i]["response"] # Should be "response" section
            question2 = generated_pairs[j]["question"]
            answer2 = generated_pairs[j]["answer"]
            category2 = generated_pairs[j]["category"]
            paragraph2 = paragraphs[j]["response"] # Should be "response" section

            # Create a dictionary for the flagged prompts
            flagged_prompt = [
                {
                "ID1": ID1,
                "question1": question1,
                "answer1": answer1,
                "category1": category1,
                "paragraph1": paragraph1
                },
                {
                "ID2": ID2,
                "question2": question2,
                "answer2": answer2,
                "category2": category2,
                "paragraph2": paragraph2
                }
            ]

            # Add the flagged prompt to the list
            flagged_prompts.append(flagged_prompt)

        
# Save the flagged prompts to the 'flagged_prompts.json' file
with open('flagged_for_run_1.json', 'w') as output_file:
    json.dump(flagged_prompts, output_file, indent=2)

# Dump the generated pairs in the JSON file
with open('run1.json', 'w') as output_file:
    json.dump(generated_pairs, output_file, indent=2)

# Print final counts and summary
print("Paragraph Category count:", paragraph_category_count)
print("Question Category count:", question_category_count)
grand_total = sum(paragraph_category_count.values())
print("Grand Total Paragraph Count:", grand_total)
print("Generated prompt-response qa pairs with categories and cosine similarity saved to ")
