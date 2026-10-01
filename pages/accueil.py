"""Page d'accueil — la vitrine du projet."""

from datetime import date
from pathlib import Path

import config
from data.cabinet import ACTUALITES, ETABLISSEMENTS, PARCOURS, UZES
from data.chirurgiens import CHIRURGIENS
from data.pathologies import FAMILLES, PAR_SLUG as PATHOS, par_famille
from data.film import calendrier, chapitres, etapes_film
from data.voyage import ETAPES
from lib.anatomie import donnees_3d, planche
from lib.composants import bandeau_rdv, carte_medecin, faq, schema_faq, video
from lib.html import C, ICONES, bouton, e, surtitre, tel_href
from lib.layout import page

TITRE = "Chirurgien digestif et viscéral à Nîmes — Nemaudig"
DESC = ("Cinq chirurgiens digestifs et viscéraux à Nîmes : cancers, hernies, vésicule, côlon, proctologie, obésité. "
        "Robot Da Vinci, cœlioscopie 3D, soins 365 j/an.")

CONFIANCE = [
    ("equipe", "Cinq chirurgiens formés en CHU"),
    ("pulse", "Continuité des soins 365 jours et nuits par an"),
    ("robot", "Robot chirurgical Da Vinci"),
    ("camera", "Cœlioscopie 3D haute définition 4K"),
    ("bouclier", "Réhabilitation améliorée reconnue par GRACE"),
    ("balance", "Concertation pluridisciplinaire en cancérologie"),
    ("maison", "Chirurgie ambulatoire"),
    ("lieu", "Consultations à Nîmes et à Uzès"),
    ("diplome", "Membres de la FCVD"),
]

FAMILLES_ACCUEIL = [
    ("oesophage-estomac", "var(--lilas)"),
    ("foie-vesicule-pancreas", "var(--peche)"),
    ("colon-rectum", "var(--menthe)"),
    ("proctologie", "var(--rose)"),
    ("paroi-abdominale", "var(--ciel)"),
    ("obesite", "var(--sable)"),
]

FAQ_ACCUEIL = [
    PATHOS["vesicule-biliaire"]["faq"][1],
    PATHOS["hernie-inguinale"]["faq"][0],
    PATHOS["chirurgie-colique"]["faq"][0],
    PATHOS["kyste-pilonidal"]["faq"][0],
]

BRAS_ROBOT = '''<svg class="bras" viewBox="0 0 300 260" aria-hidden="true">
  <path class="bras__plein" d="M40 250h120v-18a14 14 0 0 0-14-14H54a14 14 0 0 0-14 14Z"/>
  <path d="M100 218V150"/><circle cx="100" cy="140" r="12" class="bras__plein"/>
  <path d="M108 132 190 74"/><circle cx="198" cy="68" r="10" class="bras__plein"/>
  <path d="M206 72 248 120"/><circle cx="252" cy="126" r="6" class="bras__plein"/>
  <path d="M255 132 262 168M262 168l-6 10M262 168l8 8"/>
  <path d="M92 150c-12 4-20-6-16-16M120 120c10-10 26-6 26 8" opacity=".5"/>
  <path d="M30 250h260" opacity=".35"/>
</svg>'''


