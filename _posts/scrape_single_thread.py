#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

# Script to scrape a single long Twitter/X thread
#
# OVERVIEW:
# This script scrapes a single Twitter/X thread by opening Firefox with an existing
# user profile, navigating to the thread, and automatically scrolling to load and
# extract all tweets from a specified user handle.
#
# KEY FEATURES:
# - Bidirectional scrolling: Scrolls UP first to load earlier tweets, then DOWN to load later tweets
# - Handles very long threads that Twitter collapses by default
# - Incremental scrolling: Scrolls one viewport height at a time instead of jumping to extremes
# - Duplicate detection: Tracks already-processed tweets to avoid re-scraping
# - URL expansion: Attempts to expand truncated URLs in tweets using multiple fallback methods
# - Media download: Downloads images and organizes them in date-stamped folders
# - LLM tag extraction: Uses DeepSeek API to automatically generate relevant tags
# - Markdown generation: Creates formatted blog post with timestamps and embedded images
#
# KNOWN ISSUES AND FIXES:
# 1. Issue: Twitter collapses very long threads, hiding many tweets
#    Fix: User can start from any position in the thread (including bottom after manual expansion)
#         Script then scrolls bidirectionally to capture all content
#
# 2. Issue: Initial implementation only scraped visible tweets without scrolling
#    Fix: Implemented continuous scrolling loop with DOM update detection
#
# 3. Issue: Jumping to document.body.scrollHeight skipped collapsed content
#    Fix: Changed to incremental scrolling by viewport height (window.innerHeight)
#
# 4. Issue: Starting from thread top didn't work for collapsed threads
#    Fix: Allow starting from any position, scroll up first, then down
#
# 5. Issue: Needed to detect when no new content is loading
#    Fix: Track scroll position/height changes, stop after 3 consecutive scrolls with no change
#
# USAGE:
# 1. Ensure config.json contains firefox_profile_path, api_url, and api_key
# 2. Run script and navigate to the thread in the opened browser
# 3. For very long threads, manually scroll down to expand collapsed sections if needed
# 4. Press ENTER to start automatic scraping
# 5. Script will scroll and scrape automatically, then generate markdown output
#
# OUTPUT FILES:
# - YYYY-MM-DD-single-thread.md: Final blog post with header and tags
# - scraped_single_thread_YYYYMMDD.json: Raw scraped data (moved to scraping/ folder)
# - output_tags_YYYYMMDD.md: LLM-generated tags (moved to scraping/ folder)
# - /assets/images/2025/YYYYMMDD_YYYYMMDD_long_thread/: Downloaded images

import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options
import time
import json
import re
from datetime import datetime

