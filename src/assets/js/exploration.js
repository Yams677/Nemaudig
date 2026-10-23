/* Nemaudig — maquette B « Exploration intérieure ».
   Ouverture : les vrais organes assemblés. Le scroll fait plonger la caméra dans l'œsophage,
   puis la conduit à l'intérieur du tube jusqu'au rectum. Ensuite : visionneuse d'organes. */
import * as THREE from "./vendor/three.module.min.js";
import { chargerOrgane, matiere, eclairer } from "./organes3d.js";
import { creerTunnel, placer } from "./tunnel.js";
import { ETUDES } from "./etude.js";

const $ = (s, r = document) => r.querySelector(s);
const $$ = (s, r = document) => Array.from(r.querySelectorAll(s));
const DONNEES = JSON.parse($("#donnees").textContent);
const CALME = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const PETIT = window.matchMedia("(max-width: 860px)").matches;
// Contrôle visuel (captures sans défilement) : ?p=0.3 fige la progression du voyage,
// ?arret=foie&q=0.5 fige un arrêt.
const PARAMS = new URLSearchParams(location.search);
const FIGE = PARAMS.get("p");
const FIGE_ARRET = PARAMS.get("arret");
const lisse = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };

// Chronologie du défilement, en hauteurs d'écran (vh) : ouverture, puis trajets qui
// ralentissent à l'approche de chaque arrêt, et arrêts qui tiennent plusieurs écrans.
const OUV = { titre: 47, plongeeDebut: 16, plongeeFin: 84, voileHaut: 92, fin: 92 };
const LONG = { arretRiche: 340, arretSimple: 170, parU: 560, trajetMin: 60, fin: 45 };
const DERIVE = 0.004;     // la caméra avance encore un peu pendant l'arrêt
const PATHOS = { riche: [0.3, 0.86], simple: [0.3, 1] };
const douce = (t) => 0.5 - 0.5 * Math.cos(Math.PI * t);

function chronologie(stations) {
  const items = [{ type: "ouverture", long: OUV.fin }];
  let u = 0;
  stations.forEach((st, i) => {
    const arrivee = st.u - DERIVE;
    items.push({ type: "trajet", u0: u, u1: arrivee, long: Math.max(LONG.trajetMin, (arrivee - u) * LONG.parU), premier: i === 0 });
    items.push({ type: "arret", i, st, long: st.riche ? LONG.arretRiche : LONG.arretSimple });
    u = st.u + DERIVE;
  });
  items.push({ type: "trajet", u0: u, u1: 1, long: (1 - u) * LONG.parU, premier: false });
  items.push({ type: "fin", long: LONG.fin });
  let debut = 0;
  for (const it of items) { it.debut = debut; debut += it.long; }
  return { items, total: debut };
}

function etatA(chrono, y) {
  for (const it of chrono.items) {
    if (y < it.debut + it.long || it.type === "fin") {
      const k = Math.min(1, Math.max(0, (y - it.debut) / it.long));
      if (it.type === "ouverture") return { type: "ouverture", u: 0 };
      if (it.type === "trajet") return { type: "trajet", u: it.u0 + (it.u1 - it.u0) * douce(k), k, premier: it.premier, vh: y - it.debut };
      if (it.type === "arret") return { type: "arret", i: it.i, st: it.st, q: k, u: it.st.u - DERIVE + 2 * DERIVE * k };
      return { type: "fin", k, u: 1 };
    }
  }
  return { type: "fin", k: 1, u: 1 };
}

function creerRendu(canvas, alpha) {
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha, powerPreference: "high-performance" });
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, PETIT ? 1.5 : 1.75));
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.05;
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  return renderer;
}

function webglDispo() {
  try { const c = document.createElement("canvas"); return !!(c.getContext("webgl2") || c.getContext("webgl")); } catch { return false; }
}

