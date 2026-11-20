# compose.py — news-image-20261120 v2 renderer (fresh, written in-session).
# Python 3 stdlib + Pillow 10.2.0 only. No network. Deterministic output:
# fixed layout, fixed fonts, no timestamps, no randomness.
# Usage: python3 compose.py [output-path]   (default: entry.png next to this file)
import os
import sys

from PIL import Image, ImageDraw, ImageFont

from stories import (
    DATE_CHECK, FIELDS, FOOTER, LEAD_IDS, MAP_PINS, MASTHEAD_DECK,
    NUMBERS, REGIONS, STORIES, TITLE_DATE, TOP_STRIP_LEFT,
)

W = H = 1024
M = 14                      # outer margin; every block aligns to M / W-M
CW = W - 2 * M              # 996 content width

PAPER = (247, 241, 227)
CARD = (255, 253, 246)
INK = (26, 26, 26)
MUTED = (90, 84, 70)
RULE = (201, 191, 168)
RED = (176, 30, 36)
NAVY = (22, 50, 74)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SERIF_I = lambda s: font("DejaVuSerif-Italic.ttf", s) \
    if os.path.exists(os.path.join(FONT_DIR, "DejaVuSerif-Italic.ttf")) \
    else font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap by pixel width; returns a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(draw, xy, text, fnt, max_w, fill, max_lines=None, lh=None):
    """Draw wrapped text; returns the y just below the last line drawn."""
    x, y = xy
    lh = lh or int(fnt.size * 1.18)
    lines = wrap(draw, text, fnt, max_w)
    if max_lines is not None:
        lines = lines[:max_lines]
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def truncate(draw, text, fnt, max_w):
    """Shorten text with an ellipsis so it fits max_w pixels."""
    if draw.textlength(text, font=fnt) <= max_w:
        return text
    ell = "\u2026"
    while text and draw.textlength(text + ell, font=fnt) > max_w:
        text = text[:-1]
    return text + ell


def region_color(name):
    for label, _n, color in REGIONS:
        if label.lower() == name.lower():
            return color
    return "#555555"


def hex2rgb(h):
    h = h.lstrip("#")
    return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16))


# ---- flat-vector illustrations (all our own PIL drawing) ----

def ill_kyiv(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(15, 30, 52))
    for sx, sy in [(0.10, 0.20), (0.28, 0.10), (0.52, 0.24), (0.76, 0.10), (0.92, 0.28)]:
        d.ellipse([x + sx * w - 2, y + sy * h - 2, x + sx * w + 2, y + sy * h + 2],
                  fill=(255, 240, 180))
    d.rectangle([x, y + int(h * 0.70), x + w, y + h], fill=(36, 72, 108))
    for bx in (0.06, 0.50):
        d.arc([x + bx * w, y + int(h * 0.40), x + (bx + 0.42) * w, y + int(h * 0.95)],
              180, 360, fill=(222, 222, 212), width=4)
        d.line([x + bx * w, y + int(h * 0.66), x + (bx + 0.42) * w, y + int(h * 0.66)],
               fill=(222, 222, 212), width=3)
    d.line([x + int(w * 0.60), y + int(h * 0.10), x + int(w * 0.40), y + int(h * 0.48)],
           fill=(255, 200, 80), width=3)
    d.line([x + int(w * 0.86), y + int(h * 0.04), x + int(w * 0.70), y + int(h * 0.36)],
           fill=(255, 200, 80), width=3)
    for fx, fy, r in [(0.16, 0.60, 9), (0.23, 0.56, 6), (0.12, 0.64, 5)]:
        d.ellipse([x + fx * w - r, y + fy * h - r, x + fx * w + r, y + fy * h + r],
                  fill=(255, 120, 20))
        d.ellipse([x + fx * w - r // 2, y + fy * h - r // 2,
                   x + fx * w + r // 2, y + fy * h + r // 2], fill=(255, 220, 90))


def ill_akvan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + int(h * 0.45)], fill=(180, 212, 230))
    d.rectangle([x, y + int(h * 0.45), x + w, y + h], fill=(42, 106, 148))
    d.polygon([(x + int(w * 0.60), y), (x + w, y), (x + w, y + h),
               (x + int(w * 0.54), y + h), (x + int(w * 0.64), y + int(h * 0.50))],
              fill=(212, 194, 148))
    cx, cy = x + int(w * 0.36), y + int(h * 0.42)
    for r, a0, a1 in [(32, 20, 300), (23, 120, 380), (14, 200, 460), (6, 0, 360)]:
        d.arc([cx - r, cy - r, cx + r, cy + r], a0, a1, fill=(255, 255, 255), width=4)
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255))
    for rx in (0.06, 0.20, 0.52, 0.68, 0.84):
        d.line([x + rx * w, y + int(h * 0.08), x + (rx - 0.03) * w, y + int(h * 0.30)],
               fill=(118, 158, 188), width=2)
    d.text((x + 6, y + h - 14), "07:30 IST", font=SANS_B(10), fill=(255, 255, 255))