print("="*60)
print("TWITTER SINGLE THREAD SCRAPING SCRIPT STARTED")
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

                # APPROACH 1: Try to get URL from visible text first
                full_url = None

                # If visible text looks like a URL, try to reconstruct it
                if visible_text and ('.' in visible_text or visible_text.startswith('http')):
                    # Clean up the visible text and try to make it a complete URL
                    clean_text = visible_text.replace('\n', '').replace('…', '').replace('...', '').strip()
                    if clean_text:
                        if clean_text.startswith('http'):
                            full_url = clean_text
                            print(f"Using visible text as URL: '{full_url}'")
                        elif '.' in clean_text and not clean_text.startswith('.'):
                            full_url = 'https://' + clean_text
                            print(f"Added https:// to visible text: '{full_url}'")

                # APPROACH 2: Try span reconstruction (keeping for debugging)
                try:
                    spans = link.find_elements(By.TAG_NAME, 'span')
                    if spans:
                        print(f"Found {len(spans)} spans in link")
                        url_parts = []
                        for j, span in enumerate(spans):
                            span_text = span.text
                            print(f"  Span {j+1}: '{span_text}'")
                            if span_text and span_text not in ['…', '...']:
                                url_parts.append(span_text)
                            elif span_text in ['…', '...']:
                                print(f"  Found ellipsis span, URL is truncated")
                                break

                        if url_parts and not full_url:
                            reconstructed_url = ''.join(url_parts)
                            print(f"Reconstructed URL from spans: '{reconstructed_url}'")
                            if reconstructed_url.startswith('http'):
                                full_url = reconstructed_url
                            elif '.' in reconstructed_url:
                                full_url = 'https://' + reconstructed_url
                                print(f"Added https:// prefix: '{full_url}'")
                except Exception as span_error:
                    print(f"Error reconstructing URL from spans: {str(span_error)}")

                # Fallback: Try to get the full URL from various attributes
                if not full_url:
                    for attr in ['data-expanded-url', 'title', 'aria-label', 'data-url', 'data-original-url']:
                        full_url = link.get_attribute(attr)
                        if full_url and full_url.startswith('http') and not full_url.startswith('https://t.co'):
                            break

                # If we still don't have a full URL or it's incomplete, try more aggressive methods
                if not full_url or full_url.startswith('https://t.co') or (full_url and ('…' in visible_text or len(visible_text) > len(full_url))):
                    print(f"Trying hover and tooltip methods for incomplete URL: '{full_url}'")
                    try:
                        # Scroll element into view first to avoid viewport issues
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
                        time.sleep(0.5)

                        # Hover over the link to potentially trigger tooltip with full URL
                        ActionChains(driver).move_to_element(link).perform()
                        time.sleep(1.0)  # Wait longer for tooltip to appear

                        # Check for tooltip or updated attributes after hover
                        for attr in ['title', 'aria-label', 'data-expanded-url', 'data-full-url', 'data-href']:
                            hover_url = link.get_attribute(attr)
                            if hover_url and hover_url.startswith('http') and not hover_url.startswith('https://t.co'):
                                print(f"Found full URL in {attr}: '{hover_url}'")
                                full_url = hover_url
                                break

                        # Also check if there's a tooltip element that appeared
                        try:
                            # Wait a bit more for tooltip to appear
                            time.sleep(0.5)

                            tooltip_selectors = [
                                '[role="tooltip"]',
                                '.tooltip',
                                '[data-testid*="tooltip"]',
                                '[aria-describedby]',
                                '.r-1loqt21',  # Twitter-specific tooltip class
                                '[data-testid="HoverCard"]',
                                '[data-testid="card.wrapper"]',
                                '.css-1dbjc4n[role="tooltip"]',
                                'div[style*="position: absolute"]'  # Generic positioned tooltip
                            ]

                            for selector in tooltip_selectors:
                                tooltip_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                                for tooltip in tooltip_elements:
                                    if tooltip.is_displayed():  # Only check visible tooltips
                                        tooltip_text = tooltip.text.strip()
                                        if tooltip_text and tooltip_text.startswith('http') and not tooltip_text.startswith('https://t.co'):
                                            print(f"Found full URL in tooltip ({selector}): '{tooltip_text}'")
                                            full_url = tooltip_text
                                            break
                                        # Also check tooltip attributes
                                        for attr in ['title', 'aria-label', 'data-url']:
                                            attr_value = tooltip.get_attribute(attr)
                                            if attr_value and attr_value.startswith('http') and not attr_value.startswith('https://t.co'):
                                                print(f"Found full URL in tooltip {attr}: '{attr_value}'")
                                                full_url = attr_value
                                                break
                                if full_url and not full_url.startswith('https://t.co'):
                                    break
                        except Exception as tooltip_error:
                            print(f"Error checking tooltips: {str(tooltip_error)}")

                    except Exception as hover_error:
                        print(f"Error during hover: {str(hover_error)}")
                        pass

                # Final fallback: try to use JavaScript and smart text parsing
                if not full_url or full_url.startswith('https://t.co'):
                    # Try smart parsing of visible text as last resort
                    if visible_text and not full_url:
                        # Remove ellipsis and clean up
                        clean_visible = visible_text.replace('…', '').replace('...', '').replace('\n', '').strip()
                        if clean_visible and '.' in clean_visible:
                            # Try to guess common URL patterns
                            if clean_visible.startswith(('doi.org/', 'arxiv.org/', 'github.com/', 'youtube.com/')):
                                full_url = 'https://' + clean_visible
                                print(f"Smart fallback - guessed URL: '{full_url}'")
                            elif clean_visible.startswith(('www.')):
                                full_url = 'https://' + clean_visible
                                print(f"Smart fallback - added https to www: '{full_url}'")
                            elif '/' in clean_visible and not clean_visible.startswith('http'):
                                # Looks like a path, try adding https://
                                full_url = 'https://' + clean_visible
                                print(f"Smart fallback - added https to path: '{full_url}'")

                    # Try JavaScript as final attempt
                    if not full_url or full_url.startswith('https://t.co'):
                        try:
                            js_url = driver.execute_script("""
                                var link = arguments[0];
                                // Try to get the actual destination URL
                                if (link.href && !link.href.includes('t.co')) {
                                    return link.href;
                                }
                                // Try to get from data attributes
                                var attrs = ['data-expanded-url', 'data-full-url', 'data-href', 'title'];
                                for (var i = 0; i < attrs.length; i++) {
                                    var url = link.getAttribute(attrs[i]);
                                    if (url && url.startsWith('http') && !url.includes('t.co')) {
                                        return url;
                                    }
                                }
                                return null;
                            """, link)

                            if js_url and js_url.startswith('http') and not js_url.startswith('https://t.co'):
                                print(f"Found full URL via JavaScript: '{js_url}'")
                                full_url = js_url
                        except Exception as js_error:
                            print(f"Error getting URL via JavaScript: {str(js_error)}")

                # If we found a full URL and it's different from the visible text, replace it
                if full_url and visible_text:
                    # Check if we should replace the visible text with the full URL
                    should_replace = False

                    # Case 1: Visible text is clearly truncated (ends with ellipsis)
                    if visible_text.endswith('…') or visible_text.endswith('...'):
                        should_replace = True
                        print(f"URL is truncated (ellipsis): '{visible_text}'")

                    # Case 2: Full URL is significantly longer than visible text
                    elif len(full_url) > len(visible_text) + 10:  # Allow some tolerance
                        should_replace = True
                        print(f"Full URL is much longer: visible={len(visible_text)}, full={len(full_url)}")

                    # Case 3: Visible text doesn't start with http but full URL does
                    elif not visible_text.startswith('http') and full_url.startswith('http'):
                        should_replace = True
                        print(f"Adding missing protocol: '{visible_text}' -> '{full_url}'")

                    # Case 4: Visible text is a subset of the full URL
                    elif visible_text in full_url and len(visible_text) < len(full_url):
                        should_replace = True
                        print(f"Visible text is subset of full URL")

                    if should_replace and visible_text in tweet_text:
                        tweet_text = tweet_text.replace(visible_text, full_url)
                        print(f"✓ Replaced URL: '{visible_text}' -> '{full_url}'")
                    elif full_url:
                        print(f"ℹ Full URL found but not replacing: '{visible_text}' (full: '{full_url}')")

        except Exception as e:
            print(f"Error processing links in tweet: {str(e)}")

        # Clean up line breaks in the final tweet text to fix broken markdown links
        tweet_text = re.sub(r'\s*\n\s*', ' ', tweet_text).strip()
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

