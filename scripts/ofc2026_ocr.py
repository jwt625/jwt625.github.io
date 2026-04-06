#!/opt/homebrew/bin/python3

from __future__ import annotations

import html
import json
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from PIL import Image
from PIL.ExifTags import TAGS


REPO_ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = REPO_ROOT / "assets/images/2026/OFC2026"
POST_PATH = REPO_ROOT / "_posts/2026-04-04-OFC2026.md"
METADATA_PATH = REPO_ROOT / "_data/ofc2026_ocr.json"

DAY_TITLES = {
    "2026-03-15": "Sunday, March 15, 2026",
    "2026-03-16": "Monday, March 16, 2026",
    "2026-03-17": "Tuesday, March 17, 2026",
    "2026-03-18": "Wednesday, March 18, 2026",
    "2026-03-19": "Thursday, March 19, 2026",
    "2026-03-20": "Friday, March 20, 2026",
}

DAY_NOTES = {
    "2026-03-15": [
        "Went to the CPO session before the demo. marvell is spending a whole session talking about photonics for scale-up",
        "someone just asked nvidia's speaker when can he order a CPO switch",
        "the Q&A session is gold:",
        "Whats your burning strategy?",
        "Industry best practice.",
        "So is it the same as the cisco folks?",
        "The demo session was successful. Gave my talk to at least three different waves of people. Many took picture of my websites. I should have added QR codes for the websites.",
    ],
    "2026-03-16": [
        "Had leftover from yesterday lunch (mexican food across the street from the Metra Plaza Hotel).",
        "Tried to go to google's session and it was filled up",
        "Then went to room ~401 for optical switching, there was an n-eye talk.",
        "Then during lunch met people from industry and networking. Lunch break is so fun.",
    ],
    "2026-03-17": [
        "Went to a Chinese/Vietnanese coffee shop and got a banana matcha and bacon cheese croissant, good stuff.",
        "Also saw a lightmatter ads truck on the way to the conference lol.",
        "First took a meeting at the conference, then walked around the show room.",
        "In the afternoon mainly sit thru two big sessions, one on recent advances in AI cluster interconnects, mainly different ads for their own stuff.",
    ],
    "2026-03-18": [
        "Same noise from upstair since 4 am. Also no warm water in the morning for showering. Took the first cold shower in a long time.",
        "Walked around the show room in the morning, saw Arista's XPO. Then took a look thru the poster session.",
        "Then went to a PCSEL session, listened to two talks. Then went to an inter-datacenter training run session, but I was too hungry and distracted.",
        "A lot of meetings today.",
    ],
    "2026-03-19": [
        "Woke up early, got there, and caught the talk.",
        "good talk",
        "Went to theater talk in the expo, on liquid cooled pluggable from ciena lol.",
        "Then went to a AIDC networking session. Some cool diagnostic talks from Alibaba and other China cloud companies.",
    ],
    "2026-03-20": [
        "A few screenshots and supplemental images were saved after the conference itself.",
    ],
}

