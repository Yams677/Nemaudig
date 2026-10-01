"""Gabarit commun : <head>, en-tête, méga-menu, pied de page, données structurées."""

import json

import config
from data.chirurgiens import CHIRURGIENS, nom_complet
from data.pathologies import FAMILLES, par_famille
from lib.anatomie import planche
from lib.html import C, ICONES, bouton, e, tel_href

FAMILLES_MENU = ["oesophage-estomac", "foie-vesicule-pancreas", "colon-rectum", "proctologie", "paroi-abdominale"]

NAV = [
    ("/pathologies/", "Pathologies", "mega"),
    ("/chirurgiens/", "Chirurgiens", None),
    ("/obesite/", "Obésité", None),
    ("/techniques/", "Techniques", None),
    ("/votre-parcours/", "Votre parcours", None),
    ("/cabinet/", "Le cabinet", None),
]


def json_ld(obj):
    return f'<script type="application/ld+json">{json.dumps(obj, ensure_ascii=False, separators=(",", ":"))}</script>'


def organisation():
    a = C["adresse"]
    return {
        "@context": "https://schema.org",
        "@type": ["MedicalClinic", "MedicalOrganization"],
        "@id": f"{config.SITE_URL}/#cabinet",
        "name": "Nemaudig",
        "alternateName": "Cabinet Nemaudig — chirurgie digestive et viscérale",
        "description": "Association libérale de cinq chirurgiens digestifs et viscéraux à Nîmes.",
        "url": f"{config.SITE_URL}/",
        "logo": f"{config.SITE_URL}/assets/img/logo-nemaudig.png",
        "image": f"{config.SITE_URL}/og-nemaudig.png",
        "telephone": C["telephone_e164"],
        "email": C["email"],
        "medicalSpecialty": ["Surgical", "Gastroenterologic", "Oncologic"],
        "address": {"@type": "PostalAddress", "streetAddress": f"{a['rue']}, {a['complement']}",
                    "postalCode": a["code_postal"], "addressLocality": a["ville"],
                    "addressRegion": a["region"], "addressCountry": a["pays"]},
        "geo": {"@type": "GeoCoordinates", "latitude": C["geo"]["lat"], "longitude": C["geo"]["lng"]},
        "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": j, "opens": o, "closes": f}
                                      for j, o, f in C["horaires"]],
        "areaServed": [{"@type": "City", "name": "Nîmes"}, {"@type": "City", "name": "Uzès"},
                       {"@type": "AdministrativeArea", "name": "Gard"}],
        "isAcceptingNewPatients": True,
        "employee": [{"@type": "Physician", "name": nom_complet(c), "url": f"{config.SITE_URL}/chirurgiens/{c['slug']}/"}
                     for c in CHIRURGIENS],
    }


def fil_ariane(fil):
    """fil : liste de (url, libellé) — le dernier élément est la page courante."""
    if not fil:
        return "", None
    items = [("/", "Accueil")] + fil
    html = '<nav class="fil" aria-label="Fil d\'Ariane"><ol>' + "".join(
        (f'<li><a href="{u}">{e(l)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{e(l)}</li>')
        for i, (u, l) in enumerate(items)) + "</ol></nav>"
    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": l, "item": f"{config.SITE_URL}{u}"} for i, (u, l) in enumerate(items)]}
    return html, schema


def mega_menu():
    colonnes = []
    for slug in FAMILLES_MENU:
        f = next(x for x in FAMILLES if x["slug"] == slug)
        liens = "".join(f'<li><a href="/pathologies/{p["slug"]}/">{e(p["court"])}</a></li>' for p in par_famille(slug))
        colonnes.append(f'<div class="mega__col" data-organe-survol="{f["organe"]}"><a class="mega__titre" href="/pathologies/{slug}/">{e(f["titre"])}</a><ul>{liens}</ul></div>')
    return f'''<div class="mega" id="mega-pathologies">
  <div class="mega__inner">
    <div class="mega__planche" aria-hidden="true">{planche(ident="planche-mega", classe="planche--mini")}</div>
    <div class="mega__grille">{"".join(colonnes)}
      <div class="mega__col mega__col--extra">
        <a class="mega__titre" href="/cancerologie/">Cancérologie digestive</a>
        <a class="mega__titre" href="/obesite/">Chirurgie de l'obésité</a>
        <a class="mega__titre" href="/pathologies/surrenales/">Glandes surrénales</a>
        <a class="mega__titre" href="/pathologies/kystes-et-lipomes/">Kystes et lipomes</a>
        <a class="mega__titre" href="/pathologies/port-a-cath/">Port-à-cath</a>
        <a class="mega__tout" href="/pathologies/">Toutes les pathologies {ICONES["fleche"]}</a>
      </div>
    </div>
  </div>
</div>'''