def scrape_single_thread(driver, url, media_folder, str_user_handle):
    """
    Scrape a single thread by scrolling up first (to load earlier tweets),
    then down (to load later tweets).
    Terminates based on actual scraped tweet content comparison.
    """
    print(f"Scraping thread: {url}")

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'article[data-testid="tweet"]'))
        )
    except TimeoutException:
        print(f"Timeout waiting for tweet to load: {url}")
        return None

    thread_data = {'url': url, 'tweets': []}

    # Helper function to get unique identifier for a tweet
    def get_tweet_id(tweet_data):
        """Create a unique identifier from tweet timestamp and text"""
        return f"{tweet_data.get('timestamp', '')}:{tweet_data.get('text', '')[:100]}"

    # PHASE 1: Scroll UP to load earlier tweets in the thread
    print("\nPhase 1: Scrolling UP to load earlier tweets...")
    no_new_content_count = 0
    last_tweet_set = set()  # Track unique tweets from last iteration

    while no_new_content_count < 5:  # Stop after 5 consecutive scrolls with no new content
        # Process currently visible tweets
        tweets = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
        user_tweets = []
        for tweet in tweets:
            try:
                if str_user_handle.lower() in tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Name"]').text.lower():
                    user_tweets.append(tweet)
            except StaleElementReferenceException:
                continue

        current_iteration_tweets = []

        for tweet in user_tweets:
            try:
                if tweet in [t['element'] for t in thread_data['tweets']]:
                    continue

                try:
                    time_element = tweet.find_element(By.CSS_SELECTOR, 'time')
                    timestamp = time_element.get_attribute('datetime')
                    tweet_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    tweet_timestamp = tweet_date.isoformat()
                except NoSuchElementException:
                    tweet_timestamp = ''
                    tweet_date = None

                tweet_data = scrape_tweet(driver, tweet, media_folder, tweet_date)
                tweet_data['timestamp'] = tweet_timestamp
                tweet_data['element'] = tweet
                thread_data['tweets'].append(tweet_data)
                current_iteration_tweets.append(tweet_data)
                print(f"Scraped tweet {len(thread_data['tweets'])} from {str_user_handle}")
            except StaleElementReferenceException:
                continue

        # Create set of unique identifiers for tweets found in this iteration
        current_tweet_set = {get_tweet_id(t) for t in current_iteration_tweets}

        # Check if we found any new content compared to last iteration
        if current_tweet_set and current_tweet_set == last_tweet_set:
            no_new_content_count += 1
            print(f"No new content found - same tweets as last iteration (attempt {no_new_content_count}/5)")
        elif not current_iteration_tweets:
            no_new_content_count += 1
            print(f"No new tweets found in this iteration (attempt {no_new_content_count}/5)")
        else:
            no_new_content_count = 0
            print(f"Found {len(current_iteration_tweets)} new tweets in this iteration")

        last_tweet_set = current_tweet_set

        # Scroll up by one viewport height
        driver.execute_script("window.scrollBy(0, -window.innerHeight);")
        time.sleep(2.0)  # Increased wait time for content to load

        # Check if we've reached the top
        new_position = driver.execute_script("return window.pageYOffset;")
        if new_position == 0:
            print("Reached the top of the page")
            break

    # PHASE 2: Scroll DOWN to load later tweets in the thread
    print("\nPhase 2: Scrolling DOWN to load later tweets...")
    no_new_content_count = 0
    last_tweet_set = set()  # Reset for Phase 2

    while no_new_content_count < 5:  # Stop after 5 consecutive scrolls with no new content
        # Process currently visible tweets
        tweets = driver.find_elements(By.CSS_SELECTOR, 'article[data-testid="tweet"]')
        user_tweets = []
        for tweet in tweets:
            try:
                if str_user_handle.lower() in tweet.find_element(By.CSS_SELECTOR, 'div[data-testid="User-Name"]').text.lower():
                    user_tweets.append(tweet)
            except StaleElementReferenceException:
                continue

        current_iteration_tweets = []

        for tweet in user_tweets:
            try:
                if tweet in [t['element'] for t in thread_data['tweets']]:
                    continue

                try:
                    time_element = tweet.find_element(By.CSS_SELECTOR, 'time')
                    timestamp = time_element.get_attribute('datetime')
                    tweet_date = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    tweet_timestamp = tweet_date.isoformat()
                except NoSuchElementException:
                    tweet_timestamp = ''
                    tweet_date = None

                tweet_data = scrape_tweet(driver, tweet, media_folder, tweet_date)
                tweet_data['timestamp'] = tweet_timestamp
                tweet_data['element'] = tweet
                thread_data['tweets'].append(tweet_data)
                current_iteration_tweets.append(tweet_data)
                print(f"Scraped tweet {len(thread_data['tweets'])} from {str_user_handle}")
            except StaleElementReferenceException:
                continue

        # Create set of unique identifiers for tweets found in this iteration
        current_tweet_set = {get_tweet_id(t) for t in current_iteration_tweets}

        # Check if we found any new content compared to last iteration
        if current_tweet_set and current_tweet_set == last_tweet_set:
            no_new_content_count += 1
            print(f"No new content found - same tweets as last iteration (attempt {no_new_content_count}/5)")
        elif not current_iteration_tweets:
            no_new_content_count += 1
            print(f"No new tweets found in this iteration (attempt {no_new_content_count}/5)")
        else:
            no_new_content_count = 0
            print(f"Found {len(current_iteration_tweets)} new tweets in this iteration")

        last_tweet_set = current_tweet_set

        # Scroll down by one viewport height (incremental scrolling)
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(2.0)  # Increased wait time for content to load

    print(f"\nScraping complete. Total tweets scraped: {len(thread_data['tweets'])}")

    # Remove the 'element' key from tweet data before returning
    for tweet in thread_data['tweets']:
        del tweet['element']

    return thread_data


