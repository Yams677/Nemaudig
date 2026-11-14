"""Explorez votre système digestif : un organe à la fois, une image et une fiche.

Les fiches sont écrites dans la page (lisibles sans JavaScript) ; le script n'en montre
qu'une à la fois, avec l'image de l'organe.
"""
from data.chirurgiens import PAR_SLUG as CHIRURGIEN, nom_complet
from data.examens import PAR_SLUG as EXAMEN
from data.organes import ORGANES
from data.pathologies import FAM, PAR_SLUG as PATHOLOGIE
from lib.gabarit import bouton_rdv, e, fil, image_organe, liste, page, portrait, provisoire, sur_titre, u
from lib.schemas import schema
from pages.accueil import appel_rdv


def _praticiens(o):
    if not o["chirurgiens"]:
        return f'''<div class="praticien praticien--equipe"><span><strong>Toute l'équipe</strong>
      <small>Vous êtes orienté vers le chirurgien le plus à même de vous prendre en charge.</small></span>{bouton_rdv("lien-fleche", "Rendez-vous")}</div>'''
    items = []
    for slug, specialite in o["chirurgiens"]:
        c = CHIRURGIEN[slug]
        items.append(f'''<div class="praticien">{portrait(c, 400, 64, 80)}
      <span><a href="{u("/chirurgiens/" + slug + "/")}"><strong>{e(nom_complet(c))}</strong></a><small>{e(specialite)}</small></span>
      {bouton_rdv("lien-fleche", "Rendez-vous", slug)}</div>''')
    return "".join(items)


def _fiche(o):
    pathologies = "".join(f'<li><a class="puce puce--claire" href="{u("/specialites/" + s + "/")}">{e(PATHOLOGIE[s]["court"])}</a></li>'
                          for s in o["pathologies"])
    pathologies += "".join(f'<li><a class="puce puce--claire" href="{u("/specialites/" + f + "/")}">{e(FAM[f]["titre"])}</a></li>'
                           for f in o.get("familles", []))
    examens = "".join(
        f'<li><strong>{f"<a href=\"{u("/parcours-de-soins/" + lien + "/")}\">{e(nom)}</a>" if lien in EXAMEN else e(nom)}</strong><span>{e(texte)}</span></li>'
        for nom, texte, lien in o["examens"])
    maladies = ""
    if o.get("maladies"):
        lignes = "".join(f"<li><strong>{e(n)}</strong><span>{e(t)}</span></li>" for n, t in o["maladies"])
        maladies = f'''<section class="organe__section"><h3>Les principales maladies du foie</h3>
      <ul class="definitions">{lignes}</ul><p class="note">{e(o["maladies_note"])}</p></section>'''
    encarts = ""
    if o.get("encarts"):
        encarts = '<section class="organe__section"><h3>À savoir</h3><div class="encarts">' + "".join(
            f'<div class="encart"><h4>{e(t)}</h4><p>{e(x)}</p></div>' for t, x in o["encarts"]) + "</div></section>"
    anim = f'<section class="organe__section"><h3>En mouvement</h3>{schema(o["schema"])}</section>' if o["schema"] else ""
    return f'''<article class="organe" id="{o["cle"]}" data-organe="{o["cle"]}" aria-labelledby="organe-{o["cle"]}">
  <header class="organe__tete"><p class="repere">{e(o["latin"])} · {e(o["fma"])}</p>
    <h2 class="titre-l" id="organe-{o["cle"]}" tabindex="-1">{e(o["nom"])}</h2>
    <p class="chapo">{e(o["accroche"])}</p></header>
  <section class="organe__section"><h3>Son rôle</h3><p>{e(o["role"])}</p></section>
  <section class="organe__section"><h3>Comment il fonctionne</h3>{liste(o["fonctionnement"])}</section>
  {anim}{maladies}{encarts}
  <section class="organe__section"><h3>Les signes qui peuvent amener à consulter</h3>{liste(o["signes"])}
    <p class="note">Ces signes ne permettent pas de poser un diagnostic : parlez-en à votre médecin traitant.</p></section>
  <section class="organe__section"><h3>Les examens possibles</h3><ul class="definitions">{examens}</ul></section>
  <section class="organe__section"><h3>Les traitements, en général</h3>{liste(o["traitements"])}</section>
  <section class="organe__section"><h3>Pris en charge par l'équipe</h3><ul class="puces puces--claires">{pathologies}</ul></section>
  <section class="organe__section"><h3>Votre interlocuteur</h3>{_praticiens(o)}
    {provisoire("Information générale et attribution proposée — à valider par l'équipe")}</section>
</article>'''


def pages():
    onglets = "".join(f'<li><a class="onglet" href="#{o["cle"]}" data-choix="{o["cle"]}"><span class="repere">{i + 1:02d}</span>{e(o["nom"])}</a></li>'
                      for i, o in enumerate(ORGANES))
    corps = f'''<section class="explorateur plan plan--clair" data-explorateur>
  <div class="explorateur__scene" style="--teinte: var(--{ORGANES[0]["teinte"]})">
    {"".join(f'<figure class="explorateur__image" data-image="{o["cle"]}">{image_organe(o, 1024)}</figure>' for o in ORGANES)}
    <p class="explorateur__mention repere"><span aria-hidden="true">◇</span> Illustration générée par IA, à valider</p>
  </div>
  <div class="explorateur__colonne">
    <header class="explorateur__tete">
      {fil([(None, "Explorer")])}
      {sur_titre("Anatomie interactive")}
      <h1 class="titre-xl">Explorez votre <em>système digestif</em>.</h1>
      <p class="chapo">Un organe à la fois : son rôle, ses signes d'alerte, les examens et les traitements.</p>
    </header>
    <nav class="explorateur__organes" aria-label="Organes"><ol class="onglets">{onglets}</ol></nav>
    <div class="organes">
      {"".join(_fiche(o) for o in ORGANES)}</div>
  </div>
</section>'''
    donnees = {"ordre": [o["cle"] for o in ORGANES], "noms": {o["cle"]: o["nom"] for o in ORGANES},
               "teintes": {o["cle"]: o["teinte"] for o in ORGANES}}
    return [("/explorer/", page(
        chemin="/explorer/", titre="Explorez votre système digestif, organe par organe — Nemaudig",
        description="Œsophage, estomac, foie, vésicule, pancréas, intestin grêle, côlon, rectum : une fiche illustrée par organe pour comprendre son rôle, ses maladies et ses traitements.",
        corps=corps + appel_rdv(), scripts=("explorateur.js", "schemas.js"), classe="page-explorer", donnees=donnees))]
