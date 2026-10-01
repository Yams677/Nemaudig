"""Pathologies : hub, familles (par région du corps), fiches, cancérologie."""

import re

import config
from data.cabinet import VALEURS
from data.chirurgiens import CHIRURGIENS
from data.pathologies import FAM, FAMILLES, PATHOLOGIES, par_famille
from lib.anatomie import planche
from lib.composants import bandeau_rdv, carte_patho, faq, mini_medecin, schema_faq, tete_page, video
from lib.html import ICONES, e, riche, surtitre
from lib.layout import page

TEINTES = {"oesophage-estomac": "var(--lilas)", "foie-vesicule-pancreas": "var(--peche)", "colon-rectum": "var(--menthe)",
           "proctologie": "var(--rose)", "paroi-abdominale": "var(--ciel)", "endocrinien": "var(--sable)",
           "pathologie-generale": "var(--sauge)"}
HUBS = ["oesophage-estomac", "foie-vesicule-pancreas", "colon-rectum", "proctologie", "paroi-abdominale"]
ANCIENS_HUBS = {"oesophage-estomac": None, "foie-vesicule-pancreas": "pathologies-de-la-vesicule-biliaire-et-du-foie",
                "colon-rectum": "pathologies-du-colon", "proctologie": "proctologie", "paroi-abdominale": "pathologies-de-la-paroi-abdominale"}

REDIRECTIONS = {p["ancien"]: f"/pathologies/{p['slug']}/" for p in PATHOLOGIES}
REDIRECTIONS.update({a: f"/pathologies/{h}/" for h, a in ANCIENS_HUBS.items() if a})
REDIRECTIONS.update({"pathologies-et-interventions": "/pathologies/", "pathologies": "/pathologies/",
                     "pathologie-generale": "/pathologies/#peau-et-dispositifs", "pathologies-du-rectum": "/pathologies/cancer-du-rectum/",
                     "pathologies-liees-au-cancer": "/cancerologie/", "cancerologie": "/cancerologie/"})

# Chirurgiens à mettre en avant par fiche (d'après leurs spécialités déclarées).
def chirurgiens_pour(slug):
    return [c["slug"] for c in CHIRURGIENS if slug in c["pathologies"]]


def ancre(titre):
    t = titre.lower()
    for a, b in (("é", "e"), ("è", "e"), ("ê", "e"), ("à", "a"), ("â", "a"), ("ô", "o"), ("î", "i"), ("ï", "i"), ("ç", "c"), ("œ", "oe"), ("'", "-"), ("’", "-")):
        t = t.replace(a, b)
    return re.sub(r"[^a-z0-9]+", "-", t).strip("-")