IMAGE_NOTES_BEFORE = {
    "IMG_3965.JPG": [
        "Should also have added my email info. Should also have made a demo website with the slides and the links.",
        "Many people have very different usage of claude code, mostly still in web page. I showed it creating a postgres from scratch in 2 min for managing photonics experimental data, and then creating a web UI for it.",
    ],
    "IMG_3967.JPG": [
        "Also made people play my SLM guessr, it's quite fun."
    ],
    "IMG_3981.JPG": [
        "Then went to room ~401 for optical switching, there was an n-eye talk."
    ],
    "IMG_3990.JPG": [
        "After lunch, went to the space FSO session, talk from space X, very impressive fleet and topology. He got a question on whether they are using laser for ground-satellite comm, and he said he cannot say."
    ],
    "IMG_4008.JPG": [
        "Another talk in the same session says $7-10 trillion in economic impact in coming years"
    ],
    "IMG_4011.JPG": [
        "Then went to an Nvidia talk on OCS in scale up/out/across domain's role. It had a disclaimer at the beginning stating it's his personal view lol."
    ],
    "IMG_4020.JPG": [
        "Then walked around the expo, not ready yet, but I went to the EDWATEC booth and chatted with them for quite a while, talked thru some technical stuff, my experience etc."
    ],
    "IMG_4021.JPG": [
        "Then took another look in the OCS session. Some crazy shit from UC Davis from S.J. Ben Yoo."
    ],
    "IMG_4029.JPG": [
        "Coherent has some crazy thin TEC. And some really cute nanoITLA.",
        "Met quite a few waves of people while standing and eating, one mentioned they use PON for management/OOB network in DC, and they can do branching with TDM just like in PON access networking, which seems to make sense for me.",
    ],
    "IMG_4049.JPG": [
        "Then went back to expo and chatted with Taara technical guy.",
        "Also chatted with NanoLN founder & CEO, they have a beautiful 12 in wafer.",
    ],
    "IMG_4051.JPG": [
        "Arista's XPO is news to me (later today learnt the google team got a demo first, from the Sun founder himself on a whiteboard lol)"
    ],
    "IMG_4076.JPG": [
        "Second session I sat was on optical scale-up from hyperscaler to solutions provider to packaging supplier, quite good.",
        "meta, microsoft, broadcom, lumentum, celestial/marvel, GF, ASE, Jabil.",
        "a lot of mention of OCI-MS",
    ],
    "IMG_4083.JPG": [
        "broadcom's talk is pretty good, showed their assembly flow and prod readiness"
    ],
    "IMG_4087.JPG": [
        "lumentum is ofc biased, and looks similar to Manchen's startup"
    ],
    "IMG_4092.JPG": [
        "marvel/celectial is future looking and beyond CPO."
    ],
    "IMG_4116.JPG": [
        "GF showed a lot of pretty pictures, I asked a question on tradeoff between lateral alignment and angular alignment, got answer that industry has settled with 30~40 um beam size."
    ],
    "IMG_4129.JPG": [
        "ASE showed a funny table of top 10 market cap stock in 2006 vs 2026, much of the AIDC capex, many of Jensen's arguments, are bottlenecked by energy. Time for a new wave of energy companies for the next 20 years?"
    ],
    "IMG_4140.JPG": [
        "Walked around the show room in the morning, saw Arista's XPO."
    ],
    "IMG_4144.JPG": [
        "Sat in the theater 1 in the afternoon, about packaging. Not much new stuff, just different vendors/suppliers selling their stuff."
    ],
    "IMG_4152.JPG": [
        "Then went to a PCSEL session, listened to two talks. I wanted to ask how big can they scale the size, but session ran out of time and did not get to."
    ],
    "IMG_4156.JPG": [
        "kW pulsed power possible.",
        "~50% ideal, ~40% actual efficiency",
    ],
    "IMG_4160.JPG": [
        "Then went to an inter-datacenter training run session, but I was too hungry and distracted.",
        "Should reduce twitter usage.",
    ],
    "IMG_4181.JPG": [
        "Then got coffee and bread, and went to theater talk in the expo, on liquid cooled pluggable from ciena lol."
    ],
    "IMG_4186.JPG": [
        "also saw Smart Photonics's 110 GHz modulator"
    ],
    "IMG_4193.JPG": [
        "Then went to a AIDC networking session. Some cool diagnostic talks from Alibaba and other China cloud companies.",
        "showed reliability of VCSEL/EML/SiPho optics, should share this to lambda team",
    ],
    "IMG_4197.JPG": [
        "baidu showed an LLM assisted root cause localization"
    ],
    "IMG_4205.JPG": [
        "Netpreme showed network memory tiering",
        "separating GPU and memory",
        "NUMA node, HBM on another machine, could use old memory",
    ],
    "IMG_4209.JPG": [
        "work with Nvidia, hyperscalers as well as neoclouds"
    ],
    "IMG_4210.JPG": [
        "current web service is simulated with 8xH100 by turning off 2 GPUs"
    ],
    "IMG_4201.PNG": [
        "These PNG screenshots do not carry EXIF capture metadata, so they are dated using filesystem modification time."
    ],
}