/* ── Visionneuse : un organe à la fois ─────────────────────────────────────── */
function visionneuse() {
  const canvas = $(".visionneuse__canvas");
  const etat = $(".visionneuse__etat");
  const renderer = creerRendu(canvas, true);
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(30, 1, 0.1, 50);
  camera.position.set(0, 0, 6);
  eclairer(scene, renderer, { cle: 2.6, contre: 2 });
  const pivot = new THREE.Group();
  scene.add(pivot);
  let courant = null, visible = false, lacet = 0.4, tangage = 0.1, vLacet = CALME ? 0 : 0.12, glisse = null;

  const taille = () => {
    const w = canvas.clientWidth, h = canvas.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    camera.fov = w / h < 0.9 ? 40 : 30;
    camera.updateProjectionMatrix();
  };
  new ResizeObserver(taille).observe(canvas);

  async function montrer(cle) {
    etat.textContent = "Chargement du modèle…";
    const geo = await chargerOrgane(cle);
    const mesh = new THREE.Mesh(geo, matiere(cle));
    mesh.rotation.x = -Math.PI / 2;
    const boite = new THREE.Box3().setFromObject(mesh);
    const centre = boite.getCenter(new THREE.Vector3());
    const dim = boite.getSize(new THREE.Vector3());
    const echelle = 2.5 / Math.max(dim.x, dim.y, dim.z);
    const conteneur = new THREE.Group();
    mesh.position.sub(centre);
    conteneur.add(mesh);
    conteneur.scale.setScalar(echelle);
    if (courant) pivot.remove(courant);
    pivot.add(conteneur);
    courant = conteneur;
    etat.textContent = "";
  }

  canvas.addEventListener("pointerdown", (ev) => { glisse = { x: ev.clientX, y: ev.clientY }; canvas.setPointerCapture(ev.pointerId); });
  canvas.addEventListener("pointermove", (ev) => {
    if (!glisse) return;
    lacet += (ev.clientX - glisse.x) * 0.008;
    tangage = Math.max(-0.9, Math.min(0.9, tangage + (ev.clientY - glisse.y) * 0.006));
    glisse = { x: ev.clientX, y: ev.clientY };
  });
  const lacher = () => { glisse = null; };
  canvas.addEventListener("pointerup", lacher);
  canvas.addEventListener("pointercancel", lacher);
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; }, { rootMargin: "100px" }).observe(canvas);

  const boutons = $$(".organe-choix");
  const fiches = $$(".fiche-organe");
  function choisir(cle) {
    boutons.forEach((b) => b.setAttribute("aria-pressed", String(b.dataset.modele === cle)));
    fiches.forEach((f) => { f.hidden = f.dataset.fiche !== cle; });
    montrer(cle).catch(() => { etat.textContent = "Modèle indisponible"; });
  }
  boutons.forEach((b) => b.addEventListener("click", () => choisir(b.dataset.modele)));
  choisir("foie");

  return {
    choisir,
    rendre(dt) {
      if (!visible) return;
      if (!glisse) lacet += vLacet * dt;
      pivot.rotation.set(tangage, lacet, 0);
      renderer.render(scene, camera);
    },
  };
}

