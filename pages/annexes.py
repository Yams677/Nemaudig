"""Mentions légales, confidentialité, page « À propos de la maquette », page 404."""
import config
from lib.gabarit import C, bandeau, e, liste, page, sur_titre, u

M = config.MENTIONS


def _mentions():
    ad = C["adresse"]
    corps = bandeau("Informations légales", "Mentions légales", "Éditeur du site, hébergement, propriété intellectuelle.", [(None, "Mentions légales")])
    corps += f'''<section class="plan plan--clair bloc"><div class="contenu etroit prose">
  <h2>Éditeur</h2><p>{e(M["raison_sociale"])} — {e(C["statut"])}<br>{e(ad["rue"])}, {e(ad["complement"])}, {e(ad["code_postal"])} {e(ad["ville"])}<br>
    SIREN {e(M["siren"])} · {e(C["telephone_affiche"])} · {e(C["email"])}</p>
  <p>Directeur de la publication : {e(M["directeur_publication"])}.</p>
  <p class="provisoire"><span aria-hidden="true">◇</span> Numéros RPPS et inscriptions à l'Ordre des médecins de chaque praticien : à compléter.</p>
  <h2>Hébergement</h2><p>{e(M["hebergeur"])}.</p>
  <h2>Information médicale</h2><p>Les informations de ce site sont destinées à améliorer, et non à remplacer, la relation entre le patient et son médecin. Elles ne constituent ni un diagnostic ni une prescription. Le site ne comporte aucune publicité et n'est financé par aucun tiers.</p>
  <h2>Crédits</h2><p>{e(config.CREDIT_IMAGES)}. Polices Outfit, Geist et Geist Mono (licence SIL Open Font).</p>
</div></section>'''
    return ("/mentions-legales/", page(chemin="/mentions-legales/", titre="Mentions légales — Nemaudig",
                                       description="Mentions légales du site du cabinet Nemaudig, chirurgie digestive et viscérale à Nîmes.", corps=corps))


def _confidentialite():
    corps = bandeau("Vos données", "Confidentialité", "Ce site a été conçu pour ne collecter aucune donnée personnelle.", [(None, "Confidentialité")])
    corps += f'''<section class="plan plan--clair bloc"><div class="contenu etroit prose">
  <h2>Aucun cookie, aucun traceur</h2><p>Le site ne dépose aucun cookie et n'utilise aucun outil de mesure d'audience ni aucun service publicitaire. C'est pourquoi aucun bandeau de consentement ne s'affiche.</p>
  <h2>Aucun formulaire</h2><p>Le site ne comporte aucun formulaire : aucune information de santé ne transite par lui. L'aide à l'orientation de la page « Rendez-vous », la recherche dans les questions et la liste de documents fonctionnent uniquement dans votre navigateur ; rien n'est transmis ni conservé.</p>
  <h2>Services extérieurs</h2><p>La prise de rendez-vous en ligne s'effectue sur la plateforme {e(C["rdv_en_ligne_libelle"])}, qui applique sa propre politique de confidentialité. La carte OpenStreetMap n'est chargée que si vous le demandez. Les polices et les modèles 3D sont hébergés sur le site lui-même.</p>
  <h2>Vos droits</h2><p>Pour toute question relative à vos données personnelles ou à votre dossier médical, adressez-vous au secrétariat du cabinet : {e(C["telephone_affiche"])} — {e(C["email"])}.</p>
</div></section>'''
    return ("/confidentialite/", page(chemin="/confidentialite/", titre="Confidentialité — Nemaudig",
                                      description="Politique de confidentialité : le site du cabinet Nemaudig ne collecte aucune donnée personnelle, sans cookie ni traceur.", corps=corps))


def _maquette():
    apports = [
        ("Votre image professionnelle", "Une identité visuelle à la hauteur du plateau technique : robot, cœlioscopie 3D, laser."),
        ("Votre visibilité", "Une page par pathologie et par praticien, structurée pour les moteurs de recherche, à Nîmes et à Uzès."),
        ("Une information de qualité", "Vos fiches actuelles, réorganisées, complétées par un explorateur anatomique et des schémas animés."),
        ("Une expérience moderne", "Un modèle 3D réel, fluide sur ordinateur comme sur téléphone, sans rien installer."),
        ("Un accès simplifié", "Le rendez-vous à portée de main sur chaque écran ; une orientation en trois questions."),
        ("Chaque praticien mis en valeur", "Parcours, diplômes, domaines et lieux d'exercice sur une fiche personnelle."),
        ("Un outil qui évolue", "Actualités, nouvelles techniques, vidéos : le site se met à jour au rythme du cabinet."),
    ]
    reste = [
        "Relecture médicale des fiches d'organes, des fiches d'examens et des conseils de prévention",
        "Validation des attributions chirurgien ↔ domaine",
        "Liens de prise de rendez-vous en ligne propres à chaque chirurgien",
        "Production puis validation des cinq vidéos (storyboards et prompts prêts)",
        "Photographies des locaux et de l'équipe paramédicale",
        "Confirmation des honoraires, numéros RPPS, hébergeur",
    ]
    corps = bandeau("Démonstration", "Ce que ce site <em>apporte au cabinet</em>.",
                    "Une proposition de nouveau site pour Nemaudig, construite à partir des contenus de votre site actuel.", [(None, "À propos de la maquette")])
    corps += f'''<section class="plan plan--clair bloc"><div class="contenu">
  <ul class="engagements engagements--3">{"".join(f"<li><h2>{e(t)}</h2><p>{e(d)}</p></li>" for t, d in apports)}</ul>
</div></section>
<section class="plan plan--clair bloc bloc--serre"><div class="contenu deux-colonnes">
  <div>{sur_titre("Avant la mise en ligne")}<h2 class="titre-l">Ce qu'il reste à valider ensemble.</h2>
    <p>Rien n'a été inventé : les éléments qui ne viennent pas de votre site actuel sont signalés par le symbole ◇ sur chaque page.</p></div>
  <div class="prose">{liste(reste, "liste liste--losange")}
    <a class="lien-fleche" href="{u("/")}">Revenir à l'accueil</a></div>
</div></section>'''
    return ("/maquette/", page(chemin="/maquette/", titre="À propos de cette maquette — Nemaudig",
                               description="Présentation de la maquette du nouveau site du cabinet Nemaudig : apports, éléments réels et éléments provisoires.", corps=corps))


def _introuvable():
    corps = bandeau("Erreur 404", "Cette page n'existe pas.", "L'adresse a peut-être changé. Retrouvez votre chemin depuis l'accueil.",
                    [(None, "Page introuvable")], f'<div class="actions"><a class="btn" href="{u("/")}">Retour à l\'accueil</a></div>')
    return ("/404.html", page(chemin="/404.html", titre="Page introuvable — Nemaudig", description="Page introuvable.", corps=corps))


def pages():
    return [_mentions(), _confidentialite(), _maquette(), _introuvable()]
