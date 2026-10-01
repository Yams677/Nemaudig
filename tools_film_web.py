"""Prépare les films tournés (film/*.mp4) pour le site : versions web compressées + images d'affiche.

    PYTHONIOENCODING=utf-8 python tools_film_web.py

Sorties dans src/video/ (copié tel quel dans dist/ par build.py) :
  parcours-digestif.{mp4,webm,jpg,webp}            film complet 16:9 (ordinateur)
  parcours-digestif-vertical.{mp4,webm,jpg,webp}   version courte 9:16 (mobile)
"""

import subprocess
from pathlib import Path

RACINE = Path(__file__).parent
FILMS = RACINE / "film"
CIBLE = RACINE / "src" / "video"

# (source, nom web, seconde de l'image d'affiche, largeur max)
VERSIONS = [
    ("parcours-digestif.mp4", "parcours-digestif", 22.0, 1600),
    ("parcours-digestif-court-vertical.mp4", "parcours-digestif-vertical", 12.5, 1080),
]


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def main():
    CIBLE.mkdir(parents=True, exist_ok=True)
    for source, nom, affiche, largeur in VERSIONS:
        src = FILMS / source
        if not src.exists():
            print(f"  ~ {source} absent : ignoré")
            continue
        echelle = f"scale='min({largeur},iw)':-2"
        ff("-i", str(src), "-vf", echelle, "-c:v", "libx264", "-preset", "slow", "-crf", "27", "-maxrate", "2800k",
           "-bufsize", "5600k", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-an", str(CIBLE / f"{nom}.mp4"))
        ff("-i", str(src), "-vf", echelle, "-c:v", "libvpx-vp9", "-crf", "40", "-b:v", "2400k", "-row-mt", "1",
           "-deadline", "good", "-cpu-used", "2", "-an", str(CIBLE / f"{nom}.webm"))
        ff("-ss", str(affiche), "-i", str(src), "-frames:v", "1", "-vf", echelle, "-q:v", "3", str(CIBLE / f"{nom}.jpg"))
        ff("-ss", str(affiche), "-i", str(src), "-frames:v", "1", "-vf", echelle, "-quality", "80", str(CIBLE / f"{nom}.webp"))
        tailles = ", ".join(f"{e} {(CIBLE / f'{nom}.{e}').stat().st_size / 1e6:.1f} Mo" for e in ("mp4", "webm"))
        print(f"✓ {nom} — {tailles}")


if __name__ == "__main__":
    main()
