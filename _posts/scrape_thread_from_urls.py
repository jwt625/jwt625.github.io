#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# %% 20241006, load urls and scrape those tweets

import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import json
import re
from datetime import datetime

#%%

def get_original_media_url(url):
    return re.sub(r'&name=\w+', '', url)

def download_media(url, folder, filename):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        filepath = os.path.join(folder, filename)
        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        return filepath
    return None

def scrape_tweet(driver, tweet_element, media_folder, tweet_timestamp):
    tweet_data = {}

    # Extract tweet text
    try:
        tweet_text = tweet_element.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]').text
        tweet_data['text'] = tweet_text
    except NoSuchElementException:
        tweet_data['text'] = ''

    # Extract and process media
    try:
        media_elements = tweet_element.find_elements(By.CSS_SELECTOR, 'div[data-testid="tweetPhoto"] img')
        tweet_data['media'] = []
        for index, elem in enumerate(media_elements):
            media_url = elem.get_attribute('src')
            original_url = get_original_media_url(media_url)
            
            # Create filename based on tweet timestamp
            file_timestamp = tweet_timestamp.strftime("%Y%m%d_%H%M%S")
            filename = f"{file_timestamp}_{index}.jpg"
            
            # Download and save the media
            local_path = download_media(original_url, media_folder, filename)
            
            if local_path:
                tweet_data['media'].append({
                    'url': original_url,
                    'local_path': os.path.relpath(local_path, start=os.getcwd())
                })
    except Exception as e:
        print(f"Error processing media: {str(e)}")

    return tweet_data

