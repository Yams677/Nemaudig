"""Pages pratiques : préparer sa consultation, prévention, centres, rendez-vous."""
from urllib.parse import quote

import config
from data.cabinet import (DEMARCHES_ADMIN, DEMARCHES_MEDICALES, ETABLISSEMENTS, HONORAIRES, LOCAUX, SITES_UTILES, SUIVI, UZES)
from data.chirurgiens import CHIRURGIENS, nom_complet
from data.examens import DOCUMENTS, EXAMENS
from data.orientation import SIGNES
from data.pathologies import FAMILLES, PATHOLOGIES, PAR_SLUG as PATHOLOGIE
from lib import liens, videos
from lib.gabarit import C, bandeau, e, lien_tel, liste, page, provisoire, sur_titre, u
from pages.accueil import appel_rdv


# ── Préparer votre consultation ───────────────────────────────────────────────
def _faq():
    """Questions-réponses déjà publiées par le cabinet + celles des fiches d'examens (provisoires)."""
    entrees = [(q, r, p["court"], False) for p in PATHOLOGIES for q, r in p["faq"]]
    entrees += [(q, r, x["titre"], True) for x in EXAMENS for q, r in x["faq"]]
    items = "".join(f'''<details class="question" data-question><summary>{e(q)}<span class="repere">{e(theme)}{" ◇" if prov else ""}</span></summary><p>{e(r)}</p></details>'''
                    for q, r, theme, prov in entrees)
    return f'''<section class="plan plan--clair bloc bloc--serre" id="faq" aria-labelledby="faq-titre"><div class="contenu etroit">
  <div class="bloc__tete">{sur_titre("Questions fréquentes")}
    <h2 class="titre-l" id="faq-titre">Trouvez une réponse.</h2></div>
  <label class="recherche"><span class="visuellement-cache">Rechercher dans les questions</span>
    <input type="search" placeholder="Un mot : vésicule, cicatrice, polype…" data-recherche autocomplete="off"></label>
  <p class="note" data-recherche-etat role="status" aria-live="polite">{len(entrees)} questions, issues des fiches du cabinet.</p>
  <div class="questions" data-questions>{items}</div>
  <p class="note">◇ Réponses provisoires, à valider. La recherche se fait dans votre navigateur : rien n'est transmis ni enregistré.</p>
</div></section>'''


def _preparer():
    documents = "".join(f'''<li><label class="case"><input type="checkbox"><span><strong>{e(t)}</strong>{" <span aria-hidden=\"true\">◇</span>" if prov else ""}<small>{e(d)}</small></span></label></li>'''
                        for t, d, prov in DOCUMENTS)
    pdfs = "".join(f'<li><a class="lien-fleche" href="{e(p["pdf"])}" target="_blank" rel="noopener">{e(p["titre"])} — fiche PDF<span class="visuellement-cache"> (nouvel onglet)</span></a></li>'
                   for p in PATHOLOGIES if p["pdf"] and p["slug"] != "cholecystectomie")
    tarifs = "".join(f'<tr><th scope="row">{e(a)}</th><td>{e(b)}</td><td>{e(c)}</td></tr>' for a, b, c in HONORAIRES["lignes"])
    corps = bandeau("Préparer", "Préparer <em>votre consultation</em>.",
                    "Quelques documents à réunir, des démarches expliquées pas à pas : pour que le temps de la consultation soit consacré à l'essentiel.",
                    [(None, "Préparer")])
    corps += f'''<section class="plan plan--clair bloc" aria-labelledby="doc-titre"><div class="contenu deux-colonnes">
  <div>{sur_titre("Le jour de la consultation")}<h2 class="titre-l" id="doc-titre">Ce qu'il faut apporter.</h2>
    <p>Cochez au fur et à mesure, puis imprimez ou enregistrez la liste en PDF.</p>
    <button class="btn btn--sombre" type="button" data-imprimer>Imprimer la liste<span class="btn__fleche" aria-hidden="true"></span></button>
    <p class="note">◇ Liste à valider par le secrétariat. Les cases ne sont pas enregistrées.</p></div>
  <ul class="cases">{documents}</ul>
</div></section>
<section class="plan plan--clair bloc bloc--serre" aria-labelledby="dem-titre"><div class="contenu">
  <div class="bloc__tete">{sur_titre("Avant une intervention")}<h2 class="titre-l" id="dem-titre">Les démarches, dans l'ordre.</h2></div>
  <div class="trois-colonnes">
    <div><h3 class="repere">Démarches médicales</h3>{liste(DEMARCHES_MEDICALES, "liste liste--num")}</div>
    <div><h3 class="repere">Démarches administratives</h3>{liste(DEMARCHES_ADMIN, "liste liste--num")}</div>
    <div><h3 class="repere">Le suivi</h3>{liste(SUIVI, "liste liste--num")}
      <h3 class="repere">Fiches à télécharger</h3><ul class="liste-liens">{pdfs}</ul></div>
  </div>
</div></section>
<section class="plan plan--clair bloc bloc--serre" aria-labelledby="hon-titre"><div class="contenu deux-colonnes">
  <div>{sur_titre("Honoraires")}<h2 class="titre-l" id="hon-titre">Une information transparente.</h2>
    <p>{e(HONORAIRES["secteur"])}</p>{provisoire("Tarifs repris du site actuel — date de mise à jour à confirmer")}</div>
  <div><div class="tableau-defile"><table class="tableau tableau--clair">
      <thead><tr><th scope="col">Consultation</th><th scope="col">Tarif</th><th scope="col">Sécurité sociale</th></tr></thead>
      <tbody>{tarifs}</tbody></table></div>
    <p>{e(HONORAIRES["intervention"])}</p><p>{e(HONORAIRES["mutuelle"])}</p></div>
</div></section>''' + _faq()
    return ("/preparer/", page(
        chemin="/preparer/", titre="Préparer votre consultation — Nemaudig, Nîmes",
        description="Documents à apporter, consultation d'anesthésie, démarches administratives, honoraires et réponses aux questions fréquentes avant une consultation de chirurgie digestive.",
        corps=corps + appel_rdv()))


