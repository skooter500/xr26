#!/usr/bin/env python3
"""Generates the SVG diagrams used in the maths & physics slide decks.

Run from anywhere:  python3 notes/images/make_diagrams.py
Every diagram is computed from the same numbers used in the worked examples,
so if you change an example, change it here too and re-run.
"""
import math, os, colorsys

OUT = os.path.dirname(os.path.abspath(__file__))

INK = "#222"
GRID = "#ddd"
RED = "#d63031"      # Godot X axis colour
GREEN = "#2e9e44"    # Godot Y axis colour
BLUE = "#2d6cdf"     # Godot Z axis colour
ORANGE = "#e67e22"
PURPLE = "#8e44ad"
GREY = "#888"
COLORS = [INK, RED, GREEN, BLUE, ORANGE, PURPLE, GREY]


class SVG:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.parts = []

    def add(self, s):
        self.parts.append(s)

    def line(self, x1, y1, x2, y2, c=INK, w=2, dash=None, arrow=False, op=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#a{COLORS.index(c)})"' if arrow else ""
        self.add(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                 f'stroke="{c}" stroke-width="{w}" opacity="{op}"{d}{m}/>')

    def arrow(self, x1, y1, x2, y2, c=INK, w=3, dash=None, op=1):
        self.line(x1, y1, x2, y2, c, w, dash, True, op)

    def text(self, x, y, s, c=INK, size=18, anchor="middle", weight="normal", italic=False):
        st = ' font-style="italic"' if italic else ""
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.add(f'<text x="{x:.1f}" y="{y:.1f}" fill="{c}" font-size="{size}" '
                 f'text-anchor="{anchor}" font-weight="{weight}"{st}>{s}</text>')

    def circle(self, x, y, r, c=INK, fill="none", w=2, dash=None, op=1):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" stroke="{c}" '
                 f'fill="{fill}" stroke-width="{w}" fill-opacity="{op}"{d}/>')

    def rect(self, x, y, w, h, c=INK, fill="none", sw=2, rx=0, op=1, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" '
                 f'stroke="{c}" fill="{fill}" stroke-width="{sw}" fill-opacity="{op}"{d}/>')

    def path(self, d, c=INK, fill="none", w=2, dash=None, arrow=False, op=1):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#a{COLORS.index(c)})"' if arrow else ""
        self.add(f'<path d="{d}" stroke="{c}" fill="{fill}" stroke-width="{w}" '
                 f'fill-opacity="{op}"{da}{m}/>')

    def poly(self, pts, c=INK, fill="none", w=2, op=1):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.add(f'<polygon points="{p}" stroke="{c}" fill="{fill}" stroke-width="{w}" fill-opacity="{op}"/>')

    def polyline(self, pts, c=INK, w=2, dash=None, arrow=False):
        p = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        da = f' stroke-dasharray="{dash}"' if dash else ""
        m = f' marker-end="url(#a{COLORS.index(c)})"' if arrow else ""
        self.add(f'<polyline points="{p}" stroke="{c}" fill="none" stroke-width="{w}"{da}{m}/>')

    def arc(self, cx, cy, r, a0, a1, c=INK, w=2, arrow=False, dash=None):
        """Arc in *screen* degrees (0 = right, positive = clockwise on screen)."""
        x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
        x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
        large = 1 if abs(a1 - a0) > 180 else 0
        sweep = 1 if a1 > a0 else 0
        self.path(f"M{x0:.1f},{y0:.1f} A{r},{r} 0 {large} {sweep} {x1:.1f},{y1:.1f}", c, w=w,
                  arrow=arrow, dash=dash)

    def save(self, name):
        markers = "".join(
            f'<marker id="a{i}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
            f'markerHeight="6" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="{c}"/></marker>'
            for i, c in enumerate(COLORS))
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
               f'width="{self.w}" height="{self.h}" font-family="Helvetica, Arial, sans-serif">'
               f'<defs>{markers}</defs><rect width="100%" height="100%" fill="white"/>'
               + "".join(self.parts) + "</svg>")
        with open(os.path.join(OUT, name), "w") as f:
            f.write(svg)
        print("wrote", name)


def hexcol(h, s=1.0, v=1.0):
    r, g, b = colorsys.hsv_to_rgb(h % 1.0, s, v)
    return "#%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))


# --------------------------------------------------------------------------- TRIG
def trig_right_triangle():
    s = SVG(640, 330)
    A, B, C = (70, 270), (430, 270), (430, 70)
    s.poly([A, B, C], INK, "#eef4ff", 3)
    s.rect(410, 250, 20, 20, INK, "none", 2)
    s.arc(*A, 60, -29, 0, ORANGE, 3)
    s.text(150, 260, "θ", ORANGE, 26, weight="bold")
    s.text(250, 302, "Adjacent (A)", BLUE, 20, weight="bold")
    s.text(445, 175, "Opposite (O)", RED, 20, anchor="start", weight="bold")
    s.text(215, 150, "Hypotenuse (H)", GREEN, 20, weight="bold")
    s.line(*A, *B, BLUE, 5); s.line(*B, *C, RED, 5); s.line(*A, *C, GREEN, 5)
    s.text(280, 30, "SOH  CAH  TOA      H² = O² + A²", INK, 22, weight="bold")
    s.save("trig_right_triangle.svg")


def trig_unit_circle():
    s = SVG(520, 520)
    cx, cy, r = 260, 260, 190
    s.circle(cx, cy, r, GREY, w=2)
    s.arrow(cx - r - 30, cy, cx + r + 40, cy, INK, 2); s.text(cx + r + 40, cy - 10, "+X", INK, 18)
    s.arrow(cx, cy + r + 30, cx, cy - r - 40, INK, 2); s.text(cx + 22, cy - r - 25, "+Y", INK, 18)
    th = 35
    px, py = cx + r * math.cos(math.radians(th)), cy - r * math.sin(math.radians(th))
    s.line(px, py, px, cy, RED, 3, "6,4"); s.line(cx, cy, px, cy, BLUE, 5)
    s.arrow(cx, cy, px, py, GREEN, 4)
    s.circle(px, py, 6, GREEN, GREEN)
    s.text(px - 10, py - 14, "(cos θ, sin θ)", GREEN, 20, anchor="end", weight="bold")
    s.text((cx + px) / 2, cy + 25, "cos θ", BLUE, 18, weight="bold")
    s.text(px + 8, (py + cy) / 2 + 6, "sin θ", RED, 18, anchor="start", weight="bold")
    s.arc(cx, cy, 50, -th, 0, ORANGE, 3)
    s.text(cx + 62, cy - 12, "θ", ORANGE, 22, anchor="start", weight="bold")
    s.arc(cx, cy, 110, -100, -170, PURPLE, 2, arrow=True)
    s.text(cx - 100, cy - 115, "+ angles CCW", PURPLE, 16, anchor="end")
    for deg, lab, dx, dy in [(0, "0  (0)", 14, 26), (90, "90°  (π/2)", 14, -8), (180, "180°  (π)", -14, -10),
                              (270, "270°  (3π/2)", 14, 22)]:
        x, y = cx + r * math.cos(math.radians(deg)), cy - r * math.sin(math.radians(deg))
        s.circle(x, y, 5, INK, INK)
        s.text(x + dx, y + dy, lab, INK, 16, anchor="start" if dx > 0 else "end")
    s.text(cx, cy + r + 55 if False else 505, "radius = 1     360° = 2π = TAU radians", INK, 17)
    s.save("trig_unit_circle.svg")


