"""Draw assets/entry.png: a newspaper front page of Saturday 21 November 2026.

Reads data/stories.json (every claim in it is checked against the saved RSS
feeds by tools/verify_facts.py), draws the illustrations from tools/scenes.py
and lays out: dated title, by-the-numbers strip with region tabs, 3 big
illustrated stories, 12 small illustrated stories, a numbered map, an ALSO
list, a date-check box and a sources line. Every text block is fitted into its
own rectangle and the script stops if text does not fit or blocks overlap.
"""
import json
import math
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import scenes  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = "/usr/share/fonts/truetype/"
SERIF_B = F + "liberation/LiberationSerif-Bold.ttf"
SERIF = F + "liberation/LiberationSerif-Regular.ttf"
SERIF_I = F + "liberation/LiberationSerif-Italic.ttf"
SANS = F + "liberation/LiberationSans-Regular.ttf"
SANS_B = F + "liberation/LiberationSans-Bold.ttf"
COND_B = F + "dejavu/DejaVuSansCondensed-Bold.ttf"

W = H = 1024
M = 12
PAPER = (245, 240, 226)
CARD = (252, 249, 240)
INK = (22, 20, 18)
GREY = (86, 80, 72)
RED = (186, 28, 28)
REGION = {
    "Europe": (30, 78, 140), "Americas": (24, 112, 72), "Middle East": (150, 84, 20),
    "Africa": (120, 52, 120), "Climate": (20, 110, 118), "Tech": (186, 28, 28),
    "Asia": (170, 40, 100), "World": (84, 88, 100),
}
boxes = []


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, fnt, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if not cur:
                return None
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, text, path, rect, start, low, fill, align="left", valign="top", spacing=1.1):
    x0, y0, x1, y1 = rect
    for size in range(start, low - 1, -1):
        fnt = font(path, size)
        lines = wrap(d, text, fnt, x1 - x0)
        if lines is None:
            continue
        lh = int(size * spacing)
        if lh * len(lines) <= y1 - y0:
            break
    else:
        sys.exit(f"text does not fit: {text[:60]!r} in {rect}")
    y = y0 + ((y1 - y0 - lh * len(lines)) // 2 if valign == "middle" else 0)
    for ln in lines:
        w = d.textlength(ln, font=fnt)
        x = x0 if align == "left" else x0 + (x1 - x0 - w) / 2
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y, size


def register(name, x0, y0, x1, y1):
    for o in boxes:
        if x0 < o[3] and o[1] < x1 and y0 < o[4] and o[2] < y1:
            sys.exit(f"overlap: {name} and {o[0]}")
    boxes.append((name, x0, y0, x1, y1))


def tag(d, x, y, label, region, size=12):
    f = font(COND_B, size)
    w = int(d.textlength(label, font=f)) + 10
    d.rectangle([x, y, x + w, y + size + 6], fill=REGION[region])
    d.text((x + 5, y + 3), label, font=f, fill=(255, 255, 255))
    return w


def badge(d, cx, cy, n, r=10):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=INK, outline=(255, 255, 255), width=2)
    d.text((cx, cy), str(n), font=font(SANS_B, 12 if n < 10 else 11), fill=(255, 255, 255), anchor="mm")


LAND = [
    [(-168, 66), (-156, 71), (-125, 70), (-95, 73), (-80, 73), (-62, 67), (-55, 52), (-67, 45), (-76, 38), (-81, 31), (-80, 25),
     (-84, 30), (-90, 29), (-97, 26), (-97, 20), (-90, 21), (-87, 15), (-83, 9), (-78, 8), (-85, 11), (-92, 15), (-105, 20),
     (-110, 24), (-114, 31), (-118, 34), (-124, 40), (-124, 48), (-135, 58), (-150, 60), (-165, 60)],
    [(-55, 60), (-45, 60), (-20, 70), (-20, 82), (-60, 82), (-72, 76), (-58, 66)],
    [(-78, 8), (-60, 10), (-50, 0), (-35, -6), (-39, -15), (-48, -26), (-58, -38), (-66, -46), (-70, -54), (-75, -50),
     (-73, -38), (-71, -18), (-80, -6), (-80, 0)],
    [(-10, 36), (-9, 43), (-1, 46), (-5, 48), (3, 51), (8, 54), (10, 57), (5, 62), (15, 69), (30, 71), (60, 70), (100, 77),
     (140, 72), (170, 69), (180, 66), (160, 60), (155, 52), (142, 48), (135, 43), (128, 35), (122, 30), (121, 22), (108, 18),
     (106, 9), (100, 8), (98, 16), (92, 22), (80, 15), (77, 8), (72, 20), (66, 25), (57, 25), (56, 27), (50, 30), (48, 29),
     (52, 24), (56, 18), (44, 12), (34, 28), (35, 34), (27, 37), (23, 37), (20, 40), (13, 44), (18, 40), (12, 38), (7, 43),
     (-1, 37)],
    [(-17, 21), (-10, 30), (-5, 36), (10, 37), (32, 31), (35, 28), (43, 12), (51, 12), (40, -5), (40, -15), (33, -27),
     (20, -35), (15, -28), (12, -15), (9, -1), (8, 4), (-8, 4), (-17, 14)],
    [(114, -22), (122, -18), (135, -12), (142, -11), (153, -26), (150, -37), (140, -38), (130, -32), (115, -34)],
    [(-6, 50), (2, 51), (0, 54), (-3, 58), (-6, 56)],
]


