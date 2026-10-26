"""Fabrique les fichiers du logo et le kit Android.  python3 kit.py <outils> <dossier identite>"""
import json
import os
import sys
import tempfile

sys.path.insert(0, sys.argv[1])
import marque  # noqa: E402

base = sys.argv[2]
logos = marque.fichiers_logo(os.path.join(base, "logo"))
android = os.path.join(base, "android")
marque.fichiers_android(android)
liste = [{"svg": s, "taille": t, "sortie": o} for s, t, o in marque.liste_png(android)]
chemin = os.path.join(tempfile.gettempdir(), "png-a-faire.json")
json.dump(liste, open(chemin, "w"))
print(len(logos), "logos ;", len(liste), "PNG a rendre avec : node png.js", chemin)
