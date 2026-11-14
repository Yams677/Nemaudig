"""Nos chirurgiens : page d'équipe et cinq fiches. Tout provient de nemaudig.fr."""
import config
from data import obesite
from data.cabinet import EQUIPE_PARAMEDICALE, ETABLISSEMENTS, UZES, VALEURS
from data.chirurgiens import CHIRURGIENS, nom_complet
from data.pathologies import PAR_SLUG
from lib.gabarit import C, bandeau, bouton_rdv, carte_medecin, e, lien_tel, page, portrait, provisoire, sur_titre, u
from pages.accueil import appel_rdv


def _equipe():
    valeurs = "".join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in VALEURS)
    para = "".join(f'''<li><span class="chiffre">{e(x["chiffre"])}</span><h3>{e(x["titre"])}</h3>
      <p class="repere">{e(x["unite"])}</p><p>{e(x["texte"])}</p></li>''' for x in EQUIPE_PARAMEDICALE)
    corps = bandeau("Nos chirurgiens", "Cinq chirurgiens, <em>une équipe</em>.",
                    "Ils se connaissent depuis leur internat. Chacun apporte une compétence, tous partagent la même façon de travailler : ensemble, et au plus près du patient.",
                    [(None, "Chirurgiens")])
    corps += f'''<section class="plan plan--clair bloc"><div class="contenu">
    <div class="medecins medecins--grand">{"".join(carte_medecin(c) for c in CHIRURGIENS)}</div></div></section>
<section class="plan plan--clair bloc bloc--serre" aria-labelledby="engagements-titre"><div class="contenu">
    <div class="bloc__tete">{sur_titre("Nos engagements")}
      <h2 class="titre-l" id="engagements-titre">Ce que vous pouvez attendre de nous.</h2></div>
    <ul class="engagements">{valeurs}</ul></div></section>
<section class="plan plan--nuit bloc" aria-labelledby="para-titre"><div class="contenu">
    <div class="bloc__tete">{sur_titre("Autour des chirurgiens")}
      <h2 class="titre-l" id="para-titre">Une équipe paramédicale dédiée.</h2></div>
    <ul class="soutiens">{para}</ul></div></section>'''
    return ("/chirurgiens/", page(
        chemin="/chirurgiens/", titre="Nos chirurgiens — Nemaudig, Nîmes",
        description="Les cinq chirurgiens digestifs et viscéraux du cabinet Nemaudig à Nîmes : parcours, diplômes, spécialités et prise de rendez-vous.",
        corps=corps + appel_rdv()))


def _lien_domaine(slug):
    if slug in PAR_SLUG:
        return f'<li><a class="puce puce--claire" href="{u("/specialites/" + slug + "/")}">{e(PAR_SLUG[slug]["court"])}</a></li>'
    if slug in obesite.PAR_SLUG:
        return f'<li><a class="puce puce--claire" href="{u("/specialites/obesite/")}">{e(obesite.PAR_SLUG[slug]["court"])}</a></li>'
    return ""


def _fiche(c):
    nom = nom_complet(c)
    specialites = "".join(f'<li><strong>{e(s)}</strong>{f"<span>{e(d)}</span>" if d else ""}</li>' for s, d in c["specialites"])
    formation = "".join(f"<li>{e(x)}</li>" for x in c["formation"])
    diplomes = "".join(f'<li><span>{e(t)}</span>{f"<span class=\"repere\">{e(an)}</span>" if an else ""}</li>' for t, an in c["diplomes"])
    societes = "".join(f"<li>{e(x)}</li>" for x in c["societes"])
    faits = "".join(f"<li>{e(x)}</li>" for x in c["faits"])
    domaines = "".join(_lien_domaine(s) for s in c["pathologies"])
    lieux = [f'<li><strong>Cabinet Nemaudig</strong><span>{e(C["adresse"]["rue"])}, {e(C["adresse"]["ville"])} — consultations</span></li>']
    lieux += [f'<li><strong>{e(x["nom"])}</strong><span>{e(x["role"])}</span></li>' for x in ETABLISSEMENTS]
    if UZES["chirurgien"] == c["slug"]:
        lieux.append(f'<li><strong>{e(UZES["nom"])}</strong><span>Consultation — {e(UZES["creneau"].lower())}, depuis le {e(UZES["depuis"])}</span></li>')
    extra = f'<div class="actions">{bouton_rdv("btn", "Prendre rendez-vous", c["slug"])}{lien_tel(C["telephone_affiche"], "btn btn--fil")}</div>'
    corps = f'''<header class="bandeau bandeau--portrait plan plan--nuit">
  <div class="bandeau__lignes" aria-hidden="true"></div>
  <div class="contenu fiche-medecin__tete">
    <div>
      <nav class="fil" aria-label="Fil d'Ariane"><a href="{u("/")}">Accueil</a><span aria-hidden="true">/</span><a href="{u("/chirurgiens/")}">Chirurgiens</a><span aria-hidden="true">/</span><span aria-current="page">{e(nom)}</span></nav>
      {sur_titre("Chirurgien digestif et viscéral")}
      <h1 class="titre-xl">{e(nom)}</h1>
      <p class="chapo">{e(c["accroche"])}</p>
      {extra}
    </div>
    <div class="fiche-medecin__photo">{portrait(c, 800, 800, 1000)}</div>
  </div>
</header>
<section class="plan plan--clair bloc"><div class="contenu fiche-medecin">
  <div class="fiche-medecin__bloc"><h2 class="repere">Spécialités</h2><ul class="definitions">{specialites}</ul></div>
  <div class="fiche-medecin__bloc"><h2 class="repere">Parcours</h2><ul class="liste">{formation}</ul></div>
  <div class="fiche-medecin__bloc"><h2 class="repere">Diplômes et formations</h2><ul class="diplomes">{diplomes}</ul></div>
  <div class="fiche-medecin__bloc"><h2 class="repere">Sociétés savantes</h2><ul class="liste">{societes}</ul>
    {f'<h2 class="repere">Au cabinet</h2><ul class="liste">{faits}</ul>' if faits else ""}</div>
  <div class="fiche-medecin__bloc"><h2 class="repere">Domaines en lien avec son activité</h2><ul class="puces puces--claires">{domaines}</ul>
    {provisoire("Liens proposés d'après les spécialités affichées — à confirmer par le praticien")}</div>
  <div class="fiche-medecin__bloc"><h2 class="repere">Lieux d'exercice</h2><ul class="definitions">{"".join(lieux)}</ul></div>
</div></section>'''
    json_ld = {"@context": "https://schema.org", "@type": "Physician", "name": nom, "medicalSpecialty": "Surgical",
               "worksFor": {"@type": "MedicalClinic", "name": C["nom_long"]}, "url": f'{config.SITE_URL}/chirurgiens/{c["slug"]}/'}
    return (f'/chirurgiens/{c["slug"]}/', page(
        chemin=f'/chirurgiens/{c["slug"]}/', titre=f"{nom} — chirurgien digestif à Nîmes | Nemaudig",
        description=f"{nom}, chirurgien digestif et viscéral à Nîmes. {c['accroche']} Parcours, diplômes et prise de rendez-vous.",
        corps=corps + appel_rdv(), json_ld=json_ld))


def pages():
    return [_equipe()] + [_fiche(c) for c in CHIRURGIENS]