def draw_map(d, rect, pins):
    x0, y0, x1, y1 = rect
    d.rectangle(rect, fill=(205, 224, 238), outline=GREY)
    lon0, lon1, lat0, lat1 = -170, 180, 78, -56
    sx = (x1 - x0) / (lon1 - lon0)
    sy = (y1 - y0) / (lat0 - lat1)

    def proj(lon, lat):
        return x0 + (lon - lon0) * sx, y0 + (lat0 - lat) * sy

    for poly in LAND:
        d.polygon([proj(lo, la) for lo, la in poly], fill=(226, 214, 180), outline=(170, 156, 120))
    pts = [list(proj(lo, la)) for _, lo, la in pins]
    for _ in range(80):  # push crowded dots apart a little
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                dx, dy = pts[j][0] - pts[i][0], pts[j][1] - pts[i][1]
                dist = math.hypot(dx, dy) or 0.01
                if dist < 13:
                    push = (13 - dist) / 2
                    pts[i][0] -= dx / dist * push
                    pts[i][1] -= dy / dist * push
                    pts[j][0] += dx / dist * push
                    pts[j][1] += dy / dist * push
    for (n, _, _), (px, py) in zip(pins, pts):
        d.ellipse([px - 6.5, py - 6.5, px + 6.5, py + 6.5], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py), str(n), font=font(SANS_B, 9), fill=(255, 255, 255), anchor="mm")


