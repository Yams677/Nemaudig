/* Nemaudig — anatomie en 3D (WebGL, three.js r160 auto-hébergé).
   Les organes sont modélisés à partir des tracés de la planche SVG
   (lib/anatomie.py › donnees_3d) : volumes extrudés arrondis pour les organes
   pleins, tubes pour le tube digestif, enveloppe du corps en verre.
   Deux usages :
   - data-planche-3d="planche" : écartement des organes autour du curseur,
     lumière qui suit la souris, rotation au glisser, survol + clic ;
   - data-planche-3d="voyage"  : caméra pilotée par le défilement (événement
     « voyage:progression » émis par main.js), halo lumineux (bloom).
   Sans WebGL, la planche SVG d'origine reste affichée. */
import * as THREE from "./vendor/three.module.min.js";
import { RoomEnvironment } from "./vendor/RoomEnvironment.js";
import { EffectComposer } from "./vendor/postprocessing/EffectComposer.js";
import { RenderPass } from "./vendor/postprocessing/RenderPass.js";
import { UnrealBloomPass } from "./vendor/postprocessing/UnrealBloomPass.js";
import { OutputPass } from "./vendor/postprocessing/OutputPass.js";
import { BokehPass } from "./vendor/postprocessing/BokehPass.js";
import { bosseler, organique, profilOesophage, profiler, ossature, passeFilm, poussieresCinema, vaisseaux } from "./anatomie3d-cinema.js";

const reduit = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
/* Mode tournage (outil tools_film.py) : l'horloge et la progression sont pilotées de l'extérieur,
   image par image, pour enregistrer un film parfaitement fluide quelle que soit la machine. */
const FILM = window.NEMAUDIG_FILM || null;
const CENTRE = new THREE.Vector3(0, 0.2, 0);

/* Profondeur, épaisseur et teinte de chaque organe (z > 0 = vers le visiteur). */
const CONF = {
  oesophage: { tube: { r: 0.07, z: (t) => -0.1 - 0.16 * t + 0.05 * Math.sin(t * Math.PI), profil: profilOesophage, hiatus: 0.74 }, couleur: 0xe3a3b3 },
  surrenales: { plein: { z: -0.55, ep: 0.05, arrondi: 0.05 }, couleur: 0xf0d27a },
  pancreas: { plein: { z: -0.32, ep: 0.1, arrondi: 0.09 }, tube: { r: 0.05, z: () => -0.16 }, couleur: 0xf2cd8f, couleurTube: 0xeeb3c0 },
  foie: { plein: { z: 0.02, ep: 0.3, arrondi: 0.2 }, couleur: 0xe7a090 },
  vesicule: { plein: { z: 0.42, ep: 0.08, arrondi: 0.08 }, couleur: 0xa9cf7c },
  estomac: { plein: { z: 0.3, ep: 0.26, arrondi: 0.22 }, couleur: 0xb39be6 },
  intestin: { tube: { r: 0.055, z: (t) => 0.02 + 0.15 * Math.sin(t * 34) }, couleur: 0xf1aebd },
  colon: { tube: { r: 0.115, z: () => 0.12, bosses: 0.15 }, couleur: 0x8fd6c0 },
  sigmoide: { tube: { r: 0.1, z: (t) => 0.12 - 0.27 * t, bosses: 0.13 }, couleur: 0x8fd6c0 },
  rectum: { tube: { r: 0.095, z: (t) => -0.15 - 0.1 * t, bosses: 0.07 }, couleur: 0x8fd6c0 },
  anus: { plein: { z: -0.25, ep: 0.04, arrondi: 0.04 }, couleur: 0xe59fb0 },
  aine: { tube: { r: 0.02, z: () => 0.5 }, couleur: 0x2bb3a7, repere: true },
  ombilic: { anneau: true, couleur: 0x2bb3a7, repere: true },
};
const GROUPES = { paroi: ["aine", "ombilic"], colon: ["colon", "sigmoide"], "colon-rectum": ["colon", "sigmoide", "rectum"],
  foie: ["foie", "vesicule", "pancreas"], estomac: ["estomac", "oesophage"], anus: ["anus", "rectum"], surrenales: ["surrenales"] };

