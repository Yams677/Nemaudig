/* Arrêts « complets » du voyage : l'organe réel (BodyParts3D) en vue éclatée, puis une
   animation schématique par pathologie. Tout est piloté par le défilement (explosion,
   enveloppe e de la pathologie) ; seul le reflux s'écoule doucement dans le temps.
   Coordonnées des pièces : millimètres, repère BodyParts3D (Z vers le haut). */
import * as THREE from "./vendor/three.module.min.js";
import { chargerOrgane, matiere } from "./organes3d.js";

const V = (x = 0, y = 0, z = 0) => new THREE.Vector3(x, y, z);
const TAILLE = 2.6;

async function piece(chemin, teinte) {
  const geo = await chargerOrgane(chemin);
  geo.computeBoundingBox();
  const mesh = new THREE.Mesh(geo, matiere(teinte));
  return { mesh, centre: geo.boundingBox.getCenter(V()), boite: geo.boundingBox.clone(), dir: V(), ecart: 0 };
}

function boule(rayon, couleur) {
  const m = new THREE.Mesh(new THREE.SphereGeometry(rayon, 20, 14),
    new THREE.MeshStandardMaterial({ color: couleur, roughness: 0.55, emissive: 0xf38d38, emissiveIntensity: 0 }));
  m.scale.setScalar(0.0001);
  return m;
}

/* Axe d'un organe tubulaire : centres des tranches horizontales, du bas vers le haut. */
function axe(geo, tranches = 24) {
  const p = geo.attributes.position, b = geo.boundingBox;
  const somme = Array.from({ length: tranches }, () => V()), n = new Array(tranches).fill(0);
  for (let i = 0; i < p.count; i++) {
    const k = Math.min(tranches - 1, Math.floor(((p.getZ(i) - b.min.z) / (b.max.z - b.min.z)) * tranches));
    somme[k].add(V(p.getX(i), p.getY(i), p.getZ(i))); n[k]++;
  }
  return somme.map((s, k) => s.divideScalar(Math.max(1, n[k]))).filter((_, k) => n[k] > 0);
}
const surAxe = (pts, f) => {
  const x = Math.min(pts.length - 1.001, Math.max(0, f * (pts.length - 1))), i = Math.floor(x);
  return pts[i].clone().lerp(pts[i + 1], x - i);
};

/* Cadre commun : centre l'ensemble, le met à l'échelle, prépare les directions d'éclatement. */
function cadrer(pieces) {
  const corps = new THREE.Group();
  corps.rotation.x = -Math.PI / 2;
  const boite = new THREE.Box3();
  pieces.forEach((p) => boite.union(p.boite));
  const c = boite.getCenter(V()), dim = boite.getSize(V());
  const k = TAILLE / Math.max(dim.x, dim.y, dim.z);
  corps.scale.setScalar(k);
  corps.position.set(-c.x * k, -c.z * k, c.y * k);
  pieces.forEach((p) => { p.dir = p.centre.clone().sub(c).normalize(); corps.add(p.mesh); });
  const groupe = new THREE.Group();
  groupe.add(corps);
  return { groupe, corps, centre: c };
}

function reinitialiser(pieces) {
  for (const p of pieces) {
    p.mesh.position.set(0, 0, 0);
    p.mesh.material.emissiveIntensity = 0;
    p.mesh.material.userData.zone.uZoneF.value = 0;
  }
}
const eclater = (p, mm) => p.mesh.position.addScaledVector(p.dir, mm);
/* Repères anatomiques : point (mm) d'une pièce, suivi pendant l'éclatement. */
const repere = (nom, p, point) => ({ nom, p, point });
function positionsReperes(corps, liste) {
  return liste.map(({ nom, p, point }) => ({ nom, monde: corps.localToWorld(point.clone().add(p ? p.mesh.position : V())) }));
}

const zone = (p, point, rayon, force) => {
  const z = p.mesh.material.userData.zone;
  z.uZone.value.copy(point); z.uZoneR.value = rayon; z.uZoneF.value = force;
};