def ill_rout(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(17, 27, 39))
    for gy in (0.25, 0.5, 0.75):
        d.line([x, y + gy * h, x + w, y + gy * h], fill=(46, 62, 82), width=1)
    pts = [(0.04, 0.16), (0.22, 0.28), (0.38, 0.24), (0.55, 0.46),
           (0.72, 0.60), (0.88, 0.80), (0.97, 0.76)]
    for (fx, fy), (tx, ty) in zip(pts, pts[1:]):
        d.line([x + fx * w, y + fy * h, x + tx * w, y + ty * h],
               fill=(230, 60, 50), width=4)
    for fx, fy in pts:
        d.ellipse([x + fx * w - 3, y + fy * h - 3, x + fx * w + 3, y + fy * h + 3],
                  fill=(255, 120, 100))
    d.polygon([(x + int(w * 0.90), y + int(h * 0.70)), (x + int(w * 0.97), y + int(h * 0.70)),
               (x + int(w * 0.935), y + int(h * 0.80))], fill=(230, 60, 50))
    d.text((x + 6, y + h - 14), "NIKKEI -5.1%  KOSPI -5.2%  TAIEX -6.2%",
           font=SANS_B(9), fill=(255, 255, 255))


def ill_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(166, 194, 212))
    d.rectangle([x, y, x + int(w * 0.32), y + int(h * 0.13)], fill=(255, 255, 255))
    d.rectangle([x, y + int(h * 0.13), x + int(w * 0.32), y + int(h * 0.26)],
                fill=(200, 40, 50))
    d.rectangle([x, y + int(h * 0.60), x + w, y + h], fill=(94, 138, 78))
    d.polygon([(x, y + h), (x + w, y + int(h * 0.76)), (x + w, y + h)],
              fill=(118, 118, 108))
    mx, my = x + int(w * 0.40), y + int(h * 0.28)
    d.polygon([(mx, my), (mx + 50, my + 25), (mx + 42, my + 35), (mx - 6, my + 11)],
              fill=(88, 93, 98))
    d.polygon([(mx + 38, my + 21), (mx + 56, my + 17), (mx + 50, my + 31)],
              fill=(68, 73, 78))
    ix, iy = x + int(w * 0.70), y + int(h * 0.70)
    for r, col in [(15, (255, 160, 40)), (8, (255, 220, 90))]:
        d.ellipse([ix - r, iy - r, ix + r, iy + r], fill=col)
    d.line([ix - 20, iy - 24, ix, iy], fill=(118, 118, 118), width=2)


