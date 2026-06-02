from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

BASE = SRC / "panel-2-v4-base.png"
OUT = ROOT / "panel-2-v4.1.png"

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"
FONT_FALLBACK = "/System/Library/Fonts/Supplemental/ChalkboardSE.ttc"

BLACK = (18, 18, 18)
WHITE = (255, 255, 255)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in (FONT_REGULAR, FONT_FALLBACK):
        try:
            return ImageFont.truetype(path, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def draw_fit_text(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    text: str,
    max_size: int,
    min_size: int,
    align: str = "center",
) -> None:
    x1, y1, x2, y2 = box
    for size in range(max_size, min_size - 1, -2):
        font = load_font(size)
        spacing = int(size * 0.22)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align=align)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        if width <= x2 - x1 and height <= y2 - y1:
            draw.multiline_text(
                ((x1 + x2) / 2, (y1 + y2) / 2),
                text,
                font=font,
                fill=BLACK,
                spacing=spacing,
                align=align,
                anchor="mm",
            )
            return

    font = load_font(min_size)
    draw.multiline_text((x1, y1), text, font=font, fill=BLACK, spacing=int(min_size * 0.22), align=align)


def draw_xiaohei_line(draw: ImageDraw.ImageDraw) -> None:
    font = load_font(37)
    x = 705
    y = 265
    draw.text((x, y), "7 scripts…", font=font, fill=BLACK)
    y2 = 316
    draw.text((x, y2), "and ", font=font, fill=BLACK)
    prefix_width = draw.textlength("and ", font=font)
    zero_x = int(x + prefix_width)
    zero_y = y2 + 2
    zero_box = (zero_x + 4, zero_y + 3, zero_x + 25, zero_y + 32)
    draw.ellipse(zero_box, outline=BLACK, width=3)
    draw.line((zero_x + 22, zero_y + 6, zero_x + 8, zero_y + 31), fill=BLACK, width=2)
    draw.text((zero_x + 32, y2), "hours of sleep.", font=font, fill=BLACK)


def main() -> None:
    img = Image.open(BASE).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Remove a model-generated empty oval near Xiaohei so it does not read as a speech bubble.
    draw.ellipse((920, 582, 1080, 652), fill=WHITE)

    draw_fit_text(draw, (340, 220, 575, 350), "Default assumption:\nstateless?", max_size=34, min_size=26)
    draw_xiaohei_line(draw)
    draw_fit_text(draw, (980, 535, 1190, 585), "We have state!", max_size=29, min_size=23)
    draw_fit_text(draw, (1235, 730, 1505, 775), "Nothing gets lost!", max_size=29, min_size=22)

    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
