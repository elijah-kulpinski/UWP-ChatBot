import asyncio
import json
import os
import random
import time
from openai import OpenAI, AsyncOpenAI

global start_time
global end_time

# Your API key
api_key = "openai-api-key-here"

# Function to append data to a file
def append_to_file(file_path, data):
    with open(file_path, 'a') as file:
        json.dump(data, file)
        file.write('\\n')

# Exponential backoff in case of rate limit error
def backoff_hdlr(attempt, delay):
    # Add random jitter to the delay
    jitter = random.uniform(0, attempt)
    new_delay = min(delay * 2, 60) + jitter  # Cap the delay at 60 seconds
    print(f"Rate limit hit, backing off for {new_delay} seconds for attempt {attempt}. ")
    time.sleep(new_delay)

# Sync wrapper to handle the OpenAI API call with retry logic
def make_api_call_sync(client, *args, **kwargs):
    max_retries = 5
    attempt = 0
    delay = 1  # Start with a 1 second delay

    while attempt < max_retries:
        try:
            return client.chat_completions.create(*args, **kwargs)
        except Exception as e:
            error_message = str(e).lower()
            if 'rate limit' in error_message:
                attempt += 1
                backoff_hdlr(attempt, delay)
            else:
                print(f"An unexpected error occurred: {e}. ")
                raise e

# Async wrapper to handle the OpenAI API call with retry logic
async def make_api_call_async(client, *args, **kwargs):
    max_retries = 5
    attempt = 0
    delay = 1  # Start with a 1 second delay

    while attempt < max_retries:
        try:
            return await client.chat.completions.create(*args, **kwargs)
        except Exception as e:
            error_message = str(e).lower()
            if 'rate limit' in error_message:
                attempt += 1
                backoff_hdlr(attempt, delay)
            else:
                print(f"An unexpected error occurred: {e}. ")
                raise e

# Function to process the generated response and format it
def process_and_format_response(file_name, generated_text):
    # Split the text into User Query and Response (assuming this structure is consistent)
    parts = generated_text.split("\n\n")
    if len(parts) >= 2:
        return {
            "User Query": parts[0].strip(),
            "Response": parts[1].strip()
        }
    else:
        return {
            "User Query": "Query not generated for {file_name}. ",
            "Response": "Response not generated for {file_name}. "
        }

# Synchronous version
def process_paragraphs_sync(paragraphs, output_file_path):
    sync_client = OpenAI(api_key=api_key)

    for index, paragraph in enumerate(paragraphs):
        start_time = time.perf_counter()
        paragraph_text = paragraph.get('response', '')
        file_name = os.path.basename(paragraph.get('prompt', ''))
        print(f"Processing paragraph {index + 1}/{len(paragraphs)}: {file_name}")

        # Constructing the instruction
        instruction = (
            f"Based on the following information, generate a user-like query and an appropriate response:\n\n{paragraph_text[:500]}..."
            if len(paragraph_text) > 500
            else f"Based on the following information, generate a user-like query and an appropriate response:\n\n{paragraph_text}"
        )

        print(f"Making API Call. ")

        response = make_api_call_sync(
            sync_client,
            messages=[{"role": "system", "content": instruction}],
            model="gpt-3.5-turbo",
        )

        print(f"Recieved API Contents. ")

        try:
            # Process the generated text and format the result
            if response.choices:
                formatted_result = process_and_format_response(file_name, response.choices[0].message.content)
            else:
                formatted_result = process_and_format_response("")

            # Append the formatted result to the file
            append_to_file(output_file_path, formatted_result)
            end_time = time.perf_counter()
            print(f"Finished paragraph {index + 1}/{len(paragraphs)} in {(end_time-start_time):0.1f} seconds. \n")

        except Exception as e:
            print(f"Error processing paragraph: {file_name}. Error: {e}")

        # Delay added to stay well under the OpenAI API rate limit.
        time.sleep(0.5)  # Throttling to 50% of 3500 RPM limit

# New helper function for processing a single paragraph asynchronously
async def process_paragraph_async(client, semaphore, instruction, file_name, output_file_path, index, total):
    async with semaphore:  # Using semaphore to control concurrency
        start_time = time.perf_counter()

        print(f"Processing paragraph {index + 1}/{total}: {file_name}")
        print(f"Making API Call. ")

        response = await make_api_call_async(
            client,
            messages=[{"role": "system", "content": instruction}],
            model="gpt-3.5-turbo",
        )

        print(f"Received API Contents. ")

        try:
            if response.choices:
                formatted_result = process_and_format_response(file_name, response.choices[0].message.content)
            else:
                formatted_result = process_and_format_response("")

            append_to_file(output_file_path, formatted_result)
        except Exception as e:
            print(f"Error processing paragraph: {file_name}. Error: {e} \n")

        end_time = time.perf_counter()
        print(f"Finished paragraph {index + 1}/{total} in {(end_time - start_time):0.1f} seconds. \n")

        # Delay added to stay well under the OpenAI API rate limit.
        time.sleep(0.5)  # Throttling to 50% of 3500 RPM limit

# Modified asynchronous version for concurrent processing of paragraphs
async def process_paragraphs_async(paragraphs, output_file_path, max_concurrent_tasks=20):
    async_client = AsyncOpenAI(api_key=api_key)
    semaphore = asyncio.Semaphore(max_concurrent_tasks)  # Semaphore to limit concurrent tasks
    tasks = []

    for index, paragraph in enumerate(paragraphs):
        paragraph_text = paragraph.get('response', '')
        file_name = os.path.basename(paragraph.get('prompt', ''))

        instruction = (
            f"Based on the following information, generate a user-like query and an appropriate response:\n\n{paragraph_text[:500]}..."
            if len(paragraph_text) > 500
            else f"Based on the following information, generate a user-like query and an appropriate response:\n\n{paragraph_text}"
        )

        # Creating a task for each paragraph
        task = process_paragraph_async(async_client, semaphore, instruction, file_name, output_file_path, index, len(paragraphs))
        tasks.append(task)

    # Running the tasks concurrently with controlled concurrency
    await asyncio.gather(*tasks)

# Load paragraphs about the school from a JSON file
with open('instruction_dataset.json', 'r') as file:
    paragraphs = json.load(file)

# Path to the file where responses will be saved
output_file_path = 'responses.jsonl'

# Main execution
if __name__ == "__main__":
    # Asking the user to choose between synchronous and asynchronous processing
    choice = input("Choose processing mode: (S)ynchronous or (A)synchronous? [S/A]: ").strip().lower()
    if choice == 's':
        process_paragraphs_sync(paragraphs, output_file_path)
    elif choice == 'a':
        asyncio.run(process_paragraphs_async(paragraphs, output_file_path))
    else:
        print("Invalid choice. Please run the script again and choose 'S', 'A', 's', or 'a'. ")