def bearing_pt(cx, cy, r, b):
    return cx + r * math.sin(math.radians(b)), cy - r * math.cos(math.radians(b))


def trig_bearing_210():
    s = SVG(560, 560)
    cx, cy, r = 280, 270, 190
    s.circle(cx, cy, r, GRID, w=2)
    s.arrow(cx - r - 30, cy, cx + r + 30, cy, INK, 2); s.text(cx + r + 30, cy - 10, "+X", INK, 18)
    s.arrow(cx, cy + r + 30, cx, cy - r - 30, INK, 2); s.text(cx + 25, cy - r - 18, "+Y  (0°)", INK, 18, anchor="start")
    s.text(cx + r + 5, cy + 26, "90°", GREY, 16, anchor="start")
    s.text(cx + 8, cy + r + 24, "180°", GREY, 16, anchor="start")
    s.text(cx - r - 8, cy + 26, "270°", GREY, 16, anchor="end")
    # clockwise arc 0 -> 210 (screen angle = bearing - 90)
    s.arc(cx, cy, 60, -90, 120, ORANGE, 3, arrow=True)
    s.text(cx + 72, cy - 40, "210° clockwise", ORANGE, 18, anchor="start", weight="bold")
    ex, ey = bearing_pt(cx, cy, r, 210)
    s.line(ex, ey, cx, ey, RED, 3, "6,4")
    s.line(ex, ey, ex, cy, BLUE, 3, "6,4")
    s.arrow(cx, cy, ex, ey, GREEN, 5)
    s.circle(ex, ey, 6, GREEN, GREEN)
    s.text(ex - 10, ey + 30, "(−0.5, −0.866)", GREEN, 20, weight="bold")
    s.text((cx + ex) / 2 - 20, ey - 10, "x = sin 210° = −0.5", RED, 16, anchor="end")
    s.text(ex - 8, (cy + ey) / 2, "y = cos 210° = −0.866", BLUE, 16, anchor="end")
    s.arc(cx, cy, 110, 90, 120, PURPLE, 3)
    s.text(cx - 40, cy + 135, "30°", PURPLE, 18, weight="bold")
    s.text(280, 545, "0° = +Y, clockwise:   x = sin θ,  y = cos θ", INK, 20, weight="bold")
    s.save("trig_bearing_210.svg")


def trig_godot2d():
    s = SVG(520, 400)
    cx, cy = 120, 80
    s.arrow(cx, cy, cx + 330, cy, RED, 3); s.text(cx + 340, cy + 6, "+X", RED, 20, anchor="start")
    s.arrow(cx, cy, cx, cy + 280, GREEN, 3); s.text(cx + 10, cy + 300, "+Y (DOWN!)", GREEN, 20, anchor="start")
    s.circle(cx, cy, 5, INK, INK); s.text(cx - 10, cy - 12, "(0,0) top-left", INK, 16, anchor="start")
    th = 40
    ex, ey = cx + 230 * math.cos(math.radians(th)), cy + 230 * math.sin(math.radians(th))
    s.arrow(cx, cy, ex, ey, ORANGE, 4)
    s.arc(cx, cy, 90, 0, th, PURPLE, 3, arrow=True)
    s.text(cx + 105, cy + 50, "θ looks clockwise", PURPLE, 18, anchor="start")
    s.text(ex + 5, ey + 25, "Vector2.from_angle(θ) = (cos θ, sin θ)", ORANGE, 17, anchor="middle")
    s.save("trig_godot2d.svg")


def trig_hsv():
    s = SVG(720, 450)
    cx, cy, r0, r1 = 240, 180, 60, 140
    n = 72
    for i in range(n):
        a0, a1 = 360 * i / n - 90, 360 * (i + 1) / n - 90 + 0.6
        pts = []
        for a in (a0, a1):
            pts.append((cx + r1 * math.cos(math.radians(a)), cy + r1 * math.sin(math.radians(a))))
        for a in (a1, a0):
            pts.append((cx + r0 * math.cos(math.radians(a)), cy + r0 * math.sin(math.radians(a))))
        s.poly(pts, hexcol(i / n), hexcol(i / n), 0.5)
    for h, lab in [(0, "0 / 0°  red"), (1 / 3, "0.33 / 120° green"), (2 / 3, "0.67 / 240° blue")]:
        a = 360 * h - 90
        x, y = cx + (r1 + 12) * math.cos(math.radians(a)), cy + (r1 + 12) * math.sin(math.radians(a))
        s.text(x + (0 if h == 0 else (8 if h < .5 else -8)), y + (-4 if h == 0 else 18), lab, INK, 15,
               anchor="middle" if h == 0 else ("start" if h < .5 else "end"))
    s.text(cx, cy + 6, "Hue", INK, 22, weight="bold")
    s.text(560, 90, "H = hue (angle round", INK, 17); s.text(560, 112, "the wheel, 0..1)", INK, 17)
    s.text(560, 150, "S = saturation (0 grey .. 1 vivid)", INK, 15)
    s.text(560, 175, "V = value (0 black .. 1 bright)", INK, 15)
    n = 8
    s.text(360, 352, f"Color.from_hsv(float(i) / {n}, 1, 1)", INK, 18, weight="bold")
    for i in range(n):
        x = 72 + i * 72
        s.rect(x, 368, 64, 50, INK, hexcol(i / n), 1)
        s.text(x + 32, 438, f"{i}/{n}", INK, 14)
    s.save("trig_hsv.svg")


def trig_projectile_components():
    s = SVG(660, 320)
    ox, oy, k = 60, 260, 22  # px per m/s
    ux, uy = 20 * math.cos(math.radians(30)), 20 * math.sin(math.radians(30))
    ex, ey = ox + ux * k, oy - uy * k
    s.line(30, oy, 540, oy, GREY, 2)
    s.arrow(ox, oy, ex, oy, BLUE, 4)
    s.arrow(ex, oy, ex, ey, RED, 4)
    s.arrow(ox, oy, ex, ey, GREEN, 5)
    s.arc(ox, oy, 70, -30, 0, ORANGE, 3)
    s.text(ox + 82, oy - 12, "30°", ORANGE, 20, anchor="start", weight="bold")
    s.text((ox + ex) / 2 - 30, (oy + ey) / 2 - 18, "u = 20 m/s", GREEN, 22, weight="bold")
    s.text((ox + ex) / 2, oy + 30, "uₓ = 20 cos 30° = 17.32 m/s", BLUE, 19, weight="bold")
    s.text(ex + 10, (oy + ey) / 2, "uᵧ = 20 sin 30°", RED, 19, anchor="start", weight="bold")
    s.text(ex + 10, (oy + ey) / 2 + 24, "    = 10 m/s", RED, 19, anchor="start", weight="bold")
    s.save("trig_projectile_components.svg")


