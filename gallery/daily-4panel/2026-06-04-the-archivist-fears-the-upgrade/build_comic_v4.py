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
) -> None:
    x1, y1, x2, y2 = box
    for size in range(max_size, min_size - 1, -2):
        font = load_font(size, cn=cn)
        spacing = max(7, int(size * 0.22))
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align=align)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        if width <= x2 - x1 and height <= y2 - y1:
            if align == "center":
                pos = (x1 + (x2 - x1 - width) / 2 - bbox[0], y1 + (y2 - y1 - height) / 2 - bbox[1])
            else:
                pos = (x1 - bbox[0], y1 + (y2 - y1 - height) / 2 - bbox[1])
            draw.multiline_text(pos, text, font=font, fill=BLACK, spacing=spacing, align=align)
            return

    font = load_font(min_size, cn=cn)
    draw.multiline_text((x1, y1), text, font=font, fill=BLACK, spacing=max(7, int(min_size * 0.22)), align=align)


def build_panel_1(cn: bool = False) -> Path:
    img = Image.open(SRC / "panel-1-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    if cn:
        draw_fit_text(draw, (66, 372, 294, 555), "有新版本\n可升级。", 36, 24, cn=True, align="center")
        draw_fit_text(draw, (930, 335, 1590, 500), "按规矩来，\n一份都不能丢。", 45, 30, cn=True)
        out = ROOT / "panel-1-v4-cn.png"
    else:
        draw_fit_text(draw, (66, 372, 294, 555), "New version\navailable.", 33, 22, align="center")
        draw_fit_text(draw, (930, 338, 1590, 500), "By the book.\nNothing gets lost.", 47, 31)
        out = ROOT / "panel-1-v4.png"

    img.save(out)
    return out


def build_panel_2(cn: bool = False) -> Path:
    img = Image.open(SRC / "panel-2-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    if cn:
        draw_fit_text(draw, (910, 128, 1605, 285), "升级我……\n全城会不会黑掉？", 41, 29, cn=True)
        draw_fit_text(draw, (1035, 292, 1610, 405), "报表我明早就要。", 37, 27, cn=True)
        out = ROOT / "panel-2-v4-cn.png"
    else:
        draw_fit_text(draw, (910, 128, 1605, 285), "If you upgrade me…\ndoes the city go dark?", 41, 29)
        draw_fit_text(draw, (1035, 292, 1610, 405), "I need the numbers by morning.", 37, 25)
        out = ROOT / "panel-2-v4.png"

    img.save(out)
    return out


def build_panel_3(cn: bool = False) -> Path:
    img = Image.open(SRC / "panel-3-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    if cn:
        draw_fit_text(draw, (154, 348, 528, 505), "滚动升级——\n一间一间换。", 30, 22, cn=True, align="center")
        draw_fit_text(draw, (596, 305, 780, 408), "……我从没\n担心过。", 28, 20, cn=True)
        draw_fit_text(draw, (452, 610, 608, 675), "是嘛。", 27, 20, cn=True)
        out = ROOT / "panel-3-v4-cn.png"
    else:
        draw_fit_text(draw, (154, 348, 528, 505), "Rolling upgrade —\none room at a time.", 31, 21, align="center")
        draw_fit_text(draw, (596, 305, 780, 408), "…I was\nnever worried.", 28, 20)
        draw_fit_text(draw, (452, 610, 608, 675), "Sure.", 28, 20)
        out = ROOT / "panel-3-v4.png"

    img.save(out)
    return out


def build_panel_4(cn: bool = False) -> Path:
    img = Image.open(SRC / "panel-4-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    if cn:
        draw_fit_text(draw, (575, 265, 935, 400), "我以前为这事\n能熬一整夜。", 36, 25, cn=True)
        draw_fit_text(draw, (450, 424, 705, 500), "升级：100%", 27, 20, cn=True, align="center")
        draw_fit_text(draw, (176, 660, 326, 735), "睡眠：\n5 小时", 21, 16, cn=True, align="center")
        out = ROOT / "panel-4-v4-cn.png"
    else:
        font = load_font(34)
        draw.multiline_text(
            (575, 278),
            "I used to stay\nup all night for this.",
            font=font,
            fill=BLACK,
            spacing=10,
        )
        draw_fit_text(draw, (450, 424, 705, 500), "Upgrade: 100%", 27, 18, align="center")
        draw_fit_text(draw, (176, 660, 326, 735), "Sleep:\n5h", 21, 16, align="center")
        out = ROOT / "panel-4-v4.png"

    img.save(out)
    return out


def build_comic(panel_paths: list[Path], title: str, out: Path, review_out: Path, cn: bool = False) -> None:
    panels = [Image.open(path).convert("RGB") for path in panel_paths]
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
    panel_outputs = (
        build_panel_1(),
        build_panel_1(cn=True),
        build_panel_2(),
        build_panel_2(cn=True),
        build_panel_3(),
        build_panel_3(cn=True),
        build_panel_4(),
        build_panel_4(cn=True),
    )
    for output in panel_outputs:
        print(output)

    build_comic(
        [ROOT / f"panel-{idx}-v4.png" for idx in range(1, 5)],
        "The Archivist Fears the Upgrade",
        ROOT / "comic-v4.png",
        ROOT / "comic-v4-review.png",
    )
    build_comic(
        [ROOT / f"panel-{idx}-v4-cn.png" for idx in range(1, 5)],
        "档案馆怕升级",
        ROOT / "comic-v4-cn.png",
        ROOT / "comic-v4-review-cn.png",
        cn=True,
    )
    for output in (
        ROOT / "comic-v4.png",
        ROOT / "comic-v4-review.png",
        ROOT / "comic-v4-cn.png",
        ROOT / "comic-v4-review-cn.png",
    ):
        print(output)


if __name__ == "__main__":
    main()