/* ── Œsophage : reflux, hernie hiatale, tumeur de la paroi ─────────────────── */
async function etudeOesophage() {
  const [oeso, estomac] = await Promise.all([piece("oesophage", "oesophage"), piece("estomac", "estomac")]);
  const pieces = [oeso, estomac];
  const { groupe, corps, centre } = cadrer(pieces);
  oeso.dir.set(0, 0, 1); estomac.dir.set(0, 0, -1);
  const ligne = axe(oeso.mesh.geometry);
  const jonction = ligne[0].clone();
  // Orifice hiatal : anneau horizontal à la jonction œsophage-estomac
  const anneau = new THREE.Mesh(new THREE.TorusGeometry(15, 1.4, 12, 64),
    new THREE.MeshStandardMaterial({ color: 0xf38d38, emissive: 0xf38d38, emissiveIntensity: 0.8, roughness: 0.4 }));
  anneau.position.copy(jonction).add(V(0, 0, 6));
  anneau.scale.setScalar(0.0001);
  corps.add(anneau);
  // Reflux : gouttes qui remontent dans le bas de l'œsophage
  const gouttes = Array.from({ length: 12 }, () => boule(2.4, 0xffb36b));
  gouttes.forEach((g) => { g.material.emissiveIntensity = 0.9; corps.add(g); });
  const sommetEstomac = (() => {
    const p = estomac.mesh.geometry.attributes.position; let best = V(0, 0, -1e9);
    for (let i = 0; i < p.count; i++) if (p.getZ(i) > best.z) best = V(p.getX(i), p.getY(i), p.getZ(i));
    return best;
  })();
  const pointTumeur = surAxe(ligne, 0.32).add(V(0, -9, 0));   // face avant (−y)
  const reperes = [repere("Œsophage", oeso, surAxe(ligne, 0.72)), repere("Orifice hiatal", oeso, jonction.clone().add(V(0, 0, 6))),
    repere("Estomac", estomac, estomac.centre.clone())];

  return {
    groupe, corps, reperes: () => positionsReperes(corps, reperes),
    mettreAJour({ eclat, anim, e, temps }) {
      reinitialiser(pieces);
      eclater(oeso, 6 * eclat); eclater(estomac, 10 * eclat);
      anneau.scale.setScalar(Math.max(0.0001, anim === "hernie" || anim === "reflux" ? e : 0));
      gouttes.forEach((g, k) => {
        const s = (temps * 0.16 + k / gouttes.length) % 1;
        g.position.copy(surAxe(ligne, 0.02 + s * 0.42)).add(oeso.mesh.position);
        g.scale.setScalar(Math.max(0.0001, anim === "reflux" ? e * Math.sin(Math.PI * s) : 0));
      });
      let foyer = centre.clone();
      if (anim === "reflux") { zone(oeso, surAxe(ligne, 0.12), 30, 0.9 * e); foyer = surAxe(ligne, 0.18); }
      if (anim === "hernie") {
        estomac.mesh.position.z += 26 * e;
        zone(estomac, sommetEstomac, 34, 0.7 * e);
        foyer = jonction.clone().add(V(0, 0, 10));
      }
      if (anim === "zone-oeso") { zone(oeso, pointTumeur, 26, 1.1 * e); foyer = pointTumeur.clone(); }
      return corps.localToWorld(foyer.lerp(centre, 1 - e).clone());
    },
  };
}

/* ── Foie et vésicule : segments, calculs, ablation ────────────────────────── */
const SEGMENTS = ["caude", "ii", "iii", "iv", "v", "vi", "vii", "viii-a", "viii-b"];
const FOIE_DROIT = ["v", "vi", "vii", "viii-a", "viii-b"];

async function etudeFoie() {
  const segs = await Promise.all(SEGMENTS.map((s) => piece(`parties/foie-${s}`, "foie").then((p) => { p.nom = s; return p; })));
  const vesicule = await piece("vesicule", "vesicule");
  const pieces = [...segs, vesicule];
  const { groupe, corps, centre } = cadrer(pieces);
  const droit = segs.filter((p) => FOIE_DROIT.includes(p.nom));
  const centreDroit = droit.reduce((a, p) => a.add(p.centre), V()).divideScalar(droit.length);
  const gauche = segs.filter((p) => p.nom === "ii" || p.nom === "iii");
  const centreGauche = gauche.reduce((a, p) => a.add(p.centre), V()).divideScalar(gauche.length);
  const reperes = [repere("Foie droit", droit[1], centreDroit), repere("Foie gauche", gauche[0], centreGauche),
    repere("Vésicule biliaire", vesicule, vesicule.centre.clone())];
  const calculs = [[0, 0, 0], [5, 3, -4], [-4, 4, 3], [3, -5, 4], [-5, -3, -3], [1, 6, 5]].map(([x, y, z]) => {
    const b = boule(3.2 + Math.abs(x) * 0.15, 0xd8c27e);
    b.userData.base = vesicule.centre.clone().add(V(x, y, z * 1.4));
    corps.add(b);
    return b;
  });
  const mv = vesicule.mesh.material;

  return {
    groupe, corps, reperes: () => positionsReperes(corps, reperes),
    mettreAJour({ eclat, anim, e }) {
      reinitialiser(pieces);
      segs.forEach((p) => eclater(p, 14 * eclat));
      eclater(vesicule, 12 * eclat);
      let foyer = centre.clone();
      if (anim === "hepatectomie") {
        droit.forEach((p) => { eclater(p, 34 * e); p.mesh.material.emissiveIntensity = 0.22 * e; });
        foyer = centreDroit.clone();
      }
      const transparence = anim === "calculs" ? e : 0;
      mv.transparent = transparence > 0.001;
      mv.opacity = 1 - 0.62 * transparence;
      mv.depthWrite = !mv.transparent;
      calculs.forEach((b) => {
        b.scale.setScalar(Math.max(0.0001, transparence));
        b.position.copy(b.userData.base).add(vesicule.mesh.position);
      });
      if (anim === "calculs") { zone(vesicule, vesicule.centre, 40, 0.35 * e); foyer = vesicule.centre.clone(); }
      if (anim === "ablation-vesicule") {
        eclater(vesicule, 48 * e);
        vesicule.mesh.material.emissiveIntensity = 0.28 * e;
        foyer = vesicule.centre.clone().addScaledVector(vesicule.dir, 30 * e);
      }
      return corps.localToWorld(foyer.lerp(centre, 1 - e).clone());
    },
  };
}