def entete(url):
    def actif(lien):
        return ' aria-current="page"' if url == lien or (lien != "/" and url.startswith(lien)) else ""

    items = []
    for lien, libelle, mega in NAV:
        if mega:
            items.append(f'<li class="nav__item nav__item--mega"><a class="nav__lien" href="{lien}"{actif(lien)} aria-haspopup="true" aria-controls="mega-pathologies">{libelle}<span class="nav__chevron" aria-hidden="true"></span></a>{mega_menu()}</li>')
        else:
            items.append(f'<li class="nav__item"><a class="nav__lien" href="{lien}"{actif(lien)}>{libelle}</a></li>')
    return f'''<a class="evitement" href="#contenu">Aller au contenu</a>
<div class="bandeau-info">
  <div class="conteneur bandeau-info__inner">
    <p><span class="point-vif" aria-hidden="true"></span>{e(C["horaires_affiches"])} · <a href="{tel_href()}">{C["telephone_affiche"]}</a></p>
    <p class="bandeau-info__urgences">{ICONES["urgence"]} <span>Urgences<span class="bandeau-info__long"> de la Polyclinique du Grand Sud</span><span class="bandeau-info__court"> Polyclinique Grand Sud</span>&nbsp;:</span> <a href="{tel_href(C["urgences_e164"])}">{C["urgences_tel"]}</a></p>
  </div>
</div>
<header class="entete" data-entete>
  <div class="conteneur entete__inner">
    <a class="logo" href="/" aria-label="Nemaudig — accueil">
      <img class="logo__image" src="/assets/img/logo-nemaudig-160.webp" srcset="/assets/img/logo-nemaudig-160.webp 160w, /assets/img/logo-nemaudig-320.webp 320w, /assets/img/logo-nemaudig-480.webp 480w" sizes="84px" width="84" height="83" alt="Logo Nemaudig — chirurgie digestive">
      <span class="logo__texte"><strong>Nemaudig</strong><small>Chirurgie digestive · Nîmes</small></span>
    </a>
    <nav class="nav" aria-label="Navigation principale" data-nav>
      <ul class="nav__liste">{"".join(items)}</ul>
      <div class="nav__mobile-pied">
        {bouton("/contact/", "Prendre rendez-vous", "plein", icone="agenda")}
        <a class="nav__tel" href="{tel_href()}">{ICONES["tel"]} {C["telephone_affiche"]}</a>
      </div>
    </nav>
    <div class="entete__actions">
      <a class="btn btn--plein btn--compact" href="/contact/">{ICONES["agenda"]}<span>Rendez-vous</span></a>
      <button class="burger" type="button" aria-expanded="false" aria-controls="menu-mobile" aria-label="Ouvrir le menu" data-burger>{ICONES["menu"]}{ICONES["croix"]}</button>
    </div>
  </div>
</header>'''


