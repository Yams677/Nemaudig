"""Le cabinet : présentation, engagements, locaux."""

import config
from data.cabinet import EQUIPE_PARAMEDICALE, LOCAUX, PRESENTATION, VALEURS
from lib.composants import bandeau_rdv, tete_page
from lib.html import ICONES, e, surtitre
from lib.layout import page

REDIRECTIONS = {"le-cabinet": "/cabinet/", "nos-engagements": "/cabinet/#engagements"}
ICONES_VALEURS = ["equipe", "lune", "balance", "fichier", "coeur"]


def rendre(assets):
    valeurs = "".join(f'''<article class="carte" data-reveal style="--d:{i}"><span class="carte__ico">{ICONES[ICONES_VALEURS[i]]}</span>
  <h3>{e(t)}</h3><p>{e(d)}</p></article>''' for i, (t, d) in enumerate(VALEURS))
    locaux = "".join(f"<p>{e(x)}</p>" for x in LOCAUX)
    chiffres = "".join(f'<div class="chiffre"><strong>{p["chiffre"]}</strong><span>{e(p["unite"])} · {e(p["titre"].lower())}</span></div>' for p in EQUIPE_PARAMEDICALE)
    corps = tete_page("Le cabinet <em>Nemaudig</em>", e(PRESENTATION[0] + " " + PRESENTATION[2]), "Qui sommes-nous", "var(--menthe)") + f'''
<section class="section section--serree"><div class="conteneur">
  <div class="chiffres" data-reveal><div class="chiffre"><strong>5</strong><span>chirurgiens digestifs et viscéraux</span></div>{chiffres}</div>
</div></section>
<section class="section section--blanc" id="engagements" aria-labelledby="eng"><div class="conteneur">
  <div class="section__tete section__tete--2"><div>{surtitre("Nos engagements", "01")}<h2 id="eng">Ce qui ne change pas, <em>depuis l'internat.</em></h2></div>
  <p class="chapo">Travail en équipe, proximité et disponibilité : les valeurs inculquées pendant notre formation, que nous avons gardées.</p></div>
  <div class="grille grille--3">{valeurs}</div>
</div></section>
<section class="section" aria-labelledby="loc"><div class="conteneur"><div class="grille grille--2" style="align-items:start">
  <div>{surtitre("Les locaux", "02")}<h2 id="loc">Lumineux, accessibles, <em>pensés pour vous accueillir.</em></h2></div>
  <div class="prose">{locaux}
    {'<p class="note-a-valider">Photos des locaux à intégrer (disponibles sur l\'ancien site, à refaire en haute définition).</p>' if config.DEMO else ""}
    <div class="actions mt-6"><a class="btn btn--plein" href="/contact/">{ICONES["lieu"]}<span>Accès et contact</span><span class="btn__fleche" aria-hidden="true">{ICONES["fleche"]}</span></a>
    <a class="lien-fleche" href="/etablissements/">Les établissements {ICONES["fleche"]}</a></div>
  </div>
</div></div></section>''' + bandeau_rdv()
    return {"/cabinet/": page(assets, "/cabinet/", "Le cabinet Nemaudig — chirurgie digestive à Nîmes",
                              "Cabinet de chirurgie digestive près de la Polyclinique du Grand Sud à Nîmes : nos engagements, nos locaux accessibles et l'équipe qui vous accueille.",
                              corps, fil=[("/cabinet/", "Le cabinet")])}
