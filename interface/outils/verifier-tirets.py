"""Verifie qu'aucun fichier ne contient de tiret long, de tiret moyen ou de signe qui leur ressemble.

python3 -I tirets.py fichier_ou_dossier [...]
Les signes sont ecrits par leur numero Unicode, pour que ce fichier lui-meme reste propre.
"""
import os
import sys

INTERDITS = {
    0x2012: "tiret numerique",
    0x2013: "tiret moyen",
    0x2014: "tiret long",
    0x2015: "barre horizontale",
    0x2212: "signe moins",
}


def fichiers(chemins):
    for c in chemins:
        if os.path.isdir(c):
            for racine, _, noms in os.walk(c):
                for n in noms:
                    yield os.path.join(racine, n)
        else:
            yield c


probleme = 0
vus = 0
for chemin in fichiers(sys.argv[1:]):
    try:
        texte = open(chemin, encoding="utf-8").read()
    except (UnicodeDecodeError, OSError):
        continue
    vus += 1
    for num, ligne in enumerate(texte.splitlines(), 1):
        for code, nom in INTERDITS.items():
            if chr(code) in ligne:
                probleme += 1
                print(f"{chemin}:{num}: {nom}")
print(f"{vus} fichier(s) lus, {probleme} probleme(s)")
sys.exit(1 if probleme else 0)
