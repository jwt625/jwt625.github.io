# RFD-003: Twitter/X Link Extraction Bug and Fix

## Status
**RESOLVED** - 2025-09-08

## Problem Statement

The Twitter scraping script `scrape_thread_from_urls.py` stopped extracting full URLs from tweets, instead capturing only truncated versions. This issue emerged around early September 2025 despite no changes to the script itself.

### Symptoms
- **Expected behavior**: Full URLs like `https://pubs.acs.org/doi/10.1021/acsphotonics.5c00429`
- **Actual behavior**: Truncated URLs like `pubs.acs.org/doi/10.1021/ac…)`
- **Manual workaround**: Selecting and copying truncated links still yielded full URLs
- **Timeline**: Script worked correctly until approximately one week before 2025-09-08

### Root Cause Analysis

Twitter/X made frontend changes to their link handling mechanism:

1. **Previous implementation**: Full URLs were accessible via `.text` property in Selenium
2. **New implementation**: 
   - Visible text shows truncated URLs (what `.text` captures)
   - Full URLs only stored in `href` attributes (containing t.co redirects) or data attributes
   - Full URLs revealed through JavaScript hover events or tooltip mechanisms

The script's reliance on `element.text` became insufficient when Twitter separated visual presentation from actual URL data.

## Solution Implemented

Enhanced the `scrape_tweet()` function with a multi-layered URL extraction approach:

### 1. Data Attribute Extraction
```python
for attr in ['data-expanded-url', 'title', 'aria-label', 'data-url', 'data-original-url']:
    full_url = link.get_attribute(attr)
    if full_url and full_url.startswith('http') and not full_url.startswith('https://t.co'):
        break
```

### 2. Hover-Triggered URL Resolution
```python
ActionChains(driver).move_to_element(link).perform()
time.sleep(0.5)  # Wait for tooltip to appear
```

### 3. Tooltip Detection
```python
tooltip_elements = driver.find_elements(By.CSS_SELECTOR, '[role="tooltip"], .tooltip, [data-testid*="tooltip"]')
```

### 4. HTML Content Parsing
```python
url_pattern = r'https?://(?!t\.co)[^\s<>"\']+[^\s<>"\'.,;!?]'
urls_in_html = re.findall(url_pattern, inner_html)
```

### 5. Smart Text Replacement
- Only replaces obviously truncated text (ending with "…" or "...")
- Preserves original tweet structure
- Avoids t.co redirect URLs

## Technical Details

### Files Modified
- `_posts/scrape_thread_from_urls.py`: Enhanced `scrape_tweet()` function (lines 37-121)

### Dependencies Added
- `selenium.webdriver.common.action_chains.ActionChains` for hover simulation

### Key Features
- **Non-destructive**: Only replaces truncated URLs
- **Multiple fallbacks**: Tries several extraction methods in sequence
- **Debug logging**: Tracks URL extraction process
- **t.co filtering**: Specifically avoids Twitter's redirect URLs

## Testing and Validation

The fix addresses the core issue where manual copy-paste worked but automated scraping failed, by replicating the browser's hover behavior that reveals full URLs.

## Future Considerations

1. **Monitoring**: Watch for further Twitter/X frontend changes that might affect scraping
2. **Robustness**: Consider adding more data attribute checks as Twitter evolves
3. **Performance**: Monitor if hover actions significantly slow down scraping
4. **Alternative approaches**: Investigate Twitter API alternatives if scraping becomes unreliable

## Related Issues

This fix resolves the discrepancy between manual URL copying (which worked) and automated extraction (which failed), demonstrating how social media platforms increasingly separate visual presentation from underlying data to optimize performance and reduce scraper effectiveness.
