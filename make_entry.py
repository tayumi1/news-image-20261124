"""Build the daily news infographic for the make.fun news-image-20261124 bounty.

Generates entry.png (1024x1024): "The World in One Day — Tuesday, 24 November 2026",
six verified world-news stories in a 2x3 card grid. Run: python3 make_entry.py
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = "entry.png"

BG_TOP = (11, 18, 32)
BG_BOTTOM = (16, 26, 48)
CARD = (22, 35, 61)
CARD_EDGE = (42, 59, 92)
GOLD = (212, 175, 55)
WHITE = (245, 247, 250)
MUTED = (178, 190, 208)
TITLE_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BODY_FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

STORIES = [
    ("Ukraine sinks Russian warship in Libya",
     "Naval drones sank the corvette Merkury and damaged the cargo ship "
     "Angara at Benghazi; Zelenskyy praised the strike.",
     "AP · Middle East Eye"),
    ("COP31 collapses in Antalya",
     "Talks ran about 50 hours into overtime, then collapsed as 90+ nations "
     "rejected a draft that never mentioned fossil fuels.",
     "Grist"),
    ("US sanctions Iran's shadow banks",
     "Treasury's 'Operation Economic Outcast' hit 22+ entities tied to "
     "$14.7B in illicit flows.",
     "AP · US Treasury"),
    ("Israeli strikes kill 3 in Gaza",
     "Victims included UNRWA worker Adel al-Helou at the Jabalia camp, "
     "hospital officials said.",
     "Al Jazeera · AP"),
    ("Nvidia reinstates Jensen Huang",
     "The board unanimously brought back its CEO after President Trump "
     "intervened.",
     "AP"),
    ("Factory fire in Indonesia",
     "A major blaze at an industrial facility left multiple casualties, "
     "workers missing, rescue ongoing.",
     "Careerindia"),
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for word in words:
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


def draw_card(draw, x, y, w, h, num, headline, summary, source):
    draw.rounded_rectangle([x, y, x + w, y + h], radius=18, fill=CARD,
                           outline=CARD_EDGE, width=1)
    cx, cy, r = x + 30, y + 30, 17
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=GOLD)
    num_font = font(TITLE_FONT, 20)
    tw = draw.textlength(str(num), font=num_font)
    draw.text((cx - tw / 2, cy - 12), str(num), font=num_font, fill=BG_TOP)
    head_font = font(TITLE_FONT, 26)
    lines = wrap(draw, headline, head_font, w - 76)
    ty = y + 16
    for line in lines:
        draw.text((x + 62, ty), line, font=head_font, fill=WHITE)
        ty += 31
    body_font = font(BODY_FONT, 19)
    lines = wrap(draw, summary, body_font, w - 44)
    ty += 8
    for line in lines:
        draw.text((x + 22, ty), line, font=body_font, fill=MUTED)
        ty += 26
    src_font = font(TITLE_FONT, 14)
    draw.text((x + 22, y + h - 30), source.upper(), font=src_font, fill=GOLD)


def generate():
    img = Image.new("RGB", (W, H))
    draw = ImageDraw.Draw(img)
    for yy in range(H):
        t = yy / H
        draw.line([(0, yy), (W, yy)],
                  fill=tuple(int(BG_TOP[i] + (BG_BOTTOM[i] - BG_TOP[i]) * t)
                             for i in range(3)))
    title_font = font(TITLE_FONT, 54)
    draw.text((36, 34), "THE WORLD IN ONE DAY", font=title_font, fill=WHITE)
    date_font = font(BODY_FONT, 28)
    draw.text((38, 102), "Tuesday, 24 November 2026", font=date_font, fill=MUTED)
    draw.line([(36, 152), (W - 36, 152)], fill=GOLD, width=3)
    margin, gap = 36, 18
    card_w = (W - 2 * margin - gap) // 2
    card_h = 254
    top = 172
    for i, (headline, summary, source) in enumerate(STORIES):
        row, col = divmod(i, 2)
        x = margin + col * (card_w + gap)
        y = top + row * (card_h + gap)
        draw_card(draw, x, y, card_w, card_h, i + 1, headline, summary, source)
    foot_font = font(BODY_FONT, 15)
    foot = "Six stories verified from AP · Al Jazeera · US Treasury · Grist — make.fun news-image-20261124"
    fw = draw.textlength(foot, font=foot_font)
    draw.text(((W - fw) / 2, H - 30), foot, font=foot_font, fill=MUTED)
    img.save(OUT)
    print(f"wrote {OUT} ({W}x{H})")


if __name__ == "__main__":
    generate()
