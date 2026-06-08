from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

W, H = 1672, 941
BLACK = (18, 18, 18)
GRAY = (220, 220, 220)
UI_FILL = (250, 250, 247)
UI_OUTLINE = (205, 211, 211)
STICKY = (255, 246, 168)
STICKY_EDGE = (218, 198, 98)

FONT_EN = "/System/Library/Fonts/Supplemental/Bradley Hand Bold.ttf"
FONT_EN_FALLBACK = "/System/Library/Fonts/Supplemental/ChalkboardSE.ttc"
FONT_CN = "/System/Library/Fonts/PingFang.ttc"
FONT_CN_FALLBACK = "/System/Library/Fonts/STHeiti Medium.ttc"

CALLBACK_EN_SIZE = 38
CALLBACK_CN_SIZE = 36


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
    box = (1120, 62, 1595, 124)
    draw.rounded_rectangle(box, radius=15, fill=UI_FILL, outline=UI_OUTLINE, width=2)
    draw_fit_text(draw, (1138, 70, 1577, 116), text, 28 if cn else 30, 18, cn=cn, align="center")


def draw_sticky(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], text: str, cn: bool = False) -> None:
    x1, y1, x2, y2 = box
    draw.rounded_rectangle(box, radius=6, fill=STICKY, outline=STICKY_EDGE, width=2)
    draw_fit_text(
        draw,
        (x1 + 12, y1 + 10, x2 - 12, y2 - 10),
        text,
        CALLBACK_CN_SIZE if cn else CALLBACK_EN_SIZE,
        24,
        cn=cn,
        align="center",
    )


def load_base(index: int) -> Image.Image:
    img = Image.open(SRC / f"panel-{index}-v4-base.png").convert("RGB")
    return img.resize((W, H), Image.Resampling.LANCZOS)


def build_panel(index: int, cn: bool = False) -> Path:
    img = load_base(index)
    draw = ImageDraw.Draw(img)

    if index == 1:
        draw_fit_text(
            draw,
            (540, 125, 1015, 220),
            "终于，专心干活。" if cn else "Finally. Focus time.",
            42 if cn else 46,
            24,
            cn=cn,
            align="center",
        )
        draw_fit_text(draw, (845, 528, 1118, 584), "勿扰" if cn else "Do Not Disturb", 28 if cn else 24, 16, cn=cn, align="center")
    elif index == 2:
        callback = "在吗？问你个事——" if cn else "Quick question—"
        draw_fit_text(
            draw,
            (850, 150, 1395, 245),
            callback,
            CALLBACK_CN_SIZE if cn else CALLBACK_EN_SIZE,
            CALLBACK_CN_SIZE if cn else CALLBACK_EN_SIZE,
            cn=cn,
            align="center",
        )
    elif index == 4:
        draw_counter(draw, "睡眠：勿扰模式" if cn else "Sleep: do not disturb", cn=cn)
        draw_sticky(draw, (835, 386, 1138, 506), "在吗？" if cn else "Quick question?", cn=cn)

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
        1: ("Panel 1 v4 Prompt", "Image-generated text-free base: Xiaohei presses the moon do-not-disturb control and prepares to focus. Locked local text: EN `Finally. Focus time.` + `Do Not Disturb`; CN `终于，专心干活。` + `勿扰`."),
        2: ("Panel 2 v4 Prompt", "Image-generated text-free base: a coworker leans into Xiaohei's workspace and interrupts. Locked local callback setup: EN `Quick question—`; CN `在吗？问你个事——`."),
        3: ("Panel 3 v4 Prompt", "Image-generated text-free base: three physical interruption channels surround Xiaohei: paper airplane, desk phone, coworker peeking over divider. Locked local text: none."),
        4: ("Panel 4 v4 Prompt", "Image-generated text-free base: Xiaohei sits in a silver protective office fort with DND moon lamp, but a sticky note slips through. Locked local payoff text: EN `Quick question?` + `Sleep: do not disturb`; CN `在吗？` + `睡眠：勿扰模式`."),
    }
    for idx, (title, body) in prompts.items():
        (ROOT / f"panel-{idx}-v4-prompt.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")

    (ROOT / "v4-files.md").write_text(
        """# Daily 2026-06-08 Do Not Disturb v4 Files

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

- English review title: `Do Not Disturb`
- Chinese review title: `勿扰模式`
- Review-stage only; do not move to repository until三方 QA passes.
- P2/P4 callback text uses the same local font settings; punctuation changes intentionally mark live interruption vs sticky-note payoff.
- P4 should read without dialogue: the office fort and silver shell still fail against one sticky note.
- Xiaohei follows the canonical guardrail: black blob + white eyes + deadpan, no ears or paw pads.
- No product watermark, brand logo, Kubernetes logo, KubeBlocks logo, or internal meta label appears in the review comic.
""",
        encoding="utf-8",
    )


def main() -> None:
    en_panels = [build_panel(i) for i in range(1, 5)]
    cn_panels = [build_panel(i, cn=True) for i in range(1, 5)]

    build_comic(en_panels, "Do Not Disturb", ROOT / "comic-v4.png", ROOT / "comic-v4-review.png")
    build_comic(cn_panels, "勿扰模式", ROOT / "comic-v4-cn.png", ROOT / "comic-v4-review-cn.png", cn=True)
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