def main():
    with open(os.path.join(ROOT, "data", "stories.json"), encoding="utf-8") as f:
        data = json.load(f)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # masthead
    register("tag", M, 6, W - M, 22)
    text_block(d, data["tag"], COND_B, (M, 6, W - M, 22), 11, 8, INK, "center", "middle")
    d.rectangle([M, 24, W - M, 26], fill=INK)
    register("title", M, 28, W - M, 90)
    text_block(d, data["title"], SERIF_B, (M, 28, W - M, 90), 64, 40, INK, "center", "middle")
    register("lead", M, 91, W - M, 111)
    text_block(d, data["lead_line"], SERIF_I, (M, 91, W - M, 111), 17, 11, GREY, "center", "middle")

    # by the numbers
    nums = data["numbers"]
    ny0, ny1 = 114, 168
    cw = (W - 2 * M) / len(nums)
    for i, n in enumerate(nums):
        x0, x1 = int(M + i * cw) + 4, int(M + (i + 1) * cw) - 4
        register(f"num{i}", x0, ny0, x1, ny1)
        text_block(d, n["value"], SERIF_B, (x0, ny0, x1, ny0 + 32), 34, 18, INK, "center", "middle")
        text_block(d, n["label"], SANS, (x0, ny0 + 33, x1, ny1), 12, 9, GREY, "center")
        if i:
            d.line([x0 - 4, ny0 + 4, x0 - 4, ny1 - 2], fill=(150, 144, 130))
    d.rectangle([M, 171, W - M, 172], fill=INK)

    # region tabs, counted over all 31 stories
    allitems = data["big"] + data["mini"] + data["also"]
    counts = {}
    for s in allitems:
        counts[s["region"]] = counts.get(s["region"], 0) + 1
    order = sorted(counts, key=lambda r: -counts[r])
    tx, ty0, ty1 = M, 176, 192
    span = W - 2 * M - 3 * (len(order) - 1)
    wsum = sum(counts[r] + 3 for r in order)
    for i, r in enumerate(order):
        w = round(span * (counts[r] + 3) / wsum)
        if i == len(order) - 1:
            w = W - M - tx
        register("tab-" + r, tx, ty0, tx + w, ty1)
        d.rectangle([tx, ty0, tx + w, ty1], fill=REGION[r])
        text_block(d, f"{r.upper()} {counts[r]}", COND_B, (tx + 3, ty0 + 1, tx + w - 3, ty1 - 1), 12, 8,
                   (255, 255, 255), "center", "middle")
        tx += w + 3

    # three big illustrated stories
    by0, by1 = 198, 458
    gap = 8
    bw = (W - 2 * M - 2 * gap) // 3
    for i, s in enumerate(data["big"]):
        x0 = M + i * (bw + gap)
        register(f"big{i}", x0, by0, x0 + bw, by1)
        d.rectangle([x0, by0, x0 + bw, by1], fill=CARD, outline=INK, width=2)
        pic = scenes.scene(s["scene"], bw - 4, 124)
        img.paste(pic, (x0 + 2, by0 + 2))
        badge(d, x0 + 16, by0 + 16, s["n"], 11)
        tag(d, x0 + 8, by0 + 130, s["kicker"], s["region"], 11)
        hy, _ = text_block(d, s["headline"], SERIF_B, (x0 + 8, by0 + 150, x0 + bw - 8, by0 + 200), 25, 16, INK)
        text_block(d, s["body"], SANS, (x0 + 8, hy + 6, x0 + bw - 8, by1 - 5), 14, 9, INK, spacing=1.15)

    # twelve small illustrated stories (4 x 3)
    my0, my1 = 466, 738
    cols, rows, g = 4, 3, 6
    mw = (W - 2 * M - g * (cols - 1)) // cols
    mh = (my1 - my0 - g * (rows - 1)) // rows
    for i, s in enumerate(data["mini"]):
        c, r = i % cols, i // cols
        x0, y0 = M + c * (mw + g), my0 + r * (mh + g)
        register(f"mini{i}", x0, y0, x0 + mw, y0 + mh)
        d.rectangle([x0, y0, x0 + mw, y0 + mh], fill=CARD, outline=GREY)
        d.rectangle([x0, y0, x0 + 3, y0 + mh], fill=REGION[s["region"]])
        ps = mh - 8
        img.paste(scenes.scene(s["scene"], ps, ps), (x0 + 6, y0 + 4))
        badge(d, x0 + 17, y0 + 15, s["n"], 9)
        tx0 = x0 + ps + 11
        tw = tag(d, tx0, y0 + 4, s["kicker"], s["region"], 9)
        text_block(d, s["headline"], SERIF_B, (tx0, y0 + 22, x0 + mw - 5, y0 + 50), 16, 12, INK)
        text_block(d, s["body"], SANS, (tx0, y0 + 50, x0 + mw - 5, y0 + mh - 2), 11, 8, INK)

    # map and ALSO list
    by0, by1 = 745, 934
    mx1 = M + 362
    register("maphead", M, by0, mx1, by0 + 16)
    d.rectangle([M, by0, mx1, by0 + 16], fill=INK)
    d.text((M + 6, by0 + 3), "WHERE IT HAPPENED  (numbers = stories)", font=font(COND_B, 10), fill=(255, 255, 255))
    register("map", M, by0 + 17, mx1, by1)
    pins = [(s["n"], s["lon"], s["lat"]) for s in data["big"] + data["mini"] if s["lat"] is not None]
    draw_map(d, (M, by0 + 17, mx1, by1), pins)

    ax0 = mx1 + 10
    register("alsohead", ax0, by0, W - M, by0 + 16)
    d.rectangle([ax0, by0, W - M, by0 + 16], fill=RED)
    d.text((ax0 + 6, by0 + 3), f"ALSO ON SATURDAY 21 NOVEMBER: {len(data['also'])} MORE STORIES OF THE DAY", font=font(COND_B, 10), fill=(255, 255, 255))
    also = data["also"]
    colw = (W - M - ax0) // 2
    per = len(also) // 2
    rowh = (by1 - by0 - 20) // per
    for i, a in enumerate(also):
        cx = ax0 + (i // per) * colw
        cy = by0 + 20 + (i % per) * rowh
        register(f"also{i}", cx, cy, cx + colw - 4, cy + rowh - 1)
        d.rectangle([cx, cy + 3, cx + 3, cy + rowh - 5], fill=REGION[a["region"]])
        d.text((cx + 8, cy + 2), str(a["n"]), font=font(COND_B, 10), fill=GREY)
        text_block(d, a["text"], SANS_B, (cx + 26, cy, cx + colw - 6, cy + rowh - 1), 11, 8, INK, valign="middle")

    # date check and sources
    register("datecheck", M, 940, W - M, 1000)
    d.rectangle([M, 940, W - M, 1000], fill=(252, 238, 236), outline=RED, width=2)
    d.rectangle([M + 6, 947, M + 98, 965], fill=RED)
    d.text((M + 12, 950), "DATE CHECK", font=font(COND_B, 12), fill=(255, 255, 255))
    text_block(d, data["date_check"], SANS, (M + 108, 944, W - M - 8, 997), 13, 9, INK, valign="middle")
    register("sources", M, 1003, W - M, 1020)
    text_block(d, data["sources"], SANS, (M, 1003, W - M, 1020), 11, 8, GREY, "center", "middle")

    out = os.path.join(ROOT, "assets", "entry.png")
    img.save(out, optimize=True)
    print(f"wrote {out}: {os.path.getsize(out)} bytes, {len(boxes)} blocks, no overlaps")


if __name__ == "__main__":
    main()