/* ---------- Lecture des tracés SVG ---------- */
const V = (x, y) => new THREE.Vector2((x - 200) / 100, (300 - y) / 100);

function lireChemin(d) {
  const jetons = d.match(/[MCLZ]|-?\d*\.?\d+/g);
  const sous = [];
  let cmd = null, i = 0, courant = null;
  while (i < jetons.length) {
    if (/[MCLZ]/.test(jetons[i])) { cmd = jetons[i++]; if (cmd === "Z") continue; }
    const n = () => parseFloat(jetons[i++]);
    if (cmd === "M") { courant = { depart: V(n(), n()), segs: [] }; sous.push(courant); cmd = "L"; }
    else if (cmd === "C") courant.segs.push({ c: [V(n(), n()), V(n(), n()), V(n(), n())] });
    else if (cmd === "L") courant.segs.push({ l: V(n(), n()) });
  }
  return sous;
}

function echantillonner(sp, pas = 14) {
  const pts = [sp.depart.clone()];
  let p0 = sp.depart;
  for (const s of sp.segs) {
    if (s.l) { pts.push(s.l.clone()); p0 = s.l; continue; }
    const [a, b, c] = s.c;
    for (let k = 1; k <= pas; k++) {
      const t = k / pas, u = 1 - t;
      pts.push(new THREE.Vector2(
        u * u * u * p0.x + 3 * u * u * t * a.x + 3 * u * t * t * b.x + t * t * t * c.x,
        u * u * u * p0.y + 3 * u * u * t * a.y + 3 * u * t * t * b.y + t * t * t * c.y));
    }
    p0 = c;
  }
  return pts;
}

function forme(sp) {
  const f = new THREE.Shape();
  f.moveTo(sp.depart.x, sp.depart.y);
  for (const s of sp.segs) {
    if (s.l) f.lineTo(s.l.x, s.l.y);
    else f.bezierCurveTo(s.c[0].x, s.c[0].y, s.c[1].x, s.c[1].y, s.c[2].x, s.c[2].y);
  }
  f.closePath();
  return f;
}

/* ---------- Matériaux ---------- */
function matiere(couleur, repere) {
  if (repere) return new THREE.MeshStandardMaterial({ color: couleur, emissive: couleur, emissiveIntensity: 0.35, roughness: 0.4, transparent: true, opacity: 0.55 });
  return new THREE.MeshPhysicalMaterial({
    color: couleur, roughness: 0.36, metalness: 0, clearcoat: 0.85, clearcoatRoughness: 0.2,
    sheen: 0.7, sheenColor: new THREE.Color(0xffffff), sheenRoughness: 0.45,
    emissive: new THREE.Color(0x2bb3a7), emissiveIntensity: 0, transparent: true, opacity: 1,
  });
}

function enveloppe(silhouette, sombre) {
  const pts = echantillonner(lireChemin(silhouette)[0], 24).filter((p) => p.x >= 0);
  const geo = new THREE.LatheGeometry(pts.map((p) => new THREE.Vector2(Math.max(0.0001, p.x), p.y)), 96);
  geo.scale(1, 1, 0.56);
  geo.userData.profil = pts;
  const mat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, side: THREE.DoubleSide,
    uniforms: {
      uScan: { value: 9 }, uOpacite: { value: 0 },
      uRim: { value: new THREE.Color(0x2bb3a7) }, uFond: { value: new THREE.Color(sombre ? 0x0d2b36 : 0xdff3ee) },
      uBase: { value: sombre ? 0.02 : 0.05 },
    },
    vertexShader: `varying vec3 vN; varying vec3 vV; varying float vY;
      void main(){ vec4 mv = modelViewMatrix * vec4(position,1.); vN = normalize(normalMatrix*normal); vV = -mv.xyz; vY = position.y; gl_Position = projectionMatrix*mv; }`,
    fragmentShader: `uniform float uScan; uniform float uOpacite; uniform float uBase; uniform vec3 uRim; uniform vec3 uFond; varying vec3 vN; varying vec3 vV; varying float vY;
      void main(){ float f = pow(1. - abs(dot(normalize(vN), normalize(vV))), 2.4);
        float s = smoothstep(.12, 0., abs(vY - uScan));
        float l = smoothstep(.985, 1., abs(sin(vY * 26.))) * .2;
        vec3 c = mix(uFond, uRim, f) + uRim * s * .9;
        gl_FragColor = vec4(c, (uBase + f * .6 + s * .45 + l * f) * uOpacite); }`,
  });
  return new THREE.Mesh(geo, mat);
}