def trig_circle_spawn():
    s = SVG(460, 460)
    cx, cy, r = 230, 230, 150
    s.circle(cx, cy, r, GRID, w=2, dash="6,6")
    s.circle(cx, cy, 6, INK, INK)
    n = 8
    for i in range(n):
        a = 2 * math.pi * i / n
        x, y = cx + r * math.cos(a), cy - r * math.sin(a)
        s.circle(x, y, 18, INK, hexcol(i / n), 2)
        lx, ly = cx + (r + 45) * math.cos(a), cy - (r + 45) * math.sin(a)
        s.text(lx, ly + 6, f"{int(360 * i / n)}°", INK, 15)
    a = 2 * math.pi * 1 / n
    s.arrow(cx, cy, cx + r * math.cos(a), cy - r * math.sin(a), ORANGE, 3)
    s.text(cx + 40, cy - 70, "r", ORANGE, 22, weight="bold")
    s.text(cx, cy + 40, "angle = TAU * i / n", INK, 18, weight="bold")
    s.text(cx, cy + 65, "pos = (cos, 0, sin) * r", INK, 18)
    s.save("trig_circle_spawn.svg")


def trig_sine():
    s = SVG(620, 280)
    ox, oy, A = 40, 140, 80
    s.line(ox, oy, 600, oy, GREY, 2)
    pts = [(ox + t, oy - A * math.sin(2 * math.pi * t / 260)) for t in range(0, 541)]
    s.polyline(pts, BLUE, 4)
    s.arrow(ox + 65, oy, ox + 65, oy - A, RED, 3)
    s.text(ox + 75, oy - 40, "amplitude", RED, 17, anchor="start")
    s.line(ox, 245, ox + 260, 245, PURPLE, 3); s.line(ox, 237, ox, 253, PURPLE, 3)
    s.line(ox + 260, 237, ox + 260, 253, PURPLE, 3)
    s.text(ox + 130, 270, "period = TAU / frequency", PURPLE, 17)
    s.text(420, 40, "y = base + sin(time * freq) * amp", INK, 18, weight="bold")
    s.save("trig_sine.svg")


# --------------------------------------------------------------------------- VECTORS
def vec_godot_axes():
    s = SVG(660, 470)
    cx, cy = 260, 260
    s.arrow(cx, cy, cx + 200, cy, RED, 5); s.text(cx + 210, cy + 6, "+X  right", RED, 20, anchor="start", weight="bold")
    s.arrow(cx, cy, cx, cy - 180, GREEN, 5); s.text(cx - 10, cy - 165, "+Y  up", GREEN, 20, anchor="end", weight="bold")
    s.arrow(cx, cy, cx - 130, cy + 130, BLUE, 5)
    s.text(cx - 100, cy + 162, "+Z  BACK (towards you)", BLUE, 20, weight="bold")
    s.arrow(cx, cy, cx + 120, cy - 120, BLUE, 4, dash="8,6")
    s.text(cx + 130, cy - 125, "−Z  FORWARD", BLUE, 20, anchor="start", weight="bold")
    s.text(cx + 130, cy - 103, "Vector3.FORWARD = (0,0,−1)", BLUE, 15, anchor="start")
    s.circle(cx, cy, 6, INK, INK)
    s.text(20, 30, "Godot 3D: right-handed, Y up, −Z forward", INK, 20, anchor="start", weight="bold")
    s.text(20, 460, "Unity is left-handed (+Z forward). Godot is like OpenGL/Blender*", GREY, 15, anchor="start")
    s.save("vec_godot_axes.svg")


def vec_add_sub():
    s = SVG(760, 330)
    k = 60
    ox, oy = 50, 280
    a, b = (3, 1), (1, 2.5)
    A = (ox + a[0] * k, oy - a[1] * k)
    AB = (A[0] + b[0] * k, A[1] - b[1] * k)
    s.arrow(ox, oy, *A, BLUE, 4); s.text((ox + A[0]) / 2, (oy + A[1]) / 2 + 26, "a", BLUE, 24, weight="bold")
    s.arrow(*A, *AB, RED, 4); s.text((A[0] + AB[0]) / 2 + 18, (A[1] + AB[1]) / 2, "b", RED, 24, weight="bold")
    s.arrow(ox, oy, *AB, GREEN, 4); s.text((ox + AB[0]) / 2 - 25, (oy + AB[1]) / 2, "a + b", GREEN, 22, weight="bold")
    s.text(170, 30, "Addition: tip to tail", INK, 20, weight="bold")
    # subtraction panel
    ox2 = 420
    P1, P2 = (ox2 + 40, 250), (ox2 + 280, 90)
    O2 = (ox2 + 10, 300)
    s.circle(*O2, 5, INK, INK); s.text(O2[0] + 12, O2[1] + 4, "origin", GREY, 14, anchor="start")
    s.arrow(*O2, *P1, GREY, 2, "5,4"); s.arrow(*O2, *P2, GREY, 2, "5,4")
    s.circle(*P1, 10, BLUE, BLUE); s.text(P1[0] - 5, P1[1] + 32, "me (A)", BLUE, 18, weight="bold")
    s.circle(*P2, 10, RED, RED); s.text(P2[0], P2[1] - 18, "target (B)", RED, 18, weight="bold")
    s.arrow(P1[0], P1[1], P2[0] - 8, P2[1] + 6, GREEN, 4)
    s.text((P1[0] + P2[0]) / 2 - 20, (P1[1] + P2[1]) / 2 - 15, "B − A", GREEN, 22, weight="bold")
    s.text(590, 30, "Subtraction: from A to B = B − A", INK, 20, weight="bold")
    s.save("vec_add_sub.svg")


def vec_normalize():
    s = SVG(560, 340)
    ox, oy, k = 90, 278, 55
    s.circle(ox, oy, k, GREY, w=2, dash="5,5")
    s.arrow(ox, oy, ox + 3 * k, oy - 4 * k, BLUE, 4)
    s.arrow(ox, oy, ox + 0.6 * k, oy - 0.8 * k, RED, 6)
    s.line(ox + 3 * k, oy - 4 * k, ox + 3 * k, oy, GREY, 2, "5,4")
    s.text(ox + 3 * k + 15, oy - 4 * k + 5, "v = (3, 4, 0)", BLUE, 20, anchor="start", weight="bold")
    s.text(ox + 3 * k + 15, oy - 4 * k + 30, "|v| = √(9+16) = 5", BLUE, 18, anchor="start")
    s.text(ox + 0.6 * k + 40, oy - 0.8 * k + 30, "v̂ = v / |v| = (0.6, 0.8, 0)", RED, 18, anchor="start", weight="bold")
    s.text(ox + 0.6 * k + 40, oy - 0.8 * k + 54, "length 1, same direction", RED, 15, anchor="start")
    s.save("vec_normalize.svg")


