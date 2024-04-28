import requests
from bs4 import BeautifulSoup
import os
import subprocess

# Function to download a file from a given URL
def download_file(url, download_folder):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            file_name = os.path.join(download_folder, url.split("/")[-1])
            with open(file_name, 'wb') as file:
                file.write(response.content)
                print(f"Downloaded: {file_name}")
        else:
            print(f"Failed to download: {url}")
    except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

# Function to find and list downloadable file links on a webpage
def list_files_on_website(url, download_folder, visited_pages, downloaded_files):
    try:
        if url in visited_pages:
            return

        visited_pages.add(url)

        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            links = soup.find_all('a', href=True)

            download_links = []
            for link in links:
                file_url = link.get('href')
                if file_url.startswith('http'):
                    download_links.append(file_url)
                elif file_url.startswith('/'):
                    download_links.append(url + file_url)

            for link in download_links:
                if link not in downloaded_files:
                    downloaded_files.add(link)

            print("\nFiles available for download:")
            for i, link in enumerate(downloaded_files, 1):
                print(f"{i}. {link}")

        else:
            print(f"Failed to fetch URL: {url}")
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")

# Prompt the user for input and filtering options
def get_user_input():
    website_url = input("Enter the URL of the website to scrape: ")
    download_folder = input("Enter the folder to save downloaded files: ")

    return website_url, download_folder

# Create a command-line interface
def main():
    subprocess.run(["figlet", "WebFileGrab"])
    website_url, download_folder = get_user_input()

    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    visited_pages = set()
    downloaded_files = set()
    list_files_on_website(website_url, download_folder, visited_pages, downloaded_files)

    # Prompt user for download choice
    while True:
        try:
            user_choice = input("\nEnter the number of the file to download (0 to download all files, -1 to quit): ")
            user_choice = int(user_choice)

            if user_choice == -1:
                break
            elif user_choice == 0:
                for link in downloaded_files:
                    download_file(link, download_folder)
            elif 1 <= user_choice <= len(downloaded_files):
                selected_link = list(downloaded_files)[user_choice - 1]
                download_file(selected_link, download_folder)
            else:
                print("Invalid choice. Please enter a valid number.")

        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
