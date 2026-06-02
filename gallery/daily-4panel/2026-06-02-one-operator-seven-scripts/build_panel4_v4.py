from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

BASE = SRC / "panel-4-v4-base.png"
OUT = ROOT / "panel-4-v4.png"

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"
FONT_FALLBACK = "/System/Library/Fonts/Supplemental/ChalkboardSE.ttc"

BLACK = (18, 18, 18)


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
        spacing = int(size * 0.18)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align=align)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        if width <= x2 - x1 and height <= y2 - y1:
            anchor = "mm" if align == "center" else "lm"
            pos = ((x1 + x2) / 2, (y1 + y2) / 2) if align == "center" else (x1, (y1 + y2) / 2)
            draw.multiline_text(
                pos,
                text,
                font=font,
                fill=BLACK,
                spacing=spacing,
                align=align,
                anchor=anchor,
            )
            return

    font = load_font(min_size)
    draw.multiline_text((x1, y1), text, font=font, fill=BLACK, spacing=int(min_size * 0.18), align=align)


def main() -> None:
    img = Image.open(BASE).convert("RGB")
    draw = ImageDraw.Draw(img)

    xiaohei_line = "\u2026just one.\nFor emergencies."
    sleep_counter = "Sleep: 20m"

    # Punchline line: black text in open whitespace, no bubble or text box.
    draw_fit_text(draw, (650, 285, 1185, 390), xiaohei_line, max_size=46, min_size=32, align="left")

    # Counter text is object-native inside the timer screen.
    draw_fit_text(draw, (168, 678, 294, 742), sleep_counter, max_size=25, min_size=17)

    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
