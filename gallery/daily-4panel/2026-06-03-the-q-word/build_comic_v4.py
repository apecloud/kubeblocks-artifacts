from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

BLACK = (18, 18, 18)
GRAY = (220, 220, 220)

FONT_EN = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"
FONT_EN_FALLBACK = "/System/Library/Fonts/Supplemental/ChalkboardSE.ttc"
FONT_CN = "/System/Library/Fonts/PingFang.ttc"
FONT_CN_FALLBACK = "/System/Library/Fonts/STHeiti Medium.ttc"


def load_font(size: int, cn: bool = False) -> ImageFont.FreeTypeFont:
    paths = (FONT_CN, FONT_CN_FALLBACK, FONT_EN) if cn else (FONT_EN, FONT_EN_FALLBACK)
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
    *,
    cn: bool = False,
    align: str = "left",
    fill: tuple[int, int, int] = BLACK,
) -> None:
    x1, y1, x2, y2 = box
    for size in range(max_size, min_size - 1, -2):
        font = load_font(size, cn=cn)
        spacing = max(8, int(size * 0.22))
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align=align)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        if width <= x2 - x1 and height <= y2 - y1:
            if align == "center":
                pos = (x1 + (x2 - x1 - width) / 2 - bbox[0], y1 + (y2 - y1 - height) / 2 - bbox[1])
            else:
                pos = (x1 - bbox[0], y1 + (y2 - y1 - height) / 2 - bbox[1])
            draw.multiline_text(
                pos,
                text,
                font=font,
                fill=fill,
                spacing=spacing,
                align=align,
            )
            return

    font = load_font(min_size, cn=cn)
    draw.multiline_text((x1, y1), text, font=font, fill=fill, spacing=max(8, int(min_size * 0.22)), align=align)


def build_panel_1(cn: bool = False) -> Image.Image:
    img = Image.open(SRC / "panel-1-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)
    if cn:
        draw_fit_text(draw, (815, 235, 1390, 335), "嗯……今天真安静。", 42, 30, cn=True)
        out = ROOT / "panel-1-v4-cn.png"
    else:
        draw_fit_text(draw, (815, 235, 1390, 335), "Huh. Quiet today.", 52, 34)
        out = ROOT / "panel-1-v4.png"
    img.save(out)
    return img


def build_panel_2(cn: bool = False) -> Image.Image:
    img = Image.open(SRC / "panel-2-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)
    if cn:
        draw_fit_text(draw, (870, 140, 1585, 265), "……你居然真把这话\n说出口了。", 42, 28, cn=True)
        out = ROOT / "panel-2-v4-cn.png"
    else:
        draw_fit_text(draw, (940, 205, 1600, 310), "…you did NOT just say that.", 44, 30)
        out = ROOT / "panel-2-v4.png"
    img.save(out)
    return img


def build_panel_3(cn: bool = False) -> Image.Image:
    img = Image.open(SRC / "panel-3-v4-base.png").convert("RGB")
    out = ROOT / ("panel-3-v4-cn.png" if cn else "panel-3-v4.png")
    img.save(out)
    return img


def build_panel_4(cn: bool = False) -> Image.Image:
    img = Image.open(SRC / "panel-4-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)
    if cn:
        draw_fit_text(draw, (720, 250, 1240, 355), "……我真说出口了。", 40, 28, cn=True)
        draw_fit_text(draw, (158, 718, 286, 798), "睡眠：\n乌鸦嘴", 28, 18, cn=True, align="center")
        out = ROOT / "panel-4-v4-cn.png"
    else:
        draw_fit_text(draw, (740, 250, 1210, 345), "…I said the words.", 42, 28)
        draw_fit_text(draw, (158, 718, 286, 798), "Sleep:\njinxed.", 28, 18, align="center")
        out = ROOT / "panel-4-v4.png"
    img.save(out)
    return img


def build_comic(panels: list[Image.Image], title: str, out: Path, review_out: Path, cn: bool = False) -> None:
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
    draw.text((margin, 31 if cn else 34), title, font=load_font(54, cn=cn), fill=BLACK)

    positions = [
        (margin, margin + title_h),
        (margin + width + gutter, margin + title_h),
        (margin, margin + title_h + height + gutter),
        (margin + width + gutter, margin + title_h + height + gutter),
    ]
    for panel, (x, y) in zip(panels, positions):
        canvas.paste(panel, (x, y))
        draw.rectangle((x, y, x + width, y + height), outline=GRAY, width=2)

    canvas.save(out)
    review_width = 2400
    review_height = int(canvas.height * (review_width / canvas.width))
    canvas.resize((review_width, review_height), Image.Resampling.LANCZOS).save(review_out)


def main() -> None:
    en_panels = [build_panel_1(), build_panel_2(), build_panel_3(), build_panel_4()]
    cn_panels = [build_panel_1(cn=True), build_panel_2(cn=True), build_panel_3(cn=True), build_panel_4(cn=True)]

    build_comic(en_panels, "The Q-Word", ROOT / "comic-v4.png", ROOT / "comic-v4-review.png")
    build_comic(cn_panels, "乌鸦嘴", ROOT / "comic-v4-cn.png", ROOT / "comic-v4-review-cn.png", cn=True)

    for output in (
        "panel-1-v4.png",
        "panel-1-v4-cn.png",
        "panel-2-v4.png",
        "panel-2-v4-cn.png",
        "panel-3-v4.png",
        "panel-3-v4-cn.png",
        "panel-4-v4.png",
        "panel-4-v4-cn.png",
        "comic-v4.png",
        "comic-v4-review.png",
        "comic-v4-cn.png",
        "comic-v4-review-cn.png",
    ):
        print(ROOT / output)


if __name__ == "__main__":
    main()