print("\n" + "="*60)
print("SECTION 1: BROWSER SETUP AND LOGIN")
print("="*60)

# Firefox options to help avoid detection
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

print("\n" + "="*60)
print("SECTION 2: MANUAL THREAD LOADING")
print("="*60)

print("\nPlease:")
print("1. Navigate to the Twitter/X thread you want to scrape")
print("   - You can start anywhere in the thread (top, middle, or bottom)")
print("   - For very long threads, you may want to scroll down first to expand collapsed sections")
print("2. Press ENTER when ready to start scraping...")
print("   (The script will scroll UP first to load earlier tweets, then DOWN to load later tweets)")
input()

# Get the current URL
thread_url = driver.current_url
print(f"Thread URL: {thread_url}")

# Ask for user handle to filter tweets
str_user_handle = input("Enter the user handle to filter tweets (default: @jwt0625): ").strip()
if not str_user_handle:
    str_user_handle = '@jwt0625'
elif not str_user_handle.startswith('@'):
    str_user_handle = '@' + str_user_handle

print("\n" + "="*60)
print("SECTION 3: SCRAPING THREAD")
print("="*60)

# Setup
# Note: All file writes use 'w' mode which automatically overwrites existing files
media_folder = 'media'
os.makedirs(media_folder, exist_ok=True)

