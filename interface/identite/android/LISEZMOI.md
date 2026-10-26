# Icône Android de Sensor Maps

Copier le dossier `res/` dans `android/app/src/main/res/` (il remplace les icônes par défaut).

- `mipmap-anydpi-v26/ic_launcher.xml` : l'icône adaptative (Android 8 et plus), avec la version monochrome pour les icônes à thème (Android 13 et plus).
- `drawable/ic_launcher_foreground.xml` : le symbole, 48 dp de haut sur une toile de 108 dp, bien dans la zone sûre de 66 dp.
- `drawable/ic_launcher_background.xml` : le fond noir.
- `drawable/ic_launcher_monochrome.xml` : le symbole d'une seule couleur, qu'Android teinte lui-même.
- `drawable/ic_stat_sensor_maps.xml` : la petite icône blanche des notifications (24 dp).
- `mipmap-*dpi/` : les icônes PNG pour les anciens Android.
- `values/couleurs_sensor_maps.xml` : le noir, le blanc et les deux gris de la marque.
- `google-play-512.png` : l'icône de la fiche Google Play (512 px, carré plein : Google Play arrondit les coins).

Dans `AndroidManifest.xml` : `android:icon="@mipmap/ic_launcher"` et `android:roundIcon="@mipmap/ic_launcher_round"`.