SWIFT_SOURCE = r"""
import AppKit
import Foundation
import Vision

struct OCRResult: Codable {
    let filename: String
    let imagePath: String
    let lines: [String]
    let error: String?
}

func recognizeText(at path: String) -> OCRResult {
    let url = URL(fileURLWithPath: path)

    guard let image = NSImage(contentsOf: url) else {
        return OCRResult(filename: url.lastPathComponent, imagePath: path, lines: [], error: "Failed to load image")
    }

    guard let tiff = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: tiff),
          let cgImage = bitmap.cgImage else {
        return OCRResult(filename: url.lastPathComponent, imagePath: path, lines: [], error: "Failed to create CGImage")
    }

    let request = VNRecognizeTextRequest()
    request.recognitionLevel = .accurate
    request.usesLanguageCorrection = true
    request.recognitionLanguages = ["en-US"]

    let handler = VNImageRequestHandler(cgImage: cgImage, options: [:])

    do {
        try handler.perform([request])
        let observations = request.results ?? []
        let lines = observations.compactMap { observation -> String? in
            observation.topCandidates(1).first?.string
        }
        return OCRResult(filename: url.lastPathComponent, imagePath: path, lines: lines, error: nil)
    } catch {
        return OCRResult(filename: url.lastPathComponent, imagePath: path, lines: [], error: String(describing: error))
    }
}

let imagePaths = Array(CommandLine.arguments.dropFirst())
let results = imagePaths.map(recognizeText)
let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys]

do {
    let data = try encoder.encode(results)
    FileHandle.standardOutput.write(data)
} catch {
    fputs("Failed to encode OCR results: \(error)\n", stderr)
    exit(1)
}
"""


@dataclass
class OCRItem:
    filename: str
    image_path: str
    lines: list[str]
    error: str | None
    capture_dt: datetime | None
    date_source: str
    filesystem_modified: datetime

    @property
    def text(self) -> str:
        return "\n".join(self.lines).strip()

    @property
    def has_text(self) -> bool:
        return bool(self.text)

    @property
    def image_url(self) -> str:
        return "/" + self.image_path.replace("\\", "/")

    @property
    def capture_date(self) -> str:
        dt = self.capture_dt or self.filesystem_modified
        return dt.strftime("%Y-%m-%d")

    @property
    def capture_time(self) -> str:
        dt = self.capture_dt or self.filesystem_modified
        return dt.strftime("%H:%M:%S")

    @property
    def conference_day(self) -> str | None:
        if self.capture_date in DAY_TITLES and self.capture_date <= "2026-03-19":
            return DAY_TITLES[self.capture_date]
        return None


def list_images() -> list[Path]:
    return sorted(
        [*IMAGE_DIR.glob("*.JPG"), *IMAGE_DIR.glob("*.PNG")],
        key=lambda path: path.name,
    )


def extract_capture_datetime(path: Path) -> tuple[datetime | None, str, datetime]:
    filesystem_modified = datetime.fromtimestamp(path.stat().st_mtime)
    try:
        image = Image.open(path)
        exif = image.getexif()
        exif_map = {TAGS.get(key, key): value for key, value in exif.items()}
        for field in ("DateTimeOriginal", "DateTimeDigitized", "DateTime"):
            value = exif_map.get(field)
            if value:
                return datetime.strptime(value, "%Y:%m:%d %H:%M:%S"), f"EXIF:{field}", filesystem_modified
    except Exception:
        pass
    return None, "filesystem_modified", filesystem_modified


def run_ocr(image_paths: list[Path]) -> list[OCRItem]:
    with tempfile.TemporaryDirectory(prefix="ofc2026_ocr_") as tmpdir:
        swift_path = Path(tmpdir) / "vision_ocr.swift"
        swift_path.write_text(SWIFT_SOURCE, encoding="utf-8")
        cmd = ["swift", str(swift_path), *[str(path) for path in image_paths]]
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(completed.stderr.strip() or "Swift OCR command failed")

    raw_items = json.loads(completed.stdout)
    items: list[OCRItem] = []
    for raw_item in raw_items:
        image_path = Path(raw_item["imagePath"]).resolve()
        relative_image_path = image_path.relative_to(REPO_ROOT).as_posix()
        capture_dt, date_source, filesystem_modified = extract_capture_datetime(image_path)
        item = OCRItem(
            filename=raw_item["filename"],
            image_path=relative_image_path,
            lines=raw_item.get("lines", []),
            error=raw_item.get("error"),
            capture_dt=capture_dt,
            date_source=date_source,
            filesystem_modified=filesystem_modified,
        )
        items.append(item)
    return items


