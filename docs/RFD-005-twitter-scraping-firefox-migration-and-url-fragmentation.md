# RFD-005: Twitter Scraping Firefox Migration and URL Fragmentation Issues

## Status
**RESOLVED** - 2025-10-06

## Problem Statement

The Twitter scraping script `scrape_thread_from_urls.py` encountered multiple issues requiring migration from Chrome to Firefox and addressing new URL fragmentation patterns introduced by Twitter/X.

### Primary Issues

1. **Browser Detection**: Twitter/X was detecting automated Chrome browsers and preventing login
2. **URL Fragmentation**: Twitter changed their link rendering to split URLs across multiple `<span>` elements
3. **Session Persistence**: Need for persistent login sessions to avoid repeated manual authentication
4. **Content Truncation**: "Show more" buttons hiding complete tweet content

### Symptoms

- **Chrome Detection**: "Could not log in" errors with automated Chrome browser
- **Incomplete URLs**: Scraped links missing "https://" prefix and truncated
- **Fragmented URLs**: URLs split like `"https://"` + `"doi.org/10.1063/5.0291"` + `"590"` + `"…"`
- **Missing Content**: Truncated tweets not expanding to show full content

## Root Cause Analysis

### 1. Browser Detection
Twitter/X enhanced their anti-automation detection specifically targeting Chrome WebDriver characteristics.

### 2. URL Structure Changes
Twitter modified their link rendering from the previous implementation (fixed in RFD-003) to a new fragmented approach:

**Previous Structure** (RFD-003):
- Single `<a>` tag with full URL in attributes
- Truncated visible text but full URL accessible via hover/attributes

**New Structure** (Current):
```html
<a href="https://t.co/redirect">
  <span>https://</span>
  <span>doi.org/10.1063/5.0291</span>
  <span>590</span>
  <span>…</span>
</a>
```

### 3. Content Expansion
Twitter added "Show more" buttons for long tweets, requiring interaction to access full content.

## Solution Implemented

### 1. Firefox Migration
**File**: `_posts/scrape_thread_from_urls.py`

#### Browser Switch
- Changed from `webdriver.Chrome()` to `webdriver.Firefox()`
- Added Firefox-specific anti-detection options

#### Profile Management
```python
# Load profile path from config.json (not tracked in Git)
profile_path = config.get('firefox_profile_path')
if not profile_path:
    print("Error: firefox_profile_path not found in config.json")
    exit(1)
firefox_options.add_argument(f"--profile={profile_path}")
```

#### Anti-Detection Enhancements
```python
# Core stealth options
firefox_options.set_preference("dom.webdriver.enabled", False)
firefox_options.set_preference('useAutomationExtension', False)
firefox_options.set_preference("general.useragent.override", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/115.0")

# Telemetry and tracking prevention
firefox_options.set_preference("toolkit.telemetry.enabled", False)
firefox_options.set_preference("datareporting.healthreport.uploadEnabled", False)

# Network behavior normalization
firefox_options.set_preference("network.http.sendRefererHeader", 2)
firefox_options.set_preference("media.peerconnection.enabled", False)

# Natural window sizing
firefox_options.add_argument("--width=1920")
firefox_options.add_argument("--height=1080")
```

### 2. Show More Button Handling
```python
try:
    show_more_button = tweet_element.find_element(By.CSS_SELECTOR, 'button[data-testid="tweet-text-show-more-link"]')
    if show_more_button.is_displayed():
        driver.execute_script("arguments[0].click();", show_more_button)
        time.sleep(0.5)
except NoSuchElementException:
    pass
```

### 3. URL Reconstruction Logic (Complete Implementation)
Implemented multi-layered URL extraction approach:
```python
# Primary: Direct visible text processing
if visible_text and ('.' in visible_text or visible_text.startswith('http')):
    clean_text = visible_text.replace('\n', '').replace('…', '').strip()
    if clean_text.startswith('http'):
        full_url = clean_text
    elif '.' in clean_text:
        full_url = 'https://' + clean_text

# Secondary: Enhanced hover + tooltip detection
driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", link)
ActionChains(driver).move_to_element(link).perform()

# Tertiary: Smart pattern-based fallbacks
if clean_visible.startswith(('doi.org/', 'arxiv.org/', 'github.com/')):
    full_url = 'https://' + clean_visible
```

### 4. File-based URL Loading
Added option to load URLs from existing files without bulk tab opening:
```python
# Load URLs from file without opening all tabs
with open(url_file_path, 'r') as f:
    file_urls = [line.strip() for line in f if line.strip()]

# Navigate to homepage only, scrape URLs one by one
driver.get("https://x.com")
```

## Current Status

### ✅ Resolved Issues
1. **Firefox Migration**: Successfully switched to Firefox with persistent profile
2. **Session Persistence**: Login session now persists between script runs
3. **Show More Expansion**: Successfully detecting and clicking "Show more" buttons
4. **Anti-Detection**: Enhanced stealth options implemented
5. **URL Reconstruction**: Fixed incomplete URL extraction through multi-layered approach
6. **Profile Path Security**: Moved Firefox profile path to config.json (not tracked in Git)
7. **Automation Detection**: Added file-based URL loading to avoid bulk tab opening

### ✅ URL Extraction Solution
The URL fragmentation issue was resolved through a comprehensive multi-layered approach:

1. **Primary Method**: Direct visible text processing with protocol addition
2. **Viewport Fix**: Scroll elements into view before hover to prevent out-of-bounds errors
3. **Enhanced Tooltips**: Improved tooltip detection with multiple selectors and timing
4. **Smart Fallbacks**: Pattern-based URL completion for common domains (doi.org, arxiv.org, etc.)
5. **JavaScript Extraction**: Final fallback using browser JavaScript execution

### ✅ Automation Detection Mitigation
- **File-based URL Loading**: Load URLs from existing files without opening all tabs
- **Natural Navigation**: Start at homepage, login manually, then scrape one-by-one
- **Reduced Bulk Operations**: Eliminated simultaneous tab opening patterns

### Evidence of Resolution
Testing confirmed successful URL extraction with complete URLs including proper "https://" prefixes and full paths, resolving the truncation issues documented in previous scrapes.

## Technical Details

### Files Modified
- `_posts/scrape_thread_from_urls.py`:
  - Firefox migration with config-based profile path
  - Show more button handling
  - Multi-layered URL reconstruction logic
  - File-based URL loading option
  - Enhanced anti-detection measures
- `_posts/config.json`:
  - Added `firefox_profile_path` configuration
  - Properly excluded from Git tracking via `.gitignore`

### Dependencies
- Firefox browser and GeckoDriver
- Existing Firefox profile with Twitter login

### Key Features
- **Persistent Authentication**: Session persistence with Firefox profile
- **Content Expansion**: Automatic "Show more" button clicking
- **Enhanced Stealth**: Multiple anti-detection layers including natural navigation
- **Secure Configuration**: Profile path stored in ignored config.json
- **Flexible URL Loading**: Support for both manual and file-based URL collection
- **Robust URL Extraction**: Multi-layered approach handling Twitter's fragmentation
- **Automation Detection Avoidance**: One-by-one URL processing instead of bulk operations

## Related Issues

This RFD builds upon RFD-003 which addressed the previous Twitter link extraction changes. The current issue represents Twitter's continued evolution of anti-scraping measures through DOM structure modifications.
