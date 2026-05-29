from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SRC = ROOT / "source"
FONT = "/System/Library/Fonts/PingFang.ttc"

BLACK = (20, 20, 20)
RED = (224, 24, 24)
ORANGE = (238, 110, 0)
BLUE = (0, 96, 220)


def font(size):
    return ImageFont.truetype(FONT, size=size)


def text(draw, xy, s, size=42, fill=BLACK, anchor=None, align="left"):
    draw.multiline_text(
        xy,
        s,
        font=font(size),
        fill=fill,
        spacing=int(size * 0.25),
        anchor=anchor,
        align=align,
    )


def fit_text(draw, box, s, max_size=44, min_size=22, fill=BLACK, align="center"):
    x1, y1, x2, y2 = box
    for size in range(max_size, min_size - 1, -2):
        f = font(size)
        bbox = draw.multiline_textbbox((0, 0), s, font=f, spacing=int(size * 0.25), align=align)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        if w <= x2 - x1 and h <= y2 - y1:
            draw.multiline_text(
                (x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2),
                s,
                font=f,
                fill=fill,
                spacing=int(size * 0.25),
                anchor="mm",
                align=align,
            )
            return
    text(draw, (x1, y1), s, min_size, fill)


def annotate_panel(i):
    img = Image.open(SRC / f"panel-{i}-base.png").convert("RGB")
    draw = ImageDraw.Draw(img)

    if i == 1:
        fit_text(draw, (665, 335, 905, 445), "03:00\n主库告警 x47", 38, 24, RED)
        text(draw, (230, 230), "……又是这个点。", 38, ORANGE)
        text(draw, (55, 55), "①", 54, BLACK)
    elif i == 2:
        fit_text(draw, (145, 290, 430, 430), "默认题：\nstateless？", 40, 24, BLUE)
        fit_text(draw, (650, 120, 990, 265), "我有 7 个脚本……\n和 0 小时\n睡眠。", 40, 24, ORANGE)
        fit_text(draw, (1085, 310, 1350, 420), "我们有记忆！", 40, 24, RED)
        text(draw, (55, 55), "②", 54, BLACK)
    elif i == 3:
        text(draw, (965, 150), "声明期望状态，\n流程我来编排。", 34, BLUE)
        fit_text(draw, (640, 710, 960, 790), "……它怎么一点都不慌。", 34, 22, ORANGE)
        labels = ["备份", "恢复", "扩容", "故障切换"]
        boxes = [(1410, 315, 1570, 370), (1410, 435, 1570, 490), (1410, 560, 1570, 615), (1360, 680, 1570, 735)]
        for label, box in zip(labels, boxes):
            fit_text(draw, box, label, 28, 20, ORANGE)
        text(draw, (55, 55), "③", 54, BLACK)
    elif i == 4:
        text(draw, (140, 200), "昨晚那么大动静，\n是谁救的火？", 42, BLACK)
        text(draw, (565, 265), "我……主要负责\n没添乱。", 34, ORANGE)
        fit_text(draw, (1190, 750, 1575, 855), "睡眠：6h\n历史新高", 38, 24, ORANGE)
        fit_text(draw, (1130, 625, 1350, 680), "正常运行", 32, 22, BLUE)
        text(draw, (55, 55), "④", 54, BLACK)

    out = ROOT / f"panel-{i}.png"
    img.save(out)
    return out


def assemble(paths):
    panels = [Image.open(p).convert("RGB") for p in paths]
    w, h = panels[0].size
    margin = 40
    gutter = 36
    title_h = 110
    canvas = Image.new("RGB", (w * 2 + gutter + margin * 2, h * 2 + gutter + margin * 2 + title_h), "white")
    draw = ImageDraw.Draw(canvas)
    text(draw, (margin, 36), "凌晨三点，数据库城市又响了", 54, BLACK)
    text(draw, (margin, 96), "KubeBlocks 四格漫画试作 | 小黑 = SRE", 28, BLUE)
    positions = [
        (margin, margin + title_h),
        (margin + w + gutter, margin + title_h),
        (margin, margin + title_h + h + gutter),
        (margin + w + gutter, margin + title_h + h + gutter),
    ]
    for panel, pos in zip(panels, positions):
        canvas.paste(panel, pos)
        x, y = pos
        draw.rectangle((x, y, x + w, y + h), outline=(220, 220, 220), width=2)
    out = ROOT / "comic.png"
    canvas.save(out)
    return out


if __name__ == "__main__":
    panel_paths = [annotate_panel(i) for i in range(1, 5)]
    assemble(panel_paths)
