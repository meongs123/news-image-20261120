# render.py logic, rebuilt from scratch for the v3 image (Sat 21 Nov 2026).
# Draws one 1024x1024 broadsheet that sums up Friday 20 November 2026:
# masthead + day-in-numbers strip + region/field bars, three large lead
# cards, ten small lead cards with flat illustrations, a schematic world
# map with numbered pins, a briefs grid, a red DATE CHECK box and a
# sources footer. Pillow only; no network; no clock or random input, so
# two runs on the same stories.py produce byte-identical PNGs.
# Run:  python3 compose.py [out.png]     (default entry.png beside this file)
import math
import os, sys
from PIL import Image, ImageDraw, ImageFont
from stories import DATE_CHECK, FIELDS, FOOTER, LEAD_IDS
from stories import MAP_PINS, MASTHEAD_DECK, NUMBERS, REGIONS
from stories import STORIES, TITLE_DATE, TOP_STRIP_LEFT

PAGE = 1024
EDGE = 14
SPAN = PAGE - 2 * EDGE

PAL = {
    "paper": (247, 241, 227),
    "card": (255, 253, 246),
    "ink": (26, 26, 26),
    "muted": (90, 84, 70),
    "rule": (201, 191, 168),
    "red": (176, 30, 36),
    "navy": (22, 50, 74),
    "map_bg": (237, 230, 210),
    "land": (203, 185, 143),
    "pink": (255, 238, 238),
    "white": (255, 255, 255),
}

FONT_FOLDER = "/usr/share/fonts/truetype/dejavu"

_FONTS = {}


def typeface(kind, size):
    """Cached TrueType face. kind: serif/serif-bold/serif-italic/sans/sans-bold."""
    key = (kind, size)
    if key in _FONTS:
        return _FONTS[key]
    names = {
        "serif": "DejaVuSerif.ttf",
        "serif-bold": "DejaVuSerif-Bold.ttf",
        "serif-italic": "DejaVuSerif-Italic.ttf",
        "sans": "DejaVuSans.ttf",
        "sans-bold": "DejaVuSans-Bold.ttf",
    }
    fname = names[kind]
    path = os.path.join(FONT_FOLDER, fname)
    if not os.path.exists(path):
        path = os.path.join(FONT_FOLDER, "DejaVuSans.ttf")
    face = ImageFont.truetype(path, size)
    _FONTS[key] = face
    return face


def to_rgb(spec):
    """'#rrggbb' -> (r, g, b); plain tuples pass through untouched."""
    if isinstance(spec, tuple):
        return spec
    s = spec.lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def tint_for(region):
    """Region bar colour for a story region; grey when unknown."""
    for label, _count, colour in REGIONS:
        if label.lower() == region.lower():
            return to_rgb(colour)
    return (85, 85, 85)


def split_lines(canvas, text, face, limit):
    """Greedy wrap: pack as many words per line as fit inside limit px."""
    out = []
    current = ""
    for word in text.split():
        joined = (current + " " + word).strip()
        if not current or canvas.textlength(joined, font=face) <= limit:
            current = joined
        else:
            out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def draw_lines(canvas, pos, text, face, limit, colour, most=None, gap=None):
    """Paint wrapped text; returns the y coordinate just under the last line."""
    x, y = pos
    step = gap if gap is not None else int(face.size * 1.18)
    rows = split_lines(canvas, text, face, limit)
    if most is not None:
        rows = rows[:most]
    for row in rows:
        canvas.text((x, y), row, font=face, fill=colour)
        y += step
    return y  # y just below the last painted line


def cap_text(canvas, text, face, limit):
    """Clip text to limit px, ending with an ellipsis when it was clipped."""
    if canvas.textlength(text, font=face) <= limit:
        return text
    mark = "\u2026"
    cut = text
    while cut and canvas.textlength(cut + mark, font=face) > limit:
        cut = cut[:-1]
    return cut + mark


# ---- flat illustrations, drawn fresh with PIL shapes only ----
# Each art_* function paints inside (x, y, w, h) and never reads the story
# text; the card code below adds headline/deck/source on top of it.

