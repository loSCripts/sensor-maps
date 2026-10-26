// Rend des SVG en PNG a la taille exacte : node png.js liste.json
const { chromium } = require('playwright');
const fs = require('fs');
(async () => {
  const liste = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const nav = await chromium.launch();
  const p = await nav.newPage({ deviceScaleFactor: 1 });
  for (const { svg, taille, sortie } of liste) {
    await p.setViewportSize({ width: taille, height: taille });
    await p.setContent('<!doctype html><style>html,body{margin:0;background:transparent}svg{display:block}</style>' + svg);
    await p.screenshot({ path: sortie, omitBackground: true, clip: { x: 0, y: 0, width: taille, height: taille } });
  }
  await nav.close();
  console.log(liste.length + ' PNG');
})();
