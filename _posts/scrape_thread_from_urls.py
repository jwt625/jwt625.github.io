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
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import time
import json
import re
from datetime import datetime

print("="*60)
print("TWITTER SCRAPING SCRIPT STARTED")
print("="*60)

# Load configuration
try:
    with open('config.json', 'r') as f:
        config = json.load(f)
    print("Configuration loaded successfully")
except FileNotFoundError:
    print("Error: config.json not found. Please ensure config.json exists in the current directory.")
    exit(1)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON in config.json: {e}")
    exit(1)

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

    # First, check for and click "Show more" button if present
    try:
        show_more_button = tweet_element.find_element(By.CSS_SELECTOR, 'button[data-testid="tweet-text-show-more-link"]')
        if show_more_button.is_displayed():
            print("Found 'Show more' button, clicking to expand tweet...")
            driver.execute_script("arguments[0].click();", show_more_button)
            time.sleep(0.5)  # Wait for content to expand
    except NoSuchElementException:
        # No "Show more" button found, which is fine
        pass
    except Exception as e:
        print(f"Error clicking 'Show more' button: {str(e)}")

    # Extract tweet text with full URLs
    try:
        tweet_text_element = tweet_element.find_element(By.CSS_SELECTOR, 'div[data-testid="tweetText"]')
        tweet_text = tweet_text_element.text

        # Find all links within the tweet text element and extract full URLs
        try:
            links = tweet_text_element.find_elements(By.TAG_NAME, 'a')
            print(f"Found {len(links)} links in tweet")
            for i, link in enumerate(links):
                # Get the visible (potentially truncated) text
                visible_text = link.text
                href_url = link.get_attribute('href')
                print(f"Link {i+1}: visible_text='{visible_text}', href='{href_url}'")

                # NEW APPROACH: Reconstruct URL from fragmented spans within the link
                full_url = None
                try:
                    # Find all spans within this link
                    spans = link.find_elements(By.TAG_NAME, 'span')
                    if spans:
                        # Reconstruct the URL by concatenating span texts
                        url_parts = []
                        for span in spans:
                            span_text = span.text
                            # Skip the ellipsis span
                            if span_text and span_text not in ['…', '...']:
                                url_parts.append(span_text)

                        if url_parts:
                            reconstructed_url = ''.join(url_parts)
                            print(f"Reconstructed URL from spans: '{reconstructed_url}'")

                            # Validate that this looks like a URL
                            if reconstructed_url.startswith('http'):
                                full_url = reconstructed_url
                            elif reconstructed_url.startswith('www.') or '.' in reconstructed_url:
                                # Add https:// if it's missing
                                full_url = 'https://' + reconstructed_url
                except Exception as span_error:
                    print(f"Error reconstructing URL from spans: {str(span_error)}")

                # Fallback: Try to get the full URL from various attributes
                if not full_url:
                    for attr in ['data-expanded-url', 'title', 'aria-label', 'data-url', 'data-original-url']:
                        full_url = link.get_attribute(attr)
                        if full_url and full_url.startswith('http') and not full_url.startswith('https://t.co'):
                            break

                # If we still don't have a full URL, try hovering to trigger the tooltip
                if not full_url or full_url.startswith('https://t.co'):
                    try:
                        # Hover over the link to potentially trigger tooltip with full URL
                        ActionChains(driver).move_to_element(link).perform()
                        time.sleep(0.5)  # Wait for tooltip to appear

                        # Check for tooltip or updated attributes after hover
                        for attr in ['title', 'aria-label', 'data-expanded-url']:
                            hover_url = link.get_attribute(attr)
                            if hover_url and hover_url.startswith('http') and not hover_url.startswith('https://t.co'):
                                full_url = hover_url
                                break

                        # Also check if there's a tooltip element that appeared
                        try:
                            tooltip_elements = driver.find_elements(By.CSS_SELECTOR, '[role="tooltip"], .tooltip, [data-testid*="tooltip"]')
                            for tooltip in tooltip_elements:
                                tooltip_text = tooltip.text
                                if tooltip_text and tooltip_text.startswith('http') and not tooltip_text.startswith('https://t.co'):
                                    full_url = tooltip_text
                                    break
                        except:
                            pass

                    except Exception as hover_error:
                        print(f"Error during hover: {str(hover_error)}")
                        pass

                # If we found a full URL and it's different from the visible text, replace it
                if full_url and visible_text and visible_text in tweet_text:
                    # Only replace if the visible text appears to be truncated (ends with ... or is incomplete)
                    if visible_text.endswith('…') or visible_text.endswith('...') or len(visible_text) < len(full_url):
                        tweet_text = tweet_text.replace(visible_text, full_url)
                        print(f"Replaced truncated URL: '{visible_text}' -> '{full_url}'")

        except Exception as e:
            print(f"Error processing links in tweet: {str(e)}")

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


print("\n" + "="*60)
print("SECTION 1: BROWSER SETUP AND LOGIN")
print("="*60)