def vec_dot_fov():
    s = SVG(760, 470)
    cx, cy, R = 300, 330, 270
    a0, a1 = -90 - 60, -90 + 60
    x0, y0 = cx + R * math.cos(math.radians(a0)), cy + R * math.sin(math.radians(a0))
    x1, y1 = cx + R * math.cos(math.radians(a1)), cy + R * math.sin(math.radians(a1))
    s.path(f"M{cx},{cy} L{x0:.1f},{y0:.1f} A{R},{R} 0 0 1 {x1:.1f},{y1:.1f} z", GREEN, "#2e9e44", 2, op=0.15)
    s.arrow(cx, cy, cx, cy - 180, INK, 5)
    s.text(cx + 8, cy - 190, "forward = −basis.z", INK, 18, anchor="start", weight="bold")
    s.arc(cx, cy, 70, -90, -30, ORANGE, 3)
    s.text(cx + 55, cy - 80, "60°", ORANGE, 20, anchor="start", weight="bold")
    s.arc(cx, cy, 70, -150, -90, ORANGE, 3)
    s.text(cx - 75, cy - 80, "60°", ORANGE, 20, anchor="end", weight="bold")
    # player inside
    p = (cx + 0.6 * 200, cy - 0.8 * 200)
    s.arrow(cx, cy, *p, BLUE, 4)
    s.circle(*p, 12, BLUE, BLUE)
    s.text(p[0] + 18, p[1] - 4, "player A: dot = 0.8 → 37°", BLUE, 17, anchor="start", weight="bold")
    s.text(p[0] + 18, p[1] + 18, "ALARM", BLUE, 17, anchor="start", weight="bold")
    q = (cx - 0.94 * 180, cy - 0.34 * 180)
    s.arrow(cx, cy, *q, RED, 3)
    s.circle(*q, 12, RED, RED)
    s.text(q[0] - 60, q[1] + 36, "player B: dot = 0.34 → 70° (outside)", RED, 16, anchor="start")
    r = (cx + 150, cy + 80)
    s.circle(*r, 12, PURPLE, PURPLE)
    s.text(r[0] - 10, r[1] + 32, "behind: dot < 0", PURPLE, 16, anchor="middle")
    s.circle(cx, cy, 14, INK, "#ffd166", 3)
    s.text(380, 460, "cos 60° = 0.5   →   dot > 0.5  ⇔  within 60° of forward (120° cone)", INK, 18, weight="bold")
    s.save("vec_dot_fov.svg")


def vec_dot_values():
    s = SVG(600, 330)
    cx, cy, r = 300, 280, 200
    s.arc(cx, cy, r, -180, 0, GREY, 2, dash="5,5")
    s.arrow(cx, cy, cx + r, cy, INK, 5); s.text(cx + r + 10, cy + 5, "a", INK, 22, anchor="start", weight="bold")
    for deg, c in [(0, GREEN), (60, BLUE), (90, ORANGE), (120, PURPLE), (180, RED)]:
        if deg == 0:
            continue
        x, y = cx + r * math.cos(math.radians(deg)), cy - r * math.sin(math.radians(deg))
        s.arrow(cx, cy, x, y, c, 3)
        lx, ly = cx + (r + 18) * math.cos(math.radians(deg)), cy - (r + 18) * math.sin(math.radians(deg))
        if deg == 180: lx, ly = cx - r, cy + 30
        s.text(lx, ly - 4, f"{deg}°: {math.cos(math.radians(deg)):+.1f}".replace("+0.0", "0").replace("-0.0", "0"),
               c, 18, anchor="middle", weight="bold")
    s.text(cx + r - 10, cy + 30, "0°: +1", GREEN, 18, weight="bold")
    s.text(cx, 320, "a · b for unit vectors = cos θ", INK, 20, weight="bold")
    s.save("vec_dot_values.svg")


def vec_cross():
    s = SVG(560, 440)
    o = (160, 270)
    a = (o[0] + 220, o[1] + 40)
    b = (o[0] + 110, o[1] - 90 + 140 - 160 + 60)
    b = (o[0] + 90, o[1] + 90)
    pa = [o, a, (a[0] + b[0] - o[0], a[1] + b[1] - o[1]), b]
    s.poly(pa, GREY, "#cfe0ff", 1, 0.6)
    s.arrow(*o, *a, BLUE, 4); s.text(a[0] + 5, a[1] + 24, "a", BLUE, 24, weight="bold")
    s.arrow(*o, *b, RED, 4); s.text(b[0] - 18, b[1] + 18, "b", RED, 24, weight="bold")
    s.arrow(*o, o[0], o[1] - 200, GREEN, 5)
    s.text(o[0] + 10, o[1] - 190, "a × b", GREEN, 24, anchor="start", weight="bold")
    s.text(o[0] + 10, o[1] - 168, "perpendicular to both", GREEN, 16, anchor="start")
    s.text(o[0] + 10, o[1] - 145, "|a × b| = |a||b| sin θ", GREEN, 16, anchor="start")
    s.text(o[0] + 10, o[1] - 125, "= area of the parallelogram", GREEN, 16, anchor="start")
    s.text(280, 24, "Right hand rule: fingers a → b, thumb = a × b", INK, 18, weight="bold")
    s.text(280, 430, "b × a = −(a × b)   (order matters!)", INK, 18)
    s.save("vec_cross.svg")


def vec_basis():
    s = SVG(560, 460)
    cx, cy, L = 280, 250, 150
    for i in range(-5, 6):
        s.line(cx + i * 50, 40, cx + i * 50, 440, GRID, 1)
        s.line(30, cy + i * 40, 530, cy + i * 40, GRID, 1)
    s.arrow(30, cy, 530, cy, GREY, 2); s.text(520, cy - 8, "+X", GREY, 16)
    s.arrow(cx, 40, cx, 440, GREY, 2); s.text(cx + 10, 435, "+Z", GREY, 16, anchor="start")
    th = math.radians(30)
    fwd = (-math.sin(th), -math.cos(th))   # -basis.z in (x,z)
    bx = (math.cos(th), -math.sin(th))     # basis.x in (x,z)
    bz = (math.sin(th), math.cos(th))
    def scr(v, l=L):
        return cx + v[0] * l, cy + v[1] * l
    box = [(-0.25, -0.4), (0.25, -0.4), (0.25, 0.4), (-0.25, 0.4)]
    pts = []
    for x, z in box:
        rx = x * math.cos(th) + z * math.sin(th)
        rz = -x * math.sin(th) + z * math.cos(th)
        pts.append((cx + rx * 120, cy + rz * 120))
    s.poly(pts, INK, "#ffd166", 2)
    s.arrow(cx, cy, *scr(fwd), BLUE, 5)
    s.text(scr(fwd)[0] - 10, scr(fwd)[1] - 12, "−basis.z  (forward)", BLUE, 18, anchor="middle", weight="bold")
    s.arrow(cx, cy, *scr(bx), RED, 5)
    s.text(scr(bx)[0] + 8, scr(bx)[1] - 6, "basis.x (right)", RED, 18, anchor="start", weight="bold")
    s.arrow(cx, cy, *scr(bz, 100), BLUE, 3, dash="6,4")
    s.text(scr(bz, 100)[0] + 8, scr(bz, 100)[1] + 18, "basis.z (back)", BLUE, 16, anchor="start")
    s.text(280, 25, "Top-down view (looking down −Y). Node yawed 30° (rotation.y = 30°)", INK, 16, weight="bold")
    s.save("vec_basis.svg")


