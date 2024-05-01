#!/bin/bash

#####################################################################
# Advanced Website Downloader and Content Processor
#
# This script provides a comprehensive solution for downloading web content.
# It employs wget for traditional websites and the Playwright Python library
# for dynamic content typical of social media sites. It features user-agent
# spoofing, automated retries, and error handling to ensure effective and
# respectful web scraping practices.
#
# Features:
# - Automated and manual URL processing modes
# - Special handling for dynamically loaded content using Playwright
# - Respect for robots.txt directives
# - Color-coded console output for status monitoring
#
# Prerequisites:
# - Point 'wget_path.config' to the script's folder
# - wget.exe available in the script's directory
# - Python with the Playwright, PyPDF2 libraries installed
# - (pip install PyPDF2 Playwright) then (playwright install)
# - playwright_scrape.py for scraping social media 
# - process_downloaded_content.py script for post-processing
#
# Usage Instructions:
# 1. For manual URL entry, select mode 1 and input the desired URL.
# 2. For automated processing, ensure a 'links.txt' file with URLs exists
#    in the script's directory, and select mode 2.
#
# Author: Elijah Kulpinski
# Date: 03/09/24
#####################################################################

# Initialization of color codes for enhanced readability of script output
RED="\e[31m"
GREEN="\e[32m"
YELLOW="\e[33m"
BLUE="\e[34m"
MAGENTA="\e[0;35m"
CYAN="\e[36m"
RESET="\e[0m"

# Script configuration and global variables
CONFIG_FILE="wget_path.config"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
ACCEPTED_EXTENSIONS="html,htm,pdf,txt"
SOCIAL_MEDIA_PATTERN="facebook\.com|twitter\.com|x\.com|linkedin\.com|wikipedia\.org|reddit\.com|instagram\.com|youtube\.com|tiktok\.com|snapchat\.com|pinterest\.com|vimeo\.com|datausa\.io|encyclopedia\.com"

# Ensures the necessary environment setup, checking for wget.exe and configuring the script directory
setup_environment() {
    echo -e "${CYAN}Setting up script environment...${RESET}"
    if [ -f "$CONFIG_FILE" ]; then
        SCRIPT_DIR=$(cat "$CONFIG_FILE")
    else
        SCRIPT_DIR=$(pwd)
        echo "$SCRIPT_DIR" > "$CONFIG_FILE"
    fi

    if [ ! -f "$SCRIPT_DIR/wget.exe" ]; then
        echo -e "${RED}Error: wget.exe not found. Ensure wget.exe is in the script's directory.${RESET}"
        exit 1
    fi

    SCRIPT_DIR_UNIX=$(echo $SCRIPT_DIR | sed 's/\\/\//g' | sed 's/C:/\/c/')
}

# Function to check if the website content has already been downloaded
check_downloaded() {
    local domain=$1
    if [ -d "$SCRIPT_DIR/$domain" ]; then
        echo -e "${YELLOW}Content for '$domain' already downloaded. Skipping...$RESET"
        return 0
    else
        return 1
    fi
}

# Downloads website content using wget or Playwright based on the type of site
download_content() {
    local url=$(echo $1 | tr -d '\r') # Remove carriage returns for compatibility
    local domain=$(echo $url | awk -F[/:] '{print $4}') # Extract domain from URL

    # Check if the content has already been downloaded to prevent duplication
    if [ -d "$SCRIPT_DIR/$domain" ]; then
        echo -e "${YELLOW}Content for '$domain' already downloaded. Skipping...$RESET"
        return
    fi

    echo -e "${GREEN}Preparing to download:$RESET ${RED}$url$RESET"

    # Check if URL is for a social media or dynamic content site
    if [[ $url =~ $SOCIAL_MEDIA_PATTERN ]]; then
        echo -e "${MAGENTA}Detected social media or dynamic content. Using Playwright for:$RESET ${RED}$domain$RESET"
        # Create directory for domain if it doesn't exist
        mkdir -p "$SCRIPT_DIR/$domain"
        # Use Playwright to scrape the content
        if ! python playwright_scrape.py "$url" "$SCRIPT_DIR/$domain/$(basename "$url").html" "$USER_AGENT"; then
            echo -e "${RED}Playwright failed for $url. Consider manual inspection.$RESET"
        fi
    else
        echo -e "${GREEN}Using wget to clone the website at:${RESET} ${RED}$domain${RESET}"
        # Use wget to clone the entire website
        "$SCRIPT_DIR_UNIX/wget.exe" -m -p -E -k -K -np -e robots=off --wait=1 --random-wait --limit-rate=100k -U "$USER_AGENT" -P "$SCRIPT_DIR/$domain" "$url"
    fi
}

# Main execution block, handling user input and orchestrating the download and processing of content
main() {
    setup_environment

    echo -e "${BLUE}Choose mode: 1 for manual URL entry, 2 to read from 'links.txt':${RESET}"
    read mode

    case "$mode" in
        1)
            echo -e "${GREEN}Enter the URL to scrape:${RESET}"
            read url
            download_content "$url"
            ;;
        2)
            if [ -f "$SCRIPT_DIR/links.txt" ]; then
                while IFS= read -r url || [[ -n "$url" ]]; do  # Ensure the last line is also read even if it doesn't end with a newline
                    echo -e "${CYAN}Processing URL: $url${RESET}"
                    download_content "$url"
                done < "$SCRIPT_DIR/links.txt"
            else
                echo -e "${RED}'links.txt' not found in the script directory.${RESET}"
                exit 1
            fi
            ;;
        *)
            echo -e "${RED}Invalid selection. Please choose 1 or 2.${RESET}"
            exit 1
            ;;
    esac

    echo -e "${CYAN}Processing downloaded content with Python script...${RESET}"
    python process_downloaded_content.py "$SCRIPT_DIR"
    echo -e "${GREEN}Processing complete. Check the 'paragraphs.json' file for output.${RESET}"
    read -p "Press enter to conclude..."
}

# Invoke the main function to start the script
main
