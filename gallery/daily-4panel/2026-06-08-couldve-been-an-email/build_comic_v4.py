from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

W, H = 1672, 941
BLACK = (18, 18, 18)
GRAY = (220, 220, 220)
UI_FILL = (249, 250, 248)
UI_OUTLINE = (196, 202, 202)
SCREEN_TEXT = (28, 30, 30)

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


def draw_clock(draw: ImageDraw.ImageDraw, time_text: str, minute_angle: str) -> None:
    # The generated clock is intentionally blank; overlay the time where readers can catch the gag in review size.
    cx, cy = 294, 184
    draw.ellipse((cx - 72, cy - 72, cx + 72, cy + 72), fill=(255, 255, 255), outline=(90, 94, 94), width=3)
    if minute_angle == "00":
        draw.line((cx, cy, cx, cy - 50), fill=BLACK, width=5)
        draw.line((cx, cy, cx + 38, cy - 22), fill=BLACK, width=5)
    else:
        draw.line((cx, cy, cx - 13, cy - 51), fill=BLACK, width=5)
        draw.line((cx, cy, cx + 22, cy - 42), fill=BLACK, width=5)
    draw.ellipse((cx - 5, cy - 5, cx + 5, cy + 5), fill=BLACK)
    draw_fit_text(draw, (cx - 82, cy + 72, cx + 82, cy + 124), time_text, 42, 28, align="center")


def draw_counter(draw: ImageDraw.ImageDraw, text: str, cn: bool = False) -> None:
    box = (1110, 62, 1588, 122)
    draw.rounded_rectangle(box, radius=15, fill=UI_FILL, outline=UI_OUTLINE, width=2)
    draw_fit_text(draw, (1128, 69, 1570, 114), text, 28 if cn else 30, 18, cn=cn, align="center")


def load_base(index: int) -> Image.Image:
    img = Image.open(SRC / f"panel-{index}-v4-base.png").convert("RGB")
    return img.resize((W, H), Image.Resampling.LANCZOS)


def build_panel(index: int, cn: bool = False) -> Path:
    img = load_base(index)
    draw = ImageDraw.Draw(img)

    if index == 1:
        draw_clock(draw, "2:00", "00")
        draw_fit_text(draw, (515, 338, 840, 430), "好，什么事？" if cn else "Okay, what's up?", 40 if cn else 44, 24, cn=cn)
    elif index == 2:
        draw_clock(draw, "2:55", "55")
    elif index == 3:
        draw_fit_text(
            draw,
            (640, 190, 1420, 405),
            "那…我们再同步一下。" if cn else "So… let's circle back.",
            48 if cn else 54,
            30,
            cn=cn,
            align="center",
            fill=SCREEN_TEXT,
        )
    elif index == 4:
        draw_fit_text(
            draw,
            (845, 260, 1450, 360),
            "这本来就是一封邮件。" if cn else "That was an email.",
            42 if cn else 48,
            26,
            cn=cn,
            align="center",
        )
        draw_counter(draw, "睡眠：开会中" if cn else "Sleep: in a meeting", cn=cn)

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
        1: ("Panel 1 v4 Prompt", "Image-generated text-free base: Xiaohei sits upright and attentive at the start of a meeting. Locked local text: EN `Okay, what's up?` / CN `好，什么事？`; clock `2:00`."),
        2: ("Panel 2 v4 Prompt", "Image-generated text-free base: the same meeting drags on and Xiaohei is flattened on the table. Locked local clock: `2:55`."),
        3: ("Panel 3 v4 Prompt", "Image-generated text-free base: exhausted meeting room with blank projection screen. Locked local screen text: EN `So… let's circle back.` / CN `那…我们再同步一下。`."),
        4: ("Panel 4 v4 Prompt", "Image-generated text-free base: Xiaohei leaves the meeting room deadpan. Locked local text: EN `That was an email.` + `Sleep: in a meeting`; CN `这本来就是一封邮件。` + `睡眠：开会中`."),
    }
    for idx, (title, body) in prompts.items():
        (ROOT / f"panel-{idx}-v4-prompt.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")

    (ROOT / "v4-files.md").write_text(
        """# Daily 2026-06-08 Could've Been an Email v4 Files

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

- English review title: `Could've Been an Email`
- Chinese review title: `这本来可以是一封邮件`
- Review-stage only; do not move to repository until三方 QA passes.
- Clock text `2:00` / `2:55` is deterministic local overlay and is the core readability device.
- P3 conclusion appears in the meeting screen/whiteboard object-native frame, not as a speech bubble.
- Xiaohei follows the canonical guardrail: black blob + white eyes + deadpan, no ears or paw pads.
- No product watermark, brand logo, Kubernetes logo, KubeBlocks logo, or internal meta label appears in the review comic.
""",
        encoding="utf-8",
    )


def main() -> None:
    en_panels = [build_panel(i) for i in range(1, 5)]
    cn_panels = [build_panel(i, cn=True) for i in range(1, 5)]

    build_comic(en_panels, "Could've Been an Email", ROOT / "comic-v4.png", ROOT / "comic-v4-review.png")
    build_comic(cn_panels, "这本来可以是一封邮件", ROOT / "comic-v4-cn.png", ROOT / "comic-v4-review-cn.png", cn=True)
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
