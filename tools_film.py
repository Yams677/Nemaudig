"""Tournage du film « Le parcours digestif » à partir de la 3D du site (aucun crédit IA).

    PYTHONIOENCODING=utf-8 python tools_film.py                 # film complet 16:9
    PYTHONIOENCODING=utf-8 python tools_film.py --court         # version courte
    PYTHONIOENCODING=utf-8 python tools_film.py --vertical      # 1080×1920
    PYTHONIOENCODING=utf-8 python tools_film.py --essai 0,12,30  # quelques images aux secondes données

Fonctionnement : une page de tournage (dist/_film.html, supprimée à la fin) pilote la scène 3D du voyage
image par image (horloge externe, 30 i/s), y incruste titres et bandes cinéma dans les polices du site,
puis envoie chaque image à un petit serveur local. ffmpeg assemble ensuite le MP4.
Prérequis : `python build.py` exécuté, Microsoft Edge, ffmpeg.
"""

import base64
import json
import shutil
import subprocess
import sys
import threading
import time
import uuid
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from data.film import calendrier, etapes_film
from lib.anatomie import donnees_3d

RACINE = Path(__file__).parent
DIST = RACINE / "dist"
SORTIE = RACINE / "film"
IMAGES = RACINE / ".cache" / "film-images"
PORT = 8771
FPS = 30
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