def hero():
    preuves = [("5", "chirurgiens digestifs et viscéraux"), ("365", "jours et nuits de continuité des soins"),
               ("2", "établissements privés à Nîmes"), ("3D", "cœlioscopie haute définition 4K")]
    return f'''<section class="hero" aria-labelledby="hero-titre">
  <div class="hero__fond" aria-hidden="true"><div class="hero__grille"></div></div>
  <div class="conteneur hero__inner">
    <div>
      {surtitre("Association de chirurgiens digestifs · Nîmes")}
      <h1 id="hero-titre"><span class="ligne">Chirurgie digestive</span><span class="ligne">et viscérale à Nîmes,</span><span class="ligne"><em>cinq experts, une équipe.</em></span></h1>
      <p class="hero__chapo">Cancers digestifs, hernies, vésicule, côlon, proctologie, obésité : cinq chirurgiens formés en CHU vous opèrent à la Polyclinique du Grand Sud et à l'Hôpital privé des Franciscaines — et se relaient auprès de vous, 365 jours et nuits par an.</p>
      <div class="actions">
        {bouton("/contact/", "Prendre rendez-vous", "plein", icone="agenda")}
        {bouton("#explorer", "Explorer les pathologies", "ligne")}
      </div>
      <div class="hero__preuves">{"".join(f'<p class="preuve"><strong data-compteur="{v if v.isdigit() else ""}">{v}</strong><span>{l}</span></p>' for v, l in preuves)}</div>
    </div>
    <div class="hero__visuel" data-planche-zone data-planche-3d="planche">
      <div class="hero__halo" aria-hidden="true"></div>
      <svg class="hero__anneaux" viewBox="0 0 400 600" aria-hidden="true"><circle cx="200" cy="300" r="230"/><circle cx="200" cy="300" r="270"/></svg>
      {planche(interactif=True, ident="planche-hero", titre="Appareil digestif — choisissez un organe pour voir les pathologies prises en charge")}
      <span class="hero__legende" data-legende aria-hidden="true"></span>
      <a class="puce-flottante puce-flottante--1" href="/techniques/chirurgie-robotique/"><span class="puce-flottante__ico">{ICONES["robot"]}</span><span><strong>Robot Da Vinci</strong><span>Maîtrisé par toute l'équipe</span></span></a>
      <a class="puce-flottante puce-flottante--2" href="/techniques/coelioscopie/"><span class="puce-flottante__ico">{ICONES["camera"]}</span><span><strong>Cœlioscopie 3D 4K</strong><span>Aux Franciscaines</span></span></a>
      <a class="puce-flottante puce-flottante--3" href="/techniques/rehabilitation-amelioree/"><span class="puce-flottante__ico">{ICONES["bouclier"]}</span><span><strong>Réhabilitation améliorée</strong><span>Reconnue par GRACE</span></span></a>
    </div>
  </div>
</section>'''


def confiance():
    items = "".join(f'<li class="confiance__item">{ICONES[i]}<span>{e(t)}</span></li>' for i, t in CONFIANCE)
    doublon = items.replace('class="confiance__item"', 'class="confiance__item" aria-hidden="true"')
    return f'<section class="confiance" aria-label="Nos engagements en bref"><ul class="confiance__piste" style="list-style:none;margin:0">{items}{doublon}</ul></section>'


VIDEO = Path(__file__).resolve().parent.parent / "src" / "video"


def film_present():
    return (VIDEO / "parcours-digestif.mp4").exists()


def _mmss(s):
    return f"{int(s) // 60:02d}:{int(s) % 60:02d}"


def _liste_chapitres(court):
    return "".join(f'''<li><button type="button" data-t="{t}"><span>{_mmss(t)}</span>{e(nom)}</button>
<a href="{lien}" aria-label="Fiche : {e(nom)}">Voir la fiche {ICONES["fleche"]}</a></li>''' for t, nom, lien in chapitres(court))


def lecteur_film():
    """Lecteur en surimpression : film complet 16:9 sur ordinateur, version courte verticale sur mobile."""
    duree = round(calendrier(len(etapes_film()), False)[1])
    return f'''<dialog class="film" data-film aria-labelledby="film-titre">
  <div class="film__inner">
    <div class="film__tete"><div>{surtitre("Film · " + str(duree) + " s")}<h3 id="film-titre">Le parcours digestif</h3></div>
      <button type="button" class="film__fermer" data-film-fermer aria-label="Fermer le film">{ICONES["croix"]}</button></div>
    <div class="film__ecran"><video controls playsinline preload="none" data-film-video
      data-large="/video/parcours-digestif" data-haut="/video/parcours-digestif-vertical"
      poster="/video/parcours-digestif.jpg" aria-describedby="film-note"></video></div>
    <div class="film__chapitres">
      <p class="film__chap-titre">Chapitres</p>
      <ol data-chapitres="large">{_liste_chapitres(False)}</ol>
      <ol data-chapitres="haut" hidden>{_liste_chapitres(True)}</ol>
    </div>
    <p class="petit mb-0" id="film-note">Illustration animée réalisée à partir de la 3D du site, sans son — les titres sont incrustés. Elle ne remplace pas une consultation.</p>
  </div>
</dialog>'''


