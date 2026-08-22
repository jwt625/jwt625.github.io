#!/usr/bin/env python3
"""Rebuild the original network-conversions graphic from its PPTX assets."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


REPO_ROOT = Path(__file__).resolve().parents[1]
ASSET_DIR = REPO_ROOT / "assets/images/2025/20251219_CPO"
COMPONENT_DIR = ASSET_DIR / "network-conversions-components"
OUTPUT = ASSET_DIR / "network-conversions.webp"

WIDTH, HEIGHT = 1600, 900
SLIDE_WIDTH, SLIDE_HEIGHT = 9_144_000, 5_143_500
FONT_REGULAR = "/System/Library/Fonts/Supplemental/Arial.ttf"
FONT_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"


def px_x(value: int) -> int:
    return round(value * WIDTH / SLIDE_WIDTH)


def px_y(value: int) -> int:
    return round(value * HEIGHT / SLIDE_HEIGHT)


def box(x: int, y: int, width: int, height: int) -> tuple[int, int, int, int]:
    return px_x(x), px_y(y), px_x(width), px_y(height)


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REGULAR, size)


def load(name: str) -> Image.Image:
    return Image.open(COMPONENT_DIR / name).convert("RGBA")


def place(canvas: Image.Image, image: Image.Image, placement: tuple[int, int, int, int]) -> None:
    x, y, width, height = placement
    resized = image.resize((width, height), Image.Resampling.LANCZOS)
    canvas.alpha_composite(resized, (x, y))


def make_miniature(width: int, height: int) -> Image.Image:
    """Make the tiny page visible in each laptop without using the old composite."""
    miniature = Image.new("RGBA", (width, height), "white")
    map_image = load("submarine-cable-map.webp").resize((width, height), Image.Resampling.LANCZOS)
    map_image.putalpha(32)
    miniature.alpha_composite(map_image)

    database = load("cloud-database.png")
    laptop = load("laptop.png")
    eye = load("viewer-eye.png")
    arrow = load("bidirectional-arrow-small.png")
    wave = load("optical-wave-up.png")

    place(miniature, database, (round(width * 0.04), round(height * 0.28), round(width * 0.17), round(height * 0.30)))
    place(miniature, laptop, (round(width * 0.20), round(height * 0.34), round(width * 0.31), round(height * 0.48)))
    place(miniature, laptop, (round(width * 0.50), round(height * 0.20), round(width * 0.31), round(height * 0.48)))
    place(miniature, laptop, (round(width * 0.50), round(height * 0.52), round(width * 0.31), round(height * 0.48)))
    place(miniature, arrow, (round(width * 0.17), round(height * 0.44), round(width * 0.11), round(height * 0.20)))
    place(miniature, wave, (round(width * 0.76), round(height * 0.28), round(width * 0.15), round(height * 0.24)))
    place(miniature, eye, (round(width * 0.87), round(height * 0.25), round(width * 0.11), round(height * 0.22)))
    place(miniature, eye, (round(width * 0.87), round(height * 0.61), round(width * 0.11), round(height * 0.22)))
    return miniature


def main() -> None:
    canvas = Image.new("RGBA", (WIDTH, HEIGHT), "white")

    # Original slide placements, converted directly from EMU coordinates.
    background = load("submarine-cable-map.webp")
    background.putalpha(39)
    place(canvas, background, box(0, -251_550, 9_144_003, 6_032_009))

    place(canvas, load("cloud-database.png"), box(559_600, 1_149_575, 1_453_001, 1_453_001))
    place(canvas, load("bidirectional-arrow-small.png"), box(1_412_325, 1_928_875, 1_346_624, 1_345_675))
    place(canvas, load("bidirectional-arrow-large.png"), box(3_991_775, 2_513_675, 1_066_650, 1_066_650))
    place(canvas, load("optical-wave-up.png"), box(5_829_125, 588_212, 2_661_325, 2_558_525))
    place(canvas, load("optical-wave-down.png"), box(5_988_993, 2_850_926, 2_341_574, 2_238_699))
    place(canvas, load("viewer-eye.png"), box(7_591_776, 1_102_800, 1_136_926, 1_066_649))
    place(canvas, load("viewer-eye.png"), box(7_591_776, 3_589_350, 1_136_926, 1_066_649))

    laptop = load("laptop.png")
    laptop_boxes = [
        box(1_775_069, 1_369_146, 2_750_015, 2_659_534),
        box(4_375_594, 931_621, 2_750_015, 2_659_534),
        box(4_375_594, 2_474_246, 2_750_015, 2_659_534),
    ]
    screen_boxes = [
        box(2_537_227, 2_171_821, 1_226_070, 685_325),
        box(5_137_752, 1_734_296, 1_226_070, 685_325),
        box(5_137_752, 3_276_921, 1_226_070, 685_325),
    ]
    for laptop_box, screen_box in zip(laptop_boxes, screen_boxes):
        place(canvas, laptop, laptop_box)
        x, y, width, height = screen_box
        canvas.alpha_composite(make_miniature(width, height), (x, y))

    draw = ImageDraw.Draw(canvas)
    draw.text((px_x(338_400), px_y(615_298)), "How are you seeing this presentation?", font=font(62, bold=True), fill="black")
    draw.text(
        (px_x(1_412_325), px_y(4_720_325)),
        "(chatGPT: about 50 E-O conversions, ~ 40 in ISP/backbone/Google)",
        font=font(25),
        fill="black",
    )

    canvas.convert("RGB").save(OUTPUT, "WEBP", quality=90, method=6)
    print(OUTPUT)


if __name__ == "__main__":
    main()