/* ── Côlon : diverticules du sigmoïde, tumeur, colectomie ──────────────────── */
async function etudeColon() {
  const noms = [["parties/colon-droit", "colon"], ["parties/colon-transverse", "colon"], ["parties/colon-gauche", "colon"],
    ["parties/jonction", "colon"], ["rectum", "rectum"],
    ["parties/bandelette-1", "bandelette"], ["parties/bandelette-2", "bandelette"], ["parties/bandelette-3", "bandelette"]];
  const pieces = await Promise.all(noms.map(([c, t]) => piece(c, t)));
  const [droitC, transverse, gauche, , rectum] = pieces;
  const bandelettes = pieces.slice(5);
  const { groupe, corps, centre } = cadrer(pieces);
  bandelettes.forEach((b) => b.mesh.material.color.setHex(0xe9bca4));
  const reperes = [repere("Côlon droit", droitC, droitC.centre.clone()), repere("Côlon transverse", transverse, transverse.centre.clone()),
    repere("Côlon gauche", gauche, gauche.centre.clone()), repere("Rectum", rectum, rectum.centre.clone())];

  // Diverticules : petites poches sur la partie basse du côlon gauche (sigmoïde)
  const g = gauche.mesh.geometry, pos = g.attributes.position, nor = g.attributes.normal;
  const bas = Array.from({ length: pos.count }, (_, i) => i).sort((a, b) => pos.getZ(a) - pos.getZ(b));
  const bande = bas.slice(0, Math.floor(bas.length * 0.14));
  const poches = Array.from({ length: 9 }, (_, k) => {
    const i = bande[Math.floor((k + 0.5) * bande.length / 9)];
    const b = boule(4.2, 0xd99a80);
    b.userData.base = V(pos.getX(i), pos.getY(i), pos.getZ(i)).addScaledVector(V(nor.getX(i), nor.getY(i), nor.getZ(i)), 2.5);
    corps.add(b);
    return b;
  });
  const centreSigmoide = bande.reduce((a, i) => a.add(V(pos.getX(i), pos.getY(i), pos.getZ(i))), V()).divideScalar(bande.length);
  const pointTumeur = (() => {
    // Point de la face avant (−y) du côlon transverse, au milieu
    const t = transverse.mesh.geometry.attributes.position, c = transverse.centre.clone().add(V(0, -80, 0)); let best = null, d = 1e9;
    for (let i = 0; i < t.count; i += 3) {
      const v = V(t.getX(i), t.getY(i), t.getZ(i)), dd = v.distanceToSquared(c);
      if (dd < d) { d = dd; best = v; }
    }
    return best;
  })();

  return {
    groupe, corps, reperes: () => positionsReperes(corps, reperes),
    mettreAJour({ eclat, anim, e }) {
      reinitialiser(pieces);
      pieces.forEach((p) => eclater(p, (bandelettes.includes(p) ? 16 : 9) * eclat));
      bandelettes.forEach((b) => {
        const f = anim === "colectomie" ? e : 0;
        b.mesh.material.transparent = f > 0.001;
        b.mesh.material.opacity = 1 - 0.85 * f;
        b.mesh.material.depthWrite = !b.mesh.material.transparent;
      });
      let foyer = centre.clone();
      poches.forEach((b) => {
        b.position.copy(b.userData.base).add(gauche.mesh.position);
        b.scale.setScalar(Math.max(0.0001, anim === "diverticules" ? e : 0));
        b.material.emissiveIntensity = 0.45 * (anim === "diverticules" ? e : 0);
      });
      if (anim === "diverticules") { zone(gauche, centreSigmoide, 45, 0.45 * e); foyer = centreSigmoide.clone(); }
      if (anim === "zone-colon") { zone(transverse, pointTumeur, 34, 1.2 * e); foyer = pointTumeur.clone(); }
      if (anim === "colectomie") {
        eclater(gauche, 42 * e);
        gauche.mesh.material.emissiveIntensity = 0.26 * e;
        foyer = gauche.centre.clone().addScaledVector(gauche.dir, 25 * e);
      }
      return corps.localToWorld(foyer.lerp(centre, 1 - e).clone());
    },
  };
}

export const ETUDES = { oesophage: etudeOesophage, foie: etudeFoie, colon: etudeColon };
