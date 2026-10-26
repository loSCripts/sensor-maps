"""Assemble la page des pistes de logo.

python3 -I construire.py <dossier outils> <fichier artifact> <dossier depot interface/identite>
"""
import os
import sys

sys.path.insert(0, sys.argv[1])
import symboles as sy  # noqa: E402

OUTILS, ARTIFACT, DEPOT = sys.argv[1], sys.argv[2], sys.argv[3]

modele = open(os.path.join(OUTILS, "modele.html"), encoding="utf-8").read()
remplace = {
    "{{POINTS}}": sy.points(),
    "{{POINTS_PETIT}}": sy.points(petit=True),
    "{{ZONE}}": sy.zone(ident="zs"),
    "{{ONDE}}": sy.onde(),
    "{{HERO_POINTS}}": sy.points(anime=True),
    "{{HERO_ZONE}}": sy.zone(anime=True, ident="zh"),
    "{{HERO_ONDE}}": sy.onde(anime=True),
}
page = modele
for cle, val in remplace.items():
    page = page.replace(cle, val)
assert "{{" not in page

# 1. Version artifact : sans squelette, il est ajoute a la publication
os.makedirs(os.path.dirname(ARTIFACT), exist_ok=True)
open(ARTIFACT, "w", encoding="utf-8").write(page)

# 2. Version complete, pour le depot et le ZIP (s'ouvre seule sur le telephone)
fin_tete = page.index("</style>") + len("</style>")
tete, corps = page[:fin_tete], page[fin_tete:]
tete = tete.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
complet = (
    '<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
    '<meta name="color-scheme" content="light dark">\n'
    + tete
    + '\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
    'body{margin:0}[hidden]{display:none!important}</style>\n</head>\n<body>\n'
    + corps.strip() + "\n</body>\n</html>\n"
)
os.makedirs(os.path.join(DEPOT, "logos"), exist_ok=True)
open(os.path.join(DEPOT, "pistes-logo.html"), "w", encoding="utf-8").write(complet)

# 3. Les symboles en fichiers SVG
fichiers = {
    "1-points.svg": sy.points(),
    "1-points-petite-taille.svg": sy.points(petit=True),
    "2-zone.svg": sy.zone(ident="z"),
    "3-onde.svg": sy.onde(),
}
for nom, corps_svg in fichiers.items():
    open(os.path.join(DEPOT, "logos", nom), "w", encoding="utf-8").write(sy.svg_fichier(corps_svg))
print("page", len(page), "octets ; complet", len(complet), "octets")
