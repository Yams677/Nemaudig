"""Actualités, vidéos, FAQ, pages légales, charte graphique, 404, plan du site."""

import re

import config
from data.cabinet import ACTUALITES, SITES_UTILES
from data.pathologies import FAM, PATHOLOGIES
from data.videos import ORDRE, VIDEOS
from lib.anatomie import planche
from lib.composants import bandeau_rdv, faq, schema_faq, tete_page, video
from lib.html import C, ICONES, bouton, e, surtitre
from lib.layout import page

REDIRECTIONS = {"actualite": "/actualites/", "actualites": "/actualites/", "actualites-nemaudig": "/actualites/", "videos": "/videos/",
                "faq": "/faq/", "foire-au-questions": "/faq/", "mentions-legales-71": "/mentions-legales/",
                "politique-de-confidentialite": "/confidentialite/", "gestion-des-cookies": "/confidentialite/", "plan-du-site": "/plan-du-site/",
                "home": "/"}


def page_actus(assets):
    items = "".join(f'''<article class="actu" id="{a["slug"]}" data-reveal>
  <p class="actu__meta"><span class="pastille pastille--menthe">{e(a["categorie"])}</span><time datetime="{a["date"][:7]}">{e(a["date_txt"])}</time></p>
  <h2 style="font-size:1.6rem">{e(a["titre"])}</h2><p>{e(a["texte"])}</p>
  {f'<p><a class="lien-fleche" href="{a["lien"]}">En savoir plus {ICONES["fleche"]}</a></p>' if a["lien"] else ""}
</article>''' for a in ACTUALITES)
    corps = tete_page("Actualités <em>du cabinet</em>", "Nouvelles techniques, nouveaux lieux de consultation, vie de l'équipe.", "Actualités", "var(--ciel)") + \
        f'<section class="section section--serree"><div class="conteneur conteneur--etroit"><div class="actus" style="grid-template-columns:1fr">{items}</div></div></section>' + bandeau_rdv()
    return page(assets, "/actualites/", "Actualités — Nemaudig, chirurgiens digestifs à Nîmes",
                "Ballon intragastrique Allurion, cœlioscopie 3D aux Franciscaines, kyste pilonidal au laser, consultation à Uzès : les actualités du cabinet Nemaudig.",
                corps, fil=[("/actualites/", "Actualités")])


def page_videos(assets):
    vids = "".join(f'<div data-reveal style="--d:{i % 3}">{video(k)}</div>' for i, k in enumerate(ORDRE))
    corps = tete_page("Des interventions <em>filmées par l'équipe</em>",
                      "Pour comprendre concrètement le déroulement d'une opération. Les vidéos sont hébergées sur YouTube et ne se chargent que si vous les lancez.",
                      "Vidéothèque", "var(--lilas)") + f'''
<section class="section section--serree"><div class="conteneur"><div class="grille grille--3">{vids}</div>
<p class="petit mt-6">Certaines images montrent l'intérieur du corps pendant une opération.</p></div></section>''' + bandeau_rdv()
    return page(assets, "/videos/", "Vidéos d'interventions chirurgicales — Nemaudig, Nîmes",
                "Robot Da Vinci, hernie inguinale par cœlioscopie, bypass gastrique, chirurgie du rectum : les interventions filmées par les chirurgiens de Nemaudig.",
                corps, fil=[("/videos/", "Vidéos")])


def page_faq(assets):
    blocs, toutes = [], []
    for p in PATHOLOGIES:
        if not p["faq"]:
            continue
        toutes += p["faq"]
        blocs.append(f'''<section class="bloc-section" aria-labelledby="faq-t-{p["slug"]}"><h2 id="faq-t-{p["slug"]}" style="font-size:1.6rem"><a href="/pathologies/{p["slug"]}/" style="text-decoration:none">{e(p["court"])}</a></h2>
{faq(p["faq"], "faq-" + p["slug"])}</section>''')
    corps = tete_page("Une question&nbsp;? <em>Nous vous répondons.</em>",
                      "Les réponses de l'équipe aux questions les plus fréquentes, classées par intervention. Pour votre situation personnelle, parlez-en avec votre chirurgien.",
                      "Questions fréquentes", "var(--menthe)") + f'<section class="section section--serree"><div class="conteneur conteneur--etroit">{"".join(blocs)}</div></section>' + bandeau_rdv()
    return page(assets, "/faq/", "Questions fréquentes — chirurgie digestive à Nîmes",
                "Régime après ablation de la vésicule, reprise du sport après une hernie, purge avant chirurgie du côlon, cicatrisation : les réponses des chirurgiens de Nemaudig.",
                corps, fil=[("/faq/", "Questions fréquentes")], schemas=[schema_faq(toutes)])


