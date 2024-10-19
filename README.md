# Pinterest Board Image Scraper

This script allows you to download all images from specified Pinterest boards.

## Prerequisites

Before you can run this script, you need to install some software on your computer:

1. **Python**: This script is written in Python, so you need to have Python installed on your computer.

   - Go to https://www.python.org/downloads/
   - Download the latest version of Python for your operating system (Windows, macOS, or Linux)
   - Run the installer and follow the installation instructions
   - Make sure to check the box that says "Add Python to PATH" during installation

2. **pip**: This is a package manager for Python. It usually comes installed with Python.

## Installation

1. **Download the script**: 
   - Download the `main.py` file and the `requirements.txt` file to a folder on your computer.

2. **Install required libraries**:
   - Open a command prompt (on Windows) or terminal (on macOS or Linux)
   - Navigate to the folder where you saved the files
   - Run the following command:
     ```
     pip install -r requirements.txt
     ```
   This will install all the necessary libraries for the script to run.

## Usage

1. **Edit the script**:
   - Open the `main.py` file in a text editor
   - Find the section at the bottom that looks like this:
     ```python
     if __name__ == "__main__":
         pinterest_board_urls = [
             "https://www.pinterest.com/dontworry747/youngheds/",
             "https://www.pinterest.com/dontworry747/studio-shoot/"
             # Add more board URLs here
         ]
         main(pinterest_board_urls)
     ```
   - Replace the example URLs with the URLs of the Pinterest boards you want to