def vec_hierarchy():
    s = SVG(820, 400)
    def tank(x, y, ang, col):
        a = math.radians(ang)
        pts = []
        for px, py in [(-40, -25), (40, -25), (40, 25), (-40, 25)]:
            pts.append((x + px * math.cos(a) - py * math.sin(a), y + px * math.sin(a) + py * math.cos(a)))
        s.poly(pts, INK, col, 2)
        bx, by = x + 70 * math.cos(a), y + 70 * math.sin(a)
        s.line(x, y, bx, by, INK, 7)
        return bx, by
    s.text(200, 30, "Bullet is a CHILD of the tank", RED, 20, weight="bold")
    m = tank(110, 230, -20, "#a3c4f3")
    s.circle(m[0] + 120, m[1] - 44, 8, RED, RED)
    s.text(m[0] + 120, m[1] - 60, "fired", RED, 14)
    m2 = tank(110, 230, 50, "#a3c4f3")
    s.circle(110 + 140 * math.cos(math.radians(50)) + 30, 230 + 140 * math.sin(math.radians(50)), 8, RED, RED)
    s.arc(110, 230, 150, -20, 50, RED, 2, arrow=True, dash="6,4")
    s.text(200, 375, "tank turns → bullet swings round with it ✗", RED, 17)
    s.line(410, 40, 410, 390, GRID, 2)
    s.text(620, 30, "Bullet is a child of the tank's PARENT", GREEN, 20, weight="bold")
    tank(520, 230, -20, "#b7e4c7")
    tank(520, 230, 50, "#b7e4c7")
    bx, by = 520 + 70 * math.cos(math.radians(-20)), 230 + 70 * math.sin(math.radians(-20))
    for i in range(1, 4):
        s.circle(bx + i * 60 * math.cos(math.radians(-20)), by + i * 60 * math.sin(math.radians(-20)), 8, GREEN, GREEN)
    s.arrow(bx + 200 * math.cos(math.radians(-20)), by + 200 * math.sin(math.radians(-20)),
            bx + 260 * math.cos(math.radians(-20)), by + 260 * math.sin(math.radians(-20)), GREEN, 3)
    s.text(620, 375, "bullet keeps its own path ✓", GREEN, 17)
    s.save("vec_hierarchy.svg")


def vec_transform_chain():
    s = SVG(760, 260)
    boxes = [("World (root)", 20, "#eee"), ("Tank", 200, "#a3c4f3"), ("Turret", 380, "#b7e4c7"),
             ("Muzzle (Marker3D)", 560, "#ffd166")]
    for lab, x, col in boxes:
        s.rect(x, 60, 170, 60, INK, col, 2, rx=10)
        s.text(x + 85, 97, lab, INK, 17, weight="bold")
    for i in range(3):
        s.arrow(boxes[i][1] + 170, 90, boxes[i + 1][1], 90, INK, 2)
    s.text(380, 170, "muzzle.global_transform =", INK, 18, weight="bold")
    s.text(380, 200, "tank.transform * turret.transform * muzzle.transform", INK, 18)
    s.text(380, 240, "global_* needs the parents → node must be inside the tree", RED, 17, weight="bold")
    s.save("vec_transform_chain.svg")


def vec_lerp():
    s = SVG(720, 300)
    A, B = (60, 80), (660, 80)
    s.line(*A, *B, GREY, 2)
    for i in range(5):
        t = i / 4
        x = A[0] + (B[0] - A[0]) * t
        s.circle(x, A[1], 10, BLUE, BLUE if i in (0, 4) else "white", 3)
        s.text(x, A[1] - 22, f"t = {t:g}", BLUE, 16)
    s.text(360, 140, "lerp(a, b, t) = a + (b − a) · t      (t from 0 to 1 → constant speed)", INK, 17, weight="bold")
    # exponential
    y = 210
    s.line(60, y, 660, y, GREY, 2)
    x, tx, k = 60, 660, 0.35
    for i in range(9):
        s.circle(x, y, 8, ORANGE, "white" if 0 < i else ORANGE, 3)
        nx = x + (tx - x) * k
        if i < 8:
            s.arrow(x + 8, y + 22, nx - 4, y + 22, ORANGE, 2)
        x = nx
    s.circle(660, y, 10, RED, RED)
    s.text(360, 280, "pos = pos.lerp(target, k·delta) every frame → fast then slow (ease out)", INK, 17, weight="bold")
    s.save("vec_lerp.svg")


# --------------------------------------------------------------------------- QUATERNIONS
def quat_ypr():
    s = SVG(720, 420)
    cx, cy = 310, 230
    # aircraft-ish body (top/side pseudo 3D)
    s.poly([(cx - 150, cy + 10), (cx + 140, cy - 30), (cx + 170, cy - 25), (cx - 120, cy + 30)], INK, "#dfe6e9", 2)
    s.poly([(cx - 10, cy - 5), (cx - 90, cy - 110), (cx - 50, cy - 110), (cx + 50, cy - 15)], INK, "#b2bec3", 2)
    s.poly([(cx - 10, cy + 20), (cx + 40, cy + 120), (cx + 80, cy + 120), (cx + 50, cy + 10)], INK, "#b2bec3", 2)
    s.arrow(cx, cy, cx, cy - 170, GREEN, 4); s.text(cx + 10, cy - 175, "Y: YAW (turn left/right)", GREEN, 18, anchor="start", weight="bold")
    s.arrow(cx, cy, cx + 230, cy - 50, BLUE, 4); s.text(cx + 235, cy - 52, "−Z: ROLL", BLUE, 18, anchor="start", weight="bold")
    s.arrow(cx, cy, cx - 120, cy + 140, RED, 4); s.text(cx - 125, cy + 165, "X: PITCH (nose up/down)", RED, 18, weight="bold")
    s.path(f"M{cx - 40},{cy - 140} A40,12 0 1 0 {cx + 40},{cy - 140}", GREEN, w=3, arrow=True)
    s.save("quat_ypr.svg")


def quat_gimbal():
    s = SVG(760, 360)
    def rings(cx, locked):
        s.circle(cx, 180, 140, RED, w=7)
        if locked:
            s.circle(cx, 180, 115, GREEN, w=7)
            s.path(f"M{cx - 95},180 A95,40 0 1 0 {cx + 95},180 A95,40 0 1 0 {cx - 95},180", BLUE, w=7)
        else:
            s.path(f"M{cx - 120},180 A120,45 0 1 0 {cx + 120},180 A120,45 0 1 0 {cx - 120},180", GREEN, w=7)
            s.path(f"M{cx},85 A35,95 0 1 0 {cx},275 A35,95 0 1 0 {cx},85", BLUE, w=7)
        s.circle(cx, 180, 14, INK, "#ffd166", 2)
    rings(190, False)
    rings(570, True)
    s.text(190, 30, "3 independent axes", INK, 20, weight="bold")
    s.text(570, 30, "pitch = 90°: two rings line up", RED, 20, weight="bold")
    s.text(570, 345, "one degree of freedom lost = GIMBAL LOCK", RED, 18)
    s.text(190, 345, "yaw • pitch • roll", INK, 18)
    s.save("quat_gimbal.svg")


def quat_axis_angle():
    s = SVG(560, 420)
    cx, cy = 280, 250
    s.arrow(cx, cy + 120, cx, cy - 190, PURPLE, 5)
    s.text(cx + 12, cy - 190, "axis (unit vector)", PURPLE, 18, anchor="start", weight="bold")
    s.path(f"M{cx - 140},{cy} A140,45 0 1 0 {cx + 140},{cy}", GREY, w=2, dash="6,5")
    s.path(f"M{cx - 140},{cy} A140,45 0 0 1 {cx + 140},{cy}", GREY, w=2, dash="6,5")
    p0 = (cx + 140 * math.cos(math.radians(120)), cy + 45 * math.sin(math.radians(120)))
    p1 = (cx + 140 * math.cos(math.radians(10)), cy + 45 * math.sin(math.radians(10)))
    s.arrow(cx, cy, *p0, BLUE, 4); s.text(p0[0] - 10, p0[1] + 24, "v", BLUE, 22, weight="bold")
    s.arrow(cx, cy, *p1, GREEN, 4); s.text(p1[0] + 10, p1[1] + 5, "q · v", GREEN, 22, anchor="start", weight="bold")
    s.path(f"M{p0[0]:.1f},{p0[1]:.1f} A140,45 0 0 0 {p1[0]:.1f},{p1[1]:.1f}", ORANGE, w=4, arrow=True)
    s.text(cx + 30, cy + 75, "θ", ORANGE, 26, weight="bold")
    s.text(280, 30, "q = (axis · sin(θ/2),  cos(θ/2))", INK, 20, weight="bold")
    s.text(280, 400, "x, y, z = axis·sin(θ/2)      w = cos(θ/2)", INK, 17)
    s.save("quat_axis_angle.svg")


