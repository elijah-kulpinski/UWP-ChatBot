import os
import json
import sys
import re
import multiprocessing
from bs4 import BeautifulSoup
from concurrent.futures import ProcessPoolExecutor, as_completed
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')

# Refined patterns to better ignore JavaScript, CSS, and other irrelevant sections
UNWANTED_CONTENT_PATTERNS = re.compile(
    r'(\bvar\s+\w+\s*=)|(\bfunction\b)|(\bconsole\.log\b)|'
    r'(\bdocument\.getElementById\b)|(\bwindow\.\w+\b)|'
    r'(\b<head\b)|(\b<body\b)|(\b<!DOCTYPE html\b)|'
    r'(\b<script\b)|(\b<style\b)|(\b@media\b)|'
    r'(\bAd\s+Blocker\s+Detected\b)|(\bPlease\s+turn\s+off\s+your\s+ad\s+blocker\b)|'
    r'(\badsbygoogle\b)|(\bgoogletag\.cmd\b)|'
    r'({.*?})|(\[.*?\])|(\".*?\")|(\'.*?\')',  # Enhanced to remove more inline JavaScript, CSS, and strings
    re.IGNORECASE | re.DOTALL)

def is_paragraph(text):
    if UNWANTED_CONTENT_PATTERNS.search(text):
        return False
    sentences = sent_tokenize(text)
    return len(sentences) > 1 and any(len(word_tokenize(sentence)) > 3 for sentence in sentences)

def extract_domain(file_path, base_directory):
    normalized_file_path = file_path.replace(os.sep, '/')
    normalized_base_directory = base_directory.rstrip(os.sep).replace(os.sep, '/')
    relative_path = normalized_file_path.split(normalized_base_directory + '/')[1]
    domain = relative_path.split('/')[0]
    return domain

def sanitize_text(text):
    clean_text = re.sub(r'{.*?}|{.*?}|', '', text, flags=re.DOTALL)  # Remove JSON-like structures more aggressively
    clean_text = UNWANTED_CONTENT_PATTERNS.sub('', clean_text)
    return clean_text.strip()

def process_html_file(file_path):
    print(f"Processing HTML file: {file_path}", flush=True)
    paragraphs = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')
        # Focusing on tags more likely to contain meaningful content
        text_blocks = soup.find_all(['p', 'article']) + soup.find_all('div', class_='content')
        for block in text_blocks:
            text = ' '.join(block.stripped_strings)
            sanitized_text = sanitize_text(text)
            if is_paragraph(sanitized_text):
                paragraphs.add(sanitized_text)
    return list(paragraphs)

def process_file(file_path, base_directory):
    print(f"Starting file processing: {file_path}", flush=True)
    domain = extract_domain(file_path, base_directory)
    file_identifier = os.path.relpath(file_path, start=base_directory).replace(os.sep, "_")
    
    if file_path.endswith('.html'):
        paragraphs = process_html_file(file_path)
    else:
        paragraphs = []

    if not paragraphs:
        print(f"No substantial paragraphs found in {file_identifier}.", flush=True)
    return (domain, file_identifier, paragraphs)

def merge_updates(output_file_path, updates):
    print("Merging updates into the JSON file.", flush=True)
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r+', encoding='utf-8') as file:
            data = json.load(file)
            for domain, file_identifier, paragraphs in updates:
                if paragraphs:
                    if domain not in data["content"]:
                        data["content"][domain] = {}
                    data["content"][domain].setdefault(file_identifier, []).extend([{"text": para} for para in paragraphs if para not in data["content"][domain].get(file_identifier, [])])
                    data["total_paragraphs"] += len(paragraphs)
            file.seek(0)
            json.dump(data, file, ensure_ascii=False, indent=4)
            file.truncate()
    else:
        data = {"total_paragraphs": 0, "total_websites": 0, "content": {}}
        for domain, file_identifier, paragraphs in updates:
            if paragraphs:
                if domain not in data["content"]:
                    data["content"][domain] = {}
                data["content"][domain].setdefault(file_identifier, []).extend([{"text": para} for para in paragraphs if para not in data["content"][domain].get(file_identifier, [])])
                data["total_paragraphs"] += len(paragraphs)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
    print("Updates merged successfully.", flush=True)

def process_directory(directory, output_file_path):
    print(f"Starting processing of directory: {directory}", flush=True)
    with ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        tasks = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    tasks.append(executor.submit(process_file, file_path, directory))

        updates = [task.result() for task in as_completed(tasks) if task.result()[2]]
        if updates:
            merge_updates(output_file_path, updates)
    print(f"Content extraction completed. Results saved to '{output_file_path}'.", flush=True)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python process_content.py <directory> <output_file>", flush=True)
        sys.exit(1)

    base_directory = sys.argv[1]
    output_file_path = sys.argv[2]
    process_directory(base_directory, output_file_path)
