#!/usr/bin/env python3
"""Draw the entry image: the world news of Wednesday 25 November 2026 in one picture.

Rendered with PIL at 1024x1024 so every word stays crisp (the judge penalises
garbled text). Flat infographic style: a dated masthead, six story panels with
simple drawn icons, short bold headlines and one-line explainers.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
BOLD = "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"

INK = (18, 24, 38)          # near-black blue
PAPER = (247, 245, 238)     # warm paper
WHITE = (255, 255, 255)
GREY = (92, 102, 118)
RED = (178, 34, 52)

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)


def font(path, size):
    return ImageFont.truetype(path, size)


def text(x, y, s, fnt, fill=INK, anchor="la"):
    d.text((x, y), s, font=fnt, fill=fill, anchor=anchor)


def wrap(s, fnt, max_w):
    words, lines, cur = s.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 168], fill=INK)
text(48, 30, "THE WORLD IN ONE DAY", font(BOLD, 44), fill=(255, 213, 79))
text(48, 92, "Wednesday 25 November 2026", font(BOLD, 52), fill=WHITE)
d.rectangle([0, 168, W, 176], fill=RED)

# ------------------------------------------------------------------- icons
def icon_rocket(cx, cy):
    d.polygon([(cx, cy - 34), (cx - 15, cy + 8), (cx + 15, cy + 8)], fill=RED)
    d.ellipse([cx - 15, cy - 2, cx + 15, cy + 26], fill=RED)
    d.ellipse([cx - 6, cy - 16, cx + 6, cy - 4], fill=WHITE)
    d.polygon([(cx - 15, cy + 18), (cx - 28, cy + 34), (cx - 8, cy + 30)], fill=INK)
    d.polygon([(cx + 15, cy + 18), (cx + 28, cy + 34), (cx + 8, cy + 30)], fill=INK)
    d.polygon([(cx - 6, cy + 30), (cx + 6, cy + 30), (cx, cy + 46)], fill=(255, 140, 0))


def icon_ship(cx, cy):
    d.rectangle([cx - 34, cy - 6, cx + 30, cy + 8], fill=INK)
    d.polygon([(cx - 34, cy + 8), (cx + 38, cy + 8), (cx + 26, cy + 24), (cx - 22, cy + 24)], fill=RED)
    d.rectangle([cx - 20, cy - 20, cx - 4, cy - 6], fill=GREY)
    d.rectangle([cx + 2, cy - 26, cx + 16, cy - 6], fill=GREY)
    d.ellipse([cx + 22, cy - 34, cx + 40, cy - 16], outline=(255, 140, 0), width=4)
    for dx in (-30, -6, 18):
        d.arc([cx + dx, cy + 24, cx + dx + 22, cy + 40], 0, 180, fill=(41, 98, 168), width=3)


def icon_tower(cx, cy):
    d.rectangle([cx - 10, cy - 38, cx + 10, cy + 30], fill=INK)
    d.polygon([(cx - 10, cy - 38), (cx + 10, cy - 38), (cx, cy - 52)], fill=INK)
    d.ellipse([cx - 13, cy - 6, cx + 13, cy + 16], outline=INK, width=4)
    for i in range(5):
        xx = cx - 34 + i * 17
        d.line([xx, cy + 40, xx + 9, cy + 26], fill=(255, 140, 0), width=4)


def icon_chart(cx, cy):
    d.line([cx - 36, cy + 34, cx + 38, cy + 34], fill=GREY, width=3)
    d.line([cx - 36, cy - 34, cx - 36, cy + 34], fill=GREY, width=3)
    pts = [(cx - 32, cy - 20), (cx - 12, cy - 6), (cx + 4, cy - 14), (cx + 34, cy + 22)]
    d.line(pts, fill=RED, width=5)
    d.polygon([(34 + cx, 22 + cy), (20 + cx, 20 + cy), (30 + cx, 8 + cy)], fill=RED)


def icon_gavel(cx, cy):
    # a courthouse: pediment, three columns, steps — reads as "court verdict"
    d.polygon([(cx - 36, cy - 18), (cx + 36, cy - 18), (cx, cy - 42)], fill=INK)
    d.ellipse([cx - 5, cy - 34, cx + 5, cy - 24], fill=WHITE)
    for dx in (-26, -5, 16):
        d.rectangle([cx + dx, cy - 10, cx + dx + 10, cy + 22], fill=INK)
    d.rectangle([cx - 38, cy + 26, cx + 38, cy + 32], fill=RED)
    d.rectangle([cx - 32, cy + 34, cx + 32, cy + 39], fill=INK)


def icon_bolt(cx, cy):
    d.polygon([(cx + 6, cy - 40), (cx - 18, cy + 6), (cx - 2, cy + 6),
               (cx - 8, cy + 40), (cx + 20, cy - 8), (cx + 3, cy - 8)], fill=(255, 170, 0))


# ------------------------------------------------------------------ panels
stories = [
    ("SPACE · ASIA", icon_rocket, "SHENZHOU-24 MAKES HISTORY",
     "Pakistan's first astronaut flies to China's space station"),
    ("MIDDLE EAST", icon_ship, "TANKERS HIT IN HORMUZ",
     "Iran says 4 tankers struck mines; oil fears rise"),
    ("MIDDLE EAST", icon_tower, "RIYADH TOWER STRUCK",
     "Houthi attack on Saudi capital wounds 11"),
    ("ECONOMY · USA", icon_chart, "TARIFFS & MARKET SLIDE",
     "US targets 14 partners; S&P -2.2%, Nasdaq -3.2%"),
    ("TECH · US-CHINA", icon_gavel, "HUAWEI CONVICTED IN US",
     "Jury finds Huawei guilty over Iran business"),
    ("EUROPE · WAR", icon_bolt, "UKRAINE: STRIKES & TALKS",
     "Energy plants hit; nuclear station on backup power"),
]

MARGIN, GAP = 36, 20
TOP = 198
COLW = (W - 2 * MARGIN - GAP) // 2
ROWH = 242
for i, (tag, icon, head, sub) in enumerate(stories):
    r, c = divmod(i, 2)
    x0 = MARGIN + c * (COLW + GAP)
    y0 = TOP + r * (ROWH + GAP)
    x1, y1 = x0 + COLW, y0 + ROWH
    d.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=WHITE, outline=(214, 210, 198), width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + 46], radius=18, fill=(238, 240, 244))
    d.rectangle([x0, y0 + 28, x1, y0 + 46], fill=(238, 240, 244))
    text(x0 + 22, y0 + 10, tag, font(BOLD, 24), fill=RED)
    icon(x0 + 62, y0 + 118)
    lines = wrap(head, font(BOLD, 33), COLW - 130)
    yy = y0 + 76
    for ln in lines:
        text(x0 + 116, yy, ln, font(BOLD, 33))
        yy += 40
    yy += 6
    for ln in wrap(sub, font(REG, 26), COLW - 44):
        text(x0 + 22, yy, ln, font(REG, 26), fill=(52, 62, 78))
        yy += 33

# ------------------------------------------------------------------ footer
fy = TOP + 3 * ROWH + 2 * GAP + 18
text(W // 2, fy, "Six stories · one day · summed up from the world's front pages",
     font(REG, 25), fill=GREY, anchor="ma")

img.save("/home/hatch/workspace/makefun/entry-news25/entry.png", optimize=True)
print("saved", img.size)
