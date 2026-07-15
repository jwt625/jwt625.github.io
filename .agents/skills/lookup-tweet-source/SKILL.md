---
name: lookup-tweet-source
description: Trace a topic, quotation, image, paper, or section in this jwt625.github.io repository back to its original X/Twitter thread URL and scraped record. Use for requests to find a tweet mentioned in an OFS blog, recover the source URL for blog content, inspect original scraped tweet text or media, or map between weekly OFS posts and files under _posts/scraping.
---

# Lookup Tweet Source

Find the relevant OFS section, then trace its distinctive text or media back to the dated scrape. Report the X URL and the exact local source record; do not browse the web unless the user asks for external verification.

## Repository map

- `_posts/YYYY-MM-DD-weekly-OFS-N.md`: published weekly OFS posts. A section normally contains a heading, lightly edited tweet text, copied images, follow-up text, and citations.
- `_posts/scraping/scraped_tweets_DATE.json`: canonical dated scrape for a weekly batch. The top level is a list of thread objects with `url` and `tweets`. Each tweet contains `text`, `media`, and `timestamp`.
- `_posts/scraping/scraped_tweets_DATE1_DATE2.json`: older scrape batches using a date range; treat these the same way.
- `_posts/scraping/scraped_tweets.json`: undated/current scrape and possible duplicate of a dated archive. Prefer the dated archive when both contain the same thread.
- `_posts/scraping/sorted_tweet_urls_DATE.txt`: URL-only batch list. Use as confirmation when needed.
- `_posts/scraping/output_DATE.md`: generated post outline/headings, not the authoritative source for tweet URLs.
- `assets/images/...`: images copied into published posts. Their basenames usually match `media[*].local_path` in the scrape, even though the directory prefixes differ.

The thread object's `url` is normally the root tweet URL. Follow-up entries in `tweets` do not necessarily retain their own status URLs. State this limitation if the requested content is specifically a reply in the thread.

## Workflow

1. Start at the repository root. If uncertain, use `git rev-parse --show-toplevel`.
2. Search OFS posts for several likely variants, because the user's remembered terminology may differ from the post:

   ```bash
   rg -n -i -C 6 'term1|term2|distinctive phrase' _posts --glob '*weekly-OFS*.md'
   ```

3. Extract the most distinctive available key from the matching section, in this order:
   - an exact sentence fragment;
   - a paper title, DOI, author-year key, or unusual heading;
   - an image basename such as `20260601_152616_0.jpg`;
   - a small combination of topic terms.
4. Run the bundled lookup script. Quote multiword queries:

   ```bash
   python3 .agents/skills/lookup-tweet-source/scripts/find_tweet.py "distinctive phrase"
   python3 .agents/skills/lookup-tweet-source/scripts/find_tweet.py 20260601_152616_0.jpg
   ```

5. Verify the best match by comparing the full thread text, media basenames, timestamp, and nearby OFS section. For direct inspection, use:

   ```bash
   rg -n -i -C 8 'distinctive phrase|media_basename' _posts/scraping --glob 'scraped_tweets*.json'
   ```

6. Return:
   - the direct `https://x.com/.../status/...` URL;
   - a clickable local link to the dated JSON record and line;
   - a one-sentence note if the URL represents the root of a multi-tweet thread rather than the exact follow-up.

## Search fallbacks

- If an exact phrase fails, split the concept into synonyms and search both posts and JSON. Blog prose may be edited from the tweet.
- If text is generic, search an image basename; this is often the strongest join key between a post and its scrape.
- If the section contains a citation, search its DOI or title in the JSON.
- Use the blog publication date to prioritize a scrape with the same or immediately preceding batch date.
- Do not infer a tweet URL from timestamps or status-number ordering when no stored URL exists. Report the root thread URL and the limitation.

## Potential future improvements

Treat these as design directions, not currently available commands.

### OCR screenshots before searching

Add a macOS-native OCR indexer using Apple's Vision framework (`VNRecognizeTextRequest`), preferably as a small Swift command-line script. Run it over images referenced by OFS posts under `assets/images/`, then store derived records such as:

```json
{"image_path":"assets/images/.../image.jpg","text":"recognized text","post_path":"_posts/...md","tweet_url":"https://x.com/..."}
```

Search this OCR corpus with `rg` or SQLite FTS before falling back to manual image inspection. Preserve the image path and source joins so every OCR hit can be traced through the image basename to its OFS section and `scraped_tweets*.json` thread. Record OCR confidence when available, and treat recognized text as noisy derived data rather than authoritative content.

This is likely the highest-value next improvement because technical terms, graph labels, and package dimensions may exist only inside screenshots and never appear in tweet or blog text.

### Add hybrid/RAG retrieval

Build a local retrieval index when paraphrased topic searches routinely defeat exact matching. Index two linked document types:

- one document per OFS section, including heading, prose, citations, post path, date, and image basenames;
- one document per scraped thread, including all tweet text, citations, timestamps, media basenames, root URL, scrape path, and source line.

Combine lexical retrieval (BM25 or SQLite FTS) with embeddings rather than using vector similarity alone. Retrieve both document types, rerank using shared citations, image basenames, and nearby dates, then return the stored source URL and file references. Include OCR text as a lower-confidence field once the OCR index exists.

Keep embeddings and indexes in a reproducible derived-data location, update them incrementally using content hashes, and never let a generated answer or vector match replace verification against the original JSON record. A useful result schema should always include `score`, `matched_fields`, `post_path`, `scrape_path`, `source_line`, and `tweet_url`.

## Output standard

Keep simple answers compact:

```text
Tweet: https://x.com/<account>/status/<id>
Scraped record: <clickable path to scraped_tweets_DATE.json:line>

This record contains the original post and its follow-up(s).
```