def ill_ukeu(d, x, y, w, h):
    # left: Union Jack (simplified); right: EU blue with a ring of stars
    mid = x + w // 2
    d.rectangle([x, y, mid, y + h], fill=(20, 40, 90))
    d.line([x, y, mid, y + h], fill=(255, 255, 255), width=5)
    d.line([mid, y, x, y + h], fill=(255, 255, 255), width=5)
    d.line([x + w // 4, y, x + w // 4, y + h], fill=(255, 255, 255), width=9)
    d.line([x, y + h // 2, mid, y + h // 2], fill=(255, 255, 255), width=9)
    d.line([x + w // 4, y, x + w // 4, y + h], fill=(200, 40, 50), width=5)
    d.line([x, y + h // 2, mid, y + h // 2], fill=(200, 40, 50), width=5)
    d.rectangle([mid, y, x + w, y + h], fill=(0, 51, 153))
    import math
    ccx, ccy, cr = mid + w // 4, y + h // 2, int(h * 0.30)
    for k in range(12):
        ang = 2 * math.pi * k / 12 - math.pi / 2
        sx, sy = ccx + cr * math.cos(ang), ccy + cr * math.sin(ang)
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 210, 0))
    d.rectangle([x, y + h - 16, x + w, y + h], fill=(255, 210, 0))
    d.text((x + 6, y + h - 14), "RESET DEAL", font=SANS_B(10), fill=(26, 26, 26))


def ill_cop31(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(14, 74, 78))
    cx, cy, r = x + int(w * 0.38), y + int(h * 0.52), int(h * 0.34)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 130, 180))
    d.ellipse([cx - int(r * 0.55), cy - int(r * 0.5), cx - int(r * 0.05),
               cy + int(r * 0.15)], fill=(90, 170, 100))
    d.ellipse([cx + int(r * 0.1), cy + int(r * 0.2), cx + int(r * 0.6),
               cy + int(r * 0.6)], fill=(90, 170, 100))
    d.arc([cx - r, cy - r, cx + r, cy + r], 0, 360, fill=(255, 255, 255), width=2)
    # clock = overtime
    kx, ky, kr = x + int(w * 0.80), y + int(h * 0.26), 14
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(255, 253, 246),
              outline=(26, 26, 26))
    d.line([kx, ky, kx, ky - kr + 3], fill=(26, 26, 26), width=2)
    d.line([kx, ky, kx + kr - 5, ky + 3], fill=(26, 26, 26), width=2)
    d.text((x + 6, y + h - 14), "OVERTIME", font=SANS_B(10), fill=(255, 255, 255))
    d.text((x + w - 84, y + h - 14), "NO DEAL YET",
           font=SANS_B(10), fill=(255, 220, 90))


def ill_italy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 198))
    for i, col in enumerate([(0, 140, 70), (255, 255, 255), (200, 40, 50)]):
        d.polygon([(x + i * w // 3, y), (x + (i + 1) * w // 3, y),
                   (x + (i + 1) * w // 3 - 14, y + 15), (x + i * w // 3 + 14, y + 15)],
                  fill=col)
    for i, hx in enumerate((0.10, 0.28, 0.46, 0.64, 0.82)):
        hy = 0.50 + (0.06 if i % 2 else 0.0)
        d.ellipse([x + hx * w - 9, y + hy * h - 9, x + hx * w + 9, y + hy * h + 9],
                  fill=(58, 48, 42))
        d.pieslice([x + hx * w - 14, y + hy * h + 6, x + hx * w + 14, y + h + 10],
                   180, 360, fill=(50, 82, 138) if i % 2 else (148, 58, 58))
    for px, py, col in [(0.18, 0.28, (255, 255, 255)), (0.56, 0.24, (255, 228, 118)),
                        (0.80, 0.32, (255, 255, 255))]:
        d.line([x + px * w, y + py * h + 18, x + px * w, y + int(h * 0.52)],
               fill=(88, 78, 68), width=2)
        d.rectangle([x + px * w - 19, y + py * h, x + px * w + 19, y + py * h + 18],
                    fill=col, outline=(118, 108, 93))


def ill_houthis(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + int(h * 0.55)], fill=(204, 222, 230))
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(34, 88, 120))
    for cx in (0.12, 0.36):
        d.line([x + cx * w, y + int(h * 0.12), x + cx * w, y + int(h * 0.58)],
               fill=(68, 78, 88), width=4)
        d.line([x + cx * w, y + int(h * 0.14), x + (cx + 0.22) * w, y + int(h * 0.30)],
               fill=(68, 78, 88), width=3)
    d.polygon([(x + int(w * 0.50), y + int(h * 0.60)), (x + int(w * 0.93), y + int(h * 0.60)),
               (x + int(w * 0.88), y + int(h * 0.78)), (x + int(w * 0.56), y + int(h * 0.78))],
              fill=(38, 43, 53))
    for i, col in enumerate([(198, 58, 48), (38, 118, 88), (218, 158, 38)]):
        d.rectangle([x + int(w * (0.56 + i * 0.11)), y + int(h * 0.44),
                     x + int(w * (0.65 + i * 0.11)), y + int(h * 0.58)], fill=col)
    tx, ty = x + int(w * 0.76), y + int(h * 0.08)
    d.polygon([(tx, ty), (tx + 32, ty + 28), (tx - 32, ty + 28)], fill=(238, 188, 28),
              outline=(148, 98, 0))
    d.text((tx - 3, ty + 6), "!", font=SANS_B(19), fill=(26, 26, 26))


def ill_gta(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + int(h * 0.55)], fill=(58, 32, 84))
    d.ellipse([x + int(w * 0.76), y + 6, x + int(w * 0.76) + 26, y + 32],
              fill=(255, 190, 90))
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(30, 18, 48))
    for bx, bw, bh in [(0.04, 0.14, 0.30), (0.20, 0.10, 0.44), (0.32, 0.16, 0.24),
                       (0.50, 0.12, 0.38), (0.64, 0.14, 0.28), (0.80, 0.12, 0.46)]:
        d.rectangle([x + bx * w, y + int(h * (0.62 - bh)), x + (bx + bw) * w,
                     y + int(h * 0.62)], fill=(20, 12, 34))
        for wy in (0.10, 0.22):
            d.rectangle([x + (bx + 0.02) * w, y + int(h * (0.62 - bh + wy)),
                         x + (bx + bw - 0.02) * w, y + int(h * (0.62 - bh + wy + 0.04))],
                        fill=(255, 210, 110))
    d.text((x + 6, y + h - 14), "EST. $2.36bn", font=SANS_B(10), fill=(255, 255, 255))


