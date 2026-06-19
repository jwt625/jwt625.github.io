#!/usr/bin/env python3
"""
Generic CLIP image description and metadata extraction for the blog image archive.

Outputs:
  - image_clip_results.jsonl: one image/description/metadata/score record per image
  - ranked_images.csv: compact spreadsheet-friendly image-description table
  - ranked_images.html: review contact sheet
  - clip_image_embeddings.npz: cached CLIP embeddings for incremental reruns

Install options, depending on your Python environment:
  pip install torch open_clip_torch pillow numpy

Example:
  python3 scripts/process_images_clip.py
  python3 scripts/process_images_clip.py --preset pie_charts --top 300
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from PIL import Image, ImageFile, UnidentifiedImageError

ImageFile.LOAD_TRUNCATED_IMAGES = True

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IMAGE_ROOT = REPO_ROOT / "assets/images"
DEFAULT_POST_ROOT = REPO_ROOT / "_posts"
DEFAULT_OUT_DIR = REPO_ROOT / "data/image_clip_index"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

PROMPT_PRESETS = {
    "general": {
        "description": "Broad image description and repository metadata extraction.",
        "target_prompts": [
            "a technical slide",
            "a scientific plot",
            "a line chart",
            "a bar chart",
            "a pie chart",
            "a table",
            "a flow diagram",
            "a schematic diagram",
            "a screenshot of a website or app",
            "a photograph of lab equipment",
            "a photograph of hardware",
            "a microscope image",
            "a wafer or chip photograph",
            "a circuit layout or CAD image",
            "a product photo",
            "a document page",
            "a logo or icon",
            "a map",
            "an equation or math derivation",
            "an optical or photonics diagram",
        ],
        "reference_prompts": [],
        "context_keywords": [],
        "threshold": 0.0,
        "margin": -1.0,
        "out_dir": DEFAULT_OUT_DIR,
        "output_prefix": "image",
    },
    "pie_charts": {
        "description": "Find likely pie/donut charts while preserving generic image metadata.",
        "target_prompts": [
            "a pie chart",
            "a donut chart",
            "a doughnut chart",
            "a circular percentage chart",
            "a circular chart with colored slices",
            "a market share pie chart",
            "a composition breakdown pie chart",
        ],
        "reference_prompts": [
            "a line chart",
            "a bar chart",
            "a scatter plot",
            "a table",
            "a scientific plot",
            "a flow diagram",
            "a technical diagram",
            "a screenshot of a website",
            "a photograph",
            "a microscope image",
            "a wafer photo",
            "a ring resonator diagram",
            "a circular object that is not a chart",
        ],
        "context_keywords": [
            "pie chart",
            "donut chart",
            "doughnut chart",
            "market share",
            "share of",
            "composition",
            "breakdown",
            "percentage",
            "percent",
            "budget",
            "spend",
            "revenue",
        ],
        "threshold": 0.20,
        "margin": 0.03,
        "out_dir": REPO_ROOT / "data/clip_pie_charts",
        "output_prefix": "pie_chart_candidate",
    },
}


@dataclass
class ImageInfo:
    path: Path
    rel_path: str
    size_bytes: int
    mtime_ns: int
    width: int | None = None
    height: int | None = None
    mode: str | None = None
    error: str | None = None

    @property
    def cache_key(self) -> str:
        raw = f"{self.rel_path}|{self.size_bytes}|{self.mtime_ns}".encode("utf-8")
        return hashlib.sha1(raw).hexdigest()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract image descriptions, CLIP scores, and repository metadata."
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_IMAGE_ROOT, help="Image root to scan.")
    parser.add_argument("--posts-root", type=Path, default=DEFAULT_POST_ROOT, help="Markdown root for reference/context extraction.")
    parser.add_argument("--out-dir", type=Path, default=None, help="Output directory. Defaults depend on --preset.")
    parser.add_argument(
        "--preset",
        choices=sorted(PROMPT_PRESETS),
        default="general",
        help="Prompt preset to use. Use pie_charts for the old pie/donut chart search.",
    )
    parser.add_argument(
        "--target-prompt",
        action="append",
        default=None,
        help="Override/add target description prompts. Repeat for multiple prompts.",
    )
    parser.add_argument(
        "--reference-prompt",
        action="append",
        default=None,
        help="Override/add reference prompts used to suppress false positives. Repeat for multiple prompts.",
    )
    parser.add_argument(
        "--context-keyword",
        action="append",
        default=None,
        help="Optional nearby-markdown keywords that add a small context boost. Repeat for multiple keywords.",
    )
    parser.add_argument("--top", type=int, default=400, help="Number of ranked images to include in the HTML contact sheet.")
    parser.add_argument("--limit", type=int, default=None, help="Process only the first N images, for smoke tests.")
    parser.add_argument("--batch-size", type=int, default=16, help="CLIP image batch size. Lower this if memory is tight.")
    parser.add_argument("--max-image-side", type=int, default=512, help="Downscale input images before CLIP preprocessing.")
    parser.add_argument("--device", choices=["auto", "cpu", "mps", "cuda"], default="auto", help="Torch device.")
    parser.add_argument("--model", default="ViT-B-32", help="open_clip model name.")
    parser.add_argument("--pretrained", default="openai", help="open_clip pretrained weights.")
    parser.add_argument("--threshold", type=float, default=None, help="Minimum target probability for candidate=true.")
    parser.add_argument("--margin", type=float, default=None, help="Minimum target-vs-reference or top-vs-runner-up probability margin.")
    parser.add_argument("--context-boost", type=float, default=0.025, help="Small score boost when nearby markdown text has chart keywords.")
    parser.add_argument(
        "--cache-save-every",
        type=int,
        default=25,
        help="Save embedding cache every N batches. Set to 1 for maximum interruption safety.",
    )
    parser.add_argument("--force", action="store_true", help="Recompute embeddings even when cache entries match.")
    parser.add_argument("--no-html", action="store_true", help="Skip HTML contact sheet generation.")
    return parser.parse_args()


def get_prompt_config(args: argparse.Namespace) -> dict[str, Any]:
    preset = PROMPT_PRESETS[args.preset]
    target_prompts = args.target_prompt or list(preset["target_prompts"])
    reference_prompts = args.reference_prompt or list(preset["reference_prompts"])
    context_keywords = args.context_keyword or list(preset["context_keywords"])
    threshold = preset["threshold"] if args.threshold is None else args.threshold
    margin = preset["margin"] if args.margin is None else args.margin
    out_dir = args.out_dir or preset["out_dir"]
    output_prefix = preset["output_prefix"]
    return {
        "preset": args.preset,
        "preset_description": preset["description"],
        "target_prompts": target_prompts,
        "reference_prompts": reference_prompts,
        "context_keywords": context_keywords,
        "threshold": threshold,
        "margin": margin,
        "out_dir": out_dir,
        "output_prefix": output_prefix,
    }


def require_clip_dependencies() -> tuple[Any, Any, Any]:
    missing = []
    try:
        import numpy as np
    except ImportError:
        missing.append("numpy")
        np = None
    try:
        import torch
    except ImportError:
        missing.append("torch")
        torch = None
    try:
        import open_clip
    except ImportError:
        missing.append("open_clip_torch")
        open_clip = None

    if missing:
        print(
            "Missing CLIP dependencies: "
            + ", ".join(missing)
            + "\nInstall with: pip install torch open_clip_torch pillow numpy",
            file=sys.stderr,
        )
        sys.exit(2)
    return np, torch, open_clip


def resolve_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def iter_images(root: Path, limit: int | None) -> list[ImageInfo]:
    root = resolve_path(root)
    images: list[ImageInfo] = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS:
            stat = path.stat()
            try:
                rel = path.relative_to(REPO_ROOT).as_posix()
            except ValueError:
                rel = path.as_posix()
            info = ImageInfo(
                path=path,
                rel_path=rel,
                size_bytes=stat.st_size,
                mtime_ns=stat.st_mtime_ns,
            )
            try:
                with Image.open(path) as img:
                    info.width, info.height = img.size
                    info.mode = img.mode
            except (OSError, UnidentifiedImageError) as exc:
                info.error = str(exc)
            images.append(info)
            if limit and len(images) >= limit:
                break
    return images


def extract_markdown_context(posts_root: Path) -> dict[str, list[dict[str, Any]]]:
    posts_root = resolve_path(posts_root)
    context_by_image: dict[str, list[dict[str, Any]]] = {}
    if not posts_root.exists():
        return context_by_image

    image_ref_pattern = re.compile(
        r"!\[(?P<alt>[^\]]*)\]\((?P<path>[^)\s]+)(?:\s+\"[^\"]*\")?\)"
        r"|<img\b[^>]*\bsrc=[\"'](?P<src>[^\"']+)[\"'][^>]*>",
        re.IGNORECASE,
    )

    for md_path in sorted(posts_root.rglob("*.md")):
        try:
            lines = md_path.read_text(encoding="utf-8").splitlines()
        except UnicodeDecodeError:
            lines = md_path.read_text(encoding="utf-8", errors="replace").splitlines()
        for idx, line in enumerate(lines):
            for match in image_ref_pattern.finditer(line):
                raw_path = match.group("path") or match.group("src") or ""
                image_path = normalize_image_ref(raw_path)
                if not image_path:
                    continue
                window = lines[max(0, idx - 2) : min(len(lines), idx + 3)]
                post_rel = md_path.relative_to(REPO_ROOT).as_posix()
                context_by_image.setdefault(image_path, []).append(
                    {
                        "post": post_rel,
                        "line": idx + 1,
                        "alt": match.group("alt") or "",
                        "nearby_text": "\n".join(window)[:1200],
                    }
                )
    return context_by_image


def normalize_image_ref(raw_path: str) -> str | None:
    raw_path = raw_path.split("#", 1)[0].split("?", 1)[0].strip()
    if not raw_path:
        return None
    if raw_path.startswith(("http://", "https://", "data:")):
        return None
    return raw_path.lstrip("/")


def choose_device(torch: Any, requested: str) -> str:
    if requested != "auto":
        return requested
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def load_embedding_cache(np: Any, cache_path: Path) -> dict[str, Any]:
    if not cache_path.exists():
        return {}
    try:
        data = np.load(cache_path, allow_pickle=False)
        keys = data["keys"].tolist()
        embeddings = data["embeddings"]
    except Exception as exc:
        backup_path = cache_path.with_suffix(cache_path.suffix + ".unreadable")
        cache_path.replace(backup_path)
        print(f"warning: moved unreadable cache to {backup_path}: {exc}", file=sys.stderr)
        return {}
    return {key: embeddings[i].astype("float32") for i, key in enumerate(keys)}


def save_embedding_cache(np: Any, cache_path: Path, cache: dict[str, Any]) -> None:
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    keys = sorted(cache)
    if keys:
        embeddings = np.stack([cache[key] for key in keys])
    else:
        embeddings = np.empty((0, 0), dtype="float32")
    tmp_path = cache_path.with_suffix(cache_path.suffix + ".tmp")
    with tmp_path.open("wb") as f:
        np.savez_compressed(f, keys=np.array(keys), embeddings=embeddings.astype("float32"))
        f.flush()
        os.fsync(f.fileno())
    tmp_path.replace(cache_path)


def prepare_image(path: Path, max_image_side: int) -> Image.Image:
    with Image.open(path) as img:
        img = img.convert("RGB")
        width, height = img.size
        longest = max(width, height)
        if longest > max_image_side:
            scale = max_image_side / longest
            new_size = (max(1, round(width * scale)), max(1, round(height * scale)))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        return img.copy()


def compute_missing_embeddings(
    *,
    np: Any,
    torch: Any,
    open_clip: Any,
    model: Any,
    preprocess: Any,
    images: list[ImageInfo],
    cache: dict[str, Any],
    batch_size: int,
    device: str,
    max_image_side: int,
    cache_path: Path,
    cache_save_every: int,
) -> tuple[dict[str, Any], int]:
    missing = [info for info in images if not info.error and info.cache_key not in cache]
    if not missing:
        return cache, 0

    start = time.time()
    done = 0
    model.eval()
    interrupted = False
    try:
        with torch.no_grad():
            for batch_index, offset in enumerate(range(0, len(missing), batch_size), start=1):
                batch_infos = missing[offset : offset + batch_size]
                tensors = []
                valid_infos = []
                for info in batch_infos:
                    try:
                        image = prepare_image(info.path, max_image_side)
                        tensors.append(preprocess(image))
                        valid_infos.append(info)
                    except Exception as exc:
                        info.error = f"load/preprocess failed: {exc}"
                if not tensors:
                    continue
                image_tensor = torch.stack(tensors).to(device)
                features = model.encode_image(image_tensor)
                features = features / features.norm(dim=-1, keepdim=True)
                features_np = features.detach().cpu().float().numpy()
                for info, embedding in zip(valid_infos, features_np):
                    cache[info.cache_key] = embedding.astype("float32")
                done += len(valid_infos)
                elapsed = max(time.time() - start, 1e-6)
                rate = done / elapsed
                remaining = (len(missing) - done) / rate if rate else math.nan
                print(
                    f"embedded {done}/{len(missing)} missing images "
                    f"({rate:.2f} img/s, ~{remaining/60:.1f} min remaining)",
                    flush=True,
                )
                if cache_save_every > 0 and batch_index % cache_save_every == 0:
                    save_embedding_cache(np, cache_path, cache)
                    print(f"checkpointed embedding cache: {cache_path}", flush=True)
    except KeyboardInterrupt:
        interrupted = True
        print("\ninterrupted; saving completed embeddings before exiting", file=sys.stderr)
    finally:
        if done:
            save_embedding_cache(np, cache_path, cache)
            print(f"saved embedding cache: {cache_path}", flush=True)
    if interrupted:
        raise KeyboardInterrupt
    return cache, done


def encode_text_prompts(
    np: Any,
    torch: Any,
    open_clip: Any,
    model: Any,
    model_name: str,
    device: str,
    target_prompts: list[str],
    reference_prompts: list[str],
) -> dict[str, Any]:
    prompts = target_prompts + reference_prompts
    if not prompts:
        raise ValueError("At least one target or reference prompt is required.")
    tokenizer = open_clip.get_tokenizer(model_name)
    with torch.no_grad():
        tokens = tokenizer(prompts).to(device)
        features = model.encode_text(tokens)
        features = features / features.norm(dim=-1, keepdim=True)
    text_features = features.detach().cpu().float().numpy()
    return {
        "prompts": prompts,
        "target_count": len(target_prompts),
        "reference_count": len(reference_prompts),
        "features": text_features,
    }


def softmax(np: Any, values: Any, temperature: float = 100.0) -> Any:
    scaled = values * temperature
    scaled = scaled - np.max(scaled)
    exp = np.exp(scaled)
    return exp / np.sum(exp)


def score_images(
    *,
    np: Any,
    images: list[ImageInfo],
    cache: dict[str, Any],
    text_bundle: dict[str, Any],
    context_by_image: dict[str, list[dict[str, Any]]],
    prompt_config: dict[str, Any],
    context_boost: float,
    model_name: str,
    pretrained: str,
    device: str,
) -> list[dict[str, Any]]:
    prompts = text_bundle["prompts"]
    target_count = text_bundle["target_count"]
    reference_count = text_bundle["reference_count"]
    text_features = text_bundle["features"]
    results = []
    run_metadata = {
        "model": model_name,
        "pretrained": pretrained,
        "device": device,
        "preset": prompt_config["preset"],
        "preset_description": prompt_config["preset_description"],
        "target_prompts": prompt_config["target_prompts"],
        "reference_prompts": prompt_config["reference_prompts"],
        "score_temperature": 100.0,
    }

    for info in images:
        refs = context_by_image.get(info.rel_path, [])
        context_text = "\n".join(
            [ref.get("alt", "") + "\n" + ref.get("nearby_text", "") for ref in refs]
        ).lower()
        keyword_hits = sorted({kw for kw in prompt_config["context_keywords"] if kw.lower() in context_text})
        boost = context_boost if keyword_hits else 0.0

        base = {
            "image": info.rel_path,
            "description": None,
            "candidate": False,
            "score": None,
            "clip": None,
            "extracted_metadata": {
                "repository_path": info.rel_path,
                "filename": info.path.name,
                "extension": info.path.suffix.lower(),
                "parent": info.path.parent.relative_to(REPO_ROOT).as_posix()
                if info.path.is_relative_to(REPO_ROOT)
                else info.path.parent.as_posix(),
            },
            "image_metadata": {
                "width": info.width,
                "height": info.height,
                "mode": info.mode,
                "size_bytes": info.size_bytes,
                "mtime_ns": info.mtime_ns,
                "cache_key": info.cache_key,
                "error": info.error,
            },
            "post_references": refs,
            "context_keyword_hits": keyword_hits,
            "run_metadata": run_metadata,
        }
        if info.error or info.cache_key not in cache:
            base["description"] = "unscored image"
            results.append(base)
            continue

        embedding = cache[info.cache_key]
        similarities = embedding @ text_features.T
        probabilities = softmax(np, similarities)
        target_probs = probabilities[:target_count]
        reference_probs = probabilities[target_count:]
        target_sims = similarities[:target_count]
        reference_sims = similarities[target_count:]

        best_target_idx = int(np.argmax(target_probs)) if target_count else None
        best_reference_idx = int(np.argmax(reference_probs)) + target_count if reference_count else None
        best_any_idx = int(np.argmax(probabilities))
        target_prob = float(np.max(target_probs)) if target_count else 0.0
        reference_prob = float(np.max(reference_probs)) if reference_count else 0.0
        target_sim = float(np.max(target_sims)) if target_count else 0.0
        reference_sim = float(np.max(reference_sims)) if reference_count else 0.0
        if reference_count:
            margin = target_prob - reference_prob
        elif len(probabilities) > 1:
            top_two = np.sort(probabilities)[-2:]
            margin = float(top_two[-1] - top_two[-2])
        else:
            margin = target_prob
        score = target_prob + margin + boost

        base["description"] = prompts[best_any_idx]
        base["score"] = float(score)
        base["clip"] = {
            "best_target_prompt": prompts[best_target_idx] if best_target_idx is not None else None,
            "best_reference_prompt": prompts[best_reference_idx] if best_reference_idx is not None else None,
            "best_overall_prompt": prompts[best_any_idx],
            "target_probability": target_prob,
            "reference_probability": reference_prob,
            "probability_margin": float(margin),
            "target_similarity": target_sim,
            "reference_similarity": reference_sim,
            "similarity_margin": float(target_sim - reference_sim),
            "context_boost": boost,
            "prompt_scores": [
                {
                    "prompt": prompt,
                    "similarity": float(similarities[i]),
                    "probability": float(probabilities[i]),
                    "role": "target" if i < target_count else "reference",
                }
                for i, prompt in enumerate(prompts)
            ],
        }
        results.append(base)
    return results


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
        f.flush()
        os.fsync(f.fileno())
    tmp_path.replace(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "rank",
        "score",
        "image",
        "description",
        "target_probability",
        "reference_probability",
        "probability_margin",
        "best_target_prompt",
        "best_reference_prompt",
        "best_overall_prompt",
        "width",
        "height",
        "extension",
        "size_bytes",
        "references",
        "context_keyword_hits",
    ]
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for rank, row in enumerate(rows, start=1):
            clip = row.get("clip") or {}
            meta = row.get("image_metadata") or {}
            writer.writerow(
                {
                    "rank": rank,
                    "score": row.get("score"),
                    "image": row.get("image"),
                    "description": row.get("description"),
                    "target_probability": clip.get("target_probability"),
                    "reference_probability": clip.get("reference_probability"),
                    "probability_margin": clip.get("probability_margin"),
                    "best_target_prompt": clip.get("best_target_prompt"),
                    "best_reference_prompt": clip.get("best_reference_prompt"),
                    "best_overall_prompt": clip.get("best_overall_prompt"),
                    "width": meta.get("width"),
                    "height": meta.get("height"),
                    "extension": (row.get("extracted_metadata") or {}).get("extension"),
                    "size_bytes": meta.get("size_bytes"),
                    "references": "; ".join(
                        f"{ref.get('post')}:{ref.get('line')}" for ref in row.get("post_references", [])
                    ),
                    "context_keyword_hits": ", ".join(row.get("context_keyword_hits", [])),
                }
            )
        f.flush()
        os.fsync(f.fileno())
    tmp_path.replace(path)


def image_uri(rel_path: str) -> str:
    return "../../" + rel_path


def write_html(path: Path, rows: list[dict[str, Any]], top: int, title: str, subtitle: str) -> None:
    shown = rows[:top]
    cards = []
    for rank, row in enumerate(shown, start=1):
        rel = row["image"]
        clip = row.get("clip") or {}
        meta = row.get("image_metadata") or {}
        refs = row.get("post_references") or []
        ref_text = "<br>".join(
            html.escape(f"{ref.get('post')}:{ref.get('line')} {ref.get('alt') or ''}") for ref in refs[:4]
        )
        cards.append(
            f"""
            <article class="card">
              <a href="{html.escape(image_uri(rel))}" target="_blank">
                <img loading="lazy" src="{html.escape(image_uri(rel))}" alt="{html.escape(rel)}">
              </a>
              <div class="meta">
                <div><b>#{rank}</b> score {row.get('score', 0):.4f}</div>
                <div>{html.escape(row.get('description') or '')}</div>
                <code>{html.escape(rel)}</code>
                <div>target {clip.get('target_probability', 0):.4f} / ref {clip.get('reference_probability', 0):.4f} / margin {clip.get('probability_margin', 0):.4f}</div>
                <div>{meta.get('width')}x{meta.get('height')}</div>
                <div class="refs">{ref_text}</div>
              </div>
            </article>
            """
        )
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    body {{
      margin: 24px;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: #202124;
      background: #f7f7f4;
    }}
    h1 {{ font-size: 24px; margin: 0 0 8px; }}
    p {{ margin: 0 0 20px; color: #555; }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 14px;
      align-items: start;
    }}
    .card {{
      background: #fff;
      border: 1px solid #ddd;
      border-radius: 6px;
      overflow: hidden;
    }}
    img {{
      display: block;
      width: 100%;
      height: 220px;
      object-fit: contain;
      background: #eee;
      border-bottom: 1px solid #ddd;
    }}
    .meta {{
      padding: 10px;
      font-size: 13px;
      line-height: 1.35;
    }}
    code {{
      display: block;
      margin: 6px 0;
      overflow-wrap: anywhere;
      color: #0b57d0;
    }}
    .refs {{
      margin-top: 6px;
      color: #666;
      overflow-wrap: anywhere;
    }}
  </style>
</head>
<body>
  <h1>{html.escape(title)}</h1>
  <p>{html.escape(subtitle)}</p>
  <main class="grid">
    {''.join(cards)}
  </main>
</body>
</html>
"""
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        f.write(page)
        f.flush()
        os.fsync(f.fileno())
    tmp_path.replace(path)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    tmp_path.replace(path)


