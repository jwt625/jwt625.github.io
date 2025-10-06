# RFD-006: Markdown Link Line Break Bug in Twitter Scraping Script

## Status
- **Status**: Draft
- **Created**: 2025-10-06
- **Author**: AI Assistant
- **Related Files**: `_posts/scrape_thread_from_urls.py`

## Problem Statement

The Twitter scraping script `scrape_thread_from_urls.py` produces markdown files with malformed links that contain line breaks. This results in broken markdown rendering where links are split across multiple lines.

### Examples of the Bug

In the generated markdown files, links appear like this:

```markdown
Liu2025: [Quiescent power consumption of carbon-based analog operational amplifiers at low temperatures](
https://doi.org/10.1063/5.0291590)
```

Instead of the correct format:

```markdown
Liu2025: [Quiescent power consumption of carbon-based analog operational amplifiers at low temperatures](https://doi.org/10.1063/5.0291590)
```

### Impact

1. **Broken Markdown Rendering**: Links with line breaks don't render properly in markdown processors
2. **Poor User Experience**: Readers cannot click on broken links
3. **Manual Cleanup Required**: Each generated file requires manual editing to fix the links
4. **Inconsistent Output**: Some links work while others are broken

## Root Cause Analysis

The bug originates in the `scrape_tweet()` function in `scrape_thread_from_urls.py`:

### Primary Issue
- **Location**: Line 70 in `scrape_thread_from_urls.py`
- **Code**: `tweet_text = tweet_text_element.text`
- **Problem**: When extracting text from the Twitter web element, the `.text` property preserves line breaks that exist in the HTML rendering

### Secondary Issue
- **Location**: Line 88 in `scrape_thread_from_urls.py`  
- **Code**: `clean_text = visible_text.replace('\n', '').replace('…', '').replace('...', '').strip()`
- **Problem**: The newline cleaning is only applied to `visible_text` during URL reconstruction, but not to the final `tweet_text` that gets written to markdown

### Why This Happens
1. Twitter's web interface wraps long URLs across multiple lines for display
2. Selenium's `.text` property captures these line breaks as literal `\n` characters
3. When the script replaces truncated URLs with full URLs, it doesn't clean up existing line breaks in the surrounding text
4. The final `tweet_text` retains these line breaks when written to the markdown file

## Proposed Solution

### Option 1: Comprehensive Text Cleaning (Recommended)
Add a comprehensive text cleaning step before writing `tweet_text` to the markdown file:

```python
# After line 271 in scrape_thread_from_urls.py
# Clean up line breaks in the final tweet text
tweet_data['text'] = re.sub(r'\s*\n\s*', ' ', tweet_text).strip()
```

### Option 2: Post-Processing Fix
Add a post-processing step in the markdown creation function to fix broken links:

```python
# In the create_markdown function, after writing tweet text
def fix_broken_links(text):
    # Fix links that are split across lines
    # Pattern: ](newline + optional whitespace + url)
    pattern = r'\]\(\s*\n\s*([^\)]+)\)'
    return re.sub(pattern, r'](\1)', text)
```

### Option 3: Enhanced URL Replacement
Improve the URL replacement logic to also clean surrounding text:

```python
# Enhance the replacement logic around line 263
if should_replace and visible_text in tweet_text:
    # Clean up the replacement area
    replacement_text = tweet_text.replace(visible_text, full_url)
    # Remove line breaks around URLs
    replacement_text = re.sub(r'\]\(\s*\n\s*([^\)]+)\)', r'](\1)', replacement_text)
    tweet_text = replacement_text
```

## Implementation Plan

### Phase 1: Immediate Fix (Recommended)
1. Implement Option 1 (comprehensive text cleaning) in `scrape_thread_from_urls.py`
2. Test with a small sample of URLs to verify the fix
3. Add the fix before the next scraping run

### Phase 2: Validation
1. Run the fixed script on a test set of URLs
2. Verify that generated markdown has properly formatted links
3. Check that no other formatting is broken by the text cleaning

### Phase 3: Documentation Update
1. Update any documentation about the scraping process
2. Add a note about this fix in the script comments
3. Consider adding validation checks for broken links in future runs

## Testing Strategy

### Test Cases
1. **Long URLs**: Test with tweets containing very long URLs that wrap in the browser
2. **Multiple Links**: Test with tweets containing multiple links
3. **Mixed Content**: Test with tweets containing both links and other formatted text
4. **Edge Cases**: Test with tweets containing special characters, emojis, etc.

### Validation
- Check that all `](` patterns are followed immediately by URLs without line breaks
- Verify that link text is preserved correctly
- Ensure that non-link content is not affected

## Risk Assessment

### Low Risk
- The proposed text cleaning is conservative and only targets whitespace/newlines
- Existing functionality should not be affected
- Easy to revert if issues arise

### Mitigation
- Test thoroughly before production use
- Keep backup of original scraping output for comparison
- Monitor output quality after implementing the fix

## Future Considerations

1. **Automated Validation**: Consider adding automated checks for broken markdown links
2. **Enhanced Cleaning**: May need to handle other formatting issues that arise
3. **Alternative Approaches**: Could explore using different Selenium text extraction methods

## References

- **Bug Location**: `_posts/scrape_thread_from_urls.py`, lines 70, 88, 263, 271
- **Example Files**: `_posts/2025-10-06-weekly-OFS-67.md` (contains multiple instances of this bug)
- **Related**: This bug affects all markdown files generated by the scraping script