HARNAIS = """<!doctype html><html lang="fr"><head><meta charset="utf-8">
<style>
@font-face{font-family:Fraunces;src:url(/assets/fonts/fraunces-latin.woff2) format("woff2");font-weight:300 600}
@font-face{font-family:Hanken;src:url(/assets/fonts/hanken-grotesk-var.woff2) format("woff2");font-weight:100 900}
html,body{margin:0;background:#07131C;overflow:hidden}
#scene{position:fixed;inset:0;width:__W__px;height:__H__px}
</style></head><body>
<div id="scene" data-planche-3d="voyage"></div>
<div hidden>__ETAPES__</div>
<script type="application/json" id="anatomie-donnees">__DONNEES__</script>
<script>window.NEMAUDIG_FILM = { fps: __FPS__, sansFlou: new URLSearchParams(location.search).has("sansflou"), sansPost: new URLSearchParams(location.search).has("sanspost") };
window.onerror = (m) => fetch("/log", { method: "POST", body: String(m) });</script>
<script type="module">
const P = __PARAMS__;
const log = (m) => fetch("/log", { method: "POST", body: m });
await import("/assets/js/anatomie3d.js");
await Promise.all([document.fonts.load("300 64px Fraunces"), document.fonts.load("italic 300 64px Fraunces"),
                   document.fonts.load("600 24px Hanken"), document.fonts.load("400 28px Hanken")]);
const W = P.w, H = P.h, vertical = H > W;
const sortie = document.createElement("canvas"); sortie.width = W; sortie.height = H;
const cx = sortie.getContext("2d");
const gl = document.querySelector("#scene canvas").getContext("webgl2") || document.querySelector("#scene canvas").getContext("webgl");
const dbg = gl.getExtension("WEBGL_debug_renderer_info");
log("Rendu : " + (dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : "?"));
log(`Fenêtre ${innerWidth}×${innerHeight}, scène ${document.querySelector("#scene").clientWidth}×${document.querySelector("#scene").clientHeight}, tampon ${gl.drawingBufferWidth}×${gl.drawingBufferHeight}`);

const lisse = (x) => x * x * (3 - 2 * x);
function etat(t) {
  for (const [a, b, f0, f1, titre] of P.segments) {
    if (t >= a && t < b) {
      const k = (t - a) / (b - a);
      return { f: f0 + (f1 - f0) * lisse(k), titre, debut: a, fin: b, k };
    }
  }
  const s = P.segments[P.segments.length - 1];
  return { f: s[3], titre: s[4], debut: s[0], fin: s[1], k: 1 };
}

function ligne(txt, x, y, police, couleur, alpha, espacement = 0) {
  cx.globalAlpha = alpha; cx.fillStyle = couleur; cx.font = police;
  if (cx.letterSpacing !== undefined) cx.letterSpacing = espacement + "px";
  cx.fillText(txt, x, y);
}
function couper(txt, police, max) {
  cx.font = police; const mots = txt.split(" "), lignes = []; let l = "";
  for (const m of mots) { const essai = l ? l + " " + m : m; if (cx.measureText(essai).width > max && l) { lignes.push(l); l = m; } else l = essai; }
  if (l) lignes.push(l); return lignes;
}

function titres(t, e) {
  if (e.titre === null || e.titre === undefined) return;
  const d = P.etapes[e.titre];
  const entree = Math.min(1, Math.max(0, (t - e.debut - (e.titre === 0 ? 1.4 : 0.35)) / 0.7));
  const sortieA = e.titre === P.etapes.length - 1 ? 1 : Math.min(1, Math.max(0, (e.fin - t - 0.15) / 0.5));
  const a = lisse(Math.min(entree, sortieA));
  if (a <= 0) return;
  const montee = (1 - a) * 18;
  const echelle = vertical ? 0.9 : 1;
  const x = vertical ? W * 0.08 : W * 0.605, maxL = vertical ? W * 0.84 : W * 0.33;
  let y = vertical ? H * 0.70 : H * 0.42;
  y += montee;
  cx.save(); cx.textBaseline = "alphabetic";
  cx.globalAlpha = a * 0.9; cx.fillStyle = "#2BB3A7"; cx.fillRect(x, y - 9 * echelle, 34 * echelle, 2);
  ligne(d.surtitre.toUpperCase(), x + 46 * echelle, y, `600 ${Math.round(19 * echelle)}px Hanken`, "#2BB3A7", a, 3.5);
  y += 70 * echelle;
  const pT = `300 ${Math.round(64 * echelle)}px Fraunces`;
  for (const l of couper(d.titre, pT, maxL)) { ligne(l, x, y, pT, "#FFFFFF", a, -0.5); y += 70 * echelle; }
  if (d.sous) {
    y += 12 * echelle;
    const pS = `400 ${Math.round(25 * echelle)}px Hanken`;
    for (const l of couper(d.sous, pS, maxL)) { ligne(l, x, y, pS, "#B9CCD5", a * 0.95); y += 36 * echelle; }
  }
  cx.restore();
}

function habillage() {
  const bande = Math.round(H * (vertical ? 0.035 : 0.075));
  cx.globalAlpha = 1; cx.fillStyle = "#03080C";
  cx.fillRect(0, 0, W, bande); cx.fillRect(0, H - bande, W, bande);
  ligne("Illustration animée — Nemaudig", W - (vertical ? 34 : 60), H - bande / 2 + 7, "400 17px Hanken", "#8FA3AD", 0.6);
  cx.textAlign = "left";
}

// En essai, on calcule toutes les images (les mouvements sont amortis d'une image à l'autre) mais on n'envoie que celles demandées.
const garder = P.essai ? new Set(P.essai.map((s) => Math.round(s * P.fps))) : null;
const derniere = P.essai ? Math.max(...garder) : Math.ceil(P.duree * P.fps) - 1;
const depuis = parseInt(new URLSearchParams(location.search).get("depuis") || "0", 10); // reprise après blocage
const debut = performance.now();
for (let n = 0; n <= derniere; n++) {
  if (garder && !garder.has(n)) { window.NEMAUDIG_FILM.rendre(n / P.fps, etat(n / P.fps).f); continue; }
  const t = n / P.fps, e = etat(t);
  const scene = window.NEMAUDIG_FILM.rendre(t, e.f);
  cx.globalAlpha = 1; cx.drawImage(scene, 0, 0, W, H);
  titres(t, e);
  cx.save(); cx.textAlign = "right"; habillage(); cx.restore();
  if (n < depuis) continue;
  // toDataURL est synchrone : pas de rappel différé que le navigateur pourrait suspendre.
  const donnees = sortie.toDataURL("image/jpeg", 0.94);
  for (let essai = 0; ; essai++) {
    try { const r = await fetch(`/image/${String(n).padStart(5, "0")}`, { method: "POST", body: donnees }); if (r.ok) break; }
    catch (err) { if (essai > 20) throw err; }
    await new Promise((r) => setTimeout(r, 200 * (essai + 1)));
  }
  if (n % 60 === 0) log(`image ${n} — ${((performance.now() - debut) / 1000).toFixed(0)} s`);
}
await fetch("/fin", { method: "POST" });
</script></body></html>"""


def page(etapes, segments, duree, w, h, essai):
    attributs = "".join(
        f'<i data-etape-voyage="{i}" data-organes="{" ".join(e["organes"])}" '
        f'data-camera="{",".join(map(str, e["camera"])) if e["camera"] else ""}" data-ecarter="{" ".join(e.get("ecarter", []))}"></i>'
        for i, e in enumerate(etapes))
    params = {"w": w, "h": h, "fps": FPS, "duree": duree, "segments": segments, "essai": essai,
              "etapes": [{k: e[k] for k in ("surtitre", "titre", "sous")} for e in etapes]}
    return (HARNAIS.replace("__W__", str(w)).replace("__H__", str(h)).replace("__ETAPES__", attributs)
            .replace("__DONNEES__", donnees_3d()).replace("__FPS__", str(FPS)).replace("__PARAMS__", json.dumps(params, ensure_ascii=False)))


