"""Petits outils de geometrie pour dessiner les symboles en SVG."""
import math


def f(v):
    s = f"{v:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def courbe_fermee(pts):
    """Courbe lisse fermee (Catmull-Rom) qui passe par tous les points."""
    n = len(pts)
    d = f"M{f(pts[0][0])} {f(pts[0][1])}"
    for i in range(n):
        p0, p1, p2, p3 = pts[(i - 1) % n], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
        d += f"C{f(c1[0])} {f(c1[1])} {f(c2[0])} {f(c2[1])} {f(p2[0])} {f(p2[1])}"
    return d + "Z"


def champ(x, y, bosses):
    return sum(a * math.exp(-((x - cx) ** 2 + (y - cy) ** 2) / (2 * s * s)) for cx, cy, s, a in bosses)


def isoligne(centre, niveau, bosses, n=24, pas=0.05, rmax=80):
    """Points d'une courbe de niveau, cherches sur des rayons partant du sommet."""
    pts = []
    for k in range(n):
        th = 2 * math.pi * k / n - math.pi / 2
        r = 0.0
        while r < rmax and champ(centre[0] + r * math.cos(th), centre[1] + r * math.sin(th), bosses) > niveau:
            r += pas
        pts.append((centre[0] + r * math.cos(th), centre[1] + r * math.sin(th)))
    return pts


def arc(cx, cy, r, a0, a1):
    """Arc de cercle de a0 a a1 (degres, sens de l'ecran : y vers le bas)."""
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    grand = 1 if abs(a1 - a0) > 180 else 0
    sens = 1 if a1 > a0 else 0
    return f"M{f(x0)} {f(y0)}A{f(r)} {f(r)} 0 {grand} {sens} {f(x1)} {f(y1)}"


def hexagone(cx, cy, r, arrondi=0.0, pointe_en_haut=True):
    """Hexagone regulier, coins arrondis (arrondi = rayon du coin)."""
    dep = -90 if pointe_en_haut else 0
    sommets = [(cx + r * math.cos(math.radians(dep + 60 * i)), cy + r * math.sin(math.radians(dep + 60 * i))) for i in range(6)]
    if arrondi <= 0:
        return "M" + "L".join(f"{f(x)} {f(y)}" for x, y in sommets) + "Z"
    d = ""
    for i in range(6):
        p = sommets[i]
        a = sommets[(i - 1) % 6]
        b = sommets[(i + 1) % 6]
        cote = math.dist(p, a)
        t = arrondi / cote * 1.1547  # recul le long des cotes pour un coin de 120 degres
        pa = (p[0] + (a[0] - p[0]) * t, p[1] + (a[1] - p[1]) * t)
        pb = (p[0] + (b[0] - p[0]) * t, p[1] + (b[1] - p[1]) * t)
        d += ("M" if i == 0 else "L") + f"{f(pa[0])} {f(pa[1])}"
        d += f"Q{f(p[0])} {f(p[1])} {f(pb[0])} {f(pb[1])}"
    return d + "Z"
