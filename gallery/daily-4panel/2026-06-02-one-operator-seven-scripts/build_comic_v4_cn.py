from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

OUT = ROOT / "comic-v4-cn.png"
REVIEW_OUT = ROOT / "comic-v4-review-cn.png"

FONT_CN = "/System/Library/Fonts/PingFang.ttc"
FONT_FALLBACK = "/System/Library/Fonts/STHeiti Medium.ttc"
FONT_EN = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"

BLACK = (18, 18, 18)
GRAY = (220, 220, 220)


def load_font(size: int, latin: bool = False) -> ImageFont.FreeTypeFont:
    paths = (FONT_EN, FONT_CN, FONT_FALLBACK) if latin else (FONT_CN, FONT_FALLBACK)
    for path in paths:
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
    latin: bool = False,
) -> None:
    x1, y1, x2, y2 = box
    for size in range(max_size, min_size - 1, -2):
        font = load_font(size, latin=latin)
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

    font = load_font(min_size, latin=latin)
    draw.multiline_text((x1, y1), text, font=font, fill=BLACK, spacing=int(min_size * 0.18), align=align)


def draw_rotated_label(
    img: Image.Image,
    center: tuple[int, int],
    text: str,
    size: int,
    angle: float = 0,
) -> None:
    font = load_font(size, latin=True)
    label = Image.new("RGBA", (240, 80), (255, 255, 255, 0))
    draw = ImageDraw.Draw(label)
    draw.text((120, 40), text, font=font, fill=BLACK, anchor="mm")
    rotated = label.rotate(angle, expand=True, resample=Image.Resampling.BICUBIC)
    x = center[0] - rotated.width // 2
    y = center[1] - rotated.height // 2
    img.paste(rotated, (x, y), rotated)


def build_panel_1() -> Image.Image:
    img = Image.open(SRC / "panel-1-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    draw_fit_text(draw, (930, 305, 1545, 445), "一个库配一个脚本。\n我…很有条理。", max_size=46, min_size=32, align="left")

    img.save(ROOT / "panel-1-v4-cn.png")
    return img


def build_panel_2() -> Image.Image:
    img = Image.open(SRC / "panel-2-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    draw_fit_text(draw, (845, 420, 1200, 505), "…总还差一个脚本。", max_size=34, min_size=24, align="left")
    draw_fit_text(draw, (1030, 245, 1600, 360), "我们一直都这么干。", max_size=42, min_size=28, align="left")
    draw_rotated_label(img, (699, 408), "mysql.sh", 25, angle=-6)
    draw_rotated_label(img, (770, 618), "backup.sh", 22, angle=2)
    draw_rotated_label(img, (430, 820), "resize.sh", 24, angle=5)

    img.save(ROOT / "panel-2-v4-cn.png")
    return img


def build_panel_3() -> Image.Image:
    img = Image.open(SRC / "panel-3-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    draw_fit_text(draw, (600, 370, 850, 495), "一份声明，\n其余交给我。", max_size=34, min_size=24)
    draw_fit_text(draw, (990, 300, 1545, 390), "一个地方声明这一切？", max_size=40, min_size=28, align="left")

    cards = [
        ((1076, 715, 1147, 770), "PG"),
        ((1215, 715, 1295, 770), "Redis"),
        ((1353, 715, 1450, 770), "Kafka"),
        ((1490, 715, 1608, 770), "MySQL"),
    ]
    for box, label in cards:
        draw_fit_text(draw, box, label, max_size=26, min_size=18, latin=True)

    img.save(ROOT / "panel-3-v4-cn.png")
    return img


def build_panel_4() -> Image.Image:
    img = Image.open(SRC / "panel-4-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    draw_fit_text(draw, (650, 285, 1185, 390), "…就留一个。\n以防万一。", max_size=44, min_size=30, align="left")
    draw_fit_text(draw, (168, 678, 294, 742), "睡眠：20 分钟", max_size=20, min_size=14)

    img.save(ROOT / "panel-4-v4-cn.png")
    return img


def build_comic(panels: list[Image.Image]) -> None:
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
    draw.text((margin, 30), "一个运维，七个脚本", font=load_font(54), fill=BLACK)

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
    canvas.resize((review_width, review_height), Image.Resampling.LANCZOS).save(REVIEW_OUT)


def main() -> None:
    panels = [build_panel_1(), build_panel_2(), build_panel_3(), build_panel_4()]
    build_comic(panels)
    print(OUT)
    print(REVIEW_OUT)


if __name__ == "__main__":
    main()