def schema_film():
    duree = round(calendrier(len(etapes_film()), False)[1])
    return {"@context": "https://schema.org", "@type": "VideoObject", "name": "Le parcours digestif — Nemaudig",
            "description": "Illustration animée en 3D de l'appareil digestif : œsophage, estomac, foie, pancréas, intestin, côlon, rectum et paroi abdominale, avec les pathologies prises en charge par les chirurgiens de Nemaudig à Nîmes.",
            "thumbnailUrl": f"{config.SITE_URL}/video/parcours-digestif.jpg", "contentUrl": f"{config.SITE_URL}/video/parcours-digestif.mp4",
            "uploadDate": date.today().isoformat(), "duration": f"PT{duree // 60}M{duree % 60}S", "inLanguage": "fr-FR"}


def voyage():
    rail = "".join(f'<li><a href="#voyage-{x["cle"]}" data-rail="{i}"><span>{i:02d}</span>{e(x["nom"])}</a></li>'
                   for i, x in enumerate(ETAPES) if x["organes"])
    etapes = []
    for i, x in enumerate(ETAPES):
        cam = ",".join(str(v) for v in x["camera"]) if x["camera"] else ""
        faits = "".join(f'<li>{e(f)}</li>' for f in x["faits"])
        liens = "".join(f'<a class="pastille pastille--sombre" href="{u}">{e(l)} {ICONES["fleche"]}</a>' for l, u in x["liens"])
        if i == 0:
            tete = (f'{surtitre("Voyage en 3D")}<h2 id="voyage-titre">Au cœur <em>de l’appareil digestif.</em></h2>'
                    f'<p>{e(x["texte"])}</p><p class="voyage__indice">{ICONES["fleche"]} Faites défiler pour suivre le trajet</p>'
                    + (f'<p class="mt-6"><button type="button" class="btn btn--clair voyage__film-btn" data-film-ouvrir>{ICONES["lecture"]}<span>Regarder le film</span></button></p>' if film_present() else ""))
        else:
            tete = (f'<p class="voyage__num">{i:02d} — {e(x["nom"])}</p><h3>{e(x["titre"])}</h3><p>{e(x["texte"])}</p>'
                    + (f'<ul class="voyage__faits">{faits}</ul>' if faits else ""))
        etapes.append(f'''<article class="voyage__etape{' voyage__etape--intro' if i == 0 else ''}" id="voyage-{x["cle"]}" data-etape-voyage="{i}" data-organes="{" ".join(x["organes"])}" data-camera="{cam}" data-ecarter="{" ".join(x.get("ecarter", []))}">
  <div class="voyage__carte">{tete}{f'<div class="voyage__liens">{liens}</div>' if liens else ""}</div>
</article>''')
    return f'''<section class="voyage" data-voyage aria-labelledby="voyage-titre">
  <div class="voyage__scene" data-planche-zone data-planche-3d="voyage">
    {planche(ident="planche-voyage", titre="Schéma de l'appareil digestif — organe présenté")}
    <nav class="voyage__rail" aria-label="Étapes du voyage"><ol>{rail}</ol></nav>
  </div>
  <div class="voyage__etapes">{"".join(etapes)}</div>
  {lecteur_film() if film_present() else ""}
</section>'''