def ill_bepi(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(8, 10, 24))
    for sx, sy in [(0.08, 0.16), (0.22, 0.08), (0.55, 0.12), (0.78, 0.22), (0.92, 0.08),
                   (0.36, 0.26), (0.66, 0.06)]:
        d.ellipse([x + sx * w - 1, y + sy * h - 1, x + sx * w + 1, y + sy * h + 1],
                  fill=(255, 255, 255))
    mx, my, mr = x + int(w * 0.72), y + int(h * 0.60), int(h * 0.30)
    d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(168, 158, 148))
    for cfx, cfy, cr in [(0.62, 0.50, 5), (0.80, 0.66, 4), (0.70, 0.72, 3), (0.84, 0.48, 3)]:
        d.ellipse([x + cfx * w - cr, y + cfy * h - cr, x + cfx * w + cr,
                   y + cfy * h + cr], fill=(130, 120, 110))
    # spacecraft: body + panels + thruster flame
    bx, by = x + int(w * 0.22), y + int(h * 0.34)
    d.rectangle([bx - 26, by - 4, bx - 2, by + 4], fill=(90, 120, 160))
    d.rectangle([bx + 2, by - 8, bx + 22, by + 8], fill=(200, 205, 210),
                outline=(120, 125, 130))
    d.rectangle([bx + 24, by - 4, bx + 40, by + 4], fill=(90, 120, 160))
    d.polygon([(bx + 40, by - 8), (bx + 52, by), (bx + 40, by + 8)], fill=(255, 160, 40))
    d.line([bx + 12, by - 14, bx + 12, by + 14], fill=(150, 155, 160), width=2)


def ill_kenya(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + int(h * 0.55)], fill=(240, 180, 90))
    d.ellipse([x + int(w * 0.72), y + 8, x + int(w * 0.72) + 24, y + 32],
              fill=(255, 230, 150))
    d.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=(196, 140, 70))
    d.rectangle([x, y + int(h * 0.78), x + w, y + h], fill=(140, 96, 48))
    # oil derrick silhouette
    dx = x + int(w * 0.42)
    d.polygon([(dx, y + int(h * 0.12)), (dx + 34, y + int(h * 0.78)),
               (dx + 10, y + int(h * 0.78)), (dx + 4, y + int(h * 0.30))],
              fill=(40, 34, 28))
    d.polygon([(dx + 6, y + int(h * 0.12)), (dx - 18, y + int(h * 0.78)),
               (dx + 2, y + int(h * 0.78)), (dx + 10, y + int(h * 0.30))],
              fill=(40, 34, 28))
    d.line([dx - 6, y + int(h * 0.12), dx + 26, y + int(h * 0.10)],
           fill=(40, 34, 28), width=4)
    d.ellipse([x + int(w * 0.78), y + int(h * 0.62), x + int(w * 0.78) + 16,
               y + int(h * 0.62) + 12], fill=(30, 30, 30))
    d.text((x + 6, y + h - 14), "20,000 bpd", font=SANS_B(10), fill=(255, 255, 255))


