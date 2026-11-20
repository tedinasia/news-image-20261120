#!/usr/bin/env python3
"""THE WORLD TODAY -- front page for Friday 20 November 2026.

Draws a 1024 x 1024 newspaper front page with Pillow and writes it to
/output/entry.png (or to the path given as the first argument).

No network, no randomness, no timestamps, no reading of the clock: the
same input always produces the same bytes, so two runs write identical
files. Only the standard library and Pillow are used.

The stories are the world news of Friday 20 November 2026 as reported
that day: the first Trump-Xi-Putin summit in Shenzhen and its peace
declaration; Anthropic's record $81.3bn IPO; the UN court ruling that
Myanmar committed genocide against the Rohingya; the tanker fire in the
Strait of Hormuz and the Houthi missile strike on Riyadh; a fifth
straight daily fall for the S&P 500; and Cyclone Akvan's landfall in
Odisha, India.
"""

import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
WIDTH = 1024
HEIGHT = 1024
MARGIN = 36
CONTENT = WIDTH - 2 * MARGIN  # 952

PAPER = (246, 241, 229)   # newsprint off-white
INK = (17, 17, 17)        # headline black
RED = (163, 22, 33)       # kicker / accent red
NAVY = (31, 56, 100)      # panels, charts
GRAY = (88, 88, 84)       # secondary text
PANEL = (226, 232, 240)   # illustration panel blue-grey
PANEL_WARM = (238, 230, 208)  # warm panel
GOLD = (201, 162, 39)
SKY = (186, 205, 224)
SEA = (52, 110, 165)
ORANGE = (214, 90, 20)
RULE = (60, 60, 60)

# ------------------------------------------------------------------ fonts
# Try the usual system locations in order; fall back to Pillow's built-in
# bitmap font so the program still runs if a machine has no TTF fonts.
_SERIF_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerif-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf",
]
_SERIF = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSerif-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSerif.ttf",
]
_SANS_BOLD = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf",
]
_SANS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf",
    "/usr/share/fonts/truetype/freefont/FreeSans.ttf",
]


def _load(candidates, size):
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def serif_bold(size):
    return _load(_SERIF_BOLD, size)


def serif(size):
    return _load(_SERIF, size)


def sans_bold(size):
    return _load(_SANS_BOLD, size)


def sans(size):
    return _load(_SANS, size)


# ------------------------------------------------------------------- text
def wrap(text, font, max_width):
    """Split text into lines that fit max_width, measured with the font."""
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = word if not current else current + " " + word
        if font.getlength(trial) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lines(draw, x, y, lines, font, fill, leading):
    """Draw lines top-left at (x, y); return the y just below the block."""
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def draw_kicker(draw, x, y, text, color=RED, size=19):
    font = sans_bold(size)
    draw.text((x, y), text, font=font, fill=color)
    return y + size + 6


def rule(draw, x, y, width, weight=2, color=RULE):
    draw.rectangle([x, y, x + width, y + weight], fill=color)
    return y + weight


def double_rule(draw, x, y, width):
    rule(draw, x, y, width, 3)
    rule(draw, x, y + 6, width, 1)
    return y + 10