def build_metadata(items: list[OCRItem]) -> list[dict[str, object]]:
    metadata: list[dict[str, object]] = []
    for item in items:
        metadata.append(
            {
                "filename": item.filename,
                "image_path": item.image_url,
                "capture_date": item.capture_date,
                "capture_time": item.capture_time,
                "date_source": item.date_source,
                "conference_day": item.conference_day,
                "filesystem_modified": item.filesystem_modified.isoformat(timespec="seconds"),
                "ocr_text": item.text,
                "ocr_lines": item.lines,
                "has_text": item.has_text,
                "error": item.error,
            }
        )
    return metadata


def add_paragraphs(lines: list[str], paragraphs: list[str]) -> None:
    for paragraph in paragraphs:
        lines.extend([paragraph, ""])


def add_image_block(lines: list[str], item: OCRItem) -> None:
    lines.extend(
        [
            f"### {item.filename}",
            "",
            f"Captured: `{item.capture_date} {item.capture_time}`",
            f"Date source: `{item.date_source}`",
            "",
            '   <div style="display: flex; flex-direction: row; gap: 10px;">',
            f'     <img src="{item.image_url}" alt="{item.filename}" style="width: 32%; max-width: 100%; height: auto;">',
            "   </div>",
            "",
        ]
    )

    if item.has_text:
        escaped_text = html.escape(item.text)
        lines.extend(
            [
                "<details>",
                "  <summary>Detected text</summary>",
                "",
                f"  <pre>{escaped_text}</pre>",
                "</details>",
                "",
            ]
        )
    elif item.error:
        lines.extend([f"OCR error: `{item.error}`", ""])
    else:
        lines.extend(["No OCR text detected.", ""])


def build_post(items: list[OCRItem]) -> str:
    lines: list[str] = [
        "---",
        'title: "OFC 2026"',
        "categories:",
        "  - Blog",
        "tags:",
        "  - OFC",
        "  - Photonics",
        "  - Optical_Communications",
        "  - Silicon_Photonics",
        "  - Datacenter",
        "toc: true",
        "toc_sticky: True",
        "use_math: true",
        "header:",
        "  cover: /assets/images/2026/OFC2026/IMG_3967.JPG",
        "  overlay_image: /assets/images/2026/OFC2026/IMG_3967.JPG",
        "  show_overlay_excerpt: false",
        "  overlay_filter: 0.5",
        "---",
        "",
        "# OFC 2026",
        "",
        "https://www.ofcconference.org/",
        "",
        "This post follows the photo roll from OFC 2026 in chronological order. I grouped the images by capture date, added a few cleaned notes from the week, and kept the locally extracted OCR text in collapsible blocks for later search and reference.",
        "",
        "The main conference ran from March 15 to March 19, 2026. Most images have EXIF timestamps; the PNG screenshots near the end do not, so those are dated using filesystem modification time instead.",
        "",
        f"Metadata export: [`_data/ofc2026_ocr.json`](/Users/wentaojiang/Documents/GitHub/jwt625.github.io/_data/ofc2026_ocr.json)",
        "",
    ]

    current_day = None
    for item in items:
        if item.capture_date != current_day:
            current_day = item.capture_date
            day_title = DAY_TITLES.get(current_day, current_day)
            lines.extend([f"## {day_title}", ""])
            add_paragraphs(lines, DAY_NOTES.get(current_day, []))

        add_paragraphs(lines, IMAGE_NOTES_BEFORE.get(item.filename, []))
        add_image_block(lines, item)

    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    image_paths = list_images()
    if not image_paths:
        raise SystemExit("No OFC 2026 images found.")

    items = run_ocr(image_paths)
    metadata = build_metadata(items)

    METADATA_PATH.write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    POST_PATH.write_text(build_post(items), encoding="utf-8")

    print(f"OCR complete for {len(items)} images.")
    print(f"Wrote metadata to {METADATA_PATH}")
    print(f"Wrote post to {POST_PATH}")


if __name__ == "__main__":
    main()