def pied():
    a = C["adresse"]
    chirs = "".join(f'<li><a href="/chirurgiens/{c["slug"]}/">{e(nom_complet(c))}</a></li>' for c in CHIRURGIENS)
    return f'''<footer class="pied">
  <div class="conteneur">
    <div class="pied__cta">
      <div>
        <p class="pied__cta-titre">Un rendez-vous, une question&nbsp;?</p>
        <p>Nos trois secrétaires vous répondent {e(C["horaires_affiches"].lower())}.</p>
      </div>
      <div class="pied__cta-actions">
        {bouton(tel_href(), C["telephone_affiche"], "clair", icone="tel")}
        {bouton("/contact/", "Prendre rendez-vous en ligne", "ligne-clair", icone="agenda")}
      </div>
    </div>
    <div class="pied__grille">
      <div class="pied__col pied__col--id">
        <img class="pied__logo" src="/assets/img/logo-nemaudig-320.webp" srcset="/assets/img/logo-nemaudig-320.webp 320w, /assets/img/logo-nemaudig-480.webp 480w" sizes="170px" width="170" height="169" alt="Logo Nemaudig — chirurgie digestive" loading="lazy">
        <p class="pied__nom">Nemaudig</p>
        <p>{e(config.CABINET["statut"])}.</p>
        <address>{e(a["rue"])}<br>{e(a["complement"])}<br>{a["code_postal"]} {e(a["ville"])}</address>
        <p><a href="{tel_href()}">{C["telephone_affiche"]}</a><br>{e(C["horaires_affiches"])}</p>
      </div>
      <div class="pied__col"><p class="pied__titre">Chirurgiens</p><ul>{chirs}</ul></div>
      <div class="pied__col"><p class="pied__titre">Spécialités</p><ul>
        <li><a href="/pathologies/oesophage-estomac/">Œsophage et estomac</a></li>
        <li><a href="/pathologies/foie-vesicule-pancreas/">Foie, vésicule, pancréas</a></li>
        <li><a href="/pathologies/colon-rectum/">Côlon et rectum</a></li>
        <li><a href="/pathologies/proctologie/">Proctologie</a></li>
        <li><a href="/pathologies/paroi-abdominale/">Hernies et paroi</a></li>
        <li><a href="/cancerologie/">Cancérologie digestive</a></li>
        <li><a href="/obesite/">Chirurgie de l'obésité</a></li>
      </ul></div>
      <div class="pied__col"><p class="pied__titre">Patients</p><ul>
        <li><a href="/votre-parcours/">Votre parcours</a></li>
        <li><a href="/honoraires/">Honoraires</a></li>
        <li><a href="/etablissements/">Établissements</a></li>
        <li><a href="/consultation-uzes/">Consultation à Uzès</a></li>
        <li><a href="/faq/">Questions fréquentes</a></li>
        <li><a href="/videos/">Vidéos</a></li>
        <li><a href="/actualites/">Actualités</a></li>
      </ul></div>
    </div>
    <div class="pied__alerte">
      <p>{ICONES["urgence"]} <strong>Urgence vitale : composez le 15.</strong> Urgences de la Polyclinique du Grand Sud : <a href="{tel_href(C["urgences_e164"])}">{C["urgences_tel"]}</a>.</p>
      <p>Les informations médicales de ce site sont générales : elles ne remplacent pas une consultation avec votre chirurgien.</p>
    </div>
    <div class="pied__bas">
      <p>© Nemaudig — chirurgiens digestifs et viscéraux à Nîmes</p>
      <ul><li><a href="/mentions-legales/">Mentions légales</a></li><li><a href="/confidentialite/">Confidentialité</a></li><li><a href="/plan-du-site/">Plan du site</a></li></ul>
    </div>
  </div>
</footer>'''


def page(assets, url, titre, desc, corps, fil=None, schemas=None, indexer=True, classe="", extra_tete=""):
    canonique = f"{config.SITE_URL}{url}"
    robots = "noindex, nofollow" if (config.DEMO or not indexer) else "index, follow, max-image-preview:large"
    fil_html, fil_schema = fil_ariane(fil)
    tous_schemas = [organisation()] if url == "/" else []
    tous_schemas += [s for s in (schemas or []) if s]
    if fil_schema:
        tous_schemas.append(fil_schema)
    bandeau_demo = ('<div class="demo" role="note"><span>Maquette de démonstration</span> — contenus repris du site nemaudig.fr, '
                    'mise en page entièrement nouvelle. Non indexée.</div>') if config.DEMO else ""
    return f'''<!doctype html>
<html lang="fr" class="no-js">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(titre)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonique}">
<meta name="theme-color" content="#413B5D">
<meta property="og:type" content="website">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="Nemaudig">
<meta property="og:title" content="{e(titre)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canonique}">
<meta property="og:image" content="{config.SITE_URL}/og-nemaudig.png">
<link rel="icon" href="/favicon-32.png" type="image/png" sizes="32x32">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<link rel="preload" href="/assets/fonts/fraunces-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/hanken-grotesk-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{assets["css"]}">
<script>document.documentElement.classList.replace("no-js","js")</script>
<script src="{assets["js"]}" defer></script>
{extra_tete}
{"".join(json_ld(s) for s in tous_schemas)}
</head>
<body class="{classe}">
{bandeau_demo}
{entete(url)}
<main id="contenu" tabindex="-1">
{f'<div class="conteneur">{fil_html}</div>' if fil_html else ""}
{corps}
</main>
{pied()}
</body>
</html>'''