# ------------------------------------------------------------ illustrations
def draw_summit(draw, box):
    """Shenzhen skyline at dusk with the three flags of the summit."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL)
    # setting sun
    cx, cy, r = x1 - 62, y0 + 58, 34
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    # skyline silhouettes, back row then front row
    back = [(0, 96), (34, 150), (72, 118), (112, 168), (150, 128),
            (188, 158), (226, 104), (262, 142)]
    for bx, bh in back:
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + 34, y1 - 46],
                       fill=(96, 118, 158))
    front = [(10, 70), (58, 112), (104, 84), (158, 126), (206, 92),
             (252, 120)]
    for bx, bh in front:
        draw.rectangle([x0 + bx, y1 - bh, x0 + bx + 44, y1 - 46],
                       fill=NAVY)
    # lit windows on the front towers
    for wx in (20, 68, 116, 168, 216, 262):
        for wy in (y1 - 120, y1 - 96, y1 - 72):
            draw.rectangle([x0 + wx, wy, x0 + wx + 7, wy + 9], fill=GOLD)
    # ground
    draw.rectangle([x0, y1 - 46, x1, y1 - 40], fill=INK)
    # three flags on poles above the ground line
    flags = [
        ("US", [(178, 44, 34), (255, 255, 255), (178, 44, 34),
                (255, 255, 255), (178, 44, 34)]),
        ("CN", [(222, 32, 32)]),
        ("RU", [(255, 255, 255), (36, 84, 160), (222, 32, 32)]),
    ]
    fx = x0 + 26
    for _name, stripes in flags:
        # pole
        draw.rectangle([fx, y0 + 118, fx + 4, y1 - 46], fill=INK)
        fw, fh = 74, 46
        top = y0 + 118
        stripe_h = fh / len(stripes)
        for i, colour in enumerate(stripes):
            draw.rectangle(
                [fx + 4, top + i * stripe_h, fx + 4 + fw,
                 top + (i + 1) * stripe_h],
                fill=colour,
            )
        draw.rectangle([fx + 4, top, fx + 4 + fw, top + fh], outline=INK)
        fx += 96
    # caption inside the panel
    draw.text((x0 + 16, y1 - 34), "SHENZHEN  •  THE THREE FLAGS",
              font=sans_bold(14), fill=GRAY)


def draw_bars(draw, box):
    """Rising bars: Anthropic's record listing."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL_WARM)
    base = y1 - 12
    heights = [16, 26, 36, 48, 62]
    bw, gap = 34, 12
    x = x0 + 26
    for i, h in enumerate(heights):
        colour = RED if i == len(heights) - 1 else NAVY
        draw.rectangle([x, base - h, x + bw, base], fill=colour)
        x += bw + gap
    draw.rectangle([x0 + 14, base, x1 - 14, base + 2], fill=INK)
    draw.text((x0 + 26, y0 + 8), "$81.3BN", font=sans_bold(17), fill=RED)


def draw_scales(draw, box):
    """Scales of justice: the Hague ruling."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=PANEL)
    cx = (x0 + x1) // 2
    top = y0 + 10
    # pillar and beam
    draw.rectangle([cx - 2, top, cx + 2, y1 - 14], fill=NAVY)
    draw.rectangle([x0 + 30, top + 4, x1 - 30, top + 8], fill=NAVY)
    draw.ellipse([cx - 6, top - 6, cx + 6, top + 6], fill=GOLD)
    # base
    draw.rectangle([cx - 26, y1 - 14, cx + 26, y1 - 8], fill=NAVY)
    # two pans hanging from the beam ends
    for px in (x0 + 34, x1 - 34):
        draw.line([px, top + 8, px, top + 30], fill=NAVY, width=2)
        draw.line([px - 22, top + 30, px, top + 8], fill=NAVY, width=2)
        draw.line([px + 22, top + 30, px, top + 8], fill=NAVY, width=2)
        draw.pieslice([px - 24, top + 28, px + 24, top + 62],
                      start=0, end=180, fill=GOLD)
        draw.rectangle([px - 24, top + 28, px + 24, top + 32], fill=GOLD)


def draw_tanker(draw, box):
    """A tanker on fire in the Strait of Hormuz."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(214, 230, 240))
    sea_y = y1 - 24
    # flame above the tanker, kept inside the panel
    fx = (x0 + x1) // 2 + 46
    draw.polygon([(fx - 20, sea_y - 26), (fx - 6, sea_y - 50),
                  (fx + 4, sea_y - 34), (fx + 14, sea_y - 52),
                  (fx + 24, sea_y - 26)], fill=ORANGE)
    draw.polygon([(fx - 9, sea_y - 26), (fx - 1, sea_y - 40),
                  (fx + 10, sea_y - 26)], fill=(255, 196, 0))
    # hull and bow, with a small bridge tower
    draw.polygon([(x0 + 20, sea_y - 18), (x1 - 58, sea_y - 18),
                  (x1 - 20, sea_y - 4), (x0 + 20, sea_y - 4)], fill=INK)
    draw.rectangle([x0 + 30, sea_y - 34, x0 + 58, sea_y - 18], fill=NAVY)
    draw.rectangle([x0 + 36, sea_y - 46, x0 + 48, sea_y - 34], fill=NAVY)
    # waves
    for wx in (x0 + 16, x0 + 94, x0 + 172, x0 + 238):
        draw.arc([wx, sea_y + 4, wx + 44, sea_y + 18], start=180, end=360,
                 fill=SEA, width=2)