# ── Prévention et conseils ────────────────────────────────────────────────────
def _prevention():
    signes = "".join(f'''<li><p>{e(texte)}</p><ul class="puces puces--claires">{"".join(
        f'<li><a class="puce puce--claire" href="{u(liens.adresse_pathologie(s))}">{e(PATHOLOGIE[s]["court"])}</a></li>' for s in slugs)}</ul></li>'''
                     for _, texte, slugs in SIGNES)
    conseils = [
        ("Bouger", "Une activité physique régulière, adaptée à votre âge et à votre forme."),
        ("Manger des fibres", "Légumes, fruits, légumes secs, céréales complètes."),
        ("Limiter", "L'alcool, la viande rouge et les charcuteries."),
        ("Ne pas fumer", "Le tabac augmente le risque de plusieurs cancers digestifs."),
        ("Surveiller son poids", "Le surpoids favorise le reflux, les calculs et certains cancers."),
        ("Se faire dépister", "De 50 à 74 ans, tous les deux ans — et plus tôt en cas de risque particulier."),
    ]
    liens_utiles = "".join(f'<li><a class="lien-fleche" href="{e(a)}" target="_blank" rel="noopener">{e(n)}<span class="visuellement-cache"> (nouvel onglet)</span></a></li>'
                           for n, a in SITES_UTILES + [("Institut national du cancer — dépistage du cancer colorectal", "https://www.e-cancer.fr/")])
    jalons = "".join(f'<li style="--i:{i}"><span>{50 + 2 * i}</span></li>' for i in range(13))
    corps = bandeau("Prévention", "Prévenir, <em>dépister</em>, agir tôt.",
                    "La plupart des maladies digestives se soignent d'autant mieux qu'elles sont découvertes tôt.",
                    [(None, "Prévention")])
    corps += f'''<section class="plan plan--clair bloc" aria-labelledby="dep-titre"><div class="contenu">
  <div class="deux-colonnes"><div>{sur_titre("Dépistage organisé")}
      <h2 class="titre-l" id="dep-titre">Cancer colorectal : un test simple, tous les deux ans.</h2></div>
    <div class="prose"><p class="chapo">De 50 à 74 ans, les femmes et les hommes sans symptôme ni risque particulier sont invités à réaliser, chez eux, un test de recherche de sang dans les selles.</p>
      <ul class="liste"><li>Le kit est remis par le médecin traitant ou le pharmacien ; il peut aussi être commandé en ligne.</li>
        <li>Le test est pris en charge par l'Assurance Maladie, sans avance de frais.</li>
        <li>S'il est positif, une coloscopie est nécessaire pour en rechercher la cause.</li>
        <li>Antécédents personnels ou familiaux, maladie inflammatoire de l'intestin : le suivi est différent, parlez-en à votre médecin.</li></ul>
      <a class="lien-fleche" href="{u("/parcours-de-soins/coloscopie/")}">Comprendre la coloscopie</a></div></div>
  <div class="frise" role="img" aria-label="Un test tous les deux ans, de 50 à 74 ans"><ol>{jalons}</ol>
    <p class="repere">Un test tous les deux ans · de 50 à 74 ans</p></div>
  {provisoire("Texte fondé sur les recommandations de l'INCa et de l'Assurance Maladie — à relire par l'équipe")}
</div></section>
<section class="plan plan--clair bloc bloc--serre" aria-labelledby="conseils-titre"><div class="contenu">
  <div class="bloc__tete">{sur_titre("Au quotidien")}<h2 class="titre-l" id="conseils-titre">Six habitudes qui protègent.</h2></div>
  <ul class="engagements engagements--3">{"".join(f"<li><h3>{e(t)}</h3><p>{e(d)}</p></li>" for t, d in conseils)}</ul>
  {provisoire("Conseils généraux de prévention — à valider par l'équipe")}
</div></section>
<section class="plan plan--clair bloc bloc--serre" aria-labelledby="signes-titre"><div class="contenu etroit">
  <div class="bloc__tete">{sur_titre("Quand consulter ?")}<h2 class="titre-l" id="signes-titre">Des signes à ne pas laisser traîner.</h2>
    <p class="chapo">Chaque signe renvoie vers les fiches du cabinet qui en parlent. Ce n'est pas un diagnostic : seul un médecin peut l'établir.</p></div>
  <ul class="signes">{signes}</ul>
  <p class="avertissement">Douleur brutale et intense, vomissements de sang, selles noires, fièvre élevée : appelez le 15.</p>
</div></section>''' + videos.galerie("Comprendre en images") + f'''<section class="plan plan--clair bloc bloc--serre"><div class="contenu etroit">
  <div class="bloc__tete">{sur_titre("Pour aller plus loin")}<h2 class="titre-m">Sites de référence</h2></div>
  <ul class="liste-liens">{liens_utiles}</ul></div></section>'''
    return ("/prevention/", page(
        chemin="/prevention/", titre="Prévention et dépistage des maladies digestives — Nemaudig",
        description="Dépistage organisé du cancer colorectal de 50 à 74 ans, habitudes de vie, signes qui doivent amener à consulter : les conseils de prévention du cabinet Nemaudig.",
        corps=corps + appel_rdv()))