# Scrape the thread
thread_data = scrape_single_thread(driver, thread_url, media_folder, str_user_handle)

if thread_data:
    # Save to JSON file
    current_date = datetime.now().strftime("%Y%m%d")
    json_filename = f'scraped_single_thread_{current_date}.json'
    with open(json_filename, 'w', encoding='utf-8') as f:
        json.dump([thread_data], f, ensure_ascii=False, indent=4)

    print(f"Scraped {len(thread_data['tweets'])} tweets.")
    print(f"Data saved to: {json_filename}")
else:
    print("Failed to scrape thread.")
    exit(1)

print("\n" + "="*60)
print("SECTION 4: ORGANIZING MEDIA FILES")
print("="*60)

import shutil

# Move JPG files to a new folder based on date range
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

    # Create a new folder name based on the date range with "long_thread" suffix
    folder_name = f"{min_date}_{max_date}_long_thread"

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
    folder_name = None

print("\n" + "="*60)
print("SECTION 6: CREATING MARKDOWN FROM JSON")
print("="*60)

def format_media(media_item, media_folder):
    file_name = os.path.basename(media_item['local_path'])
    new_path = f"/assets/images/2025/{media_folder}/{file_name}"
    return f"![{file_name}]({new_path})"

def create_markdown_single_thread(json_file, output_file, media_folder):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open(output_file, 'w', encoding='utf-8') as f:
        # For a single thread, we just list all tweets sequentially
        thread = data[0]  # Only one thread

        for i, tweet in enumerate(thread['tweets'], 1):
            # Format the timestamp if available
            timestamp_str = ""
            if tweet.get('timestamp'):
                try:
                    tweet_dt = datetime.fromisoformat(tweet['timestamp'])
                    timestamp_str = f" ({tweet_dt.strftime('%Y-%m-%d %H:%M:%S')})"
                except:
                    pass

            f.write(f"{i}.{timestamp_str} {tweet['text']}\n")

            # Media for this tweet
            for media in tweet['media']:
                f.write(format_media(media, media_folder) + "\n")

            f.write("\n")  # Add a blank line between tweets

# Generate markdown
output_md_file = f"{datetime.now().strftime('%Y-%m-%d')}-single-thread.md"
create_markdown_single_thread(json_filename, output_md_file, folder_name)
print(f"Markdown file '{output_md_file}' has been created.")

print("\n" + "="*60)
print("SECTION 6: EXTRACTING TAGS USING LLM")
print("="*60)