def art_kyiv(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(12, 28, 50))
    for sx, sy in [(0.07, 0.14), (0.20, 0.26), (0.41, 0.08), (0.63, 0.20),
                   (0.83, 0.12), (0.95, 0.30)]:
        c.ellipse([x + sx * w - 2, y + sy * h - 2, x + sx * w + 2, y + sy * h + 2],
                  fill=(255, 238, 170))
    c.rectangle([x, y + int(h * 0.74), x + w, y + h], fill=(30, 66, 100))
    for bx in (0.04, 0.54):
        c.arc([x + bx * w, y + int(h * 0.46), x + (bx + 0.40) * w, y + int(h * 0.98)],
              180, 360, fill=(225, 225, 215), width=4)
        c.line([x + bx * w, y + int(h * 0.70), x + (bx + 0.40) * w, y + int(h * 0.70)],
               fill=(225, 225, 215), width=3)
    for mx0, my0, mx1, my1 in [(0.34, 0.06, 0.18, 0.42), (0.70, 0.10, 0.56, 0.40)]:
        c.line([x + mx0 * w, y + my0 * h, x + mx1 * w, y + my1 * h],
               fill=(255, 196, 70), width=3)
    for fx, fy, r in [(0.14, 0.62, 8), (0.20, 0.58, 5), (0.10, 0.66, 4),
                      (0.62, 0.64, 7)]:
        c.ellipse([x + fx * w - r, y + fy * h - r, x + fx * w + r, y + fy * h + r],
                  fill=(255, 110, 15))
        c.ellipse([x + fx * w - r // 2, y + fy * h - r // 2,
                   x + fx * w + r // 2, y + fy * h + r // 2], fill=(255, 216, 80))


def art_akvan(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + int(h * 0.48)], fill=(176, 210, 228))
    c.rectangle([x, y + int(h * 0.48), x + w, y + h], fill=(38, 102, 144))
    c.polygon([(x + int(w * 0.66), y), (x + w, y), (x + w, y + h),
               (x + int(w * 0.58), y + h), (x + int(w * 0.70), y + int(h * 0.52))],
              fill=(214, 196, 150))
    cx, cy = x + int(w * 0.34), y + int(h * 0.44)
    for r, start, end in [(30, 40, 320), (21, 140, 400), (12, 220, 480), (5, 0, 360)]:
        c.arc([cx - r, cy - r, cx + r, cy + r], start, end, fill=(255, 255, 255), width=4)
    c.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
    for rx in (0.08, 0.24, 0.50, 0.72, 0.88):
        c.line([x + rx * w, y + int(h * 0.10), x + (rx - 0.04) * w, y + int(h * 0.32)],
               fill=(116, 156, 186), width=2)
    c.text((x + 6, y + h - 14), "07:30 IST", font=typeface("sans-bold", 10),
           fill=PAL["white"])


def art_rout(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(16, 26, 38))
    for gy in (0.22, 0.48, 0.74):
        c.line([x, y + gy * h, x + w, y + gy * h], fill=(44, 60, 80), width=1)
    pts = [(0.05, 0.14), (0.20, 0.26), (0.36, 0.22), (0.52, 0.42),
           (0.70, 0.58), (0.86, 0.78), (0.96, 0.74)]
    for (fx, fy), (tx, ty) in zip(pts, pts[1:]):
        c.line([x + fx * w, y + fy * h, x + tx * w, y + ty * h],
               fill=(228, 58, 48), width=4)
    for fx, fy in pts:
        c.ellipse([x + fx * w - 3, y + fy * h - 3, x + fx * w + 3, y + fy * h + 3],
                  fill=(255, 118, 98))
    c.polygon([(x + int(w * 0.88), y + int(h * 0.68)), (x + int(w * 0.96), y + int(h * 0.68)),
               (x + int(w * 0.92), y + int(h * 0.78))], fill=(228, 58, 48))
    c.text((x + 6, y + h - 14), "NIKKEI -5.1%  KOSPI -5.2%  TAIEX -6.2%",
           font=typeface("sans-bold", 9), fill=PAL["white"])


def art_poland(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(164, 192, 210))
    c.rectangle([x, y, x + int(w * 0.30), y + int(h * 0.12)], fill=PAL["white"])
    c.rectangle([x, y + int(h * 0.12), x + int(w * 0.30), y + int(h * 0.24)],
                fill=(198, 38, 48))
    c.rectangle([x, y + int(h * 0.62), x + w, y + h], fill=(92, 136, 76))
    c.polygon([(x, y + h), (x + w, y + int(h * 0.78)), (x + w, y + h)],
              fill=(116, 116, 106))
    mx, my = x + int(w * 0.38), y + int(h * 0.30)
    c.polygon([(mx, my), (mx + 48, my + 24), (mx + 40, my + 34), (mx - 6, my + 10)],
              fill=(86, 91, 96))
    c.polygon([(mx + 36, my + 20), (mx + 54, my + 16), (mx + 48, my + 30)],
              fill=(66, 71, 76))
    ix, iy = x + int(w * 0.68), y + int(h * 0.72)
    for r, col in [(14, (255, 158, 38)), (7, (255, 218, 88))]:
        c.ellipse([ix - r, iy - r, ix + r, iy + r], fill=col)
    c.line([ix - 18, iy - 22, ix, iy], fill=(116, 116, 116), width=2)


def art_ukeu(c, x, y, w, h):
    mid = x + w // 2
    c.rectangle([x, y, mid, y + h], fill=(18, 38, 88))
    c.line([x, y, mid, y + h], fill=PAL["white"], width=4)
    c.line([mid, y, x, y + h], fill=PAL["white"], width=4)
    c.line([x + w // 4, y, x + w // 4, y + h], fill=PAL["white"], width=8)
    c.line([x, y + h // 2, mid, y + h // 2], fill=PAL["white"], width=8)
    c.line([x + w // 4, y, x + w // 4, y + h], fill=(198, 38, 48), width=4)
    c.line([x, y + h // 2, mid, y + h // 2], fill=(198, 38, 48), width=4)
    c.rectangle([mid, y, x + w, y + h], fill=(0, 49, 150))
    ccx, ccy, cr = mid + w // 4, y + h // 2, int(h * 0.28)
    for star in range(12):
        theta = -math.pi / 2 + star * (2 * math.pi / 12)
        sx = ccx + cr * math.cos(theta)
        sy = ccy + cr * math.sin(theta)
        c.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 208, 0))
    c.rectangle([x, y + h - 16, x + w, y + h], fill=(255, 208, 0))
    c.text((x + 6, y + h - 14), "RESET DEAL", font=typeface("sans-bold", 10),
           fill=PAL["ink"])


def art_cop31(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(12, 72, 76))
    cx, cy, r = x + int(w * 0.36), y + int(h * 0.54), int(h * 0.32)
    c.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(50, 128, 178))
    c.ellipse([cx - int(r * 0.6), cy - int(r * 0.45), cx - int(r * 0.1),
               cy + int(r * 0.2)], fill=(88, 168, 98))
    c.ellipse([cx + int(r * 0.05), cy + int(r * 0.25), cx + int(r * 0.55),
               cy + int(r * 0.65)], fill=(88, 168, 98))
    c.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=PAL["white"], width=2)
    kx, ky, kr = x + int(w * 0.82), y + int(h * 0.24), 13
    c.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=PAL["card"],
              outline=PAL["ink"])
    c.line([kx, ky, kx, ky - kr + 3], fill=PAL["ink"], width=2)
    c.line([kx, ky, kx + kr - 5, ky + 3], fill=PAL["ink"], width=2)
    c.text((x + 6, y + h - 14), "OVERTIME", font=typeface("sans-bold", 10),
           fill=PAL["white"])
    c.text((x + w - 84, y + h - 14), "NO DEAL YET",
           font=typeface("sans-bold", 10), fill=(255, 218, 88))


def art_italy(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(236, 224, 196))
    for i, col in enumerate([(0, 138, 68), PAL["white"], (198, 38, 48)]):
        c.polygon([(x + i * w // 3, y), (x + (i + 1) * w // 3, y),
                   (x + (i + 1) * w // 3 - 12, y + 14), (x + i * w // 3 + 12, y + 14)],
                  fill=col)
    for i, hx in enumerate((0.08, 0.26, 0.44, 0.62, 0.80, 0.92)):
        hy = 0.52 + (0.05 if i % 2 else 0.0)
        c.ellipse([x + hx * w - 8, y + hy * h - 8, x + hx * w + 8, y + hy * h + 8],
                  fill=(56, 46, 40))
        c.pieslice([x + hx * w - 13, y + hy * h + 5, x + hx * w + 13, y + h + 8],
                   180, 360, fill=(48, 80, 136) if i % 2 else (146, 56, 56))
    for px, py, col in [(0.16, 0.26, PAL["white"]), (0.54, 0.22, (255, 226, 116)),
                        (0.82, 0.30, PAL["white"])]:
        c.line([x + px * w, y + py * h + 16, x + px * w, y + int(h * 0.50)],
               fill=(86, 76, 66), width=2)
        c.rectangle([x + px * w - 18, y + py * h, x + px * w + 18, y + py * h + 16],
                    fill=col, outline=(116, 106, 91))


def art_houthis(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + int(h * 0.52)], fill=(202, 220, 228))
    c.rectangle([x, y + int(h * 0.52), x + w, y + h], fill=(32, 86, 118))
    for cx in (0.10, 0.34):
        c.line([x + cx * w, y + int(h * 0.10), x + cx * w, y + int(h * 0.56)],
               fill=(66, 76, 86), width=4)
        c.line([x + cx * w, y + int(h * 0.12), x + (cx + 0.20) * w, y + int(h * 0.28)],
               fill=(66, 76, 86), width=3)
    c.polygon([(x + int(w * 0.48), y + int(h * 0.58)), (x + int(w * 0.92), y + int(h * 0.58)),
               (x + int(w * 0.87), y + int(h * 0.76)), (x + int(w * 0.54), y + int(h * 0.76))],
              fill=(36, 41, 51))
    for i, col in enumerate([(196, 56, 46), (36, 116, 86), (216, 156, 36)]):
        c.rectangle([x + int(w * (0.54 + i * 0.11)), y + int(h * 0.42),
                     x + int(w * (0.63 + i * 0.11)), y + int(h * 0.56)], fill=col)
    tx, ty = x + int(w * 0.78), y + int(h * 0.06)
    c.polygon([(tx, ty), (tx + 30, ty + 26), (tx - 30, ty + 26)], fill=(236, 186, 26),
              outline=(146, 96, 0))
    c.text((tx - 3, ty + 5), "!", font=typeface("sans-bold", 18), fill=PAL["ink"])


def art_gta(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + int(h * 0.52)], fill=(56, 30, 82))
    c.ellipse([x + int(w * 0.74), y + 6, x + int(w * 0.74) + 24, y + 30],
              fill=(255, 188, 88))
    c.rectangle([x, y + int(h * 0.52), x + w, y + h], fill=(28, 16, 46))
    for bx, bw, bh in [(0.03, 0.13, 0.28), (0.18, 0.09, 0.42), (0.30, 0.15, 0.22),
                       (0.48, 0.11, 0.36), (0.62, 0.13, 0.26), (0.78, 0.11, 0.44)]:
        c.rectangle([x + bx * w, y + int(h * (0.60 - bh)), x + (bx + bw) * w,
                     y + int(h * 0.60)], fill=(18, 10, 32))
        for wy in (0.08, 0.20):
            c.rectangle([x + (bx + 0.02) * w, y + int(h * (0.60 - bh + wy)),
                         x + (bx + bw - 0.02) * w,
                         y + int(h * (0.60 - bh + wy + 0.04))],
                        fill=(255, 208, 108))
    c.text((x + 6, y + h - 14), "EST. $2.36bn", font=typeface("sans-bold", 10),
           fill=PAL["white"])


def art_bepi(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(7, 9, 22))
    for sx, sy in [(0.06, 0.14), (0.18, 0.06), (0.48, 0.10), (0.72, 0.20),
                   (0.90, 0.06), (0.32, 0.24), (0.60, 0.04)]:
        c.ellipse([x + sx * w - 1, y + sy * h - 1, x + sx * w + 1, y + sy * h + 1],
                  fill=PAL["white"])
    mx, my, mr = x + int(w * 0.70), y + int(h * 0.62), int(h * 0.28)
    c.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(166, 156, 146))
    for cfx, cfy, cr in [(0.60, 0.52, 5), (0.78, 0.68, 4), (0.68, 0.74, 3), (0.82, 0.50, 3)]:
        c.ellipse([x + cfx * w - cr, y + cfy * h - cr, x + cfx * w + cr,
                   y + cfy * h + cr], fill=(128, 118, 108))
    bx, by = x + int(w * 0.20), y + int(h * 0.36)
    c.rectangle([bx - 24, by - 4, bx - 2, by + 4], fill=(88, 118, 158))
    c.rectangle([bx + 2, by - 8, bx + 20, by + 8], fill=(198, 203, 208),
                outline=(118, 123, 128))
    c.rectangle([bx + 22, by - 4, bx + 38, by + 4], fill=(88, 118, 158))
    c.polygon([(bx + 38, by - 8), (bx + 50, by), (bx + 38, by + 8)], fill=(255, 158, 38))
    c.line([bx + 11, by - 13, bx + 11, by + 13], fill=(148, 153, 158), width=2)


def art_kenya(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + int(h * 0.52)], fill=(238, 178, 88))
    c.ellipse([x + int(w * 0.70), y + 8, x + int(w * 0.70) + 22, y + 30],
              fill=(255, 228, 148))
    c.rectangle([x, y + int(h * 0.52), x + w, y + h], fill=(194, 138, 68))
    c.rectangle([x, y + int(h * 0.76), x + w, y + h], fill=(138, 94, 46))
    dx = x + int(w * 0.40)
    c.polygon([(dx, y + int(h * 0.10)), (dx + 32, y + int(h * 0.76)),
               (dx + 10, y + int(h * 0.76)), (dx + 4, y + int(h * 0.28))],
              fill=(38, 32, 26))
    c.polygon([(dx + 6, y + int(h * 0.10)), (dx - 16, y + int(h * 0.76)),
               (dx + 2, y + int(h * 0.76)), (dx + 10, y + int(h * 0.28))],
              fill=(38, 32, 26))
    c.line([dx - 6, y + int(h * 0.10), dx + 24, y + int(h * 0.08)],
           fill=(38, 32, 26), width=4)
    c.ellipse([x + int(w * 0.76), y + int(h * 0.60), x + int(w * 0.76) + 15,
               y + int(h * 0.60) + 11], fill=(28, 28, 28))
    c.text((x + 6, y + h - 14), "20,000 bpd", font=typeface("sans-bold", 10),
           fill=PAL["white"])


def art_japan(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(248, 246, 238))
    c.ellipse([x + int(w * 0.72), y + 6, x + int(w * 0.72) + 24, y + 30],
              fill=(198, 38, 48))
    pts = [(0.07, 0.70), (0.26, 0.62), (0.44, 0.64), (0.62, 0.42),
           (0.80, 0.28), (0.93, 0.12)]
    for (fx, fy), (tx, ty) in zip(pts, pts[1:]):
        c.line([x + fx * w, y + fy * h, x + tx * w, y + ty * h],
               fill=PAL["red"], width=4)
    for fx, fy in pts:
        c.ellipse([x + fx * w - 3, y + fy * h - 3, x + fx * w + 3, y + fy * h + 3],
                  fill=PAL["red"])
    c.polygon([(x + int(w * 0.84), y + int(h * 0.06)), (x + int(w * 0.94), y + int(h * 0.12)),
               (x + int(w * 0.84), y + int(h * 0.18))], fill=PAL["red"])
    c.text((x + 6, y + h - 14), "CPI 2.3%", font=typeface("sans-bold", 11),
           fill=PAL["ink"])


def art_presser(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=(20, 40, 80))
    fx, fy, fw, fh = x + 8, y + 6, 42, 24
    for i in range(7):
        c.rectangle([fx, fy + i * fh // 7, fx + fw, fy + (i + 1) * fh // 7],
                    fill=(198, 38, 48) if i % 2 == 0 else PAL["white"])
    c.rectangle([fx, fy, fx + 17, fy + 13], fill=(28, 48, 108))
    for sx in (4, 10):
        for sy in (4, 9):
            c.ellipse([fx + sx - 1, fy + sy - 1, fx + sx + 1, fy + sy + 1],
                      fill=PAL["white"])
    px = x + int(w * 0.44)
    c.polygon([(px - 24, y + h - 8), (px + 24, y + h - 8),
               (px + 17, y + int(h * 0.50)), (px - 17, y + int(h * 0.50))],
              fill=(58, 58, 64))
    c.ellipse([px - 11, y + int(h * 0.56), px + 11, y + int(h * 0.56) + 19],
              fill=(238, 198, 88), outline=(148, 108, 18))
    c.line([px - 7, y + int(h * 0.50), px - 13, y + int(h * 0.28)],
           fill=(198, 198, 198), width=2)
    c.line([px + 7, y + int(h * 0.50), px + 13, y + int(h * 0.28)],
           fill=(198, 198, 198), width=2)
    c.ellipse([px - 15, y + int(h * 0.28) - 3, px - 11, y + int(h * 0.28) + 1],
              fill=(198, 198, 198))
    c.ellipse([px + 11, y + int(h * 0.28) - 3, px + 15, y + int(h * 0.28) + 1],
              fill=(198, 198, 198))
    c.text((x + w - 50, y + 6), "$17bn+", font=typeface("sans-bold", 10),
           fill=(255, 218, 88))


ART = {
    "kyiv": art_kyiv,
    "akvan": art_akvan,
    "rout": art_rout,
    "poland": art_poland,
    "ukeu": art_ukeu,
    "cop31": art_cop31,
    "italy": art_italy,
    "houthis": art_houthis,
    "gta": art_gta,
    "bepi": art_bepi,
    "kenya": art_kenya,
    "japan": art_japan,
    "presser": art_presser,
}


# A lead without its own art gets this neutral panel, never a crash.
def art_plain(c, x, y, w, h):
    """Neutral stand-in for a lead that has no illustration yet.

    A new lead must never crash the render; it gets this grey panel and
    the build note has to flag it, instead of a KeyError at build time.
    """
    c.rectangle([x, y, x + w, y + h], fill=(118, 116, 106))
    c.rectangle([x, y + h - 14, x + w, y + h], fill=PAL["ink"])
    c.text((x + 6, y + h - 12), "NEWS", font=typeface("sans-bold", 9),
           fill=PAL["white"])


# ---- page sections: masthead, lead cards, map, briefs, date check ----

def paint_masthead(c):
    c.text((EDGE, 8), TOP_STRIP_LEFT, font=typeface("sans-bold", 11),
           fill=PAL["red"])
    # Header counts come from the story data itself, so a re-check that
    # adds or drops a story can never leave a stale number on the page.
    tally = "%d STORIES \u00b7 %d REGIONS \u00b7 %d FIELDS" % (
        len(STORIES), len(REGIONS), len(FIELDS))
    c.text((PAGE - EDGE - c.textlength(tally, font=typeface("sans-bold", 11)), 8),
           tally, font=typeface("sans-bold", 11), fill=PAL["ink"])
    c.line([EDGE, 26, PAGE - EDGE, 26], fill=PAL["rule"], width=1)
    c.text((EDGE, 28), TITLE_DATE, font=typeface("serif-bold", 48), fill=PAL["ink"])
    c.text((EDGE, 80), MASTHEAD_DECK, font=typeface("serif-italic", 14),
           fill=PAL["muted"])
    top, bottom = 104, 146
    c.rectangle([EDGE, top, PAGE - EDGE, bottom], outline=PAL["rule"], width=1)
    cell = SPAN / len(NUMBERS)
    for i, (value, label) in enumerate(NUMBERS):
        cx = EDGE + i * cell
        if i:
            c.line([cx, top + 6, cx, bottom - 6], fill=PAL["rule"], width=1)
        c.text((cx + 9, top + 4), value, font=typeface("sans-bold", 19),
               fill=PAL["red"])
        draw_lines(c, (cx + 9, top + 25), label, typeface("sans", 9),
                   cell - 16, PAL["muted"], most=1)
    y = 152
    x = EDGE
    for label, n, colour in REGIONS:
        seg = "%s %d" % (label, n)
        wseg = c.textlength(seg, font=typeface("sans-bold", 10)) + 14
        c.rectangle([x, y, x + wseg, y + 14], fill=to_rgb(colour))
        c.text((x + 7, y + 2), seg, font=typeface("sans-bold", 10),
               fill=PAL["white"])
        x += wseg + 4
    y = 172
    c.text((EDGE, y), "FIELDS:", font=typeface("sans-bold", 10), fill=PAL["ink"])
    fx = EDGE + c.textlength("FIELDS: ", font=typeface("sans-bold", 10)) + 4
    parts = "  \u00b7  ".join("%s %d" % (name, n) for name, n in FIELDS)
    c.text((fx, y), parts, font=typeface("sans", 10), fill=PAL["ink"])


def paint_lead(c, story, x, y, w, h, big):
    c.rectangle([x, y, x + w, y + h], fill=PAL["card"], outline=PAL["rule"], width=1)
    art_h = 80 if big else 48
    painter = ART.get(story["art"], art_plain)
    painter(c, x + 1, y + 1, w - 2, art_h)
    ty = y + art_h + 5
    c.rectangle([x + 8, ty, x + 24, ty + 14], fill=PAL["red"])
    num = str(story["id"])
    c.text((x + 8 + (16 - c.textlength(num, font=typeface("sans-bold", 10))) / 2,
            ty + 1), num, font=typeface("sans-bold", 10), fill=PAL["white"])
    tag = "%s \u00b7 %s" % (story["place"], story["field"].upper())
    reserve = c.textlength(story["src"], font=typeface("sans", 8)) + 6 if big else 0
    tag = cap_text(c, tag, typeface("sans-bold", 9), w - 30 - reserve)
    c.text((x + 30, ty + 2), tag, font=typeface("sans-bold", 9),
           fill=tint_for(story["region"]))
    if big:
        src_w = c.textlength(story["src"], font=typeface("sans", 8))
        c.text((x + w - 8 - src_w, ty + 2), story["src"],
               font=typeface("sans", 8), fill=PAL["muted"])
    hy = ty + 18
    # A headline or deck that needs more lines than the card holds is a
    # build failure, not a silent trim: refuse instead of dropping words
    # off the page (v2 lost "warning", "estimate" and "Saturday" this way).
    head_face = typeface("serif-bold", 19 if big else 14)
    deck_face = typeface("sans", 11 if big else 9)
    deck_budget = 2 if big else 3
    if len(split_lines(c, story["headline"], head_face, w - 16)) > 2:
        raise SystemExit("lead %d headline needs >2 lines: %r"
                         % (story["id"], story["headline"]))
    if len(split_lines(c, story["deck"], deck_face, w - 16)) > deck_budget:
        raise SystemExit("lead %d deck needs >%d lines: %r"
                         % (story["id"], deck_budget, story["deck"]))
    if big:
        draw_lines(c, (x + 8, hy), story["headline"], typeface("serif-bold", 19),
                   w - 16, PAL["ink"], most=2, gap=22)
        draw_lines(c, (x + 8, hy + 46), story["deck"], typeface("sans", 11),
                   w - 16, PAL["muted"], most=2, gap=13)
    else:
        draw_lines(c, (x + 8, hy), story["headline"], typeface("serif-bold", 14),
                   w - 16, PAL["ink"], most=2, gap=16)
        draw_lines(c, (x + 8, hy + 34), story["deck"], typeface("sans", 9),
                   w - 16, PAL["muted"], most=3, gap=11)
        # Small cards carry their source bottom-right: the tag line is
        # already full (place + field), and the three-line deck ends
        # just above the card bottom, so this slot stays clear of it.
        src_w = c.textlength(story["src"], font=typeface("sans", 8))
        c.text((x + w - 8 - src_w, y + h - 13), story["src"],
               font=typeface("sans", 8), fill=PAL["muted"])


# Schematic continents, as fractions of the map panel. These outlines are
# the fix-v2 shapes: Europe widened so its five-pin cluster fits, Asia
# with an Arabia bulge so the Yemen/Saudi pin sits on land. The pin audit
# imports this exact table, so the renderer and the audit can never drift.
LAND = {
    "namerica": [(0.06, 0.30), (0.10, 0.20), (0.20, 0.18), (0.28, 0.24), (0.26, 0.34), (0.18, 0.40), (0.10, 0.38)],
    "samerica": [(0.22, 0.52), (0.28, 0.50), (0.32, 0.58), (0.28, 0.72), (0.23, 0.62)],
    "europe": [(0.40, 0.27), (0.44, 0.18), (0.54, 0.17), (0.60, 0.23), (0.60, 0.31), (0.57, 0.38), (0.49, 0.40), (0.41, 0.34)],
    "africa": [(0.47, 0.42), (0.55, 0.40), (0.59, 0.48), (0.56, 0.62), (0.50, 0.58), (0.47, 0.50)],
    "asia": [(0.57, 0.22), (0.72, 0.16), (0.88, 0.20), (0.92, 0.32), (0.84, 0.44), (0.74, 0.48), (0.63, 0.49), (0.585, 0.41), (0.58, 0.32)],
    "oceania": [(0.82, 0.62), (0.90, 0.60), (0.93, 0.68), (0.86, 0.72), (0.81, 0.68)],
}


def paint_map(c, x, y, w, h):
    c.rectangle([x, y, x + w, y + h], fill=PAL["map_bg"], outline=PAL["rule"], width=1)
    c.text((x + 8, y + 5), "WHERE IT HAPPENED", font=typeface("sans-bold", 11),
           fill=PAL["ink"])
    for poly in LAND.values():
        c.polygon([(x + px * w, y + py * h) for px, py in poly], fill=PAL["land"])
    c.text((x + 8, y + h - 16), "Pins mark the 13 lead stories.",
           font=typeface("sans", 9), fill=PAL["muted"])
    for sid, fx, fy in MAP_PINS:
        px, py = x + fx * w, y + fy * h
        c.ellipse([px - 7, py - 7, px + 7, py + 7], fill=PAL["red"],
                  outline=PAL["white"])
        label = str(sid)
        c.text((px - c.textlength(label, font=typeface("sans-bold", 9)) / 2, py - 5),
               label, font=typeface("sans-bold", 9), fill=PAL["white"])


def paint_briefs(c, x, y, w, h):
    briefs = [s for s in STORIES if s["id"] not in LEAD_IDS]
    c.text((x, y), "ALSO ON FRIDAY 20 NOVEMBER \u2014 %d MORE STORIES" % len(briefs),
           font=typeface("sans-bold", 11), fill=PAL["ink"])
    c.line([x, y + 16, x + w, y + 16], fill=PAL["rule"], width=1)
    cols = 3
    rows = -(-len(briefs) // cols)
    col_w = w // cols  # width of one brief column
    row_h = (h - 22) // rows
    for i, s in enumerate(briefs):
        row, col = divmod(i, cols)
        bx = x + col * col_w
        by = y + 22 + row * row_h
        c.rectangle([bx, by + 1, bx + 7, by + 8], fill=tint_for(s["region"]))
        c.text((bx + 11, by), "%d" % s["id"], font=typeface("sans-bold", 10),
               fill=PAL["red"])
        tx = bx + 11 + c.textlength("%d  " % s["id"], font=typeface("sans-bold", 10))
        head = cap_text(c, s["headline"], typeface("sans-bold", 9),
                        col_w - (tx - bx) - 4)
        if head != s["headline"]:
            raise SystemExit("brief %d headline truncates: %r"
                             % (s["id"], s["headline"]))
        c.text((tx, by), head, font=typeface("sans-bold", 9), fill=PAL["ink"])
        # The source tag gets its own reserved width, so it is never the
        # part of the deck that truncation eats.
        src_txt = " \u2014 " + s["src"]
        src_w = c.textlength(src_txt, font=typeface("sans", 8))
        deck = cap_text(c, s["deck"], typeface("sans", 8),
                        col_w - 12 - src_w - 4) + src_txt
        c.text((bx + 11, by + 10), deck, font=typeface("sans", 8), fill=PAL["muted"])


def paint_date_check(c, y):
    c.rectangle([EDGE, y, PAGE - EDGE, y + 60], fill=PAL["pink"],
                outline=PAL["red"], width=2)
    c.text((EDGE + 10, y + 6), "DATE CHECK \u2014 NOT 20 NOVEMBER",
           font=typeface("sans-bold", 12), fill=PAL["red"])
    draw_lines(c, (EDGE + 10, y + 24), DATE_CHECK, typeface("sans", 11),
               SPAN - 20, PAL["ink"], most=2, gap=14)


LEAD_CAP = 13
BRIEF_CAP = 27


def assemble(out_path):
    """Lay out the whole page. Refuses loudly when the story counts no
    longer fit this geometry, instead of silently dropping a story or
    letting a brief run into the DATE CHECK box."""
    leads = [s for s in STORIES if s["id"] in LEAD_IDS]
    briefs = [s for s in STORIES if s["id"] not in LEAD_IDS]
    if len(leads) > LEAD_CAP:
        raise SystemExit(
            "page holds max %d leads, got %d \u2014 re-layout before adding more"
            % (LEAD_CAP, len(leads)))
    if len(briefs) > BRIEF_CAP:
        raise SystemExit(
            "page holds max %d briefs, got %d \u2014 re-layout before adding more"
            % (BRIEF_CAP, len(briefs)))
    img = Image.new("RGB", (PAGE, PAGE), PAL["paper"])
    c = ImageDraw.Draw(img)
    paint_masthead(c)
    gap = 8
    big_w = (SPAN - 2 * gap) // 3
    xs3 = [EDGE, EDGE + big_w + gap, EDGE + 2 * (big_w + gap)]
    for i, s in enumerate(leads[:3]):
        paint_lead(c, s, xs3[i], 194, big_w, 184, big=True)
    small_w = (SPAN - 4 * gap) // 5
    xs5 = [EDGE + i * (small_w + gap) for i in range(5)]
    for i, s in enumerate(leads[3:8]):
        paint_lead(c, s, xs5[i], 386, small_w, 150, big=False)
    for i, s in enumerate(leads[8:13]):
        paint_lead(c, s, xs5[i], 544, small_w, 150, big=False)
    paint_map(c, EDGE, 702, 300, 184)
    paint_briefs(c, EDGE + 300 + 8, 702, SPAN - 300 - 8, 184)
    paint_date_check(c, 894)
    draw_lines(c, (EDGE, 962), FOOTER, typeface("sans", 9), SPAN,
               PAL["muted"], most=2, gap=11)
    img.save(out_path, "PNG", optimize=True)
    saved = out_path
    return saved

# Entry point: optional output path, else entry.png beside this file.
if __name__ == "__main__":
    dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    assemble(dest)
    print("wrote %s (%d bytes)" % (dest, os.path.getsize(dest)))
