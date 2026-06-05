from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

W, H = 1672, 941
BLACK = (18, 18, 18)
GRAY = (220, 220, 220)
SOFT_GRAY = (238, 238, 238)
BLUE = (74, 135, 190)
ORANGE = (238, 134, 28)
RED = (230, 78, 52)

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
                x = x1 + (x2 - x1 - width) / 2 - bbox[0]
            elif align == "right":
                x = x2 - width - bbox[0]
            else:
                x = x1 - bbox[0]
            y = y1 + (y2 - y1 - height) / 2 - bbox[1]
            draw.multiline_text((x, y), text, font=font, fill=fill, spacing=spacing, align=align)
            return

    font = load_font(min_size, cn=cn)
    draw.multiline_text((x1, y1), text, font=font, fill=fill, spacing=max(8, int(min_size * 0.22)), align=align)


def jitter(points: list[tuple[float, float]], amount: float = 2.2, seed: int = 0) -> list[tuple[float, float]]:
    rng = random.Random(seed)
    return [(x + rng.uniform(-amount, amount), y + rng.uniform(-amount, amount)) for x, y in points]


def line(draw: ImageDraw.ImageDraw, points: list[tuple[float, float]], fill=BLACK, width: int = 3, seed: int = 0) -> None:
    draw.line(jitter(points, seed=seed), fill=fill, width=width, joint="curve")


def rect(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], outline=BLACK, width: int = 3, seed: int = 0) -> None:
    x1, y1, x2, y2 = xy
    line(draw, [(x1, y1), (x2, y1), (x2, y2), (x1, y2), (x1, y1)], outline, width, seed)


def ellipse(draw: ImageDraw.ImageDraw, xy: tuple[int, int, int, int], fill=None, outline=BLACK, width: int = 3) -> None:
    draw.ellipse(xy, fill=fill, outline=outline, width=width)


def draw_xiaohei(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float = 1.0, mood: str = "normal") -> None:
    body = (cx - int(74 * scale), cy - int(92 * scale), cx + int(74 * scale), cy + int(92 * scale))
    ellipse(draw, body, fill=(0, 0, 0), outline=(0, 0, 0), width=max(3, int(4 * scale)))
    eye_y = cy - int(22 * scale)
    if mood == "stare":
        ellipse(draw, (cx + int(10 * scale), eye_y - int(11 * scale), cx + int(29 * scale), eye_y + int(11 * scale)), fill="white", outline="white", width=1)
        ellipse(draw, (cx + int(44 * scale), eye_y - int(11 * scale), cx + int(63 * scale), eye_y + int(11 * scale)), fill="white", outline="white", width=1)
    elif mood == "shock":
        ellipse(draw, (cx + int(5 * scale), eye_y - int(16 * scale), cx + int(30 * scale), eye_y + int(16 * scale)), fill="white", outline="white", width=1)
        ellipse(draw, (cx + int(45 * scale), eye_y - int(16 * scale), cx + int(70 * scale), eye_y + int(16 * scale)), fill="white", outline="white", width=1)
        line(draw, [(cx - int(84 * scale), cy - int(120 * scale)), (cx - int(112 * scale), cy - int(145 * scale))], width=max(2, int(3 * scale)), seed=22)
        line(draw, [(cx + int(84 * scale), cy - int(120 * scale)), (cx + int(112 * scale), cy - int(145 * scale))], width=max(2, int(3 * scale)), seed=23)
    else:
        ellipse(draw, (cx + int(14 * scale), eye_y - int(9 * scale), cx + int(31 * scale), eye_y + int(9 * scale)), fill="white", outline="white", width=1)
        ellipse(draw, (cx + int(48 * scale), eye_y - int(9 * scale), cx + int(65 * scale), eye_y + int(9 * scale)), fill="white", outline="white", width=1)

    line(draw, [(cx - int(38 * scale), cy + int(87 * scale)), (cx - int(42 * scale), cy + int(135 * scale))], width=max(4, int(5 * scale)), seed=24)
    line(draw, [(cx + int(38 * scale), cy + int(87 * scale)), (cx + int(42 * scale), cy + int(135 * scale))], width=max(4, int(5 * scale)), seed=25)
    line(draw, [(cx - int(43 * scale), cy + int(135 * scale)), (cx - int(24 * scale), cy + int(135 * scale))], width=max(4, int(5 * scale)), seed=26)
    line(draw, [(cx + int(42 * scale), cy + int(135 * scale)), (cx + int(63 * scale), cy + int(135 * scale))], width=max(4, int(5 * scale)), seed=27)


