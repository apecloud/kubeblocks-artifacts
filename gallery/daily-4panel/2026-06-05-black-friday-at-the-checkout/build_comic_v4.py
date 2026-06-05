from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

BLACK = (18, 18, 18)
GRAY = (220, 220, 220)
WHITE = (255, 255, 255)

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
        spacing = max(8, int(size * 0.22))
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
    draw.multiline_text((x1, y1), text, font=font, fill=BLACK, spacing=max(8, int(min_size * 0.22)), align=align)


def draw_xiaohei_pocket_hands(draw: ImageDraw.ImageDraw) -> None:
    """Clarify the relaxed hands-in-pockets silhouette in the finale panel."""
    draw.arc((198, 662, 252, 727), start=160, end=230, fill=WHITE, width=5)
    draw.arc((326, 666, 386, 733), start=315, end=35, fill=WHITE, width=5)


def build_panel_1(cn: bool = False) -> Path:
    img = Image.open(SRC / "panel-1-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    if cn:
        draw_fit_text(draw, (110, 112, 760, 250), "今天挺闲。\n也许能睡会儿。", 42, 28, cn=True)
        draw_fit_text(draw, (1305, 630, 1510, 725), "促销", 36, 24, cn=True, align="center")
        out = ROOT / "panel-1-v4-cn.png"
    else:
        draw_fit_text(draw, (110, 112, 760, 250), "Quiet day.\nMaybe I sleep.", 44, 28)
        draw_fit_text(draw, (1305, 630, 1510, 725), "SALE", 38, 24, align="center")
        out = ROOT / "panel-1-v4.png"

    img.save(out)
    return out


def build_panel_2(cn: bool = False) -> Path:
    img = Image.open(SRC / "panel-2-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    if cn:
        draw_fit_text(draw, (92, 105, 730, 235), "上线了没？\n订单要丢了！", 42, 28, cn=True)
        out = ROOT / "panel-2-v4-cn.png"
    else:
        draw_fit_text(draw, (92, 105, 760, 245), "Is it live yet?\nWe're losing orders!", 42, 28)
        out = ROOT / "panel-2-v4.png"

    img.save(out)
    return out


def build_panel_3(cn: bool = False) -> Path:
    img = Image.open(SRC / "panel-3-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    if cn:
        draw_fit_text(draw, (1118, 242, 1375, 330), "正在扩容——\n更多通道上线。", 22, 15, cn=True, align="center")
        draw_fit_text(draw, (548, 300, 930, 385), "能不能天天这样？", 30, 20, cn=True)
        draw_fit_text(draw, (118, 675, 405, 755), "……求你别。", 32, 22, cn=True)
        out = ROOT / "panel-3-v4-cn.png"
    else:
        draw_fit_text(draw, (1118, 242, 1375, 330), "Scaling out —\nmore lanes online.", 20, 14, align="center")
        draw_fit_text(draw, (548, 300, 940, 385), "Can we do this every day?", 30, 20)
        draw_fit_text(draw, (118, 675, 390, 755), "…please, no.", 32, 22)
        out = ROOT / "panel-3-v4.png"

    img.save(out)
    return out


def build_panel_4(cn: bool = False) -> Path:
    img = Image.open(SRC / "panel-4-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)
    draw_xiaohei_pocket_hands(draw)

    if cn:
        draw_fit_text(draw, (1140, 285, 1530, 365), "所有设施——\n一切正常。", 28, 18, cn=True, align="center")
        draw_fit_text(draw, (100, 150, 420, 222), "睡眠：0 小时", 32, 22, cn=True)
        out = ROOT / "panel-4-v4-cn.png"
    else:
        draw_fit_text(draw, (1140, 285, 1530, 365), "All facilities —\nnominal.", 28, 18, align="center")
        draw_fit_text(draw, (100, 150, 400, 222), "Sleep: 0h", 32, 22, cn=True)
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
    en_panels = [build_panel_1(), build_panel_2(), build_panel_3(), build_panel_4()]
    cn_panels = [build_panel_1(cn=True), build_panel_2(cn=True), build_panel_3(cn=True), build_panel_4(cn=True)]

    build_comic(
        en_panels,
        "Black Friday at the Checkout",
        ROOT / "comic-v4.png",
        ROOT / "comic-v4-review.png",
    )
    build_comic(
        cn_panels,
        "黑五·结账区",
        ROOT / "comic-v4-cn.png",
        ROOT / "comic-v4-review-cn.png",
        cn=True,
    )

    for output in (
        *en_panels,
        *cn_panels,
        ROOT / "comic-v4.png",
        ROOT / "comic-v4-review.png",
        ROOT / "comic-v4-cn.png",
        ROOT / "comic-v4-review-cn.png",
    ):
        print(output)


if __name__ == "__main__":
    main()