def page_mentions(assets):
    M = config.MENTIONS
    a = C["adresse"]
    corps = tete_page("Mentions légales", None, "Informations légales", "var(--ivoire-2)") + f'''
<section class="section section--serree"><div class="conteneur conteneur--etroit prose">
<h2>Éditeur</h2><p>{e(M["raison_sociale"])} — {e(config.CABINET["statut"])}<br>{e(a["rue"])}, {a["code_postal"]} {e(a["ville"])}<br>SIREN : {e(M["siren"])}<br>Contact : <a href="mailto:{C["email"]}">{C["email"]}</a> · {C["telephone_affiche"]}</p>
<h2>Directeur de la publication</h2><p>{e(M["directeur_publication"])}</p>
<h2>Hébergement</h2><p>{e(M["hebergeur"])}</p>
<h2>Propriété intellectuelle</h2><p>Les textes, illustrations et visuels de ce site sont la propriété de Nemaudig et/ou de leurs détenteurs respectifs. Les fiches d'information patient au format PDF sont © Fédération de chirurgie viscérale et digestive. Toute reproduction sans autorisation est interdite.</p>
<h2>Informations médicales</h2><p>Les informations de ce site sont générales. Elles ne remplacent pas une consultation et ne permettent pas d'établir un diagnostic. En cas d'urgence vitale, composez le 15.</p>
{'<p class="note-a-valider">Mentions à compléter avant mise en ligne : n° RPPS et ordre des médecins de chaque chirurgien, conception du site.</p>' if config.DEMO else ""}
</div></section>'''
    return page(assets, "/mentions-legales/", "Mentions légales — Nemaudig",
                "Mentions légales du site du cabinet Nemaudig, association de chirurgiens digestifs et viscéraux à Nîmes : éditeur, hébergement, propriété intellectuelle.",
                corps, fil=[("/mentions-legales/", "Mentions légales")], indexer=False)


def page_confidentialite(assets):
    corps = tete_page("Confidentialité <em>et cookies</em>", None, "Vos données", "var(--ivoire-2)") + f'''
<section class="section section--serree"><div class="conteneur conteneur--etroit prose">
<h2>Aucun cookie de suivi</h2><p>Ce site ne dépose aucun cookie publicitaire ni de mesure d'audience. Aucun bandeau de consentement n'est donc nécessaire.</p>
<h2>Vidéos YouTube</h2><p>Les vidéos ne sont chargées qu'au moment où vous cliquez dessus, depuis le domaine youtube-nocookie.com. Avant ce clic, seule une image d'aperçu est affichée.</p>
<h2>Aucune donnée de santé collectée</h2><p>Le site ne comporte aucun formulaire : aucune donnée personnelle ni de santé n'y est saisie. Les rendez-vous se prennent par téléphone ou sur la plateforme Maiia, soumise à sa propre politique de confidentialité.</p>
<h2>Calculateur d'IMC</h2><p>Le calcul est effectué dans votre navigateur ; les valeurs saisies ne sont ni transmises ni conservées.</p>
<h2>Vos droits</h2><p>Pour toute question relative à vos données : Nemaudig, {e(C["adresse"]["rue"])}, {C["adresse"]["code_postal"]} Nîmes — <a href="mailto:{C["email"]}">{C["email"]}</a>.</p>
</div></section>'''
    return page(assets, "/confidentialite/", "Confidentialité et cookies — Nemaudig",
                "Politique de confidentialité du site Nemaudig : aucun cookie de suivi, vidéos chargées au clic, aucune donnée de santé collectée en ligne.",
                corps, fil=[("/confidentialite/", "Confidentialité")], indexer=False)