#%% login manually and keep using the same tag
print("Opening Firefox browser...")

# Firefox options to help avoid detection
from selenium.webdriver.firefox.options import Options
firefox_options = Options()

# Use your existing Firefox profile where you're already logged in
profile_path = config.get('firefox_profile_path')
if not profile_path:
    print("Error: firefox_profile_path not found in config.json")
    exit(1)
firefox_options.add_argument(f"--profile={profile_path}")

# Set window size to appear more natural
firefox_options.add_argument("--width=1920")
firefox_options.add_argument("--height=1080")

# Add options to make the browser less detectable
firefox_options.set_preference("dom.webdriver.enabled", False)
firefox_options.set_preference('useAutomationExtension', False)
firefox_options.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0")

# Disable telemetry and data reporting (safe options)
firefox_options.set_preference("toolkit.telemetry.enabled", False)
firefox_options.set_preference("toolkit.telemetry.unified", False)
firefox_options.set_preference("datareporting.healthreport.uploadEnabled", False)
firefox_options.set_preference("datareporting.policy.dataSubmissionEnabled", False)

# Network settings to appear more natural
firefox_options.set_preference("network.http.sendRefererHeader", 2)
firefox_options.set_preference("network.http.sendSecureXSiteReferrer", True)

# Disable some automated browser indicators
firefox_options.set_preference("media.peerconnection.enabled", False)

driver = webdriver.Firefox(options=firefox_options)
print("Browser opened successfully!")
print("\nPlease:")
print("1. Login to Twitter/X manually in the browser")
print("2. Open multiple tabs with the tweet URLs you want to scrape")
print("3. Make sure all URLs follow the pattern: https://x.com/jwt0625/status/[tweet_id]")
print("4. Press ENTER when you're ready to continue...")
input()

print("\n" + "="*60)
print("SECTION 2: COLLECTING URLS FROM BROWSER TABS")
print("="*60)

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
current_date = datetime.now().strftime("%Y%m%d")
filename_urls = f"sorted_tweet_urls_{current_date}.txt"
with open(filename_urls, "w") as file:
    for tweet_id, url in sorted_urls:
        file.write(url + "\n")

print(f"Found and sorted {len(sorted_urls)} URLs")
print(f"URLs saved to: {filename_urls}")

print("\n" + "="*60)
print("SECTION 3: SCRAPING TWEETS")
print("="*60)

#%% Setup
media_folder = 'media'
os.makedirs(media_folder, exist_ok=True)
str_user_handle = "@jwt0625"  # Replace with the actual user handle

# Read URLs from file
str_fn = filename_urls

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

# Save to JSON file with date in filename
current_date = datetime.now().strftime("%Y%m%d")
json_filename = f'scraped_tweets_{current_date}.json'
with open(json_filename, 'w', encoding='utf-8') as f:
    json.dump(threads_data, f, ensure_ascii=False, indent=4)

print(f"Scraped {len(threads_data)} threads.")
print(f"Data saved to: {json_filename}")

print("\n" + "="*60)
print("SECTION 4: ORGANIZING MEDIA FILES")
print("="*60)

# %%

import shutil
from datetime import datetime

#% Move JPG files to a new folder based on date range

# Get all JPG files in the media folder
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
    
    # Define target path (go up one directory from _posts to repository root)
    target_path = os.path.join(os.path.dirname(os.getcwd()), "assets", "images", "2025")
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

print("\n" + "="*60)
print("SECTION 5: CREATING MARKDOWN FROM JSON")
print("="*60)

# %%

########################################
# process the json file
########################################
#%%
import json
import os
from datetime import datetime

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
# json_file = "scraped_tweets_20250420_20250427.json"
json_file = json_filename

# Automatically generate output filename with current date and next OFS index
import glob

# Get current date in YYYY-MM-DD format
current_date = datetime.now().strftime("%Y-%m-%d")

# Find all existing OFS files to determine the next index
ofs_files = glob.glob("*-weekly-OFS-*.md")
if ofs_files:
    # Extract OFS numbers from filenames
    ofs_numbers = []
    for filename in ofs_files:
        # Extract number after "OFS-" and before ".md"
        import re
        match = re.search(r'OFS-(\d+)\.md', filename)
        if match:
            ofs_numbers.append(int(match.group(1)))

    # Get the next OFS number
    next_ofs_number = max(ofs_numbers) + 1 if ofs_numbers else 1
else:
    next_ofs_number = 1

output_md_file = f"{current_date}-weekly-OFS-{next_ofs_number}.md"
print(f"Generated output filename: {output_md_file}")

# output_file = "tmp.md"
create_markdown(json_file, output_md_file)
print(f"Markdown file '{output_md_file}' has been created.")

print("\n" + "="*60)
print("SECTION 6: EXTRACTING TAGS AND SECTION TITLES USING LLM")
print("="*60)

# %% extract tags and section titles using deepseek

from helpers_LLM import process_with_llm_from_files
from datetime import datetime

