"""
Maquette C « Anatomie de verre » — génération du site statique.

    PYTHONIOENCODING=utf-8 python build.py      # → dist/

Contrôles bloquants : un seul <h1> par page, titres et descriptions uniques,
liens internes et ancres existants, identifiants uniques.
"""
import re
import shutil
import sys
from pathlib import Path

import config
from data.videos_ia import FORMAT, NEGATIF, STYLE, VIDEOS
from lib.gabarit import VERSION
from pages import accueil, annexes, equipe, explorer, parcours, pratique, specialites

RACINE = Path(__file__).parent
SRC, DIST, DOCS = RACINE / "src", RACINE / "dist", RACINE / "docs"
CSS = ["socle.css", "organes.css", "composants.css", "accueil.css", "animations.css", "pages.css", "impression.css"]


def horodatage(s):
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}.000"


def sous_titres(v):
    lignes, t = ["WEBVTT", ""], 0
    for duree, _, texte in v["plans"]:
        lignes += [f"{horodatage(t)} --> {horodatage(t + duree)}", texte, ""]
        t += duree
    return "\n".join(lignes)


def prompts_markdown():
    blocs = ["# Vidéos IA — storyboards et prompts de génération", "",
             "Cinq séquences à produire (Veo, Kling, Runway…). Aucune n'existe encore : le site affiche des",
             "emplacements « Séquence en préparation ». Fichier généré par `build.py` depuis `data/videos_ia.py`.", "",
             "## Règles communes", "",
             f"- **Image** : {FORMAT['image']}", f"- **Fichiers** : {FORMAT['fichiers']}", f"- **Poids** : {FORMAT['poids']}",
             f"- **Sous-titres** : {FORMAT['sous_titres']} (fichiers prêts dans `dist/videos/`)",
             "- **Deux versions** : la courte suit le storyboard ; la détaillée reprend chaque plan en le ralentissant (×3 environ) et ajoute un texte d'accompagnement validé par l'équipe.",
             "- **Méthode conseillée** : générer d'abord une image de référence par plan (capture de l'explorateur 3D du site), puis animer cette image (image-to-video) : l'anatomie reste celle du modèle réel.",
             "- **Avant publication** : chaque séquence est relue par un chirurgien de l'équipe.", "",
             "### Style commun (à placer à la fin de chaque prompt)", "", "```", STYLE, "```", "",
             "### Prompt négatif", "", "```", NEGATIF, "```", ""]
    for v in VIDEOS:
        blocs += [f"## {v['numero']} — {v['titre']}", "", v["objet"], "",
                  f"Durée : {v['courte']} s (courte) · {v['detaillee']} s (détaillée) — sous-titres : `videos/{v['id']}.fr.vtt`", "",
                  "| Temps | À l'image | Sous-titre |", "|---|---|---|"]
        t = 0
        for duree, visuel, texte in v["plans"]:
            blocs.append(f"| {t:02d}–{t + duree:02d} s | {visuel} | {texte} |")
            t += duree
        blocs += ["", "**Prompt**", "", "```", f"{v['prompt']} {STYLE}", "```", "", "**À vérifier avant publication**", ""]
        blocs += [f"- [ ] {x}" for x in v["verifier"]] + [""]
    return "\n".join(blocs)


def controler(sorties):
    """Refuse la génération si une page est incohérente."""
    erreurs, titres, descriptions = [], {}, {}
    chemins = {c for c, _ in sorties}
    ancres = {c: set(re.findall(r'\bid="([^"]+)"', h)) for c, h in sorties}
    for chemin, html in sorties:
        if len(re.findall(r"<h1[\s>]", html)) != 1:
            erreurs.append(f"{chemin} : il faut exactement un <h1>")
        ids = re.findall(r'\bid="([^"]+)"', html)
        doublons = {i for i in ids if ids.count(i) > 1}
        if doublons:
            erreurs.append(f"{chemin} : identifiants en double {sorted(doublons)}")
        titre = re.search(r"<title>(.*?)</title>", html).group(1)
        desc = re.search(r'<meta name="description" content="(.*?)"', html).group(1)
        for registre, valeur, nom in ((titres, titre, "titre"), (descriptions, desc, "description")):
            if valeur in registre:
                erreurs.append(f"{chemin} : {nom} identique à {registre[valeur]}")
            registre[valeur] = chemin
        for lien in re.findall(r'href="([^"]+)"', html):
            if lien.startswith(("http", "mailto:", "tel:")) or lien == "#":
                continue
            lien = lien[len(config.BASE):] if config.BASE and lien.startswith(config.BASE) else lien
            cible, _, ancre = lien.partition("#")
            cible = cible.split("?")[0] or chemin
            if cible.startswith(("/assets/", "/img/", "/favicon", "/apple")):
                continue
            if cible not in chemins:
                erreurs.append(f"{chemin} : lien vers une page absente {lien}")
            elif ancre and ancre not in ancres[cible]:
                erreurs.append(f"{chemin} : ancre absente {lien}")
    return erreurs


def main():
    sorties = []
    for module in (accueil, equipe, specialites, explorer, parcours, pratique, annexes):
        sorties += module.pages()
    erreurs = controler(sorties)
    if erreurs:
        print("\n".join("✗ " + x for x in erreurs))
        sys.exit(1)

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(SRC, DIST, ignore=shutil.ignore_patterns("*.css"))
    for chemin, html in sorties:
        cible = DIST / chemin.lstrip("/") if chemin.endswith(".html") else DIST / chemin.strip("/") / "index.html"
        cible.parent.mkdir(parents=True, exist_ok=True)
        cible.write_text(html, encoding="utf-8")

    # Une seule feuille de style, dans l'ordre de la cascade
    css = "\n".join((SRC / "assets" / "css" / nom).read_text(encoding="utf-8") for nom in CSS)
    (DIST / "assets" / "css").mkdir(parents=True, exist_ok=True)
    (DIST / "assets" / "css" / "site.css").write_text(css.replace("url(/", f"url({config.BASE}/"), encoding="utf-8")

    # Même version sur les modules importés entre eux (sinon le navigateur garde les anciens)
    for js in (DIST / "assets" / "js").glob("*.js"):
        texte = js.read_text(encoding="utf-8")
        js.write_text(re.sub(r'from "\./([a-z0-9-]+\.js)"', lambda m: f'from "./{m.group(1)}?v={VERSION}"', texte), encoding="utf-8")

    (DIST / "videos").mkdir(exist_ok=True)
    for v in VIDEOS:
        (DIST / "videos" / f"{v['id']}.fr.vtt").write_text(sous_titres(v), encoding="utf-8")
    DOCS.mkdir(exist_ok=True)
    (DOCS / "PROMPTS-VIDEO.md").write_text(prompts_markdown(), encoding="utf-8")

    (DIST / "robots.txt").write_text("User-agent: *\nDisallow: /\n" if config.DEMO else "User-agent: *\nAllow: /\n", encoding="utf-8")
    (DIST / ".nojekyll").write_text("", encoding="utf-8")
    print(f"✓ dist/ — {len(sorties)} pages · maquette C « Anatomie de verre »")


if __name__ == "__main__":
    main()
