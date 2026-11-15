"""Gabarit commun : en-tête, navigation, pied de page, petits composants HTML."""
import json
import time
from html import escape

import config
from data.chirurgiens import CHIRURGIENS, nom_complet

C = config.CABINET
VERSION = time.strftime("%Y%m%d%H%M%S")

NAV = [
    ("/chirurgiens/", "Chirurgiens"),
    ("/specialites/", "Spécialités"),
    ("/explorer/", "Explorer"),
    ("/parcours-de-soins/", "Parcours de soins"),
    ("/preparer/", "Préparer"),
    ("/prevention/", "Prévention"),
    ("/centres/", "Centres"),
]


def e(texte):
    return escape(str(texte), quote=True)


def u(chemin):
    """Adresse interne, préfixée pour une publication dans un sous-dossier."""
    return config.BASE + chemin


def texte_riche(texte):
    """Paragraphes séparés par une ligne vide ; lignes « - » rendues en liste."""
    blocs = []
    for bloc in texte.split("\n\n"):
        lignes = [l for l in bloc.split("\n") if l.strip()]
        puces = [l[2:] for l in lignes if l.startswith("- ")]
        avant = [l for l in lignes if not l.startswith("- ")]
        if avant:
            blocs.append(f"<p>{e(' '.join(avant))}</p>")
        if puces:
            blocs.append("<ul class=\"liste\">" + "".join(f"<li>{e(p)}</li>" for p in puces) + "</ul>")
    return "".join(blocs)


def liste(elements, classe="liste"):
    return f'<ul class="{classe}">' + "".join(f"<li>{e(x)}</li>" for x in elements) + "</ul>"


def provisoire(texte="Contenu provisoire — à valider par l'équipe"):
    return f'<p class="provisoire"><span aria-hidden="true">◇</span> {e(texte)}</p>'


def sur_titre(texte):
    return f'<p class="sur-titre">{e(texte)}</p>'


def lien_tel(numero, classe="", libelle=None):
    """En démonstration, le lien n'appelle pas : un message explique ce qu'il fera en ligne."""
    propre = "+33" + numero.replace(" ", "")[1:]
    attributs = f'href="#" data-demo-tel="{e(numero)}"' if config.DEMO else f'href="tel:{propre}"'
    return f'<a class="{classe}" {attributs}>{e(libelle or numero)}</a>'


def bouton_rdv(classe="btn", libelle="Prendre rendez-vous", chirurgien=None):
    cible = u("/rendez-vous/") + (f"?c={chirurgien}" if chirurgien else "")
    return f'<a class="{classe}" href="{cible}">{e(libelle)}<span class="btn__fleche" aria-hidden="true"></span></a>'


def portrait(c, taille=400, largeur=400, hauteur=500, classe=""):
    return (f'<img class="{classe}" src="{u("/img/" + c["slug"] + f"-{taille}.webp")}" width="{largeur}" height="{hauteur}" '
            f'alt="Portrait du {e(nom_complet(c))}" loading="lazy" decoding="async">')


def image_organe(o, taille=640):
    """Image réaliste de l'organe (générée par IA, à valider)."""
    return (f'<img src="{u("/assets/img/organes/" + o["cle"] + ".webp")}" width="{taille}" height="{taille}" '
            f'alt="Illustration réaliste : {e(o["nom"].lower())}" loading="lazy" decoding="async">')


def carte_medecin(c):
    """Portrait ; au survol ou au focus, les spécialités se révèlent."""
    specialites = "".join(f"<li>{e(s)}</li>" for s, _ in c["specialites"])
    return f'''<article class="medecin">
  <a class="medecin__lien" href="{u("/chirurgiens/" + c["slug"] + "/")}" aria-label="{e(nom_complet(c))} — voir la fiche">
    <span class="medecin__photo">{portrait(c)}</span>
    <span class="medecin__voile" aria-hidden="true"><span class="repere">Compétences</span><ul>{specialites}</ul></span>
  </a>
  <div class="medecin__bas">
    <h3 class="medecin__nom">{e(nom_complet(c))}</h3>
    <p class="medecin__role">{e(c["accroche"])}</p>
    {bouton_rdv("lien-fleche", "Rendez-vous", c["slug"])}
  </div>
</article>'''


