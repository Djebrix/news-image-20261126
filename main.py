#!/usr/bin/env python3
"""THE WORLD IN ONE DAY - front page for Thursday 26 November 2026.

Draws a newspaper front page (1024x1024 PNG) summing up the day's world
news. Pure standard library: own 5x7 bitmap font, own PNG encoder,
deterministic output - no network, no clock, no randomness.
"""
import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (247, 242, 228)
INK = (17, 17, 17)
RED = (176, 32, 32)
BLUE = (31, 78, 121)
ORANGE = (208, 96, 0)
GOLD = (180, 138, 20)
GREEN = (46, 107, 52)
GREY = (120, 116, 104)
LIGHT = (232, 226, 210)
SKY = (196, 222, 240)
SEA = (46, 110, 150)

# ---------------------------------------------------------------- 5x7 font
# Each glyph: 7 rows of 5 bits, written as strings of 0/1.
FONT = {
    "A": ("01110", "10001", "10001", "11111", "10001", "10001", "10001"),
    "B": ("11110", "10001", "10001", "11110", "10001", "10001", "11110"),
    "C": ("01110", "10001", "10000", "10000", "10000", "10001", "01110"),
    "D": ("11110", "10001", "10001", "10001", "10001", "10001", "11110"),
    "E": ("11111", "10000", "10000", "11110", "10000", "10000", "11111"),
    "F": ("11111", "10000", "10000", "11110", "10000", "10000", "10000"),
    "G": ("01110", "10001", "10000", "10111", "10001", "10001", "01111"),
    "H": ("10001", "10001", "10001", "11111", "10001", "10001", "10001"),
    "I": ("01110", "00100", "00100", "00100", "00100", "00100", "01110"),
    "J": ("00111", "00010", "00010", "00010", "00010", "10010", "01100"),
    "K": ("10001", "10010", "10100", "11000", "10100", "10010", "10001"),
    "L": ("10000", "10000", "10000", "10000", "10000", "10000", "11111"),
    "M": ("10001", "11011", "10101", "10101", "10001", "10001", "10001"),
    "N": ("10001", "11001", "10101", "10011", "10001", "10001", "10001"),
    "O": ("01110", "10001", "10001", "10001", "10001", "10001", "01110"),
    "P": ("11110", "10001", "10001", "11110", "10000", "10000", "10000"),
    "Q": ("01110", "10001", "10001", "10001", "10101", "10010", "01101"),
    "R": ("11110", "10001", "10001", "11110", "10100", "10010", "10001"),
    "S": ("01111", "10000", "10000", "01110", "00001", "00001", "11110"),
    "T": ("11111", "00100", "00100", "00100", "00100", "00100", "00100"),
    "U": ("10001", "10001", "10001", "10001", "10001", "10001", "01110"),
    "V": ("10001", "10001", "10001", "10001", "10001", "01010", "00100"),
    "W": ("10001", "10001", "10001", "10101", "10101", "11011", "10001"),
    "X": ("10001", "10001", "01010", "00100", "01010", "10001", "10001"),
    "Y": ("10001", "10001", "01010", "00100", "00100", "00100", "00100"),
    "Z": ("11111", "00001", "00010", "00100", "01000", "10000", "11111"),
    "0": ("01110", "10001", "10011", "10101", "11001", "10001", "01110"),
    "1": ("00100", "01100", "00100", "00100", "00100", "00100", "01110"),
    "2": ("01110", "10001", "00001", "00010", "00100", "01000", "11111"),
    "3": ("11110", "00001", "00001", "01110", "00001", "00001", "11110"),
    "4": ("00010", "00110", "01010", "10010", "11111", "00010", "00010"),
    "5": ("11111", "10000", "11110", "00001", "00001", "10001", "01110"),
    "6": ("01110", "10000", "10000", "11110", "10001", "10001", "01110"),
    "7": ("11111", "00001", "00010", "00100", "01000", "01000", "01000"),
    "8": ("01110", "10001", "10001", "01110", "10001", "10001", "01110"),
    "9": ("01110", "10001", "10001", "01111", "00001", "00001", "01110"),
    " ": ("00000", "00000", "00000", "00000", "00000", "00000", "00000"),
    ".": ("00000", "00000", "00000", "00000", "00000", "01100", "01100"),
    ",": ("00000", "00000", "00000", "00000", "01100", "00100", "01000"),
    ":": ("00000", "01100", "01100", "00000", "01100", "01100", "00000"),
    ";": ("00000", "01100", "01100", "00000", "01100", "00100", "01000"),
    "!": ("00100", "00100", "00100", "00100", "00100", "00000", "00100"),
    "?": ("01110", "10001", "00001", "00010", "00100", "00000", "00100"),
    "-": ("00000", "00000", "00000", "01110", "00000", "00000", "00000"),
    "'": ("00100", "00100", "01000", "00000", "00000", "00000", "00000"),
    '"': ("01010", "01010", "00000", "00000", "00000", "00000", "00000"),
    "(": ("00010", "00100", "01000", "01000", "01000", "00100", "00010"),
    ")": ("01000", "00100", "00010", "00010", "00010", "00100", "01000"),
    "/": ("00001", "00010", "00010", "00100", "01000", "01000", "10000"),
    "%": ("11001", "11010", "00010", "00100", "01000", "01011", "10011"),
    "$": ("00100", "01111", "10100", "01110", "00101", "11110", "00100"),
    "&": ("01100", "10010", "10100", "01000", "10101", "10010", "01101"),
    "+": ("00000", "00100", "00100", "11111", "00100", "00100", "00000"),
    "=": ("00000", "00000", "11111", "00000", "11111", "00000", "00000"),
    "*": ("00000", "10101", "01110", "11111", "01110", "10101", "00000"),
    "#": ("01010", "01010", "11111", "01010", "11111", "01010", "01010"),
    "_": ("00000", "00000", "00000", "00000", "00000", "00000", "11111"),
    "•": ("00000", "00000", "01100", "01100", "01100", "00000", "00000"),
    "—": ("00000", "00000", "00000", "11111", "00000", "00000", "00000"),
}

# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.set(xx, yy, c)

    def frame(self, x, y, w, h, c, t=1):
        self.rect(x, y, w, t, c)
        self.rect(x, y + h - t, w, t, c)
        self.rect(x, y, t, h, c)
        self.rect(x + w - t, y, t, h, c)

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx - dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                return
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x0 += sx
            if e2 < dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for yy in range(cy - r, cy + r + 1):
            for xx in range(cx - r, cx + r + 1):
                d = (xx - cx) ** 2 + (yy - cy) ** 2
                if fill:
                    if d <= r * r:
                        self.set(xx, yy, c)
                else:
                    if r * r - 2 * r <= d <= r * r:
                        self.set(xx, yy, c)

    def tri(self, x0, y0, x1, y1, x2, y2, c):
        pts = sorted([(x0, y0), (x1, y1), (x2, y2)], key=lambda p: p[1])
        (ax, ay), (bx, by), (cx, cy) = pts
        def edge(xa, ya, xb, yb, y):
            if yb == ya:
                return xa
            return xa + (xb - xa) * (y - ya) / (yb - ya)
        for y in range(ay, cy + 1):
            if y < by:
                xa = edge(ax, ay, bx, by, y)
                xb = edge(ax, ay, cx, cy, y)
            else:
                xa = edge(bx, by, cx, cy, y)
                xb = edge(ax, ay, cx, cy, y)
            for x in range(int(min(xa, xb)), int(max(xa, xb)) + 1):
                self.set(x, y, c)

    # ---- text ----
    def glyph(self, x, y, ch, s, c):
        g = FONT.get(ch.upper(), FONT["?"])
        for r, row in enumerate(g):
            for col, bit in enumerate(row):
                if bit == "1":
                    self.rect(x + col * s, y + r * s, s, s, c)

    def text(self, x, y, s, c, txt):
        cx = x
        for ch in txt:
            if ch == "\n":
                continue
            self.glyph(cx, y, ch, s, c)
            cx += 6 * s
        return cx

    def text_w(self, s, txt):
        return len(txt) * 6 * s

    def text_center(self, y, s, c, txt, cx=512):
        self.text(cx - self.text_w(s, txt) // 2, y, s, c, txt)

    def wrap(self, txt, max_chars):
        words, lines, cur = txt.split(), [], ""
        for wd in words:
            add = wd if not cur else " " + wd
            if len(cur) + len(add) <= max_chars:
                cur += add
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def para(self, x, y, s, c, txt, max_chars, max_lines=None, lh=None):
        lines = self.wrap(txt, max_chars)
        if max_lines:
            lines = lines[:max_lines]
        step = lh if lh else 9 * s
        for i, ln in enumerate(lines):
            self.text(x, y + i * step, s, c, ln)
        return y + len(lines) * step


# ---------------------------------------------------------------- scenes
def scene_ship(cv, x, y, w, h):
    """Container ship at sea - lead illustration."""
    cv.rect(x, y, w, h, SKY)
    cv.rect(x, y + h - 26, w, 26, SEA)
    for i in range(5):
        cv.rect(x + 12 + i * 46, y + h - 30, 30, 4, (255, 255, 255))
    # hull
    cv.tri(x + 14, y + h - 58, x + w - 14, y + h - 58, x + w - 40, y + h - 26, (140, 40, 30))
    cv.rect(x + 14, y + h - 58, w - 28, 32, (140, 40, 30))
    # containers
    cols = [RED, BLUE, GOLD, GREEN, (200, 90, 20)]
    for r in range(2):
        for i in range(6):
            cv.rect(x + 26 + i * 34, y + h - 58 - (r + 1) * 22, 30, 20,
                    cols[(i + r) % len(cols)])
            cv.frame(x + 26 + i * 34, y + h - 58 - (r + 1) * 22, 30, 20, INK, 1)
    # bridge tower
    cv.rect(x + w - 66, y + h - 118, 40, 60, (240, 240, 235))
    cv.frame(x + w - 66, y + h - 118, 40, 60, INK, 1)
    for i in range(3):
        cv.rect(x + w - 60, y + h - 112 + i * 16, 28, 8, BLUE)
    # smoke
    cv.circle(x + w - 46, y + h - 128, 7, GREY)
    cv.circle(x + w - 38, y + h - 140, 9, GREY)
    cv.circle(x + w - 26, y + h - 150, 11, GREY)
    cv.frame(x, y, w, h, INK, 2)


def scene_refinery(cv, x, y, w, h):
    cv.rect(x, y, w, h, LIGHT)
    cv.rect(x, y + h - 14, w, 14, (90, 80, 66))
    for i, tx in enumerate((x + 8, x + 30, x + 52)):
        cv.rect(tx, y + 22, 10, h - 36, (70, 66, 60))
        cv.tri(tx - 4, y + 8, tx + 14, y + 8, tx + 5, y + 26, ORANGE)
        cv.tri(tx - 2, y + 14, tx + 12, y + 14, tx + 5, y + 26, RED)
    cv.circle(x + w - 12, y + 16, 6, GOLD)
    cv.frame(x, y, w, h, INK, 2)


def scene_eu(cv, x, y, w, h):
    import math
    cv.rect(x, y, w, h, (28, 48, 110))
    cx, cy = x + w // 2, y + h // 2
    for k in range(12):
        a = math.pi * 2 * k / 12 - math.pi / 2
        sx = int(cx + 24 * math.cos(a))
        sy = int(cy + 24 * math.sin(a))
        cv.circle(sx, sy, 3, GOLD)
    cv.frame(x, y, w, h, INK, 2)


def scene_missile(cv, x, y, w, h):
    cv.rect(x, y, w, h, SKY)
    cx = x + w // 2
    cv.tri(cx - 9, y + 12, cx + 9, y + 12, cx, y + 30, INK)
    cv.rect(cx - 9, y + 30, 18, 26, (220, 220, 215))
    cv.frame(cx - 9, y + 30, 18, 26, INK, 1)
    cv.tri(cx - 16, y + 48, cx - 9, y + 48, cx - 9, y + 62, RED)
    cv.tri(cx + 9, y + 48, cx + 16, y + 48, cx + 9, y + 62, RED)
    cv.tri(cx - 7, y + 56, cx + 7, y + 56, cx, y + h - 8, ORANGE)
    cv.circle(x + 10, y + 12, 4, (255, 255, 255))
    cv.frame(x, y, w, h, INK, 2)


def scene_jet(cv, x, y, w, h):
    cv.rect(x, y, w, h, LIGHT)
    cx, cy = x + w // 2, y + h // 2
    cv.tri(cx - 26, cy - 4, cx + 26, cy - 4, cx + 30, cy + 6, (60, 60, 60))
    cv.tri(cx - 8, cy - 16, cx + 6, cy - 4, cx - 2, cy - 2, (60, 60, 60))
    cv.tri(cx - 8, cy + 8, cx + 6, cy + 6, cx - 2, cy + 10, (60, 60, 60))
    cv.circle(cx + 24, cy - 1, 3, RED)
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)):
        cv.line(x + w - 18, y + 16, x + w - 18 + dx * 10, y + 16 + dy * 10, ORANGE)
    cv.circle(x + w - 18, y + 16, 4, ORANGE)
    cv.frame(x, y, w, h, INK, 2)


