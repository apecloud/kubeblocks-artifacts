from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

BASE = SRC / "panel-2-v4-base.png"
OUT = ROOT / "panel-2-v4.png"

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


def draw_rotated_label(
    img: Image.Image,
    center: tuple[int, int],
    text: str,
    size: int,
    angle: float = 0,
) -> None:
    font = load_font(size)
    label = Image.new("RGBA", (240, 80), (255, 255, 255, 0))
    draw = ImageDraw.Draw(label)
    draw.text((120, 40), text, font=font, fill=BLACK, anchor="mm")
    rotated = label.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    x = center[0] - rotated.width // 2
    y = center[1] - rotated.height // 2
    img.paste(rotated, (x, y), rotated)


def main() -> None:
    img = Image.open(BASE).convert("RGB")
    draw = ImageDraw.Draw(img)

    xiaohei_line = "\u2026always one more script."
    mysql_line = "We've always done it this way."

    # Character lines: black text in open whitespace, no bubble or ordinary frame.
    draw_fit_text(draw, (845, 420, 1200, 505), xiaohei_line, max_size=38, min_size=28, align="left")
    draw_fit_text(draw, (1030, 245, 1600, 360), mysql_line, max_size=48, min_size=34, align="left")

    # Short script labels sit on script tabs/papers, so the object itself is the only frame.
    draw_rotated_label(img, (699, 408), "mysql.sh", 25, angle=-6)
    draw_rotated_label(img, (770, 618), "backup.sh", 22, angle=2)
    draw_rotated_label(img, (430, 820), "resize.sh", 24, angle=5)

    img.save(OUT)
    print(OUT)


if __name__ == "__main__":
    main()
