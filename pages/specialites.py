"""Nos spécialités : huit domaines, 24 fiches de pathologies et la page obésité (contenus du site actuel)."""
from data import obesite
from data.chirurgiens import nom_complet
from data.organes import PAR_CLE
from data.pathologies import FAM, FAMILLES, PATHOLOGIES
from lib import liens
from lib.gabarit import bandeau, bouton_rdv, e, page, portrait, provisoire, sur_titre, texte_riche, u
from pages.accueil import appel_rdv


def _vignette_chirurgien(c):
    return f'''<li><a class="praticien" href="{u("/chirurgiens/" + c["slug"] + "/")}">{portrait(c, 400, 64, 80)}
      <span><strong>{e(nom_complet(c))}</strong><small>{e(c["accroche"])}</small></span></a></li>'''


def _sommaire():
    blocs = []
    for i, f in enumerate(FAMILLES):
        if f["slug"] == "obesite":
            items = "".join(f'<li><a href="{u("/specialites/obesite/")}#{t["slug"]}"><span>{e(t["court"])}</span><small>{e(t["type"])}</small></a></li>'
                            for t in obesite.TECHNIQUES)
            plus = f'<a class="lien-fleche" href="{u("/specialites/obesite/")}">Le parcours obésité</a>'
        else:
            items = "".join(f'<li><a href="{u(liens.adresse_pathologie(p["slug"]))}"><span>{e(p["court"])}</span><small>{e(p["resume"])}</small></a></li>'
                            for p in liens.PATHOLOGIES_PAR_FAMILLE[f["slug"]])
            plus = ""
        blocs.append(f'''<section class="famille" id="{f["slug"]}" aria-labelledby="fam-{f["slug"]}">
      <div class="famille__tete"><p class="repere">{i + 1:02d} / {len(FAMILLES):02d}</p>
        <h2 class="titre-m" id="fam-{f["slug"]}">{e(f["titre"])}</h2><p>{e(f["intro"])}</p>{plus}</div>
      <ul class="famille__fiches">{items}</ul></section>''')
    corps = bandeau("Nos spécialités", "Tout l'appareil digestif, <em>domaine par domaine</em>.",
                    "Chaque fiche explique la maladie, l'intervention, ses risques et ses suites. Une information claire et loyale, rédigée par l'équipe.",
                    [(None, "Spécialités")])
    corps += f'<section class="plan plan--clair bloc"><div class="contenu familles">{"".join(blocs)}</div></section>'
    return ("/specialites/", page(
        chemin="/specialites/", titre="Nos spécialités en chirurgie digestive — Nemaudig, Nîmes",
        description="Œsophage et estomac, foie, vésicule et pancréas, côlon et rectum, proctologie, paroi abdominale, obésité : les domaines de prise en charge du cabinet Nemaudig.",
        corps=corps + appel_rdv()))


