#!/usr/bin/env python3

"""
Content Extraction Script for HTML, PDF, and TXT Files

This script is part of a workflow designed for extracting text content from various file types
within a specified directory structure. It processes HTML, PDF, and TXT files, extracting paragraphs
of text and organizing the output based on the website and file from which the text was extracted.

The script is intended to be invoked by a shell script or another process that specifies the target
directory containing the files to be processed. The output is a JSON file that includes metadata such
as the total number of paragraphs and websites processed, along with the extracted content organized
by website and file.

Requirements:
- BeautifulSoup4: For parsing HTML files and extracting text content from <p> tags.
- PyPDF2: For extracting text content from PDF files.
- Python's built-in modules: os, json, sys, and urllib.parse.

Output:
- A JSON file named 'paragraphs.json' containing metadata and the structured content extracted from
  the specified directory's files. The content is organized first by website, then by file, and finally
  as a list of paragraphs with unique IDs and text.

Usage:
This script should not be run standalone. It is designed to be invoked with the target directory as
an argument, specifying where the HTML, PDF, and TXT files are located.

Author: Elijah Kulpinski
Date: 03/09/24
"""

import os
import json
import sys
from bs4 import BeautifulSoup
import PyPDF2
from urllib.parse import urlparse

def extract_domain(file_path, base_directory):
    """
    Extracts the domain (website name) from the file path. The domain is considered to be the
    first directory name following the base directory in the path.

    Parameters:
    - file_path (str): The full path to the file being processed.
    - base_directory (str): The base directory where the script is located and from which
                            file processing begins.

    Returns:
    - str: The extracted domain (website name) if found; otherwise, an empty string.
    """
    try:
        # Ensure consistent path separators and remove trailing separator from base_directory if present
        normalized_file_path = file_path.replace(os.sep, '/')
        normalized_base_directory = base_directory.rstrip(os.sep).replace(os.sep, '/')

        # Extract the part of the file path that comes after the base_directory
        relative_path = normalized_file_path.split(normalized_base_directory + '/')[1]
        
        # The domain is the first directory in the relative path
        domain = relative_path.split('/')[0]
        return domain
    except IndexError:
        # Return an empty string if the domain cannot be extracted
        return ""

def process_html_file(file_path, paragraphs):
    """
    Extracts text from <p> tags in an HTML file, applying a length threshold to consider only
    substantial paragraphs. The extracted paragraphs are appended to the provided list.
    Now excludes paragraphs containing specific phrases related to ad blockers.

    Parameters:
    - file_path (str): The path to the HTML file.
    - paragraphs (list): The list to which extracted paragraphs are appended.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

        for tag in soup.find_all('p'):
            text = ' '.join(tag.stripped_strings)
            # Define phrases that indicate ad blocker content
            ad_blocker_phrases = [
                "blocks ads hinders",
                "turning off your ad blocker"
            ]

            # Check if the paragraph contains any of the ad blocker phrases
            if any(phrase in text for phrase in ad_blocker_phrases):
                continue  # Skip this paragraph

            if text and len(text.split()) > 10:  # Filter out short paragraphs
                paragraphs.append(text)

def process_pdf_file(file_path, paragraphs):
    """
    Extracts text from a PDF file, combining text from all pages and splitting it into paragraphs
    based on double newlines. Substantial paragraphs are appended to the provided list.

    Parameters:
    - file_path (str): The path to the PDF file.
    - paragraphs (list): The list to which extracted paragraphs are appended.
    """
    with open(file_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        text = ' '.join(page.extract_text() for page in pdf.pages if page.extract_text())
    paragraphs += [para.strip() for para in text.strip().split('\n\n') if para.strip() and len(para.split()) > 10]

def process_txt_file(file_path, paragraphs):
    """
    Processes a TXT file, treating each blank-line-separated section as a paragraph. Substantial
    paragraphs are appended to the provided list.

    Parameters:
    - file_path (str): The path to the TXT file.
    - paragraphs (list): The list to which extracted paragraphs are appended.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        paragraph = []
        for line in file:
            stripped_line = line.strip()
            if stripped_line:
                paragraph.append(stripped_line)
            elif paragraph:  # End of a paragraph
                paragraph_text = ' '.join(paragraph)
                if len(paragraph_text.split()) > 10:
                    paragraphs.append(paragraph_text)
                paragraph = []
        if paragraph:  # Handle the last paragraph in the file
            paragraph_text = ' '.join(paragraph)
            if len(paragraph_text.split()) > 10:
                paragraphs.append(paragraph_text)

