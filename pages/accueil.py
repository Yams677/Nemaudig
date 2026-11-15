"""Accueil : les cinq chirurgiens d'abord, puis « un organe à la fois », puis le cabinet."""
import config
from data.cabinet import ACTUALITES, PARCOURS, PRESENTATION
from data.chirurgiens import CHIRURGIENS, nom_complet
from data.organes import ORGANES
from data.pathologies import FAMILLES, PATHOLOGIES
from lib import liens, videos
from lib.gabarit import C, bouton_rdv, e, image_organe, page, sur_titre, u

# Ordre des portraits dans les arches (alternance des teintes et des silhouettes).
ARCHES = ["dr-mathias-alline", "dr-david-amielh", "dr-fanelly-torres", "dr-sylvain-laporte", "dr-emmanuel-prieur"]


def _mots(texte, depart=0):
    """Chaque mot dans son cadre : ils montent l'un après l'autre à l'ouverture."""
    return " ".join(f'<span class="mot"><span style="--i:{depart + i}">{e(m)}</span></span>' for i, m in enumerate(texte.split(" ")))


def _ouverture():
    par_slug = {c["slug"]: c for c in CHIRURGIENS}
    arches = "".join(f'''<li><a href="{u("/chirurgiens/" + s + "/")}" aria-label="{e(nom_complet(par_slug[s]))} — voir la fiche">
      <img src="{u("/img/" + s + "-800.webp")}" width="800" height="1000" alt="" fetchpriority="high">
      <span class="arche__nom">{e(nom_complet(par_slug[s]))}</span></a></li>''' for s in ARCHES)
    return f'''<section class="ouverture plan plan--clair" aria-labelledby="ouverture-titre">
  <div class="ouverture__halos" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="contenu ouverture__grille">
    <div class="ouverture__texte">
      {sur_titre("Chirurgie digestive et viscérale · Nîmes")}
      <h1 class="ouverture__titre" id="ouverture-titre">{_mots("Cinq chirurgiens,")} <em>{_mots("une équipe", 2)}</em> {_mots("à votre écoute.", 4)}</h1>
      <p class="chapo">{e(PRESENTATION[1])}</p>
      <div class="actions">
        {bouton_rdv()}
        <a class="btn btn--fil" href="{u("/specialites/")}">Découvrir nos spécialités</a>
      </div>
    </div>
    <ul class="arches" aria-label="Les chirurgiens du cabinet">{arches}</ul>
  </div>
</section>'''


def _chiffres():
    donnees = [
        ("5", "chirurgiens associés", "qui se connaissent depuis leur internat"),
        ("2", "établissements à Nîmes", "et une consultation à Uzès"),
        ("365", "jours et nuits par an", "de continuité des soins"),
        (str(len(PATHOLOGIES)), "pathologies expliquées", "avec leurs risques et leurs suites"),
    ]
    items = "".join(f'<li><span class="chiffre" data-compte="{n}">{n}</span><span class="chiffre__nom">{e(a)}</span><span class="chiffre__detail">{e(b)}</span></li>'
                    for n, a, b in donnees)
    return f'''<section class="plan plan--clair bloc bloc--serre" aria-label="Le cabinet en quelques repères">
  <div class="contenu"><ul class="chiffres">{items}</ul></div>
</section>'''


def _defilant():
    """Bandeau qui défile : les pathologies expliquées sur le site. Il se met en pause au survol ou au bouton."""
    noms = "".join(f'<li><a href="{u(liens.adresse_pathologie(p["slug"]))}">{e(p["court"])}</a></li>' for p in PATHOLOGIES)
    return f'''<section class="defilant" data-defilant aria-label="Les pathologies expliquées sur ce site">
  <div class="defilant__piste"><ul>{noms}</ul><ul aria-hidden="true">{noms.replace("<a ", '<a tabindex="-1" ')}</ul></div>
  <button class="defilant__pause" type="button" data-pause aria-pressed="false">Mettre le défilement en pause</button>
</section>'''


def _organes():
    """Un organe à la fois : image réaliste, quelques mots, lien vers la fiche."""
    onglets = "".join(f'<li><button class="onglet" type="button" data-organe="{o["cle"]}" aria-pressed="{"true" if i == 0 else "false"}">{e(o["nom"])}</button></li>'
                      for i, o in enumerate(ORGANES))
    vues = "".join(f'''<div class="vitrine__vue{" est-choisie" if i == 0 else ""}" data-vue="{o["cle"]}" style="--teinte: var(--{o["teinte"]})">
      <div class="vitrine__image">{image_organe(o)}</div>
      <div class="vitrine__texte"><p class="repere">{e(o["latin"])}</p>
        <h3 class="titre-l">{e(o["nom"])}</h3><p class="chapo">{e(o["role"])}</p>
        <a class="lien-fleche" href="{u("/explorer/")}#{o["cle"]}">Tout comprendre sur {e(o["article"])}</a></div>
    </div>''' for i, o in enumerate(ORGANES))
    return f'''<section class="plan plan--nuit bloc vitrine" data-vitrine aria-labelledby="vitrine-titre">
  <div class="contenu">
    <div class="bloc__tete">{sur_titre("Comprendre")}
      <h2 class="titre-l" id="vitrine-titre">Un organe à la fois.</h2></div>
    <div class="vitrine__barre"><ul class="onglets" aria-label="Organe affiché">{onglets}</ul>
      <button class="vitrine__pause" type="button" data-pause aria-pressed="false">Arrêter le changement automatique</button></div>
    <div class="vitrine__scene">{vues}</div>
  </div>
</section>'''


