"""Comprendre votre parcours de soins : examens prescrits et techniques opératoires."""
from data.cabinet import TECHNIQUES
from data.examens import EXAMENS, REALISE_PAR, RUBRIQUES
from data.organes import PAR_CLE
from lib.gabarit import bandeau, e, liste, page, provisoire, sur_titre, texte_riche, u
from lib.schemas import schema
from pages.accueil import appel_rdv

SCHEMA_DE = {"coloscopie": "colon"}


def _sommaire():
    examens = "".join(f'''<li><a class="carte" href="{u("/parcours-de-soins/" + x["slug"] + "/")}">
      <p class="repere">Examen · {e(x["autre_nom"])}</p><h3>{e(x["titre"])}</h3><p>{e(x["resume"])}</p>
      <span class="lien-fleche" aria-hidden="true">Comprendre l'examen</span></a></li>''' for x in EXAMENS)
    techniques = "".join(f'''<li><a class="carte" href="{u("/parcours-de-soins/" + t["slug"] + "/")}">
      <p class="repere">Technique · {e(t["court"])}</p><h3>{e(t["titre"])}</h3><p>{e(t["accroche"])}</p>
      <span class="lien-fleche" aria-hidden="true">En savoir plus</span></a></li>''' for t in TECHNIQUES)
    corps = bandeau("Parcours de soins", "Comprendre votre <em>parcours de soins</em>.",
                    "Savoir pourquoi un examen est demandé, comment il se passe et ce qui se passe ensuite : c'est déjà moins d'inquiétude.",
                    [(None, "Parcours de soins")])
    corps += f'''<section class="plan plan--clair bloc" aria-labelledby="examens-titre"><div class="contenu">
  <div class="bloc__tete">{sur_titre("Avant une intervention")}
    <h2 class="titre-l" id="examens-titre">Les examens qui peuvent vous être prescrits.</h2>
    <p class="chapo">{e(REALISE_PAR)} Ils ne sont pas réalisés au cabinet : nous les expliquons parce qu'ils jalonnent souvent votre parcours.</p></div>
  <ul class="cartes">{examens}</ul>
  {provisoire("Fiches d'examens rédigées pour la maquette — à valider par l'équipe et les gastro-entérologues correspondants")}
</div></section>
<section class="plan plan--clair bloc bloc--serre" aria-labelledby="techniques-titre"><div class="contenu">
  <div class="bloc__tete">{sur_titre("Au bloc opératoire")}
    <h2 class="titre-l" id="techniques-titre">Les techniques de l'équipe.</h2></div>
  <ul class="cartes cartes--4">{techniques}</ul>
</div></section>'''
    return ("/parcours-de-soins/", page(
        chemin="/parcours-de-soins/", titre="Comprendre votre parcours de soins — Nemaudig, Nîmes",
        description="Gastroscopie, coloscopie, écho-endoscopie, cœlioscopie, chirurgie robotique, ambulatoire : comprendre les examens et les techniques de votre parcours de soins.",
        corps=corps + appel_rdv()))


def _examen(x):
    blocs = []
    for i, (cle, question) in enumerate(RUBRIQUES):
        contenu = liste(x[cle]) if x[cle] else provisoire("Rubrique à compléter avec l'équipe")
        blocs.append(f'<details class="question question--num"{" open" if i == 0 else ""}><summary><span class="repere">{i + 1:02d}</span>{e(question)}</summary>{contenu}</details>')
    faq = ""
    if x["faq"]:
        faq = '<h2 class="titre-m">Questions fréquentes</h2>' + "".join(
            f'<details class="question"><summary>{e(q)}</summary><p>{e(r)}</p></details>' for q, r in x["faq"])
    cle_schema = SCHEMA_DE.get(x["slug"])
    figure = f'<div class="article__figure">{schema(cle_schema)}</div>' if cle_schema else ""
    organes = "".join(f'<li><a class="puce puce--claire" href="{u("/explorer/")}#{o}">{e(PAR_CLE[o]["nom"])}</a></li>' for o in x["organes"])
    corps = bandeau("Examen", e(x["titre"]), x["resume"], [("/parcours-de-soins/", "Parcours de soins"), (None, x["titre"])],
                    f'<p class="bandeau__note repere">{e(REALISE_PAR)}</p>')
    corps += f'''<section class="plan plan--clair bloc"><div class="contenu article article--examen">
  <div class="article__corps">
    {provisoire("Fiche provisoire — durées, anesthésie et consignes à valider avant publication")}
    {figure}
    <div class="questions">{"".join(blocs)}</div>
    {faq}
    <p class="avertissement">Ces informations générales ne remplacent pas les consignes personnelles remises par le médecin qui réalise l'examen. En cas de doute, appelez-le.</p>
  </div>
  <aside class="cote" aria-label="Pour aller plus loin">
    <div class="cote__bloc"><h2 class="repere">Organes concernés</h2><ul class="puces puces--claires">{organes}</ul></div>
    <div class="cote__bloc"><h2 class="repere">Sources d'information</h2>
      <p class="note">Société française d'endoscopie digestive, Assurance Maladie, Institut national du cancer.</p></div>
  </aside>
</div></section>'''
    return (f'/parcours-de-soins/{x["slug"]}/', page(
        chemin=f'/parcours-de-soins/{x["slug"]}/', titre=f'{x["titre"]} : déroulement, préparation, suites — Nemaudig',
        description=f'{x["titre"]} : pourquoi cet examen, comment il se déroule, comment s\'y préparer et ce qui se passe ensuite.',
        corps=corps + appel_rdv(), scripts=("schemas.js",) if cle_schema else ()))


def _technique(t):
    extra = ""
    if t.get("conditions"):
        extra += f'<h2 class="titre-m">Les conditions</h2>{liste(t["conditions"])}'
    if t.get("encart"):
        titre, texte = t["encart"]
        extra += f'<div class="encart encart--large"><h2>{e(titre)}</h2><p>{e(texte)}</p></div>'
    corps = bandeau("Technique opératoire", e(t["titre"]), t["accroche"], [("/parcours-de-soins/", "Parcours de soins"), (None, t["court"])])
    corps += f'''<section class="plan plan--clair bloc"><div class="contenu article article--simple">
  <div class="article__corps prose">{texte_riche(t["texte"])}{extra}
    <p class="avertissement">Votre chirurgien vous indique, en consultation, si cette technique est adaptée à votre situation.</p></div>
</div></section>'''
    return (f'/parcours-de-soins/{t["slug"]}/', page(
        chemin=f'/parcours-de-soins/{t["slug"]}/', titre=f'{t["titre"]} à Nîmes — Nemaudig', description=t["desc"],
        corps=corps + appel_rdv()))


def pages():
    return [_sommaire()] + [_examen(x) for x in EXAMENS] + [_technique(t) for t in TECHNIQUES]
