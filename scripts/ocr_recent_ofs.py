#!/usr/bin/env python3
"""OCR images referenced by recent weekly OFS posts with macOS Vision.

The output is derived, searchable metadata. Each OCR record keeps its OFS post
location and, when available, the canonical scraped-tweet record and X URL.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = REPO_ROOT / "_data/ofs_recent_image_ocr.json"
IMAGE_RE = re.compile(r"/assets/images/[^\s)\"'>]+")

SWIFT_SOURCE = r"""
import Foundation
import Vision

struct OCRLine: Codable {
    let text: String
    let confidence: Float
    let boundingBox: [Double]
}

struct OCRResult: Codable {
    let imagePath: String
    let width: Int?
    let height: Int?
    let lines: [OCRLine]
    let error: String?
}

func recognize(path: String) -> OCRResult {
    let url = URL(fileURLWithPath: path)
    guard let source = CGImageSourceCreateWithURL(url as CFURL, nil),
          let image = CGImageSourceCreateImageAtIndex(source, 0, nil) else {
        return OCRResult(imagePath: path, width: nil, height: nil, lines: [],
                         error: "Failed to load image")
    }

    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    request.recognitionLanguages = ["en-US"]
    request.minimumTextHeight = 0.004

    do {
        try VNImageRequestHandler(url: url, options: [:]).perform([request])
        let lines = (request.results ?? []).compactMap { observation -> OCRLine? in
            guard let candidate = observation.topCandidates(1).first else { return nil }
            let box = observation.boundingBox
            return OCRLine(
                text: candidate.string,
                confidence: candidate.confidence,
                boundingBox: [box.origin.x, box.origin.y, box.size.width, box.size.height]
            )
        }
        return OCRResult(imagePath: path, width: image.width, height: image.height,
                         lines: lines, error: nil)
    } catch {
        return OCRResult(imagePath: path, width: image.width, height: image.height,
                         lines: [], error: String(describing: error))
    }
}

let results = CommandLine.arguments.dropFirst().map { recognize(path: $0) }
let encoder = JSONEncoder()
encoder.outputFormatting = [.sortedKeys]
do {
    FileHandle.standardOutput.write(try encoder.encode(results))
} catch {
    fputs("Failed to encode OCR output: \(error)\n", stderr)
    exit(1)
}
"""


def default_posts() -> list[Path]:
    post_name = re.compile(r"\d{4}-\d{2}-\d{2}-weekly-OFS-\d+\.md")
    posts = sorted(
        path
        for path in REPO_ROOT.glob("_posts/*-weekly-OFS-*.md")
        if post_name.fullmatch(path.name)
    )
    return posts[-5:]


def relative(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def post_image_references(posts: list[Path]) -> dict[str, list[dict[str, object]]]:
    references: dict[str, list[dict[str, object]]] = {}
    for post in posts:
        section: str | None = None
        for line_number, line in enumerate(
            post.read_text(encoding="utf-8").splitlines(), start=1
        ):
            if line.startswith("# "):
                section = line[2:].strip()
            for match in IMAGE_RE.finditer(line):
                image_url = match.group(0)
                reference = {
                    "post_path": relative(post),
                    "post_line": line_number,
                    "section": section,
                }
                if reference not in references.setdefault(image_url, []):
                    references[image_url].append(reference)
    return references


def scrape_index() -> dict[str, list[dict[str, object]]]:
    index: dict[str, list[dict[str, object]]] = {}
    for scrape_path in sorted(
        (REPO_ROOT / "_posts/scraping").glob("scraped_tweets*.json")
    ):
        raw = scrape_path.read_text(encoding="utf-8")
        try:
            threads = json.loads(raw)
        except json.JSONDecodeError:
            continue
        for thread in threads:
            root_url = thread.get("url")
            for tweet_number, tweet in enumerate(thread.get("tweets", []), start=1):
                for media in tweet.get("media", []):
                    basename = Path(media.get("local_path", "")).name
                    if not basename:
                        continue
                    needle = f'"local_path": "media/{basename}"'
                    offset = raw.find(needle)
                    source_line = raw.count("\n", 0, offset) + 1 if offset >= 0 else None
                    source = {
                        "scrape_path": relative(scrape_path),
                        "source_line": source_line,
                        "thread_root_url": root_url,
                        "tweet_number_in_thread": tweet_number,
                        "media_url": media.get("url"),
                    }
                    if source not in index.setdefault(basename, []):
                        index[basename].append(source)
    return index


def run_vision_ocr(image_paths: list[Path]) -> list[dict[str, object]]:
    with tempfile.TemporaryDirectory(prefix="ofs_vision_ocr_") as temp_dir:
        swift_path = Path(temp_dir) / "vision_ocr.swift"
        swift_path.write_text(SWIFT_SOURCE, encoding="utf-8")
        completed = subprocess.run(
            ["swift", str(swift_path), *map(str, image_paths)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
    if completed.returncode:
        raise RuntimeError(completed.stderr.strip() or "macOS Vision OCR failed")
    return json.loads(completed.stdout)


def build_collection(posts: list[Path]) -> dict[str, object]:
    references = post_image_references(posts)
    sources = scrape_index()
    existing_urls = [
        image_url for image_url in sorted(references) if (REPO_ROOT / image_url[1:]).is_file()
    ]
    missing_urls = sorted(set(references) - set(existing_urls))
    raw_results = run_vision_ocr([REPO_ROOT / url[1:] for url in existing_urls])

    records = []
    for image_url, raw in zip(existing_urls, raw_results, strict=True):
        image_path = REPO_ROOT / image_url[1:]
        lines = raw.get("lines", [])
        records.append(
            {
                "filename": image_path.name,
                "image_path": image_url,
                "width": raw.get("width"),
                "height": raw.get("height"),
                "sha256": hashlib.sha256(image_path.read_bytes()).hexdigest(),
                "ocr_text": "\n".join(line["text"] for line in lines).strip(),
                "ocr_lines": lines,
                "has_text": bool(lines),
                "error": raw.get("error"),
                "post_references": references[image_url],
                "tweet_sources": sources.get(image_path.name, []),
            }
        )

    return {
        "schema_version": 1,
        "generated_at": datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(
            timespec="seconds"
        ),
        "ocr_engine": {
            "framework": "Apple Vision",
            "request": "VNRecognizeTextRequest",
            "recognition_level": "accurate",
            "languages": ["en-US"],
            "language_correction": True,
        },
        "scope": {
            "posts": [relative(post) for post in posts],
            "unique_image_references": len(references),
            "processed_images": len(records),
            "missing_images": missing_urls,
        },
        "records": records,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "posts",
        nargs="*",
        type=Path,
        help="Weekly OFS Markdown posts (default: latest five)",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    posts = [path.resolve() for path in args.posts] if args.posts else default_posts()
    missing_posts = [str(path) for path in posts if not path.is_file()]
    if missing_posts:
        raise SystemExit(f"Missing posts: {', '.join(missing_posts)}")

    collection = build_collection(posts)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(collection, indent=2) + "\n", encoding="utf-8")
    scope = collection["scope"]
    print(
        f"OCR complete: {scope['processed_images']} images, "
        f"{len(scope['missing_images'])} missing."
    )
    print(f"Wrote {relative(output)}")


if __name__ == "__main__":
    main()
