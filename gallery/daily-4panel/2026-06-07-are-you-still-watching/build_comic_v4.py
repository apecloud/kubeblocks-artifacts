from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

W, H = 1672, 941
BLACK = (18, 18, 18)
GRAY = (220, 220, 220)
UI_TEXT = (22, 26, 28)
UI_FILL = (224, 235, 244)
UI_OUTLINE = (60, 72, 80)

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


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    bbox = draw.textbbox((0, 0), text, font=font)
    return bbox[2] - bbox[0], bbox[3] - bbox[1]


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
        spacing = max(7, int(size * 0.18))
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align=align)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        if width <= x2 - x1 and height <= y2 - y1:
            if align == "center":
                x = x1 + (x2 - x1 - width) / 2 - bbox[0]
            elif align == "right":
                x = x2 - width - bbox[0]
            else:
                x = x1 - bbox[0]
            y = y1 + (y2 - y1 - height) / 2 - bbox[1]
            draw.multiline_text((x, y), text, font=font, fill=fill, spacing=spacing, align=align)
            return
    draw.multiline_text((x1, y1), text, font=load_font(min_size, cn=cn), fill=fill, align=align)


def draw_counter(draw: ImageDraw.ImageDraw, text: str, cn: bool = False) -> None:
    box = (52, 54, 470, 118)
    draw.rounded_rectangle(box, radius=16, fill=(250, 250, 247), outline=(212, 216, 216), width=2)
    draw_fit_text(draw, (70, 62, 452, 110), text, 28 if cn else 30, 18, cn=cn, align="center", fill=BLACK)


def draw_screen_prompt(draw: ImageDraw.ImageDraw, cn: bool = False) -> None:
    modal = (1326, 342, 1645, 545)
    button = (1436, 486, 1554, 533)
    draw.rounded_rectangle(modal, radius=12, fill=UI_FILL, outline=UI_OUTLINE, width=3)
    draw_fit_text(
        draw,
        (1354, 370, 1618, 455),
        "还在看吗？" if cn else "Are you\nstill watching?",
        34 if cn else 32,
        22,
        cn=cn,
        align="center",
        fill=UI_TEXT,
    )
    draw.rounded_rectangle(button, radius=9, fill=(210, 226, 239), outline=UI_OUTLINE, width=2)


def draw_continue_button(draw: ImageDraw.ImageDraw, cn: bool = False) -> None:
    button = (1368, 478, 1504, 531)
    draw.rounded_rectangle(button, radius=12, fill=(211, 228, 241), outline=UI_OUTLINE, width=2)
    draw_fit_text(
        draw,
        (1380, 485, 1492, 524),
        "继续" if cn else "Continue",
        25 if cn else 22,
        15,
        cn=cn,
        align="center",
        fill=UI_TEXT,
    )


def load_base(index: int) -> Image.Image:
    img = Image.open(SRC / f"panel-{index}-v4-base.png").convert("RGB")
    return img.resize((W, H), Image.Resampling.LANCZOS)


def build_panel(index: int, cn: bool = False) -> Path:
    img = load_base(index)
    draw = ImageDraw.Draw(img)

    if index == 2:
        draw_screen_prompt(draw, cn=cn)
    elif index == 3:
        draw_fit_text(draw, (565, 126, 880, 210), "…没礼貌。" if cn else "…rude.", 42 if cn else 48, 26, cn=cn)
    elif index == 4:
        draw_continue_button(draw, cn=cn)
        draw_fit_text(
            draw,
            (605, 126, 975, 206),
            "看。不然呢。" if cn else "Yes. Obviously.",
            38 if cn else 42,
            24,
            cn=cn,
            align="center",
        )
        draw_counter(draw, "睡眠：还在看…" if cn else "Sleep: still watching…", cn=cn)

    suffix = "-cn" if cn else ""
    out = ROOT / f"panel-{index}-v4{suffix}.png"
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


def write_prompt_records() -> None:
    prompts = {
        1: ("Panel 1 v4 Prompt", "Image-generated text-free base: Xiaohei is extremely relaxed and sprawled on the sofa watching TV. Locked local text: none."),
        2: ("Panel 2 v4 Prompt", "Image-generated text-free base: Xiaohei snaps bolt upright after the TV interruption. Locked local TV UI text: EN `Are you still watching?` / CN `还在看吗？`."),
        3: ("Panel 3 v4 Prompt", "Image-generated text-free base: Xiaohei stares down the TV in offended silence. Locked local deadpan line: EN `…rude.` / CN `…没礼貌。`."),
        4: ("Panel 4 v4 Prompt", "Image-generated text-free base: Xiaohei presses the TV Continue button while slouching back into the sofa. Locked local text: EN `Continue`, `Yes. Obviously.`, `Sleep: still watching…`; CN `继续`, `看。不然呢。`, `睡眠：还在看…`."),
    }
    for idx, (title, body) in prompts.items():
        (ROOT / f"panel-{idx}-v4-prompt.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")

    (ROOT / "v4-files.md").write_text(
        """# Daily 2026-06-07 Are You Still Watching v4 Files

## Review Comic

- `comic-v4-review.png` — English review-scaled 2x2 comic for chat QA
- `comic-v4-review-cn.png` — Chinese review-scaled 2x2 comic for chat QA

## Original Comic Candidates

- `comic-v4.png` — English original 2x2 comic candidate
- `comic-v4-cn.png` — Chinese original 2x2 comic candidate

## Single Panels

- `panel-1-v4.png`
- `panel-2-v4.png`
- `panel-3-v4.png`
- `panel-4-v4.png`
- `panel-1-v4-cn.png`
- `panel-2-v4-cn.png`
- `panel-3-v4-cn.png`
- `panel-4-v4-cn.png`

## Source Bases

- `source/panel-1-v4-base.png`
- `source/panel-2-v4-base.png`
- `source/panel-3-v4-base.png`
- `source/panel-4-v4-base.png`

## Build Scripts

- `build_comic_v4.py`

## Notes

- English review title: `Are You Still Watching?`
- Chinese review title: `还在看吗？`
- Review-stage only; do not move to repository until三方 QA passes.
- TV prompt and Continue/继续 are deterministic local overlays in object-native UI areas.
- Counter uses locked shortened text: `Sleep: still watching…` / `睡眠：还在看…`.
- No product watermark, brand logo, Kubernetes logo, KubeBlocks logo, or internal meta label appears in the review comic.
""",
        encoding="utf-8",
    )


def main() -> None:
    en_panels = [build_panel(i) for i in range(1, 5)]
    cn_panels = [build_panel(i, cn=True) for i in range(1, 5)]

    build_comic(en_panels, "Are You Still Watching?", ROOT / "comic-v4.png", ROOT / "comic-v4-review.png")
    build_comic(cn_panels, "还在看吗？", ROOT / "comic-v4-cn.png", ROOT / "comic-v4-review-cn.png", cn=True)
    write_prompt_records()

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
