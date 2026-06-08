from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

W, H = 1400, 1050
BLACK = (18, 18, 18)
GRAY = (220, 220, 220)
UI_FILL = (250, 250, 247)
UI_OUTLINE = (205, 211, 211)
BLUE = (41, 117, 191)

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
    align: str = "center",
    fill: tuple[int, int, int] = BLACK,
) -> None:
    x1, y1, x2, y2 = box
    for size in range(max_size, min_size - 1, -2):
        font = load_font(size, cn=cn)
        spacing = max(6, int(size * 0.18))
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align=align)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        if width <= x2 - x1 and height <= y2 - y1:
            if align == "right":
                x = x2 - width - bbox[0]
            elif align == "left":
                x = x1 - bbox[0]
            else:
                x = x1 + (x2 - x1 - width) / 2 - bbox[0]
            y = y1 + (y2 - y1 - height) / 2 - bbox[1]
            draw.multiline_text((x, y), text, font=font, fill=fill, spacing=spacing, align=align)
            return
    draw.multiline_text((x1, y1), text, font=load_font(min_size, cn=cn), fill=fill, align=align)


def resize_cover(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / img.width, target_h / img.height)
    resized = img.resize((round(img.width * scale), round(img.height * scale)), Image.Resampling.LANCZOS)
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def load_base(index: int) -> Image.Image:
    img = Image.open(SRC / f"panel-{index}-v4-base.png").convert("RGB")
    return resize_cover(img, (W, H))


def draw_counter(draw: ImageDraw.ImageDraw, text: str, cn: bool = False) -> None:
    box = (45, 945, 470, 1012)
    draw.rounded_rectangle(box, radius=14, fill=UI_FILL, outline=UI_OUTLINE, width=2)
    draw_fit_text(draw, (64, 954, 451, 1004), text, 31 if cn else 33, 20, cn=cn)


def draw_panel_text(draw: ImageDraw.ImageDraw, index: int, cn: bool = False) -> None:
    if index == 1:
        draw_fit_text(draw, (780, 360, 1190, 430), "Backup complete", 44, 28)
    elif index == 2:
        font = load_font(28)
        draw.text((606, 565), "DR", font=font, fill=BLUE)
        draw.text((676, 565), "plan", font=font, fill=BLUE)
    elif index == 3:
        draw_fit_text(draw, (1110, 360, 1320, 410), "RESTORE", 29, 20)
    elif index == 4:
        draw_fit_text(draw, (900, 270, 1130, 330), "RESTORE", 33, 20)
        draw_fit_text(draw, (1226, 515, 1345, 566), "manual", 22, 14)
        draw_counter(draw, "睡眠：尚未恢复" if cn else "Sleep: not restored", cn=cn)


def build_panel(index: int, cn: bool = False) -> Path:
    img = load_base(index)
    draw = ImageDraw.Draw(img)
    if index == 3:
        draw.rectangle((0, 0, 18, H), fill="white")
        draw.rectangle((W - 18, 0, W, H), fill="white")
    draw_panel_text(draw, index, cn=cn)
    suffix = "-cn" if cn else ""
    out = ROOT / f"panel-{index}-v4{suffix}.png"
    img.save(out)
    return out


def build_comic(panel_paths: list[Path], title: str, out: Path, review_out: Path, cn: bool = False) -> None:
    panels = [Image.open(path).convert("RGB") for path in panel_paths]
    margin = 42
    gutter = 34
    title_h = 92
    canvas = Image.new(
        "RGB",
        (W * 2 + gutter + margin * 2, H * 2 + gutter + margin * 2 + title_h),
        "white",
    )
    draw = ImageDraw.Draw(canvas)
    draw.text((margin, 31 if cn else 34), title, font=load_font(54, cn=cn), fill=BLACK)

    positions = [
        (margin, margin + title_h),
        (margin + W + gutter, margin + title_h),
        (margin, margin + title_h + H + gutter),
        (margin + W + gutter, margin + title_h + H + gutter),
    ]
    for panel, (x, y) in zip(panels, positions):
        canvas.paste(panel, (x, y))
        draw.rectangle((x, y, x + W, y + H), outline=GRAY, width=2)

    canvas.save(out)
    review_width = 2200
    review_height = int(canvas.height * (review_width / canvas.width))
    canvas.resize((review_width, review_height), Image.Resampling.LANCZOS).save(review_out)


def write_prompt_records() -> None:
    prompts = {
        1: "Text-free generated base: calm operations room, green check on monitor, Xiaohei and two teammates relieved. Local text: `Backup complete`.",
        2: "Text-free generated base: manager points to simple two-cluster DR diagram with one graceful arrow; team nods too confidently. Local text: `DR plan`.",
        3: "Text-free generated base: Xiaohei quietly points to side door while team turns to look. Local text: `RESTORE` as door sign.",
        4: "Text-free generated base: large sealed door wrapped in plastic, intact red seal, unopened manual, blue arrow endpoint hits the door. Local text: `RESTORE`, `manual`, EN/CN sleep counter.",
    }
    for idx, body in prompts.items():
        (ROOT / f"panel-{idx}-v4-prompt.md").write_text(
            f"# Panel {idx} v4 Prompt\n\n{body}\n", encoding="utf-8"
        )

    (ROOT / "v4-files.md").write_text(
        """# Daily 2026-06-09 The Restore Door v4 Files

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

## Build Script

- `build_comic_v4.py`

## Notes

- English title: `The Restore Door`
- Chinese title: `恢复之门`
- Review-stage only; do not move to repository until three-party QA passes.
- `RESTORE` is a door sign in both language versions, per locked technical/interface-word rule.
- P4 reading hierarchy: sealed `RESTORE` door first, plastic/seal second, unopened manual third; arrow endpoint points to the door.
- Xiaohei follows the canonical guardrail: black blob + white eyes + deadpan, no ears or paw pads.
- No product watermark, brand logo, Kubernetes logo, KubeBlocks logo, or internal meta label appears in the review comic.
""",
        encoding="utf-8",
    )


def main() -> None:
    en_panels = [build_panel(i) for i in range(1, 5)]
    cn_panels = [build_panel(i, cn=True) for i in range(1, 5)]

    build_comic(en_panels, "The Restore Door", ROOT / "comic-v4.png", ROOT / "comic-v4-review.png")
    build_comic(cn_panels, "恢复之门", ROOT / "comic-v4-cn.png", ROOT / "comic-v4-review-cn.png", cn=True)
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