/* ── Voyage : ouverture, plongée, tunnel et arrêts ─────────────────────────── */
function voyage(choisirOrgane) {
  const section = $(".voyage");
  const scene3d = $(".voyage__scene");
  const canvas = $(".voyage__canvas");
  const renderer = creerRendu(canvas, true);
  const camera = new THREE.PerspectiveCamera(30, 1, 0.05, 160);
  const chrono = chronologie(DONNEES.stations);

  // Ouverture : organes réels assemblés
  const sceneOrganes = new THREE.Scene();
  eclairer(sceneOrganes, renderer);
  const assemblage = new THREE.Group();
  const corps = new THREE.Group();
  corps.rotation.x = -Math.PI / 2;
  corps.scale.setScalar(0.01);
  assemblage.add(corps);
  sceneOrganes.add(assemblage);
  const maillages = [];
  const hautLocal = new THREE.Vector3(0, 0, 0);

  Promise.all(DONNEES.modeles.map((cle) => chargerOrgane(cle).then((geo) => {
    const m = new THREE.Mesh(geo, matiere(cle));
    m.userData.cle = cle;
    corps.add(m);
    maillages.push(m);
  }))).then(() => {
    // Centre de l'assemblage calculé dans le repère BodyParts3D (mm, Z vers le haut)
    const boite = new THREE.Box3();
    maillages.forEach((m) => { m.geometry.computeBoundingBox(); boite.union(m.geometry.boundingBox); });
    const c = boite.getCenter(new THREE.Vector3());
    corps.position.set(-c.x * 0.01, -c.z * 0.01, c.y * 0.01);
    const bo = maillages.find((m) => m.userData.cle === "oesophage").geometry.boundingBox;
    hautLocal.set((bo.min.x + bo.max.x) / 2, (bo.min.y + bo.max.y) / 2, bo.max.z);
  }).catch(() => {});

  // Tunnel
  const sceneTunnel = new THREE.Scene();
  const tunnel = creerTunnel(PETIT ? { anneaux: 900, cotes: 64 } : { anneaux: 1500, cotes: 96 });
  sceneTunnel.add(tunnel.maillage);

  // Arrêts complets : une scène par organe étudié, chargée en arrière-plan
  const sceneEtude = new THREE.Scene();
  eclairer(sceneEtude, renderer, { cle: 2.5, contre: 2 });
  const etudes = {};
  Object.entries(ETUDES).forEach(([cle, creer]) => creer().then((et) => { et.groupe.visible = false; sceneEtude.add(et.groupe); etudes[cle] = et; }).catch(() => {}));
  const camEtude = new THREE.PerspectiveCamera(30, 1, 0.1, 60);
  const foyerLisse = new THREE.Vector3();
  // Repères anatomiques posés sur l'organe éclaté (étiquettes HTML projetées)
  const calqueReperes = document.createElement("div");
  calqueReperes.className = "reperes";
  calqueReperes.setAttribute("aria-hidden", "true");
  scene3d.append(calqueReperes);
  const etiquettesReperes = new Map();
  const centreEcran = new THREE.Vector3();
  function poserReperes(et, opacite) {
    calqueReperes.style.opacity = opacite.toFixed(3);
    if (opacite < 0.01) return;
    const w = scene3d.clientWidth, h = scene3d.clientHeight;
    centreEcran.setFromMatrixPosition(et.groupe.matrixWorld).project(camEtude);
    const vus = new Set();
    for (const { nom, monde } of et.reperes()) {
      let el = etiquettesReperes.get(nom);
      if (!el) {
        el = document.createElement("p");
        el.className = "repere";
        el.innerHTML = "<span></span>";
        el.firstChild.textContent = nom;
        calqueReperes.append(el);
        etiquettesReperes.set(nom, el);
      }
      const v = monde.project(camEtude);
      el.classList.toggle("repere--gauche", v.x < centreEcran.x);
      el.style.transform = `translate(${((v.x + 1) / 2) * w}px, ${((1 - v.y) / 2) * h}px)`;
      el.hidden = false;
      vus.add(nom);
    }
    etiquettesReperes.forEach((el, nom) => { if (!vus.has(nom)) el.hidden = true; });
  }

  // Survol / clic sur un organe de l'ouverture
  const etiquette = document.createElement("p");
  etiquette.className = "etiquette-3d";
  etiquette.setAttribute("aria-hidden", "true");
  scene3d.append(etiquette);
  const rayon = new THREE.Raycaster();
  const souris = new THREE.Vector2(9, 9);
  let survole = null;
  const NOMS = Object.fromEntries($$(".organe-choix").map((b) => [b.dataset.modele, b.textContent]));
  canvas.addEventListener("pointermove", (ev) => {
    const r = canvas.getBoundingClientRect();
    souris.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1);
    etiquette.style.transform = `translate(${ev.clientX - r.left + 18}px, ${ev.clientY - r.top + 14}px)`;
  });
  canvas.addEventListener("pointerleave", () => souris.set(9, 9));
  canvas.addEventListener("click", () => {
    if (!survole) return;
    choisirOrgane(survole);
    $("#organes").scrollIntoView({ behavior: CALME ? "auto" : "smooth" });
  });

  // Mise en page : la hauteur de la section suit la chronologie
  let large = true, vh = window.innerHeight / 100;
  const taille = () => {
    const w = scene3d.clientWidth, h = scene3d.clientHeight;
    renderer.setSize(w, h, false);
    camera.aspect = camEtude.aspect = w / h;
    large = w / h > 1.05;
    camera.updateProjectionMatrix();
    camEtude.updateProjectionMatrix();
    vh = h / 100;
    section.style.height = `${Math.round((chrono.total + 100) * vh)}px`;
  };
  new ResizeObserver(taille).observe(scene3d);
  taille();

  // Stations et rail
  const stations = $$(".station").map((el, i) => ({ el, pathos: $$(".patho", el), ...DONNEES.stations[i] }));
  const rail = $(".rail");
  const jalons = $$(".rail li");
  const pct = $(".rail__pct");
  let active = null, pathoActive = -1, phaseActive = "";

  const viser = (y) => {
    const haut = section.getBoundingClientRect().top + window.scrollY;
    window.scrollTo({ top: haut + y * vh, behavior: CALME ? "auto" : "smooth" });
  };
  $$('a[href="#voyage-depart"]').forEach((a) => a.addEventListener("click", (ev) => { ev.preventDefault(); viser(OUV.fin + 30); }));

  let yLisse = 0, visible = true, t = 0;
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; }).observe(section);
  const camHero = new THREE.Vector3(), cible = new THREE.Vector3(), tmp = new THREE.Vector3();

  function rendreOuverture(y, dt) {
    const plonge = lisse(OUV.plongeeDebut, OUV.plongeeFin, y);
    const balance = CALME ? 0 : Math.sin(t * 0.22) * 0.32;
    assemblage.rotation.y = balance * (1 - plonge);
    camHero.set(0, 0.2, large ? 14 : 21);
    const demiLarg = Math.tan(THREE.MathUtils.degToRad(15)) * camHero.z * camera.aspect;
    assemblage.position.set(large ? demiLarg * 0.5 : 0, large ? 0.15 : 2.1, 0);
    assemblage.updateMatrixWorld(true);
    const haut = corps.localToWorld(tmp.copy(hautLocal));
    const entree = haut.clone().add(new THREE.Vector3(0, 0.22, 0.02));
    camera.position.lerpVectors(camHero, entree, plonge * plonge);
    const fond = haut.clone().add(new THREE.Vector3(0, -2, -0.15));
    cible.set(0, 0, 0).lerp(haut, Math.min(1, plonge * 1.6)).lerp(fond, lisse(0.55, 1, plonge));
    camera.up.set(0, 1, 0).lerp(new THREE.Vector3(0, 0, -1), lisse(0.5, 1, plonge)).normalize();
    camera.fov = 30 + plonge * 20;
    camera.updateProjectionMatrix();
    camera.lookAt(cible);

    survole = null;
    if (plonge < 0.05 && maillages.length) {
      rayon.setFromCamera(souris, camera);
      const hit = rayon.intersectObjects(maillages, false)[0];
      survole = hit ? hit.object.userData.cle : null;
    }
    for (const m of maillages) {
      const but = m.userData.cle === survole ? 0.22 : 0;
      m.material.emissiveIntensity += (but - m.material.emissiveIntensity) * Math.min(1, dt * 8);
    }
    canvas.style.cursor = survole ? "pointer" : "";
    etiquette.textContent = survole ? `${NOMS[survole]} — voir en 3D` : "";
    etiquette.classList.toggle("is-on", !!survole);
    renderer.render(sceneOrganes, camera);
  }

  function rendreTunnel(u) {
    camera.fov = PETIT && !large ? 78 : 64;
    camera.updateProjectionMatrix();
    placer(camera, tunnel, Math.min(1, u) * 0.985);
    renderer.render(sceneTunnel, camera);
  }

  function rendreEtude(st, q, dt) {
    const et = etudes[st.cle];
    if (!et) return false;
    Object.values(etudes).forEach((x) => { x.groupe.visible = x === et; });
    const [a, b] = PATHOS.riche;
    const n = st.anims.length;
    const x = (q - a) / (b - a);
    const i = Math.min(n - 1, Math.floor(x * n));
    const local = x * n - i;
    const e = x < 0 || x > 1 ? 0 : lisse(0, 0.2, local) * (1 - lisse(0.82, 1, local));
    const eclat = lisse(0.16, 0.3, q) * (1 - lisse(0.84, 0.9, q));
    // L'organe : à droite sur grand écran, en haut sur mobile
    const demiH = Math.tan(THREE.MathUtils.degToRad(15)) * 10;
    et.groupe.position.set(large ? demiH * camEtude.aspect * 0.5 : 0, large ? 0.1 : demiH * 0.5, 0);
    et.groupe.rotation.y = -0.5 + q * 1.0;
    et.groupe.updateMatrixWorld(true);
    const foyer = et.mettreAJour({ eclat, anim: x >= 0 && x <= 1 ? st.anims[i] : null, e, temps: t });
    foyerLisse.lerp(foyer, CALME || FIGE_ARRET ? 1 : Math.min(1, dt * 3));
    const recul = large ? 10 : 15;
    // On garde l'organe à sa place et on se rapproche doucement de la zone concernée
    camEtude.position.set(foyerLisse.x * 0.3, foyerLisse.y * 0.3 + 0.3, recul * (1 - 0.14 * e));
    camEtude.lookAt(foyerLisse.x * 0.3, foyerLisse.y * 0.3, 0);
    renderer.render(sceneEtude, camEtude);
    // Les repères se montrent pendant l'éclatement, puis s'effacent devant la pathologie
    poserReperes(et, large ? eclat * (1 - 0.7 * e) : 0);
    return true;
  }

  function hud(etat) {
    const u = etat.u ?? 0;
    const dans = etat.type !== "ouverture" && etat.type !== "fin";
    rail.style.setProperty("--rail", dans ? "1" : "0");
    rail.style.setProperty("--p", Math.min(1, u).toFixed(4));
    pct.textContent = `${String(Math.round(Math.min(1, u) * 100)).padStart(3, "0")} %`;
    jalons.forEach((j, i) => j.classList.toggle("is-passe", u >= stations[i].u - 0.01));
    const st = etat.type === "arret" ? stations[etat.i] : null;
    if (st !== active) {
      active?.el.classList.remove("is-active");
      st?.el.classList.add("is-active");
      active = st; pathoActive = -1; phaseActive = "";
    }
    if (!st) return;
    const [a, b] = st.riche ? PATHOS.riche : PATHOS.simple;
    const n = st.pathos.length;
    const phase = etat.q < a ? "intro" : etat.q < b ? "patho" : "sortie";
    const i = phase === "patho" ? Math.min(n - 1, Math.floor(((etat.q - a) / (b - a)) * n)) : -1;
    if (phase !== phaseActive) { st.el.dataset.phase = phase; phaseActive = phase; }
    if (i !== pathoActive) { st.pathos.forEach((li, k) => li.classList.toggle("is-on", k === i)); pathoActive = i; }
  }

  return function rendre(dt) {
    if (!visible) return;
    t += dt;
    let yCible;
    if (FIGE_ARRET) {
      const it = chrono.items.find((x) => x.type === "arret" && x.st.cle === FIGE_ARRET);
      yCible = it.debut + it.long * +(PARAMS.get("q") ?? 0.5);
    } else if (FIGE !== null) yCible = +FIGE * chrono.total;
    else yCible = Math.min(chrono.total, Math.max(0, -section.getBoundingClientRect().top / vh));
    yLisse = CALME || FIGE !== null || FIGE_ARRET ? yCible : yLisse + (yCible - yLisse) * Math.min(1, dt * 5);
    const y = Math.abs(yCible - yLisse) < 0.01 ? yCible : yLisse;
    const etat = etatA(chrono, y);

    // Voile (fondus au noir entre les mondes) et sortie du titre
    let voile = 0;
    if (etat.type === "ouverture") voile = lisse(OUV.plongeeFin - 26, OUV.voileHaut, y);
    else if (etat.type === "trajet" && etat.premier) voile = 1 - lisse(0, 26, etat.vh);
    else if (etat.type === "arret" && etat.st.riche) voile = lisse(0, 0.08, etat.q) * (1 - lisse(0.1, 0.18, etat.q)) + lisse(0.86, 0.92, etat.q) * (1 - lisse(0.92, 1, etat.q));
    else if (etat.type === "fin") voile = lisse(0, 1, etat.k);
    scene3d.style.setProperty("--voile", Math.min(1, voile).toFixed(3));
    scene3d.style.setProperty("--sortie", lisse(0, OUV.titre, etat.type === "ouverture" ? y : OUV.titre).toFixed(3));
    scene3d.classList.toggle("en-etude", etat.type === "arret" && etat.st.riche && etat.q >= 0.09 && etat.q < 0.92);

    if (etat.type === "ouverture") { calqueReperes.style.opacity = "0"; rendreOuverture(y, dt); }
    else {
      etiquette.classList.remove("is-on");
      canvas.style.cursor = "";
      const etude = etat.type === "arret" && etat.st.riche && etat.q >= 0.09 && etat.q < 0.92;
      if (!(etude && rendreEtude(etat.st, etat.q, dt))) { calqueReperes.style.opacity = "0"; rendreTunnel(etat.u); }
    }
    hud(etat);
  };
}

