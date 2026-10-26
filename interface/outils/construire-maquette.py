"""Assemble la maquette de l'appli.  python3 construire-maquette.py <outils> <fichier artifact> <fichier complet>"""
import math
import os
import sys

sys.path.insert(0, sys.argv[1])
import icones  # noqa: E402
import symboles as sy  # noqa: E402
from geo import hexagone  # noqa: E402

OUTILS, ARTIFACT, COMPLET = sys.argv[1], sys.argv[2], sys.argv[3]


def mini_carte():
    r, cx, cy = 12.0, 40.0, 36.0
    w = math.sqrt(3) * r * 1.09
    voisins = [(cx + w, cy), (cx - w, cy), (cx + w / 2, cy - w * 0.866), (cx - w / 2, cy - w * 0.866),
               (cx + w / 2, cy + w * 0.866), (cx - w / 2, cy + w * 0.866)]
    s = "".join(f'<path class="mc" d="{hexagone(x, y, r, arrondi=2)}"/>' for x, y in voisins)
    return s + f'<path class="mc-toi" d="{hexagone(cx, cy, r - 1, arrondi=2)}"/>'


modele = open(os.path.join(OUTILS, "modele-maquette.html"), encoding="utf-8").read()
remplace = {
    "{{ICONES}}": icones.sprite(),
    "{{LOGO_DEMARRAGE}}": sy.zone(anime=True, ident="ld"),
    "{{LOGO_INTRO}}": sy.zone(anime=True, ident="li"),
    "{{LOGO_BARRE}}": sy.zone(ident="lb"),
    "{{ZONE_ETAT}}": sy.zone(anime=True, ident="ze"),
    "{{LOGO_DON}}": sy.zone(ident="ldn"),
    "{{MINI_CARTE}}": mini_carte(),
}
page = modele
for k, v in remplace.items():
    assert k in page, k
    page = page.replace(k, v)
assert "{{" not in page
os.makedirs(os.path.dirname(ARTIFACT), exist_ok=True)
open(ARTIFACT, "w", encoding="utf-8").write(page)

fin = page.index("</style>") + len("</style>")
tete, corps = page[:fin], page[fin:]
tete = tete.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
complet = ('<!doctype html>\n<html lang="fr">\n<head>\n<meta charset="utf-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
           '<meta name="color-scheme" content="light dark">\n'
           '<meta name="theme-color" content="#ffffff" media="(prefers-color-scheme: light)">\n'
           '<meta name="theme-color" content="#000000" media="(prefers-color-scheme: dark)">\n'
           + tete + '\n<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
           '[hidden]{display:none!important}</style>\n</head>\n<body>\n' + corps.strip() + "\n</body>\n</html>\n")
os.makedirs(os.path.dirname(COMPLET), exist_ok=True)
open(COMPLET, "w", encoding="utf-8").write(complet)
print("maquette", len(page), "caracteres")
