"""Contrôle visuel (hors site) : capture pleine page via Edge headless, animations figées à l'état final.

    MSYS_NO_PATHCONV=1 python tools_capture.py /chemin/ largeur hauteur_ecran hauteur_totale sortie.png

Nécessite le serveur d'aperçu (port 8770) et Microsoft Edge.
"""
import subprocess
import sys
import time
import uuid
from pathlib import Path

url, w, h_ecran, h_tot, sortie = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
dist = Path(__file__).parent / "dist"
source = dist / (url.strip("/") + "/index.html" if url != "/" else "index.html")
fige = ("<style>*,*::before,*::after{animation:none!important;transition:none!important}"
        ".js [data-reveal]{opacity:1!important;transform:none!important}"
        ".planche .org__f,.planche .silhouette{stroke-dashoffset:0!important;fill-opacity:1!important}.planche .org__t{opacity:1!important}"
        ".js .hero h1 .ligne,.js .hero__chapo,.js .hero .actions,.js .hero__preuves{opacity:1!important}"
        f".entete{{position:relative!important}}.hero{{min-height:{h_ecran - 140}px}}</style></head>")
html = source.read_text(encoding="utf-8").replace("</head>", fige, 1).replace('loading="lazy"', 'loading="eager"')
test = source.parent / "_capture.html"
test.write_text(html, encoding="utf-8")
Path(sortie).unlink(missing_ok=True)
profil = Path(sortie).parent / f"edge-{uuid.uuid4().hex[:6]}"
chemin = "/" + test.relative_to(dist).as_posix()
subprocess.run([r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe", "--headless=new", "--disable-gpu",
                "--hide-scrollbars", f"--user-data-dir={profil}", f"--window-size={w},{h_tot}",
                "--virtual-time-budget=4000", "--run-all-compositor-stages-before-draw",
                f"--screenshot={sortie}", f"http://127.0.0.1:8770{chemin}"])
for _ in range(60):
    if Path(sortie).exists() and Path(sortie).stat().st_size:
        time.sleep(1)
        break
    time.sleep(1)
test.unlink()
