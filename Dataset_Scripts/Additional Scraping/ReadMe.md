# Parkside ChatBot Dataset Scraper

## Overview
This collection of scripts is specifically tailored for the automated extraction of web content to refine an academic ChatBot with domain knowledge pertinent to Parkside. It's particularly adept at sourcing information from educational websites and other scholarly resources. The toolkit utilizes `wget` for static web pages and the Playwright Python library for dynamically generated content, common on social media platforms. It ensures adherence to `robots.txt` directives and employs user-agent spoofing to simulate genuine browser requests.

## Features
- **Dual Mode Operation**: Allows both direct URL input and batch processing from a `links.txt` file.
- **Dynamic Content Handling**: Employs Playwright for sites that extensively use JavaScript to render content.
- **Efficient Content Processing**: Extracts textual information from HTML, PDF, and TXT files, sorting it by origin for seamless incorporation into the ChatBot's knowledge base.
- **User-Agent Spoofing**: Imitates well-known web browsers to minimize the chance of being blocked during scraping.
- **Error Handling and Retries**: Features automated retries with exponential backoff for managing temporary connectivity issues or delays in content loading.

## Prerequisites
- Place `wget.exe` in the same directory as the scripts for downloading static content.
- Python environment with the Playwright and PyPDF2 libraries installed. Use the following commands for installation:
  ```
  pip install playwright PyPDF2
  playwright install
  ```
- The scripts `playwright_scrape.py` and `process_downloaded_content.py` should be located in the script's directory.

## Usage

### Setting Up
1. Download or clone the scripts to your desired location.
2. Verify the presence of `wget.exe` in the script's directory.
3. Install the necessary Python packages if not already done.

### Running the Script
1. Launch a terminal or command prompt window.
2. Navigate to the script directory.
3. Execute `scrape-website.sh` and select your mode:
   - **Mode 1**: Manual URL input. You will be prompted to enter the URL.
   - **Mode 2**: Automated processing from `links.txt`. Ensure this file is present in the directory with one URL per line.

### Output
- The downloaded content is systematically arranged in domain-named directories within the script's directory.
- Extracted text is compiled into a `paragraphs.json` file, categorized by source and formatted for straightforward integration with the ChatBot's knowledge base.

## Customization
- Adjust `SOCIAL_MEDIA_PATTERN` in `scrape-website.sh` to modify the domains for special processing by Playwright.
- Fine-tune scrolling behavior or timeouts in `playwright_scrape.py` according to the specific requirements of the target websites.
- Modify content extraction logic in `process_downloaded_content.py` based on the layout of your target content.

## Known Bugs
Social media scraping remains imperfect, and as these platforms don't host significant unique content about UW Parkside, this aspect is currently de-prioritized. The relevant code is retained for potential future enhancements. For the moment, progress continues with minor manual corrections to address the inaccuracies introduced by the script.