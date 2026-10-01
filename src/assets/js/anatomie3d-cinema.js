/* Nemaudig — détails anatomiques et effets cinématographiques de la 3D.
   Utilisé par anatomie3d.js. Tout est procédural : aucune texture à charger. */
import * as THREE from "./vendor/three.module.min.js";
import { ShaderPass } from "./vendor/postprocessing/ShaderPass.js";

const V = (x, y, z = 0) => new THREE.Vector3((x - 200) / 100, (300 - y) / 100, z);

/* Bosselures du côlon (haustrations) : on module le rayon du tube le long de sa longueur. */
export function bosseler(geo, courbe, rayon, amplitude, pas = 0.21) {
  const { tubularSegments: ts, radialSegments: rs } = geo.parameters;
  const nb = Math.max(2, Math.round(courbe.getLength() / pas));
  const pos = geo.attributes.position, nor = geo.attributes.normal;
  const v = new THREE.Vector3(), n = new THREE.Vector3();
  for (let i = 0; i <= ts; i++) {
    const u = i / ts;
    const repli = Math.pow(Math.abs(Math.sin(Math.PI * u * nb)), 0.55); // creux marqués entre les bosses
    const d = rayon * amplitude * (repli - 0.5);
    for (let j = 0; j <= rs; j++) {
      const k = i * (rs + 1) + j;
      v.fromBufferAttribute(pos, k); n.fromBufferAttribute(nor, k);
      v.addScaledVector(n, d);
      pos.setXYZ(k, v.x, v.y, v.z);
    }
  }
  pos.needsUpdate = true;
  geo.computeVertexNormals();
  return geo;
}

/* Profil de rayon le long d'un tube : multiplicateur f(u) appliqué à chaque anneau (u de 0 à 1). */
export function profiler(geo, rayon, f) {
  const { tubularSegments: ts, radialSegments: rs } = geo.parameters;
  const pos = geo.attributes.position, nor = geo.attributes.normal;
  const v = new THREE.Vector3(), n = new THREE.Vector3();
  for (let i = 0; i <= ts; i++) {
    const d = rayon * (f(i / ts) - 1);
    for (let j = 0; j <= rs; j++) {
      const k = i * (rs + 1) + j;
      v.fromBufferAttribute(pos, k); n.fromBufferAttribute(nor, k);
      v.addScaledVector(n, d);
      pos.setXYZ(k, v.x, v.y, v.z);
    }
  }
  pos.needsUpdate = true;
  geo.computeVertexNormals();
  return geo;
}

/* Œsophage : fin en haut, rétrécissements naturels, renflement avant l'estomac, fins anneaux musculaires. */
const cloche = (u, c, l) => Math.exp(-Math.pow((u - c) / l, 2));
export const profilOesophage = (u) =>
  (1 - 0.28 * cloche(u, 0.04, 0.06) - 0.16 * cloche(u, 0.36, 0.05) - 0.18 * cloche(u, 0.78, 0.035)
    + 0.42 * cloche(u, 0.93, 0.06)) * (1 + 0.012 * Math.sin(u * Math.PI * 130));

/* Surface organique : légère perturbation des normales par un bruit 3D (aspect vivant, satiné). */
const BRUIT = `
float n3h(vec3 p){ return fract(sin(dot(p, vec3(127.1,311.7,74.7))) * 43758.5453); }
float n3(vec3 p){ vec3 i=floor(p), f=fract(p); f=f*f*(3.-2.*f);
  return mix(mix(mix(n3h(i),n3h(i+vec3(1,0,0)),f.x), mix(n3h(i+vec3(0,1,0)),n3h(i+vec3(1,1,0)),f.x),f.y),
             mix(mix(n3h(i+vec3(0,0,1)),n3h(i+vec3(1,0,1)),f.x), mix(n3h(i+vec3(0,1,1)),n3h(i+vec3(1,1,1)),f.x),f.y), f.z); }
float fbm3(vec3 p){ return .55*n3(p) + .3*n3(p*2.07) + .15*n3(p*4.13); }`;

export function organique(mat, force = 0.1, echelle = 9.0) {
  const ech = typeof echelle === "number" ? `vec3(${echelle.toFixed(1)})` : echelle; // nombre, ou vec3 GLSL pour un relief étiré
  mat.onBeforeCompile = (sh) => {
    sh.vertexShader = sh.vertexShader
      .replace("#include <common>", "#include <common>\nvarying vec3 vPosOrg;")
      .replace("#include <begin_vertex>", "#include <begin_vertex>\nvPosOrg = position;");
    sh.fragmentShader = sh.fragmentShader
      .replace("#include <common>", `#include <common>\nvarying vec3 vPosOrg;${BRUIT}`)
      .replace("#include <normal_fragment_maps>", `#include <normal_fragment_maps>
        vec3 qq = vPosOrg * ${ech};
        normal = normalize(normal + ${force.toFixed(3)} * vec3(fbm3(qq) - .5, fbm3(qq + 4.7) - .5, fbm3(qq + 9.1) - .5));`);
  };
  mat.customProgramCacheKey = () => `organique-${force}-${ech}`;
  return mat;
}

