# Outils de l'identité et de la maquette

Ces scripts fabriquent les pages et les fichiers de `interface/`. Il faut Python 3, et Node avec Playwright pour les PNG.

Depuis la racine du dépôt :

    python3 interface/outils/kit.py interface/outils interface/identite
    node interface/outils/png.js /tmp/png-a-faire.json
    python3 interface/outils/construire-maquette.py interface/outils /tmp/maquette-artifact.html interface/maquette/index.html
    python3 interface/outils/construire-identite.py interface/outils /tmp/identite-artifact.html interface/identite/index.html LIEN_DE_LA_MAQUETTE
    python3 interface/outils/verifier-tirets.py interface

- `marque.py` : les couleurs, les signatures (symbole et nom) et le kit Android.
- `symboles.py` et `geo.py` : la géométrie du symbole Zone (et des deux autres pistes du départ).
- `icones.py` : les icônes de l'appli.
- `modele-identite.html` et `modele-maquette.html` : les deux pages avant assemblage.
- `nom-600.json` : le nom « Sensor Maps » déjà mis en contours (Instrument Sans SemiBold). `nom.py` le refait, avec fontTools et uharfbuzz.
- `verifier-tirets.py` : vérifie qu'aucun fichier ne contient de tiret long ou de tiret moyen.
