/* Nemaudig — effets visuels de la planche 3D du premier écran :
   flux lumineux le long du trajet digestif, anneaux holographiques en orbite. */
import * as THREE from "./vendor/three.module.min.js";

const V = (x, y, z) => new THREE.Vector3((x - 200) / 100, (300 - y) / 100, z);

let textureLueur = null;
function lueur() {
  if (textureLueur) return textureLueur;
  const c = document.createElement("canvas");
  c.width = c.height = 64;
  const g = c.getContext("2d");
  const d = g.createRadialGradient(32, 32, 0, 32, 32, 32);
  d.addColorStop(0, "rgba(255,255,255,1)");
  d.addColorStop(0.25, "rgba(160,245,235,.9)");
  d.addColorStop(0.6, "rgba(43,179,167,.35)");
  d.addColorStop(1, "rgba(43,179,167,0)");
  g.fillStyle = d;
  g.fillRect(0, 0, 64, 64);
  textureLueur = new THREE.CanvasTexture(c);
  return textureLueur;
}

/* Trajet du bol alimentaire, repris des tracés de la planche (coordonnées SVG 400×600). */
const TRAJET = [
  [201, 18, -0.1], [200, 60, -0.12], [207, 108, -0.16], [213, 160, -0.22], [218, 180, 0.3],
  [252, 172, 0.55], [280, 200, 0.55], [268, 245, 0.55], [232, 258, 0.5], [203, 255, 0.2],
  [180, 268, -0.1], [180, 298, -0.1], [212, 306, -0.1], [238, 292, 0],
  [252, 340, 0.1], [215, 340, 0.15], [176, 350, 0.05], [190, 366, 0.12], [240, 364, 0.12], [268, 375, 0.05],
  [240, 390, 0.12], [190, 393, 0.12], [172, 405, 0.05], [205, 418, 0.12], [255, 414, 0.12], [262, 428, 0.05],
  [190, 432, 0.1], [155, 436, 0.12], [138, 430, 0.15], [131, 380, 0.15], [134, 322, 0.15], [170, 300, 0.15],
  [215, 314, 0.15], [262, 309, 0.15], [295, 305, 0.15], [298, 370, 0.15], [295, 430, 0.12], [262, 455, 0.05],
  [232, 453, -0.05], [212, 475, -0.12], [205, 505, -0.18], [203, 532, -0.22],
];

export function fluxDigestif(nbImpulsions = 3, longueurTrainee = 14) {
  const courbe = new THREE.CatmullRomCurve3(TRAJET.map(([x, y, z]) => V(x, y, z)), false, "centripetal");
  const groupe = new THREE.Group();
  const impulsions = [];
  for (let i = 0; i < nbImpulsions; i++) {
    const points = [];
    for (let k = 0; k < longueurTrainee; k++) {
      const m = new THREE.SpriteMaterial({ map: lueur(), color: k === 0 ? 0x7ff0e2 : 0x2bb3a7, transparent: true, depthTest: false, depthWrite: false,
        opacity: (1 - k / longueurTrainee) * 0.95 });
      const s = new THREE.Sprite(m);
      const taille = 0.26 * (1 - k / longueurTrainee * 0.7);
      s.scale.set(taille, taille, 1);
      s.renderOrder = 10;
      groupe.add(s);
      points.push(s);
    }
    impulsions.push({ points, decalage: i / nbImpulsions });
  }
  groupe.userData.animer = (t, intensite = 1) => {
    for (const imp of impulsions) {
      const u0 = (t / 11 + imp.decalage) % 1;
      imp.points.forEach((s, k) => {
        const u = (u0 - k * 0.0045 + 1) % 1;
        s.position.copy(courbe.getPointAt(u));
        const base = (1 - k / imp.points.length) * 0.95;
        s.material.opacity = base * intensite * Math.min(1, u0 * 20, (1 - u0) * 20);
      });
    }
  };
  return groupe;
}

/* Deux anneaux inclinés autour du corps, avec de petits satellites lumineux. */
export function orbites() {
  const groupe = new THREE.Group();
  const anneaux = [];
  [[2.15, 0.35, 0.2, 0.0], [2.45, -0.28, -0.35, 1.8]].forEach(([r, inclX, inclZ, phase]) => {
    const pivot = new THREE.Group();
    pivot.rotation.set(Math.PI / 2 + inclX, 0, inclZ);
    pivot.position.y = 0.1;
    const trait = new THREE.Mesh(new THREE.TorusGeometry(r, 0.006, 6, 220),
      new THREE.MeshBasicMaterial({ color: 0x2bb3a7, transparent: true, opacity: 0.32, depthWrite: false }));
    pivot.add(trait);
    const satellites = [];
    for (let i = 0; i < 3; i++) {
      const s = new THREE.Sprite(new THREE.SpriteMaterial({ map: lueur(), transparent: true, depthWrite: false, opacity: 0.9 }));
      s.scale.set(0.16, 0.16, 1);
      pivot.add(s);
      satellites.push({ s, a: phase + (i * Math.PI * 2) / 3 });
    }
    groupe.add(pivot);
    anneaux.push({ r, satellites, vitesse: 0.22 + phase * 0.04 });
  });
  groupe.userData.animer = (t) => {
    for (const a of anneaux) {
      for (const sat of a.satellites) {
        const ang = sat.a + t * a.vitesse;
        sat.s.position.set(Math.cos(ang) * a.r, Math.sin(ang) * a.r, 0);
      }
    }
  };
  return groupe;
}