def page_404(assets):
    corps = f'''<section class="section"><div class="conteneur conteneur--etroit centre">
  <div style="max-width:200px;margin:0 auto 24px">{planche(actif="estomac", ident="planche-404", classe="a-un-actif")}</div>
  {surtitre("Erreur 404")}<h1>Cette page <em>est introuvable.</em></h1>
  <p class="chapo" style="margin-inline:auto">Le site de Nemaudig a fait peau neuve : certaines adresses ont changé.</p>
  <div class="actions" style="justify-content:center">{bouton("/", "Retour à l'accueil", "plein")}{bouton("/pathologies/", "Les pathologies", "ligne")}</div>
</div></section>'''
    return page(assets, "/404.html", "Page introuvable — Nemaudig", "La page demandée n'existe pas ou a changé d'adresse. Retrouvez les pathologies, les chirurgiens et la prise de rendez-vous.",
                corps, indexer=False)


def page_charte(assets):
    teintes = [("Ivoire", "--ivoire", "#F6F4EE", "Fond de page"), ("Encre", "--encre", "#0E2230", "Texte, sections sombres"),
               ("Lagon", "--lagon", "#0B6A66", "Action principale · 6,1:1 sur blanc"), ("Lagon vif", "--lagon-vif", "#2BB3A7", "Lueurs, accents"),
               ("Menthe", "--menthe", "#DCF1EA", "Côlon, rassurance"), ("Ciel", "--ciel", "#DDEAF6", "Information"),
               ("Lilas", "--lilas", "#E8E3F5", "Estomac, cancérologie"), ("Pêche", "--peche", "#FBE5DA", "Foie, alertes douces"),
               ("Sable", "--sable", "#F4EAD6", "Obésité"), ("Rose", "--rose", "#F7DCE2", "Proctologie"), ("Nuit", "--nuit", "#0A1A26", "Technologie, pied de page")]
    nuancier = "".join(f'<div class="teinte"><i style="background:var({v})"></i><p><strong>{n}</strong><br><code>{h}</code><br>{e(u)}</p></div>' for n, v, h, u in teintes)
    icos = "".join(f'<div class="spec" style="display:grid;place-items:center;gap:6px;text-align:center">{ICONES[k]}<span>{k}</span></div>' for k in ICONES)
    organes = "".join(f'<div class="encart" style="padding:12px">{planche(actif=o, ident="ch-" + o, classe="a-un-actif")}<p class="petit centre mb-0">{o}</p></div>'
                      for o in ["oesophage", "estomac", "foie", "pancreas", "colon", "rectum", "anus", "paroi", "surrenales", "peau"])
    corps = tete_page("Charte <em>graphique</em>", "Le système visuel du nouveau site : couleurs, typographies, composants, iconographie et planches anatomiques.", "Design system", "var(--lilas)") + f'''
<section class="section section--serree"><div class="conteneur">
  <h2>Couleurs</h2><p class="chapo">Une base ivoire chaleureuse, un lagon profond pour l'action, et des pastels médicaux : chacun signe une région du corps.</p>
  <div class="nuancier mt-6">{nuancier}</div>
  <h2 class="mt-7">Typographies</h2>
  <div class="grille grille--2">
    <div class="encart"><p class="surtitre">Titres · Fraunces</p><p style="font:300 4rem/1 var(--t-titre)">Aa <em style="color:var(--lagon)">Aa</em></p><p>Une serif « old style » à axe optique : l'autorité de l'édition médicale, la douceur d'un accueil. Italique en couleur pour l'émotion.</p></div>
    <div class="encart"><p class="surtitre">Texte · Hanken Grotesk</p><p style="font:500 4rem/1 var(--t-texte)">Aa</p><p>Une grotesque claire et généreuse, lisible dès 16 px, pour les explications médicales.</p></div>
  </div>
  <h2 class="mt-7">Boutons et liens</h2>
  <div class="actions">{bouton("#", "Prendre rendez-vous", "plein", icone="agenda")}{bouton("#", "Action secondaire", "ligne")}<a class="lien-fleche" href="#">Lien fléché {ICONES["fleche"]}</a>
  <span class="pastille pastille--menthe">Pastille</span><span class="pastille pastille--lilas">Cancérologie</span><span class="pastille pastille--peche">Restrictive</span></div>
  <div class="section--nuit mt-6" style="padding:24px;border-radius:var(--r-l)"><div class="actions">{bouton("#", "Sur fond sombre", "clair")}{bouton("#", "Contour clair", "ligne-clair")}</div></div>
  <h2 class="mt-7">Planches anatomiques</h2><p class="chapo">Un seul dessin, vue de face (droite du patient à gauche), décliné pour chaque fiche : l'organe concerné s'allume, le reste s'efface.</p>
  <div class="grille grille--4 mt-6" style="grid-template-columns:repeat(auto-fill,minmax(150px,1fr))">{organes}</div>
  <h2 class="mt-7">Icônes</h2><p class="chapo">Trait 1,6 px, angles arrondis, couleur héritée.</p>
  <div class="grille mt-6" style="grid-template-columns:repeat(auto-fill,minmax(110px,1fr))">{icos}</div>
  <h2 class="mt-7">Mouvement</h2>
  <ul class="liste"><li>Tracé progressif des organes à l'arrivée sur l'accueil, puis balayage lumineux type « scanner »</li><li>Apparition douce des blocs au défilement (26 px, 0,9 s, courbe ease-out)</li><li>Survol : élévation de 4 px et ombre portée ; la planche et les cartes se répondent</li><li>Tout mouvement est désactivé si l'utilisateur a demandé à réduire les animations</li></ul>
  <h2 class="mt-7">Direction photographique</h2>
  <ul class="liste"><li>Portraits des cinq chirurgiens : même fond ivoire, lumière naturelle latérale, tenue de ville ou blouse, regard caméra, cadrage poitrine 4:5</li><li>Le cabinet et les blocs : lumière douce, teintes froides désaturées, aucun sang ni geste opératoire en gros plan</li><li>Pas de photos de banque d'images d'inconnus en blouse : uniquement l'équipe et les lieux réels</li></ul>
</div></section>'''
    return page(assets, "/charte/", "Charte graphique — Nemaudig", "Design system du site Nemaudig : palette pastel médicale, typographies Fraunces et Hanken Grotesk, composants, planches anatomiques et icônes.",
                corps, fil=[("/charte/", "Charte graphique")], indexer=False)


