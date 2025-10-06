# RFD-005: Twitter Scraping Firefox Migration and URL Fragmentation Issues

## Status
**IN PROGRESS** - 2025-10-06

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
profile_path = config.get('firefox_profile_path')
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

### 3. URL Reconstruction Logic (Partial Implementation)
Added span-based URL reconstruction approach:
```python
spans = link.find_elements(By.TAG_NAME, 'span')
url_parts = []
for span in spans:
    span_text = span.text
    if span_text and span_text not in ['…', '...']:
        url_parts.append(span_text)

reconstructed_url = ''.join(url_parts)
```

## Current Status

### ✅ Resolved Issues
1. **Firefox Migration**: Successfully switched to Firefox with persistent profile
2. **Session Persistence**: Login session now persists between script runs
3. **Show More Expansion**: Successfully detecting and clicking "Show more" buttons
4. **Anti-Detection**: Enhanced stealth options implemented

### ❌ Outstanding Issues
1. **URL Reconstruction**: Current implementation still produces incomplete URLs
   - Missing "https://" prefix in final output
   - URLs still truncated (e.g., `doi.org/10.1063/5.0291…`)
2. **Span Concatenation**: Logic needs refinement for proper URL assembly

### Evidence from Latest Scrape
From `2025-10-05-weekly-OFS-67.md`:
- Line 49-50: `doi.org/10.1063/5.0291…` (should be `https://doi.org/10.1063/5.0291590`)
- Line 60-61: `x-celeprint.com/cms/wp-content…` (missing https:// and truncated)
- Line 71-72: `pubs.acs.org/doi/10.1021/ac…` (missing https:// and truncated)

## Next Steps

1. **Debug URL Reconstruction**: Investigate why span concatenation isn't producing complete URLs
2. **Protocol Prefix**: Ensure "https://" is properly added to reconstructed URLs
3. **Truncation Handling**: Address remaining truncation issues in URL assembly
4. **Testing**: Validate fixes against current Twitter/X structure

## Technical Details

### Files Modified
- `_posts/scrape_thread_from_urls.py`: 
  - Firefox migration (lines 235-265)
  - Show more button handling (lines 39-52)
  - URL reconstruction enhancement (lines 59-80)

### Dependencies
- Firefox browser and GeckoDriver
- Existing Firefox profile with Twitter login

### Key Features
- **Persistent Authentication**: No manual login required
- **Content Expansion**: Automatic "Show more" button clicking
- **Enhanced Stealth**: Multiple anti-detection layers
- **Profile Isolation**: Uses dedicated Firefox profile path

## Related Issues

This RFD builds upon RFD-003 which addressed the previous Twitter link extraction changes. The current issue represents Twitter's continued evolution of anti-scraping measures through DOM structure modifications.
