"""Capture d'écran avec rendu WebGL (Edge headless + SwiftShader) — contrôle visuel de la 3D.

    MSYS_NO_PATHCONV=1 python tools_capture3d.py "/#voyage-foie" 1440 900 sortie.png [souris_x souris_y]

Facultatif : coordonnées de souris simulées (événement pointermove sur la zone 3D survolée).
"""
import subprocess, sys, time, uuid
from pathlib import Path

url, w, h, sortie = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
souris = sys.argv[5:7]
chemin, _, ancre = url.partition("#")
dist = Path(__file__).parent / "dist"
source = dist / (chemin.strip("/") + "/index.html" if chemin.strip("/") else "index.html")
script = ""
if ancre.startswith("voyage-"):
    # Les captures après défilement sortent blanches : on isole l'étape en haut de page.
    script += ("<style>.demo,.bandeau-info,.entete,main>*:not(.voyage),.pied{display:none!important}"
               f".voyage__etapes{{position:absolute;inset:0;margin:0!important}}.voyage__etape:not(#{ancre}){{display:none!important}}"
               f"#{ancre} .voyage__carte{{opacity:1;transform:none}}" + (".voyage__carte,.voyage__rail{display:none!important}" if "--propre" in sys.argv else "") + "</style>"
               f"<script>addEventListener('load',()=>{{const n=+document.getElementById('{ancre}').dataset.etapeVoyage;"
               "setInterval(()=>dispatchEvent(new CustomEvent('voyage:progression',{detail:{f:n}})),50);});</script>")
if souris:
    x, y = souris
    script += (f"<script>setTimeout(()=>{{const el=document.elementFromPoint({x},{y});if(el){{['pointerenter','pointermove'].forEach(t=>"
              f"el.dispatchEvent(new PointerEvent(t,{{bubbles:true,clientX:{x},clientY:{y}}})));}}}},2500)</script>")
html = source.read_text(encoding="utf-8").replace(
    "</head>", "<style>.js [data-reveal]{opacity:1!important;transform:none!important}html{scroll-behavior:auto!important}</style></head>", 1)
html = html.replace("</body>", script + "</body>").replace('loading="lazy"', 'loading="eager"')
test = source.parent / "_capture3d.html"
test.write_text(html, encoding="utf-8")
Path(sortie).unlink(missing_ok=True)
profil = Path(sortie).parent / f"edge-{uuid.uuid4().hex[:6]}"
cible = f"http://127.0.0.1:8770/{test.relative_to(dist).as_posix()}"
subprocess.run([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "--headless=new", "--use-angle=swiftshader",
                "--enable-unsafe-swiftshader", "--hide-scrollbars", f"--user-data-dir={profil}", f"--window-size={w},{h}",
                "--virtual-time-budget=14000", f"--screenshot={sortie}", cible])
for _ in range(60):
    if Path(sortie).exists() and Path(sortie).stat().st_size:
        time.sleep(1); break
    time.sleep(1)
test.unlink()
