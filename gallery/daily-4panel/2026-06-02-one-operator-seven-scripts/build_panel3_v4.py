from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

BASE = SRC / "panel-3-v4-base.png"
OUT = ROOT / "panel-3-v4.png"

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

    tower_line = "One manifest.\nEverything else\nhandled."
    xiaohei_line = "One place to declare all this?"

    # Tower line is inside the control tower's own display panel.
    draw_fit_text(draw, (600, 370, 850, 495), tower_line, max_size=34, min_size=24)

    # Xiaohei line: black text in nearby open whitespace, no bubble or text box.
    draw_fit_text(draw, (990, 300, 1545, 390), xiaohei_line, max_size=38, min_size=28, align="left")

    # Each declaration card remains separate; labels are object-native card text.
    cards = [
        ((1076, 715, 1147, 770), "PG"),
        ((1215, 715, 1295, 770), "Redis"),
        ((1353, 715, 1450, 770), "Kafka"),
        ((1490, 715, 1608, 770), "MySQL"),
    ]
    for box, label in cards:
        draw_fit_text(draw, box, label, max_size=26, min_size=18)

    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