def main() -> int:
    args = parse_args()
    prompt_config = get_prompt_config(args)
    np, torch, open_clip = require_clip_dependencies()

    image_root = resolve_path(args.root)
    posts_root = resolve_path(args.posts_root)
    out_dir = resolve_path(prompt_config["out_dir"])
    out_dir.mkdir(parents=True, exist_ok=True)
    cache_path = out_dir / "clip_image_embeddings.npz"

    print(f"scanning images under {image_root}")
    images = iter_images(image_root, args.limit)
    print(f"found {len(images)} images")
    print(f"extracting markdown context under {posts_root}")
    context_by_image = extract_markdown_context(posts_root)

    device = choose_device(torch, args.device)
    print(f"loading CLIP model {args.model}/{args.pretrained} on {device}")
    model, _, preprocess = open_clip.create_model_and_transforms(
        args.model,
        pretrained=args.pretrained,
        device=device,
    )

    if args.force and cache_path.exists():
        cache = {}
    else:
        print(f"loading embedding cache {cache_path}")
        cache = load_embedding_cache(np, cache_path)
        print(f"cache entries: {len(cache)}")

    try:
        cache, computed = compute_missing_embeddings(
            np=np,
            torch=torch,
            open_clip=open_clip,
            model=model,
            preprocess=preprocess,
            images=images,
            cache=cache,
            batch_size=args.batch_size,
            device=device,
            max_image_side=args.max_image_side,
            cache_path=cache_path,
            cache_save_every=args.cache_save_every,
        )
    except KeyboardInterrupt:
        interrupted_path = out_dir / "interrupted_run_summary.json"
        write_json(
            interrupted_path,
            {
                "status": "interrupted",
                "message": "Embedding cache was checkpointed. Re-run the same command to resume.",
                "repo_root": REPO_ROOT.as_posix(),
                "image_root": image_root.as_posix(),
                "out_dir": out_dir.as_posix(),
                "image_count": len(images),
                "cache_entries": len(cache),
                "embedding_cache": cache_path.as_posix(),
                "preset": prompt_config["preset"],
                "model": args.model,
                "pretrained": args.pretrained,
                "device": device,
                "batch_size": args.batch_size,
                "max_image_side": args.max_image_side,
            },
        )
        print(f"interrupted; resume by re-running the command. Summary: {interrupted_path}", file=sys.stderr)
        return 130
    if computed:
        print(f"saving embedding cache with {len(cache)} entries")
        save_embedding_cache(np, cache_path, cache)

    print("encoding text prompts and scoring images")
    text_bundle = encode_text_prompts(
        np,
        torch,
        open_clip,
        model,
        args.model,
        device,
        prompt_config["target_prompts"],
        prompt_config["reference_prompts"],
    )
    results = score_images(
        np=np,
        images=images,
        cache=cache,
        text_bundle=text_bundle,
        context_by_image=context_by_image,
        prompt_config=prompt_config,
        context_boost=args.context_boost,
        model_name=args.model,
        pretrained=args.pretrained,
        device=device,
    )

    scored = [row for row in results if row.get("score") is not None and row.get("clip")]
    for row in scored:
        clip = row["clip"]
        row["candidate"] = (
            clip["target_probability"] >= prompt_config["threshold"]
            and clip["probability_margin"] >= prompt_config["margin"]
        )
    ranked = sorted(
        scored,
        key=lambda row: row["score"],
        reverse=True,
    )
    candidates = sorted(
        [row for row in scored if row["candidate"]],
        key=lambda row: row["score"],
        reverse=True,
    )
    all_sorted = sorted(
        results,
        key=lambda row: row["score"] if row.get("score") is not None else -999,
        reverse=True,
    )

    prefix = prompt_config["output_prefix"]
    all_path = out_dir / "image_clip_results.jsonl"
    candidates_path = out_dir / f"{prefix}s.jsonl"
    csv_path = out_dir / "ranked_images.csv"
    html_path = out_dir / "ranked_images.html"
    run_path = out_dir / "run_summary.json"

    write_jsonl(all_path, all_sorted)
    write_jsonl(candidates_path, candidates)
    write_csv(csv_path, ranked)
    if not args.no_html:
        title = f"CLIP Image Index: {prompt_config['preset']}"
        subtitle = (
            f"Top {min(args.top, len(ranked))} of {len(ranked)} scored images. "
            f"{len(candidates)} rows satisfy candidate thresholds."
        )
        write_html(html_path, ranked, args.top, title, subtitle)

    summary = {
        "repo_root": REPO_ROOT.as_posix(),
        "image_root": image_root.as_posix(),
        "posts_root": posts_root.as_posix(),
        "out_dir": out_dir.as_posix(),
        "preset": prompt_config["preset"],
        "preset_description": prompt_config["preset_description"],
        "target_prompts": prompt_config["target_prompts"],
        "reference_prompts": prompt_config["reference_prompts"],
        "context_keywords": prompt_config["context_keywords"],
        "image_count": len(images),
        "scored_count": len(scored),
        "candidate_count": len(candidates),
        "threshold": prompt_config["threshold"],
        "margin": prompt_config["margin"],
        "context_boost": args.context_boost,
        "model": args.model,
        "pretrained": args.pretrained,
        "device": device,
        "batch_size": args.batch_size,
        "max_image_side": args.max_image_side,
        "outputs": {
            "image_clip_results": all_path.as_posix(),
            "candidates_jsonl": candidates_path.as_posix(),
            "ranked_csv": csv_path.as_posix(),
            "ranked_html": None if args.no_html else html_path.as_posix(),
            "embedding_cache": cache_path.as_posix(),
        },
    }
    write_json(run_path, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