def scene_city(cv, x, y, w, h):
    cv.rect(x, y, w, h, (210, 196, 170))
    cv.rect(x + 8, y + 30, 18, h - 44, (70, 66, 60))
    cv.rect(x + 30, y + 18, 18, h - 32, (90, 86, 78))
    cv.rect(x + 52, y + 38, 16, h - 52, (70, 66, 60))
    for bx in (x + 12, x + 34, x + 56):
        for by in (y + 34, y + 46):
            cv.rect(bx, by, 4, 5, GOLD)
    cv.circle(x + 38, y + 12, 5, GREY)
    cv.circle(x + 46, y + 6, 7, GREY)
    cv.rect(x, y + h - 14, w, 14, (90, 80, 66))
    cv.frame(x, y, w, h, INK, 2)


def scene_tanker(cv, x, y, w, h):
    cv.rect(x, y, w, h, LIGHT)
    cv.tri(x + 12, y + 8, x + 30, y + 8, x + 21, y + 30, ORANGE)
    cv.tri(x + 16, y + 16, x + 28, y + 16, x + 22, y + 30, RED)
    cv.tri(x + 40, y + 12, x + 56, y + 12, x + 48, y + 32, ORANGE)
    cv.rect(x + 10, y + 34, 44, 18, (200, 200, 195))
    cv.frame(x + 10, y + 34, 44, 18, INK, 1)
    cv.rect(x + 54, y + 38, 14, 14, RED)
    cv.circle(x + 18, y + 56, 6, INK)
    cv.circle(x + 46, y + 56, 6, INK)
    cv.circle(x + 62, y + 56, 6, INK)
    cv.rect(x, y + h - 12, w, 12, (90, 80, 66))
    cv.frame(x, y, w, h, INK, 2)


