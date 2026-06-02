from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

BASE = SRC / "panel-1-v4-base.png"
OUT = ROOT / "panel-1-v4.1.png"

FONT_REGULAR = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"
FONT_FALLBACK = "/System/Library/Fonts/Supplemental/ChalkboardSE.ttc"

BLACK = (18, 18, 18)
RED = (224, 24, 24)


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


def main() -> None:
    img = Image.open(BASE).convert("RGB")
    draw = ImageDraw.Draw(img)

    phone_alert = "03:00\nPRIMARY DOWN\n\u00d747"
    xiaohei_line = "\u2026not again.\nNot at 3 A.M."

    # Phone screen text: object-native frame only, black readable text.
    draw_fit_text(draw, (255, 245, 520, 505), phone_alert, max_size=50, min_size=34)

    # Xiaohei line: no bubble or text box, positioned in open whitespace.
    draw_fit_text(draw, (820, 330, 1230, 455), xiaohei_line, max_size=52, min_size=34, align="left")

    # v4.1: one tiny city alert glint, reinforcing that Database City is also affected.
    city_alert = (1355, 502)
    draw.ellipse((city_alert[0] - 4, city_alert[1] - 4, city_alert[0] + 4, city_alert[1] + 4), fill=RED)
    for dx, dy in ((0, -16), (12, -10), (-12, -10)):
        draw.line((city_alert[0], city_alert[1] - 8, city_alert[0] + dx, city_alert[1] + dy), fill=RED, width=3)

    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
