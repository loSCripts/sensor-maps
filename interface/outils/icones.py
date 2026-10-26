"""Icones de l'interface : grille de 24, trait de 1,8, bouts ronds. Dessinees pour Sensor Maps."""

T = 'fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
P = 'fill="currentColor"'

ICONES = {
    # navigation
    "accueil": f'<path {T} d="M12 3.2l7.2 4.15v8.3L12 19.8l-7.2-4.15v-8.3z"/>'
               f'<path {P} d="M5.7 12.4c2-1.6 3.9-1.6 6.3 0s4.3 1.6 6.3 0v3.1L12 19.1l-6.3-3.6z"/>',
    "capteurs": f'<rect {T} x="6.5" y="3" width="9" height="18" rx="2.2"/><path {T} d="M18.6 8.6a5 5 0 0 1 0 6.8M20.9 6.4a8.3 8.3 0 0 1 0 11.2"/>'
                f'<circle {P} cx="11" cy="17.6" r="1"/>',
    "carte": f'<path {T} d="M8 3.6l3.6 2.1v4.1L8 11.9 4.4 9.8V5.7zM15.6 8.2l3.6 2.1v4.1l-3.6 2.1-3.6-2.1v-4.1zM8 12.6l3.6 2.1v4.1L8 20.9l-3.6-2.1v-4.1z"/>',
    "soutenir": f'<path {T} d="M12 20s-7.5-4.6-7.5-10.2A4.3 4.3 0 0 1 12 7.1a4.3 4.3 0 0 1 7.5 2.7C19.5 15.4 12 20 12 20z"/>',
    "reglages": f'<path {T} d="M4 7h9M17 7h3M4 17h3M11 17h9"/><circle {T} cx="15" cy="7" r="2.2"/><circle {T} cx="9" cy="17" r="2.2"/>',
    "retour": f'<path {T} d="M19 12H5M11 6l-6 6 6 6"/>',
    "chevron": f'<path {T} d="M9.5 6l6 6-6 6"/>',
    "externe": f'<path {T} d="M14 5h5v5M19 5l-8 8M17 14v4a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 5 18V8.5A1.5 1.5 0 0 1 6.5 7H10"/>',
    "fermer": f'<path {T} d="M6 6l12 12M18 6L6 18"/>',
    "coche": f'<path {T} d="M5 12.5l4.5 4.5L19 7.5"/>',
    "bas": f'<path {T} d="M6 9.5l6 6 6-6"/>',
    # actions
    "pause": f'<rect {P} x="6.5" y="5" width="3.6" height="14" rx="1.4"/><rect {P} x="13.9" y="5" width="3.6" height="14" rx="1.4"/>',
    "lecture": f'<path {P} d="M8 5.6v12.8a1 1 0 0 0 1.5.86l10.2-6.4a1 1 0 0 0 0-1.72L9.5 4.74A1 1 0 0 0 8 5.6z"/>',
    "partager": f'<circle {T} cx="17.5" cy="5.8" r="2.6"/><circle {T} cx="6.5" cy="12" r="2.6"/><circle {T} cx="17.5" cy="18.2" r="2.6"/><path {T} d="M8.8 10.7l6.4-3.6M8.8 13.3l6.4 3.6"/>',
    "effacer": f'<path {T} d="M4.5 7h15M9.5 7V5.2a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1V7M6.5 7l.8 11.6a1.5 1.5 0 0 0 1.5 1.4h6.4a1.5 1.5 0 0 0 1.5-1.4L17.5 7"/>',
    "rejouer": f'<path {T} d="M4.5 12a7.5 7.5 0 1 0 2.2-5.3M4.5 4.5v4.4h4.4"/>',
    # etats et vie privee
    "batterie": f'<rect {T} x="3" y="7.5" width="16" height="9" rx="2.2"/><path {T} d="M21 10.5v3"/><rect {P} x="5.4" y="9.9" width="6" height="4.2" rx=".8"/>',
    "lune": f'<path {T} d="M19.5 14.6A8 8 0 0 1 9.4 4.5a8 8 0 1 0 10.1 10.1z"/>',
    "cloche": f'<path {T} d="M6 16.5V11a6 6 0 0 1 12 0v5.5l1.5 1.5h-15zM10 20.5a2.2 2.2 0 0 0 4 0"/>',
    "pose": f'<rect {T} x="5" y="9.2" width="14" height="6.6" rx="1.8"/><path {T} d="M3 19h18"/><circle {P} cx="16.4" cy="12.5" r=".9"/>',
    "zone-point": f'<path {T} d="M12 3.2l7.2 4.15v8.3L12 19.8l-7.2-4.15v-8.3z"/><circle {P} cx="12" cy="11.5" r="2.2"/>',
    "bouclier": f'<path {T} d="M12 3.5l7 2.6v5.4c0 4.4-3 7.7-7 9-4-1.3-7-4.6-7-9V6.1z"/><path {T} d="M9 12l2.2 2.2L15.3 10"/>',
    "personne-barre": f'<circle {T} cx="12" cy="8" r="3.4"/><path {T} d="M5.5 19.5a6.5 6.5 0 0 1 13 0M4 4l16 16"/>',
    "micro-barre": f'<rect {T} x="9" y="3.5" width="6" height="10.5" rx="3"/><path {T} d="M6 11.5a6 6 0 0 0 12 0M12 17.5v3M4 4l16 16"/>',
    "cinq": f'<path {T} d="M12 3.2l7.2 4.15v8.3L12 19.8l-7.2-4.15v-8.3z"/><path {T} d="M13.9 7.9h-3.5l-.5 3.4a2.6 2.6 0 1 1-.2 3.9"/>',
    "pluie": f'<path {T} d="M7.5 14.5h9.2a3.8 3.8 0 0 0 .6-7.6 5.3 5.3 0 0 0-10.2 1.3A3.2 3.2 0 0 0 7.5 14.5z"/><path {T} d="M8.5 17.5l-1 2M12.5 17.5l-1 2M16.5 17.5l-1 2"/>',
    "telephone": f'<rect {T} x="7" y="3" width="10" height="18" rx="2.2"/><path {T} d="M10.5 17.8h3"/>',
    # capteurs
    "aimant": f'<path {T} d="M6 4.5v7a6 6 0 0 0 12 0v-7h-3.6v7a2.4 2.4 0 0 1-4.8 0v-7z"/><path {T} d="M6 8.2h3.6M14.4 8.2H18"/>',
    "soleil": f'<circle {T} cx="12" cy="12" r="3.8"/><path {T} d="M12 2.8v2M12 19.2v2M2.8 12h2M19.2 12h2M5.5 5.5l1.4 1.4M17.1 17.1l1.4 1.4M5.5 18.5l1.4-1.4M17.1 6.9l1.4-1.4"/>',
    "bruit": f'<path {T} d="M4 10v4M8 7v10M12 4.5v15M16 8v8M20 10.5v3"/>',
    "signal": f'<path {T} d="M5 19v-2.5M9.7 19v-5.5M14.3 19v-8.5M19 19V5"/>',
    "pression": f'<path {T} d="M4.2 16.8a8.5 8.5 0 1 1 15.6 0"/><path {T} d="M12 13.5l3.6-4.2"/><circle {P} cx="12" cy="13.5" r="1.4"/>',
    "info": f'<circle {T} cx="12" cy="12" r="8.6"/><path {T} d="M12 11v5.5M12 7.8v.1"/>',
}


def sprite():
    return "".join(f'<symbol id="i-{n}" viewBox="0 0 24 24">{c}</symbol>' for n, c in ICONES.items())