def scene_mine(cv, x, y, w, h):
    cv.rect(x, y, w, h, (120, 96, 66))
    cv.rect(x + 8, y + 20, w - 16, h - 34, INK)
    cv.tri(x + 8, y + 20, x + w - 8, y + 20, x + w // 2, y + 2, INK)
    cv.circle(x + w // 2, y + 44, 12, GOLD)
    cv.rect(x + w // 2 - 14, y + 44, 28, 4, GOLD)
    cv.circle(x + w // 2, y + 38, 4, (255, 255, 220))
    cv.rect(x + 8, y + h - 22, w - 16, 8, SEA)
    cv.rect(x, y + h - 14, w, 14, (90, 80, 66))
    cv.frame(x, y, w, h, INK, 2)


# ---------------------------------------------------------------- stories
STORIES = [
    ("MIDDLE EAST",
     ["HOUTHIS STRIKE SAUDI", "PORTS AND REFINERY"],
     "Houthis claim hits on Jeddah, Jizan ports and Ras Tanura.",
     scene_refinery),
    ("EUROPE",
     ["EU SPLIT OVER 45BN", "UKRAINE LOAN"],
     "Leaders meet in Brussels over a EUR 45bn loan for Ukraine.",
     scene_eu),
    ("ASIA",
     ["KIM ORDERS MORE", "TACTICAL NUKES"],
     "Kim says North Korea should deploy tactical nukes widely.",
     scene_missile),
    ("UKRAINE WAR",
     ["UKRAINE HITS AIRBASE;", "KYIV UNDER FIRE"],
     "Kyiv says five jets hit at Savasleyka; Russia hits Kyiv.",
     scene_jet),
    ("GAZA",
     ["ISRAELI STRIKES KILL", "NINE IN GAZA"],
     "Strikes kill at least nine in Gaza overnight, medics say.",
     scene_city),
    ("EGYPT",
     ["CAIRO TANKER FIRE", "KILLS AT LEAST 31"],
     "Tanker overturns on Cairo's Ring Road; 31 dead, 21 hurt.",
     scene_tanker),
    ("INDONESIA",
     ["13 MINERS TRAPPED", "IN FLOODED MINE"],
     "Race to save 13 miners trapped in a flooded mine.",
     scene_mine),
]

LEAD_HEAD = ["TRUMP HITS 14 PARTNERS", "WITH NEW TARIFFS"]
LEAD_BODY = ("Washington unveils country-by-country tariffs on 14 economies - "
             "China, the EU, Japan and India among them - accusing them of "
             "flooding world markets with excess factory output.")


# ---------------------------------------------------------------- draw page
def draw():
    cv = Canvas(W, H, PAPER)
    M = 28
    # masthead
    cv.text_center(26, 6, INK, "THE WORLD IN ONE DAY")
    cv.hline(M, 118, W - 2 * M, INK, 4)
    cv.hline(M, 126, W - 2 * M, INK, 1)
    cv.text_center(140, 2, RED, "THURSDAY, 26 NOVEMBER 2026")
    cv.text_center(164, 1, GREY, "THE DAY'S NEWS IN ONE PAGE  •  EVERY STORY BELOW HAPPENED OR WAS FIRST REPORTED TODAY")
    cv.hline(M, 186, W - 2 * M, INK, 2)

    # lead story
    lx, ly, lw, lh = M, 198, W - 2 * M, 196
    cv.frame(lx, ly, lw, lh, INK, 3)
    cv.text(lx + 16, ly + 12, 2, RED, "LEAD STORY  —  TRADE WAR, WASHINGTON")
    y = ly + 40
    for ln in LEAD_HEAD:
        cv.text(lx + 16, y, 4, INK, ln)
        y += 36
    cv.para(lx + 16, y + 6, 2, INK, LEAD_BODY, 52, max_lines=4, lh=18)
    scene_ship(cv, lx + lw - 300, ly + 14, 284, 168)

    # grid of 7 stories
    gx, gy = M, 406
    cw, ch, gap = 476, 114, 10
    for i, (kick, head, body, scene) in enumerate(STORIES):
        row, col = divmod(i, 2)
        bx = gx + col * (cw + gap)
        by = gy + row * (ch + gap)
        cv.frame(bx, by, cw, ch, INK, 2)
        cv.rect(bx + 2, by + 2, cw - 4, 20, LIGHT)
        cv.text(bx + 12, by + 7, 1, RED, kick)
        scene(cv, bx + 12, by + 28, 72, 76)
        hx = bx + 96
        hy = by + 28
        for ln in head:
            cv.text(hx, hy, 3, INK, ln)
            hy += 24
        cv.para(bx + 96, hy + 2, 2, INK, body, 30, max_lines=2, lh=17)

    # also-today strip
    sy = 900
    cv.rect(M, sy, W - 2 * M, 64, LIGHT)
    cv.frame(M, sy, W - 2 * M, 64, INK, 2)
    cv.text(M + 12, sy + 6, 2, RED, "ALSO TODAY")
    strip = ("MACY'S 100TH THANKSGIVING PARADE IN NEW YORK  •  "
             "PUERTO RICO COURT CANCELS LUMA CONTRACT  •  "
             "NASDAQ NEARS BEAR MARKET  •  "
             "LIVERPOOL BEAT CLUB BRUGGE 3-0")
    cv.para(M + 12, sy + 26, 2, INK, strip, 78, max_lines=2, lh=18)

    # footer
    cv.text_center(982, 1, GREY,
                   "SOURCES: REUTERS  •  AP  •  KCNA  •  ONETURN.NEWS  •  OPEN CHRONICLE  •  DAILY SUMMARY OF  •  NEWSQUAWK")
    return cv


# ---------------------------------------------------------------- PNG encode
def chunk(typ, data):
    out = struct.pack(">I", len(data)) + typ + data
    out += struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF)
    return out


def png_bytes(cv):
    raw = bytearray()
    for y in range(cv.h):
        raw.append(0)  # filter: none
        raw += cv.px[y * cv.w * 3:(y + 1) * cv.w * 3]
    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
            + chunk(b"IEND", b""))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    data = png_bytes(draw())
    with open(os.path.join(out_dir, "entry.png"), "wb") as f:
        f.write(data)


if __name__ == "__main__":
    main()