# Embedded prompt for tag extraction only
TAG_EXTRACTION_PROMPT = """I will give you a long post and ask you to extract tags from it. I will also give you list of example tags from past posts.

Here are some example tags. Please note that these are just examples for style guidelines. Extract your own proper tags from the actual content of the blog.

  - PCSEL
  - Nanotube
  - Lens
  - Optics
  - Flexure
  - RSA
  - Microwave
  - Optical_switch
  - MEMS
  - Photonics
  - Capacitor
  - OCR
  - WGM
  - Taper
  - Neutrino
  - Calorimeter
  - Acoustics
  - NIST
  - Egocentric_video
  - Inverse_design
  - Quantum_computing
  - Ultrasonic
  - Ultrasonic_imaging
  - Leidenfrost
  - Superconducting_circuits
  - Waveguide
  - Semiconductor
  - WFE
  - Applied_materials
  - ASML
  - Photoacoustic
  - LIDAR
  - Frequency_comb
  - Satellite_gravimetry
  - EDFA
  - EDWA
  - Annealing
  - ALD
  - ALE
  - Quantum
  - NIF
  - Fusion
  - Plasma
  - CT
  - Antenna
  - Atom
  - Scattering
  - RCS
  - Laser
  - Superconducting_qubit
  - COMSOL
  - Google
  - IBM
  - LED
  - Quantum_dot
  - Piezo
  - Magnetorquer
  - VCSEL
  - Facebook
  - Qubit
  - Wood
  - Satellite
  - AFM
  - Membrane
  - Optomechanics
  - Entanglement
  - BellLab
  - Blender
  - ComputerVision
  - DNN
  - MATLAB
  - PCB
  - FailureAnalysis
  - Camera
  - Microscopy
  - Robotics
  - Prosthetic
  - Electronics
  - Optimization
  - RL
  - Sensor
  - Sensing
  - Noise
  - Blackhole
  - ifixit
  - R2R
  - NIL
  - Stycast
  - Cryogenics
  - Humanoid
  - Self-driving
  - Nanosphere
  - Plutonium
  - DNA
  - CNN
  - IoT

Make the list of tags more compact: deduplicate and merge similar words. Omit common ones such as compute_trends. Only keep highly technical ones. Keep the total number of tags to be less than 30.

Generate them as markdown in a code block. DO NOT include anything else in the markdown code block."""

# Use LLM to extract tags
from helpers_LLM import process_with_llm_from_files

# Create a temporary prompt file
temp_prompt_file = 'temp_prompt_tags.md'
with open(temp_prompt_file, 'w', encoding='utf-8') as f:
    f.write(TAG_EXTRACTION_PROMPT)

output_tags_file = f"output_tags_{datetime.now().strftime('%Y%m%d')}.md"
try:
    res = process_with_llm_from_files(config_file='config.json',
                                      prompt_file=temp_prompt_file,
                                      content_file=output_md_file,
                                      output_file=output_tags_file)
    print(f"LLM tag extraction completed. Output saved to: {output_tags_file}")
except Exception as e:
    print(f"Error during LLM processing: {e}")
    print("Continuing without LLM-generated tags...")
    output_tags_file = None

# Clean up temp prompt file
if os.path.exists(temp_prompt_file):
    os.remove(temp_prompt_file)

print("\n" + "="*60)
print("SECTION 7: ADDING HEADER TO MARKDOWN")
print("="*60)