def scrape_thread(driver, url, media_folder, str_user_handle):
    driver.get(url)
    time.sleep(2)
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
        )
    except TimeoutException:
        print(f"Timeout waiting for tweet to load: {url}")
        return None

    thread_data = {'url': url, 'tweets': []}
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # Find all tweets from the specified user
        tweets = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
        user_tweets = [tweet for tweet in tweets if str_user_handle.lower() in tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Name"]').text.lower()]

        for tweet in user_tweets:
            # Check if we've already processed this tweet
            if tweet in [t['element'] for t in thread_data['tweets']]:
                continue

            # Extract tweet timestamp
            try:
                time_element = tweet.find_element(By.CSS_SELECTOR, 'time')
                timestamp = time_element.get_attribute('datetime')
                tweet_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                tweet_timestamp = tweet_date.isoformat()
            except NoSuchElementException:
                tweet_timestamp = ''

            tweet_data = scrape_tweet(driver, tweet, media_folder, tweet_date)
            tweet_data['timestamp'] = tweet_timestamp
            tweet_data['element'] = tweet  # Store the element for later comparison
            thread_data['tweets'].append(tweet_data)

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Remove the 'element' key from tweet data before returning
    for tweet in thread_data['tweets']:
        del tweet['element']

    return thread_data


#%% login manually and keep using the same tag
driver = webdriver.Chrome()  # Or whichever browser you're using


#%% get all urls

# Get the list of all window handles (tabs)
window_handles = driver.window_handles

# List to store valid URLs
urls = []

# Iterate through each tab and get the URL
for handle in window_handles:
    driver.switch_to.window(handle)
    url = driver.current_url
    
    # Check if the URL matches the expected format
    if url.startswith("https://x.com/jwt0625/status/"):
        # Extract the numeric part at the end
        try:
            tweet_id = int(url.split("/")[-1])
            urls.append((tweet_id, url))  # Store as a tuple (tweet_id, url)
        except ValueError:
            # Ignore URLs that don't end with a valid number
            continue

# Sort the URLs based on the tweet ID (ascending order)
sorted_urls = sorted(urls, key=lambda x: x[0])

# Export sorted URLs to a text file
with open("sorted_tweet_urls.txt", "w") as file:
    for tweet_id, url in sorted_urls:
        file.write(url + "\n")


#%% Setup
media_folder = 'media'
os.makedirs(media_folder, exist_ok=True)
str_user_handle = "@jwt0625"  # Replace with the actual user handle

# Read URLs from file
# str_fn = 'urls_tweet_to_scrape_20241215.txt'
str_fn = 'sorted_tweet_urls_20250420.txt'

# str_fn = 'urls_test.txt'
with open(str_fn, 'r') as f:
    urls = [line.strip() for line in f if line.strip()]

# Scrape tweets
threads_data = []
for url in urls:
    thread_data = scrape_thread(driver, url, media_folder, str_user_handle)
    if thread_data:
        threads_data.append(thread_data)
        # Save to JSON file
        with open('scraped_tweets.json', 'w', encoding='utf-8') as f:
            json.dump(threads_data, f, ensure_ascii=False, indent=4)
    time.sleep(1)  # Add a small delay between requests

# Save to JSON file
with open('scraped_tweets.json', 'w', encoding='utf-8') as f:
    json.dump(threads_data, f, ensure_ascii=False, indent=4)

print(f"Scraped {len(threads_data)} threads.")

# %%

import shutil
from datetime import datetime

#% Move JPG files to a new folder based on date range

# Get all JPG files in the media folder
target_path = "../assets/images/2025"
media_folder = 'media'
jpg_files = [f for f in os.listdir(media_folder) if f.endswith('.jpg')]

if jpg_files:
    # Extract dates from filenames (assuming format: YYYYMMDD_HHMMSS_index.jpg)
    dates = []
    for jpg in jpg_files:
        try:
            # Extract the date part from the filename (first 8 characters)
            date_str = jpg.split('_')[0]
            if len(date_str) == 8:  # Ensure it's in YYYYMMDD format
                date_obj = datetime.strptime(date_str, '%Y%m%d')
                dates.append(date_obj)
        except (ValueError, IndexError):
            # If filename doesn't match expected format, use creation time as fallback
            creation_time = os.path.getctime(os.path.join(media_folder, jpg))
            dates.append(datetime.fromtimestamp(creation_time))

    # Determine the date range
    min_date = min(dates).strftime("%Y%m%d")
    max_date = max(dates).strftime("%Y%m%d")

    # Create a new folder name based on the date range
    folder_name = f"{min_date}_{max_date}"
    
    # Define target path
    new_folder_path = os.path.join(target_path, folder_name)
    
    # Create the target directory if it doesn't exist
    os.makedirs(new_folder_path, exist_ok=True)

    # Move JPG files to the new folder
    for jpg in jpg_files:
        source_path = os.path.join(media_folder, jpg)
        dest_path = os.path.join(new_folder_path, jpg)
        shutil.move(source_path, dest_path)

    print(f"Moved {len(jpg_files)} JPG files to folder: {new_folder_path}")
else:
    print("No JPG files found in the media folder.")

# %%


########################################
# process the json file
########################################
#%%
import json
import os
from datetime import datetime


#%%
def format_media(media_item, media_folder):
    file_name = os.path.basename(media_item['local_path'])
    new_path = f"/assets/images/2025/{media_folder}/{file_name}"
    return f"![{file_name}]({new_path})"

def create_markdown(json_file, output_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Determine the date range for the media folder name
    all_dates = [datetime.fromisoformat(tweet['timestamp']) for thread in data for tweet in thread['tweets']]
    earliest_date = min(all_dates)
    latest_date = max(all_dates)
    media_folder = f"{earliest_date.strftime('%Y%m%d')}_{latest_date.strftime('%Y%m%d')}"

    with open(output_file, 'w', encoding='utf-8') as f:
        for i, thread in enumerate(data, 1):
            print(i)
            if len(thread['tweets']) == 0:
                continue
            # First tweet in the thread
            first_tweet = thread['tweets'][0]
            f.write(f"{i}. {first_tweet['text']}\n")
            
            # Media for the first tweet
            for media in first_tweet['media']:
                f.write(format_media(media, media_folder) + "\n")
            
            # If there are more tweets in the thread
            if len(thread['tweets']) > 1:
                for tweet in thread['tweets'][1:]:
                    f.write(f"   - {tweet['text']}\n")
                    # Media for this tweet
                    for media in tweet['media']:
                        f.write("   " + format_media(media, media_folder) + "\n")
            
            f.write("\n")  # Add a blank line between threads


#%%
json_file = "scraped_tweets_20250413_20250420.json"
output_md_file = "2025-04-20-weekly-OFS-43.md"
# output_file = "tmp.md"
create_markdown(json_file, output_md_file)
print(f"Markdown file '{output_md_file}' has been created.")
# %% extract tags and section titles using deepseek

from helpers_LLM import process_with_llm_from_files
from datetime import datetime

output_file = f"output_{datetime.now().strftime('%Y%m%d')}.md"
res = process_with_llm_from_files(config_file='config.json',
                                  prompt_file='prompt_extract_tag_section.md',
                                  content_file=output_md_file,
                                  output_file=output_file)

# %%