def draw_monitor(draw: ImageDraw.ImageDraw, percent: int, *, reset: bool = False) -> None:
    rect(draw, (460, 190, 1260, 650), width=4, seed=1)
    rect(draw, (505, 245, 1215, 575), outline=(90, 90, 90), width=2, seed=2)
    line(draw, [(760, 650), (735, 735), (985, 735), (960, 650)], width=4, seed=3)
    rect(draw, (675, 735, 1045, 780), width=4, seed=4)

    rect(draw, (590, 385, 1125, 475), outline=BLACK, width=4, seed=5)
    fill_w = int((1125 - 590 - 20) * (percent / 100))
    if fill_w > 0:
        draw.rounded_rectangle((600, 397, 600 + fill_w, 463), radius=8, fill=BLUE)
    if reset:
        line(draw, [(600, 397), (600, 463)], fill=RED, width=4, seed=30)
        line(draw, [(1120, 397), (1120, 463)], fill=RED, width=4, seed=31)

    pct_text = f"{percent}%"
    draw_fit_text(draw, (610, 300, 1105, 370), pct_text, 72, 42, align="center", fill=BLACK)


def draw_clock_marks(draw: ImageDraw.ImageDraw) -> None:
    for i in range(7):
        x = 1360 + i * 38
        line(draw, [(x, 155), (x + 12, 155)], fill=(160, 160, 160), width=2, seed=60 + i)
    for i in range(4):
        angle = -0.6 + i * 0.35
        x = 1378 + math.cos(angle) * 80
        y = 180 + math.sin(angle) * 35
        line(draw, [(1378, 180), (x, y)], fill=(180, 180, 180), width=2, seed=70 + i)


def draw_floor(draw: ImageDraw.ImageDraw) -> None:
    line(draw, [(210, 812), (1500, 812)], fill=(170, 170, 170), width=2, seed=90)
    line(draw, [(250, 850), (680, 850)], fill=(210, 210, 210), width=2, seed=91)
    line(draw, [(990, 842), (1420, 842)], fill=(210, 210, 210), width=2, seed=92)


def make_base(index: int) -> Path:
    img = Image.new("RGB", (W, H), "white")
    draw = ImageDraw.Draw(img)
    draw_floor(draw)

    if index == 1:
        draw_monitor(draw, 99)
        draw_xiaohei(draw, 285, 560, 1.0, mood="normal")
        line(draw, [(365, 595), (445, 545)], width=3, seed=101)
        for offset in (0, 14, 28):
            line(draw, [(1130 + offset, 515), (1160 + offset, 515)], fill=ORANGE, width=3, seed=110 + offset)
    elif index == 2:
        draw_monitor(draw, 99)
        draw_clock_marks(draw)
        draw_xiaohei(draw, 360, 565, 1.0, mood="stare")
        line(draw, [(435, 570), (515, 520)], width=3, seed=121)
        for offset in (0, 14, 28, 42):
            line(draw, [(1130 + offset, 515), (1160 + offset, 515)], fill=ORANGE, width=3, seed=130 + offset)
    elif index == 3:
        draw_monitor(draw, 0, reset=True)
        draw_xiaohei(draw, 350, 565, 1.1, mood="shock")
        for offset in (0, 24, 48):
            line(draw, [(575 + offset, 505), (560 + offset, 535)], fill=RED, width=3, seed=140 + offset)
            line(draw, [(1115 + offset, 505), (1140 + offset, 535)], fill=RED, width=3, seed=150 + offset)
    else:
        draw_monitor(draw, 99)
        draw_xiaohei(draw, 310, 540, 0.95, mood="normal")
        # A small improvised "residence" around the stuck progress bar.
        rect(draw, (160, 690, 555, 800), outline=BLACK, width=3, seed=170)
        line(draw, [(160, 690), (555, 800)], width=3, seed=171)
        line(draw, [(555, 690), (160, 800)], width=3, seed=172)
        rect(draw, (188, 628, 520, 690), outline=BLACK, width=3, seed=173)
        line(draw, [(202, 660), (505, 660)], fill=(160, 160, 160), width=2, seed=174)
        line(draw, [(370, 700), (430, 642)], fill=ORANGE, width=4, seed=175)
        line(draw, [(430, 642), (468, 700)], fill=ORANGE, width=4, seed=176)

    out = SRC / f"panel-{index}-v4-base.png"
    img.save(out)
    return out


