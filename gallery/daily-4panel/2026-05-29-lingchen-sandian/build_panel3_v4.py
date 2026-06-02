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


def label(draw: ImageDraw.ImageDraw, xy: tuple[int, int], text: str) -> None:
    draw.text(xy, text, font=load_font(26), fill=BLACK)


def main() -> None:
    img = Image.open(BASE).convert("RGB")
    draw = ImageDraw.Draw(img)

    tower = "Declare the desired state.\nI'll orchestrate the workflow."
    xiaohei = "…how is it\nnot panicking?"

    draw_fit_text(draw, (915, 280, 1220, 375), tower, max_size=25, min_size=20)
    draw_fit_text(draw, (245, 430, 565, 520), xiaohei, max_size=30, min_size=24, align="left")

    label(draw, (585, 515), "Backup")
    label(draw, (755, 815), "Restore")
    label(draw, (1140, 812), "Scale")
    label(draw, (1410, 735), "Failover")

    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
