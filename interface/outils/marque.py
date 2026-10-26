"""La marque Sensor Maps : couleurs, signatures (symbole et nom) et kit Android."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import symboles as sy  # noqa: E402
from geo import f  # noqa: E402

# ---------- Couleurs : noir et blanc, la couleur seulement pour les mesures ----------
NOIR = "#000000"         # le logo, le texte et les boutons en clair ; le fond en sombre
BLANC = "#ffffff"        # le fond en clair ; le logo, le texte et les boutons en sombre
GRIS = "#5c5c5c"         # texte doux en clair
GRIS_CLAIR = "#a3a3a3"   # texte doux en sombre
SURFACE_CLAIRE = "#f2f2f2"
SURFACE_SOMBRE = "#141414"
DOUX_CLAIR = "#e6e6e6"   # boutons doux en clair
DOUX_SOMBRE = "#262626"  # boutons doux en sombre
TRAIT_CLAIR = "#e3e3e3"
TRAIT_SOMBRE = "#2a2a2a"

# ---------- Le nom en contours ----------
_NOM = None


def nom():
    global _NOM
    if _NOM is None:
        chemin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nom-600.json")
        _NOM = json.load(open(chemin, encoding="utf-8"))
    return _NOM


def symbole(contour, rempli, ident, x=0.0, y=0.0, k=1.0):
    """Le symbole place dans un groupe : coin haut gauche du carre de 96 en (x, y), echelle k."""
    return f'<g transform="translate({f(x)} {f(y)}) scale({f(k)})">{sy.zone(ident=ident, contour=contour, rempli=rempli)}</g>'


def signature_horizontale(contour, rempli, texte, ident, cap=100.0, rapport=1.62, ecart=0.56):
    """Symbole a gauche, nom a droite. Hauteur du symbole = rapport x hauteur des capitales."""
    n = nom()
    h_hex = rapport * cap
    k = h_hex / sy.Z_HAUTEUR
    x_hex = -sy.Z_GAUCHE * k
    y_hex = -sy.Z_HAUT * k
    centre = h_hex / 2
    x_nom = sy.Z_LARGEUR * k + ecart * cap
    e = cap / n["capitale"]
    base = centre + cap / 2
    largeur = x_nom + n["largeur"] * e
    corps = (symbole(contour, rempli, ident, x_hex, y_hex, k)
             + f'<path fill="{texte}" transform="translate({f(x_nom)} {f(base)}) scale({e:.5f})" d="{n["d"]}"/>')
    return corps, largeur, h_hex


def signature_verticale(contour, rempli, texte, ident, cap=100.0, rapport=2.7, ecart=0.62):
    n = nom()
    e = cap / n["capitale"]
    l_nom = n["largeur"] * e
    h_hex = rapport * cap
    k = h_hex / sy.Z_HAUTEUR
    l_hex = sy.Z_LARGEUR * k
    largeur = max(l_nom, l_hex)
    x_hex = (largeur - l_hex) / 2 - sy.Z_GAUCHE * k
    y_hex = -sy.Z_HAUT * k
    base = h_hex + ecart * cap + cap
    desc = -n["descendante"] * e
    hauteur = base + desc
    corps = (symbole(contour, rempli, ident, x_hex, y_hex, k)
             + f'<path fill="{texte}" transform="translate({f((largeur - l_nom) / 2)} {f(base)}) scale({e:.5f})" d="{n["d"]}"/>')
    return corps, largeur, hauteur


def svg(corps, largeur, hauteur, marge=0.0, fond=None, titre="Sensor Maps"):
    l, h = largeur + 2 * marge, hauteur + 2 * marge
    rect = f'<rect x="{f(-marge)}" y="{f(-marge)}" width="{f(l)}" height="{f(h)}" fill="{fond}"/>' if fond else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{f(-marge)} {f(-marge)} {f(l)} {f(h)}" '
            f'width="{f(l)}" height="{f(h)}" role="img" aria-label="{titre}">{rect}{corps}</svg>\n')


# ---------- Variantes du logo : noir sur fond clair, blanc sur fond sombre ----------
VARIANTES = {
    "noir": (NOIR, NOIR, NOIR),
    "blanc": (BLANC, BLANC, BLANC),
}


def fichiers_logo(dossier):
    os.makedirs(dossier, exist_ok=True)
    ecrits = []
    for nom_v, (c, r, t) in VARIANTES.items():
        corps = sy.zone(ident="z", contour=c, rempli=r)
        g = sy.Z_GAUCHE
        ecrits.append((f"symbole-{nom_v}.svg", svg(f'<g transform="translate({-g} {-sy.Z_HAUT})">{corps}</g>', sy.Z_LARGEUR, sy.Z_HAUTEUR)))
        corps, l, h = signature_horizontale(c, r, t, "zh")
        ecrits.append((f"signature-{nom_v}.svg", svg(corps, l, h)))
        corps, l, h = signature_verticale(c, r, t, "zv")
        ecrits.append((f"signature-verticale-{nom_v}.svg", svg(corps, l, h)))
    for n, contenu in ecrits:
        open(os.path.join(dossier, n), "w", encoding="utf-8").write(contenu)
    return [n for n, _ in ecrits]


# ---------- Kit Android ----------
# Icone adaptative : 108 dp, le symbole fait 48 dp de haut, bien dans la zone sure (cercle de 66 dp)
K_ADAPT = 48 / sy.Z_HAUTEUR
DEC_ADAPT = (108 - 96 * K_ADAPT) / 2


def _vd_symbole(contour, rempli, k, dx, dy):
    hx, inter, vg = sy.zone_chemins()
    return (f'  <group android:translateX="{f(dx)}" android:translateY="{f(dy)}" android:scaleX="{k:.5f}" android:scaleY="{k:.5f}">\n'
            f'    <group>\n'
            f'      <clip-path android:pathData="{inter}"/>\n'
            f'      <path android:fillColor="{rempli}" android:pathData="{vg}"/>\n'
            f'    </group>\n'
            f'    <path android:fillColor="#00000000" android:strokeColor="{contour}" android:strokeWidth="{sy.ZTRAIT}"\n'
            f'        android:strokeLineJoin="round" android:pathData="{hx}"/>\n'
            f'  </group>\n')


def _vd(taille_dp, viewport, contenu):
    return ('<?xml version="1.0" encoding="utf-8"?>\n'
            '<vector xmlns:android="http://schemas.android.com/apk/res/android"\n'
            f'    android:width="{taille_dp}dp" android:height="{taille_dp}dp"\n'
            f'    android:viewportWidth="{viewport}" android:viewportHeight="{viewport}">\n'
            f'{contenu}</vector>\n')


def fichiers_android(dossier):
    res = os.path.join(dossier, "res")
    for d in ("drawable", "mipmap-anydpi-v26", "values"):
        os.makedirs(os.path.join(res, d), exist_ok=True)
    w = lambda chemin, txt: open(os.path.join(res, chemin), "w", encoding="utf-8").write(txt)
    w("drawable/ic_launcher_background.xml", _vd(108, 108,
      f'  <path android:fillColor="{NOIR.upper()}" android:pathData="M0,0h108v108h-108z"/>\n'))
    w("drawable/ic_launcher_foreground.xml", _vd(108, 108, _vd_symbole("#FFFFFF", "#FFFFFF", K_ADAPT, DEC_ADAPT, DEC_ADAPT)))
    w("drawable/ic_launcher_monochrome.xml", _vd(108, 108, _vd_symbole("#FFFFFF", "#FFFFFF", K_ADAPT, DEC_ADAPT, DEC_ADAPT)))
    w("drawable/ic_stat_sensor_maps.xml", _vd(24, 96, _vd_symbole("#FFFFFF", "#FFFFFF", 1, 0, 0)))
    adaptive = ('<?xml version="1.0" encoding="utf-8"?>\n'
                '<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n'
                '    <background android:drawable="@drawable/ic_launcher_background"/>\n'
                '    <foreground android:drawable="@drawable/ic_launcher_foreground"/>\n'
                '    <monochrome android:drawable="@drawable/ic_launcher_monochrome"/>\n'
                '</adaptive-icon>\n')
    w("mipmap-anydpi-v26/ic_launcher.xml", adaptive)
    w("mipmap-anydpi-v26/ic_launcher_round.xml", adaptive)
    w("values/couleurs_sensor_maps.xml", (
        '<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'
        f'    <color name="sm_noir">{NOIR.upper()}</color>\n'
        f'    <color name="sm_blanc">{BLANC.upper()}</color>\n'
        f'    <color name="sm_gris">{GRIS.upper()}</color>\n'
        f'    <color name="sm_gris_clair">{GRIS_CLAIR.upper()}</color>\n'
        f'    <color name="ic_launcher_background">{NOIR.upper()}</color>\n'
        '</resources>\n'))


def svg_icone(taille, forme="carre", fond=NOIR, contour=BLANC, rempli=BLANC, k_rel=48 / 72):
    """Icone en SVG pour les PNG : 'carre' plein (Google Play), 'arrondi' ou 'rond' (anciens Android)."""
    s = taille
    if forme == "carre":
        cadre = f'<rect width="{s}" height="{s}" fill="{fond}"/>'
        visible = s
    else:
        marge = s * 0.04
        cote = s - 2 * marge
        rayon = cote / 2 if forme == "rond" else cote * 0.22
        cadre = f'<rect x="{f(marge)}" y="{f(marge)}" width="{f(cote)}" height="{f(cote)}" rx="{f(rayon)}" fill="{fond}"/>'
        visible = cote
    h_hex = visible * k_rel
    k = h_hex / sy.Z_HAUTEUR
    x = s / 2 - (sy.Z_GAUCHE + sy.Z_LARGEUR / 2) * k
    y = s / 2 - (sy.Z_HAUT + sy.Z_HAUTEUR / 2) * k
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {s} {s}" width="{s}" height="{s}">'
            f'{cadre}{symbole(contour, rempli, "i", x, y, k)}</svg>')


def liste_png(dossier):
    """Ce qu'il faut rendre en PNG : [(svg, taille, chemin)]."""
    out = [(svg_icone(512, "carre"), 512, os.path.join(dossier, "google-play-512.png"))]
    for nom_d, t in (("mdpi", 48), ("hdpi", 72), ("xhdpi", 96), ("xxhdpi", 144), ("xxxhdpi", 192)):
        d = os.path.join(dossier, "res", f"mipmap-{nom_d}")
        os.makedirs(d, exist_ok=True)
        out.append((svg_icone(t, "arrondi", k_rel=0.6), t, os.path.join(d, "ic_launcher.png")))
        out.append((svg_icone(t, "rond", k_rel=0.56), t, os.path.join(d, "ic_launcher_round.png")))
    return out
