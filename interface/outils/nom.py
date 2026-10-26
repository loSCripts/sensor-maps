"""Le nom « Sensor Maps » en contours SVG (police Instrument Sans SemiBold, approche resserree).

Usage : python nom.py police.ttf  ->  affiche un JSON {d, largeur, hauteur_capitale, ascendante, descendante}
"""
import json
import sys

import uharfbuzz as hb
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

TEXTE = "Sensor Maps"
APPROCHE = -0.012  # en em, comme letter-spacing

chemin = sys.argv[1]
police = TTFont(chemin)
upm = police["head"].unitsPerEm
jeu = police.getGlyphSet()

blob = hb.Blob.from_file_path(chemin)
face = hb.Face(blob)
fonte = hb.Font(face)
tampon = hb.Buffer()
tampon.add_str(TEXTE)
tampon.guess_segment_properties()
hb.shape(fonte, tampon, {"kern": True, "liga": True})

ordre = police.getGlyphOrder()
x = 0.0
morceaux = []
for info, pos in zip(tampon.glyph_infos, tampon.glyph_positions):
    nom = ordre[info.codepoint]
    stylo = SVGPathPen(jeu, ntos=lambda v: ("%.1f" % v).rstrip("0").rstrip("."))
    # retourne l'axe vertical (police : y vers le haut, SVG : y vers le bas)
    tp = TransformPen(stylo, (1, 0, 0, -1, x + pos.x_offset, -pos.y_offset))
    jeu[nom].draw(tp)
    d = stylo.getCommands()
    if d:
        morceaux.append(d)
    x += pos.x_advance + APPROCHE * upm
x -= APPROCHE * upm
os2 = police["OS/2"]
print(json.dumps({
    "d": "".join(morceaux),
    "largeur": round(x, 1),
    "upm": upm,
    "capitale": getattr(os2, "sCapHeight", 700),
    "ascendante": police["hhea"].ascent,
    "descendante": police["hhea"].descent,
    "copyright": police["name"].getDebugName(0),
}))