def ill_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 248, 240))
    d.ellipse([x + int(w * 0.74), y + 6, x + int(w * 0.74) + 26, y + 32],
              fill=(200, 40, 50))
    pts = [(0.08, 0.72), (0.28, 0.64), (0.46, 0.66), (0.64, 0.44),
           (0.82, 0.30), (0.94, 0.14)]
    for (fx, fy), (tx, ty) in zip(pts, pts[1:]):
        d.line([x + fx * w, y + fy * h, x + tx * w, y + ty * h],
               fill=(176, 30, 36), width=4)
    for fx, fy in pts:
        d.ellipse([x + fx * w - 3, y + fy * h - 3, x + fx * w + 3, y + fy * h + 3],
                  fill=(176, 30, 36))
    d.polygon([(x + int(w * 0.86), y + int(h * 0.08)), (x + int(w * 0.96), y + int(h * 0.14)),
               (x + int(w * 0.86), y + int(h * 0.20))], fill=(176, 30, 36))
    d.text((x + 6, y + h - 14), "CPI 2.3%", font=SANS_B(11), fill=(26, 26, 26))


def ill_india(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(230, 240, 226))
    d.ellipse([x + int(w * 0.76), y + 8, x + int(w * 0.76) + 24, y + 32],
              fill=(238, 188, 88))
    for i, bh in enumerate((0.16, 0.26, 0.20, 0.34)):
        d.rectangle([x + int(w * (0.08 + i * 0.14)), y + h - int(bh * h) - 6,
                     x + int(w * (0.18 + i * 0.14)), y + h - 6],
                    fill=(118, 178, 138))
    pts = [(0.06, 0.76), (0.26, 0.64), (0.44, 0.68), (0.62, 0.46),
           (0.80, 0.32), (0.95, 0.14)]
    for (fx, fy), (tx, ty) in zip(pts, pts[1:]):
        d.line([x + fx * w, y + fy * h, x + tx * w, y + ty * h],
               fill=(28, 128, 68), width=4)
    for fx, fy in pts:
        d.ellipse([x + fx * w - 3, y + fy * h - 3, x + fx * w + 3, y + fy * h + 3],
                  fill=(28, 128, 68))
    d.polygon([(x + int(w * 0.87), y + int(h * 0.08)), (x + int(w * 0.96), y + int(h * 0.14)),
               (x + int(w * 0.87), y + int(h * 0.20))], fill=(28, 128, 68))


