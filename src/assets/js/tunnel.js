/* Le tube digestif vu de l'intérieur : un seul maillage, relief propre à chaque segment
   (plis longitudinaux de l'œsophage, rides de l'estomac, valvules de l'intestin grêle,
   haustrations et bandelettes du côlon). Seule lumière : la lampe portée par la caméra.
   Tout est ancré dans la géométrie et anticrénelé (fwidth) : rien ne scintille. */
import * as THREE from "./vendor/three.module.min.js";

// Bornes des segments (u = 0 en haut de l'œsophage, 1 à l'anus)
const SEG = { oesophage: [0, 0.13], estomac: [0.15, 0.29], duodenum: [0.31, 0.47], intestin: [0.47, 0.64], colon: [0.66, 0.86], rectum: [0.88, 1] };
const RAYONS = [[0, 2.1], [0.125, 2.1], [0.165, 6.2], [0.27, 5.8], [0.305, 2.6], [0.47, 2.35], [0.64, 2.35], [0.68, 3.9], [0.85, 3.9], [0.89, 4.4], [0.975, 3.4], [1, 0.9]];
const TEINTES = [[0, 0xe0907e], [0.13, 0xe0907e], [0.16, 0xf0a08f], [0.29, 0xf0a08f], [0.32, 0xf2b08b], [0.64, 0xf4ac96], [0.67, 0xe8a07f], [0.86, 0xe8a07f], [0.9, 0xdc8f7a], [1, 0xdc8f7a]];

const lisse = (a, b, x) => { const t = Math.min(1, Math.max(0, (x - a) / (b - a))); return t * t * (3 - 2 * t); };
const fenetre = (u, [a, b], f = 0.02) => lisse(a - f, a + f, u) * (1 - lisse(b - f, b + f, u));
function interp(table, u) {
  for (let i = 1; i < table.length; i++) {
    if (u <= table[i][0]) {
      const [u0, v0] = table[i - 1], [u1, v1] = table[i];
      return [v0, v1, lisse(u0, u1, u)];
    }
  }
  const d = table[table.length - 1][1];
  return [d, d, 0];
}

/* Trajet : on intègre un cap qui tourne doucement, segment par segment. */
function trajet() {
  const pts = [];
  const pos = new THREE.Vector3();
  let lacet = 0, tangage = 0;
  const N = 96;
  for (let i = 0; i <= N; i++) {
    const u = i / N;
    let dl = 0, dt = 0;
    if (u > 0.13 && u < 0.29) { dl = 0.2; dt = -0.05; }                         // l'estomac en J
    else if (u >= 0.29 && u < 0.47) { dl = -0.22; dt = 0.06 * Math.sin(i * 0.5); } // le cadre duodénal
    else if (u >= 0.47 && u < 0.64) { dl = 0.3 * Math.sin(i * 0.9); dt = 0.18 * Math.cos(i * 0.7); } // anses grêles
    else if (u >= 0.64 && u < 0.86) { dl = 0.16; dt = 0.04 * Math.sin(i * 0.4); }  // le cadre colique
    else { dl = -0.04; dt = 0.02; }
    lacet += dl; tangage = tangage * 0.8 + dt;
    const dir = new THREE.Vector3(Math.sin(lacet) * Math.cos(tangage), Math.sin(tangage), -Math.cos(lacet) * Math.cos(tangage));
    pts.push(pos.clone());
    pos.addScaledVector(dir, 7);
  }
  return new THREE.CatmullRomCurve3(pts, false, "centripetal");
}