def dump_json(content_data, total_paragraphs, total_websites, output_file_path):
    """
    Saves the extracted content data along with metadata to a JSON file.

    This function creates a JSON object that includes the total number of paragraphs, the total number of
    websites processed, and the structured content data. It then writes this JSON object to the specified output
    file, overwriting any existing content. This ensures that the latest extracted data is always preserved,
    providing a checkpoint mechanism in case the script is interrupted.

    Parameters:
    - content_data (dict): A dictionary containing the structured content data organized by website and file,
                           with each file containing a list of paragraph dictionaries.
    - total_paragraphs (int): The total number of paragraphs that have been extracted and processed across all files.
    - total_websites (int): The total number of unique websites from which content has been extracted.
    - output_file_path (str): The file path where the JSON data should be saved. If the file already exists,
                              it will be overwritten with the new data.

    Output:
    - A JSON file is created or updated at the specified output_file_path, containing the metadata and the structured
      content data. This file serves as both the output of the script and a checkpoint for data that has been processed,
      ensuring that progress is not lost if the script needs to be restarted.
    """
    metadata = {
        "total_paragraphs": total_paragraphs,
        "total_websites": total_websites,
        "content": content_data
    }
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(metadata, output_file, ensure_ascii=False, indent=4)

def process_directory(directory, existing_data):
    """
    Recursively processes the specified directory, extracting text content from HTML, PDF, and TXT files.
    The extracted paragraphs are organized by the website and file from which they were obtained. Only
    new websites not present in the existing data are processed.

    Parameters:
    - directory (str): The base directory containing the files to process.
    - existing_data (dict): Data loaded from an existing 'paragraphs.json', if present.

    Returns:
    - tuple: Contains the updated content data, total number of paragraphs extracted, and the number of unique websites processed.
    """
    output_data = existing_data if existing_data else {}
    paragraph_id = sum(len(p["text"]) for website in existing_data.values() for file in website.values() for p in file) if existing_data else 0
    website_count = set(output_data.keys())

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith((".html", ".pdf", ".txt")):  # Ensure only supported file types are processed
                file_path = os.path.join(root, file)
                domain = extract_domain(file_path, directory)

                # Adjusted to continue processing even if the domain is already in the data, to handle subdirectories
                paragraphs = []
                if file.endswith(".html"):
                    process_html_file(file_path, paragraphs)
                elif file.endswith(".pdf"):
                    process_pdf_file(file_path, paragraphs)
                elif file.endswith(".txt"):
                    process_txt_file(file_path, paragraphs)

                if paragraphs:
                    website_count.add(domain)
                    # Create a unique identifier for each file based on its path, to avoid overwriting files with the same name in different subdirectories
                    file_identifier = os.path.relpath(file_path, start=directory).replace(os.sep, "_")
                    if domain not in output_data:
                        output_data[domain] = {}
                    if file_identifier not in output_data[domain]:
                        output_data[domain][file_identifier] = []

                    output_data[domain][file_identifier] += [{"id": paragraph_id + i, "text": para} for i, para in enumerate(paragraphs)]
                    paragraph_id += len(paragraphs)
                    
                    # Update the JSON file with new paragraphs
                    dump_json(output_data, paragraph_id, len(website_count), output_file_path)
                    print(f"Updated '{output_file_path}' with content from '{file_identifier}'.", flush=True)

    return output_data, paragraph_id, len(website_count)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python process_content.py <directory>", flush=True)
        sys.exit(1)

    base_directory = sys.argv[1]
    
    # Check if 'paragraphs.json' already exists and load existing data if present.
    output_file_path = 'paragraphs.json'
    existing_data = None
    if os.path.exists(output_file_path):
        with open(output_file_path, 'r', encoding='utf-8') as existing_file:
            existing_data = json.load(existing_file).get("content", {})

    content_data, total_paragraphs, total_websites = process_directory(base_directory, existing_data)

    metadata = {
        "total_paragraphs": total_paragraphs,
        "total_websites": total_websites,
        "content": content_data
    }

    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        json.dump(metadata, output_file, ensure_ascii=False, indent=4)

    print(f"Processing completed. Total paragraphs: {total_paragraphs}, Total websites: {total_websites}. Check '{existing_file_path}' for the output.", flush=True)