def ill_presser(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(22, 42, 82))
    # US flag, simplified, top-left
    fx, fy, fw, fh = x + 8, y + 6, 44, 26
    for i in range(7):
        d.rectangle([fx, fy + i * fh // 7, fx + fw, fy + (i + 1) * fh // 7],
                    fill=(200, 40, 50) if i % 2 == 0 else (255, 255, 255))
    d.rectangle([fx, fy, fx + 18, fy + 14], fill=(30, 50, 110))
    for sx in (4, 11):
        for sy in (4, 10):
            d.ellipse([fx + sx - 1, fy + sy - 1, fx + sx + 1, fy + sy + 1],
                      fill=(255, 255, 255))
    # podium + microphones + seal
    px = x + int(w * 0.42)
    d.polygon([(px - 26, y + h - 8), (px + 26, y + h - 8),
               (px + 18, y + int(h * 0.52)), (px - 18, y + int(h * 0.52))],
              fill=(60, 60, 66))
    d.ellipse([px - 12, y + int(h * 0.58), px + 12, y + int(h * 0.58) + 20],
              fill=(240, 200, 90), outline=(150, 110, 20))
    d.line([px - 8, y + int(h * 0.52), px - 14, y + int(h * 0.30)],
           fill=(200, 200, 200), width=2)
    d.line([px + 8, y + int(h * 0.52), px + 14, y + int(h * 0.30)],
           fill=(200, 200, 200), width=2)
    d.ellipse([px - 16, y + int(h * 0.30) - 3, px - 12, y + int(h * 0.30) + 1],
              fill=(200, 200, 200))
    d.ellipse([px + 12, y + int(h * 0.30) - 3, px + 16, y + int(h * 0.30) + 1],
              fill=(200, 200, 200))
    d.text((x + w - 52, y + 6), "$17bn+", font=SANS_B(10), fill=(255, 220, 90))


ILLUSTRATIONS = {
    "kyiv": ill_kyiv, "akvan": ill_akvan, "rout": ill_rout,
    "poland": ill_poland, "ukeu": ill_ukeu, "cop31": ill_cop31,
    "italy": ill_italy, "houthis": ill_houthis, "gta": ill_gta,
    "bepi": ill_bepi, "kenya": ill_kenya, "japan": ill_japan,
    "india": ill_india, "presser": ill_presser,
}


# ---- page sections ----

def draw_header(d):
    d.text((M, 8), TOP_STRIP_LEFT, font=SANS_B(11), fill=RED)
    # Counts are computed from the story data, never hardcoded (risk-team
    # note: a hardcoded count goes stale the moment the 04:30 re-check
    # adds or drops a story).
    right = "%d STORIES \u00b7 %d REGIONS \u00b7 %d FIELDS" % (
        len(STORIES), len(REGIONS), len(FIELDS))
    d.text((W - M - d.textlength(right, font=SANS_B(11)), 8), right,
           font=SANS_B(11), fill=INK)
    d.line([M, 26, W - M, 26], fill=RULE, width=1)
    d.text((M, 28), TITLE_DATE, font=SERIF_B(48), fill=INK)
    d.text((M, 80), MASTHEAD_DECK, font=SERIF_I(14), fill=MUTED)
    y0, y1 = 104, 146
    d.rectangle([M, y0, W - M, y1], outline=RULE, width=1)
    cell_w = CW / len(NUMBERS)
    for i, (val, label) in enumerate(NUMBERS):
        cx = M + i * cell_w
        if i:
            d.line([cx, y0 + 6, cx, y1 - 6], fill=RULE, width=1)
        d.text((cx + 9, y0 + 4), val, font=SANS_B(19), fill=RED)
        draw_wrapped(d, (cx + 9, y0 + 25), label, SANS(9), cell_w - 16,
                     MUTED, max_lines=1)
    y = 152
    x = M
    for label, n, color in REGIONS:
        seg = "%s %d" % (label, n)
        wseg = d.textlength(seg, font=SANS_B(10)) + 14
        d.rectangle([x, y, x + wseg, y + 14], fill=hex2rgb(color))
        d.text((x + 7, y + 2), seg, font=SANS_B(10), fill=(255, 255, 255))
        x += wseg + 4
    y = 172
    d.text((M, y), "FIELDS:", font=SANS_B(10), fill=INK)
    fx = M + d.textlength("FIELDS: ", font=SANS_B(10)) + 4
    parts = "  \u00b7  ".join("%s %d" % (name, n) for name, n in FIELDS)
    d.text((fx, y), parts, font=SANS(10), fill=INK)


def ill_fallback(d, x, y, w, h):
    # Generic panel for a lead whose own illustration does not exist yet.
    # The renderer must never crash on a new lead (risk-team note) — it
    # falls back to this neutral panel and the build note flags it.
    d.rectangle([x, y, x + w, y + h], fill=(120, 118, 108))
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(26, 26, 26))
    d.text((x + 6, y + h - 12), "NEWS", font=SANS_B(9), fill=(255, 255, 255))


