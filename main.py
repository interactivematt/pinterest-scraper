import os
import time
import requests
from bs4 import BeautifulSoup
from seleniumbase import Driver
from urllib.parse import urljoin, urlparse
import json
import hashlib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    print("Setting up driver...")
    return Driver(uc=True)

def scroll_once(driver):
    print("Scrolling once...")
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    new_height = driver.execute_script("return document.body.scrollHeight")
    return new_height > last_height

def extract_image_urls(html_content):
    print("Extracting image URLs...")
    soup = BeautifulSoup(html_content, 'html.parser')
    img_tags = soup.find_all('img', {'src': True})
    print(f"Found {len(img_tags)} img tags")
    urls = []
    for img in img_tags:
        url = img['src']
        if '/200x' in url or '/236x' in url:
            url = url.replace('/200x', '/1200x').replace('/236x', '/1200x')
        urls.append(url)
    print(f"Extracted {len(urls)} image URLs")
    return urls

def get_original_filename(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = os.path.basename(path)
    name, ext = os.path.splitext(filename)
    if not ext:
        ext = '.jpg'
    return f"{name}{ext}"

def download_images(urls, folder_name, existing_files):
    print(f"Downloading {len(urls)} images to {folder_name}")
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    
    new_files = []
    for url in urls:
        try:
            original_filename = get_original_filename(url)
            if original_filename in existing_files:
                print(f"Skipping existing file: {original_filename}")
                continue

            response = requests.get(url)
            if response.status_code == 200:
                file_path = os.path.join(folder_name, original_filename)
                with open(file_path, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {original_filename}")
                new_files.append(original_filename)
            else:
                print(f"Failed to download: {url}")
        except Exception as e:
            print(f"Error downloading {url}: {str(e)}")
    
    return new_files

def get_pin_count(driver):
    try:
        pin_count_element = driver.find_element(By.CSS_SELECTOR, '[data-test-id="pin-count"]')
        pin_count_text = pin_count_element.text
        pin_count = int(''.join(filter(str.isdigit, pin_count_text)))
        print(f"Detected pin count: {pin_count}")
        return pin_count
    except Exception as e:
        print(f"Error detecting pin count: {str(e)}")
        return None

def get_board_name(url):
    parsed_url = urlparse(url)
    path_parts = parsed_url.path.strip('/').split('/')
    return path_parts[-1] if len(path_parts) > 1 else 'unknown_board'

def scrape_pinterest_board(url, base_folder):
    board_name = get_board_name(url)
    folder_name = os.path.join(base_folder, board_name)
    print(f"Starting to scrape Pinterest board: {url}")
    driver = setup_driver()
    try:
        print("Loading page...")
        driver.get(url)
        print("Waiting for images to load...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "img"))
        )
        
        pin_count = get_pin_count(driver)
        if pin_count is None:
            print("Unable to detect pin count. Using default limit of 500.")
            pin_count = 500
        
        existing_files = set(os.listdir(folder_name)) if os.path.exists(folder_name) else set()
        all_urls = set()
        image_count = len(existing_files)
        scroll_count = 0
        keep_scrolling = True
        
        while keep_scrolling and image_count < pin_count:
            print(f"Iteration {scroll_count + 1}")
            
            # Extract images
            html_content = driver.page_source
            new_urls = set(extract_image_urls(html_content)) - all_urls
            all_urls.update(new_urls)
            
            # Download new images
            if new_urls:
                new_files = download_images(list(new_urls), folder_name, existing_files)
                image_count += len(new_files)
                existing_files.update(new_files)
                print(f"Total unique images downloaded so far: {image_count}")
            
            # Check if we've reached the pin count
            if image_count >= pin_count:
                print(f"Reached pin count limit of {pin_count}. Stopping.")
                break
            
            # Scroll once
            keep_scrolling = scroll_once(driver)
            scroll_count += 1
            
            time.sleep(1)  # Short pause between iterations
        
        print(f"Scraping completed. Total scrolls: {scroll_count}, Total images: {image_count}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        print("Closing driver...")
        driver.quit()

def main(urls):
    base_folder = "pinterest_images"
    if not os.path.exists(base_folder):
        os.makedirs(base_folder)
    
    for url in urls:
        scrape_pinterest_board(url, base_folder)

if __name__ == "__main__":
    pinterest_board_urls = [
        "https://www.pinterest.com/dontworry747/youngheds/",
        "https://www.pinterest.com/dontworry747/studio-shoot/"
        # Add more board URLs here
    ]
    main(pinterest_board_urls)
