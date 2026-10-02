// Crée un PowerPoint avec un algorigramme modifiable par diapositive
// (utilise les fichiers .json produits par dessiner.py)
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.defineLayout({ name: "A4_PORTRAIT", width: 8.27, height: 11.69 });
pres.layout = "A4_PORTRAIT";
pres.title = "Algorigrammes TP1 Python";

const SCHEMAS = [
  ["exo10", "Exercice 10 – Moyenne de 3 valeurs"],
  ["exo11", "Exercice 11 – Aire du rectangle"],
  ["exo12", "Exercice 12 – Admission"],
  ["exo13", "Exercice 13 – Assurances"],
  ["exo14", "Exercice 14 – Table de multiplication"],
  ["algo1", "Algorigramme 1 – Saisie des 4 couleurs"],
  ["algo2", "Algorigramme 2 – Valeur d'une couleur"],
  ["algo3", "Algorigramme 3 – Valeur de R à partir de 3 couleurs"],
  ["algo4", "Algorigramme 4 – Valeur et tolérance d'une résistance"],
  ["tolerance", "Sous-programme tolérance (utilisé par l'algorigramme 4)"],
];
const COULEURS = { debut: "DFF5DF", rect: "E8F0FF", sp: "F3E6FF", test: "FFF4D6" };
const FONT = "Calibri";

for (const [nom, titre] of SCHEMAS) {
  const data = JSON.parse(fs.readFileSync(path.join(__dirname, nom + ".json"), "utf8"));
  const [x0, x1, y0, y1] = data.bornes;
  const slide = pres.addSlide();
  slide.background = { color: "FFFFFF" };
  slide.addText(titre, {
    x: 0.5, y: 0.35, w: 7.27, h: 0.6, fontFace: FONT, fontSize: 20, bold: true,
    color: "1F1F1F", align: "center", isTextBox: true,
  });

  // échelle : 0,5 pouce par unité au maximum, réduite pour tenir sur la page
  const zoneW = 7.27, zoneH = 10.2, zoneY = 1.15;
  const s = Math.min(0.5, zoneW / (x1 - x0), zoneH / (y1 - y0));
  const ox = 0.5 + (zoneW - (x1 - x0) * s) / 2;
  const X = (x) => ox + (x - x0) * s;
  const Y = (y) => zoneY + (y1 - y) * s;
  const taille = Math.max(7, Math.min(12, 10 * s / 0.5));

  const segment = (p, q, fleche) => {
    const [ax, ay, bx, by] = [X(p[0]), Y(p[1]), X(q[0]), Y(q[1])];
    slide.addShape(pres.shapes.LINE, {
      x: Math.min(ax, bx), y: Math.min(ay, by),
      w: Math.abs(bx - ax), h: Math.abs(by - ay),
      flipH: bx < ax, flipV: by < ay,
      line: { color: "000000", width: 1.25, ...(fleche ? { endArrowType: "triangle" } : {}) },
    });
  };

  for (const p of data.prims) {
    if (p.t === "forme") {
      const opts = {
        x: X(p.x - p.w / 2), y: Y(p.y + p.h / 2), w: p.w * s, h: p.h * s,
        fill: { color: COULEURS[p.forme] }, line: { color: "000000", width: 1.25 },
        fontFace: FONT, fontSize: taille, color: "000000", align: "center", valign: "middle",
        margin: 0,
      };
      const forme = p.forme === "test" ? pres.shapes.DIAMOND : pres.shapes.RECTANGLE;
      slide.addText(p.texte, { shape: forme, ...opts });
      if (p.forme === "sp") {
        for (const dx of [0.18, p.w - 0.18]) {
          const xl = p.x - p.w / 2 + dx;
          segment([xl, p.y + p.h / 2], [xl, p.y - p.h / 2], false);
        }
      }
    } else if (p.t === "ligne") {
      for (let i = 0; i < p.pts.length - 1; i++) {
        segment(p.pts[i], p.pts[i + 1], p.fleche && i === p.pts.length - 2);
      }
    } else if (p.t === "etiquette") {
      slide.addText(p.texte, {
        x: X(p.x), y: Y(p.y) - 0.15, w: 0.5, h: 0.3, fontFace: FONT,
        fontSize: Math.max(7, taille - 1), italic: true, color: "B00000",
        margin: 0, valign: "middle", isTextBox: true,
      });
    }
  }
}

pres.writeFile({ fileName: path.join(__dirname, "..", "Algorigrammes_TP1.pptx") })
  .then((f) => console.log(f));
