"""Les trois symboles retenus, en SVG (carre de 96 sur 96, centre 48 48)."""
import math
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from geo import f, arc, hexagone  # noqa: E402

C = 48
S3 = math.sqrt(3)


# ---------- 1. Points : 19 points en hexagone, leur taille dessine un champ ----------
def trame(s=17.4, rmin=2.7, rmax=7.0, pic=(1.05, -0.85), sigma=1.55):
    ronds = []
    for q in range(-2, 3):
        for r in range(-2, 3):
            if abs(q + r) > 2:
                continue
            u, v = S3 / 2 * r, q + r / 2  # u vers la droite, v vers le bas
            d = math.hypot(u - pic[0], v - pic[1])
            k = math.exp(-d * d / (2 * sigma * sigma))
            ronds.append((C + u * s, C + v * s, rmin + (rmax - rmin) * k, d))
    return ronds


def points(petit=False, anime=False):
    ronds = trame(rmin=4.3, rmax=7.0) if petit else trame()
    out = ""
    for x, y, r, d in ronds:
        if anime:
            out += f'<circle class="pt" style="--d:{round(d * 170)}" cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>'
        else:
            out += f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}"/>'
    return out


# ---------- 2. Zone : une zone de la carte qui se remplit de mesures ----------
ZR, ZCOIN, ZTRAIT = 39.5, 7.5, 6.4
NIVEAU, AMPL, LONG = 55.5, 5.0, 62.0


def vague(x0=-45.5, x1=170.0, y=NIVEAU, a=AMPL, lg=LONG, bas=100):
    d = f"M{f(x0)} {f(y)}"
    x = x0
    d += f"Q{f(x + lg / 4)} {f(y - 2 * a)} {f(x + lg / 2)} {f(y)}"
    x += lg / 2
    while x < x1:
        x += lg / 2
        d += f"T{f(x)} {f(y)}"
    return d + f"V{bas}H{f(x0)}Z"


# Boite du symbole dans le carre de 96 (bord exterieur du trait)
Z_GAUCHE, Z_HAUT, Z_LARGEUR, Z_HAUTEUR = 10.59, 7.47, 74.82, 81.07


def zone_chemins():
    """Les trois chemins du symbole : contour, interieur (decoupe) et vague (remplissage)."""
    return hexagone(C, C, ZR, arrondi=ZCOIN), hexagone(C, C, ZR - 0.5, arrondi=ZCOIN), vague(x1=104)


def zone(anime=False, ident="z", contour="currentColor", rempli=None):
    hx, interieur, vg = zone_chemins()
    clip = f'<clipPath id="{ident}-clip"><path d="{interieur}"/></clipPath>'
    couleur = f' fill="{rempli}"' if rempli else ""
    if anime:
        bloc = (f'<g clip-path="url(#{ident}-clip)"><g class="z-niveau">'
                f'<path class="z-vague"{couleur} d="{vague()}"/></g></g>')
        trait = (f'<path class="z-contour" pathLength="1" d="{hx}" fill="none" stroke="{contour}" '
                 f'stroke-width="{ZTRAIT}" stroke-linejoin="round"/>')
    else:
        bloc = f'<g clip-path="url(#{ident}-clip)"><path{couleur} d="{vg}"/></g>'
        trait = f'<path d="{hx}" fill="none" stroke="{contour}" stroke-width="{ZTRAIT}" stroke-linejoin="round"/>'
    return f"<defs>{clip}</defs>{bloc}{trait}"


# ---------- 3. Onde : un S en forme d'onde, et le point qui mesure ----------
ORX, ORY, OTRAIT = 21.0, 16.2, 10.4
T_HAUT, T_BAS, T_POINT, OPOINT = -36.0, 142.0, 14.0, 6.3


def _ell(cx, cy, t):
    return cx + ORX * math.cos(math.radians(t)), cy + ORY * math.sin(math.radians(t))


def onde_chemin():
    """Du bas vers le haut : le trait finit pres du point."""
    haut, bas = (C, C - ORY), (C, C + ORY)
    x0, y0 = _ell(*bas, T_BAS)
    x2, y2 = _ell(*haut, T_HAUT)
    return (f"M{f(x0)} {f(y0)}A{f(ORX)} {f(ORY)} 0 1 0 {C} {C}"
            f"A{f(ORX)} {f(ORY)} 0 1 1 {f(x2)} {f(y2)}")


def onde_point():
    return _ell(C, C - ORY, T_POINT)


def onde(anime=False):
    px, py = onde_point()
    d = onde_chemin()
    if anime:
        return (f'<circle class="o-cercle" cx="{f(px)}" cy="{f(py)}" r="{f(OPOINT)}" fill="none" stroke="currentColor" stroke-width="2.4"/>'
                f'<path class="o-trait" pathLength="1" d="{d}" fill="none" stroke="currentColor" stroke-width="{OTRAIT}" stroke-linecap="round"/>'
                f'<circle class="o-point" cx="{f(px)}" cy="{f(py)}" r="{f(OPOINT)}"/>')
    return (f'<path d="{d}" fill="none" stroke="currentColor" stroke-width="{OTRAIT}" stroke-linecap="round"/>'
            f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(OPOINT)}"/>')


def svg_fichier(corps, couleur="#0e1b2a", fond=None, taille=96):
    rect = f'<rect width="96" height="96" fill="{fond}"/>' if fond else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 96 96" width="{taille}" height="{taille}" '
            f'fill="{couleur}" color="{couleur}">{rect}{corps}</svg>\n')
