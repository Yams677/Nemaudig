/* Vrais organes (BodyParts3D, CC BY 4.0) : chargement, lissage, matière.
   Les maillages d'origine sont parfois très légers (œsophage : ~600 triangles) ;
   on les subdivise une fois puis on les lisse (Taubin, sans rétrécissement). */
import * as THREE from "./vendor/three.module.min.js";
import { GLTFLoader } from "./vendor/GLTFLoader.js";
import { MeshoptDecoder } from "./vendor/meshopt_decoder.module.js";
import { mergeVertices } from "./vendor/BufferGeometryUtils.js";

export const TEINTES = {
  oesophage: 0xc97a6d, estomac: 0xd99282, foie: 0x7f3127, vesicule: 0x6d7f3c, pancreas: 0xe2b27c,
  duodenum: 0xd89c84, intestin: 0xe3a493, colon: 0xcd8d74, rectum: 0xbd7462,
};

const chargeur = new GLTFLoader().setMeshoptDecoder(MeshoptDecoder);
const cache = new Map();

function subdiviser(geo) {
  const pos = geo.attributes.position.array;
  const idx = geo.index.array;
  const sommets = Array.from(pos);
  const milieux = new Map();
  const milieu = (a, b) => {
    const cle = a < b ? a * 1e7 + b : b * 1e7 + a;
    let m = milieux.get(cle);
    if (m === undefined) {
      m = sommets.length / 3;
      sommets.push((pos[a * 3] + pos[b * 3]) / 2, (pos[a * 3 + 1] + pos[b * 3 + 1]) / 2, (pos[a * 3 + 2] + pos[b * 3 + 2]) / 2);
      milieux.set(cle, m);
    }
    return m;
  };
  const faces = [];
  for (let i = 0; i < idx.length; i += 3) {
    const [a, b, c] = [idx[i], idx[i + 1], idx[i + 2]];
    const ab = milieu(a, b), bc = milieu(b, c), ca = milieu(c, a);
    faces.push(a, ab, ca, ab, b, bc, ca, bc, c, ab, bc, ca);
  }
  const g = new THREE.BufferGeometry();
  g.setAttribute("position", new THREE.Float32BufferAttribute(sommets, 3));
  g.setIndex(faces);
  return g;
}

function lisser(geo, passes) {
  const n = geo.attributes.position.count;
  const pos = geo.attributes.position.array;
  const idx = geo.index.array;
  const voisins = Array.from({ length: n }, () => new Set());
  for (let i = 0; i < idx.length; i += 3) {
    const [a, b, c] = [idx[i], idx[i + 1], idx[i + 2]];
    voisins[a].add(b).add(c); voisins[b].add(a).add(c); voisins[c].add(a).add(b);
  }
  const listes = voisins.map((s) => Array.from(s));
  const tmp = new Float32Array(pos.length);
  const pas = (f) => {
    for (let v = 0; v < n; v++) {
      const l = listes[v];
      if (!l.length) { tmp.set(pos.subarray(v * 3, v * 3 + 3), v * 3); continue; }
      let x = 0, y = 0, z = 0;
      for (const w of l) { x += pos[w * 3]; y += pos[w * 3 + 1]; z += pos[w * 3 + 2]; }
      const k = 1 / l.length;
      tmp[v * 3] = pos[v * 3] + f * (x * k - pos[v * 3]);
      tmp[v * 3 + 1] = pos[v * 3 + 1] + f * (y * k - pos[v * 3 + 1]);
      tmp[v * 3 + 2] = pos[v * 3 + 2] + f * (z * k - pos[v * 3 + 2]);
    }
    pos.set(tmp);
  };
  for (let i = 0; i < passes; i++) { pas(0.5); pas(-0.53); }
  geo.attributes.position.needsUpdate = true;
}

function preparer(geoSource) {
  let geo = new THREE.BufferGeometry();
  geo.setAttribute("position", geoSource.attributes.position.clone());
  if (geoSource.index) geo.setIndex(geoSource.index.clone());
  geo = mergeVertices(geo, 0.05);
  const triangles = geo.index.count / 3;
  if (triangles < 9000) geo = subdiviser(geo);
  lisser(geo, triangles < 9000 ? 4 : 2);
  geo.computeVertexNormals();
  return geo;
}

/* Renvoie une géométrie lissée, en millimètres, repère BodyParts3D (Z vers le haut). */
export function chargerOrgane(cle) {
  if (!cache.has(cle)) {
    cache.set(cle, chargeur.loadAsync(`/models/${cle}.glb`).then((gltf) => {
      const geos = [];
      gltf.scene.updateMatrixWorld(true);
      gltf.scene.traverse((o) => {
        if (o.isMesh) {
          const g = o.geometry.clone();
          g.applyMatrix4(o.matrixWorld);
          geos.push(g);
        }
      });
      return preparer(geos[0]);
    }));
  }
  return cache.get(cle);
}

/* Matière « tissu propre ». Chaque matière porte une zone lumineuse réglable
   (point, rayon en mm, force) qui sert à situer une pathologie sur l'organe. */
export function matiere(cle) {
  const m = new THREE.MeshPhysicalMaterial({
    color: new THREE.Color(TEINTES[cle] ?? 0xd08a78), roughness: 0.48, metalness: 0,
    clearcoat: 0.55, clearcoatRoughness: 0.32,
    sheen: 0.5, sheenRoughness: 0.6, sheenColor: new THREE.Color(0xffc9a8),
    emissive: new THREE.Color(0xf38d38), emissiveIntensity: 0, envMapIntensity: 0.45,
  });
  const zone = { uZone: { value: new THREE.Vector3() }, uZoneR: { value: 20 }, uZoneF: { value: 0 } };
  m.userData.zone = zone;
  m.onBeforeCompile = (sh) => {
    Object.assign(sh.uniforms, zone);
    sh.vertexShader = sh.vertexShader
      .replace("#include <common>", "#include <common>\nvarying vec3 vZoneP;")
      .replace("#include <begin_vertex>", "#include <begin_vertex>\nvZoneP = position;");
    sh.fragmentShader = sh.fragmentShader
      .replace("#include <common>", "#include <common>\nvarying vec3 vZoneP;\nuniform vec3 uZone; uniform float uZoneR; uniform float uZoneF;")
      .replace("#include <emissivemap_fragment>", `#include <emissivemap_fragment>
        float zd = distance(vZoneP, uZone);
        float zk = 1.0 - smoothstep(uZoneR * 0.35, uZoneR, zd);
        totalEmissiveRadiance += vec3(0.85, 0.3, 0.06) * uZoneF * zk;
        diffuseColor.rgb = mix(diffuseColor.rgb, vec3(0.95, 0.42, 0.14), min(1.0, uZoneF * zk * 0.6));`);
  };
  return m;
}

/* Lumière commune : environnement doux + lampe chaude + contre-jour violet. */
export function eclairer(scene, renderer, { cle = 2.2, contre = 1.6 } = {}) {
  const pmrem = new THREE.PMREMGenerator(renderer);
  return import("./vendor/RoomEnvironment.js").then(({ RoomEnvironment }) => {
    scene.environment = pmrem.fromScene(new RoomEnvironment(renderer), 0.04).texture;
    const lampe = new THREE.DirectionalLight(0xffc08a, cle);
    lampe.position.set(-2, 3, 4);
    const rim = new THREE.DirectionalLight(0x9d8cff, contre);
    rim.position.set(3, 1, -4);
    const sol = new THREE.HemisphereLight(0xffe2cc, 0x2a1f45, 0.35);
    scene.add(lampe, rim, sol);
  });
}