def plan_du_site(assets, pages):
    def titre(html):
        t = re.search(r"<title>(.*?)</title>", html).group(1)
        return t.split(" — ")[0]
    groupes = {}
    for u in sorted(pages):
        if u in ("/404.html", "/charte/"):
            continue
        cle = u.strip("/").split("/")[0] or "accueil"
        groupes.setdefault(cle, []).append(u)
    blocs = "".join(f'<div class="encart"><ul class="encart__liste">{"".join(f"<li><a href={chr(34)}{u}{chr(34)}><span>{titre(pages[u])}</span></a></li>" for u in us)}</ul></div>'
                    for us in groupes.values())
    corps = tete_page("Plan du site", None, "Navigation", "var(--ivoire-2)") + f'<section class="section section--serree"><div class="conteneur"><div class="grille grille--3">{blocs}</div></div></section>'
    return {"/plan-du-site/": page(assets, "/plan-du-site/", "Plan du site — Nemaudig",
                                   "Toutes les pages du site Nemaudig : pathologies, chirurgiens, chirurgie de l'obésité, techniques, parcours patient et informations pratiques.",
                                   corps, fil=[("/plan-du-site/", "Plan du site")])}


def rendre(assets):
    return {"/actualites/": page_actus(assets), "/videos/": page_videos(assets), "/faq/": page_faq(assets),
            "/mentions-legales/": page_mentions(assets), "/confidentialite/": page_confidentialite(assets),
            "/404.html": page_404(assets), "/charte/": page_charte(assets)}
