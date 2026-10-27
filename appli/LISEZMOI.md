# Appli Sensor Maps

L'appli Android de Sensor Maps. Pour l'instant, elle montre l'interface avec des chiffres pour l'exemple : rien n'est mesuré ni envoyé, et elle ne demande aucune autorisation.

**Installer** : ouvre https://github.com/loSCripts/sensor-maps/releases/download/appli/sensor-maps.apk sur le téléphone. Le téléchargement démarre. Ouvre le fichier, autorise l'installation depuis ton navigateur si Android le demande, puis appuie sur **Installer**. Elle s'installe à côté de l'appli de test.

**Comment elle est faite**

- Une seule page : `src/main/kotlin/.../EcranPrincipal.kt` affiche l'interface (`src/main/assets/index.html`) dans une WebView. Les fichiers sont dans l'appli : elle marche sans internet, sauf pour ouvrir la carte en ligne, qui s'ouvre dans le navigateur.
- L'interface vient de la maquette. Ne pas modifier `src/main/assets/` à la main : le refaire avec `interface/outils/construire-maquette.py` (voir `interface/outils/LISEZMOI.md`). La police Instrument Sans est incluse, avec sa licence (`polices/OFL.txt`).
- Android 15 et plus dessinent l'appli sous les barres du système : l'écran envoie leur taille à la page. Le geste retour revient à l'écran d'avant. Le thème suit le téléphone, ou le choix fait dans Réglages.
- Icône adaptative, version monochrome et écran de démarrage : `src/main/res/`.

**Fabrication** : chaque modification du dossier `appli/` fabrique une nouvelle version. La tâche `.github/workflows/appli.yml` l'essaie sur un téléphone virtuel Android 15, puis la publie dans la release fixe « appli » : le lien d'installation ne change pas. Une nouvelle version s'installe par-dessus l'ancienne.

La clé de signature `cle-de-test-publique.jks` est volontairement publique : elle ne protège rien et sert seulement aux mises à jour. Pour Google Play, il faudra une vraie clé, secrète.
