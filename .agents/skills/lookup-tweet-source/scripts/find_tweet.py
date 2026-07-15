#!/usr/bin/env python3
"""Rank scraped X/Twitter threads by text, URL, citation, or media terms."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


def find_repo(explicit: str | None) -> Path:
    candidates = [Path(explicit).resolve()] if explicit else []
    candidates.extend([Path.cwd().resolve(), *Path(__file__).resolve().parents])
    for candidate in candidates:
        if (candidate / "_posts" / "scraping").is_dir():
            return candidate
    raise SystemExit("Could not find a repo containing _posts/scraping; pass --repo PATH")


def line_for_url(path: Path, url: str) -> int:
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if url in line:
            return number
    return 1


def searchable_text(thread: dict) -> str:
    chunks = [str(thread.get("url", ""))]
    for tweet in thread.get("tweets", []):
        chunks.append(str(tweet.get("text", "")))
        for media in tweet.get("media", []):
            chunks.extend([str(media.get("url", "")), str(media.get("local_path", ""))])
    return "\n".join(chunks)


def score(text: str, query: str, terms: list[str]) -> int:
    folded = text.casefold()
    value = 40 * folded.count(query.casefold()) if query else 0
    hits = sum(term.casefold() in folded for term in terms)
    value += hits * 5
    if terms and hits == len(terms):
        value += 20
    for term in terms:
        value += min(folded.count(term.casefold()), 5)
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="+", help="phrase or topic terms")
    parser.add_argument("--repo", help="repository root (auto-detected by default)")
    parser.add_argument("--limit", type=int, default=8, help="maximum matches to show")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args()

    repo = find_repo(args.repo)
    scraping = repo / "_posts" / "scraping"
    query = " ".join(args.query).strip()
    terms = list(dict.fromkeys(re.findall(r"[\w./:-]+", query.casefold())))
    results: dict[str, dict] = {}

    for path in sorted(scraping.glob("scraped_tweets*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            print(f"warning: skipping {path}: {exc}", file=sys.stderr)
            continue
        if not isinstance(payload, list):
            continue
        for thread in payload:
            if not isinstance(thread, dict) or not thread.get("url"):
                continue
            text = searchable_text(thread)
            rank = score(text, query, terms)
            if rank <= 0:
                continue
            url = str(thread["url"])
            source = {
                "path": str(path.relative_to(repo)),
                "line": line_for_url(path, url),
            }
            item = results.setdefault(
                url,
                {"score": rank, "url": url, "sources": [], "tweets": thread.get("tweets", [])},
            )
            item["score"] = max(item["score"], rank)
            item["sources"].append(source)
            # Prefer the dated archive's content over the rolling undated file.
            if path.name != "scraped_tweets.json":
                item["tweets"] = thread.get("tweets", [])

    ranked = sorted(results.values(), key=lambda item: (-item["score"], item["url"]))[: args.limit]
    if args.json:
        print(json.dumps(ranked, ensure_ascii=False, indent=2))
        return 0 if ranked else 1

    if not ranked:
        print(f"No scraped tweet matched: {query}")
        return 1

    for index, item in enumerate(ranked, 1):
        dated = [s for s in item["sources"] if Path(s["path"]).name != "scraped_tweets.json"]
        source = (dated or item["sources"])[-1]
        print(f"{index}. score={item['score']}  {item['url']}")
        print(f"   source: {source['path']}:{source['line']}")
        for tweet in item["tweets"]:
            tweet_text = " ".join(str(tweet.get("text", "")).split())
            if any(term.casefold() in searchable_text({"tweets": [tweet]}).casefold() for term in terms):
                stamp = tweet.get("timestamp", "")
                print(f"   {stamp}  {tweet_text[:300]}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
