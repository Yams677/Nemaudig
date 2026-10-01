"""
Génère le site statique dans dist/ — c'est ce dossier (et lui seul) qu'on dépose chez l'hébergeur.

    PYTHONIOENCODING=utf-8 python build.py

Contrôles automatiques : titres et descriptions uniques, un seul <h1> par page,
liens internes valides, ancres #… existantes. En production (config.DEMO = False),
la génération est refusée tant qu'il reste un élément « À VALIDER ».
Produit aussi sitemap.xml, robots.txt et .htaccess (redirections 301 des
anciennes URL de nemaudig.fr vers les nouvelles).
"""

import hashlib
import importlib
import re
import shutil
import sys
from datetime import date
from pathlib import Path

import config
from lib import portraits
from data.chirurgiens import CHIRURGIENS

RACINE = Path(__file__).parent
SRC = RACINE / "src"
DIST = RACINE / "dist"

MODULES = ["accueil", "chirurgiens", "pathologies", "obesite", "techniques", "patients", "cabinet", "annexes"]


def empreinte(f):
    return hashlib.md5(f.read_bytes()).hexdigest()[:10]


def chemin_sortie(url):
    if url.endswith(".html"):
        return DIST / url.lstrip("/")
    return DIST / url.strip("/") / "index.html" if url != "/" else DIST / "index.html"


def verifier(pages):
    erreurs, alertes = [], []
    titres, descriptions = {}, {}
    ids_par_page = {u: set(re.findall(r'\sid="([^"]+)"', h)) for u, h in pages.items()}
    for url, html in pages.items():
        t = re.search(r"<title>(.*?)</title>", html, re.S).group(1)
        d = re.search(r'<meta name="description" content="(.*?)">', html).group(1)
        if t in titres:
            erreurs.append(f"Titre dupliqué : {url} et {titres[t]}")
        if d in descriptions and url != "/404.html":
            erreurs.append(f"Description dupliquée : {url} et {descriptions[d]}")
        titres[t], descriptions[d] = url, url
        n_h1 = len(re.findall(r"<h1[\s>]", html))
        if n_h1 != 1:
            erreurs.append(f"{url} : {n_h1} balises <h1>")
        if len(t) > 70:
            alertes.append(f"{url} : titre long ({len(t)} car.)")
        if not 70 <= len(d.replace("&#x27;", "'").replace("&amp;", "&")) <= 170:
            alertes.append(f"{url} : description de {len(d)} car.")
        ids = re.findall(r'\sid="([^"]+)"', html)
        doublons = {i for i in ids if ids.count(i) > 1}
        if doublons:
            erreurs.append(f"{url} : id dupliqués {sorted(doublons)[:5]}")
    for url, html in pages.items():
        for lien in set(re.findall(r'href="(/[^"?]*)"', html)):
            chemin, _, ancre = lien.partition("#")
            if chemin.startswith(("/assets/", "/video/", "/img/")) or (SRC / chemin.lstrip("/")).is_file():
                continue
            cible = chemin or url
            if cible not in pages:
                erreurs.append(f"{url} : lien interne cassé → {lien}")
            elif ancre and ancre not in ids_par_page[cible]:
                erreurs.append(f"{url} : ancre absente → {lien}")
        for ancre in set(re.findall(r'href="#([^"]+)"', html)):
            if ancre not in ids_par_page[url]:
                erreurs.append(f"{url} : ancre absente → #{ancre}")
    return erreurs, alertes


def verifier_production(pages):
    if config.DEMO:
        return []
    problemes = []
    if not config.PORTRAITS_VALIDES:
        problemes.append("Portraits des chirurgiens non validés par le cabinet (config.PORTRAITS_VALIDES)")
    for url, html in pages.items():
        for m in config.MARQUEURS_A_VALIDER:
            if m in html:
                problemes.append(f"{url} : « {m} » subsiste")
    return problemes


def htaccess(redirections):
    lignes = ["# Généré par build.py — ne pas modifier à la main.", "Options -Indexes", "ErrorDocument 404 /404.html",
              "AddDefaultCharset UTF-8", "",
              "<IfModule mod_headers.c>",
              '  Header set X-Content-Type-Options "nosniff"',
              '  Header set Referrer-Policy "strict-origin-when-cross-origin"',
              '  Header set Permissions-Policy "geolocation=(), camera=(), microphone=()"',
              '  <FilesMatch "\\.(css|js|woff2|svg)$">', '    Header set Cache-Control "public, max-age=31536000, immutable"', "  </FilesMatch>",
              "</IfModule>", "", "RewriteEngine On",
              "# Anciennes URL de nemaudig.fr → nouvelles (301)"]
    for ancien, nouveau in sorted(redirections.items()):
        lignes.append(f"RewriteRule ^{re.escape(ancien)}/?$ {nouveau} [R=301,L,NE]")
    return "\n".join(lignes) + "\n"


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SRC, DIST)

    css, js = SRC / "assets/css/style.css", SRC / "assets/js/main.js"
    js3d = SRC / "assets/js/anatomie3d.js"
    assets = {"css": f"/assets/css/style.css?v={empreinte(css)}", "js": f"/assets/js/main.js?v={empreinte(js)}",
              "js3d": f"/assets/js/anatomie3d.js?v={empreinte(js3d)}"}

    pages, redirections = {}, {}
    for nom in MODULES:
        module = importlib.import_module(f"pages.{nom}")
        pages.update(module.rendre(assets))
        redirections.update(getattr(module, "REDIRECTIONS", {}))

    annexes = importlib.import_module("pages.annexes")
    pages.update(annexes.plan_du_site(assets, pages))

    erreurs, alertes = verifier(pages)
    erreurs += verifier_production(pages)
    for cible in redirections.values():
        if cible.split("#")[0] not in pages:
            erreurs.append(f"Redirection vers une page inexistante : {cible}")
    for a in alertes:
        print("  ~", a)
    if erreurs:
        print("\nGÉNÉRATION REFUSÉE :")
        for e in erreurs:
            print("  ✗", e)
        sys.exit(1)

    n_img = portraits.produire([c["slug"] for c in CHIRURGIENS])
    if portraits.CACHE.exists():
        shutil.copytree(portraits.CACHE, DIST / "img" / "chirurgiens")

    for url, html in pages.items():
        f = chemin_sortie(url)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(html, encoding="utf-8")

    exclues = ("/404.html", "/mentions-legales/", "/confidentialite/", "/charte/")
    indexables = [u for u in pages if u not in exclues]
    aujourdhui = date.today().isoformat()
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "".join(f"  <url><loc>{config.SITE_URL}{u}</loc><lastmod>{aujourdhui}</lastmod></url>\n" for u in sorted(indexables))
        + "</urlset>\n", encoding="utf-8")
    (DIST / "robots.txt").write_text(
        "User-agent: *\nDisallow: /\n" if config.DEMO
        else f"User-agent: *\nAllow: /\nDisallow: /charte/\n\nSitemap: {config.SITE_URL}/sitemap.xml\n", encoding="utf-8")
    (DIST / ".htaccess").write_text(htaccess(redirections), encoding="utf-8")

    mode = "MAQUETTE (noindex)" if config.DEMO else "PRODUCTION"
    print(f"✓ {len(pages)} pages générées dans dist/ — {len(redirections)} redirections 301 — {n_img} portraits recalculés — mode {mode}")


if __name__ == "__main__":
    main()