def _fiche(p):
    f = FAM[p["famille"]]
    organe = liens.organe_de(p)
    sections = "".join(f'<section class="article__section" id="s{i}"><h2>{e(t)}</h2>{texte_riche(c)}</section>'
                       for i, (t, c) in enumerate(p["sections"]))
    sommaire = "".join(f'<li><a href="#s{i}">{e(t)}</a></li>' for i, (t, _) in enumerate(p["sections"]))
    faq = ""
    if p["faq"]:
        qr = "".join(f'<details class="question"><summary>{e(q)}</summary><p>{e(r)}</p></details>' for q, r in p["faq"])
        faq = f'<section class="article__section" id="faq"><h2>Questions fréquentes</h2>{qr}</section>'
        sommaire += '<li><a href="#faq">Questions fréquentes</a></li>'
    praticiens = liens.chirurgiens_de_la_pathologie(p["slug"])
    bloc_praticiens = ""
    if praticiens:
        bloc_praticiens = f'''<div class="cote__bloc"><h2 class="repere">Dans l'équipe</h2>
      <ul class="praticiens">{"".join(_vignette_chirurgien(c) for c in praticiens)}</ul>
      {provisoire("Proposé d'après les spécialités affichées")}</div>'''
    bloc_organe = ""
    if organe:
        bloc_organe = f'''<div class="cote__bloc"><h2 class="repere">Situer l'organe</h2>
      <a class="lien-fleche" href="{u("/explorer/")}#{organe}">{e(PAR_CLE[organe]["nom"])}, en images</a></div>'''
    bloc_pdf = ""
    if p["pdf"]:
        bloc_pdf = f'''<div class="cote__bloc"><h2 class="repere">Fiche à télécharger</h2>
      <a class="lien-fleche" href="{e(p["pdf"])}" rel="noopener" target="_blank">Fiche d'information (PDF)<span class="visuellement-cache"> — nouvel onglet</span></a></div>'''
    corps = bandeau(f["titre"], e(p["titre"]), p["resume"], [("/specialites/", "Spécialités"), (None, p["court"])])
    corps += f'''<section class="plan plan--clair bloc"><div class="contenu article">
  <nav class="article__sommaire" aria-label="Sommaire de la fiche"><p class="repere">Dans cette fiche</p><ol>{sommaire}</ol></nav>
  <div class="article__corps prose">{sections}{faq}
    <p class="avertissement">Cette fiche vous informe ; elle ne remplace pas la consultation, au cours de laquelle votre chirurgien vous explique ce qui vous concerne personnellement.</p></div>
  <aside class="cote" aria-label="Pour aller plus loin">{bloc_praticiens}{bloc_organe}{bloc_pdf}
    <div class="cote__bloc">{bouton_rdv("btn btn--bloc")}</div></aside>
</div></section>'''
    return (liens.adresse_pathologie(p["slug"]), page(
        chemin=liens.adresse_pathologie(p["slug"]), titre=f'{p["titre"]} — Nemaudig, chirurgie digestive à Nîmes',
        description=p["desc"], corps=corps + appel_rdv()))


def _obesite():
    techniques = "".join(f'''<li class="technique" id="{t["slug"]}"><p class="repere">{e(t["type"])}</p>
      <h3>{e(t["titre"])}</h3><p>{e(t["resume"])}</p></li>''' for t in obesite.TECHNIQUES)
    preparation = "".join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in obesite.PREPARATION)
    decision = "".join(f"<li>{e(x)}</li>" for x in obesite.DECISION)
    praticiens = "".join(_vignette_chirurgien(c) for c in liens.chirurgiens_de_la_famille("obesite"))
    corps = bandeau("Obésité", "Chirurgie de l'obésité : <em>un parcours</em>, pas seulement une opération.",
                    obesite.DEFINITION, [("/specialites/", "Spécialités"), (None, "Obésité")])
    corps += f'''<section class="plan plan--clair bloc"><div class="contenu">
  <div class="deux-colonnes"><div>{sur_titre("Pour qui ?")}<h2 class="titre-l">Une décision pluridisciplinaire.</h2></div>
    <div class="prose"><p class="chapo">{e(obesite.CANDIDAT)}</p><ul class="liste">{decision}</ul></div></div>
</div></section>
<section class="plan plan--clair bloc bloc--serre"><div class="contenu">
  <div class="bloc__tete">{sur_titre("Les techniques")}<h2 class="titre-l">Quatre réponses possibles.</h2></div>
  <ul class="techniques">{techniques}</ul></div></section>
<section class="plan plan--clair bloc bloc--serre"><div class="contenu">
  <div class="bloc__tete">{sur_titre("La préparation")}<h2 class="titre-l">Une équipe autour de vous.</h2></div>
  <ul class="engagements">{preparation}</ul>
  <div class="cote__bloc cote__bloc--large"><h2 class="repere">Dans l'équipe</h2><ul class="praticiens">{praticiens}</ul></div>
</div></section>'''
    return ("/specialites/obesite/", page(
        chemin="/specialites/obesite/", titre="Chirurgie de l'obésité à Nîmes — Nemaudig",
        description="Ballon intragastrique, sleeve, bypass, anneau : le parcours pluridisciplinaire de chirurgie de l'obésité du cabinet Nemaudig à Nîmes.",
        corps=corps + appel_rdv()))


def pages():
    return [_sommaire(), _obesite()] + [_fiche(p) for p in PATHOLOGIES]