output_file = f"output_{datetime.now().strftime('%Y%m%d')}.md"
res = process_with_llm_from_files(config_file='config.json',
                                  prompt_file='prompt_extract_tag_section.md',
                                  content_file=output_md_file,
                                  output_file=output_file)
print(f"LLM processing completed. Output saved to: {output_file}")

print("\n" + "="*60)
print("SECTION 7: PROCESSING MARKDOWN FILES")
print("="*60)

# %%

########################################
# Process markdown files to add header and section titles
########################################
#%%
import re

def process_markdown_files(header_file, output_file, content_file):
    """
    Process markdown files to:
    1. Get the header from standard_header.md
    2. Extract tags from the first markdown codeblock in output.md
    3. Add the extracted tags below the 'tags:' in the header
    4. Add the header to the beginning of weekly-OFS.md
    5. Extract section titles from the second markdown codeblock of output.md
    6. Locate corresponding sections by numerical indices in weekly-OFS.md
    7. Remove numerical indices and insert extracted section titles
    
    Args:
        header_file (str): Path to the header template file
        output_file (str): Path to the output file with extracted tags and titles
        content_file (str): Path to the content file to be modified
    """
    # 1. Read the header template
    with open(header_file, 'r', encoding='utf-8') as f:
        header_content = f.read()
    
    # 2. Extract tags from the first markdown codeblock in output.md
    with open(output_file, 'r', encoding='utf-8') as f:
        output_content = f.read()
    
    # Find the first markdown codeblock with tags
    tags_match = re.search(r'```markdown\n(.*?)\n```', output_content, re.DOTALL)
    if not tags_match:
        raise Exception("Could not find tags in the output file")
    
    tags_content = tags_match.group(1).strip()
    
    # 3. Add the extracted tags below the 'tags:' in the header
    # Find the position of 'tags:' in the header
    tags_pos = header_content.find('tags:')
    if tags_pos == -1:
        raise Exception("Could not find 'tags:' in the header template")
    
    # Insert the tags after 'tags:'
    new_header = header_content[:tags_pos + 5] + '\n' + tags_content + header_content[tags_pos + 5:]
    
    # 5. Extract section titles from the second markdown codeblock
    titles_match = re.search(r'```markdown\n(.*?)\n```', output_content[tags_match.end():], re.DOTALL)
    if not titles_match:
        raise Exception("Could not find section titles in the output file")
    
    titles_content = titles_match.group(1).strip()
    
    # Parse the titles into a list
    section_titles = []
    for line in titles_content.split('\n'):
        if line.startswith('#'):
            # Extract the title without the leading '#'
            title = line[1:].strip()
            section_titles.append(title)
    
    # 4. Read the content file
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 6. Locate corresponding sections by numerical indices
    # Find all section numbers in the content
    section_pattern = r'^(\d+)\.\s+(.*?)$'
    section_matches = list(re.finditer(section_pattern, content, re.MULTILINE))
    
    # Create a mapping of section numbers to titles
    section_number_to_title = {}
    
    # Match section titles with content sections
    for i, match in enumerate(section_matches):
        section_number = match.group(1)
        section_text = match.group(2)
        
        # If we have a title for this section, use it
        if i < len(section_titles):
            section_number_to_title[section_number] = section_titles[i]
        else:
            # If we don't have a title, keep the original text
            section_number_to_title[section_number] = section_text
    
    # 7. Remove numerical indices and insert extracted section titles
    new_content = content
    for section_number, title in section_number_to_title.items():
        # Replace the section number with the title
        pattern = f'^{section_number}\\.\\s+'
        replacement = f'# {title}\n\n'
        new_content = re.sub(pattern, replacement, new_content, flags=re.MULTILINE)
    
    # Combine the header and the modified content
    final_content = new_header + '\n\n' + new_content
    
    # Write the final content back to the content file
    with open(content_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"Successfully processed markdown files and updated {content_file}")

# Example usage:
process_markdown_files('standard_header.md',
                       output_file, output_md_file)

print("\n" + "="*60)
print("SECTION 8: CLEANING UP FILES")
print("="*60)

# %%
# Move files to scraping folder
scraping_folder = 'scraping'
os.makedirs(scraping_folder, exist_ok=True)

# Get all files in _posts directory
# posts_dir = '_posts'
posts_dir = '.'
for filename in os.listdir(posts_dir):
    # Check if file starts with any of the specified prefixes
    if filename.startswith(('output_', 'scraped_', 'sorted_')):
        source_path = os.path.join(posts_dir, filename)
        dest_path = os.path.join(scraping_folder, filename)
        shutil.move(source_path, dest_path)
        print(f"Moved {filename} to {scraping_folder}")

print("Finished moving files to scraping folder")

print("\n" + "="*60)
print("SCRIPT COMPLETED SUCCESSFULLY!")
print("="*60)
print(f"Final blog post created: {output_md_file}")
print("All temporary files moved to 'scraping' folder")

# %%
input()