/* ---------- Construction ---------- */
function construire(donnees, sombre) {
  const racine = new THREE.Group();
  const organes = {};
  donnees.organes.forEach((o, rang) => {
    const conf = CONF[o.cle];
    if (!conf) return;
    const groupe = new THREE.Group();
    const mats = [];
    o.formes.forEach((f) => {
      const sous = lireChemin(f.d);
      if (f.type === "f" && conf.plein) {
        const { z, ep, arrondi } = conf.plein;
        const geo = new THREE.ExtrudeGeometry(forme(sous[0]), { depth: ep, bevelEnabled: true, bevelThickness: arrondi, bevelSize: arrondi * 0.75, bevelSegments: 8, curveSegments: 32 });
        geo.translate(0, 0, z - ep / 2);
        const m = matiere(conf.couleur, conf.repere); mats.push(m);
        if (!conf.repere) organique(m, 0.13, 8);
        groupe.add(new THREE.Mesh(geo, m));
      } else if ((f.type === "t" || f.type === "r") && conf.tube) {
        sous.forEach((sp) => {
          const pts = echantillonner(sp);
          const n = pts.length - 1;
          const courbe = new THREE.CatmullRomCurve3(pts.map((p, k) => new THREE.Vector3(p.x, p.y, conf.tube.z(k / n))));
          const geo = new THREE.TubeGeometry(courbe, Math.max(60, n * 4), conf.tube.r, 24, false);
          if (conf.tube.bosses) bosseler(geo, courbe, conf.tube.r, conf.tube.bosses);
          if (conf.tube.profil) profiler(geo, conf.tube.r, conf.tube.profil);
          const m = matiere(f.type === "t" && conf.couleurTube ? conf.couleurTube : conf.couleur, conf.repere); mats.push(m);
          if (!conf.repere) organique(m, o.cle === "oesophage" ? 0.22 : 0.07, o.cle === "oesophage" ? "vec3(34., 5., 34.)" : 14);
          groupe.add(new THREE.Mesh(geo, m));
          if (conf.tube.hiatus) {
            // Orifice du diaphragme (hiatus) : anneau lumineux autour de l'œsophage.
            const p = courbe.getPointAt(conf.tube.hiatus), tg = courbe.getTangentAt(conf.tube.hiatus);
            const mh = matiere(0x2bb3a7, true); mats.push(mh);
            const anneau = new THREE.Mesh(new THREE.TorusGeometry(conf.tube.r * 1.75, 0.011, 10, 48), mh);
            anneau.position.copy(p);
            anneau.quaternion.setFromUnitVectors(new THREE.Vector3(0, 0, 1), tg);
            groupe.add(anneau);
          }
          if (!conf.repere) {
            [0, 1].forEach((u) => {
              const pt = courbe.getPoint(u);
              const rb = conf.tube.r * (conf.tube.profil ? conf.tube.profil(u) : 1);
              const bout = new THREE.Mesh(new THREE.SphereGeometry(rb, 20, 14), m);
              bout.position.copy(pt); groupe.add(bout);
            });
          }
        });
      } else if (f.type === "o" && conf.anneau) {
        const m = matiere(conf.couleur, true); mats.push(m);
        const anneau = new THREE.Mesh(new THREE.TorusGeometry(0.06, 0.016, 12, 40), m);
        anneau.position.set(sous[0].depart.x, sous[0].depart.y, 0.62);
        groupe.add(anneau);
      }
    });
    const boite = new THREE.Box3().setFromObject(groupe);
    groupe.userData = { cle: o.cle, libelle: o.libelle, lien: o.lien, rang, mats, centre: boite.getCenter(new THREE.Vector3()), haut: boite.max.y, decalage: new THREE.Vector3() };
    organes[o.cle] = groupe;
    racine.add(groupe);
  });
  const corps = enveloppe(donnees.silhouette, sombre);
  racine.add(corps);
  if (sombre) {
    racine.add(ossature(corps.geometry.userData.profil));
    const vx = vaisseaux();
    racine.add(vx);
    corps.userData.vaisseaux = vx;
  }
  return { racine, organes, corps };
}

