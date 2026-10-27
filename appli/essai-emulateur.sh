#!/usr/bin/env bash
# Essai automatique de l'appli sur un émulateur Android (lancé par GitHub Actions).
# Il ouvre l'appli, attend que l'interface soit prête, touche « Go », fait le geste retour,
# ferme l'appli, la rouvre, passe le téléphone en thème sombre, puis vérifie qu'elle n'a
# jamais planté. Les captures d'écran sont gardées.
# Usage : bash essai-emulateur.sh sensor-maps.apk
set -euo pipefail
APK="$1"
P=io.github.loscripts.sensormaps

journal() { adb logcat -d -s SensorMaps:I; }

# Attend que le journal de l'appli contienne n fois le texte donné, 60 secondes au plus
attendre() {
  local texte="$1" n="$2" vu=0
  for _ in $(seq 1 60); do
    vu=$(journal | grep -c "$texte" || true)
    if [ "$vu" -ge "$n" ]; then return 0; fi
    sleep 1
  done
  echo "Pas vu « $texte » $n fois (vu : $vu)."
  return 1
}

# L'appli est-elle à l'écran ?
devant() {
  adb shell dumpsys activity activities \
    | grep -E "^[[:space:]]*(topResumedActivity|mResumedActivity|ResumedActivity|Resumed)[:=]" | grep -q "$P"
}

# Donne le centre du bouton dont le texte est donné, s'il est visible à l'écran
trouver() {
  timeout 40 adb shell uiautomator dump /sdcard/ecran.xml >/dev/null 2>&1 || return 1
  adb pull /sdcard/ecran.xml ecran.xml >/dev/null 2>&1 || return 1
  python3 -c '
import re, sys, xml.etree.ElementTree as ET
for n in ET.parse("ecran.xml").iter("node"):
    for a in ("text", "content-desc"):
        if (n.get(a) or "").strip().casefold() == sys.argv[1].casefold():
            x1, y1, x2, y2 = map(int, re.findall(r"\d+", n.get("bounds")))
            print((x1 + x2) // 2, (y1 + y2) // 2)
            sys.exit(0)
sys.exit(1)
' "$1"
}

adb install -r "$APK"
# Grande mémoire pour les messages système : rien ne doit être perdu pendant l'essai
adb logcat -G 16M || true
adb logcat -c

echo "===== 1. Premier lancement ====="
adb shell am start -W -n $P/.EcranPrincipal
attendre "Interface prête" 1
attendre "Police" 1
sleep 2
adb exec-out screencap -p > ecran-1.png

echo "===== 2. Go, puis geste retour ====="
navigation=non
xy=""
for _ in 1 2 3; do
  if xy=$(trouver "Go"); then break; fi
  xy=""
  sleep 2
done
if [ -n "$xy" ]; then
  adb shell input tap $xy
  attendre "Écran : promesse" 1
  sleep 1
  adb exec-out screencap -p > ecran-2.png
  adb shell input keyevent 4
  attendre "Écran : bienvenue" 2
  sleep 1
  if devant; then
    navigation=oui
    echo "Le geste retour revient à l'écran d'avant, l'appli reste ouverte."
  else
    echo "Le geste retour a fermé l'appli au lieu de revenir à l'écran d'avant."
    exit 1
  fi
else
  echo "Bouton « Go » introuvable par uiautomator : étape passée."
fi

echo "===== 3. Geste retour depuis le premier écran : l'appli se ferme ====="
adb shell input keyevent 4
sleep 3
if devant; then
  echo "L'appli est restée ouverte après le geste retour depuis le premier écran."
  exit 1
fi

echo "===== 4. Deuxième ouverture ====="
adb shell am start -W -n $P/.EcranPrincipal
attendre "Interface prête" 2
sleep 2
adb exec-out screencap -p > ecran-3.png

echo "===== 5. Thème sombre du téléphone ====="
adb shell cmd uimode night yes
attendre "Interface prête" 3
sleep 3
adb exec-out screencap -p > ecran-4.png
adb shell cmd uimode night no
sleep 3

echo "===== Journal de l'appli ====="
journal

echo "===== Vérifications ====="
if adb logcat -d | grep -A 20 "FATAL EXCEPTION" | grep -q "$P"; then
  adb logcat -d | grep -A 30 "FATAL EXCEPTION"
  echo "L'appli a planté."
  exit 1
fi
if ! journal | grep -q "Police chargée"; then
  echo "La police de l'appli ne s'est pas chargée."
  exit 1
fi
echo "Aucun plantage. Interface chargée $(journal | grep -c "Interface prête") fois, police chargée, navigation essayée : $navigation."
