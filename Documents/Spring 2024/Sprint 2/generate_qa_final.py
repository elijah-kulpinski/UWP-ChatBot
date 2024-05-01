# Import necessary libraries
from openai import OpenAI  # For interacting with OpenAI's API
import json  # For loading and saving data in JSON format
from sklearn.feature_extraction.text import TfidfVectorizer  # For converting text to TF-IDF vectors
from sklearn.metrics.pairwise import cosine_similarity  # For computing similarity between vectors
from transformers import AutoTokenizer # For tokenizing text to ChatML format


# Initialize the OpenAI client with an API key for authentication
client = OpenAI(
    api_key="openai-api-key-here" # Add your API key here
)

# Load paragraphs from a JSON file into the 'paragraphs' variable
with open('instruction_dataset.json', 'r') as file:
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
    instruction = "Analyze and then classify this paragraph into one and only one of the following categories: Campus Life, Academics, Admissions and Aid, Athletics and Art, or About Us. You must use one of the categories I mentioned and the category may not exceed more than 3 words. Here's the paragraph:\n\n + paragraph_text{paragraph_text[:500]}..." if len(paragraph_text) > 500 else f"Analyze and then classify this paragraph into one and only one of the following categories: Campus Life, Academics, Admissions and Aid, Athletics and Art, or About Us. You must use one of the categories I mentioned and the category may not exceed than 3 words. Here's the paragraph:'.\n\n{paragraph_text}"
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

# Initialize variables for processing and storing data
generated_pairs = []
paragraph_category_count = {}
question_category_count = {}
paragraph_counter = 1  # Initialize a counter for paragraphs
system_prompt = "You are an expert assistant helping a student with a question about your university."

print("Processing paragraphs...")
# Iterate through each paragraph to process it
for paragraph in paragraphs:
    paragraph_text = paragraph['response']
    
    # Generate a question-answer pair based on the paragraph text
    instruction = f"Please read the following information and generate a simple user-like question and an appropriate answer about the given information. The question should start with 'Question:' and the answer should start with 'Answer:'\n\n{paragraph_text[100:2000]}..." if len(paragraph_text) > 2000 else f"Please Analyze the following information and generate a simple user-like question and an appropriate answer about the given information. Try not to focus too much on financial aid questions unless the given information is about it. The question should start with 'Question:' and the answer should start with 'Answer:'\n\n{paragraph_text[100:]}"
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
    question_category = classify_paragraph_gpt(question)
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
    generated_pairs.append({"Number": paragraph_counter, "System Prompt": system_prompt, "question": question, "answer": answer, "category": category})

    with open('generated_dataset.json', 'w') as output_file:
        json.dump(generated_pairs, output_file, indent=2)

    # Increment the paragraph counter
    paragraph_counter += 1

# Vectorize all questions for similarity comparison
questions = [pair["question"] for pair in generated_pairs]
tfidf_matrix = vectorizer.fit_transform(questions)

# Calculate cosine similarity between all question pairs to find duplicates or similar questions
similarities = cosine_similarity(tfidf_matrix)
similarity_threshold = 0.6  # Threshold for considering questions as similar

# Iterate through similarities to identify and report similar questions
for i in range(len(similarities)):
    for j in range(i + 1, len(similarities)):  # Avoid repeating pairs and self-comparison
        if similarities[i, j] > similarity_threshold:
            # Report similar questions
            print(f"Questions {i + 1} and {j + 1} are very similar with a cosine similarity of {similarities[i, j]}.")

# Print final counts and summary
print("Paragraph Category count:", paragraph_category_count)
print("Question Category count:", question_category_count)
grand_total = sum(paragraph_category_count.values())
print("Grand Total Paragraph Count:", grand_total)
print("Generated prompt-response qa pairs with categories and cosine similarity saved to generated_pairs_with_cosine_similarity_test.json")
