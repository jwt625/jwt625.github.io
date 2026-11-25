# DevLog-001: X scraping - login block, browser profiles, logged-out extractor

Date: 2026-11-24
Scope: `_posts/scrape_thread_from_urls.py`, browser profiles, OFS-126
Status: shipped; one extraction defect deferred by decision

## TODO

- [ ] Fix quoted-tweet contamination in the logged-out extractor (next task)
- [ ] Post title still reads `#00`: `standard_header.md` is a fixed template, number is set by hand (this run: 126)
- [ ] Decide whether the Chrome branch and `chrome_user_data_dir` stay in `config.json`
- [x] Stop spoofing User-Agent / disabling WebRTC
- [x] Stop writing automation prefs into the daily Firefox profile
- [x] Add logged-out DOM extraction path
- [x] Full run on 19 URLs

## Symptom

`python scrape_thread_from_urls.py` opened Firefox, X answered the login attempt with
"Something went wrong. Please try again."

Firefox session-restore files from the failed runs showed the sequence:

```
https://x.com/                          title "X. It's what's happening / X"   (logged-out landing page)
https://x.com/i/jf/onboarding/web#/s/knowledge_check/r-0x1v8p
https://x.com/i/jf/onboarding/web#/s/knowledge_check/r-9o6leu
storage: rweb.new_onboarding.mode = login
```

So X accepted the login and then routed the session into its onboarding/risk flow. Cookies were
not the problem: the profile still had `auth_token`, `ct0`, `twid`, `guest_id`, `cf_clearance`.

## Root causes in the Firefox path

1. `general.useragent.override` claimed Firefox 115 / macOS 10.15 on a Firefox 160.0.1 / macOS 15.5
   binary. TLS fingerprint and header disagreed, and `cf_clearance` is bound to IP + UA, so the
   cookie minted under the real UA was invalid under the fake one.
2. `media.peerconnection.enabled = false` removed `RTCPeerConnection`, a common bot signal.
3. Both prefs were written by geckodriver into `user.js` in the daily profile
   (`9ons1v9u.default-release`) and persisted into `prefs.js`, so normal browsing inherited the
   spoof. Removed; backup at `Firefox/Profiles/_backup_prefs_20261124/`.
4. `--width` / `--height` are not Firefox flags (only `--window-size` exists, screenshot only), and
   `useAutomationExtension` is a Chrome pref. Both were no-ops.

Fingerprint now measures `Firefox/160.0`, `RTCPeerConnection: function`.

## Chrome profile transplant: negative result

Goal was to reuse the existing Chrome session. Copied `Local State` plus `Default/Cookies`
(17 `.x.com` cookies, all `v10`) into a separate `--user-data-dir` and launched Chrome 158.

```
no navigation, launch + quit:
  before: 5582 cookies (google 116, x.com 22)
  after : 0
```

Chrome discards cookies it cannot decrypt in a foreign user-data-dir. Copying a Chrome profile is
not a session-transfer mechanism on this build. Also note Chrome 136+ refuses remote debugging on
the default data dir, so CDP attach to the live profile is not an option either.

## Logged-out route

Logged-out X serves a different frontend: `<article>` nodes inside `<main>` with no `data-testid`,
no `<time>`, no `User-Name`. Structure:

- author: `a[href="/handle"]`
- text: `div[dir="auto"][lang]`
- media: `img[src*="pbs.twimg.com/media"]`
- permalink: `a[href="/handle/status/<id>"]`, anchor text like `6:45 PM - Nov 9, 2026`

Added `scrape_thread_ssr()` plus a JS extractor; `scrape_thread()` still tries the classic
`article[data-testid="tweet"]` for 10 s first, so the logged-in path is unchanged.

Timestamps come from the status id (snowflake), not the rendered string, to stay locale independent.
Checked against the page: `6:45 PM - Nov 9, 2026` PST = `2026-11-10T02:45:09.246Z`, exact match.

Own replies are rendered on logged-out pages: two spot checks showed the root's self-replies all
present (`2120307858038542463`: 2 of 2). Others' replies may be truncated.

## Run result (19 URLs, logged out, no login)

```
threads 19 | tweets 34 | images 43
post        _posts/2026-11-24-weekly-OFS-126.md
images      assets/images/2026/20240708_20261124/
log         _posts/scraping/run_20261124_232342.log
json        _posts/scraping/scraped_tweets_20261124.json
```

Completeness check against live pages: 17 of 19 threads matched the page's author-tweet count
exactly. No case where the page had an author tweet that the scrape missed.

## Known defect (fix next)

Sections 8 (`Depth Sensing Pattern Matching Limitations`, URL `2120545675163390037`) and
14 (`LLM-Based Photonics Paper Auditing`, URL `2122720315239481486`) contain a quoted tweet.

Inside the authored `<article>` the quoted tweet's permalink appears before the tweet's own:

```
/jwt0625/status/2120545675163390037/photo/1
/icanc4/status/2120495385445900316        <- quoted tweet, matched first
/icanc4/status/2120495385445900316/photo/1
/jwt0625/status/2120545675163390037        <- real permalink, "7:54 AM - Nov 11, 2026"
```

Effect: timestamp taken from the quoted status id (12:34:31Z instead of 15:54:21Z) and one extra
image from the quote. Tweet text is correct.

Accepted for OFS-126 on 2026-11-24. Fix plan:

- pick the permalink anchor whose text matches a time pattern (`\d{1,2}:\d{2}\s?(AM|PM)`), fall back
  to the last status anchor;
- exclude nested `<article>` elements when collecting text and media.

## Files changed

- `_posts/scrape_thread_from_urls.py` - driver options, Firefox/Chrome branch, `scrape_thread_ssr()`
- `_posts/config.json` (untracked) - `browser: firefox`, `firefox_profile_path` -> `x-scrape`,
  `chrome_user_data_dir` added (unused while `browser: firefox`)
- `~/Library/Application Support/Firefox/Profiles/x-scrape` - dedicated automation profile (copy)
- `~/Library/Application Support/Firefox/Profiles/_backup_prefs_20261124/` - prefs backup
- `~/Library/Application Support/chrome-scrape-profile` - Chrome attempt, empty, unused

## How to run

```
cd _posts
.venv/bin/python scrape_thread_from_urls.py
# 1 -> enter URL file -> ENTER at the login prompt (no login needed on the logged-out path)
```

## Lessons

- A spoofed User-Agent that disagrees with the binary is worse than no spoof: it invalidates
  UA-bound cookies and trips risk flows.
- Never point automation at the daily browser profile; geckodriver writes `user.js` into it.
- A DOM probe that finds zero nodes is not proof the page did not render. Hydration timing varies
  between runs and window modes; verify twice before concluding.
- Copying a Chrome profile does not move the session. Do not spend time on cookie transplants.
- Deriving timestamps from status ids beats parsing localized date strings.