/* ── Orientation ───────────────────────────────────────────────────────────── */
function orientation() {
  const signes = $$(".signe");
  const lectures = $$("[data-lecture]");
  signes.forEach((b) => b.addEventListener("click", () => {
    const actif = b.getAttribute("aria-pressed") === "true";
    signes.forEach((s) => s.setAttribute("aria-pressed", "false"));
    if (!actif) b.setAttribute("aria-pressed", "true");
    const cle = actif ? "vide" : b.dataset.signe;
    lectures.forEach((l) => { l.hidden = l.dataset.lecture !== cle; });
    if (!actif && window.matchMedia("(max-width: 860px)").matches) $(".releve").scrollIntoView({ behavior: CALME ? "auto" : "smooth", block: "start" });
  }));
}

/* ── Rendez-vous : chirurgien → canal → confirmation (rien n'est saisi ni envoyé) ── */
function rendezVous() {
  const module = $(".rdv");
  if (!module) return { choisir() {} };
  const aller = (n) => { module.dataset.etape = String(n); };
  const medecins = $$('input[name="rdv-medecin"]', module);
  const canaux = $$('input[name="rdv-canal"]', module);
  const uzes = $('[data-seulement="dr-david-amielh"]', module);
  let nom = "Nemaudig";
  const majRecap = () => {
    const canal = canaux.find((c) => c.checked)?.value;
    $$("[data-canal]", module).forEach((b) => { b.hidden = b.dataset.canal !== canal; });
    $$("[data-recherche]", module).forEach((r) => { r.textContent = nom; });
  };
  medecins.forEach((m) => m.addEventListener("change", () => {
    nom = m.dataset.nom;
    uzes.hidden = m.value !== "dr-david-amielh";
    canaux.forEach((c) => { c.checked = false; });
    aller(2);
  }));
  canaux.forEach((c) => c.addEventListener("change", () => { majRecap(); aller(3); }));
  $$("[data-aller]", module).forEach((b) => b.addEventListener("click", () => aller(+b.dataset.aller)));
  const copier = $(".rdv__copier", module);
  copier.addEventListener("click", async () => {
    try { await navigator.clipboard.writeText(nom); copier.textContent = "Copié"; } catch { copier.textContent = "Sélectionnez le nom"; }
    setTimeout(() => { copier.textContent = "Copier"; }, 1800);
  });
  uzes.hidden = true;
  // Depuis une carte chirurgien (voyage, équipe) : on présélectionne
  const choisir = (slug) => {
    const m = medecins.find((x) => x.value === slug);
    if (m) { m.checked = true; m.dispatchEvent(new Event("change")); }
  };
  $$("[data-rdv]").forEach((a) => a.addEventListener("click", () => choisir(a.dataset.rdv)));
  return { choisir };
}