# ── Nos centres ───────────────────────────────────────────────────────────────
def _itineraire(recherche):
    return e("https://www.openstreetmap.org/search?query=" + quote(recherche))


def _centres():
    ad = C["adresse"]
    lieux = [f'''<li class="lieu" data-lieu="cabinet"><p class="repere">01 · Consultations</p><h2 class="titre-m">Cabinet Nemaudig</h2>
      <p>{e(ad["rue"])}<br>{e(ad["complement"])}<br>{e(ad["code_postal"])} {e(ad["ville"])}</p>
      <p>{e(C["horaires_affiches"])}<br>{lien_tel(C["telephone_affiche"], "lien-tel")}</p>
      <a class="lien-fleche" href="{_itineraire(ad["rue"] + " " + ad["ville"])}" target="_blank" rel="noopener">Voir le plan<span class="visuellement-cache"> (nouvel onglet)</span></a></li>''']
    for i, x in enumerate(ETABLISSEMENTS):
        urgences = f'<p>Urgences : {lien_tel(x["urgences"], "lien-tel")}</p>' if x["urgences"] else ""
        an = x["anesthesie"]
        tels = " · ".join(lien_tel(t, "lien-tel") for t in an["tel"])
        lieux.append(f'''<li class="lieu" data-lieu="{x["slug"]}"><p class="repere">{i + 2:02d} · {e(x["role"])}</p><h2 class="titre-m">{e(x["nom"])}</h2>
      <p>{e(x["detail"])}</p>{urgences}
      <p class="note"><strong>Consultation d'anesthésie</strong><br>{e(an["adresse"])}<br>{tels}</p>
      <a class="lien-fleche" href="{_itineraire(x["nom"] + " Nîmes")}" target="_blank" rel="noopener">Voir le plan<span class="visuellement-cache"> (nouvel onglet)</span></a></li>''')
    medecin = next(c for c in CHIRURGIENS if c["slug"] == UZES["chirurgien"])
    tels = " · ".join(lien_tel(t, "lien-tel") for t in UZES["tel"])
    lieux.append(f'''<li class="lieu" data-lieu="uzes"><p class="repere">04 · Consultation avancée</p><h2 class="titre-m">{e(UZES["nom"])}</h2>
      <p>Le <a href="{u("/chirurgiens/" + medecin["slug"] + "/")}">{e(nom_complet(medecin))}</a> y consulte {e(UZES["creneau"].lower())}, depuis le {e(UZES["depuis"])}.</p>
      <p>{tels}<br>{e(UZES["horaires_tel"])}</p>
      <a class="lien-fleche" href="{_itineraire("Centre hospitalier Uzès")}" target="_blank" rel="noopener">Voir le plan<span class="visuellement-cache"> (nouvel onglet)</span></a></li>''')
    g = C["geo"]
    boite = f'{g["lng"] - 0.02}%2C{g["lat"] - 0.012}%2C{g["lng"] + 0.02}%2C{g["lat"] + 0.012}'
    carte_src = f'https://www.openstreetmap.org/export/embed.html?bbox={boite}&layer=mapnik&marker={g["lat"]}%2C{g["lng"]}'
    corps = bandeau("Nos centres", "Quatre lieux, <em>une même équipe</em>.",
                    "Un cabinet de consultation, deux établissements privés à Nîmes où nous opérons, et une consultation à Uzès.",
                    [(None, "Centres")])
    corps += f'''<section class="plan plan--clair bloc"><div class="contenu centres">
  <div class="carte-lieux">
    <svg viewBox="0 0 400 420" role="img" aria-labelledby="carte-titre"><title id="carte-titre">Situation schématique : Uzès au nord, Nîmes au sud</title>
      <path class="carte-lieux__axe" d="M210 70 C196 150 220 230 204 318"/>
      <text class="carte-lieux__km" x="232" y="196">≈ 25 km</text>
      <g class="carte-lieux__point" data-point="uzes" transform="translate(210 66)"><circle r="6"/><text x="16" y="5">Uzès · centre hospitalier</text></g>
      <g class="carte-lieux__ville" transform="translate(204 330)"><circle r="62"/><text x="0" y="86" text-anchor="middle">Nîmes</text></g>
      <g class="carte-lieux__point" data-point="cabinet" transform="translate(186 348)"><circle r="6"/><text x="-14" y="5" text-anchor="end">Cabinet</text></g>
      <g class="carte-lieux__point" data-point="polyclinique-grand-sud" transform="translate(204 362)"><circle r="6"/><text x="14" y="18">Polyclinique du Grand Sud</text></g>
      <g class="carte-lieux__point" data-point="hopital-prive-franciscaines" transform="translate(222 312)"><circle r="6"/><text x="14" y="-6">Hôpital privé des Franciscaines</text></g>
    </svg>
    <p class="note">Schéma de situation, sans échelle.</p>
    <div class="carte-osm" data-carte="{e(carte_src)}">
      <button class="btn btn--sombre" type="button" data-carte-charger>Afficher la carte du cabinet<span class="btn__fleche" aria-hidden="true"></span></button>
      <p class="note">La carte OpenStreetMap n'est chargée qu'à votre demande. ◇ Position du repère à vérifier sur place.</p>
    </div>
  </div>
  <ol class="lieux">{"".join(lieux)}</ol>
</div></section>
<section class="plan plan--nuit bloc" aria-labelledby="locaux-titre"><div class="contenu deux-colonnes">
  <div>{sur_titre("Le cabinet")}<h2 class="titre-l" id="locaux-titre">Des locaux pensés pour l'accueil.</h2></div>
  <div class="prose">{"".join(f"<p>{e(x)}</p>" for x in LOCAUX)}
    {provisoire("Photographies des locaux à fournir par le cabinet")}</div>
</div></section>'''
    return ("/centres/", page(
        chemin="/centres/", titre="Nos centres à Nîmes et Uzès — Nemaudig",
        description="Cabinet Nemaudig, Polyclinique du Grand Sud, Hôpital privé des Franciscaines et consultation au Centre hospitalier d'Uzès : adresses, téléphones et accès.",
        corps=corps + appel_rdv(), classe="page-centres"))


