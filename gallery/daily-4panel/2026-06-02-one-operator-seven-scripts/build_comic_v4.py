from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent

PANEL_FILES = [
    "panel-1-v4.png",
    "panel-2-v4.png",
    "panel-3-v4.png",
    "panel-4-v4.png",
]

OUT = ROOT / "comic-v4.png"
REVIEW_OUT = ROOT / "comic-v4-review.png"

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"
FONT_FALLBACK = "/System/Library/Fonts/Supplemental/ChalkboardSE.ttc"

BLACK = (18, 18, 18)
GRAY = (220, 220, 220)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in (FONT_REGULAR, FONT_FALLBACK):
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def main() -> None:
    panels = [Image.open(ROOT / filename).convert("RGB") for filename in PANEL_FILES]
    width, height = panels[0].size

    margin = 42
    gutter = 36
    title_h = 92
    canvas = Image.new(
        "RGB",
        (width * 2 + gutter + margin * 2, height * 2 + gutter + margin * 2 + title_h),
        "white",
    )
    draw = ImageDraw.Draw(canvas)

    draw.text((margin, 34), "One Operator, Seven Scripts", font=load_font(54), fill=BLACK)

    positions = [
        (margin, margin + title_h),
        (margin + width + gutter, margin + title_h),
        (margin, margin + title_h + height + gutter),
        (margin + width + gutter, margin + title_h + height + gutter),
    ]

    for panel, (x, y) in zip(panels, positions):
        canvas.paste(panel, (x, y))
        draw.rectangle((x, y, x + width, y + height), outline=GRAY, width=2)

    canvas.save(OUT)

    review_width = 2400
    review_height = int(canvas.height * (review_width / canvas.width))
    review = canvas.resize((review_width, review_height), Image.Resampling.LANCZOS)
    review.save(REVIEW_OUT)

    print(OUT)
    print(REVIEW_OUT)


if __name__ == "__main__":
    main()
