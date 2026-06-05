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
        draw_fit_text(draw, (74, 365, 390, 525), "快车道，\n短记性。", 42, 28, cn=True, align="center")
        out = ROOT / "panel-1-v4-cn.png"
    else:
        draw_fit_text(draw, (74, 365, 390, 525), "Fast lane,\nshort memory.", 42, 28, align="center")
        out = ROOT / "panel-1-v4.png"

    img.save(out)
    return out


def build_panel_2(cn: bool = False) -> Path:
    img = Image.open(SRC / "panel-2-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    if cn:
        draw_fit_text(draw, (650, 62, 1225, 150), "等等——那件\n过检查点了吗？", 32, 24, cn=True)
        draw_fit_text(draw, (128, 210, 560, 330), "凌晨三点了——\n我只想要我的包裹。", 38, 26, cn=True)
        out = ROOT / "panel-2-v4-cn.png"
    else:
        draw_fit_text(draw, (650, 62, 1225, 150), "Wait — was that before\nthe checkpoint?", 32, 23)
        draw_fit_text(draw, (128, 210, 570, 330), "It's 3 A.M. —\nI just want my parcel.", 38, 26)
        out = ROOT / "panel-2-v4.png"

    img.save(out)
    return out


def build_panel_3(cn: bool = False) -> Path:
    img = Image.open(SRC / "panel-3-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    if cn:
        draw_fit_text(
            draw,
            (105, 365, 500, 535),
            "已从最近一致检查点恢复。\n热备接管。",
            29,
            19,
            cn=True,
            align="center",
        )
        out = ROOT / "panel-3-v4-cn.png"
    else:
        draw_fit_text(
            draw,
            (105, 365, 500, 535),
            "Restored from last\nconsistent checkpoint.\nStandby takes over.",
            27,
            17,
            align="center",
        )
        out = ROOT / "panel-3-v4.png"

    img.save(out)
    return out


def build_panel_4(cn: bool = False) -> Path:
    img = Image.open(SRC / "panel-4-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    if cn:
        draw_fit_text(draw, (85, 118, 690, 230), "平台接住了，就不算事故。", 40, 26, cn=True)
        draw_fit_text(draw, (85, 252, 390, 315), "睡眠：7 小时", 30, 20, cn=True)
        out = ROOT / "panel-4-v4-cn.png"
    else:
        draw_fit_text(
            draw,
            (85, 112, 700, 245),
            "It's not an incident\nwhen the platform catches it.",
            38,
            24,
        )
        draw_fit_text(draw, (85, 252, 380, 315), "Sleep: 7h", 30, 20)
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
        "The Courier Missed a Checkpoint",
        ROOT / "comic-v4.png",
        ROOT / "comic-v4-review.png",
    )
    build_comic(
        cn_panels,
        "快递站漏了个检查点",
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