/* Côtes et colonne en filigrane, calées sur le profil de l'enveloppe. */
export function ossature(profil) {
  const g = new THREE.Group();
  const mat = new THREE.MeshStandardMaterial({ color: 0x8fe3d8, emissive: 0x2bb3a7, emissiveIntensity: 0.25,
    roughness: 0.3, transparent: true, opacity: 0.055, depthWrite: false });
  const rayonA = (y) => {
    let best = profil[0];
    for (const p of profil) if (Math.abs(p.y - y) < Math.abs(best.y - y)) best = p;
    return best.x;
  };
  for (let k = 0; k < 7; k++) {
    const y = 1.72 - k * 0.19;
    const r = rayonA(y) * 0.9;
    const pts = [];
    for (let a = -0.85; a <= 0.85 + 1e-6; a += 0.05) {
      const ang = Math.PI * a;
      pts.push(new THREE.Vector3(Math.sin(ang) * r, y - Math.cos(ang) * 0.18 + 0.18, Math.cos(ang) * r * 0.52));
    }
    g.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 64, 0.016, 6, false), mat));
  }
  const vert = new THREE.SphereGeometry(0.075, 14, 10);
  vert.scale(1.3, 0.75, 1);
  for (let y = 2.35; y > -1.9; y -= 0.2) {
    const m = new THREE.Mesh(vert, mat);
    m.position.set(0, y, -0.5 + Math.max(0, y - 1.2) * 0.05);
    g.add(m);
  }
  return g;
}

/* Pédicule du foie : artère, veine porte et canal biliaire (fiche « Le foie » : chaque moitié
   est alimentée par une artère, une veine et un canal biliaire). Schéma, pas une cartographie. */
export function vaisseaux() {
  const g = new THREE.Group();
  const types = [
    { couleur: 0xff7a6b, dz: 0.06, tronc: [V(198, 300, 0.1), V(196, 262, 0.12)] },
    { couleur: 0x7c8dff, dz: -0.02, tronc: [V(206, 300, -0.05), V(202, 262, 0.02)] },
    { couleur: 0x8bd96a, dz: 0.14, tronc: [V(186, 286, -0.1), V(190, 262, 0.08)] },
  ];
  const hile = V(192, 214);
  const branches = [[V(150, 196), V(124, 178)], [V(160, 170), V(140, 152)], [V(222, 186), V(246, 160)], [V(208, 168), V(222, 146)]];
  types.forEach(({ couleur, dz, tronc }) => {
    const m = new THREE.MeshStandardMaterial({ color: couleur, emissive: couleur, emissiveIntensity: 0.6, roughness: 0.35, transparent: true, opacity: 0 });
    const h = hile.clone().setZ(0.15 + dz);
    g.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3([...tronc, h]), 40, 0.022, 8, false), m));
    branches.forEach(([a, b], i) => {
      const pts = [h, a.clone().setZ(0.2 + dz + i * 0.01), b.clone().setZ(0.18 + dz)];
      g.add(new THREE.Mesh(new THREE.TubeGeometry(new THREE.CatmullRomCurve3(pts), 30, 0.014, 6, false), m));
    });
    g.userData.mats = (g.userData.mats || []).concat(m);
  });
  return g;
}

/* Poussières lumineuses avec flou de profondeur (les plus proches deviennent de larges disques doux). */
export function poussieresCinema(n = 340) {
  const pos = new Float32Array(n * 3), taille = new Float32Array(n), phase = new Float32Array(n);
  for (let i = 0; i < n; i++) {
    pos[i * 3] = (Math.random() - 0.5) * 7;
    pos[i * 3 + 1] = (Math.random() - 0.5) * 7;
    pos[i * 3 + 2] = (Math.random() - 0.5) * 6 + (Math.random() < 0.15 ? 3 : 0);
    taille[i] = 0.5 + Math.random() * 1.5;
    phase[i] = Math.random() * 100;
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geo.setAttribute("aTaille", new THREE.BufferAttribute(taille, 1));
  geo.setAttribute("aPhase", new THREE.BufferAttribute(phase, 1));
  const mat = new THREE.ShaderMaterial({
    transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    uniforms: { uTemps: { value: 0 }, uEchelle: { value: window.devicePixelRatio || 1 } },
    vertexShader: `attribute float aTaille; attribute float aPhase; uniform float uTemps; uniform float uEchelle; varying float vA;
      void main(){ vec3 p = position; p.y = mod(p.y + uTemps * .05 * aTaille + 3.5, 7.) - 3.5; p.x += sin(uTemps * .3 + aPhase) * .08;
        vec4 mv = modelViewMatrix * vec4(p, 1.); float d = -mv.z;
        gl_PointSize = aTaille * uEchelle * (18. / d) * (1. + smoothstep(4., 1., d) * 6.);
        vA = mix(.5, .12, smoothstep(4., 1., d)) * smoothstep(.2, 1.5, d); gl_Position = projectionMatrix * mv; }`,
    fragmentShader: `varying float vA; void main(){ float r = length(gl_PointCoord - .5); float a = smoothstep(.5, .1, r) * vA;
      gl_FragColor = vec4(mix(vec3(.55,.95,.9), vec3(1.), .3), a); }`,
  });
  const pts = new THREE.Points(geo, mat);
  pts.frustumCulled = false;
  return pts;
}

/* Passe « pellicule » : grain animé, vignettage, légère aberration chromatique sur les bords. */
export function passeFilm() {
  return new ShaderPass({
    uniforms: { tDiffuse: { value: null }, uTemps: { value: 0 }, uGrain: { value: 0.06 }, uVignette: { value: 1.15 } },
    vertexShader: "varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.); }",
    fragmentShader: `uniform sampler2D tDiffuse; uniform float uTemps; uniform float uGrain; uniform float uVignette; varying vec2 vUv;
      float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }
      void main(){ vec2 c = vUv - .5; float d = length(c);
        vec2 dec = c * d * .006;
        vec3 col = vec3(texture2D(tDiffuse, vUv + dec).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - dec).b);
        col *= smoothstep(uVignette, .25, d);
        col += (h(vUv * 1000. + fract(uTemps * 7.)) - .5) * uGrain;
        gl_FragColor = vec4(col, 1.); }`,
  });
}
