"""Assemble la page Identite (noir et blanc).

python3 construire-identite.py <outils> <fichier artifact> <fichier complet> <lien maquette artifact>
"""
import os
import sys

sys.path.insert(0, sys.argv[1])
import marque as m  # noqa: E402
import symboles as sy  # noqa: E402
from geo import f  # noqa: E402

OUTILS, ARTIFACT, COMPLET, URL_MAQUETTE = sys.argv[1:5]
COURANT = "currentColor"


def lum(h):
    r, g, b = [int(h.lstrip("#")[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = lambda x: x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4
    return 0.2126 * c(r) + 0.7152 * c(g) + 0.0722 * c(b)


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def paires(liste):
    out = ""
    for nom, a, b in liste:
        r = ratio(a, b)
        assert r >= 4.5, (nom, r)
        classe = "ratio aaa" if r >= 7 else "ratio"
        txt = f"{r:.1f}".replace(".", ",") + " : 1"
        out += f'<li><span>{nom}</span><span class="{classe}">{txt}</span></li>'
    return out


def svg_boite(corps, l, h):
    return f'<svg viewBox="0 0 {f(l)} {f(h)}" aria-hidden="true">{corps}</svg>'


def symbole_seul(couleur, ident):
    corps = sy.zone(ident=ident, contour=couleur, rempli=couleur)
    return svg_boite(f'<g transform="translate({-sy.Z_GAUCHE} {-sy.Z_HAUT})">{corps}</g>', sy.Z_LARGEUR, sy.Z_HAUTEUR)


def signature(fn, couleur, ident):
    c, l, h = fn(couleur, couleur, couleur, ident)
    return svg_boite(c, l, h)


hx, inter, vg = sy.zone_chemins()
trait = f'<path d="{hx}" fill="none" stroke="currentColor" stroke-width="{sy.ZTRAIT}" stroke-linejoin="round"/>'
etape_2 = (f'<defs><clipPath id="e2-clip"><path d="{inter}"/></clipPath></defs>'
           f'<g clip-path="url(#e2-clip)"><path class="repos" transform="translate(0 17)" d="{vg}"/></g>{trait}')

# Icone adaptative : fond noir, symbole blanc, partie hors cadre voilee, reperes
k, dec = m.K_ADAPT, m.DEC_ADAPT
adaptative = (f'<rect width="108" height="108" fill="{m.NOIR}"/>{m.symbole(m.BLANC, m.BLANC, "ad", dec, dec, k)}'
              '<path fill-rule="evenodd" fill="#ffffff" fill-opacity=".42" d="M0 0h108v108H0zM18 18v72h72V18z"/>'
              '<rect x="18" y="18" width="72" height="72" fill="none" style="stroke:var(--guide-visible)" stroke-width="1"/>'
              '<circle cx="54" cy="54" r="33" fill="none" style="stroke:var(--guide-sur)" stroke-width="1"/>'
              '<rect x=".5" y=".5" width="107" height="107" fill="none" style="stroke:var(--guide-toile)" stroke-width="1"/>')


def icone_108(ident):
    return (f'<svg viewBox="0 0 108 108" aria-hidden="true"><rect width="108" height="108" fill="{m.NOIR}"/>'
            f'{m.symbole(m.BLANC, m.BLANC, ident, dec, dec, k)}</svg>')


def mono(ident):
    return f'<svg viewBox="0 0 96 96" aria-hidden="true" style="fill:currentColor">{sy.zone(ident=ident)}</svg>'


notif = f'<svg viewBox="0 0 96 96" aria-hidden="true" style="fill:#ffffff;color:#ffffff">{sy.zone(ident="nt")}</svg>'
play = m.svg_icone(512, "carre").replace(' width="512" height="512">', ' aria-hidden="true">', 1)

remplace = {
    "{{SIG_TETE}}": signature(m.signature_horizontale, COURANT, "st"),
    "{{HERO}}": sy.zone(anime=True, ident="hero"),
    "{{ETAPE_1}}": trait,
    "{{ETAPE_2}}": etape_2,
    "{{ETAPE_3}}": sy.zone(ident="e3"),
    "{{SIG_H_NOIR}}": signature(m.signature_horizontale, m.NOIR, "s1"),
    "{{SIG_H_BLANC}}": signature(m.signature_horizontale, m.BLANC, "s2"),
    "{{SIG_V_NOIR}}": signature(m.signature_verticale, m.NOIR, "s3"),
    "{{SIG_V_BLANC}}": signature(m.signature_verticale, m.BLANC, "s4"),
    "{{SYM_NOIR}}": symbole_seul(m.NOIR, "y1"),
    "{{SYM_BLANC}}": symbole_seul(m.BLANC, "y2"),
    "{{ADAPTATIVE}}": adaptative,
    "{{ICONE_108_1}}": icone_108("ic1"),
    "{{ICONE_108_2}}": icone_108("ic2"),
    "{{ICONE_108_3}}": icone_108("ic3"),
    "{{MONO_1}}": mono("mo1"),
    "{{MONO_2}}": mono("mo2"),
    "{{NOTIF}}": notif,
    "{{PLAY}}": play,
    "{{SYM_DEM_1}}": sy.zone(ident="dm1"),
    "{{SYM_DEM_2}}": sy.zone(ident="dm2"),
    "{{SYM_APERCU_1}}": sy.zone(ident="ap1"),
    "{{SYM_APERCU_2}}": sy.zone(ident="ap2"),
    "{{ANIME}}": sy.zone(anime=True, ident="an"),
    "{{PAIRES_CLAIR}}": paires([
        ("Texte", m.NOIR, m.BLANC), ("Texte doux", m.GRIS, m.BLANC), ("Texte doux sur un bloc", m.GRIS, m.SURFACE_CLAIRE),
        ("Bouton noir", m.BLANC, m.NOIR), ("Bouton doux", m.NOIR, m.DOUX_CLAIR)]),
    "{{PAIRES_SOMBRE}}": paires([
        ("Texte", m.BLANC, m.NOIR), ("Texte doux", m.GRIS_CLAIR, m.NOIR), ("Texte doux sur un bloc", m.GRIS_CLAIR, m.SURFACE_SOMBRE),
        ("Bouton blanc", m.NOIR, m.BLANC), ("Bouton doux", m.BLANC, m.DOUX_SOMBRE)]),
}

page = open(os.path.join(OUTILS, "modele-identite.html"), encoding="utf-8").read()
for cle, val in remplace.items():
    assert cle in page, cle
    page = page.replace(cle, val)

artifact = page.replace("{{LIEN_MAQUETTE}}", URL_MAQUETTE).replace("{{CIBLE_MAQUETTE}}", ' target="_blank" rel="noopener"')
complet_corps = page.replace("{{LIEN_MAQUETTE}}", "../maquette/index.html").replace("{{CIBLE_MAQUETTE}}", "")
for t in (artifact, complet_corps):
    i = t.find("{{")
    assert i < 0, t[max(0, i - 120):i + 60]
os.makedirs(os.path.dirname(ARTIFACT), exist_ok=True)
open(ARTIFACT, "w", encoding="utf-8").write(artifact)

fin = complet_corps.index("</style>") + len("</style>")
tete, corps = complet_corps[:fin], complet_corps[fin:]
tete = tete.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
complet = ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           '<meta name="color-scheme" content="light dark">\n'
           '<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">\n'
           '<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">\n'
           + tete + '\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
           'body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n' + corps.strip() + "\n</body>\n</html>\n")
os.makedirs(os.path.dirname(COMPLET), exist_ok=True)
open(COMPLET, "w", encoding="utf-8").write(complet)
print("identite", len(artifact), "caracteres")