def explorer():
    cartes = []
    for i, (slug, teinte) in enumerate(FAMILLES_ACCUEIL):
        f = next(x for x in FAMILLES if x["slug"] == slug)
        lien = "/obesite/" if slug == "obesite" else f"/pathologies/{slug}/"
        if slug == "obesite":
            noms = ["Ballon Allurion", "Sleeve", "Bypass", "Anneau"]
        else:
            noms = [p["court"] for p in par_famille(slug)]
        puces = "".join(f"<span>{e(n)}</span>" for n in noms[:5])
        cartes.append(f'''<a class="famille" href="{lien}" style="--fond:{teinte};--d:{i}" data-organe-survol="{f["organe"] if slug != "paroi-abdominale" else "paroi"}" data-reveal>
  <span class="famille__num">{i + 1:02d}</span><h3>{e(f["titre"])}</h3><p>{e(f["intro"])}</p><div class="famille__liens">{puces}</div>
</a>''')
    cartes.append(f'''<a class="famille famille--large" href="/cancerologie/" data-organe-survol="colon-rectum" data-reveal>
  <div><span class="famille__num">Cancérologie digestive</span><h3>Tous les cancers du tube digestif, du foie et du pancréas</h3>
  <p>Chaque dossier est présenté et validé en réunion de concertation pluridisciplinaire.</p></div>
  <span class="btn btn--clair">Découvrir la prise en charge<span class="btn__fleche" aria-hidden="true">{ICONES["fleche"]}</span></span>
</a>''')
    return f'''<section class="section" id="explorer" aria-labelledby="explorer-titre">
  <div class="conteneur">
    <div class="section__tete section__tete--2">
      <div>{surtitre("Pathologies et interventions", "01")}<h2 id="explorer-titre">De l'œsophage au rectum, <em>chaque organe a son expert.</em></h2></div>
      <p class="chapo">Survolez la planche ou choisissez une famille : vous trouverez, pour chaque pathologie, l'intervention, ses risques et la vie après l'opération — expliqués par l'équipe.</p>
    </div>
    <div class="explorer">
      <div class="explorer__planche" data-planche-zone data-planche-3d="planche">{planche(interactif=True, ident="planche-explorer", titre="Planche interactive de l'appareil digestif")}<span class="hero__legende" data-legende aria-hidden="true"></span></div>
      <div class="familles">{"".join(cartes)}</div>
    </div>
  </div>
</section>'''


def equipe():
    cartes = "".join(carte_medecin(c, i) for i, c in enumerate(CHIRURGIENS))
    return f'''<section class="section section--blanc" aria-labelledby="equipe-titre">
  <div class="conteneur">
    <div class="section__tete section__tete--2">
      <div>{surtitre("L'équipe médicale", "02")}<h2 id="equipe-titre">Une même génération, <em>formée en CHU.</em></h2></div>
      <div><p class="chapo">Nous nous connaissons depuis l'internat. Nous en avons gardé le travail en équipe : dossiers difficiles discutés ensemble, consultation commune pour les cas complexes, interventions lourdes à plusieurs chirurgiens.</p>
      <p class="mt-4"><a class="lien-fleche" href="/chirurgiens/">Toute l'équipe médicale et paramédicale {ICONES["fleche"]}</a></p></div>
    </div>
    <div class="equipe">{cartes}</div>
  </div>
</section>'''


def technologies():
    return f'''<section class="section section--nuit" aria-labelledby="techno-titre">
  <div class="conteneur">
    <div class="section__tete section__tete--2">
      <div>{surtitre("Techniques opératoires", "03")}<h2 id="techno-titre">La technologie <em>au service du geste.</em></h2></div>
      <p class="chapo" style="color:#AFC1CB">Moins de cicatrices, moins de douleurs, une récupération plus rapide : l'équipe s'appuie sur des techniques mini-invasives de pointe, dans les deux établissements privés de Nîmes.</p>
    </div>
    <div class="techno">
      <a class="tuile tuile--robot" href="/techniques/chirurgie-robotique/" data-reveal>
        <span class="tuile__ico">{ICONES["robot"]}</span>
        <h3>Chirurgie robot-assistée Da Vinci</h3>
        <p style="max-width:34ch">Un robot chirurgical piloté par votre chirurgien, proposé pour certaines opérations. Les cinq chirurgiens de l'équipe pratiquent la chirurgie robotique.</p>
        <span class="tuile__pied">Voir le robot en vidéo {ICONES["fleche"]}</span>
        {BRAS_ROBOT}
      </a>
      <a class="tuile" href="/techniques/coelioscopie/" data-reveal style="--d:1">
        <span class="tuile__chiffre">4K<small>3D</small></span>
        <h3>Cœlioscopie 3D</h3>
        <p>Depuis mars 2025 aux Franciscaines : les organes vus en relief, comme à l'œil nu.</p>
        <span class="tuile__pied">En savoir plus {ICONES["fleche"]}</span>
      </a>
      <a class="tuile" href="/pathologies/kyste-pilonidal/" data-reveal style="--d:2">
        <span class="tuile__chiffre">100<small>e</small></span>
        <h3>Kyste pilonidal au laser</h3>
        <p>Précurseurs à Nîmes : cent kystes traités au laser en moins d'un an.</p>
        <span class="tuile__pied">La technique {ICONES["fleche"]}</span>
      </a>
      <a class="tuile" href="/techniques/chirurgie-ambulatoire/" data-reveal style="--d:3">
        <span class="tuile__chiffre">&lt;12<small>h</small></span>
        <h3>Ambulatoire</h3>
        <p>Hernies, vésicule, proctologie, peau : rentrer dormir chez soi le soir même.</p>
        <span class="tuile__pied">Les conditions {ICONES["fleche"]}</span>
      </a>
      <a class="tuile" href="/techniques/rehabilitation-amelioree/" data-reveal style="--d:4">
        <span class="tuile__ico">{ICONES["bouclier"]}</span>
        <h3>Réhabilitation améliorée</h3>
        <p>Des mesures validées pour récupérer plus vite — pratique reconnue par le groupe GRACE.</p>
        <span class="tuile__pied">Comprendre {ICONES["fleche"]}</span>
      </a>
    </div>
  </div>
</section>'''


