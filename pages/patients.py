"""Espace patients : parcours, honoraires, contact / rendez-vous, Uzès, établissements."""

from urllib.parse import quote

import config
from data.cabinet import (ANESTHESIE_KENNEDY, DEMARCHES_ADMIN, DEMARCHES_MEDICALES, ETABLISSEMENTS, HONORAIRES, PARCOURS,
                          SUIVI, UZES)
from lib.composants import bandeau_rdv, mini_medecin, tete_page
from lib.html import C, ICONES, bouton, e, surtitre, tel_href
from lib.layout import page

REDIRECTIONS = {"parcours-de-nos-patients": "/votre-parcours/", "demarches-medicales": "/votre-parcours/#demarches-medicales",
                "demarches-administratives": "/votre-parcours/#demarches-administratives", "suivi-post-operatoire": "/votre-parcours/#suivi",
                "les-honoraires": "/honoraires/", "contact": "/contact/", "uzes": "/consultation-uzes/", "les-cliniques": "/etablissements/"}

ADRESSE_TXT = f"{C['adresse']['rue']}, {C['adresse']['code_postal']} {C['adresse']['ville']}"
ITINERAIRE = f"https://www.google.com/maps/search/?api=1&query={quote('Nemaudig ' + ADRESSE_TXT)}"


def bloc_anesthesie(a):
    tels = " · ".join(f'<a href="{tel_href(t)}">{t}</a>' for t in a["tel"])
    return f'<div class="encart"><h3>{e(a["nom"])}</h3><p class="lieu__ligne">{ICONES["lieu"]}<span>{e(a["adresse"])}</span></p><p class="lieu__ligne mb-0">{ICONES["tel"]}<span>{tels}</span></p></div>'


