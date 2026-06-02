from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"

OUT = ROOT / "comic-v4-cn.png"
REVIEW_OUT = ROOT / "comic-v4-review-cn.png"

FONT_CN = "/System/Library/Fonts/PingFang.ttc"
FONT_FALLBACK = "/System/Library/Fonts/STHeiti Medium.ttc"

BLACK = (18, 18, 18)
GRAY = (220, 220, 220)
RED = (224, 24, 24)
WHITE = (255, 255, 255)


def load_font(size: int) -> ImageFont.FreeTypeFont:
    for path in (FONT_CN, FONT_FALLBACK):
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
    align: str = "center",
) -> None:
    x1, y1, x2, y2 = box
    for size in range(max_size, min_size - 1, -2):
        font = load_font(size)
        spacing = int(size * 0.18)
        bbox = draw.multiline_textbbox((0, 0), text, font=font, spacing=spacing, align=align)
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        if width <= x2 - x1 and height <= y2 - y1:
            anchor = "mm" if align == "center" else "lm"
            pos = ((x1 + x2) / 2, (y1 + y2) / 2) if align == "center" else (x1, (y1 + y2) / 2)
            draw.multiline_text(
                pos,
                text,
                font=font,
                fill=BLACK,
                spacing=spacing,
                align=align,
                anchor=anchor,
            )
            return

    font = load_font(min_size)
    draw.multiline_text((x1, y1), text, font=font, fill=BLACK, spacing=int(min_size * 0.18), align=align)


def build_panel_1() -> Image.Image:
    img = Image.open(SRC / "panel-1-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    draw_fit_text(draw, (255, 245, 520, 505), "03:00\n主库宕机\n×47", max_size=50, min_size=32)
    draw_fit_text(draw, (820, 330, 1230, 455), "…又来了。\n偏偏三点。", max_size=46, min_size=32, align="left")

    city_alert = (1355, 502)
    draw.ellipse((city_alert[0] - 4, city_alert[1] - 4, city_alert[0] + 4, city_alert[1] + 4), fill=RED)
    for dx, dy in ((0, -16), (12, -10), (-12, -10)):
        draw.line((city_alert[0], city_alert[1] - 8, city_alert[0] + dx, city_alert[1] + dy), fill=RED, width=3)

    img.save(ROOT / "panel-1-v4-cn.png")
    return img


def build_panel_2() -> Image.Image:
    img = Image.open(SRC / "panel-2-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    draw.ellipse((920, 582, 1080, 652), fill=WHITE)
    draw_fit_text(draw, (340, 220, 575, 350), "默认假设：\n无状态？", max_size=34, min_size=24)
    draw_fit_text(draw, (705, 255, 1000, 365), "7 个脚本…\n睡眠 0 小时。", max_size=36, min_size=26, align="left")
    draw_fit_text(draw, (980, 535, 1190, 585), "我们有状态！", max_size=28, min_size=20)
    draw_fit_text(draw, (1235, 730, 1505, 775), "一条也不能丢！", max_size=28, min_size=20)

    img.save(ROOT / "panel-2-v4-cn.png")
    return img


def build_panel_3() -> Image.Image:
    img = Image.open(SRC / "panel-3-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    draw_fit_text(draw, (915, 280, 1220, 375), "声明期望状态，\n流程交给我编排。", max_size=27, min_size=20)
    draw_fit_text(draw, (245, 430, 565, 520), "…它怎么\n一点都不慌？", max_size=32, min_size=24, align="left")
    draw_fit_text(draw, (575, 510, 705, 555), "备份", max_size=27, min_size=20)
    draw_fit_text(draw, (745, 810, 890, 855), "恢复", max_size=27, min_size=20)
    draw_fit_text(draw, (1130, 807, 1265, 852), "扩容", max_size=27, min_size=20)
    draw_fit_text(draw, (1400, 730, 1535, 775), "切换", max_size=27, min_size=20)

    img.save(ROOT / "panel-3-v4-cn.png")
    return img


def build_panel_4() -> Image.Image:
    img = Image.open(SRC / "panel-4-v4-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    draw_fit_text(draw, (235, 290, 600, 410), "昨晚动静这么大，\n谁救的火？", max_size=34, min_size=24, align="left")
    draw_fit_text(draw, (835, 385, 1245, 500), "我…主要负责\n没添乱。", max_size=34, min_size=24, align="left")
    draw_fit_text(draw, (1040, 695, 1240, 795), "睡眠：\n6 分钟", max_size=35, min_size=24)

    img.save(ROOT / "panel-4-v4-cn.png")
    return img


def build_comic(panels: list[Image.Image]) -> None:
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
    draw.text((margin, 30), "凌晨三点，数据库城市又响了", font=load_font(54), fill=BLACK)

    positions = [
        (margin, margin + title_h),
        (margin + width + gutter, margin + title_h),
        (margin, margin + title_h + height + gutter),
        (margin + width + gutter, margin + title_h + height + gutter),
    ]
    for panel, (x, y) in zip(panels, positions):
        canvas.paste(panel, (x, y))
        draw.rectangle((x, y, x + width, y + height), outline=GRAY, width=2)

    canvas.save(OUT)
    review_width = 2400
    review_height = int(canvas.height * (review_width / canvas.width))
    canvas.resize((review_width, review_height), Image.Resampling.LANCZOS).save(REVIEW_OUT)


def main() -> None:
    panels = [build_panel_1(), build_panel_2(), build_panel_3(), build_panel_4()]
    build_comic(panels)
    print(OUT)
    print(REVIEW_OUT)


if __name__ == "__main__":
    main()