def page_hub(assets):
    blocs = []
    for i, slug in enumerate(HUBS):
        f = FAM[slug]
        cartes = "".join(carte_patho(p) for p in par_famille(slug))
        blocs.append(f'''<section class="section section--serree" id="{slug}" aria-labelledby="h-{slug}"><div class="conteneur">
  <div class="section__tete section__tete--2"><div>{surtitre(f["titre"], f"{i + 1:02d}")}<h2 id="h-{slug}"><a href="/pathologies/{slug}/" style="text-decoration:none">{e(f["titre"])}</a></h2></div>
  <p class="chapo">{e(f["intro"])}</p></div>
  <div class="liste-pathos">{cartes}</div></div></section>''')
    autres = [p for p in PATHOLOGIES if p["famille"] in ("endocrinien", "pathologie-generale")]
    blocs.append(f'''<section class="section section--serree" id="peau-et-dispositifs" aria-labelledby="h-autres"><div class="conteneur">
  <div class="section__tete section__tete--2"><div>{surtitre("Et aussi", "06")}<h2 id="h-autres">Surrénales, peau <em>et dispositifs</em></h2></div>
  <p class="chapo">Chirurgie des glandes surrénales, kystes et lipomes sous anesthésie locale, pose de chambre implantable.</p></div>
  <div class="liste-pathos">{"".join(carte_patho(p) for p in autres)}</div>
  <div class="grille grille--2 mt-7">
    <a class="famille famille--large" href="/cancerologie/" style="grid-column:auto"><div><span class="famille__num">Transversal</span><h3>Cancérologie digestive</h3><p>Œsophage, estomac, côlon, rectum, foie, pancréas.</p></div></a>
    <a class="famille famille--large" href="/obesite/" style="grid-column:auto"><div><span class="famille__num">Parcours dédié</span><h3>Chirurgie de l'obésité</h3><p>Ballon intragastrique, sleeve, bypass, anneau.</p></div></a>
  </div></div></section>''')
    corps = f'''<header class="tete-page tete-page--organe" style="--teinte:var(--menthe)"><div class="conteneur">
  <div>{surtitre("Pathologies et interventions")}<h1>Ce que nous opérons, <em>expliqué simplement.</em></h1>
  <p class="chapo">Les cinq chirurgiens prennent en charge l'ensemble des maladies de l'appareil digestif et de la paroi abdominale. Choisissez un organe sur la planche ou parcourez les familles ci-dessous.</p></div>
  <div class="tete-page__planche" data-planche-zone style="max-width:280px;position:relative">{planche(interactif=True, ident="planche-hub")}<span class="hero__legende" data-legende aria-hidden="true"></span></div>
</div></header>''' + "".join(blocs) + bandeau_rdv()
    return page(assets, "/pathologies/", "Pathologies digestives opérées à Nîmes — Nemaudig",
                "Hernies, vésicule, reflux, côlon, rectum, proctologie, foie, pancréas : toutes les pathologies prises en charge par les chirurgiens digestifs de Nemaudig à Nîmes.",
                corps, fil=[("/pathologies/", "Pathologies")])


def page_famille(assets, slug):
    f = FAM[slug]
    url = f"/pathologies/{slug}/"
    cartes = "".join(carte_patho(p) for p in par_famille(slug))
    chirs = sorted({c for p in par_famille(slug) for c in chirurgiens_pour(p["slug"])})
    medecins = "".join(mini_medecin(c) for c in chirs)
    vids = [v for p in par_famille(slug) for v in p["videos"]]
    vids = list(dict.fromkeys(vids))[:3]
    bloc_vid = (f'<section class="section section--blanc"><div class="conteneur"><div class="section__tete">{surtitre("En vidéo")}<h2>Au bloc opératoire</h2></div>'
                f'<div class="grille grille--3">{"".join(f"<div>{video(v)}</div>" for v in vids)}</div></div></section>') if vids else ""
    corps = tete_page(e(f["titre"]) + " <em>— chirurgie à Nîmes</em>", e(f["intro"]), "Pathologies", TEINTES[slug], organe=f["organe"] if slug != "paroi-abdominale" else "paroi") + f'''
<section class="section section--serree"><div class="conteneur"><div class="article" style="grid-template-columns:minmax(0,1fr) 300px">
  <div class="liste-pathos" style="grid-template-columns:1fr">{cartes}</div>
  <aside class="aside"><div class="encart"><h2>Chirurgiens concernés</h2>{medecins}</div>
  <div class="encart encart--menthe"><h2>Un doute sur votre situation&nbsp;?</h2><p>Une consultation permet de poser l'indication et de choisir la technique la plus adaptée.</p><a class="lien-fleche" href="/contact/">Prendre rendez-vous {ICONES["fleche"]}</a></div></aside>
</div></div></section>{bloc_vid}''' + bandeau_rdv()
    titre = f"{f['titre']} : chirurgie à Nîmes — Nemaudig"
    desc = {
        "oesophage-estomac": "Reflux gastro-œsophagien, hernie hiatale, cancers de l'œsophage et de l'estomac : la chirurgie de la partie haute du tube digestif à Nîmes.",
        "foie-vesicule-pancreas": "Calculs de la vésicule, cholécystectomie, chirurgie du foie et du pancréas : explications des chirurgiens digestifs de Nemaudig à Nîmes.",
        "colon-rectum": "Diverticulite, maladie de Crohn, rectocolite, cancers du côlon et du rectum : chirurgie colorectale par cœlioscopie et robot à Nîmes.",
        "proctologie": "Hémorroïdes, fissure anale, abcès et fistule, kyste pilonidal au laser : la proctologie chirurgicale à Nîmes avec l'équipe Nemaudig.",
        "paroi-abdominale": "Hernie inguinale, hernie ombilicale, éventration : réparation de la paroi abdominale par incision ou cœlioscopie, souvent en ambulatoire, à Nîmes.",
    }[slug]
    return page(assets, url, titre, desc, corps, fil=[("/pathologies/", "Pathologies"), (url, f["titre"])])


