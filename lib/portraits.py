"""Portraits des chirurgiens : photos/chirurgiens/<slug>.(png|jpg) → dist/img/chirurgiens/<slug>-<largeur>.(webp|jpg).

Recadrage 4:5 centré sur le haut de l'image (visage), deux largeurs. Les variantes sont
mises en cache dans .cache/portraits (reconstruites seulement si la source change).
"""

from pathlib import Path

from PIL import Image

RACINE = Path(__file__).resolve().parent.parent
SOURCES = RACINE / "photos" / "chirurgiens"
CACHE = RACINE / ".cache" / "portraits"
LARGEURS = (400, 800)
RATIO = 4 / 5


def source(slug):
    for ext in (".jpg", ".jpeg", ".png", ".webp"):
        f = SOURCES / f"{slug}{ext}"
        if f.exists():
            return f
    return None


def url(slug, largeur, ext="webp"):
    return f"/img/chirurgiens/{slug}-{largeur}.{ext}"


def _recadrer(im):
    w, h = im.size
    if w / h > RATIO:
        nw = round(h * RATIO)
        g = (w - nw) // 2
        return im.crop((g, 0, g + nw, h))
    nh = round(w / RATIO)
    haut = min(round(h * 0.04), h - nh)  # on garde le visage : coupe surtout en bas
    return im.crop((0, haut, w, haut + nh))


def produire(slugs):
    CACHE.mkdir(parents=True, exist_ok=True)
    n = 0
    for slug in slugs:
        f = source(slug)
        if not f:
            continue
        im = None
        for l in LARGEURS:
            for ext, opts in (("webp", {"quality": 82, "method": 6}), ("jpg", {"quality": 84, "optimize": True, "progressive": True})):
                cible = CACHE / f"{slug}-{l}.{ext}"
                if cible.exists() and cible.stat().st_mtime >= f.stat().st_mtime:
                    continue
                if im is None:
                    im = _recadrer(Image.open(f).convert("RGB"))
                im.resize((l, round(l / RATIO)), Image.LANCZOS).save(cible, **opts)
                n += 1
    return n