def build_panel(index: int, cn: bool = False) -> Path:
    base = make_base(index)
    img = Image.open(base).convert("RGB")
    draw = ImageDraw.Draw(img)

    if cn:
        copy = {
            1: "就快好了。",
            2: "……马上就好。",
            3: "",
            4: "……我就住这儿了。",
        }[index]
        if copy:
            draw_fit_text(draw, (110, 110, 690, 230), copy, 46, 30, cn=True)
        if index == 4:
            draw_fit_text(draw, (1120, 115, 1530, 190), "睡眠：99%", 34, 24, cn=True)
        out = ROOT / f"panel-{index}-v4-cn.png"
    else:
        copy = {
            1: "Almost there.",
            2: "…any second now.",
            3: "",
            4: "…I live here now.",
        }[index]
        if copy:
            draw_fit_text(draw, (110, 110, 760, 230), copy, 48, 30)
        if index == 4:
            draw_fit_text(draw, (1120, 115, 1530, 190), "Sleep: 99%", 36, 24)
        out = ROOT / f"panel-{index}-v4.png"

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
        1: ("Panel 1 v4 Prompt", "Xiaohei watches a large monitor showing a progress bar at 99%, hopeful and still. Locked text: EN `Almost there.` / CN `就快好了。`."),
        2: ("Panel 2 v4 Prompt", "The same progress bar remains stuck at 99%; small clock/time marks imply waiting. Xiaohei leans in, staring. Locked text: EN `…any second now.` / CN `……马上就好。`."),
        3: ("Panel 3 v4 Prompt", "The progress bar has reset to 0%; Xiaohei freezes with wide eyes. No dialogue. This is the silent reversal beat."),
        4: ("Panel 4 v4 Prompt", "Xiaohei accepts the stuck progress bar as his new home, with a small improvised residence marker beside the monitor. Locked text: EN `…I live here now.` / CN `……我就住这儿了。`; counter EN `Sleep: 99%` / CN `睡眠：99%`."),
    }
    for idx, (title, body) in prompts.items():
        (ROOT / f"panel-{idx}-v4-prompt.md").write_text(f"# {title}\n\n{body}\n", encoding="utf-8")

    (ROOT / "v4-files.md").write_text(
        """# Daily 2026-06-05 99% v4 Files

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

- English final artwork title: `99%`
- Chinese final artwork title: `99%`
- No product watermark, brand logo, Kubernetes logo, KubeBlocks logo, or internal meta label appears in the final combined comic.
- Panel order is 1 -> 2 -> 3 -> 4.
- Chinese versions reuse the same deterministic source bases and local lettering.
- New readability workflow sample: one universal concept only; no narration fallback needed.
""",
        encoding="utf-8",
    )


def main() -> None:
    SRC.mkdir(parents=True, exist_ok=True)
    en_panels = [build_panel(i) for i in range(1, 5)]
    cn_panels = [build_panel(i, cn=True) for i in range(1, 5)]

    build_comic(en_panels, "99%", ROOT / "comic-v4.png", ROOT / "comic-v4-review.png")
    build_comic(cn_panels, "99%", ROOT / "comic-v4-cn.png", ROOT / "comic-v4-review-cn.png", cn=True)
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