function socle() {
  const g = new THREE.Group();
  [1.35, 1.7, 2.1].forEach((r, i) => {
    const anneau = new THREE.Mesh(new THREE.TorusGeometry(r, 0.006, 8, 160),
      new THREE.MeshBasicMaterial({ color: 0x2bb3a7, transparent: true, opacity: [0.4, 0.2, 0.1][i] }));
    anneau.rotation.x = Math.PI / 2;
    g.add(anneau);
  });
  g.position.y = -2.75;
  return g;
}

function poussieres(n = 160) {
  const pos = new Float32Array(n * 3);
  for (let i = 0; i < n; i++) {
    pos[i * 3] = (Math.random() - 0.5) * 5;
    pos[i * 3 + 1] = (Math.random() - 0.5) * 6.4;
    pos[i * 3 + 2] = (Math.random() - 0.5) * 3;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  return new THREE.Points(geo, new THREE.PointsMaterial({ color: 0x5fd8cb, size: 0.03, transparent: true, opacity: 0.55, depthWrite: false }));
}

const easeBack = (x) => { const c = 1.5; return 1 + (c + 1) * Math.pow(x - 1, 3) + c * Math.pow(x - 1, 2); };
const lisse = (x) => x * x * (3 - 2 * x);

/* ---------- Une vue par zone ---------- */
function monter(zone, donnees) {
  const mode = zone.getAttribute("data-planche-3d");
  const voyage = mode === "voyage";
  const canvas = document.createElement("canvas");
  canvas.className = "planche3d";
  canvas.setAttribute("aria-hidden", "true");
  zone.appendChild(canvas);

  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: !voyage, powerPreference: "high-performance" });
  } catch (e) { canvas.remove(); return; }
  renderer.setPixelRatio(FILM ? 1 : Math.min(window.devicePixelRatio || 1, voyage ? 1.5 : 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = voyage ? 0.82 : 1.05;
  if (voyage) renderer.setClearColor(0x0a1a26, 1);

  const scene = new THREE.Scene();
  if (voyage) scene.background = new THREE.Color(0x07131c);
  const pmrem = new THREE.PMREMGenerator(renderer);
  scene.environment = pmrem.fromScene(new RoomEnvironment(renderer), 0.04).texture;
  scene.add(new THREE.HemisphereLight(0xffffff, voyage ? 0x0d2b36 : 0xd9e8ee, voyage ? 0.35 : 0.55));
  const cle = new THREE.DirectionalLight(0xffffff, voyage ? 1.3 : 1.7); cle.position.set(3, 5, 6); scene.add(cle);
  const contre = new THREE.DirectionalLight(0x7fe3d6, voyage ? 2.2 : 1.3); contre.position.set(-4, 2, -5); scene.add(contre);
  const torche = new THREE.PointLight(0xc8fff6, 0, 0, 1.6);
  scene.add(torche);

  const camera = new THREE.PerspectiveCamera(30, 1, 0.05, 100);
  const { racine, organes, corps } = construire(donnees, voyage);
  const pivot = new THREE.Group();
  const base = socle();
  pivot.add(racine, base);
  const etoiles = voyage ? poussieresCinema() : poussieres(150);
  scene.add(pivot, etoiles);
  const liste = Object.values(organes);

  let composer = null, bloom = null, bokeh = null, film = null, impulsion = 0, etapeVue = -1;
  if (voyage && !(FILM && FILM.sansPost)) {
    composer = new EffectComposer(renderer);
    composer.addPass(new RenderPass(scene, camera));
    if (window.innerWidth > 700 && !(FILM && FILM.sansFlou)) {
      bokeh = new BokehPass(scene, camera, { focus: 6, aperture: 0.004, maxblur: 0.009 });
      // La profondeur se calcule sans le verre, les os ni les poussières : le point se fait sur les organes.
      const rendre = bokeh.render.bind(bokeh);
      const masques = () => [corps, etoiles, base, ...racine.children.filter((o) => o !== corps && !o.userData.cle)];
      bokeh.render = (...args) => { const m = masques(); m.forEach((o) => { o.userData.vis = o.visible; o.visible = false; });
        rendre(...args); m.forEach((o) => { o.visible = o.userData.vis; }); };
      composer.addPass(bokeh);
    }
    bloom = new UnrealBloomPass(new THREE.Vector2(256, 256), 0.32, 0.4, 0.9);
    composer.addPass(bloom);
    composer.addPass(new OutputPass());
    film = passeFilm();
    composer.addPass(film);
  }

  const legende = zone.querySelector("[data-legende]");
  const ray = new THREE.Raycaster();
  const souris = new THREE.Vector2(-9, -9);
  const plan = new THREE.Plane(new THREE.Vector3(0, 0, 1), 0);
  const curseur = new THREE.Vector3(99, 99, 0);
  let dedans = false, survol = null, externe = null, visible = true, glisse = null, rotManuelle = 0;
  let ecart = 0, proche = 0;
  let progression = 0;
  let largeur = 1, hauteur = 1, distPlein = 12;
  const t0 = performance.now();

  /* Voyage : images-clés de caméra lues dans le DOM (data-camera, data-organes, data-ecarter). */
  const etapes = voyage ? Array.from(document.querySelectorAll("[data-etape-voyage]")).map((el) => {
    const cles = (el.dataset.organes || "").split(" ").filter(Boolean);
    const cam = el.dataset.camera ? el.dataset.camera.split(",").map(Number) : null;
    let cible = CENTRE.clone();
    if (cles.length) {
      const b = new THREE.Box3();
      cles.forEach((k) => organes[k] && b.expandByObject(organes[k]));
      cible = b.getCenter(new THREE.Vector3());
    }
    return { cles, cible, cam, ecarter: (el.dataset.ecarter || "").split(" ").filter(Boolean) };
  }) : [];
  if (voyage) window.addEventListener("voyage:progression", (ev) => { progression = ev.detail.f; if (visible) boucle(); });

  function ajuster() {
    largeur = zone.clientWidth; hauteur = zone.clientHeight;
    if (!largeur || !hauteur) return;
    renderer.setSize(largeur, hauteur, false);
    camera.aspect = largeur / hauteur;
    const demi = Math.tan(THREE.MathUtils.degToRad(camera.fov / 2));
    const marge = voyage ? 1.0 : (zone.classList.contains("explorer__planche") ? 1.0 : 1.15);
    distPlein = Math.max(3.15 * marge / demi, 1.7 * marge / (demi * camera.aspect));
    if (voyage) {
      // Sur grand écran, le sujet est décalé à gauche pour laisser la place au texte.
      const large = largeur > 960 && largeur > hauteur;
      camera.setViewOffset(largeur, hauteur, large ? largeur * 0.16 : 0, large ? 0 : hauteur * 0.2, largeur, hauteur);
      if (composer) composer.setSize(largeur, hauteur);
    }
    camera.updateProjectionMatrix();
  }
  new ResizeObserver(ajuster).observe(zone);
  ajuster();

  function placerLegende(groupe) {
    if (!legende) return;
    if (!groupe) { legende.classList.remove("is-visible"); return; }
    const p = new THREE.Vector3(groupe.userData.centre.x, groupe.userData.haut, groupe.userData.centre.z)
      .add(groupe.position).applyMatrix4(pivot.matrixWorld).project(camera);
    legende.textContent = groupe.userData.libelle;
    legende.style.left = `${(p.x + 1) / 2 * largeur}px`;
    legende.style.top = `${(1 - p.y) / 2 * hauteur}px`;
    legende.classList.add("is-visible");
  }

  if (!voyage) {
    canvas.addEventListener("pointerenter", () => { dedans = true; });
    canvas.addEventListener("pointerleave", () => { dedans = false; souris.set(-9, -9); });
    canvas.addEventListener("pointermove", (ev) => {
      const r = canvas.getBoundingClientRect();
      souris.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1);
      dedans = true;
      if (glisse) {
        const dx = ev.clientX - glisse.x;
        if (Math.abs(dx) > 5) glisse.bouge = true;
        rotManuelle = glisse.rot + dx * 0.009;
      }
      boucle();
    });
    canvas.addEventListener("pointerdown", (ev) => { glisse = { x: ev.clientX, rot: rotManuelle, bouge: false }; });
    // Proximité du curseur : les organes commencent à s'écarter avant même le survol.
    window.addEventListener("pointermove", (ev) => {
      const r = zone.getBoundingClientRect();
      const dx = (ev.clientX - (r.left + r.width / 2)) / r.width, dy = (ev.clientY - (r.top + r.height / 2)) / r.height;
      const d = Math.hypot(dx, dy);
      const avant = proche;
      proche = THREE.MathUtils.clamp(1 - (d - 0.25) / 0.55, 0, 1);
      if (proche !== avant && visible) boucle();
    }, { passive: true });
    window.addEventListener("pointerup", () => {
      if (glisse && !glisse.bouge && survol) window.location.href = organes[survol].userData.lien;
      glisse = null;
    });
    window.addEventListener("anatomie:survol", (ev) => {
      externe = ev.detail.actif ? ev.detail.cles.flatMap((k) => GROUPES[k] || [k]) : null;
      if (visible) boucle();
    });
  } else {
    window.addEventListener("pointermove", (ev) => {
      const r = canvas.getBoundingClientRect();
      if (ev.clientY < r.top || ev.clientY > r.bottom) return;
      souris.set(((ev.clientX - r.left) / r.width) * 2 - 1, -((ev.clientY - r.top) / r.height) * 2 + 1);
      dedans = true;
    }, { passive: true });
  }

  const io = new IntersectionObserver(([en]) => { visible = en.isIntersecting; if (visible) boucle(); }, { rootMargin: "80px" });
  io.observe(zone);
  document.addEventListener("visibilitychange", () => { if (!document.hidden) boucle(); });

  /* État cible pour l'étape de voyage en cours (interpolation continue entre deux étapes). */
  const camPos = new THREE.Vector3(0, 0.2, 12), camCible = CENTRE.clone();
  function etatVoyage(t) {
    const n = etapes.length;
    const f = THREE.MathUtils.clamp(progression, 0, n - 1);
    const i = Math.min(n - 2, Math.floor(f)), k = lisse(f - i);
    const pose = (e) => {
      if (!e.cam) return { pos: new THREE.Vector3(0, 0.2, distPlein), cible: CENTRE.clone() };
      const recul = Math.max(1, 1.05 / camera.aspect); // écrans étroits : on recule
      return { pos: e.cible.clone().add(new THREE.Vector3(...e.cam).multiplyScalar(recul)), cible: e.cible.clone() };
    };
    const a = pose(etapes[i]), b = pose(etapes[i + 1] || etapes[i]);
    const orbite = reduit ? 0 : Math.sin(t * 0.25) * 0.25;
    camPos.lerp(a.pos.lerp(b.pos, k).add(new THREE.Vector3(orbite, 0, 0)), 0.06);
    camCible.lerp(a.cible.lerp(b.cible, k), 0.06);
    // Caméra « à l'épaule » : micro-dérive et respiration de focale, comme un travelling filmé.
    const main = reduit ? 0 : 1;
    camera.position.copy(camPos).add(new THREE.Vector3(Math.sin(t * 0.7) * 0.025, Math.sin(t * 0.9 + 1) * 0.02, 0).multiplyScalar(main));
    camera.up.set(Math.sin(t * 0.33) * 0.012 * main, 1, 0);
    camera.lookAt(camCible);
    camera.fov = 30 + Math.sin(t * 0.21) * 0.8 * main;
    camera.updateProjectionMatrix();
    const n2 = Math.round(f);
    const courante = etapes[n2];
    return { allumes: courante.cles, ecarter: courante.ecarter, cible: courante.cible, plein: !courante.cles.length, n: n2 };
  }

  let enCours = false, premier = true;

  let tFilm = 0;
  function image(dessiner = true) {
    const t = FILM ? tFilm : (performance.now() - t0) / 1000;
    let allumes = [], ecarter = [], focus = null;

    if (voyage) {
      const st = etatVoyage(t);
      allumes = st.allumes; ecarter = st.ecarter; focus = st.cible;
      if (st.n !== etapeVue) { if (etapeVue >= 0) impulsion = 1; etapeVue = st.n; }
      impulsion *= 0.95;
      if (bloom) bloom.strength = 0.24 + impulsion * 0.5;
      if (bokeh) bokeh.uniforms.focus.value = camera.position.distanceTo(camCible);
      if (film) film.uniforms.uTemps.value = t;
      const vx = corps.userData.vaisseaux;
      if (vx) {
        const voir = allumes.includes("foie") || allumes.includes("pancreas") ? 0.95 : 0;
        vx.userData.mats.forEach((m) => { m.opacity += (voir - m.opacity) * 0.08; m.emissiveIntensity = 0.5 + Math.sin(t * 2.4) * 0.25; });
        vx.visible = vx.userData.mats[0].opacity > 0.01;
      }
      pivot.rotation.y += ((st.plein && !reduit ? Math.sin(t * 0.2) * 0.5 : 0) - pivot.rotation.y) * 0.04;
    } else {
      camera.position.set(0, 0.2, distPlein);
      camera.lookAt(CENTRE);
      ray.setFromCamera(souris, camera);
      const touche = ray.intersectObjects(liste, true)[0];
      let g = touche ? touche.object : null;
      while (g && !g.userData.cle) g = g.parent;
      const nouveau = g ? g.userData.cle : null;
      if (nouveau !== survol) {
        survol = nouveau;
        canvas.style.cursor = survol ? "pointer" : "grab";
        if (!survol) placerLegende(null);
      }
      if (survol) placerLegende(organes[survol]);
      allumes = survol ? [survol] : (externe || []);
      const auto = reduit || survol || glisse ? 0 : Math.sin(t * 0.32) * 0.42;
      pivot.rotation.y += ((auto + rotManuelle) - pivot.rotation.y) * 0.06;
      pivot.rotation.x += ((dedans ? souris.y * -0.08 : 0) - pivot.rotation.x) * 0.05;
    }

    /* Curseur projeté dans le repère du corps : sert à l'écartement et à la torche. */
    ray.setFromCamera(souris, camera);
    const pt = new THREE.Vector3();
    if (dedans && ray.ray.intersectPlane(plan, pt)) {
      torche.position.set(pt.x, pt.y, 1.8);
      curseur.copy(pivot.worldToLocal(pt.clone()));
    } else curseur.set(99, 99, 0);
    torche.intensity += ((dedans ? (voyage ? 3 : 9) : 0) - torche.intensity) * 0.08;
    ecart += ((voyage ? 0 : Math.max(proche, dedans ? 1 : 0)) - ecart) * 0.06;

    const quelque = allumes.length > 0;
    for (const groupe of liste) {
      const u = groupe.userData;
      const on = allumes.includes(u.cle);
      const apparition = reduit ? 1 : THREE.MathUtils.clamp((t - 0.2 - u.rang * 0.11) / 0.9, 0, 1);

      // Écartement : éclatement doux autour du centre + répulsion locale autour du curseur.
      const cible = new THREE.Vector3();
      if (!voyage) {
        cible.copy(u.centre).sub(CENTRE).multiplyScalar(0.5 * ecart);
        cible.z += (u.centre.z > 0 ? 0.6 : -0.5) * ecart;
        cible.y += Math.sin(t * 1.3 + u.rang) * 0.04 * ecart;
        const d = new THREE.Vector2(u.centre.x - curseur.x, u.centre.y - curseur.y);
        const force = Math.pow(Math.max(0, 1 - d.length() / 1.5), 2);
        if (u.cle === survol) cible.z += 0.8;
        else if (force > 0 && d.length() > 0.001) cible.add(new THREE.Vector3(d.x, d.y, 0.4).normalize().multiplyScalar(force * 0.7));
      } else if (ecarter.includes(u.cle) && focus) {
        const d = u.centre.clone().sub(focus); d.z = 0;
        cible.copy(d.normalize().multiplyScalar(1.1)).add(new THREE.Vector3(0, 0, 0.6));
      }
      u.decalage.lerp(cible, 0.09);
      groupe.position.copy(u.decalage);

      const echelle = (reduit ? 1 : easeBack(apparition)) * (on ? 1.05 : 1);
      groupe.scale.lerp(new THREE.Vector3(echelle, echelle, echelle), apparition < 1 ? 1 : 0.15);
      for (const m of u.mats) {
        const pleine = m.isMeshPhysicalMaterial ? 1 : 0.55;
        const opac = (quelque && !on ? (voyage ? 0.1 : 0.22) : pleine) * apparition;
        m.opacity += (opac - m.opacity) * 0.12;
        if (m.isMeshPhysicalMaterial) m.emissiveIntensity += ((on ? (voyage ? 0.03 : 0.38) : 0) - m.emissiveIntensity) * 0.12;
        else m.emissiveIntensity += ((on ? 1.2 : 0.35) - m.emissiveIntensity) * 0.12;
        m.depthWrite = m.opacity > 0.9;
      }
    }

    corps.material.uniforms.uOpacite.value = reduit ? 1 : Math.min(1, t / 1.2);
    corps.material.uniforms.uScan.value = reduit ? 9 : (voyage && focus && allumes.length)
      ? focus.y + Math.sin(t * 1.1) * 0.55
      : 3.2 - ((t * 0.5) % 1) * 6.6;
    if (etoiles.material.uniforms) etoiles.material.uniforms.uTemps.value = t;
    base.rotation.y = t * 0.15;
    etoiles.rotation.y = t * 0.03;
    etoiles.position.y = Math.sin(t * 0.4) * 0.06;

    if (!dessiner) return;
    if (composer) composer.render(); else renderer.render(scene, camera);
    if (premier) { premier = false; zone.classList.add("is-3d"); }
  }

  function boucle() {
    if (enCours || (FILM && voyage)) return;
    enCours = true;
    const pas = () => {
      if (!visible || document.hidden) { enCours = false; return; }
      image();
      requestAnimationFrame(pas);
    };
    requestAnimationFrame(pas);
  }
  if (FILM && voyage) {
    // Deux pas de simulation à 60 Hz par image à 30 i/s : mêmes amortis que sur le site.
    FILM.rendre = (t, f) => {
      progression = f;
      tFilm = t - 1 / 60; image(false);
      tFilm = t; image(true);
      return canvas;
    };
    return;
  }
  boucle();
}

const source = document.getElementById("anatomie-donnees");
const zones = Array.from(document.querySelectorAll("[data-planche-3d]"));
if (source && zones.length) {
  const essai = document.createElement("canvas");
  if (essai.getContext("webgl2") || essai.getContext("webgl")) {
    const donnees = JSON.parse(source.textContent);
    zones.forEach((z) => { try { monter(z, donnees); } catch (err) { console.warn("Anatomie 3D indisponible :", err); } });
  }
}
