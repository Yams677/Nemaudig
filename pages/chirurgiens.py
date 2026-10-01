"""Équipe médicale (liste) + une fiche premium par chirurgien."""

import config
from data.cabinet import EQUIPE_PARAMEDICALE, PRESENTATION
from data.chirurgiens import CHIRURGIENS, initiales, nom_complet
from data.pathologies import PAR_SLUG as PATHOS
from data.videos import VIDEOS
from lib import portraits
from lib.composants import TEINTES, bandeau_rdv, carte_medecin, carte_patho, portrait, tete_page, video
from lib.html import ICONES, e, surtitre
from lib.layout import page

REDIRECTIONS = {"l-equipe-medicale": "/chirurgiens/", "qui-sommes-nous": "/chirurgiens/",
                "l-equipe-paramedicale": "/chirurgiens/#equipe-paramedicale"}
REDIRECTIONS.update({c["ancien_slug"]: f"/chirurgiens/{c['slug']}/" for c in CHIRURGIENS})


def page_equipe(assets):
    cartes = "".join(carte_medecin(c, i) for i, c in enumerate(CHIRURGIENS))
    para = "".join(f'''<article class="carte" data-reveal style="--d:{i}">
  <p class="tuile__chiffre" style="color:var(--lagon);font-size:3.4rem">{p["chiffre"]}</p>
  <p class="surtitre mb-0">{e(p["unite"])}</p>
  <h3>{e(p["titre"])}</h3><p>{e(p["texte"])}</p>
</article>''' for i, p in enumerate(EQUIPE_PARAMEDICALE))
    corps = tete_page("Cinq chirurgiens, <em>une seule équipe.</em>", e(PRESENTATION[1]), "L'équipe médicale") + f'''
<section class="section section--serree"><div class="conteneur"><div class="equipe">{cartes}</div>
  <div class="grille grille--2 mt-7"><p class="chapo">{e(PRESENTATION[0])} {e(PRESENTATION[2])}</p>
  <p class="chapo">Nous avons gardé les valeurs de l'internat : travail en équipe, proximité et disponibilité vis-à-vis du patient et de sa famille, discussion des dossiers difficiles, consultation commune pour les cas complexes et suivi commun des patients hospitalisés.</p></div>
</div></section>
<section class="section section--blanc" id="equipe-paramedicale" aria-labelledby="para-titre"><div class="conteneur">
  <div class="section__tete section__tete--2"><div>{surtitre("L'équipe paramédicale")}<h2 id="para-titre">Ceux qui vous accompagnent <em>à chaque étape.</em></h2></div>
  <p class="chapo">Secrétaires, infirmières aides opératoires et infirmière stomathérapeute : une équipe dédiée, disponible comme les chirurgiens 365 jours par an.</p></div>
  <div class="grille grille--3">{para}</div>
</div></section>''' + bandeau_rdv()
    return page(assets, "/chirurgiens/", "Chirurgiens digestifs à Nîmes — l'équipe Nemaudig",
                "Les Drs Alline, Amielh, Laporte, Prieur et Torres, chirurgiens digestifs et viscéraux à Nîmes, et leur équipe : secrétaires, aides opératoires, stomathérapie.",
                corps, fil=[("/chirurgiens/", "Chirurgiens")])