def draw_card(d, story, x, y, w, h, big):
    d.rectangle([x, y, x + w, y + h], fill=CARD, outline=RULE, width=1)
    art_h = 80 if big else 48
    art_fn = ILLUSTRATIONS.get(story["art"], ill_fallback)
    art_fn(d, x + 1, y + 1, w - 2, art_h)
    ty = y + art_h + 5
    d.rectangle([x + 8, ty, x + 24, ty + 14], fill=RED)
    d.text((x + 8 + (16 - d.textlength(str(story["id"]), font=SANS_B(10))) / 2,
            ty + 1), str(story["id"]), font=SANS_B(10), fill=(255, 255, 255))
    tag = "%s \u00b7 %s" % (story["place"], story["field"].upper())
    tag = truncate(d, tag, SANS_B(9), w - 30 - (d.textlength(story["src"], font=SANS(8)) + 6 if big else 0))
    d.text((x + 30, ty + 2), tag, font=SANS_B(9), fill=hex2rgb(region_color(story["region"])))
    if big:
        src_w = d.textlength(story["src"], font=SANS(8))
        d.text((x + w - 8 - src_w, ty + 2), story["src"], font=SANS(8), fill=MUTED)
    hy = ty + 18
    if big:
        draw_wrapped(d, (x + 8, hy), story["headline"], SERIF_B(18), w - 16,
                     INK, max_lines=2, lh=21)
        draw_wrapped(d, (x + 8, hy + 44), story["deck"], SANS(11), w - 16,
                     MUTED, max_lines=2, lh=13)
    else:
        draw_wrapped(d, (x + 8, hy), story["headline"], SERIF_B(14), w - 16,
                     INK, max_lines=2, lh=16)
        draw_wrapped(d, (x + 8, hy + 34), story["deck"], SANS(9), w - 16,
                     MUTED, max_lines=3, lh=11)
        # Fix-v2 (LOW-1): small cards carry a source tag too. It goes
        # bottom-right, not in the tag line — the tag line has no room
        # for it (place.field already fills it) and the 3-line deck
        # ends ~14px above the card bottom, so this cannot overlap it.
        src_w = d.textlength(story["src"], font=SANS(8))
        d.text((x + w - 8 - src_w, y + h - 13), story["src"],
               font=SANS(8), fill=MUTED)


# World-map land polygons, in 0..1 fractions of the map panel.
# Fix-v2 (21 Nov): the Europe blob is drawn larger than in the first v2
# render (x 0.40-0.60, y 0.17-0.40 instead of a 0.46-0.56 sliver) so the
# five-pin Europe cluster (London/Brussels, Poland, Kyiv, Italy, ESA)
# fits on land with pin centres >=15px apart; the Asia polygon gains an
# Arabia bulge (0.585-0.63, 0.41-0.49) so the Yemen/Saudi pin sits on
# land instead of in the sea between Africa and Asia. Kept module-level
# so the pin audit can import the same polygons the renderer draws.
LAND_POLYS = [
    # North America
    [(0.06, 0.30), (0.10, 0.20), (0.20, 0.18), (0.28, 0.24), (0.26, 0.34),
     (0.18, 0.40), (0.10, 0.38)],
    # South America
    [(0.22, 0.52), (0.28, 0.50), (0.32, 0.58), (0.28, 0.72), (0.23, 0.62)],
    # Europe (enlarged, fix-v2)
    [(0.40, 0.27), (0.44, 0.18), (0.54, 0.17), (0.60, 0.23),
     (0.60, 0.31), (0.57, 0.38), (0.49, 0.40), (0.41, 0.34)],
    # Africa
    [(0.47, 0.42), (0.55, 0.40), (0.59, 0.48), (0.56, 0.62), (0.50, 0.58),
     (0.47, 0.50)],
    # Asia (Arabia bulge, fix-v2)
    [(0.57, 0.22), (0.72, 0.16), (0.88, 0.20), (0.92, 0.32), (0.84, 0.44),
     (0.74, 0.48), (0.63, 0.49), (0.585, 0.41), (0.58, 0.32)],
    # Oceania
    [(0.82, 0.62), (0.90, 0.60), (0.93, 0.68), (0.86, 0.72), (0.81, 0.68)],
]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(237, 230, 210), outline=RULE, width=1)
    d.text((x + 8, y + 5), "WHERE IT HAPPENED", font=SANS_B(11), fill=INK)
    land = (203, 185, 143)
    for poly in LAND_POLYS:
        d.polygon([(x + px * w, y + py * h) for px, py in poly], fill=land)
    d.text((x + 8, y + h - 16), "Pins mark the 13 lead stories.",
           font=SANS(9), fill=MUTED)
    for sid, fx, fy in MAP_PINS:
        px, py = x + fx * w, y + fy * h
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255))
        label = str(sid)
        d.text((px - d.textlength(label, font=SANS_B(9)) / 2, py - 5), label,
               font=SANS_B(9), fill=(255, 255, 255))