def quat_slerp():
    s = SVG(700, 420)
    cx, cy, r = 80, 370, 320
    s.arc(cx, cy, r, -90, 0, GREY, 2, dash="6,5")
    q1 = (cx + r, cy); q2 = (cx, cy - r)
    s.line(*q1, *q2, ORANGE, 2)
    for i in range(5):
        t = i / 4
        a = math.radians(90 * t)
        p = (cx + r * math.cos(a), cy - r * math.sin(a))
        s.arrow(cx, cy, *p, BLUE, 2, op=0.6)
        s.circle(*p, 9, BLUE, BLUE)
        l = ((1 - t) * q1[0] + t * q2[0], (1 - t) * q1[1] + t * q2[1])
        s.circle(*l, 7, ORANGE, "white", 3)
        if 0 < i < 4:
            s.text(p[0] + 14, p[1] - 6, f"t={t:g}", BLUE, 15, anchor="start")
    s.circle(cx, cy, 5, INK, INK)
    s.text(q1[0] - 10, q1[1] + 30, "q1", INK, 22, weight="bold")
    s.text(q2[0] - 25, q2[1] + 5, "q2", INK, 22, weight="bold", anchor="end")
    s.text(470, 90, "slerp: equal ANGLES", BLUE, 19, anchor="start", weight="bold")
    s.text(470, 115, "constant rotation speed", BLUE, 16, anchor="start")
    s.text(470, 230, "lerp: cuts the corner,", ORANGE, 17, weight="bold", anchor="start")
    s.text(470, 252, "uneven angles,", ORANGE, 17, anchor="start")
    s.text(470, 274, "result not unit length", ORANGE, 17, anchor="start")
    s.save("quat_slerp.svg")


def quat_turret_turn():
    s = SVG(620, 380)
    cx, cy = 140, 300
    s.circle(cx, cy, 30, INK, "#ffd166", 3)
    tx, ty = 540, 90
    s.circle(tx, ty, 22, RED, RED); s.text(tx, ty - 32, "tank", RED, 18, weight="bold")
    target = math.degrees(math.atan2(ty - cy, tx - cx))
    a = -90.0
    for i in range(8):
        x, y = cx + 170 * math.cos(math.radians(a)), cy + 170 * math.sin(math.radians(a))
        s.arrow(cx, cy, x, y, BLUE, 3, op=0.3 + 0.09 * i)
        a = a + (target - a) * 0.35
    s.arrow(cx, cy, cx + 230 * math.cos(math.radians(target)), cy + 230 * math.sin(math.radians(target)), GREEN, 3, "6,5")
    s.text(cx - 20, cy - 190, "frame 0", BLUE, 15)
    s.text(330, 360, "each frame: q = current.slerp(desired, turn_speed · delta)", INK, 17, weight="bold")
    s.save("quat_turret_turn.svg")


# --------------------------------------------------------------------------- PHYSICS
def phys_timestep():
    s = SVG(820, 260)
    s.text(20, 40, "_process (every rendered frame — irregular)", BLUE, 18, anchor="start", weight="bold")
    t = 0
    xs = [0, 11, 30, 37, 52, 75, 82, 101, 112, 130, 148, 155]
    for x in xs:
        s.line(40 + x * 5, 60, 40 + x * 5, 100, BLUE, 4)
    s.text(20, 150, "_physics_process (fixed, 60 Hz → delta = 1/60 = 0.0167 s)", RED, 18, anchor="start", weight="bold")
    for i in range(0, 13):
        s.line(40 + i * 62, 170, 40 + i * 62, 210, RED, 4)
    s.arrow(40, 235, 800, 235, INK, 2); s.text(790, 255, "time", INK, 16)
    s.save("phys_timestep.svg")


def phys_vt_graph():
    s = SVG(560, 380)
    ox, oy = 70, 320
    s.arrow(ox, oy, ox, 30, INK, 2); s.text(ox - 10, 30, "v", INK, 20, anchor="end")
    s.arrow(ox, oy, 520, oy, INK, 2); s.text(515, oy + 26, "t", INK, 20)
    u, v, T = 100, 250, 380
    s.poly([(ox, oy), (ox + T, oy), (ox + T, oy - u), (ox, oy - u)], BLUE, "#a3c4f3", 2, 0.7)
    s.poly([(ox, oy - u), (ox + T, oy - u), (ox + T, oy - v)], RED, "#f5a3a3", 2, 0.7)
    s.line(ox, oy - u, ox + T, oy - v, INK, 4)
    s.text(ox + T / 2, oy - u / 2 + 6, "A = u·t", BLUE, 20, weight="bold")
    s.text(ox + T * 0.68, oy - u - 30, "B = ½(v−u)·t = ½at²", RED, 18, weight="bold")
    s.text(ox - 8, oy - u + 5, "u", INK, 20, anchor="end"); s.text(ox - 8, oy - v + 5, "v", INK, 20, anchor="end")
    s.text(ox + T, oy + 26, "t", INK, 18)
    s.text(300, 370, "distance = area under graph:  s = ut + ½at²", INK, 18, weight="bold")
    s.save("phys_vt_graph.svg")


def phys_projectile():
    s = SVG(820, 380)
    ox, oy, kx, ky = 50, 320, 20, 40
    u, g, ang = 20.0, 9.8, math.radians(30)
    ux, uy = u * math.cos(ang), u * math.sin(ang)
    T = 2 * uy / g
    pts = []
    for i in range(101):
        t = T * i / 100
        pts.append((ox + ux * t * kx, oy - (uy * t - 0.5 * g * t * t) * ky))
    s.line(20, oy, 800, oy, GREY, 2)
    # drag version (linear drag k)
    k = 0.15
    vx, vy, x, y, dpts = ux, uy, 0.0, 0.0, []
    dt = 0.001
    while True:
        dpts.append((ox + x * kx, oy - y * ky))
        ax, ay = -k * vx, -g - k * vy
        vx += ax * dt; vy += ay * dt; x += vx * dt; y += vy * dt
        if y < 0:
            break
    s.polyline(dpts, ORANGE, 3, "8,6")
    s.polyline(pts, BLUE, 4)
    tp = uy / g
    px, py = ox + ux * tp * kx, oy - (uy * tp - 0.5 * g * tp * tp) * ky
    s.line(px, py, px, oy, GREY, 2, "5,4")
    s.circle(px, py, 7, RED, RED)
    s.text(px, py - 18, f"peak: t = {tp:.2f} s, h = {uy * uy / (2 * g):.2f} m", RED, 17, weight="bold")
    R = ux * T
    s.circle(ox + R * kx, oy, 7, GREEN, GREEN)
    s.text(ox + R * kx + 10, oy + 28, f"lands: t = {T:.2f} s, x = {R:.1f} m", GREEN, 17, anchor="end", weight="bold")
    for t in [0, tp, T]:
        x = ox + ux * t * kx; y = oy - (uy * t - 0.5 * g * t * t) * ky
        vyy = uy - g * t
        s.arrow(x, y, x + ux * 3.5, y, BLUE, 2)
        if abs(vyy) > 0.1:
            s.arrow(x, y, x, y - vyy * 3.5, RED, 2)
    s.text(dpts[-1][0] - 10, oy - 20, "with air", ORANGE, 16, anchor="end")
    s.text(410, 30, "u = 20 m/s at 30°, g = 9.8 m/s²  (blue: horizontal v constant, red: vertical v changes)", INK, 15)
    s.save("phys_projectile.svg")