def page_parcours(assets):
    etapes = "".join(f'<li class="etape" data-reveal style="--d:{i}" data-etape><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(PARCOURS))
    med = "".join(f"<li>{e(x)}</li>" for x in DEMARCHES_MEDICALES)
    adm = "".join(f'<li class="etape" data-etape style="padding-bottom:20px"><p style="font-size:1rem;color:var(--encre)">{e(x)}</p></li>' for x in DEMARCHES_ADMIN)
    anest = "".join(bloc_anesthesie(x["anesthesie"]) for x in ETABLISSEMENTS)
    suivi = "".join(f"<li>{e(x)}</li>" for x in SUIVI)
    corps = tete_page("Votre parcours, <em>étape par étape.</em>",
                      "De la première consultation au suivi, nos secrétaires coordonnent chaque étape. Voici ce qu'il faut savoir et ce qu'il faut faire.",
                      "Patients", "var(--ciel)") + f'''
<section class="section section--serree"><div class="conteneur"><ol class="parcours">{etapes}</ol></div></section>
<section class="section section--blanc" id="demarches-medicales" aria-labelledby="dm"><div class="conteneur">
  <div class="section__tete section__tete--2"><div>{surtitre("Avant l'opération", "01")}<h2 id="dm">Démarches <em>médicales</em></h2></div><ul class="liste">{med}</ul></div>
  <h3>Cabinets d'anesthésie</h3><div class="grille grille--2 mt-4">{anest}</div>
</div></section>
<section class="section" id="demarches-administratives" aria-labelledby="da"><div class="conteneur">
  <div class="section__tete section__tete--2"><div>{surtitre("Avant et après le séjour", "02")}<h2 id="da">Démarches <em>administratives</em></h2></div>
  <p class="chapo">Dans tous les cas, le consentement éclairé signé doit être rapporté au cabinet avant l'opération.</p></div>
  <ol class="parcours" style="grid-template-columns:1fr;max-width:720px">{adm}</ol>
  <p><a class="lien-fleche" href="/honoraires/">Honoraires et remboursements {ICONES["fleche"]}</a></p>
</div></section>
<section class="section section--blanc" id="suivi" aria-labelledby="su"><div class="conteneur">
  <div class="section__tete section__tete--2"><div>{surtitre("Après l'opération", "03")}<h2 id="su">Le suivi <em>postopératoire</em></h2></div><ul class="liste">{suivi}</ul></div>
  <div class="grille grille--3">
    <a class="carte" href="/techniques/rehabilitation-amelioree/"><span class="carte__ico">{ICONES["bouclier"]}</span><h3>Réhabilitation améliorée</h3><p>Récupérer plus vite, avec moins de complications.</p></a>
    <a class="carte" href="/chirurgiens/#equipe-paramedicale"><span class="carte__ico">{ICONES["coeur"]}</span><h3>Stomathérapie</h3><p>Une infirmière spécialisée vous accompagne avant et après une stomie.</p></a>
    <a class="carte" href="/faq/"><span class="carte__ico">{ICONES["question"]}</span><h3>Questions fréquentes</h3><p>Douleur, alimentation, reprise du sport, arrêt de travail…</p></a>
  </div>
</div></section>''' + bandeau_rdv()
    return page(assets, "/votre-parcours/", "Votre parcours patient — Nemaudig, chirurgie à Nîmes",
                "Consultation, anesthésie, préadmission, intervention et suivi : toutes les démarches médicales et administratives avant et après une opération à Nîmes.",
                corps, fil=[("/votre-parcours/", "Votre parcours")])


def page_honoraires(assets):
    H = HONORAIRES
    lignes = "".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td><td>{e(c)}</td></tr>" for a, b, c in H["lignes"])
    note = '<p class="note-a-valider mt-4">Tarifs repris tels quels du site actuel — à confirmer par le cabinet avant mise en ligne.</p>' if config.DEMO else ""
    corps = tete_page("Honoraires <em>et remboursements</em>", e(H["secteur"]), "Patients", "var(--sable)") + f'''
<section class="section section--serree"><div class="conteneur conteneur--etroit">
  <h2>Consultations</h2>
  <table class="tableau"><thead><tr><th>Acte</th><th>Tarif</th><th>Sécurité sociale</th></tr></thead><tbody>{lignes}</tbody></table>{note}
  <h2 class="mt-7">Interventions</h2><p>{e(H["intervention"])}</p>
  <h2 class="mt-7">Votre mutuelle</h2><p>{e(H["mutuelle"])}</p>
  <div class="encart encart--menthe mt-4"><p class="mb-0">{e(H["exemple"])}</p></div>
</div></section>''' + bandeau_rdv()
    return page(assets, "/honoraires/", "Honoraires des chirurgiens — Nemaudig, secteur 2, Nîmes",
                "Chirurgiens conventionnés secteur 2 à Nîmes : tarifs de consultation, devis pour les interventions, prise en charge des dépassements par votre mutuelle.",
                corps, fil=[("/votre-parcours/", "Votre parcours"), ("/honoraires/", "Honoraires")])


def plan_stylise():
    """Plan schématique (aucun service tiers chargé)."""
    return '''<svg viewBox="0 0 600 360" preserveAspectRatio="xMidYMid slice" aria-hidden="true">
  <rect width="600" height="360" fill="#DCF1EA"/>
  <g fill="none" stroke="#fff" stroke-linecap="round">
    <path d="M-20 250 C120 230 220 260 320 200 S520 120 640 140" stroke-width="22"/>
    <path d="M180 -20 C200 80 240 160 300 200 S360 320 380 400" stroke-width="14"/>
    <path d="M-20 90 C100 110 200 80 300 120 S480 220 640 260" stroke-width="9"/>
    <path d="M420 -20 C410 80 430 160 470 240" stroke-width="7"/>
  </g>
  <g fill="#C9E7DD"><rect x="60" y="130" width="70" height="44" rx="8"/><rect x="380" y="170" width="90" height="56" rx="8"/><rect x="230" y="270" width="60" height="40" rx="8"/><rect x="470" y="40" width="80" height="50" rx="8"/></g>
</svg>'''


def page_contact(assets):
    a = C["adresse"]
    corps = tete_page("Prendre <em>rendez-vous</em>",
                      "Par téléphone auprès du secrétariat, en ligne, ou à Uzès avec le Dr Amielh. Pour votre sécurité, aucune information médicale n'est demandée sur ce site.",
                      "Contact", "var(--menthe)") + f'''
<section class="section section--serree"><div class="conteneur">
  <div class="contact">
    <div class="lieu lieu--principal" data-reveal><p class="lieu__role">Par téléphone</p><h2 style="color:#fff;font-size:2.2rem">{C["telephone_affiche"]}</h2>
      <p class="lieu__ligne">{ICONES["horloge"]}<span>{e(C["horaires_affiches"])}</span></p><p>Nos trois secrétaires programment consultations, examens et interventions.</p>
      <div class="actions">{bouton(tel_href(), "Appeler le cabinet", "clair", icone="tel")}</div></div>
    <div class="lieu" id="en-ligne" data-reveal style="--d:1"><p class="lieu__role">En ligne, 24 h/24</p><h2 style="font-size:2.2rem">{C["rdv_en_ligne_libelle"]}</h2>
      <p>Sur le site Maiia, recherchez « Nemaudig » ou le nom de l'un des cinq chirurgiens.</p>
      {'<p class="note-a-valider">Lien direct vers la page Maiia du cabinet à récupérer.</p>' if config.DEMO else ""}
      <div class="actions">{bouton(C["rdv_en_ligne"], "Ouvrir Maiia", "plein", externe=True, icone="agenda")}</div></div>
    <div class="lieu" data-reveal style="--d:2"><p class="lieu__role">À Uzès</p><h2 style="font-size:2.2rem">Dr Amielh</h2>
      <p>{e(UZES["creneau"])}, au {e(UZES["nom"])}.</p><p class="lieu__ligne">{ICONES["tel"]}<span>{" ou ".join(UZES["tel"])}</span></p><p class="petit">{e(UZES["horaires_tel"])}</p>
      <div class="actions"><a class="lien-fleche" href="/consultation-uzes/">Consultation à Uzès {ICONES["fleche"]}</a></div></div>
  </div>
</div></section>
<section class="section section--serree" aria-labelledby="venir"><div class="conteneur">
  <div class="grille grille--2" style="align-items:stretch">
    <figure class="carte-plan" data-reveal>{plan_stylise()}<div class="carte-plan__epingle"><span>Nemaudig · 2e étage</span><i></i></div><figcaption class="visuellement-cache">Illustration décorative, sans valeur de plan : utilisez le bouton Itinéraire.</figcaption></figure>
    <div data-reveal style="--d:1">{surtitre("Venir au cabinet")}<h2 id="venir">Immeuble l'Odyssée, <em>à deux pas de la Polyclinique.</em></h2>
      <address class="chapo">{e(a["rue"])}<br>{e(a["complement"])}<br>{a["code_postal"]} {e(a["ville"])}</address>
      <ul class="liste mt-4"><li>Parking, ascenseurs</li><li>Locaux accessibles aux personnes handicapées</li><li>Au 1er étage, un espace adapté à l'accueil des patients en situation d'obésité</li></ul>
      <div class="actions mt-6">{bouton(ITINERAIRE, "Itinéraire", "ligne", externe=True, icone="lieu")}<a class="lien-fleche" href="mailto:{C["email"]}">{ICONES["mail"]} {C["email"]}</a></div>
      <p class="petit mt-4">Pour un rendez-vous, privilégiez le téléphone ou Maiia : n'envoyez pas d'informations médicales par e-mail.</p>
    </div>
  </div>
</div></section>
<section class="section section--serree"><div class="conteneur"><div class="encart encart--peche" style="display:flex;gap:16px;align-items:flex-start">{ICONES["urgence"]}<div>
  <h2>En cas d'urgence</h2><p class="mb-0">Urgence vitale : composez le <strong>15</strong>. {e(C["urgences_nom"])} : <a href="{tel_href(C["urgences_e164"])}"><strong>{C["urgences_tel"]}</strong></a>.</p></div></div></div></section>'''
    schema = {"@context": "https://schema.org", "@type": "ContactPage", "name": "Contact et rendez-vous — Nemaudig",
              "about": {"@id": f"{config.SITE_URL}/#cabinet"}}
    return page(assets, "/contact/", "Rendez-vous chirurgien digestif Nîmes — Nemaudig",
                "Prendre rendez-vous avec un chirurgien digestif à Nîmes : 04 66 05 24 63 du lundi au vendredi 8 h – 18 h 30, en ligne sur Maiia, ou à Uzès.",
                corps, fil=[("/contact/", "Rendez-vous")], schemas=[schema])


def page_uzes(assets):
    corps = tete_page("Consultation de chirurgie digestive <em>à Uzès</em>",
                      f"Depuis le {UZES['depuis']}, le Dr David Amielh consulte {UZES['creneau'].lower()} au {UZES['nom']} — au plus près des patients de l'Uzège.",
                      "Uzès · Gard", "var(--sauge)") + f'''
<section class="section section--serree"><div class="conteneur"><div class="grille grille--2" style="align-items:start">
  <div class="lieu lieu--principal" data-reveal><p class="lieu__role">Rendez-vous</p><h2 style="color:#fff">{" ou ".join(UZES["tel"])}</h2>
    <p class="lieu__ligne">{ICONES["horloge"]}<span>{e(UZES["horaires_tel"])}</span></p><p class="lieu__ligne">{ICONES["lieu"]}<span>{e(UZES["nom"])}</span></p>
    <div class="actions">{bouton(tel_href(UZES["tel"][0]), "Appeler le centre hospitalier", "clair", icone="tel")}</div></div>
  <div class="encart" data-reveal style="--d:1"><h2>Votre chirurgien à Uzès</h2>{mini_medecin("dr-david-amielh")}
    <p class="mt-4">Cancérologie digestive, chirurgie de l'œsophage, chirurgie générale et robotique. Il est aussi formateur pour la technique mini-invasive TEP de chirurgie des hernies inguinales.</p>
    <p class="mb-0">Les interventions ont lieu à Nîmes, dans l'un des deux établissements privés où opère l'équipe.</p></div>
</div></div></section>''' + bandeau_rdv()
    return page(assets, "/consultation-uzes/", "Chirurgien digestif à Uzès — Dr Amielh, Nemaudig",
                "Consultation de chirurgie digestive à Uzès : le Dr David Amielh consulte le lundi matin au centre hospitalier d'Uzès. Rendez-vous au 04 66 63 71 09.",
                corps, fil=[("/consultation-uzes/", "Consultation à Uzès")])


def page_etablissements(assets):
    cartes = "".join(f'''<article class="lieu" data-reveal style="--d:{i}"><p class="lieu__role">{e(x["role"])}</p><h2 style="font-size:1.9rem">{e(x["nom"])}</h2>
  <p>{e(x["detail"])}</p>{f'<p class="lieu__ligne">{ICONES["urgence"]}<span>Urgences : <a href="{tel_href(C["urgences_e164"])}">{x["urgences"]}</a></span></p>' if x["urgences"] else ""}
  <div class="actions"><a class="lien-fleche" href="{x["site"]}" target="_blank" rel="noopener">Site de l'établissement {ICONES["externe"]}</a></div></article>''' for i, x in enumerate(ETABLISSEMENTS))
    anest = "".join(bloc_anesthesie(x["anesthesie"]) for x in ETABLISSEMENTS)
    kennedy = (f'<div class="encart mt-4"><h3>{e(ANESTHESIE_KENNEDY["nom"])}</h3><p class="lieu__ligne mb-0">{ICONES["tel"]}<span>{ANESTHESIE_KENNEDY["tel"][0]}</span></p>'
               f'<p class="note-a-valider mt-4">Mentionné sur l\'ancienne page « Uzès » sans autre précision : rôle à confirmer avec le cabinet.</p></div>') if config.DEMO else ""
    corps = tete_page("Deux établissements <em>privés à Nîmes</em>",
                      "Les interventions sont réalisées dans l'un des deux centres privés de Nîmes, qui disposent d'un plateau technique complet : endoscopie, imagerie médicale, radiologie interventionnelle, réanimation chirurgicale, unité de soins continus, centre de dialyse…",
                      "Établissements", "var(--ciel)") + f'''
<section class="section section--serree"><div class="conteneur"><div class="grille grille--2">{cartes}</div>
  <div class="section__tete mt-7">{surtitre("Consultation d'anesthésie")}<h2>Prendre rendez-vous <em>avec l'anesthésiste</em></h2>
  <p class="chapo">Obligatoire avant toute anesthésie générale ou loco-régionale, auprès du cabinet rattaché à l'établissement où vous serez opéré.</p></div>
  <div class="grille grille--2">{anest}</div>{kennedy}
</div></section>''' + bandeau_rdv()
    return page(assets, "/etablissements/", "Polyclinique Grand Sud et Franciscaines — Nemaudig",
                "Les chirurgiens de Nemaudig opèrent à la Polyclinique du Grand Sud et à l'Hôpital privé des Franciscaines, à Nîmes. Coordonnées des cabinets d'anesthésie.",
                corps, fil=[("/etablissements/", "Établissements")])


def rendre(assets):
    return {"/votre-parcours/": page_parcours(assets), "/honoraires/": page_honoraires(assets), "/contact/": page_contact(assets),
            "/consultation-uzes/": page_uzes(assets), "/etablissements/": page_etablissements(assets)}
