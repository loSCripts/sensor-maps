# Outils de l'identité

- `construire.py` fabrique `interface/identite/pistes-logo.html` et les SVG de `interface/identite/logos/`, à partir de `modele.html` et `symboles.py`.
- `verifier-tirets.py` vérifie qu'aucun fichier ne contient de tiret long ou de tiret moyen.

Depuis la racine du dépôt :

    python3 interface/outils/construire.py interface/outils /tmp/identite-artifact.html interface/identite
    python3 interface/outils/verifier-tirets.py interface