def draw_also_on(d, x, y, w, h):
    briefs = [s for s in STORIES if s["id"] not in LEAD_IDS]
    d.text((x, y), "ALSO ON FRIDAY 20 NOVEMBER \u2014 %d MORE STORIES" % len(briefs),
           font=SANS_B(11), fill=INK)
    d.line([x, y + 16, x + w, y + 16], fill=RULE, width=1)
    cols = 3
    rows = (len(briefs) + cols - 1) // cols
    col_w = w // cols
    row_h = (h - 22) // rows
    for i, s in enumerate(briefs):
        col, row = i % cols, i // cols
        bx = x + col * col_w
        by = y + 22 + row * row_h
        d.rectangle([bx, by + 1, bx + 7, by + 8],
                    fill=hex2rgb(region_color(s["region"])))
        d.text((bx + 11, by), "%d" % s["id"], font=SANS_B(10), fill=RED)
        tx = bx + 11 + d.textlength("%d  " % s["id"], font=SANS_B(10))
        head = truncate(d, s["headline"], SANS_B(9), col_w - (tx - bx) - 4)
        d.text((tx, by), head, font=SANS_B(9), fill=INK)
        # Reserve room for the source tag so it always survives truncation.
        src_txt = " \u2014 " + s["src"]
        src_w = d.textlength(src_txt, font=SANS(8))
        deck = truncate(d, s["deck"], SANS(8), col_w - 12 - src_w - 4) + src_txt
        d.text((bx + 11, by + 10), deck, font=SANS(8), fill=MUTED)


def draw_date_check(d, y):
    d.rectangle([M, y, W - M, y + 60], fill=(255, 238, 238), outline=RED, width=2)
    d.text((M + 10, y + 6), "DATE CHECK \u2014 NOT 20 NOVEMBER",
           font=SANS_B(12), fill=RED)
    draw_wrapped(d, (M + 10, y + 24), DATE_CHECK, SANS(11), CW - 20,
                 INK, max_lines=2, lh=14)


def build(out_path):
    # Hard layout limits — fail LOUDLY instead of silently dropping a lead
    # or letting a brief overflow into the DATE CHECK box (risk-team note:
    # v1's fixed 2x4 grid would have put brief 9 inside the DATE CHECK box,
    # and its [:3]/[3:6]/[6:9] slices would have dropped a 10th lead).
    # This layout holds 3 big + 10 small leads and 24 briefs (3 cols x 8).
    leads = [s for s in STORIES if s["id"] in LEAD_IDS]
    briefs = [s for s in STORIES if s["id"] not in LEAD_IDS]
    if len(leads) > 13:
        raise SystemExit(
            "layout holds max 13 leads, got %d — re-layout before adding more"
            % len(leads))
    if len(briefs) > 24:
        raise SystemExit(
            "layout holds max 24 briefs, got %d — re-layout before adding more"
            % len(briefs))
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_header(d)
    gap = 8
    big_w = (CW - 2 * gap) // 3
    xs3 = [M, M + big_w + gap, M + 2 * (big_w + gap)]
    for i, s in enumerate(leads[:3]):
        draw_card(d, s, xs3[i], 194, big_w, 184, big=True)
    small_w = (CW - 4 * gap) // 5
    xs5 = [M + i * (small_w + gap) for i in range(5)]
    for i, s in enumerate(leads[3:8]):
        draw_card(d, s, xs5[i], 386, small_w, 150, big=False)
    for i, s in enumerate(leads[8:13]):
        draw_card(d, s, xs5[i], 544, small_w, 150, big=False)
    draw_map(d, M, 702, 300, 184)
    draw_also_on(d, M + 300 + 8, 702, CW - 300 - 8, 184)
    draw_date_check(d, 894)
    draw_wrapped(d, (M, 962), FOOTER, SANS(9), CW, MUTED, max_lines=2, lh=11)
    img.save(out_path, format="PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build(target)
    print("wrote %s (%d bytes)" % (target, os.path.getsize(target)))
