from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

W, H = 1672, 941
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
        spacing = max(8, int(size * 0.22))
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
            draw.multiline_text((x, y), text, font=font, fill=BLACK, spacing=spacing, align=align)
            return

    font = load_font(min_size, cn=cn)
    draw.multiline_text((x1, y1), text, font=font, fill=BLACK, spacing=max(8, int(min_size * 0.22)), align=align)


def load_base(index: int) -> Image.Image:
    img = Image.open(SRC / f"panel-{index}-v4-base.png").convert("RGB")
    return img.resize((W, H), Image.Resampling.LANCZOS)


def build_panel(index: int, cn: bool = False) -> Path:
    img = load_base(index)
    draw = ImageDraw.Draw(img)

    if index == 1:
        draw_fit_text(draw, (95, 70, 390, 185), "选出所有\n红绿灯" if cn else "Select all\ntraffic lights", 38 if cn else 40, 26, cn=cn)
        draw_fit_text(draw, (115, 350, 350, 430), "小意思。" if cn else "Easy.", 40 if cn else 44, 26, cn=cn, align="center")
    elif index == 2:
        draw_fit_text(draw, (95, 70, 830, 175), "再选出所有公交车" if cn else "Now select the buses", 42 if cn else 44, 28, cn=cn)
        draw_fit_text(draw, (120, 430, 410, 515), "……行吧。" if cn else "…okay.", 40 if cn else 44, 26, cn=cn, align="center")
    elif index == 3:
        draw_fit_text(draw, (95, 96, 610, 205), "……到底有多少？" if cn else "…how many ARE there?", 42 if cn else 44, 28, cn=cn)
    else:
        draw_fit_text(draw, (95, 90, 670, 190), "……我才是机器人吧？" if cn else "…am I the robot?", 42 if cn else 46, 28, cn=cn)
        draw_fit_text(draw, (1080, 82, 1580, 165), "睡眠：验证中…" if cn else "Sleep: verifying…", 32 if cn else 34, 22, cn=cn, align="right")

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
        1: ("Panel 1 v4 Prompt", "Image-generated text-free base: Xiaohei confidently faces a monitor with a nine-tile online puzzle containing traffic-light pictograms. Locked local text: EN `Select all traffic lights` + `Easy.` / CN `选出所有红绿灯` + `小意思。`."),
        2: ("Panel 2 v4 Prompt", "Image-generated text-free base: the tile puzzle refreshes into buses, and Xiaohei is slightly resigned. Locked local text: EN `Now select the buses` + `…okay.` / CN `再选出所有公交车` + `……行吧。`."),
        3: ("Panel 3 v4 Prompt", "Image-generated text-free base: endless cascading tile puzzles fill the monitor while Xiaohei is overwhelmed. Locked local text: EN `…how many ARE there?` / CN `……到底有多少？`."),
        4: ("Panel 4 v4 Prompt", "Image-generated text-free base: the final grid mixes robot icons with Xiaohei-shaped silhouettes, and a tiny wind-up key becomes the self-doubt joke. Locked local text: EN `…am I the robot?` + `Sleep: verifying…` / CN `……我才是机器人吧？` + `睡眠：验证中…`."),
    }
    for idx, (title, body) in prompts.items():
        (ROOT / f"panel-{idx}-v4-prompt.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")

    (ROOT / "v4-files.md").write_text(
        """# Daily 2026-06-06 Prove You're Not a Robot v4 Files

## Final Comic

- `comic-v4.png` — English original 2x2 final comic
- `comic-v4-review.png` — English review-scaled 2x2 comic for chat preview
- `comic-v4-cn.png` — Chinese original 2x2 final comic
- `comic-v4-review-cn.png` — Chinese review-scaled 2x2 comic for chat preview

## Locked Single Panels

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

## Prompt Records

- `panel-1-v4-prompt.md`
- `panel-2-v4-prompt.md`
- `panel-3-v4-prompt.md`
- `panel-4-v4-prompt.md`

## Notes

- English final artwork title: `Prove You're Not a Robot`
- Chinese final artwork title: `证明你不是机器人`
- No product watermark, brand logo, Kubernetes logo, KubeBlocks logo, or internal meta label appears in the final combined comic.
- Panel order is 1 -> 2 -> 3 -> 4.
- Chinese versions reuse the same image-generated source bases and deterministic local lettering.
- One universal online-verification-puzzle concept only; no narration fallback needed.
- Source bases use image generation rather than deterministic line-art placeholders, matching the Ep1-Ep5 quality bar.
""",
        encoding="utf-8",
    )


def main() -> None:
    en_panels = [build_panel(i) for i in range(1, 5)]
    cn_panels = [build_panel(i, cn=True) for i in range(1, 5)]

    build_comic(en_panels, "Prove You're Not a Robot", ROOT / "comic-v4.png", ROOT / "comic-v4-review.png")
    build_comic(cn_panels, "证明你不是机器人", ROOT / "comic-v4-cn.png", ROOT / "comic-v4-review-cn.png", cn=True)
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