def parcours():
    etapes = "".join(f'<li class="etape" data-reveal style="--d:{i}" data-etape><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(PARCOURS))
    return f'''<section class="section" aria-labelledby="parcours-titre">
  <div class="conteneur">
    <div class="section__tete section__tete--2">
      <div>{surtitre("Votre parcours", "04")}<h2 id="parcours-titre">De la première consultation <em>au suivi.</em></h2></div>
      <div><p class="chapo">Nos secrétaires coordonnent chaque étape pour raccourcir les délais. Voici, simplement, ce qui vous attend.</p>
      <p class="mt-4"><a class="lien-fleche" href="/votre-parcours/">Démarches médicales et administratives {ICONES["fleche"]}</a></p></div>
    </div>
    <ol class="parcours">{etapes}</ol>
  </div>
</section>'''


def videos():
    return f'''<section class="section section--blanc" aria-labelledby="videos-titre">
  <div class="conteneur">
    <div class="section__tete section__tete--2">
      <div>{surtitre("Au bloc opératoire", "05")}<h2 id="videos-titre">Des interventions <em>filmées par l'équipe.</em></h2></div>
      <div><p class="chapo">Pour comprendre concrètement ce qui se passe pendant l'opération. Les vidéos se chargent depuis YouTube uniquement si vous les lancez.</p>
      <p class="mt-4"><a class="lien-fleche" href="/videos/">Toutes les vidéos {ICONES["fleche"]}</a></p></div>
    </div>
    <div class="grille grille--3">
      <div data-reveal>{video("robot-da-vinci")}</div>
      <div data-reveal style="--d:1">{video("hernie-inguinale-tep")}</div>
      <div data-reveal style="--d:2">{video("bypass-coelio")}</div>
    </div>
  </div>
</section>'''


def lieux():
    a = C["adresse"]
    pgs, hpf = ETABLISSEMENTS
    return f'''<section class="section" aria-labelledby="lieux-titre">
  <div class="conteneur">
    <div class="section__tete section__tete--2">
      <div>{surtitre("Où nous trouver", "06")}<h2 id="lieux-titre">Au cœur de Nîmes, <em>et jusqu'à Uzès.</em></h2></div>
      <p class="chapo">Le cabinet est à deux pas de la Polyclinique du Grand Sud. Les interventions ont lieu dans deux établissements privés nîmois, au plateau technique complet.</p>
    </div>
    <div class="lieux lieux--4">
      <article class="lieu lieu--principal" data-reveal>
        <p class="lieu__role">Le cabinet · consultations</p>
        <h3>Cabinet Nemaudig</h3>
        <div class="lieu__ligne">{ICONES["lieu"]}<address>{e(a["rue"])}<br>{e(a["complement"])}<br>{a["code_postal"]} {e(a["ville"])}</address></div>
        <p class="lieu__ligne">{ICONES["horloge"]}<span>{e(C["horaires_affiches"])}</span></p>
        <p class="lieu__ligne">{ICONES["tel"]}<a href="{tel_href()}" style="color:#fff">{C["telephone_affiche"]}</a></p>
        <div class="actions">{bouton("/cabinet/", "Découvrir le cabinet", "clair")}</div>
      </article>
      <article class="lieu" data-reveal style="--d:1">
        <p class="lieu__role">{e(pgs["role"])}</p>
        <h3>{e(pgs["nom"])}</h3>
        <p>{e(pgs["detail"])}</p>
        <p class="lieu__ligne">{ICONES["urgence"]}<span>Urgences : <a href="{tel_href(C["urgences_e164"])}">{C["urgences_tel"]}</a></span></p>
        <div class="actions"><a class="lien-fleche" href="/etablissements/">Établissements et anesthésie {ICONES["fleche"]}</a></div>
      </article>
      <article class="lieu" data-reveal style="--d:2">
        <p class="lieu__role">{e(hpf["role"])}</p>
        <h3>{e(hpf["nom"])}</h3>
        <p>{e(hpf["detail"])}</p>
        <div class="actions"><a class="lien-fleche" href="/etablissements/">Établissements et anesthésie {ICONES["fleche"]}</a></div>
      </article>
      <article class="lieu" data-reveal style="--d:3">
        <p class="lieu__role">Consultation avancée</p>
        <h3>{e(UZES["nom"])}</h3>
        <p>{e(UZES["creneau"])}, le Dr David Amielh consulte au plus près des patients de l'Uzège, depuis le {e(UZES["depuis"])}.</p>
        <p class="lieu__ligne">{ICONES["tel"]}<span>{" ou ".join(UZES["tel"])}</span></p>
        <div class="actions"><a class="lien-fleche" href="/consultation-uzes/">Consulter à Uzès {ICONES["fleche"]}</a></div>
      </article>
    </div>
  </div>
</section>'''


def actualites():
    cartes = "".join(f'''<a class="actu" href="/actualites/#{a["slug"]}" data-reveal style="--d:{i}">
  <p class="actu__meta"><span class="pastille pastille--menthe">{e(a["categorie"])}</span><span>{e(a["date_txt"])}</span></p>
  <h3>{e(a["titre"])}</h3><p>{e(a["texte"][:150].rsplit(" ", 1)[0])}…</p>
</a>''' for i, a in enumerate(ACTUALITES[:3]))
    return f'''<section class="section section--blanc" aria-labelledby="actus-titre">
  <div class="conteneur">
    <div class="section__tete section__tete--2">
      <div>{surtitre("Actualités", "07")}<h2 id="actus-titre">La vie <em>du cabinet.</em></h2></div>
      <p><a class="lien-fleche" href="/actualites/">Toutes les actualités {ICONES["fleche"]}</a></p>
    </div>
    <div class="actus">{cartes}</div>
  </div>
</section>'''


def questions():
    return f'''<section class="section" aria-labelledby="faq-titre">
  <div class="conteneur conteneur--etroit">
    <div class="section__tete centre">
      <div>{surtitre("Questions fréquentes", "08")}<h2 id="faq-titre">Vos questions, <em>nos réponses.</em></h2></div>
    </div>
    {faq(FAQ_ACCUEIL)}
    <p class="centre mt-6"><a class="lien-fleche" href="/faq/">Toutes les questions {ICONES["fleche"]}</a></p>
  </div>
</section>'''


def rendre(assets):
    corps = hero() + confiance() + voyage() + explorer() + equipe() + technologies() + parcours() + videos() + lieux() + actualites() + questions() + bandeau_rdv()
    corps += f'<script type="application/json" id="anatomie-donnees">{donnees_3d()}</script>'
    module = f'<script type="module" src="{assets["js3d"]}"></script>'
    return {"/": page(assets, "/", TITRE, DESC, corps, schemas=[schema_faq(FAQ_ACCUEIL)] + ([schema_film()] if film_present() else []), classe="accueil", extra_tete=module)}