def fil(chemin_noms):
    """Fil d'Ariane : [(adresse ou None, libellé), …]."""
    morceaux = [f'<a href="{u("/")}">Accueil</a>']
    for adresse, nom in chemin_noms:
        morceaux.append(f'<a href="{u(adresse)}">{e(nom)}</a>' if adresse else f'<span aria-current="page">{e(nom)}</span>')
    return '<nav class="fil" aria-label="Fil d\'Ariane">' + '<span aria-hidden="true">/</span>'.join(morceaux) + "</nav>"


def bandeau(sur, titre, chapo, ariane, extra=""):
    """En-tête des pages intérieures (fond nuit, lignes fines)."""
    return f'''<header class="bandeau plan plan--nuit">
  <div class="bandeau__lignes" aria-hidden="true"></div>
  <div class="contenu">
    {fil(ariane)}
    {sur_titre(sur)}
    <h1 class="titre-xl">{titre}</h1>
    <p class="chapo">{e(chapo)}</p>
    {extra}
  </div>
</header>'''


def _entete(actif):
    liens = "".join(
        f'<li><a href="{u(a)}"{" aria-current=\"page\"" if actif.startswith(a) else ""}>{e(n)}</a></li>' for a, n in NAV)
    return f'''<a class="evitement" href="#contenu">Aller au contenu</a>
<div class="lecture" data-lecture-page aria-hidden="true"></div>
<header class="entete" data-entete>
  <a class="marque" href="{u("/")}" aria-label="Nemaudig — accueil">
    <span class="marque__nom">NEMAUDIG</span>
    <span class="marque__metier">Chirurgie digestive · Nîmes</span>
  </a>
  <nav class="nav" id="nav" aria-label="Navigation principale"><ul>{liens}</ul>
    <div class="nav__bas">{lien_tel(C["telephone_affiche"], "nav__tel")}<span>{e(C["horaires_affiches"])}</span></div>
  </nav>
  <div class="entete__actions">
    <button class="maquette-btn" type="button" data-ouvre="tiroir-maquette" aria-haspopup="dialog">Maquette</button>
    {bouton_rdv("btn btn--compact")}
    <button class="burger" type="button" aria-controls="nav" aria-expanded="false" data-burger><span></span><span></span><span class="visuellement-cache">Menu</span></button>
  </div>
</header>'''


def _tiroir_maquette():
    reel = ["Les cinq chirurgiens, leurs diplômes et leurs spécialités (site actuel)",
            "Les 24 fiches de pathologies et les techniques opératoires (site actuel)",
            "Coordonnées, établissements, horaires, parcours (site actuel)",
            "Les portraits des chirurgiens, validés par l'équipe"]
    a_venir = ["Les images d'organes : générées par IA, anatomie à faire valider",
               "Les 5 vidéos : emplacements seulement, storyboards et prompts prêts",
               "Fiches d'organes et d'examens : textes de vulgarisation à valider par l'équipe",
               "Prise de rendez-vous : lien Maiia générique, liens directs à fournir",
               "Attribution chirurgien ↔ organe : proposée d'après les spécialités affichées"]
    return f'''<dialog class="tiroir" id="tiroir-maquette" aria-labelledby="tiroir-titre">
  <div class="tiroir__tete"><p class="sur-titre">Démonstration</p>
    <button class="tiroir__fermer" type="button" data-ferme aria-label="Fermer">×</button></div>
  <h2 class="titre-m" id="tiroir-titre">À propos de cette maquette</h2>
  <p>Proposition de nouveau site pour le cabinet Nemaudig. Elle n'est pas en ligne et n'est pas référencée.</p>
  <h3 class="repere">Déjà réel</h3>{liste(reel, "liste liste--coche")}
  <h3 class="repere">Provisoire, signalé par ◇</h3>{liste(a_venir, "liste liste--losange")}
  <a class="lien-fleche" href="{u("/maquette/")}">Ce que ce site apporte au cabinet</a>
</dialog>'''