function rayon(u, th, s) {
  const [r0, r1, t] = interp(RAYONS, u);
  const R = r0 + (r1 - r0) * t;
  let r = R;
  // Œsophage : plis longitudinaux, lumière étoilée
  r -= R * 0.17 * fenetre(u, SEG.oesophage) * Math.pow(0.5 + 0.5 * Math.cos(7 * th + 0.4 * Math.sin(s * 0.25)), 2);
  // Estomac : rides sinueuses
  r -= R * 0.075 * fenetre(u, SEG.estomac) * Math.pow(0.5 + 0.5 * Math.sin(13 * th + 2.2 * Math.sin(s * 0.18 + th * 2)), 3);
  // Duodénum et intestin grêle : valvules conniventes en croissant
  const grele = Math.max(fenetre(u, SEG.duodenum), fenetre(u, SEG.intestin));
  r -= R * 0.3 * grele * Math.pow(0.5 + 0.5 * Math.cos(s * 2.3 + 0.6 * Math.sin(th)), 10) * (0.55 + 0.45 * Math.sin(th * 2 + s * 0.3));
  // Côlon : haustrations + trois bandelettes
  const colon = fenetre(u, SEG.colon);
  r += R * 0.16 * colon * Math.pow(Math.sin(s * 0.62), 2);
  r -= R * 0.12 * colon * Math.pow(0.5 + 0.5 * Math.cos(3 * th), 14);
  // Rectum : grands replis
  r -= R * 0.12 * fenetre(u, SEG.rectum) * Math.pow(0.5 + 0.5 * Math.cos(s * 0.35 + th), 6);
  // Vie organique douce
  r *= 1 + 0.035 * Math.sin(3 * th + s * 0.11) + 0.02 * Math.sin(5 * th - s * 0.07);
  return r;
}

