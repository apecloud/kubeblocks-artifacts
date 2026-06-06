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
        draw_fit_text(draw, (1040, 160, 1570, 250), "来了来了。" if cn else "Oh, here it comes.", 42 if cn else 46, 28, cn=cn)
        draw_fit_text(draw, (855, 340, 1130, 410), "typing…" if not cn else "对方正在输入…", 30 if cn else 34, 22, cn=cn, align="center")
    elif index == 2:
        draw_fit_text(draw, (1010, 140, 1580, 250), "……这得是长篇大论。" if cn else "…this is gonna be BIG.", 42 if cn else 46, 28, cn=cn)
        draw_fit_text(draw, (860, 245, 1135, 320), "typing…" if not cn else "输入中…", 30 if cn else 34, 22, cn=cn, align="center")
    elif index == 3:
        pass
    else:
        draw_fit_text(draw, (115, 115, 790, 235), "……憋这么久就一个\"嗯\"。" if cn else "…all that for a \"k\".", 42 if cn else 46, 28, cn=cn)
        draw_fit_text(draw, (930, 545, 1085, 610), "嗯" if cn else "k", 32 if cn else 38, 22, cn=cn, align="center")
        draw_fit_text(draw, (1000, 83, 1585, 165), "睡眠：对方正在输入…" if cn else "Sleep: typing…", 32 if cn else 34, 22, cn=cn, align="right")

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
        1: ("Panel 1 v4 Prompt", "Image-generated text-free base: Xiaohei expects a chat reply while three-dot typing indicators appear. Locked local text: EN `typing…` + `Oh, here it comes.` / CN `对方正在输入…` + `来了来了。`."),
        2: ("Panel 2 v4 Prompt", "Image-generated text-free base: typing indicators stack up as the wait grows; Xiaohei braces for a big message. Locked local text: EN `typing…` + `…this is gonna be BIG.` / CN `输入中…` + `……这得是长篇大论。`."),
        3: ("Panel 3 v4 Prompt", "Image-generated text-free base: the typing indicator disappears with no reply; Xiaohei freezes. No local dialogue."),
        4: ("Panel 4 v4 Prompt", "Image-generated text-free base: a tiny reply bubble finally arrives after the long buildup; Xiaohei is deadpan. Locked local text: EN bubble `k`, dialogue `…all that for a \"k\".`, counter `Sleep: typing…` / CN bubble `嗯`, dialogue `……憋这么久就一个\"嗯\"。`, counter `睡眠：对方正在输入…`."),
    }
    for idx, (title, body) in prompts.items():
        (ROOT / f"panel-{idx}-v4-prompt.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")

    (ROOT / "v4-files.md").write_text(
        """# Daily 2026-06-06 Typing v4 Files

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

- English final artwork title: `Typing…`
- Chinese final artwork title: `对方正在输入…`
- No product watermark, brand logo, Kubernetes logo, KubeBlocks logo, or internal meta label appears in the final combined comic.
- Panel order is 1 -> 2 -> 3 -> 4.
- Chinese versions reuse the same image-generated source bases and deterministic local lettering.
- One universal chat-typing suspense concept only; no narration fallback needed.
- Source bases use image generation rather than deterministic line-art placeholders, matching the Ep1-Ep5 quality bar.
""",
        encoding="utf-8",
    )


def main() -> None:
    en_panels = [build_panel(i) for i in range(1, 5)]
    cn_panels = [build_panel(i, cn=True) for i in range(1, 5)]

    build_comic(en_panels, "Typing…", ROOT / "comic-v4.png", ROOT / "comic-v4-review.png")
    build_comic(cn_panels, "对方正在输入…", ROOT / "comic-v4-cn.png", ROOT / "comic-v4-review-cn.png", cn=True)
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