def page_patho(assets, p):
    url = f"/pathologies/{p['slug']}/"
    f = FAM[p["famille"]]
    sections = p["sections"] + ([("Questions fréquentes", None)] if p["faq"] else []) + ([("En vidéo", None)] if p["videos"] else [])
    sommaire = "".join(f'<li><a href="#{ancre(t)}">{e(t)}</a></li>' for t, _ in sections)
    blocs = []
    for i, (t, txt) in enumerate(p["sections"]):
        blocs.append(f'<section class="bloc-section" aria-labelledby="{ancre(t)}"><div class="bloc-section__tete"><span class="bloc-section__num">{i + 1:02d}</span><h2 id="{ancre(t)}">{e(t)}</h2></div>{riche(txt)}</section>')
    if p["faq"]:
        blocs.append(f'<section class="bloc-section" aria-labelledby="questions-frequentes"><h2 id="questions-frequentes">Questions fréquentes</h2>{faq(p["faq"], "faq-" + p["slug"])}</section>')
    if p["videos"]:
        blocs.append(f'<section class="bloc-section" aria-labelledby="en-video"><h2 id="en-video">En vidéo</h2><div class="grille grille--2">{"".join(f"<div>{video(v)}</div>" for v in p["videos"])}</div></section>')
    if p.get("a_completer") and config.DEMO:
        blocs.append('<p class="note-a-valider">Fiche à compléter avec le cabinet : le site actuel ne contient qu\'une vidéo pour cette rubrique.</p>')

    chirs = chirurgiens_pour(p["slug"])
    medecins = "".join(mini_medecin(c) for c in chirs) or "".join(mini_medecin(c["slug"]) for c in CHIRURGIENS)
    voisines = [x for x in par_famille(p["famille"]) if x is not p]
    liens_voisins = "".join(f'<li><a href="/pathologies/{x["slug"]}/"><span>{e(x["court"])}</span>{ICONES["fleche"]}</a></li>' for x in voisines)
    pdf = (f'<a class="pdf" href="{p["pdf"]}" target="_blank" rel="noopener">{ICONES["fichier"]}<span><strong>Fiche d\'information patient</strong>'
           f'<small>PDF · © Fédération de chirurgie viscérale et digestive</small></span></a>') if p["pdf"] else ""
    meta = f'<span class="pastille">{e(f["titre"])}</span>' + ('<span class="pastille pastille--lilas">Cancérologie · RCP</span>' if p.get("cancer") else "")

    corps = tete_page(e(p["titre"]), e(p["resume"]), "Pathologie · Nîmes", TEINTES[p["famille"]], organe=p["organe"], meta_html=meta) + f'''
<section class="section section--serree" style="padding-top:24px"><div class="conteneur">
  <div class="article">
    <nav class="sommaire" aria-label="Sommaire de la fiche" data-sommaire><p>Sur cette page</p><ol>{sommaire}</ol></nav>
    <div class="prose">{"".join(blocs)}</div>
    <aside class="aside">
      <div class="encart encart--lagon"><h2>Consulter un chirurgien</h2><p>Le secrétariat vous oriente vers le chirurgien le plus adapté à votre situation.</p>
        <a class="btn btn--clair" href="/contact/">{ICONES["agenda"]}<span>Prendre rendez-vous</span><span class="btn__fleche" aria-hidden="true">{ICONES["fleche"]}</span></a></div>
      <div class="encart"><h2>{"Chirurgiens concernés" if chirs else "L'équipe"}</h2>{medecins}</div>
      {f'<div class="encart">{pdf}</div>' if pdf else ""}
      {f'<div class="encart"><h2>Même famille</h2><ul class="encart__liste">{liens_voisins}</ul></div>' if voisines else ""}
      {'<div class="encart encart--peche"><h2>Cancérologie</h2><p>Tous les dossiers sont présentés et validés en réunion de concertation pluridisciplinaire de cancérologie digestive.</p><a class="lien-fleche" href="/cancerologie/">La prise en charge ' + ICONES["fleche"] + '</a></div>' if p.get("cancer") else ""}
    </aside>
  </div>
</div></section>''' + bandeau_rdv()

    schema = {"@context": "https://schema.org", "@type": "MedicalWebPage", "name": p["titre"], "url": f"{config.SITE_URL}{url}",
              "inLanguage": "fr-FR", "audience": {"@type": "MedicalAudience", "audienceType": "Patient"},
              "about": {"@type": "MedicalCondition", "name": p["titre"]},
              "publisher": {"@id": f"{config.SITE_URL}/#cabinet"}}
    titre = f"{p['titre']} — chirurgie à Nîmes"
    if len(titre) > 66:
        titre = f"{p['court']} — chirurgie digestive à Nîmes"
    return page(assets, url, titre, p["desc"], corps,
                fil=[("/pathologies/", "Pathologies")] + ([(f"/pathologies/{p['famille']}/", f["titre"])] if p["famille"] in HUBS else []) + [(url, p["court"])],
                schemas=[schema, schema_faq(p["faq"])])


