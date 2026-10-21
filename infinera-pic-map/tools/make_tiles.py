"""Build a WebP tile pyramid for the Infinera PIC micrograph.

Usage: uv run --with pillow python make_tiles.py SRC.jpg OUT_DIR [--quality 72] [--tile 512] [--sample N]
Level 0 is a single tile; the last level is native resolution. The source carries an EXIF
orientation tag, so it is transposed to display orientation first.
"""
import argparse
import json
import math
import time
from pathlib import Path

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("out")
    ap.add_argument("--quality", type=int, default=72)
    ap.add_argument("--tile", type=int, default=512)
    ap.add_argument("--sample", type=int, default=0, help="only encode N tiles of the top level, report size")
    a = ap.parse_args()
    t0 = time.time()
    im = ImageOps.exif_transpose(Image.open(a.src)).convert("RGB")
    W, H = im.size
    T = a.tile
    nlev = math.ceil(math.log2(max(W, H) / T)) + 1
    out = Path(a.out)
    print(f"loaded {W}x{H} in {time.time() - t0:.1f}s, {nlev} levels")
    total = 0
    cur = im
    for lev in range(nlev - 1, -1, -1):
        s = 2 ** (nlev - 1 - lev)
        w, h = math.ceil(W / s), math.ceil(H / s)
        if cur.size != (w, h):
            cur = cur.resize((w, h), Image.LANCZOS)
        nx, ny = math.ceil(w / T), math.ceil(h / T)
        d = out / str(lev)
        d.mkdir(parents=True, exist_ok=True)
        idx = [(x, y) for y in range(ny) for x in range(nx)]
        if a.sample:
            idx = idx[len(idx) // 2: len(idx) // 2 + a.sample]
        for x, y in idx:
            p = d / f"{x}_{y}.webp"
            if p.exists() and not a.sample:
                total += p.stat().st_size
                continue
            cur.crop((x * T, y * T, min(w, (x + 1) * T), min(h, (y + 1) * T))).save(p, "WEBP", quality=a.quality, method=4)
            total += p.stat().st_size
        print(f"level {lev}: {w}x{h}, {nx}x{ny} tiles, cum {total / 1e6:.1f} MB, {time.time() - t0:.0f}s")
        if a.sample:
            print(f"sample avg {total / len(idx) / 1e3:.1f} kB/tile, est top level {total / len(idx) * nx * ny / 1e6:.1f} MB")
            return
    (out / "manifest.json").write_text(json.dumps({"width": W, "height": H, "tile": T, "levels": nlev, "format": "webp"}))
    print(f"done {total / 1e6:.1f} MB in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