def _specialites():
    lignes = []
    for i, f in enumerate(FAMILLES):
        n = len(liens.slugs_de_la_famille(f["slug"]))
        cible = u("/specialites/") + "#" + f["slug"]
        lignes.append(f'''<li><a class="ligne" href="{cible}"><span class="repere">{i + 1:02d}</span>
      <span class="ligne__titre">{e(f["titre"])}</span><span class="ligne__texte">{e(f["intro"])}</span>
      <span class="ligne__compte">{n} fiche{"s" if n > 1 else ""}</span></a></li>''')
    return f'''<section class="plan plan--clair bloc" aria-labelledby="spe-titre">
  <div class="contenu">
    <div class="bloc__tete">{sur_titre("Nos spécialités")}
      <h2 class="titre-l" id="spe-titre">Huit domaines de prise en charge.</h2></div>
    <ol class="lignes">{"".join(lignes)}</ol>
  </div>
</section>'''


def _parcours():
    etapes = "".join(f'<li><span class="repere">Étape {i + 1}</span><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(PARCOURS))
    return f'''<section class="plan plan--clair bloc bloc--serre" aria-labelledby="parcours-titre">
  <div class="contenu">
    <div class="bloc__tete bloc__tete--ligne"><div>{sur_titre("Votre parcours")}
      <h2 class="titre-l" id="parcours-titre">De la première consultation au suivi.</h2></div>
      <a class="lien-fleche" href="{u("/preparer/")}">Préparer votre consultation</a></div>
    <ol class="etapes" data-avance>{etapes}</ol>
  </div>
</section>'''


def _actualites():
    cartes = "".join(f'''<li class="actu"><p class="repere">{e(a["date_txt"])} · {e(a["categorie"])}</p>
      <h3>{e(a["titre"])}</h3><p>{e(a["texte"])}</p></li>''' for a in ACTUALITES[:3])
    return f'''<section class="plan plan--clair bloc" aria-labelledby="actus-titre">
  <div class="contenu">
    <div class="bloc__tete">{sur_titre("Actualités du cabinet")}
      <h2 class="titre-l" id="actus-titre">Un site qui vit avec l'équipe.</h2></div>
    <ul class="actus">{cartes}</ul>
  </div>
</section>'''


def appel_rdv():
    """Bloc final commun à plusieurs pages."""
    from lib.gabarit import lien_tel
    return f'''<section class="plan plan--prune appel" aria-labelledby="appel-titre">
  <div class="contenu appel__grille">
    <div>{sur_titre("Prendre rendez-vous")}
      <h2 class="titre-l" id="appel-titre">Un secrétariat à votre écoute.</h2>
      <p class="chapo">{e(C["horaires_affiches"])}. Vous êtes orienté vers le chirurgien le plus à même de vous prendre en charge, en respectant vos souhaits et ceux du médecin qui vous adresse.</p></div>
    <div class="appel__actions">
      {bouton_rdv()}
      {lien_tel(C["telephone_affiche"], "btn btn--fil")}
    </div>
  </div>
</section>'''


def pages():
    ad = C["adresse"]
    json_ld = {
        "@context": "https://schema.org", "@type": "MedicalClinic", "name": C["nom_long"],
        "medicalSpecialty": "Surgical", "telephone": C["telephone_e164"], "url": config.SITE_URL,
        "address": {"@type": "PostalAddress", "streetAddress": ad["rue"], "postalCode": ad["code_postal"],
                    "addressLocality": ad["ville"], "addressCountry": "FR"},
    }
    corps = (_ouverture() + _chiffres() + _defilant() + _organes() + _specialites() + _parcours()
             + videos.galerie() + _actualites() + appel_rdv())
    return [("/", page(
        chemin="/", titre="Nemaudig — chirurgie digestive et viscérale à Nîmes",
        description="Cinq chirurgiens digestifs à Nîmes : cancérologie digestive, foie, côlon et rectum, proctologie, obésité, hernies. Comprendre chaque organe et prendre rendez-vous.",
        corps=corps, scripts=("accueil.js",), classe="page-accueil", json_ld=json_ld))]
