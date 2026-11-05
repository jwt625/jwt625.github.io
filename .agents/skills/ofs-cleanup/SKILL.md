---
name: ofs-cleanup
description: Clean up a freshly scraped weekly OFS (outside five sigma) draft in this jwt625.github.io repository before publishing. Use for requests to review, clean up, or tidy an OFS post, remove repeated content from scraping glitches, fix image links overwritten by filename collisions, comment out out-of-context replies, fix missing or shifted section titles, or format references.
---

# OFS Cleanup

Turn the raw scraped draft `_posts/YYYY-MM-DD-weekly-OFS-N.md` into the state of the published posts. Fix scraper damage and hide context-less replies. Do not rewrite the author's voice.

The draft is usually untracked and the author edits it by hand, sometimes while you work. Back it up first, patch it in place, never regenerate it. Do not commit.

## Inputs

- `_posts/scraping/scraped_tweets_DATE.json`: source of truth. A list of threads with `url` and `tweets`; each tweet has `text`, `media[].url`, `media[].local_path`, `timestamp`.
- `_posts/scraping/output_DATE.md`: generated tags and headings, one heading per thread, in thread order.
- `assets/images/YYYY/<daterange>/`: scraped images.
- Reference posts: the latest cleaned posts. `git diff 0bb6d30 2eb2ce7 -- _posts/2026-10-14-weekly-OFS-120.md` shows a full before and after.

## Workflow

1. Copy the draft to the scratchpad as a backup.
2. Run the checker from the repository root. It only reads:

   ```bash
   python3 .agents/skills/ofs-cleanup/scripts/check_post.py _posts/YYYY-MM-DD-weekly-OFS-N.md
   ```

3. Read the full draft, then apply the fixes below in a single patch script that asserts each old string matches exactly once. A failed assert means the author changed the file, so re-read it.
4. Re-run the checker and diff against the backup. Every remaining report line should be explained.
5. Report: what changed, judgement calls that could go either way, what needs the author. Keep it short.

## Fixes

**Repeated content.** Delete, keep one copy. The scraper repeats tweets, sometimes as whole blocks of text plus images (non-adjacent repeats too), and the same text appears twice in the JSON.

**Image filename collisions.** Files are named from the tweet timestamp. A tweet quoting an older one inherits the older timestamp, so both write `<timestamp>_<index>.jpg`, and the later thread overwrites the earlier files. Nothing is lost when the quoted images are also on the newer tweet; only the indices shift.
- The checker prints where each media URL really lives. Trust `real=`, not `json=`.
- Point the old section at its images' real files. Remove quoted repeats from the newer section so it shows only its own images.
- Prove it with hashes if unsure: download the `media[].url` values to the scratchpad and compare to the local files. Do not open images to work this out.

**Byte-identical images under different names.** A reply can inherit its parent's images. Keep them under the parent, remove the copies.

**Section titles.** Headings are generated separately from the body and can drift. Every thread needs one heading that matches its content.
- The checker flags sections holding 0 or 2+ threads. That means shifted titles: drop the stale heading, move each later heading down one section, add a heading if the last section lacks one.
- Also read each heading against its section. A shift can leave counts correct.

**Out-of-context replies.** Comment out, never delete, using this exact format:

```md
   <!-- - the reply text -->
```

- Hide a line when a reader needs the hidden parent tweet to follow it: short reactions ("lol nice", "yes", "exactly", "this"), questions or answers to other people, and side remarks to a specific person. Hide these even when they carry substance. The test is whether the line makes sense without the parent, not whether it is interesting.
- Signals: the checker's reply candidates (posted long after the thread, or out of timestamp order), openings like "yes", "yeah", "hmm", "kind of", "maybe", "it's", "they are".
- Keep the author's own continuation: root text, follow-ups minutes later, citations, figures, answers to his own quizzes. Multi-line tweets split into separate bullets, so judge each bullet: one tweet can hold both a keeper and a reply.
- Hide images belonging to a hidden reply, as `<!-- ![name.jpg](path) -->`.
- If a line could go either way, keep it visible and list it in the report.

**References and links.**
- Papers: `   - Author2026: [Title](https://doi.org/...)`. No space in the key. Key uses the first author's surname and the year.
- Bare URLs become markdown links, including `(https://...)` forms. Rejoin sentences the scraper split around a URL or an @mention, for example `see e.g.` followed by a URL bullet.
- Fix extraction damage in titles, such as run-together words, and check it against the source.
- Verify each DOI and arXiv ID resolves to the cited title and first author (Crossref `api.crossref.org/works/<doi>`, arXiv `export.arxiv.org/api/query?id_list=<id>`), one request at a time. Wrong or repeated DOIs have shipped before: a repeated DOI means at least one is wrong. On a mismatch, search by title and fix it only once a primary source confirms it. Otherwise leave it and report it.

## Leave alone

- The author's words: slang, profanity, typos in tweet text, strikethrough, emoji. Report nothing about these unless a typo changes the meaning.
- Tags, and the post title.
- Old threads the scrape re-surfaced: keep them even if an earlier OFS already covered them.
- `cover` and `overlay_image`, section order: the author picks. The cover is usually an image from the lead section, and the lead section is often moved to the top. Report that the placeholder is still there and suggest a section if asked.
- The `# Projects (2026)` section: the author adds and maintains it. Do not write or copy it unless asked.
- The scraper itself, unless asked. Mention bugs instead.
- `assets/`: never delete or rename image files, even unreferenced ones.