def draw_downtrend(draw, box):
    """A falling market line."""
    x0, y0, x1, y1 = box
    points = [(x0 + 6, y0 + 10), (x0 + 26, y0 + 16), (x0 + 44, y0 + 14),
              (x0 + 62, y0 + 30), (x0 + 80, y0 + 40), (x0 + 98, y0 + 52)]
    draw.line(points, fill=RED, width=4, joint="curve")
    draw.polygon([(x0 + 98, y0 + 52), (x0 + 84, y0 + 46),
                  (x0 + 92, y0 + 62)], fill=RED)
    draw.text((x0 + 6, y1 - 20), "-2.0%", font=sans_bold(16), fill=RED)


def draw_cyclone(draw, box):
    """Cyclone swirl over the coast."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r, start in ((30, 20), (22, 110), (14, 200)):
        draw.arc([cx - r, cy - r, cx + r, cy + r], start=start,
                 end=start + 250, fill=NAVY, width=3)
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=RED)
    draw.rectangle([x0, y1 - 8, x1, y1 - 4], fill=SEA)


# -------------------------------------------------------------------- page
def build_page():
    img = Image.new("RGB", (WIDTH, HEIGHT), PAPER)
    draw = ImageDraw.Draw(img)
    x = MARGIN

    # ---- masthead
    title_font = serif_bold(84)
    title = "THE WORLD TODAY"
    tw = title_font.getlength(title)
    draw.text(((WIDTH - tw) / 2, 26), title, font=title_font, fill=INK)
    y = double_rule(draw, x, 128, CONTENT)
    # ---- dateline
    date_font = sans_bold(19)
    draw.text((x, y + 4), "FRIDAY, 20 NOVEMBER 2026", font=date_font,
              fill=INK)
    right = "WORLD NEWS IN ONE PAGE"
    draw.text((WIDTH - MARGIN - date_font.getlength(right), y + 4), right,
              font=date_font, fill=INK)
    y = rule(draw, x, y + 34, CONTENT, 1)

    # ---- lead story
    y = 190
    lead_w = 620
    y = draw_kicker(draw, x, y, "THE SUMMIT  •  SHENZHEN, CHINA")
    head_font = serif_bold(52)
    head = wrap("TRUMP, XI AND PUTIN SIGN PEACE DECLARATION", head_font,
                lead_w)
    y = draw_lines(draw, x, y + 2, head, head_font, INK, 60)
    deck_font = serif(21)
    deck = wrap("The first three-way summit of the three leaders puts "
                "Ukraine first \u2014 and ends with a four-point declaration.",
                deck_font, lead_w)
    y = draw_lines(draw, x, y + 8, deck, deck_font, INK, 27)
    # lead illustration, right of the text
    draw_summit(draw, (x + lead_w + 16, 190, WIDTH - MARGIN, 470))
    y = rule(draw, x, 484, CONTENT, 2)

    # ---- three cards
    card_y = 500
    card_w = 304
    card_gap = 20
    cards = [
        ("ANTHROPIC  •  NEW YORK", "ANTHROPIC SOARS 17% ON RECORD "
         "$81.3BN IPO",
         "Priced at $83, shares close near $97.", draw_bars),
        ("THE HAGUE  •  JUSTICE", "MYANMAR GUILTY OF GENOCIDE, UN COURT "
         "RULES",
         "First ruling of its kind against a state, over the Rohingya "
         "in 2017.", draw_scales),
        ("THE GULF  •  HORMUZ", "TANKER ABLAZE IN HORMUZ AS GULF BURNS",
         "Mine strike sets a ship on fire; a Houthi missile hits "
         "Riyadh's tallest tower.", draw_tanker),
    ]
    cx = x
    for kicker, headline, deck_text, painter in cards:
        painter(draw, (cx, card_y, cx + card_w, card_y + 74))
        ky = draw_kicker(draw, cx, card_y + 84, kicker, size=17)
        h_font = serif_bold(27)
        h_lines = wrap(headline, h_font, card_w)
        hy = draw_lines(draw, cx, ky + 2, h_lines, h_font, INK, 32)
        d_font = sans(18)
        d_lines = wrap(deck_text, d_font, card_w)
        draw_lines(draw, cx, hy + 6, d_lines, d_font, GRAY, 22)
        cx += card_w + card_gap
    y = rule(draw, x, 772, CONTENT, 2)

    # ---- bottom row: markets + cyclone
    bottom_y = 788
    half_w = 466
    # markets
    by = draw_kicker(draw, x, bottom_y, "MARKETS  •  NEW YORK & TOKYO")
    h_font = serif_bold(26)
    m_head = wrap("S&P 500 FALLS 2% FOR FIFTH DAY", h_font, 350)
    my = draw_lines(draw, x, by + 2, m_head, h_font, INK, 31)
    draw_downtrend(draw, (x + 366, bottom_y + 6, x + half_w, bottom_y + 78))
    d_font = sans(18)
    draw.text((x, my + 6),
              "Nikkei drops 4.7% as AI valuations wobble.",
              font=d_font, fill=GRAY)
    # cyclone
    cx2 = x + half_w + 20
    by = draw_kicker(draw, cx2, bottom_y, "CYCLONE AKVAN  •  INDIA")
    c_head = wrap("AKVAN SLAMS INTO ODISHA", h_font, 350)
    cy = draw_lines(draw, cx2, by + 2, c_head, h_font, INK, 31)
    draw_cyclone(draw, (cx2 + 366, bottom_y + 6, cx2 + half_w,
                        bottom_y + 78))
    draw.text((cx2, cy + 6),
              "Landfall begins; heavy rain lashes the coast.",
              font=d_font, fill=GRAY)
    y = rule(draw, x, 918, CONTENT, 1)

    # ---- footer ticker (shrunk until it fits the page width)
    ticker = ("KYIV HIT BY 4 MISSILES   •   EUROPE READY FOR RUSSIA "
              "TALKS   •   COP31 CLOSES   •   PETE ROSE PARDONED")
    tick_size = 17
    tick_font = sans(tick_size)
    while tick_font.getlength(ticker) > CONTENT and tick_size > 12:
        tick_size -= 1
        tick_font = sans(tick_size)
    tw = tick_font.getlength(ticker)
    draw.text(((WIDTH - tw) / 2, 930), ticker, font=tick_font, fill=INK)
    y = rule(draw, x, 962, CONTENT, 1)
    col_font = sans_bold(15)
    colophon = "THE WORLD TODAY  •  FRIDAY 20 NOVEMBER 2026  •  ONE PAGE, THE WHOLE DAY"
    cw = col_font.getlength(colophon)
    draw.text(((WIDTH - cw) / 2, 974), colophon, font=col_font, fill=GRAY)

    return img


def main():
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/output/entry.png")
    out.parent.mkdir(parents=True, exist_ok=True)
    page = build_page()
    page.save(out, format="PNG")


if __name__ == "__main__":
    main()