def _pied():
    ad = C["adresse"]
    colonnes = "".join(f'<li><a href="{u(a)}">{e(n)}</a></li>' for a, n in NAV)
    equipe = "".join(f'<li><a href="{u("/chirurgiens/" + c["slug"] + "/")}">{e(nom_complet(c))}</a></li>' for c in CHIRURGIENS)
    return f'''<footer class="pied plan plan--prune">
  <div class="contenu pied__grille">
    <div class="pied__marque">
      <img src="{u("/assets/img/logo-nemaudig-320.webp")}" width="96" height="95" alt="Logo du cabinet Nemaudig" loading="lazy">
      <p>{e(C["statut"])}.</p>
      <p>{e(ad["rue"])}<br>{e(ad["complement"])}<br>{e(ad["code_postal"])} {e(ad["ville"])}</p>
      <p>{lien_tel(C["telephone_affiche"], "pied__tel")}<br>{e(C["horaires_affiches"])}</p>
    </div>
    <nav aria-label="Rubriques"><h2 class="repere">Le site</h2><ul>{colonnes}<li><a href="{u("/rendez-vous/")}">Prendre rendez-vous</a></li></ul></nav>
    <nav aria-label="Chirurgiens"><h2 class="repere">L'équipe</h2><ul>{equipe}</ul></nav>
    <div><h2 class="repere">En cas d'urgence</h2>
      <p>{e(C["urgences_nom"])}<br>{lien_tel(C["urgences_tel"], "pied__tel")}</p>
      <p>Urgence vitale : composez le 15.</p></div>
  </div>
  <div class="contenu pied__bas">
    <p>© {time.strftime("%Y")} Nemaudig · <a href="{u("/mentions-legales/")}">Mentions légales</a> · <a href="{u("/confidentialite/")}">Confidentialité</a> · <a href="{u("/maquette/")}">À propos de la maquette</a></p>
    <p>Ce site n'utilise aucun cookie ni traceur. Les informations médicales ne remplacent pas une consultation.</p>
    <p class="pied__credit">Images d'organes : illustrations générées par intelligence artificielle.</p>
  </div>
</footer>
<div class="barre-mobile" data-barre>
  {lien_tel(C["telephone_affiche"], "barre-mobile__tel", "Appeler")}
  {bouton_rdv("barre-mobile__rdv", "Prendre rendez-vous")}
</div>
<div class="toast" role="status" aria-live="polite" data-toast></div>'''


def page(*, chemin, titre, description, corps, scripts=(), classe="", donnees=None, json_ld=None):
    """Assemble une page complète. `scripts` : modules de assets/js à charger en plus de site.js."""
    v = f"?v={VERSION}"
    modules = "".join(f'<script type="module" src="{u("/assets/js/" + s)}{v}"></script>' for s in ("site.js", *scripts))
    bloc_donnees = (f'<script type="application/json" id="donnees">{json.dumps(donnees, ensure_ascii=False).replace("</", "<\\/")}</script>'
                    if donnees is not None else "")
    bloc_ld = (f'<script type="application/ld+json">{json.dumps(json_ld, ensure_ascii=False).replace("</", "<\\/")}</script>' if json_ld else "")
    robots = '<meta name="robots" content="noindex, nofollow">' if config.DEMO else ""
    return f'''<!doctype html>
<html lang="fr" data-base="{e(config.BASE)}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titre)}</title>
<meta name="description" content="{e(description)}">
{robots}
<meta name="theme-color" content="#FBF6F1">
<link rel="canonical" href="{config.SITE_URL}{chemin}">
<link rel="icon" href="{u("/favicon-32.png")}" sizes="32x32">
<link rel="apple-touch-icon" href="{u("/apple-touch-icon.png")}">
<link rel="preload" href="{u("/assets/fonts/outfit-var.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{u("/assets/fonts/geist-var.woff2")}" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{u("/assets/css/site.css")}{v}">
<script>document.documentElement.classList.add("js");if(/[?&](p|fige|vue)=/.test(location.search))document.documentElement.classList.add("fige")</script>
{bloc_ld}
</head>
<body class="{classe}">
{_entete(chemin)}
<main id="contenu">
{corps}
</main>
{_pied()}
{_tiroir_maquette()}
{bloc_donnees}
{modules}
</body>
</html>'''
