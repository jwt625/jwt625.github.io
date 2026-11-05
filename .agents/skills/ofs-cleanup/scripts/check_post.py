#!/usr/bin/env python3
"""Read-only checks for a weekly OFS draft against its dated scrape. Stdlib only.

Usage: python3 .agents/skills/ofs-cleanup/scripts/check_post.py _posts/YYYY-MM-DD-weekly-OFS-N.md [scrape.json]
"""
import collections
import datetime as dt
import hashlib
import json
import os
import re
import sys

IMG = re.compile(r"!\[[^\]]*\]\((/assets/images/[^)]+)\)")
post = sys.argv[1]
date = re.search(r"(\d{4})-(\d{2})-(\d{2})", os.path.basename(post))
scrape = sys.argv[2] if len(sys.argv) > 2 else f"_posts/scraping/scraped_tweets_{''.join(date.groups())}.json"
raw = open(post, encoding="utf-8").read().split("\n")
live = [(n, l) for n, l in enumerate(raw, 1) if not l.strip().startswith("<!--")]
body = "\n".join(l for _, l in live)
threads = json.load(open(scrape, encoding="utf-8")) if os.path.exists(scrape) else []
if not threads:
    print(f"no scrape found at {scrape}; scrape-based checks skipped")


def head(title):
    print(f"\n[{title}]")


head("front matter")
for n, l in live[:60]:
    if re.match(r"\s*(cover|overlay_image):\s*\S*/$", l):
        print(f"L{n}: placeholder, no image set: {l.strip()}")

head("sections vs threads (each section should hold exactly one thread)")
sections, cur = [], None
for n, l in live:
    if l.startswith("# "):
        cur = {"line": n, "title": l[2:], "text": ""}
        sections.append(cur)
    elif cur:
        cur["text"] += l + "\n"
sections = [s for s in sections if not s["title"].startswith("Projects")]
print(f"{len(sections)} sections, {len(threads)} threads")
hits = collections.Counter()
for i, t in enumerate(threads):
    first = next((x["text"] for x in t["tweets"] if x["text"].strip()), "")
    key = first.split("\n")[0][:40]
    where = [s for s in sections if key and key in s["text"]]
    if where:
        hits[where[0]["line"]] += 1
    else:
        print(f"thread {i}: root text not found: {key!r} ({t['url']})")
for s in sections:
    if hits[s["line"]] != 1:
        print(f"L{s['line']}: {hits[s['line']]} threads under '{s['title']}'")

head("images")
refs = collections.Counter(os.path.basename(m) for _, l in live for m in IMG.findall(l))
dirs = {os.path.dirname(m) for _, l in live for m in IMG.findall(l)}
weekly = [d for d in dirs if re.search(r"/\d{8}_\d{8}$", d)]
folder = max(weekly, key=lambda d: sum(os.path.basename(m) in os.listdir("." + d) for m in refs) if os.path.isdir("." + d) else 0, default=None)
print("multi-referenced:", sorted(k for k, v in refs.items() if v > 1))
if folder and os.path.isdir("." + folder):
    files = os.listdir("." + folder)
    print("folder:", folder)
    print("missing:", sorted(k for k in refs if k not in files and all(not os.path.exists(f".{d}/{k}") for d in dirs)))
    print("unreferenced:", sorted(set(files) - set(refs)))
    groups = collections.defaultdict(list)
    for f in files:
        groups[hashlib.md5(open(f".{folder}/{f}", "rb").read()).hexdigest()].append(f)
    print("byte-identical:", [sorted(v) for v in groups.values() if len(v) > 1])

head("filename collisions (same name, different source: later scrape overwrote the file)")
order, by_name = [], collections.defaultdict(set)
for t in threads:
    for x in t["tweets"]:
        for m in x["media"]:
            order.append((m["url"], os.path.basename(m["local_path"])))
            by_name[os.path.basename(m["local_path"])].add(m["url"])
holder = {name: url for url, name in order}  # last writer owns the file on disk
for name in sorted(k for k, v in by_name.items() if len(v) > 1):
    print(f"{name}: on disk = {holder[name]}")
if any(len(v) > 1 for v in by_name.values()):
    print("where each thread's media really lives:")
    for i, t in enumerate(threads):
        for x in t["tweets"]:
            for m in x["media"]:
                name = os.path.basename(m["local_path"])
                if len(by_name[name]) > 1:
                    real = sorted(k for k, u in holder.items() if u == m["url"])
                    print(f"  thread {i}: {m['url'].split('/')[-1]} json={name} real={real}")

head("repeated lines")
prev = None
for n, l in live:
    if l.strip() and l == prev:
        print(f"L{n}: {l.strip()[:90]}")
    prev = l or prev
blocks = collections.defaultdict(list)
for n, l in live:
    if l.strip().startswith("- ") and len(l.strip()) > 12:
        blocks[l.strip()].append(n)
for text, ns in blocks.items():
    if len(ns) > 1:
        print(f"L{ns}: {text[:90]}")

head("links and citations")
for n, l in live:
    bare = re.sub(r"\]\([^)]*\)", "]", l)
    if "http" in bare and not l.lstrip().startswith(("<", "!")):
        print(f"L{n} bare URL: {l.strip()[:100]}")
    if re.match(r"\s*- [A-Z][\w-]* \d{4}:", l):
        print(f"L{n} key has a space, should be Author2026: {l.strip()[:60]}")
dois = re.findall(r"doi\.org/([^)\s]+)", body)
print("repeated DOI:", sorted(d for d, c in collections.Counter(dois).items() if c > 1))
print("to verify (doi, arXiv):", sorted(set(dois + re.findall(r"arxiv\.org/abs/([\d.]+)", body))))

head("reply candidates (posted >30 min after the previous tweet, or out of order)")
for i, t in enumerate(threads):
    last = None
    seen = set()
    for x in t["tweets"]:
        text = x["text"].strip()
        stamp = x.get("timestamp")
        when = dt.datetime.fromisoformat(stamp) if stamp else None
        if text in seen or not text:
            continue
        seen.add(text)
        if last and when and (when < last or (when - last).total_seconds() > 1800):
            state = "live" if text.split("\n")[0][:40] in body else "hidden/absent"
            print(f"thread {i} [{state}]: {text[:90]!r}")
        last = max(last, when) if last and when else (when or last)