def page_chirurgien(assets, c):
    url = f"/chirurgiens/{c['slug']}/"
    nom = nom_complet(c)
    specs = "".join(f'<div class="spec" data-reveal style="--d:{i}"><strong>{e(s)}</strong>{f"<span>{e(d)}</span>" if d else ""}</div>'
                    for i, (s, d) in enumerate(c["specialites"]))
    formation = "".join(f'<li><span class="chrono__an" aria-hidden="true">{ICONES["diplome"]}</span><span class="chrono__txt">{e(f)}</span></li>' for f in c["formation"])
    diplomes = "".join(f'<li><span class="chrono__an">{e(an) if an else "—"}</span><span class="chrono__txt">{e(t)}</span></li>' for t, an in c["diplomes"])
    societes = "".join(f"<li>{e(s)}</li>" for s in c["societes"])
    faits = "".join(f'<div class="fait">{ICONES["check"]}<p>{e(f)}</p></div>' for f in c["faits"])
    vids = "".join(f"<div>{video(v)}</div>" for v in c["videos"])
    pathos = "".join(carte_patho(PATHOS[p]) for p in c["pathologies"] if p in PATHOS)
    obesite = ""
    if c["slug"] == "dr-fanelly-torres":
        obesite = f'<p class="mt-6"><a class="lien-fleche" href="/obesite/">Le parcours de chirurgie de l\'obésité {ICONES["fleche"]}</a></p>'
    autres = "".join(f'<li><a href="/chirurgiens/{o["slug"]}/"><span>{e(nom_complet(o))}</span>{ICONES["fleche"]}</a></li>' for o in CHIRURGIENS if o is not c)
    note = '<span class="medecin__note">Portrait à venir</span>' if config.DEMO else ""
    elle = c["genre"] == "f"

    corps = f'''<section class="section section--serree" style="padding-top:32px">
  <div class="conteneur profil">
    <div class="profil__portrait" style="--teinte:{TEINTES[c["slug"]]}">{portrait(c, "(min-width: 900px) 380px, 100vw", charge="eager")}</div>
    <div>
      {surtitre(("Chirurgienne digestive et viscérale" if elle else "Chirurgien digestif et viscéral") + " · Nîmes")}
      <h1>{e(nom)}</h1>
      <p class="chapo">{e(c["accroche"])}</p>
      <div class="actions mt-6">
        <a class="btn btn--plein" href="/contact/">{ICONES["agenda"]}<span>Prendre rendez-vous</span><span class="btn__fleche" aria-hidden="true">{ICONES["fleche"]}</span></a>
        {'<a class="btn btn--ligne" href="/consultation-uzes/"><span>Consulter à Uzès</span><span class="btn__fleche" aria-hidden="true">' + ICONES["fleche"] + '</span></a>' if c["slug"] == "dr-david-amielh" else ""}
      </div>

      <h2 class="mt-7" style="font-size:1.9rem">Spécialités</h2>
      <div class="specs">{specs}</div>

      {f'<h2 class="mt-7" style="font-size:1.9rem">À la une</h2><div class="faits">{faits}</div>' if faits else ""}

      <h2 class="mt-7" style="font-size:1.9rem">Formation</h2>
      <ul class="chrono">{formation}</ul>

      <h2 class="mt-7" style="font-size:1.9rem">Diplômes</h2>
      <ul class="chrono">{diplomes}</ul>

      <h2 class="mt-7" style="font-size:1.9rem">Sociétés savantes</h2>
      <ul class="liste">{societes}</ul>
    </div>
  </div>
</section>
{f"""<section class="section section--blanc" aria-labelledby="v-titre"><div class="conteneur">
  <div class="section__tete">{surtitre("Au bloc opératoire")}<h2 id="v-titre">Les interventions filmées <em>du {e(nom)}</em></h2></div>
  <div class="grille grille--3">{vids}</div></div></section>""" if vids else ""}
<section class="section" aria-labelledby="p-titre"><div class="conteneur">
  <div class="section__tete section__tete--2"><div>{surtitre("Pathologies")}<h2 id="p-titre">En lien avec <em>ses spécialités</em></h2></div>
  <p class="chapo">Ces fiches sont rédigées par l'équipe ; elles expliquent l'intervention, ses risques et la vie après l'opération.</p></div>
  <div class="liste-pathos">{pathos}</div>{obesite}
</div></section>
<section class="section section--serree"><div class="conteneur"><div class="encart" style="max-width:520px"><h2>Les autres chirurgiens de l'équipe</h2><ul class="encart__liste">{autres}</ul></div></div></section>
''' + bandeau_rdv(f"Prendre rendez-vous avec le {nom}")

    schema = {"@context": "https://schema.org", "@type": "Physician", "name": nom, "url": f"{config.SITE_URL}{url}",
              "medicalSpecialty": "Surgical", "knowsAbout": [s for s, _ in c["specialites"]],
              "memberOf": [{"@type": "MedicalOrganization", "name": s} for s in c["societes"]],
              "worksFor": {"@id": f"{config.SITE_URL}/#cabinet"},
              "address": {"@type": "PostalAddress", "streetAddress": "480 avenue Saint-André de Codols", "postalCode": "30900", "addressLocality": "Nîmes", "addressCountry": "FR"},
              "telephone": config.CABINET["telephone_e164"]}
    if portraits.source(c["slug"]):
        schema["image"] = f"{config.SITE_URL}{portraits.url(c['slug'], 800, 'jpg')}"
    specs_txt = ", ".join(s.lower() for s, _ in c["specialites"][:3])
    desc = f"{nom}, {'chirurgienne digestive' if elle else 'chirurgien digestif'} à Nîmes (Nemaudig) : {specs_txt}. Formation, diplômes, vidéos et rendez-vous."
    return page(assets, url, f"{nom} — {'chirurgienne digestive' if elle else 'chirurgien digestif'} à Nîmes", desc[:170], corps,
                fil=[("/chirurgiens/", "Chirurgiens"), (url, nom)], schemas=[schema])


def rendre(assets):
    pages = {"/chirurgiens/": page_equipe(assets)}
    for c in CHIRURGIENS:
        pages[f"/chirurgiens/{c['slug']}/"] = page_chirurgien(assets, c)
    return pages
