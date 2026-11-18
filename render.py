#!/usr/bin/env python3
"""Render the 17 November 2026 world-news front page (1024x1024 PNG).

Build-time tool only: it runs here with Pillow to produce entry.png, which
the entry program (main.py, stdlib only) then copies to /output/entry.png.
It is kept in the repo as provenance for how the image was made.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 24, 31)
NAVY = (15, 42, 74)
NAVY_LT = (28, 68, 110)
RED = (179, 38, 30)
GOLD = (201, 162, 39)
GREY = (90, 96, 104)
SKY = (168, 205, 225)
SEA = (46, 92, 128)
TEAL = (14, 122, 110)
GREEN = (46, 125, 50)
ORANGE = (230, 126, 34)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, fill, max_w, leading=None):
    """Draw wrapped text; returns y just below the last line."""
    leading = leading or int(fnt.size * 1.22)
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def starburst(draw, cx, cy, r_out, r_in, n=10, fill=ORANGE):
    pts = []
    for i in range(n * 2):
        r = r_out if i % 2 == 0 else r_in
        a = math.pi * i / n - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill)


# ---------------------------------------------------------------- icons
def icon_bridge(d, x, y, s):
    """Crimean Bridge under drone attack: sky, sea, deck, arches, bursts."""
    d.rectangle([x, y, x + s, y + s], fill=SKY)
    d.rectangle([x, y + int(s * 0.62), x + s, y + s], fill=SEA)
    # sun / smoke
    d.ellipse([x + s * 0.72, y + s * 0.08, x + s * 0.88, y + s * 0.24],
              fill=(245, 222, 160))
    # deck
    dy = y + int(s * 0.58)
    d.rectangle([x, dy, x + s, dy + 8], fill=(40, 44, 52))
    # towers + arches
    for tx in (0.22, 0.72):
        px = x + int(s * tx)
        d.line([px, dy, px, y + int(s * 0.22)], fill=(40, 44, 52), width=6)
    d.arc([x + int(s * 0.06), dy - int(s * 0.34), x + int(s * 0.48),
           dy + int(s * 0.10)], 180, 360, fill=(40, 44, 52), width=5)
    d.arc([x + int(s * 0.52), dy - int(s * 0.34), x + int(s * 0.94),
           dy + int(s * 0.10)], 180, 360, fill=(40, 44, 52), width=5)
    # cables
    for tx in (0.22, 0.72):
        px = x + int(s * tx)
        d.line([px, y + int(s * 0.24), x + int(s * 0.06), dy],
               fill=(70, 76, 86), width=2)
        d.line([px, y + int(s * 0.24), x + int(s * 0.94), dy],
               fill=(70, 76, 86), width=2)
    # explosion bursts on the deck
    starburst(d, x + int(s * 0.38), dy - 14, 20, 9, fill=(245, 176, 65))
    starburst(d, x + int(s * 0.38), dy - 14, 11, 5, fill=(230, 90, 30))
    starburst(d, x + int(s * 0.66), dy - 10, 14, 6, fill=(245, 176, 65))
    # drones
    for dx, dy2 in ((0.12, 0.18), (0.55, 0.10), (0.85, 0.30)):
        px, py = x + int(s * dx), y + int(s * dy2)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=INK)
        d.line([px - 9, py, px - 4, py], fill=INK, width=2)
        d.line([px + 4, py, px + 9, py], fill=INK, width=2)
    # waves
    for wy in (0.72, 0.84, 0.95):
        d.arc([x + 8, y + int(s * wy), x + int(s * 0.45), y + int(s * wy) + 18],
              200, 340, fill=(220, 235, 242), width=3)


def icon_tanker(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 232, 240))
    d.rectangle([x, y + int(s * 0.60), x + s, y + s], fill=SEA)
    # hull
    d.polygon([(x + 8, y + int(s * 0.52)), (x + s - 8, y + int(s * 0.52)),
               (x + s - 26, y + int(s * 0.72)), (x + 26, y + int(s * 0.72))],
              fill=(120, 40, 32))
    # containers
    for i, c in enumerate(((240, 200, 60), (60, 140, 90), (220, 120, 40))):
        cx = x + int(s * (0.18 + i * 0.22))
        d.rectangle([cx, y + int(s * 0.38), cx + int(s * 0.18),
                     y + int(s * 0.52)], fill=c)
    # funnel
    d.rectangle([x + int(s * 0.74), y + int(s * 0.34), x + int(s * 0.84),
                 y + int(s * 0.52)], fill=INK)
    # flame + smoke
    starburst(d, x + int(s * 0.55), y + int(s * 0.30), 18, 8, fill=(245, 176, 65))
    starburst(d, x + int(s * 0.55), y + int(s * 0.30), 10, 4, fill=(230, 90, 30))
    d.ellipse([x + int(s * 0.60), y + int(s * 0.10), x + int(s * 0.68),
               y + int(s * 0.20)], fill=(120, 120, 120))
    d.ellipse([x + int(s * 0.68), y + int(s * 0.05), x + int(s * 0.78),
               y + int(s * 0.16)], fill=(150, 150, 150))
    # waves
    for wy in (0.80, 0.90):
        d.arc([x + 10, y + int(s * wy), x + int(s * 0.5), y + int(s * wy) + 16],
              200, 340, fill=(220, 235, 242), width=3)


def icon_globe(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 232, 240))
    cx, cy, r = x + s // 2, y + s // 2, int(s * 0.36)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(126, 180, 214),
              outline=NAVY, width=4)
    d.arc([cx - r, cy - r, cx + r, cy + r], 90, 270, fill=NAVY, width=3)
    d.arc([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r], 90, 270,
          fill=NAVY, width=3)
    d.line([cx - r, cy, cx + r, cy], fill=NAVY, width=3)
    d.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)], 20, 160,
          fill=NAVY, width=3)
    # three leaders
    for i, c in enumerate((RED, NAVY, (200, 170, 40))):
        px = x + int(s * (0.22 + i * 0.28))
        py = y + int(s * (0.72 + (i % 2) * 0.10))
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=c, outline=(255, 255, 255),
                  width=2)


def icon_flags4(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 232, 240))
    cols = (RED, NAVY, (200, 170, 40), (40, 110, 60))
    for i, c in enumerate(cols):
        px = x + int(s * (0.14 + i * 0.20))
        d.line([px, y + int(s * 0.22), px, y + int(s * 0.82)], fill=INK, width=3)
        d.rectangle([px, y + int(s * 0.22), px + int(s * 0.16),
                     y + int(s * 0.42)], fill=c)
    d.ellipse([x + int(s * 0.30), y + int(s * 0.60), x + int(s * 0.70),
               y + int(s * 0.80)], outline=TEAL, width=4)


def icon_cyber(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(24, 28, 38))
    # padlock
    bx0, by0 = x + int(s * 0.28), y + int(s * 0.44)
    bx1, by1 = x + int(s * 0.72), y + int(s * 0.82)
    d.arc([x + int(s * 0.36), y + int(s * 0.18), x + int(s * 0.64),
           y + int(s * 0.52)], 180, 360, fill=(245, 200, 60), width=7)
    d.rounded_rectangle([bx0, by0, bx1, by1], radius=8, fill=(245, 200, 60))
    d.ellipse([x + int(s * 0.47), y + int(s * 0.55), x + int(s * 0.53),
               y + int(s * 0.61)], fill=INK)
    d.rectangle([x + int(s * 0.485), y + int(s * 0.60), x + int(s * 0.515),
                 y + int(s * 0.72)], fill=INK)
    # warning triangle
    d.polygon([(x + int(s * 0.10), y + int(s * 0.86)),
               (x + int(s * 0.26), y + int(s * 0.58)),
               (x + int(s * 0.42), y + int(s * 0.86))], fill=RED)
    d.text((x + int(s * 0.235), y + int(s * 0.66)), "!", font=font(SANS_B, 22),
           fill=(255, 255, 255))


def icon_chart(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 232, 240))
    d.line([x + 10, y + s - 12, x + s - 8, y + s - 12], fill=GREY, width=3)
    d.line([x + 10, y + 10, x + 10, y + s - 12], fill=GREY, width=3)
    pts = [(x + 16, y + int(s * 0.25)), (x + int(s * 0.35), y + int(s * 0.38)),
           (x + int(s * 0.55), y + int(s * 0.34)), (x + int(s * 0.72),
           y + int(s * 0.62)), (x + s - 14, y + int(s * 0.78))]
    d.line(pts, fill=RED, width=6, joint="curve")
    d.polygon([(x + s - 14, y + int(s * 0.78)), (x + s - 30, y + int(s * 0.70)),
               (x + s - 26, y + int(s * 0.86))], fill=RED)


def icon_cyclone(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 232, 240))
    cx, cy = x + s // 2, y + s // 2
    w = max(3, s // 12)
    for i, f in enumerate((0.13, 0.23, 0.33, 0.42)):
        r = int(s * f)
        d.arc([cx - r, cy - r, cx + r, cy + r], 30 + i * 55, 300 + i * 55,
              fill=TEAL, width=w)
    r0 = max(2, int(s * 0.06))
    d.ellipse([cx - r0, cy - r0, cx + r0, cy + r0], fill=TEAL)


def icon_leaf(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 232, 240))
    d.pieslice([x + int(s * 0.18), y + int(s * 0.12), x + int(s * 0.82),
                y + int(s * 0.88)], 200, 20, fill=GREEN)
    d.line([x + int(s * 0.50), y + int(s * 0.80), x + int(s * 0.50),
            y + int(s * 0.94)], fill=(60, 60, 40), width=5)
    d.line([x + int(s * 0.50), y + int(s * 0.55), x + int(s * 0.30),
            y + int(s * 0.40)], fill=(220, 235, 220), width=3)
    d.line([x + int(s * 0.50), y + int(s * 0.55), x + int(s * 0.70),
            y + int(s * 0.40)], fill=(220, 235, 220), width=3)


def icon_plane(d, x, y, s):
    d.rectangle([x, y, x + s, y + s], fill=(214, 232, 240))
    d.polygon([(x + int(s * 0.15), y + int(s * 0.30)),
               (x + int(s * 0.85), y + int(s * 0.55)),
               (x + int(s * 0.15), y + int(s * 0.80)),
               (x + int(s * 0.38), y + int(s * 0.55))], fill=NAVY_LT)
    d.line([x + int(s * 0.15), y + int(s * 0.80), x + int(s * 0.85),
            y + int(s * 0.55)], fill=(255, 255, 255), width=3)


# ---------------------------------------------------------------- layout
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---- masthead
    d.rectangle([0, 0, W, 118], fill=NAVY)
    d.text((W // 2, 16), "THE WORLD IN ONE DAY", font=font(SERIF_B, 58),
           fill=(255, 255, 255), anchor="ma")
    d.text((W // 2, 84), "A picture of the day's news  ·  make.fun",
           font=font(SANS, 20), fill=(190, 205, 220), anchor="ma")
    d.rectangle([0, 118, W, 126], fill=RED)
    d.text((W // 2, 138), "TUESDAY 17 NOVEMBER 2026",
           font=font(SANS_B, 40), fill=NAVY, anchor="ma")
    d.line([M, 186, W - M, 186], fill=INK, width=3)

    # ---- lead story
    ly = 200
    icon_bridge(d, M, ly, 250)
    tx = M + 250 + 22
    tw = W - M - tx
    d.text((tx, ly), "UKRAINE  ·  WAR", font=font(SANS_B, 21), fill=RED)
    y = text_block(d, tx, ly + 30,
                   "Ukraine hits Crimean Bridge in 1,300-drone barrage",
                   font(SERIF_B, 37), INK, tw, leading=44)
    text_block(d, tx, y + 6,
               "Traffic halted after a second strike in under 24 hours. "
               "Russia says it downed 1,336 drones and hit Kyiv's river "
               "crossings in reply.",
               font(SANS, 22), (50, 56, 64), tw, leading=28)
    d.line([M, 466, W - M, 466], fill=INK, width=2)

    # ---- 2x2 grid
    grid = [
        ("MIDDLE EAST  ·  SHIPPING", "Tankers hit by mines near the Strait of Hormuz",
         "Two tankers hit mines and caught fire; more hit east of the strait.",
         icon_tanker),
        ("ASIA-PACIFIC  ·  DIPLOMACY", "China confirms first Xi–Trump–Putin summit",
         "The three leaders meet in Shenzhen on Thursday, at the APEC summit.",
         icon_globe),
        ("ASIA  ·  SUMMITS", "Quad leaders meet in Manila",
         "Trump joins Modi, Takaichi and Albanese at the ASEAN summit in Manila.",
         icon_flags4),
        ("TECHNOLOGY  ·  CYBERATTACK", "Hack hits 178 top websites, incl. BBC and CNN",
         "Malicious code via Optimizely tried to steal crypto and card data.",
         icon_cyber),
    ]
    gy = 482
    cell_w = (W - 2 * M - 24) // 2
    cell_h = 140
    for i, (kick, head, deck, icon) in enumerate(grid):
        cx = M + (i % 2) * (cell_w + 24)
        cy = gy + (i // 2) * (cell_h + 12)
        icon(d, cx, cy, 124)
        tx2 = cx + 124 + 14
        tw2 = cx + cell_w - tx2
        d.text((tx2, cy + 2), kick, font=font(SANS_B, 16), fill=RED)
        y2 = text_block(d, tx2, cy + 24, head, font(SERIF_B, 23), INK, tw2,
                        leading=27)
        text_block(d, tx2, y2 + 3, deck, font(SANS, 17), (50, 56, 64), tw2,
                   leading=21)
    d.line([M, 786, W - M, 786], fill=INK, width=2)

    # ---- bottom strip: 4 columns
    strip = [
        ("MARKETS", "Stocks tumble; Nasdaq in correction",
         "Nasdaq −2.49%; Brent −3.6%.",
         icon_chart),
        ("WEATHER", "Cyclone Akvan heads for India's east coast",
         "Odisha evacuates as the storm turns severe.",
         icon_cyclone),
        ("CLIMATE", "COP31 draft: exit fossil fuels faster",
         "Negotiators' draft deal calls for 'accelerated action'.",
         icon_leaf),
        ("EUROPE", "Five nations plan a Rwanda return hub",
         "Five EU states in talks with Rwanda.",
         icon_plane),
    ]
    sy = 800
    col_w = (W - 2 * M - 3 * 16) // 4
    for i, (kick, head, deck, icon) in enumerate(strip):
        cx = M + i * (col_w + 16)
        icon(d, cx, sy, 52)
        d.text((cx, sy + 60), kick, font=font(SANS_B, 15), fill=RED)
        y3 = text_block(d, cx, sy + 80, head, font(SERIF_B, 19), INK, col_w,
                        leading=21)
        text_block(d, cx, y3 + 2, deck, font(SANS, 15), (50, 56, 64), col_w,
                   leading=17)

    # ---- footer
    d.line([M, 972, W - M, 972], fill=INK, width=2)
    d.text((W // 2, 978),
           "ALSO: Pattinson named the next James Bond  ·  Fire kills 11 in Thailand  ·  "
           "WHO warns of illness in Gaza as winter floods arrive",
           font=font(SANS, 15), fill=GREY, anchor="ma")
    d.text((W // 2, 996),
           "All events reported on Tuesday 17 November 2026  ·  Sources: AP, Reuters, "
           "Al Jazeera, RNZ, Outlook India",
           font=font(SANS_B, 15), fill=INK, anchor="ma")

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