export function creerTunnel({ anneaux = 1500, cotes = 96 } = {}) {
  const courbe = trajet();
  const L = courbe.getLength();
  const cadres = courbe.computeFrenetFrames(anneaux, false);
  const n = (anneaux + 1) * (cotes + 1);
  const pos = new Float32Array(n * 3), sArr = new Float32Array(n), thArr = new Float32Array(n), col = new Float32Array(n * 3);
  const p = new THREE.Vector3(), c = new THREE.Color(), c2 = new THREE.Color();
  for (let i = 0; i <= anneaux; i++) {
    const u = i / anneaux, s = u * L;
    courbe.getPointAt(u, p);
    const N = cadres.normals[i], B = cadres.binormals[i];
    const [a, b, t] = interp(TEINTES, u);
    c.setHex(a).lerp(c2.setHex(b), t);
    for (let j = 0; j <= cotes; j++) {
      const th = (j / cotes) * Math.PI * 2;
      const r = rayon(u, th, s);
      const k = i * (cotes + 1) + j;
      pos[k * 3] = p.x + r * (Math.cos(th) * N.x + Math.sin(th) * B.x);
      pos[k * 3 + 1] = p.y + r * (Math.cos(th) * N.y + Math.sin(th) * B.y);
      pos[k * 3 + 2] = p.z + r * (Math.cos(th) * N.z + Math.sin(th) * B.z);
      sArr[k] = s; thArr[k] = j / cotes;
      col[k * 3] = c.r; col[k * 3 + 1] = c.g; col[k * 3 + 2] = c.b;
    }
  }
  const idx = [];
  for (let i = 0; i < anneaux; i++) {
    for (let j = 0; j < cotes; j++) {
      const a = i * (cotes + 1) + j, b = a + cotes + 1;
      idx.push(a, b, a + 1, b, b + 1, a + 1);
    }
  }
  const geo = new THREE.BufferGeometry();
  geo.setAttribute("position", new THREE.BufferAttribute(pos, 3));
  geo.setAttribute("aS", new THREE.BufferAttribute(sArr, 1));
  geo.setAttribute("aTh", new THREE.BufferAttribute(thArr, 1));
  geo.setAttribute("aCol", new THREE.BufferAttribute(col, 3));
  geo.setIndex(idx);
  geo.computeVertexNormals();

  const mat = new THREE.ShaderMaterial({
    side: THREE.DoubleSide,
    extensions: { derivatives: true },
    uniforms: {
      uLampe: { value: new THREE.Vector3() },
      uBrume: { value: new THREE.Color(0x160f26) },
      uOmbre: { value: new THREE.Color(0x2b1f4a) },
      uOrange: { value: new THREE.Color(0xf38d38) },
      uPortee: { value: 14 },
    },
    vertexShader: /* glsl */`
      attribute float aS; attribute float aTh; attribute vec3 aCol;
      varying vec3 vPos; varying vec3 vN; varying float vS; varying float vTh; varying vec3 vCol;
      void main() {
        vPos = position; vN = normal; vS = aS; vTh = aTh; vCol = aCol;
        gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
      }`,
    fragmentShader: /* glsl */`
      uniform vec3 uLampe; uniform vec3 uBrume; uniform vec3 uOmbre; uniform vec3 uOrange; uniform float uPortee;
      varying vec3 vPos; varying vec3 vN; varying float vS; varying float vTh; varying vec3 vCol;
      float trait(float x, float largeur) {
        float w = fwidth(x);
        float d = abs(fract(x + 0.5) - 0.5);
        return (1.0 - smoothstep(largeur, largeur + w * 1.5, d)) * (1.0 - smoothstep(0.08, 0.3, w));
      }
      // Bruit de valeur 3D (périodique autour du tube : on l'échantillonne sur un cylindre)
      float h3(vec3 p) { p = fract(p * 0.3183099 + 0.1); p *= 17.0; return fract(p.x * p.y * p.z * (p.x + p.y + p.z)); }
      float bruit(vec3 x) {
        vec3 i = floor(x), f = fract(x); f = f * f * (3.0 - 2.0 * f);
        return mix(mix(mix(h3(i), h3(i + vec3(1,0,0)), f.x), mix(h3(i + vec3(0,1,0)), h3(i + vec3(1,1,0)), f.x), f.y),
                   mix(mix(h3(i + vec3(0,0,1)), h3(i + vec3(1,0,1)), f.x), mix(h3(i + vec3(0,1,1)), h3(i + vec3(1,1,1)), f.x), f.y), f.z);
      }
      float fbm(vec3 p) { return 0.55 * bruit(p) + 0.3 * bruit(p * 2.03 + 7.1) + 0.15 * bruit(p * 4.1 + 3.7); }
      void main() {
        vec3 versLampe = uLampe - vPos;
        float d = length(versLampe);
        vec3 L = versLampe / d;
        vec3 N = normalize(vN);
        if (dot(N, L) < 0.0) N = -N;
        float diff = max(dot(N, L), 0.0);
        float att = exp(-d / uPortee);
        float spec = pow(diff, 30.0) * 0.35 * att;
        vec3 tissu = vCol * (0.04 + 0.9 * pow(diff, 1.4)) * att + vec3(1.0, 0.88, 0.78) * spec;
        tissu = mix(uOmbre * 0.5, tissu, smoothstep(0.0, 0.25, att));
        // Muqueuse : marbrure douce + fin réseau de vaisseaux, ancrés dans la paroi
        float ang = vTh * 6.2831853;
        vec3 q = vec3(cos(ang) * 2.4, sin(ang) * 2.4, vS * 0.42);
        tissu *= 0.88 + 0.24 * fbm(q * 0.6);
        float v = 1.0 - abs(fbm(q * 1.35) * 2.0 - 1.0);
        float wv = fwidth(v);
        float vaisseau = smoothstep(0.93 - wv, 0.975 + wv, v) * (1.0 - smoothstep(0.04, 0.12, wv)) * exp(-d * 0.07);
        tissu = mix(tissu, tissu * vec3(0.62, 0.22, 0.26), vaisseau * 0.55);
        // Relevés : anneaux le long du trajet + génératrices, discrets, fondus au loin
        float anneaux = trait(vS / 2.4, 0.012);
        float gener = trait(vTh * 24.0, 0.01);
        float proche = exp(-d * 0.09);
        tissu += uOrange * anneaux * 0.45 * proche;
        tissu += vec3(0.75, 0.7, 1.0) * gener * 0.05 * proche;
        float brume = 1.0 - exp(-d * 0.045);
        gl_FragColor = vec4(mix(tissu, uBrume, brume), 1.0);
        #include <colorspace_fragment>
      }`,
  });
  const maillage = new THREE.Mesh(geo, mat);
  maillage.frustumCulled = false;
  return { maillage, courbe, cadres, anneaux, longueur: L, materiau: mat };
}

/* Place la caméra au point u, regard vers l'avant, roulis suivant le cadre transporté. */
const tmpP = new THREE.Vector3(), tmpV = new THREE.Vector3(), tmpN = new THREE.Vector3();
export function placer(camera, tunnel, u) {
  const { courbe, cadres, anneaux } = tunnel;
  const uu = Math.min(0.996, Math.max(0, u));
  courbe.getPointAt(uu, tmpP);
  courbe.getPointAt(Math.min(1, uu + 0.01), tmpV);
  const f = uu * anneaux, i = Math.floor(f), k = f - i;
  tmpN.copy(cadres.normals[i]).lerp(cadres.normals[Math.min(anneaux, i + 1)], k).normalize();
  camera.position.copy(tmpP);
  camera.up.copy(tmpN);
  camera.lookAt(tmpV);
  tunnel.materiau.uniforms.uLampe.value.copy(tmpP);
}
