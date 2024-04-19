"""Download website content or search for specific information.

This module allows users to download website content or search for specific
information on a website. It provides functionalities for:

Creating a local copy of a website's HTML content. (Option 1)
Downloading an entire website along with its directory structure. (Option 2)
Downloading specific file types from a website. (Option 3)
Searching a website for given keywords. (Option 4)
Navigating and downloading linked websites from a central site. (Option 5)
It utilizes libraries like requests, BeautifulSoup, os, and re for network communication,
HTML parsing, file system interaction, and regular expressions.
"""

import os
import re
from bs4 import BeautifulSoup
import requests

def download_website():
 """
Prompts the user for a choice and calls the appropriate download function.
This function presents a menu to the user with different download options
and calls the corresponding function based on the user's choice.
"""
 print("What do you want to do?")
 print("1. Create a copy of the website on a hard drive.")
 print("2. Duplicate an entire website along with its directory structure.")
 print("3. Look up a site for specific types of files.")
 print("4. Search a website for given keywords.")
 print("5. Navigate all the sites linked from a central site.")
choice = input("Enter your choice (1-5): ")

if choice == '1' or choice == '2':
 url = input("Enter the URL of the website: ")
download_path = os.path.join("/workspaces/dev", os.path.basename(url))
file_types = None
keywords = None
follow_links = (choice == '2')
elif choice == "3":
url = input("Enter the URL of the website: ")
download_path = os.path.join("/workspaces", os.path.basename(url))
file_types = input("Enter the file extensions to download (e.g., .pdf .docx): ").split()
keywords = None
follow_links = False
elif choice == '4':
url = input("Enter the URL of the website: ")
download_path = os.path.join("/workspaces", os.path.basename(url))
file_types = None
keywords = input("Enter the keywords to search for (separated by spaces): ").split()
follow_links = False
elif choice == '5':
url = input("Enter the URL of the website: ")
download_path = os.path.join("/workspaces", os.path.basename(url))
file_types = None
keywords = None
follow_links = True
else:
print("Invalid choice. Exiting...")
return

download_website_impl(url, download_path, file_types, keywords, follow_links)

def download_website_impl(url, download_path, file_types=None, keywords=None, follow_links=False):
"""
Downloads website content based on user-specified options.

This function takes the URL, download path, file types (optional), keywords (optional),
and follow links option (optional) as arguments. It then downloads the website's HTML content,
optionally downloads specific file types, searches for keywords, and follows linked websites
based on user selections.

Args:
url (str): The URL of the website to download.
download_path (str): The path to download the website content.
file_types (list, optional): A list of file extensions to download (e.g., [".pdf", ".docx"]).
Defaults to None.
keywords (list, optional): A list of keywords to search for on the website.
Defaults to None.
follow_links (bool, optional): A flag indicating whether to follow links to other websites.
Defaults to False.
"""
try:
response = requests.get(url, timeout=(60, 500)) # 60s for connection, 500s for reading
response.raise_for_status()

soup = BeautifulSoup(response.text, 'html.parser')

# Create the directory structure
parsed_url = re.sub(r'https?://(www\.)?', '', url)
path = os.path.join(download_path, parsed_url)
os.makedirs(path, exist_ok=True)

# Save the HTML file
with open(os.path.join(path, 'index.html'), 'w', encoding='utf-8') as file:
    file.write(soup.prettify())

# Download files based on file types
if file_types:
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and any(href.endswith(ext) for ext in file_types):
            file_url = f"{url}/{href}" if not href.startswith('http') else href
            download_file(file_url, path)

# Search for keywords
if keywords:
    search_website(soup, keywords, path)

# Follow links and recursively download linked websites
if follow_links:
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('http'):
            download_website_impl(href, download_path, file_types, keywords, follow_links)

except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
def download_file(url, path):
"""
Downloads a file from the specified URL.

This function downloads a file from the given URL and saves it to the specified path.

Args:
url (str): The URL of the file to download.
path (str): The path to save the downloaded file.
"""
try:
response = requests.get(url, timeout=60, stream=True)
response.raise_for_status()

file_name = os.path.basename(url)
file_path = os.path.join(path, file_name)

with open(file_path, 'wb') as file:
file.write(response.content)

except requests.exceptions.Timeout:
print(f"Error: The request to {url} timed out.")
except requests.exceptions.RequestException as e:
print(f"Error downloading {url}: {e}")

def search_website(soup, keywords, path):
"""
Searches a website for given keywords and saves matches to a file.

This function searches the parsed HTML content (soup) for the provided keywords.
If a keyword is found in any text element, it prints a message and writes the
matching text to a file named 'keyword_matches.txt' within the specified path.

Args:
soup (BeautifulSoup): The BeautifulSoup object representing the parsed HTML content.
keywords (list): A list of keywords to search for.
path (str): The path to the directory where the 'keyword_matches.txt' file will be saved.
"""
with open(os.path.join(path, 'keyword_matches.txt'), 'w', encoding='utf-8') as file:
for text in soup.find_all(text=True):
if any(keyword.lower() in text.lower() for keyword in keywords):
print(f"Found keyword in: {text}")
file.write(f"{text}\n")

if name == 'main':
download_website()
print() # Explicit newline character for better compatibility