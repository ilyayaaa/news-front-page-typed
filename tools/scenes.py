"""Hand-drawn news illustrations for the front page, made with Pillow shapes only.

scene(name, w, h) returns an RGB image. Each scene is drawn in a logical space:
x runs from -50 to 50 around the picture's centre and y from 0 (top) to 100
(bottom), both scaled by k = h / 100, so the same scene works for a wide card
and a small square. Pictures are drawn 3x larger and shrunk for smooth edges.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SS = 3


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w * SS, h * SS
        self.k = self.h / 100.0
        self.img = Image.new("RGB", (self.w, self.h), (0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def X(self, dx):
        return self.w / 2 + dx * self.k

    def Y(self, dy):
        return dy * self.k

    def P(self, pts):
        return [(self.X(x), self.Y(y)) for x, y in pts]

    def sky(self, top, bottom, y0=0, y1=100):
        for yy in range(int(self.Y(y0)), int(self.Y(y1))):
            t = (yy - self.Y(y0)) / max(1, self.Y(y1) - self.Y(y0))
            col = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
            self.d.line([(0, yy), (self.w, yy)], fill=col)

    def rect(self, x0, y0, x1, y1, fill, outline=None, width=1):
        self.d.rectangle([self.X(x0), self.Y(y0), self.X(x1), self.Y(y1)], fill=fill,
                         outline=outline, width=max(1, int(width * SS)))

    def poly(self, pts, fill):
        self.d.polygon(self.P(pts), fill=fill)

    def circle(self, cx, cy, r, fill, outline=None, width=1):
        self.d.ellipse([self.X(cx - r), self.Y(cy - r), self.X(cx + r), self.Y(cy + r)],
                       fill=fill, outline=outline, width=max(1, int(width * SS)))

    def line(self, pts, fill, width=1):
        self.d.line(self.P(pts), fill=fill, width=max(1, int(width * self.k)))

    def text(self, cx, cy, s, size, fill, font=FONT_B):
        f = ImageFont.truetype(font, max(6, int(size * self.k)))
        self.d.text((self.X(cx), self.Y(cy)), s, font=f, fill=fill, anchor="mm")

    def stars(self, n, seed, y_max=60, color=(255, 255, 255)):
        rnd = random.Random(seed)
        for _ in range(n):
            x = rnd.uniform(0, self.w)
            y = rnd.uniform(0, self.Y(y_max))
            r = rnd.choice([1, 1, 2]) * SS * 0.6
            self.d.ellipse([x - r, y - r, x + r, y + r], fill=color)

    def burst(self, cx, cy, r, c1, c2, points=10):
        outer, inner = [], []
        for i in range(points * 2):
            a = math.pi * i / points
            rr = r if i % 2 == 0 else r * 0.45
            outer.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
        self.d.polygon(outer, fill=c1)
        inner = [(cx + (x - cx) * 0.55, cy + (y - cy) * 0.55) for x, y in outer]
        self.d.polygon(inner, fill=c2)

    def done(self, w, h):
        return self.img.resize((w, h), Image.LANCZOS)


def rotate_pts(pts, ang, ox, oy):
    c, s = math.cos(ang), math.sin(ang)
    return [(ox + x * c - y * s, oy + x * s + y * c) for x, y in pts]


def missile(c, x, y, ang, length=26, color=(230, 230, 235)):
    body = [(-length, -2.6), (length * 0.55, -2.6), (length, 0), (length * 0.55, 2.6), (-length, 2.6)]
    fins = [(-length, -2.6), (-length - 5, -7), (-length + 7, -2.6)], [(-length, 2.6), (-length - 5, 7), (-length + 7, 2.6)]
    flame = [(-length, -2), (-length - 20, 0), (-length, 2)]
    c.poly(rotate_pts(flame, ang, x, y), (255, 150, 30))
    c.poly(rotate_pts([(-length, -1), (-length - 11, 0), (-length, 1)], ang, x, y), (255, 240, 150))
    c.poly(rotate_pts(body, ang, x, y), color)
    for f in fins:
        c.poly(rotate_pts(f, ang, x, y), (200, 40, 40))
    c.poly(rotate_pts([(length * 0.55, -2.6), (length, 0), (length * 0.55, 2.6)], ang, x, y), (200, 40, 40))


def scene_poland(c):
    c.sky((8, 14, 44), (48, 58, 120))
    c.stars(40, 1)
    c.rect(-400, 82, 400, 100, (22, 30, 28))
    # Polish flag
    c.rect(-47, 44, -45, 92, (150, 150, 150))
    c.rect(-45, 46, -9, 62, (245, 245, 245))
    c.rect(-45, 62, -9, 78, (210, 30, 50))
    # glowing impact on the ground
    c.burst(c.X(-22), c.Y(88), 20 * c.k, (255, 140, 30), (255, 235, 120), 9)
    # missile coming down from upper right with a long trail
    c.line([(50, 0), (-8, 66)], (255, 120, 60), 1.6)
    missile(c, 10, 40, math.radians(131), 24)
    c.circle(-22, 88, 6, (255, 250, 200))
    for i, dx in enumerate([-110, -86, 62, 88, 112]):
        c.rect(dx - 5, 78 - (i % 3) * 5, dx + 5, 90, (30, 38, 44))


def scene_cop31(c):
    c.sky((120, 175, 225), (225, 238, 248))
    c.rect(-400, 86, 400, 100, (70, 110, 80))
    for dx, h in [(-46, 38), (-38, 48), (-30, 34)]:  # smokestacks
        c.rect(dx - 3, 100 - h - 8, dx + 3, 90, (90, 90, 96))
        c.rect(dx - 3, 100 - h - 8, dx + 3, 100 - h - 5, (200, 60, 50))
        for i in range(4):
            c.circle(dx + i * 4, 100 - h - 12 - i * 8, 5 + i * 1.8, (150, 150, 155))
    c.circle(2, 50, 31, (35, 105, 195), (20, 60, 120), 1.2)
    for pts in [[(-14, 32), (-4, 28), (4, 36), (-2, 46), (-12, 50), (-20, 42)],
                [(4, 50), (16, 46), (24, 56), (16, 72), (8, 66)],
                [(-20, 56), (-10, 58), (-8, 72), (-16, 74)]]:
        c.poly(pts, (70, 160, 85))
    c.circle(-20, 36, 5, (240, 245, 250))
    # thermometer
    c.rect(37, 18, 43, 70, (245, 245, 245), (60, 60, 60), 1)
    c.rect(39, 30, 41, 70, (220, 40, 40))
    c.circle(40, 74, 7, (220, 40, 40), (60, 60, 60), 1)
    # overtime clock
    c.circle(-38, 22, 12, (250, 250, 250), (30, 30, 30), 1.5)
    c.line([(-38, 22), (-38, 14)], (20, 20, 20), 1.5)
    c.line([(-38, 22), (-32, 25)], (200, 30, 30), 1.5)


def scene_riyadh(c):
    c.sky((12, 10, 38), (150, 70, 70), 0, 85)
    c.stars(30, 4, 40)
    rnd = random.Random(7)
    dx = -100
    while dx < 100:
        w = rnd.randint(7, 13)
        h = rnd.randint(18, 44)
        c.rect(dx, 90 - h, dx + w, 100, (22, 22, 38))
        for wy in range(int(90 - h + 3), 96, 6):
            for wx in range(int(dx + 2), int(dx + w - 2), 4):
                if rnd.random() < 0.45:
                    c.rect(wx, wy, wx + 1.4, wy + 2.4, (255, 205, 90))
        dx += w + 1
    # tower with an arch notch at the top
    c.rect(-6, 16, 14, 100, (34, 38, 64))
    c.poly([(-6, 16), (4, 34), (14, 16), (14, 12), (-6, 12)], (150, 70, 70))
    for wy in range(40, 96, 5):
        c.rect(-4, wy, 12, wy + 1.2, (255, 205, 90))
    # three incoming missiles and three interceptions
    for i, (x, y) in enumerate([(-30, 30), (24, 22), (46, 44)]):
        c.line([(x + 40, y - 34), (x, y)], (255, 130, 60), 1.2)
        missile(c, x + 8, y - 6, math.radians(140), 10)
        c.burst(c.X(x), c.Y(y), 9 * c.k, (255, 220, 90), (255, 255, 235), 8)


def scene_kyiv(c):
    c.sky((60, 40, 80), (235, 130, 70), 0, 70)
    c.rect(-400, 70, 400, 100, (30, 70, 110))
    for i in range(6):
        c.line([(-90 + i * 30, 80 + (i % 2) * 6), (-70 + i * 30, 80 + (i % 2) * 6)], (80, 130, 175), 1)
    c.rect(-400, 52, 400, 57, (40, 40, 48))
    for dx in [-36, -12, 12, 36]:
        c.rect(dx - 2, 52, dx + 2, 82, (60, 60, 70))
        c.d.arc([c.X(dx + 2), c.Y(30), c.X(dx + 24), c.Y(74)], 180, 360, fill=(90, 90, 100), width=int(2.4 * c.k))
    c.poly([(-8, 52), (-3, 40), (0, 46), (4, 32), (8, 44), (14, 38), (12, 52)], (255, 140, 30))
    c.poly([(-2, 52), (1, 44), (4, 49), (8, 42), (9, 52)], (255, 230, 110))
    for i, (x, y, r) in enumerate([(2, 28, 7), (9, 20, 8), (17, 12, 9)]):
        c.circle(x, y, r, (70, 66, 74))


def scene_wallstreet(c):
    c.sky((14, 22, 46), (28, 40, 78))
    for gy in range(15, 95, 16):
        c.line([(-400, gy), (400, gy)], (50, 64, 100), 0.5)
    vals = [(22, 40), (26, 46), (34, 52), (40, 60), (48, 66), (56, 76), (64, 80), (72, 90)]
    for i, (a, b) in enumerate(vals):
        x = -42 + i * 12
        col = (225, 55, 55) if i > 0 else (70, 190, 110)
        c.rect(x - 3, a + 2, x + 3, b, col)
        c.line([(x, a - 4), (x, b + 4)], col, 0.7)
    c.line([(-44, 18), (-20, 30), (0, 38), (24, 58), (44, 82)], (255, 255, 255), 1.4)
    c.poly([(48, 90), (36, 83), (42, 77)], (255, 255, 255))
    c.rect(-48, 8, -22, 18, (225, 55, 55))
    c.text(-35, 13, "-10%", 8, (255, 255, 255))


def scene_riemann(c):
    c.rect(-400, 0, 400, 100, (92, 62, 36))
    c.rect(-46, 8, 46, 92, (28, 78, 66), (160, 120, 70), 3)
    c.text(0, 32, "ζ(s) = 0", 15, (245, 245, 235), FONT_SERIF)
    c.line([(0, 50), (0, 84)], (255, 215, 110), 0.8)
    for y in (56, 63, 70, 77):
        c.circle(0, y, 1.8, (255, 215, 110))
    c.text(22, 56, "Re(s) = ½", 6, (235, 235, 225), FONT_SERIF)
    c.line([(-40, 50), (40, 50)], (235, 235, 225), 0.4)
    c.text(-26, 70, "?", 26, (255, 120, 100), FONT_SERIF)


def scene_ukeu(c):
    c.sky((200, 210, 225), (235, 238, 245))
    # UK flag, left
    x0, x1, y0, y1 = -46, -4, 22, 58
    c.rect(x0, y0, x1, y1, (0, 40, 120))
    c.line([(x0, y0), (x1, y1)], (255, 255, 255), 5)
    c.line([(x0, y1), (x1, y0)], (255, 255, 255), 5)
    c.line([(x0, y0), (x1, y1)], (200, 30, 50), 2)
    c.line([(x0, y1), (x1, y0)], (200, 30, 50), 2)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    c.rect(x0, my - 5, x1, my + 5, (255, 255, 255))
    c.rect(mx - 5, y0, mx + 5, y1, (255, 255, 255))
    c.rect(x0, my - 3, x1, my + 3, (200, 30, 50))
    c.rect(mx - 3, y0, mx + 3, y1, (200, 30, 50))
    # EU flag, right
    c.rect(4, 42, 46, 78, (0, 51, 153))
    for i in range(12):
        a = math.radians(i * 30)
        c.circle(25 + 11 * math.cos(a), 60 + 11 * math.sin(a), 1.7, (255, 204, 0))
    # handshake arrows
    c.poly([(-2, 68), (-14, 62), (-14, 66), (-30, 66), (-30, 70), (-14, 70), (-14, 74)], (60, 60, 70))
    c.poly([(2, 30), (14, 24), (14, 28), (30, 28), (30, 32), (14, 32), (14, 36)], (60, 60, 70))
    c.rect(-400, 88, 400, 100, (150, 160, 175))


def scene_genz(c):
    c.sky((236, 150, 90), (250, 215, 160), 0, 70)
    for dx, h in [(-44, 40), (-30, 52), (-16, 36), (18, 48), (32, 38), (46, 56)]:
        c.rect(dx - 6, 70 - h, dx + 6, 100, (110, 100, 125))
    c.rect(-400, 90, 400, 100, (70, 70, 82))
    rnd = random.Random(3)
    cols = [(200, 40, 60), (40, 100, 190), (40, 150, 90), (240, 190, 40), (140, 60, 170), (230, 110, 40)]
    signs = [(255, 255, 255), (255, 235, 130), (255, 255, 255), (170, 230, 255), (255, 255, 255), (255, 200, 200)]
    for i in range(11):
        x = -48 + i * 9.6
        y = 76 + (i % 2) * 4
        col = cols[i % 6]
        c.rect(x - 3.4, y, x + 3.4, 100, col)
        c.circle(x, y - 4, 3.6, (240, 205, 170))
        if i % 3 != 1:
            c.line([(x + 1, y + 3), (x + 1, y - 22 - (i % 2) * 4)], (90, 60, 40), 0.8)
            c.rect(x - 7, y - 36 - (i % 2) * 4, x + 9, y - 22 - (i % 2) * 4, signs[i % 6], (70, 70, 70), 0.6)
            c.line([(x - 4, y - 31 - (i % 2) * 4), (x + 6, y - 31 - (i % 2) * 4)], col, 1)
            c.line([(x - 4, y - 27 - (i % 2) * 4), (x + 3, y - 27 - (i % 2) * 4)], col, 1)


def scene_peru(c):
    c.sky((150, 190, 225), (240, 225, 200), 0, 70)
    c.poly([(-400, 70), (-62, 28), (-48, 44), (-30, 14), (-8, 48), (10, 30), (34, 52), (58, 24), (400, 70)], (120, 100, 90))
    c.poly([(-30, 14), (-37, 27), (-30, 24), (-25, 28)], (250, 250, 255))
    c.poly([(58, 24), (51, 35), (57, 32), (63, 36)], (250, 250, 255))
    c.rect(-400, 66, 400, 100, (200, 175, 120))
    c.rect(-400, 72, 400, 96, (250, 248, 240))
    pts = [(-46, 84)]
    rnd = random.Random(11)
    for i in range(1, 24):
        amp = 3 + 11 * math.sin(math.pi * i / 24) ** 2
        pts.append((-46 + i * 4, 84 + (amp if i % 2 else -amp) * rnd.uniform(0.7, 1.0)))
    c.line(pts + [(46, 84)], (200, 40, 40), 1.1)
    c.rect(-46, 83.6, 46, 84.4, (200, 150, 150))


def scene_datacentre(c):
    c.sky((10, 48, 60), (22, 90, 100))
    for i, dx in enumerate([-42, -22, -2]):
        c.rect(dx - 8, 20, dx + 8, 92, (36, 42, 52), (90, 100, 115), 1)
        for ry in range(24, 90, 8):
            c.rect(dx - 6, ry, dx + 6, ry + 5, (58, 66, 80))
            c.circle(dx - 3.5, ry + 2.5, 1, (90, 235, 130) if (ry + i) % 16 else (255, 190, 60))
    c.line([(18, 12), (18, 94)], (255, 255, 255), 0.5)
    c.circle(33, 42, 14, (240, 190, 40), (160, 110, 20), 1.5)
    c.text(33, 42, "$", 22, (120, 80, 10))
    c.rect(22, 66, 46, 80, (210, 40, 50))
    c.text(34, 73, "TAX", 9, (255, 255, 255))
    c.rect(-400, 92, 400, 100, (14, 30, 36))


def scene_denmark(c):
    c.rect(-400, 0, 400, 100, (200, 16, 46))
    c.rect(-400, 42, 400, 54, (255, 255, 255))
    c.rect(-28, 0, -16, 100, (255, 255, 255))
    # suitcase being sent out
    c.rect(6, 54, 38, 84, (92, 60, 40), (50, 30, 20), 1.2)
    c.rect(14, 46, 30, 54, (200, 16, 46), (50, 30, 20), 1.6)
    c.line([(6, 64), (38, 64)], (60, 38, 24), 1)
    c.rect(20, 61, 24, 67, (230, 200, 80))
    c.poly([(40, 40), (50, 50), (40, 60), (40, 54), (34, 54), (34, 46), (40, 46)], (255, 255, 255))


def scene_boat(c):
    c.sky((250, 190, 110), (255, 230, 175), 0, 60)
    c.rect(-400, 56, 400, 100, (28, 110, 120))
    for i in range(7):
        c.line([(-48 + i * 14, 68 + (i % 3) * 8), (-38 + i * 14, 68 + (i % 3) * 8)], (140, 205, 205), 1)
    # capsized hull
    c.poly([(-30, 60), (30, 56), (22, 78), (-20, 80)], (110, 70, 45))
    c.poly([(-30, 60), (30, 56), (28, 60), (-28, 64)], (70, 44, 28))
    c.line([(-20, 80), (22, 78)], (190, 230, 230), 1.4)
    # lifebuoy
    c.circle(38, 78, 9, (240, 240, 240), (200, 40, 40), 3)
    c.circle(38, 78, 4, (28, 110, 120))
    for a in (45, 135, 225, 315):
        c.circle(38 + 6.5 * math.cos(math.radians(a)), 78 + 6.5 * math.sin(math.radians(a)), 2.2, (200, 40, 40))


def scene_tanker(c):
    c.sky((60, 36, 52), (240, 140, 70), 0, 62)
    c.poly([(-400, 62), (-70, 52), (-46, 58), (-24, 50), (0, 62)], (50, 40, 52))
    c.rect(-400, 62, 400, 100, (18, 44, 80))
    c.poly([(-44, 70), (46, 70), (36, 86), (-34, 86)], (36, 34, 40))
    c.rect(-44, 66, 46, 70, (160, 40, 40))
    c.rect(26, 52, 40, 66, (200, 200, 205))
    c.rect(28, 55, 38, 58, (60, 60, 70))
    c.poly([(-14, 66), (-6, 48), (-2, 56), (4, 40), (10, 54), (14, 46), (18, 66)], (255, 140, 30))
    c.poly([(-4, 66), (2, 54), (6, 60), (10, 52), (12, 66)], (255, 230, 110))
    for x, y, r in [(2, 34, 7), (-2, 24, 8), (4, 13, 9)]:
        c.circle(x, y, r, (60, 56, 62))
    for i in range(6):
        c.line([(-48 + i * 17, 92), (-38 + i * 17, 92)], (70, 110, 150), 1)


def scene_rikers(c):
    c.sky((46, 50, 92), (220, 150, 120), 0, 75)
    for dx, h in [(-44, 30), (-34, 44), (-24, 26), (-10, 38), (22, 28), (34, 48), (44, 34)]:
        c.rect(dx - 4, 75 - h, dx + 4, 80, (36, 36, 60))
    c.rect(-400, 78, 400, 100, (30, 70, 100))
    for i in range(7):
        c.rect(-48 + i * 15.5, 0, -45 + i * 15.5, 100, (28, 28, 34))
    c.rect(-50, 0, 50, 6, (28, 28, 34))
    c.rect(-50, 90, 50, 100, (28, 28, 34))
    c.rect(-18, 38, 18, 64, (235, 235, 225), (28, 28, 34), 1.5)
    c.text(0, 51, "2032", 14, (190, 40, 40))


def scene_fire(c):
    c.sky((90, 30, 30), (255, 150, 50), 0, 70)
    c.poly([(-400, 70), (-60, 52), (-30, 62), (0, 46), (34, 60), (60, 50), (400, 66), (400, 100), (-400, 100)], (40, 28, 26))
    for dx, s in [(-36, 1.0), (-8, 1.3), (22, 1.1), (44, 0.8)]:
        c.poly([(dx - 8 * s, 76), (dx - 6 * s, 56), (dx - 1 * s, 62), (dx, 40 - 8 * s), (dx + 4 * s, 58), (dx + 8 * s, 52), (dx + 9 * s, 76)], (255, 120, 20))
        c.poly([(dx - 4 * s, 76), (dx - 1 * s, 62), (dx + 2 * s, 66), (dx + 5 * s, 76)], (255, 225, 100))
    for dx in (-48, 50):
        c.line([(dx, 78), (dx + 2, 42)], (24, 16, 16), 1.2)
        c.poly([(dx + 2, 44), (dx - 10, 50), (dx - 4, 40), (dx + 2, 36), (dx + 8, 40), (dx + 14, 50)], (24, 16, 16))
    c.circle(-4, 22, 8, (90, 70, 66))
    c.circle(8, 14, 9, (80, 62, 58))


SCENES = {
    "poland": scene_poland, "cop31": scene_cop31, "riyadh": scene_riyadh, "kyiv": scene_kyiv,
    "wallstreet": scene_wallstreet, "riemann": scene_riemann, "ukeu": scene_ukeu, "genz": scene_genz,
    "peru": scene_peru, "datacentre": scene_datacentre, "denmark": scene_denmark, "boat": scene_boat,
    "tanker": scene_tanker, "rikers": scene_rikers, "fire": scene_fire,
}


def scene(name, w, h):
    c = Canvas(w, h)
    SCENES[name](c)
    return c.done(w, h)
