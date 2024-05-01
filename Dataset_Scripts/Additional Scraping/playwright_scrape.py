#!/usr/bin/env python3

"""
Playwright Web Scraper for Dynamic and Social Media Content

This script utilizes the Playwright library to automate browser interactions, making it highly effective for
scraping web pages that dynamically load content, such as social media platforms. It includes mechanisms to
scroll through the page to trigger the loading of lazy-loaded content and to sanitize URLs to create valid
filenames for saving the HTML output.

Usage:
    python playwright_scrape.py <URL> <output_file_path> <user_agent>

Requirements:
    - Playwright Python package and compatible browser binaries ('playwright install').
    - Python 3.6 or higher.

Arguments:
    - URL: The web page's URL to scrape.
    - output_file_path: The directory where the scraped HTML content will be saved.
    - user_agent: The user agent string for the browser session to mimic a particular browser.

Output:
    - Saves the HTML content of the scraped web page into a file within the specified directory.

Author: Elijah Kulpinski
Date: 03/09/24
"""

import sys
import time
from playwright.sync_api import sync_playwright
from pathlib import Path
import re
import os

def sanitize_filename(url):
    """
    Creates a safe filename from a URL by removing or replacing characters that are not allowed in file names.

    Parameters:
    - url (str): The original URL intended to be converted into a filename.

    Returns:
    - (str): A sanitized string that can be safely used as a filename.
    """
    return re.sub(r'[<>:"/\\|?*]', '_', url)[:255]

def ensure_directory_exists(directory_path):
    """
    Ensures that the specified directory exists; if not, it creates the directory.

    Parameters:
    - directory_path (str): The path to the directory that needs to be checked or created.
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path, exist_ok=True)

def scroll_and_wait_for_navigation(page, scroll_timeout=5, max_scrolls=3):
    """
    Scrolls through the webpage and waits for lazy-loaded content to load. Handles potential navigations triggered by scrolling.
    
    Args:
        page (Playwright Page object): The page to scroll and extract content from.
        scroll_timeout (int): The time to wait after each scroll to allow content to load.
        max_scrolls (int): Maximum number of times to scroll the page.
    """
    for _ in range(max_scrolls):
        try:
            # Scroll to the bottom of the page to trigger lazy loading
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(scroll_timeout * 1000)  # Wait for content to load
        except Exception as e:
            print(f"Scrolling issue encountered: {str(e)}", flush=True)
            break  # Exit the loop if an error occurs during scrolling

def scrape_with_playwright(url, output_dir, user_agent):
    """
    Scrapes the content of the specified URL using Playwright, handling dynamic content loading and navigation issues.
    Saves the resulting HTML content to a file in the specified output directory.

    Parameters:
    - url (str): The URL of the webpage to scrape.
    - output_dir (str): The directory where the scraped content should be saved.
    - user_agent (str): The user agent string to be used for the browser session.
    """
    print(f"Sanitizing URL.", flush=True)
    sanitized_name = sanitize_filename(url)  # Sanitize URL to create a valid filename
    
    print(f"Constructing Output Path.", flush=True)
    output_file_path = os.path.join(output_dir, f"{sanitized_name}.html")  # Construct full output file path

    with sync_playwright() as p:
        print(f"Launching Headless Browser.", flush=True)
        browser = p.chromium.launch(headless=True)  # Launch a headless browser
        page = browser.new_page(user_agent=user_agent)  # Set the specified user agent
        
        print(f"Navigating to URL.", flush=True)
        page.goto(url, wait_until='domcontentloaded', timeout=60000)  # Navigate to the URL and wait for content to load

        # Scroll through the page to ensure all lazy-loaded content is triggered
        print(f"Scrolling Down Page.", flush=True)
        scroll_and_wait_for_navigation(page)

        print(f"Extracting Page HTML.", flush=True)
        content = page.content()  # Extract the page's HTML content

        # Ensure the output directory exists before attempting to write the file
        print(f"Ensuring Directory Exists.", flush=True)
        ensure_directory_exists(output_dir)

        # Save the extracted content to the specified file
        print(f"Writing File Contents.", flush=True)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(content)

        print(f"Content Successfully Saved To: {output_file_path}.", flush=True)
        browser.close()  # Close the browser session

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python playwright_scrape.py <URL> <output_directory> <user_agent>", flush=True)
        sys.exit(1)

    url = sys.argv[1]
    output_dir = sys.argv[2]
    user_agent = sys.argv[3]
    scrape_with_playwright(url, output_dir, user_agent)
    print(f"Finished scraping {url} with Playwright. Exiting script instance.", flush=True)