def phys_euler():
    s = SVG(780, 400)
    ox, oy, kx, ky = 70, 340, 480, 55
    s.arrow(ox, oy, ox, 30, INK, 2); s.text(ox - 8, 40, "height (m)", INK, 15, anchor="end")
    s.arrow(ox, oy, 600, oy, INK, 2); s.text(590, oy + 26, "t (s)", INK, 15)
    for h in range(0, 6):
        s.line(ox - 5, oy - h * ky, ox, oy - h * ky, INK, 2); s.text(ox - 10, oy - h * ky + 5, str(h), INK, 14, anchor="end")
    for t in (0.5, 1.0):
        s.text(ox + t * kx, oy + 22, f"{t}", INK, 14)
    ex = [(ox + t / 100 * kx, oy - (10 * t / 100 - 4.9 * (t / 100) ** 2) * ky) for t in range(101)]
    s.polyline(ex, GREEN, 4)
    def euler(dt):
        v, y, out = 10.0, 0.0, [(0, 0)]
        n = int(round(1 / dt))
        for i in range(n):
            v -= 9.8 * dt; y += v * dt
            out.append(((i + 1) * dt, y))
        return out
    for dt, c in [(0.5, RED), (0.1, ORANGE)]:
        e = euler(dt)
        s.polyline([(ox + t * kx, oy - y * ky) for t, y in e], c, 3, "7,5")
        for t, y in e:
            s.circle(ox + t * kx, oy - y * ky, 5, c, c)
    s.text(ox + kx + 10, oy - 5.1 * ky + 5, "exact 5.10 m", GREEN, 16, anchor="start", weight="bold")
    s.text(ox + kx + 10, oy - euler(0.1)[-1][1] * ky + 5, f"Δt=0.1 → {euler(0.1)[-1][1]:.2f} m", ORANGE, 16, anchor="start", weight="bold")
    s.text(ox + kx + 10, oy - 2.65 * ky + 5, "Δt=0.5 → 2.65 m", RED, 16, anchor="start", weight="bold")
    s.text(320, 390, "Smaller time step → smaller error", INK, 17, weight="bold")
    s.save("phys_euler.svg")


def phys_torque():
    s = SVG(880, 380)
    # panel 1 central force
    def box(cx, cy, col):
        s.rect(cx - 60, cy - 60, 120, 120, INK, col, 2)
        s.circle(cx, cy, 6, INK, INK)
    box(170, 210, "#a3c4f3")
    s.arrow(170, 210, 310, 210, RED, 5)
    s.text(240, 195, "F", RED, 22, weight="bold")
    s.text(170, 40, "apply_central_force(F)", INK, 19, weight="bold")
    s.text(170, 320, "moves, no spin (torque = 0)", INK, 17)
    s.line(410, 30, 410, 360, GRID, 2)
    # panel 2 offset force
    cx, cy = 600, 230
    box(cx, cy, "#b7e4c7")
    s.arrow(cx, cy, cx, cy - 60, BLUE, 4)
    s.text(cx - 68, cy - 25, "r = (0, 0.5, 0)", BLUE, 16, anchor="end", weight="bold")
    s.arrow(cx, cy - 60, cx + 130, cy - 60, RED, 5)
    s.text(cx + 70, cy - 105, "F = (10, 0, 0)", RED, 17, weight="bold")
    s.arc(cx, cy, 95, -150, -20, PURPLE, 3, arrow=True)
    s.circle(cx + 95, cy + 20, 16, PURPLE, "white", 3)
    s.line(cx + 84, cy + 9, cx + 106, cy + 31, PURPLE, 3); s.line(cx + 106, cy + 9, cx + 84, cy + 31, PURPLE, 3)
    s.text(cx + 75, cy + 62, "τ = (0, 0, −5) N·m", PURPLE, 17, anchor="start", weight="bold")
    s.text(cx + 75, cy + 82, "into screen (−Z)", PURPLE, 14, anchor="start")
    s.text(cx, 40, "apply_force(F, r)", INK, 19, weight="bold")
    s.text(cx, 360, "moves AND spins clockwise:  τ = r × F", INK, 17)
    s.save("phys_torque.svg")


def phys_seek():
    s = SVG(620, 380)
    p = (120, 280)
    t = (520, 90)
    s.circle(*t, 16, RED, RED); s.text(t[0], t[1] - 26, "target", RED, 18, weight="bold")
    s.poly([(p[0] - 15, p[1] + 12), (p[0] + 22, p[1]), (p[0] - 15, p[1] - 12)], INK, "#ffd166", 2)
    v = (p[0] + 230, p[1] - 10)
    s.arrow(*p, *v, BLUE, 4); s.text(v[0] + 8, v[1] + 20, "velocity", BLUE, 18, anchor="start", weight="bold")
    d = (t[0] - p[0], t[1] - p[1]); L = math.hypot(*d); d = (p[0] + d[0] / L * 240, p[1] + d[1] / L * 240)
    s.arrow(*p, *d, GREEN, 4); s.text(d[0] - 130, d[1] - 10, "desired", GREEN, 18, anchor="start", weight="bold")
    s.arrow(*v, *d, PURPLE, 4, dash="7,5")
    s.text((v[0] + d[0]) / 2 + 12, (v[1] + d[1]) / 2 + 10, "steering = desired − velocity", PURPLE, 17, anchor="start", weight="bold")
    s.text(310, 365, "desired = (target − pos).normalized() * max_speed", INK, 16)
    s.save("phys_seek.svg")


def phys_wall():
    s = SVG(820, 340)
    rows, cols, sz, gap = 4, 6, 44, 6
    ox, oy = 40, 280
    for r in range(rows):
        for c in range(cols):
            s.rect(ox + c * (sz + gap), oy - (r + 1) * (sz + gap) + gap, sz, sz, INK, hexcol((c + r * cols) / (rows * cols)), 2)
    s.line(20, oy + 2, 360, oy + 2, INK, 3)
    s.text(180, 30, f"Wall: rows = {rows}, cols = {cols}", INK, 19, weight="bold")
    s.text(180, 320, "pos = (col * step, row * step + 0.5, 0)", INK, 16)
    s.line(410, 20, 410, 330, GRID, 2)
    layers = 5
    ox2 = 620
    for y in range(layers):
        n = layers - y
        off = (n - 1) * (sz + gap) / 2
        for x in range(n):
            s.rect(ox2 - off + x * (sz + gap) - sz / 2, oy - (y + 1) * (sz + gap) + gap, sz, sz, INK, hexcol(y / layers, .6), 2)
    s.line(430, oy + 2, 810, oy + 2, INK, 3)
    s.circle(ox2, oy + 2, 6, RED, RED)
    s.text(ox2, 30, "Pyramid: each layer one narrower, centred", INK, 19, weight="bold")
    s.text(ox2, 320, "offset = (n − 1) * step / 2", INK, 16)
    s.save("phys_wall.svg")