def page_cancero(assets):
    cancers = [p for p in PATHOLOGIES if p.get("cancer")]
    concertation = next(d for t, d in VALEURS if t == "La concertation")
    corps = tete_page("Cancérologie digestive <em>à Nîmes</em>",
                      "Nous prenons en charge tous les cancers du tube digestif — œsophage, estomac, intestin grêle, côlon, rectum, anus — mais également du foie, de la vésicule biliaire et du pancréas.",
                      "Cancérologie", "var(--lilas)", organe="colon-rectum") + f'''
<section class="section section--serree"><div class="conteneur">
  <div class="grille grille--2" style="align-items:start">
    <div class="encart encart--lagon" data-reveal><h2 style="font-size:1.6rem">Chaque dossier, discuté à plusieurs</h2>
      <p>Tous les dossiers de cancérologie sont présentés et validés en réunion pluridisciplinaire de cancérologie digestive, composée de cancérologues, de radiologues, de gastro-entérologues, de chirurgiens digestifs et de médecins anatomopathologistes, afin d'assurer la meilleure prise en charge possible, en concertation.</p></div>
    <div class="encart" data-reveal style="--d:1"><h2 style="font-size:1.6rem">Avec l'Institut de cancérologie du Gard</h2><p>{e(concertation)}</p>
      <p>Après l'opération, le suivi est régulier et rigoureux, selon les recommandations de la Haute Autorité de santé. Les examens complémentaires sont prescrits par l'équipe.</p></div>
  </div>
  <div class="section__tete mt-7">{surtitre("Les fiches")}<h2>Cancers opérés par l'équipe</h2></div>
  <div class="liste-pathos">{"".join(carte_patho(p) for p in cancers)}</div>
  <div class="section__tete mt-7">{surtitre("Chirurgiens")}<h2>Cancérologie digestive : <em>quatre spécialistes</em></h2></div>
  <div class="grille grille--2">{"".join(f'<div class="encart">{mini_medecin(c["slug"])}</div>' for c in CHIRURGIENS if any("Cancérologie" in s for s, _ in c["specialites"]))}</div>
</div></section>''' + bandeau_rdv()
    return page(assets, "/cancerologie/", "Cancérologie digestive à Nîmes — chirurgie des cancers",
                "Cancers de l'œsophage, de l'estomac, du côlon, du rectum, du foie et du pancréas : chirurgie à Nîmes, dossiers validés en réunion pluridisciplinaire.",
                corps, fil=[("/cancerologie/", "Cancérologie digestive")])


def rendre(assets):
    pages = {"/pathologies/": page_hub(assets), "/cancerologie/": page_cancero(assets)}
    for slug in HUBS:
        pages[f"/pathologies/{slug}/"] = page_famille(assets, slug)
    for p in PATHOLOGIES:
        pages[f"/pathologies/{p['slug']}/"] = page_patho(assets, p)
    return pages