# ── Prendre rendez-vous ───────────────────────────────────────────────────────
def _rdv():
    domaines = [{"cle": f["slug"], "nom": f["titre"], "chirurgiens": [c["slug"] for c in liens.chirurgiens_de_la_famille(f["slug"])]}
                for f in FAMILLES]
    chirurgiens = [{"cle": c["slug"], "nom": nom_complet(c), "accroche": c["accroche"],
                    "photo": u(f'/img/{c["slug"]}-400.webp'), "fiche": u(f'/chirurgiens/{c["slug"]}/'),
                    "uzes": c["slug"] == UZES["chirurgien"]} for c in CHIRURGIENS]
    donnees = {"domaines": domaines, "chirurgiens": chirurgiens, "tel": C["telephone_affiche"],
               "telUzes": UZES["tel"], "horaires": C["horaires_affiches"], "horairesUzes": UZES["horaires_tel"],
               "creneauUzes": UZES["creneau"], "maiia": C["rdv_en_ligne"], "demo": config.DEMO}
    options = "".join(f'<li><button class="choix" type="button" data-domaine="{f["slug"]}">{e(f["titre"])}</button></li>' for f in FAMILLES)
    tels_uzes = " · ".join(lien_tel(t, "lien-tel") for t in UZES["tel"])
    corps = bandeau("Rendez-vous", "Prendre <em>rendez-vous</em>.",
                    "Trois questions pour vous orienter, puis le bon numéro. Aucune information de santé n'est demandée ni enregistrée.",
                    [(None, "Rendez-vous")])
    corps += f'''<section class="plan plan--clair bloc"><div class="contenu rdv">
  <div class="orienteur" data-orienteur>
    <ol class="orienteur__pas" aria-label="Étapes">
      <li data-pas="1" aria-current="step"><span class="repere">01</span>Votre motif</li>
      <li data-pas="2"><span class="repere">02</span>Votre chirurgien</li>
      <li data-pas="3"><span class="repere">03</span>Le lieu</li></ol>
    <div class="orienteur__etape" data-etape="1">
      <h2 class="titre-m" tabindex="-1">Pour quel domaine consultez-vous ?</h2>
      <ul class="choix-liste">{options}
        <li><button class="choix choix--neutre" type="button" data-domaine="">Je ne sais pas, ou j'ai déjà un chirurgien</button></li></ul>
    </div>
    <div class="orienteur__etape" data-etape="2" hidden>
      <h2 class="titre-m" tabindex="-1">Avec qui souhaitez-vous consulter ?</h2>
      <p class="note" data-orientation></p>
      <ul class="choix-liste choix-liste--photos" data-chirurgiens></ul>
      <button class="lien-retour" type="button" data-retour="1">Modifier le motif</button>
    </div>
    <div class="orienteur__etape" data-etape="3" hidden>
      <h2 class="titre-m" tabindex="-1">Où souhaitez-vous consulter ?</h2>
      <ul class="choix-liste" data-lieux></ul>
      <button class="lien-retour" type="button" data-retour="2">Modifier le chirurgien</button>
    </div>
    <div class="orienteur__etape orienteur__resultat" data-etape="4" hidden>
      <h2 class="titre-m" tabindex="-1">Votre rendez-vous</h2>
      <div data-resultat></div>
      <button class="lien-retour" type="button" data-retour="1">Recommencer</button>
    </div>
    {provisoire("Orientation indicative, proposée d'après les spécialités affichées : le secrétariat confirme le chirurgien")}
  </div>
  <aside class="rdv__direct" aria-label="Contact direct">
    <h2 class="repere">Contact direct</h2>
    <div class="rdv__ligne"><h3>Par téléphone</h3><p>{lien_tel(C["telephone_affiche"], "rdv__numero")}</p><p class="note">{e(C["horaires_affiches"])}</p></div>
    <div class="rdv__ligne"><h3>En ligne</h3><p><a class="lien-fleche" href="{e(C["rdv_en_ligne"])}" target="_blank" rel="noopener">{e(C["rdv_en_ligne_libelle"])}<span class="visuellement-cache"> (nouvel onglet)</span></a></p>
      <p class="note">◇ Lien général : les liens directs par chirurgien seront fournis par le cabinet.</p></div>
    <div class="rdv__ligne"><h3>À Uzès</h3><p>{tels_uzes}</p><p class="note">{e(UZES["creneau"])} · {e(UZES["horaires_tel"])}</p></div>
    <div class="rdv__ligne"><h3>Avant de venir</h3><p><a class="lien-fleche" href="{u("/preparer/")}">Les documents à apporter</a></p></div>
    <div class="rdv__ligne rdv__ligne--urgence"><h3>Urgence</h3><p>{e(C["urgences_nom"])} : {lien_tel(C["urgences_tel"], "lien-tel")}</p><p class="note">Urgence vitale : composez le 15.</p></div>
  </aside>
</div></section>'''
    return ("/rendez-vous/", page(
        chemin="/rendez-vous/", titre="Prendre rendez-vous — Nemaudig, chirurgie digestive à Nîmes",
        description="Prendre rendez-vous avec un chirurgien digestif du cabinet Nemaudig à Nîmes ou à Uzès : par téléphone au 04 66 05 24 63 ou en ligne.",
        corps=corps, scripts=("orienteur.js",), donnees=donnees, classe="page-rdv"))


def pages():
    return [_preparer(), _prevention(), _centres(), _rdv()]