def phys_joints():
    s = SVG(900, 330)
    # pin
    s.text(150, 30, "PinJoint3D", INK, 20, weight="bold")
    pts = [(150, 70)]
    for i in range(4):
        pts.append((150 + (i + 1) * 28, 70 + (i + 1) * 45))
    for i in range(len(pts) - 1):
        s.line(*pts[i], *pts[i + 1], GREY, 10)
    for p in pts[1:]:
        s.circle(*p, 8, RED, "white", 3)
    s.rect(120, 55, 60, 14, INK, "#555")
    s.text(150, 300, "point — free rotation", INK, 15); s.text(150, 320, "chains, ropes, wrecking balls", GREY, 14)
    # hinge
    s.text(450, 30, "HingeJoint3D", INK, 20, weight="bold")
    s.rect(380, 60, 12, 200, INK, "#555")
    s.poly([(392, 70), (520, 100), (520, 280), (392, 250)], INK, "#a3c4f3", 2)
    s.line(386, 50, 386, 275, PURPLE, 3, "6,4")
    s.arc(386, 160, 80, -30, 30, PURPLE, 3, arrow=True)
    s.text(450, 300, "one axis — doors, wheels", INK, 15); s.text(450, 320, "limits + motor", GREY, 14)
    # slider
    s.text(750, 30, "SliderJoint3D", INK, 20, weight="bold")
    s.rect(620, 160, 260, 14, INK, "#555")
    s.rect(700, 130, 70, 70, INK, "#b7e4c7", 2)
    s.arrow(720, 230, 650, 230, PURPLE, 3); s.arrow(750, 230, 830, 230, PURPLE, 3)
    s.text(750, 300, "slides along one axis", INK, 15); s.text(750, 320, "pistons, lifts, drawers", GREY, 14)
    s.save("phys_joints.svg")


def phys_raycast():
    s = SVG(760, 330)
    T = (90, 170)
    s.circle(*T, 30, INK, "#ffd166", 3); s.text(T[0], T[1] + 55, "turret", INK, 17)
    s.rect(330, 40, 30, 120, INK, "#7f8c8d", 2); s.text(345, 30, "wall", INK, 16)
    a = (640, 70); b = (640, 270)
    s.circle(*a, 22, RED, RED); s.text(a[0] + 30, a[1] + 5, "tank A", RED, 17, anchor="start")
    s.circle(*b, 22, GREEN, GREEN); s.text(b[0] + 30, b[1] + 5, "tank B", GREEN, 17, anchor="start")
    hit = (330, T[1] + (a[1] - T[1]) * (330 - T[0]) / (a[0] - T[0]))
    s.line(*T, *hit, RED, 3); s.line(*hit, *a, RED, 2, "4,6", op=0.5)
    s.text(*hit, "", RED)
    s.add(f'<text x="{hit[0] - 6}" y="{hit[1] + 6}" font-size="28" fill="{RED}" text-anchor="end">✕</text>')
    s.arrow(*T, b[0] - 22, b[1] - 5, GREEN, 3)
    s.text(470, 315, "first hit == target → line of sight → fire", INK, 17, weight="bold")
    s.text(250, 250, "first hit = wall → don't fire", RED, 16)
    s.save("phys_raycast.svg")


def tween_easing():
    s = SVG(860, 260)
    def plot(x0, title, f, col):
        w, h, y0 = 170, 150, 200
        s.rect(x0, y0 - h, w, h, GRID, "none", 1)
        s.polyline([(x0 + w * i / 100, y0 - h * f(i / 100)) for i in range(101)], col, 4)
        s.text(x0 + w / 2, y0 + 30, title, INK, 15, weight="bold")
    plot(20, "TRANS_LINEAR", lambda t: t, GREY)
    plot(230, "QUAD, EASE_IN", lambda t: t * t, BLUE)
    plot(440, "QUAD, EASE_OUT", lambda t: 1 - (1 - t) ** 2, GREEN)
    def bounce(t):
        n, d = 7.5625, 2.75
        if t < 1 / d: return n * t * t
        if t < 2 / d: t -= 1.5 / d; return n * t * t + .75
        if t < 2.5 / d: t -= 2.25 / d; return n * t * t + .9375
        t -= 2.625 / d; return n * t * t + .984375
    plot(650, "BOUNCE, EASE_OUT", bounce, ORANGE)
    s.text(430, 25, "set_trans = shape of the curve   ·   set_ease = which end it is applied to", INK, 17, weight="bold")
    s.save("tween_easing.svg")


def coin_tween():
    s = SVG(640, 300)
    ox, oy, kx, ky = 70, 250, 300, 90
    s.arrow(ox, oy, ox, 30, INK, 2); s.text(ox - 8, 40, "scale", INK, 16, anchor="end")
    s.arrow(ox, oy, 580, oy, INK, 2); s.text(575, oy + 26, "t (s)", INK, 16)
    for v in (1, 2):
        s.text(ox - 10, oy - v * ky + 5, str(v), INK, 15, anchor="end"); s.line(ox - 5, oy - v * ky, ox, oy - v * ky, INK, 2)
    eo = lambda t: 1 - (1 - t) ** 2
    p1 = [(ox + t / 100 * kx, oy - (1 + eo(t / 100)) * ky) for t in range(101)]
    p2 = [(ox + kx + t / 100 * 0.5 * kx, oy - 2 * (1 - eo(t / 100)) * ky) for t in range(101)]
    s.polyline(p1 + p2, GREEN, 4)
    s.line(ox + kx, oy, ox + kx, oy - 2 * ky, GREY, 1, "4,4")
    s.text(ox + kx, oy + 22, "1.0", INK, 14); s.text(ox + 1.5 * kx, oy + 22, "1.5", INK, 14)
    s.text(ox + kx / 2, 40, "tween 1: → 2×, 1 s", GREEN, 16)
    s.text(ox + 1.25 * kx + 10, 70, "tween 2: → 0, 0.5 s", GREEN, 16, anchor="start")
    s.circle(ox + 1.5 * kx, oy, 7, RED, RED)
    s.text(ox + 1.5 * kx + 10, oy - 12, "queue_free", RED, 16, anchor="start", weight="bold")
    s.save("coin_tween.svg")


if __name__ == "__main__":
    for f in [trig_right_triangle, trig_unit_circle, trig_bearing_210, trig_godot2d, trig_hsv,
              trig_projectile_components, trig_circle_spawn, trig_sine,
              vec_godot_axes, vec_add_sub, vec_normalize, vec_dot_fov, vec_dot_values, vec_cross,
              vec_basis, vec_hierarchy, vec_transform_chain, vec_lerp,
              quat_ypr, quat_gimbal, quat_axis_angle, quat_slerp, quat_turret_turn,
              phys_timestep, phys_vt_graph, phys_projectile, phys_euler, phys_torque, phys_seek,
              phys_wall, phys_joints, phys_raycast, tween_easing, coin_tween]:
        f()