def main():
    court, vertical = "--court" in sys.argv, "--vertical" in sys.argv
    essai = None
    if "--essai" in sys.argv:
        essai = [float(x) for x in sys.argv[sys.argv.index("--essai") + 1].split(",")]
    w, h = (1080, 1920) if vertical else (1920, 1080)
    etapes = etapes_film(court)
    segments, duree = calendrier(len(etapes), court)
    nom = "parcours-digestif" + ("-court" if court else "") + ("-vertical" if vertical else "")

    if IMAGES.exists():
        shutil.rmtree(IMAGES)
    IMAGES.mkdir(parents=True)
    SORTIE.mkdir(exist_ok=True)
    (DIST / "_film.html").write_text(page(etapes, segments, duree, w, h, essai), encoding="utf-8")

    fini = threading.Event()

    class Recepteur(SimpleHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def do_POST(self):
            corps = self.rfile.read(int(self.headers.get("Content-Length", 0)))
            if self.path.startswith("/image/"):
                (IMAGES / f"{self.path.rsplit('/', 1)[1]}.jpg").write_bytes(base64.b64decode(corps.split(b",", 1)[1]))
            elif self.path == "/log":
                print("  ·", corps.decode("utf-8", "replace"), flush=True)
            elif self.path == "/fin":
                fini.set()
            self.send_response(204)
            self.send_header("Content-Length", "0")
            self.end_headers()

        def log_message(self, *args):
            pass

    serveur = ThreadingHTTPServer(("127.0.0.1", PORT), partial(Recepteur, directory=str(DIST)))
    threading.Thread(target=serveur.serve_forever, daemon=True).start()
    profil = RACINE / ".cache" / f"edge-film-{uuid.uuid4().hex[:6]}"
    print(f"Tournage « {nom} » : {duree:.1f} s, {len(etapes)} plans, {w}×{h}", flush=True)

    def lancer(depuis=0):
        return subprocess.Popen([EDGE, "--headless=new", "--enable-gpu", "--ignore-gpu-blocklist", "--use-angle=d3d11",
                                 "--enable-unsafe-swiftshader", "--disable-background-timer-throttling",
                                 "--disable-renderer-backgrounding", "--disable-backgrounding-occluded-windows",
                                 "--disable-features=CalculateNativeWinOcclusion,IntensiveWakeUpThrottling",
                                 f"--user-data-dir={profil}", f"--window-size={w + 40},{h + 120}",  # la fenêtre perd ~24×92 px de cadre : la scène doit y tenir entière

                                 f"http://127.0.0.1:{PORT}/_film.html?depuis={depuis}" + ("&sansflou" if "--sans-flou" in sys.argv else "") + ("&sanspost" if "--sans-post" in sys.argv else "")])

    def arreter(proc):
        # Tue tout l'arbre de processus d'Edge (GPU, rendu…), sinon des instances orphelines restent actives.
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)], capture_output=True)

    total = len(essai) if essai else int(duree * FPS)
    edge, debut, dernier_n, dernier_t, relances = lancer(), time.time(), -1, time.time(), 0
    try:
        while not fini.wait(timeout=10):
            n = len(list(IMAGES.glob("*.jpg")))
            if n != dernier_n:
                dernier_n, dernier_t = n, time.time()
                print(f"  {n}/{total} images — {time.time() - debut:.0f} s", flush=True)
            elif time.time() - dernier_t > 60 and not essai:
                relances += 1
                if relances > 8:
                    print("Trop de blocages, abandon.")
                    return
                print(f"  ! blocage à {n} images — relance n°{relances}", flush=True)
                arreter(edge)
                time.sleep(2)
                edge, dernier_t = lancer(n), time.time()
            if time.time() - debut > 4 * 3600:
                print("Délai dépassé.")
                return
    finally:
        arreter(edge)
        time.sleep(1)
        serveur.shutdown()
        (DIST / "_film.html").unlink(missing_ok=True)
        shutil.rmtree(profil, ignore_errors=True)

    if essai:
        print(f"Images d'essai dans {IMAGES}")
        return
    cible = SORTIE / f"{nom}.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", str(IMAGES / "%05d.jpg"),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "17", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    str(cible)], check=True)
    print(f"✓ {cible} ({cible.stat().st_size / 1e6:.1f} Mo)")


if __name__ == "__main__":
    main()