/* ── Apparitions : titres et blocs entrent une fois, sans rebond ─────────────── */
function apparitions() {
  const cibles = $$(".organes h2, .organes__tete p, .visionneuse, .orientation h2, .signe, .equipe h2, .equipe__tete p, .portrait, .parcours h2, .etapes li, .journal article, .contact h2, .rdv, .contact__fiche > div");
  if (CALME || !("IntersectionObserver" in window)) return;
  cibles.forEach((el) => {
    el.classList.add("revele");
    const freres = Array.from(el.parentElement.children).filter((x) => x.matches(el.tagName));
    el.style.setProperty("--d", `${Math.min(8, freres.indexOf(el)) * 70}ms`);
  });
  const io = new IntersectionObserver((entrees) => entrees.forEach((en) => {
    if (en.isIntersecting) { en.target.classList.add("vu"); io.unobserve(en.target); }
  }), { rootMargin: "0px 0px -8% 0px" });
  cibles.forEach((el) => io.observe(el));
}

/* ── Démarrage ─────────────────────────────────────────────────────────────── */
orientation();
rendezVous();
apparitions();
if (!webglDispo()) {
  document.documentElement.classList.add("sans-3d");
} else {
  const vue = visionneuse();
  $$("[data-voir]").forEach((a) => a.addEventListener("click", () => vue.choisir(a.dataset.voir)));
  const voy = voyage(vue.choisir);
  let avant = performance.now();
  const boucle = (maintenant) => {
    const dt = Math.min(0.05, (maintenant - avant) / 1000);
    avant = maintenant;
    if (!document.hidden) { voy(dt); vue.rendre(dt); }
    requestAnimationFrame(boucle);
  };
  requestAnimationFrame(boucle);
}