def add_header_to_markdown(header_file, tags_file, content_file, media_folder):
    """Add header to markdown file with extracted tags"""
    # Read the header template
    with open(header_file, 'r', encoding='utf-8') as f:
        header_content = f.read()

    # Extract tags if available
    tags_content = ""
    if tags_file and os.path.exists(tags_file):
        with open(tags_file, 'r', encoding='utf-8') as f:
            tags_output = f.read()

        # Find the markdown codeblock with tags
        tags_match = re.search(r'```markdown\n(.*?)\n```', tags_output, re.DOTALL)
        if tags_match:
            tags_content = tags_match.group(1).strip()

    # Add the extracted tags below the 'tags:' in the header
    tags_pos = header_content.find('tags:')
    if tags_pos != -1 and tags_content:
        new_header = header_content[:tags_pos + 5] + '\n' + tags_content + header_content[tags_pos + 5:]
    else:
        new_header = header_content

    # Update the cover and overlay_image paths with the media folder
    if media_folder:
        new_header = new_header.replace('/assets/images/2025/', f'/assets/images/2025/{media_folder}/')

    # Read the content file
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Combine the header and the content
    final_content = new_header + '\n\n' + content

    # Write the final content back to the content file
    with open(content_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Successfully added header to {content_file}")

# Add header to markdown
add_header_to_markdown('standard_header.md', output_tags_file, output_md_file, folder_name)

print("\n" + "="*60)
print("SECTION 8: CLEANING UP FILES")
print("="*60)

# Move files to scraping folder
scraping_folder = 'scraping'
os.makedirs(scraping_folder, exist_ok=True)

# Get all files in current directory
posts_dir = '.'
for filename in os.listdir(posts_dir):
    # Check if file starts with any of the specified prefixes
    if filename.startswith(('output_tags_', 'scraped_single_thread_', 'temp_')):
        source_path = os.path.join(posts_dir, filename)
        dest_path = os.path.join(scraping_folder, filename)
        if os.path.isfile(source_path):
            shutil.move(source_path, dest_path)
            print(f"Moved {filename} to {scraping_folder}")

print("Finished moving files to scraping folder")

print("\n" + "="*60)
print("SCRIPT COMPLETED SUCCESSFULLY!")
print("="*60)
print(f"Final blog post created: {output_md_file}")
print("All temporary files moved to 'scraping' folder")

# Keep browser open for user inspection
print("\nBrowser will remain open. Close it manually when done.")
input("Press ENTER to exit the script...")

# Use LLM to extract tags
from helpers_LLM import process_with_llm_from_files

# Create a temporary prompt file
temp_prompt_file = 'temp_prompt_tags.md'
with open(temp_prompt_file, 'w', encoding='utf-8') as f:
    f.write(TAG_EXTRACTION_PROMPT)

output_tags_file = f"output_tags_{datetime.now().strftime('%Y%m%d')}.md"
try:
    res = process_with_llm_from_files(config_file='config.json',
                                      prompt_file=temp_prompt_file,
                                      content_file=output_md_file,
                                      output_file=output_tags_file)
    print(f"LLM tag extraction completed. Output saved to: {output_tags_file}")
except Exception as e:
    print(f"Error during LLM processing: {e}")
    print("Continuing without LLM-generated tags...")
    output_tags_file = None

# Clean up temp prompt file
if os.path.exists(temp_prompt_file):
    os.remove(temp_prompt_file)

print("\n" + "="*60)
print("SECTION 7: ADDING HEADER TO MARKDOWN")
print("="*60)

def add_header_to_markdown(header_file, tags_file, content_file, media_folder):
    """
    Add header to markdown file with extracted tags

    Args:
        header_file (str): Path to the header template file
        tags_file (str): Path to the file with extracted tags (can be None)
        content_file (str): Path to the content file to be modified
        media_folder (str): Name of the media folder for images
    """
    # 1. Read the header template
    with open(header_file, 'r', encoding='utf-8') as f:
        header_content = f.read()

    # 2. Extract tags if available
    tags_content = ""
    if tags_file and os.path.exists(tags_file):
        with open(tags_file, 'r', encoding='utf-8') as f:
            tags_output = f.read()

        # Find the markdown codeblock with tags
        tags_match = re.search(r'```markdown\n(.*?)\n```', tags_output, re.DOTALL)
        if tags_match:
            tags_content = tags_match.group(1).strip()

    # 3. Add the extracted tags below the 'tags:' in the header
    tags_pos = header_content.find('tags:')
    if tags_pos != -1 and tags_content:
        new_header = header_content[:tags_pos + 5] + '\n' + tags_content + header_content[tags_pos + 5:]
    else:
        new_header = header_content

    # 4. Update the cover and overlay_image paths with the media folder
    if media_folder:
        new_header = new_header.replace('/assets/images/2025/', f'/assets/images/2025/{media_folder}/')

    # 5. Read the content file
    with open(content_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 6. Combine the header and the content
    final_content = new_header + '\n\n' + content

    # 7. Write the final content back to the content file
    with open(content_file, 'w', encoding='utf-8') as f:
        f.write(final_content)

    print(f"Successfully added header to {content_file}")

# Add header to markdown
add_header_to_markdown('standard_header.md', output_tags_file, output_md_file, folder_name)

print("\n" + "="*60)
print("SECTION 8: CLEANING UP FILES")
print("="*60)

# Move files to scraping folder
scraping_folder = 'scraping'
os.makedirs(scraping_folder, exist_ok=True)

# Get all files in current directory
posts_dir = '.'
for filename in os.listdir(posts_dir):
    # Check if file starts with any of the specified prefixes
    if filename.startswith(('output_tags_', 'scraped_single_thread_', 'temp_')):
        source_path = os.path.join(posts_dir, filename)
        dest_path = os.path.join(scraping_folder, filename)
        if os.path.isfile(source_path):
            shutil.move(source_path, dest_path)
            print(f"Moved {filename} to {scraping_folder}")

print("Finished moving files to scraping folder")

print("\n" + "="*60)
print("SCRIPT COMPLETED SUCCESSFULLY!")
print("="*60)
print(f"Final blog post created: {output_md_file}")
print("All temporary files moved to 'scraping' folder")
print("\nNote: You mentioned you'll update the filename manually.")
print("Don't forget to update the title in the header as well!")

# Keep browser open for user inspection
print("\nBrowser will remain open. Close it manually when done.")
input("Press ENTER to exit the script...")

