"""Chirurgie de l'obésité : hub + techniques + parcours + suivi."""

import config
from data import obesite as O
from lib.composants import bandeau_rdv, mini_medecin, tete_page, video
from lib.html import ICONES, bouton, e, riche, surtitre
from lib.layout import page
from pages.pathologies import ancre

REDIRECTIONS = {"chirurgie-bariatrique-obesite": "/obesite/", "techniques": "/obesite/#techniques", "points-importants": "/obesite/",
                "principes": "/obesite/", "parcours-pre-operatoire": "/obesite/parcours/", "suivi-post-operatoire-86": "/obesite/suivi/"}
REDIRECTIONS.update({t["ancien"]: f"/obesite/{t['slug']}/" for t in O.TECHNIQUES})

FIL = ("/obesite/", "Obésité")


def calculateur():
    jauge = "".join("<span></span>" for _ in O.IMC)
    legende = "".join(f"<span>{e(l)}</span>" for *_, l in O.IMC)
    return f'''<div class="imc" data-imc data-reveal>
  <div>
    {surtitre("Calculer son IMC")}
    <h2 style="font-size:2rem">Où vous situez-vous&nbsp;?</h2>
    <p class="petit">IMC = poids (kg) / taille (m)². Le calcul se fait dans votre navigateur : rien n'est envoyé.</p>
    <div class="imc__champs mt-4">
      <div class="champ"><label for="imc-poids">Poids (kg)</label><input id="imc-poids" inputmode="decimal" autocomplete="off" placeholder="95"></div>
      <div class="champ"><label for="imc-taille">Taille (cm)</label><input id="imc-taille" inputmode="decimal" autocomplete="off" placeholder="170"></div>
    </div>
  </div>
  <div aria-live="polite">
    <p class="petit mb-0">Votre IMC</p>
    <p class="imc__resultat" data-imc-valeur>—</p>
    <p class="imc__classe" data-imc-classe></p>
    <div class="imc__jauge" aria-hidden="true">{jauge}<i class="imc__curseur" data-imc-curseur></i></div>
    <div class="imc__legende" aria-hidden="true">{legende}</div>
    <p class="petit mt-4 mb-0">{e(O.CANDIDAT)}</p>
  </div>
</div>'''


def carte_tech(t, i):
    chiffres = "".join(f"<li><strong>{e(v)}</strong> {e(l)}</li>" for v, l in t["chiffres"][:2])
    return f'''<a class="carte" href="/obesite/{t["slug"]}/" data-reveal style="--d:{i}">
  <span class="pastille {"pastille--menthe" if i == 0 else "pastille--peche"}">{e(t["type"])}</span>
  <h3 class="mt-4">{e(t["titre"])}</h3><p>{e(t["resume"])}</p>
  <ul class="liste petit mt-4" style="margin-bottom:0">{chiffres}</ul>
  <span class="carte__pied lien-fleche">Principe, résultats, suivi {ICONES["fleche"]}</span>
</a>'''


def page_hub(assets):
    techs = "".join(carte_tech(t, i) for i, t in enumerate(O.TECHNIQUES))
    causes = "".join(f'<div class="spec"><strong>{e(t)}</strong>{f"<span>{e(", ".join(l))}</span>" if l else ""}</div>' for t, l in O.CAUSES)
    conseq = "".join(f'<li class="pastille">{e(c)}</li>' for c in O.CONSEQUENCES)
    corps = tete_page("Chirurgie de l'obésité <em>à Nîmes</em>",
                      "Un parcours pluridisciplinaire, du ballon intragastrique sans chirurgie à la sleeve et au bypass — dans des locaux spécialement conçus pour accueillir les patients en situation d'obésité.",
                      "Chirurgie bariatrique", "var(--sable)", organe="estomac") + f'''
<section class="section section--serree"><div class="conteneur">{calculateur()}</div></section>
<section class="section section--serree" id="techniques" aria-labelledby="t-titre"><div class="conteneur">
  <div class="section__tete section__tete--2"><div>{surtitre("Les techniques", "01")}<h2 id="t-titre">Quatre solutions, <em>un choix collégial.</em></h2></div>
  <p class="chapo">Le type d'intervention est discuté en équipe pluridisciplinaire selon votre âge, vos maladies et antécédents, votre IMC, votre mode de vie et votre désir de grossesse.</p></div>
  <div class="grille grille--4">{techs}</div>
</div></section>
<section class="section section--blanc" aria-labelledby="p-titre"><div class="conteneur">
  <div class="section__tete section__tete--2"><div>{surtitre("Comprendre", "02")}<h2 id="p-titre">L'obésité, <em>une maladie chronique.</em></h2></div>
  <p class="chapo">{e(O.DEFINITION)}</p></div>
  <h3>Une maladie multifactorielle</h3><div class="specs mt-4">{causes}</div>
  <h3 class="mt-7">Ses conséquences sur la santé</h3><ul class="pastilles mt-4">{conseq}</ul>
</div></section>
<section class="section" aria-labelledby="pa-titre"><div class="conteneur">
  <div class="section__tete section__tete--2"><div>{surtitre("Votre parcours", "03")}<h2 id="pa-titre">Au moins six mois <em>de préparation.</em></h2></div>
  <p class="chapo">Une phase indispensable qui demande un véritable engagement : vous rencontrez les professionnels de l'équipe pluridisciplinaire, puis votre dossier est discuté collégialement.</p></div>
  <div class="grille grille--2">
    <a class="carte" href="/obesite/parcours/"><span class="carte__ico">{ICONES["equipe"]}</span><h3>Le parcours avant l'opération</h3><p>Les spécialistes rencontrés, les examens, la décision collégiale.</p><span class="carte__pied lien-fleche">Le détail {ICONES["fleche"]}</span></a>
    <a class="carte" href="/obesite/suivi/"><span class="carte__ico">{ICONES["coeur"]}</span><h3>Le suivi après l'opération</h3><p>Alimentation, activité physique, consultations : un suivi à vie.</p><span class="carte__pied lien-fleche">Le détail {ICONES["fleche"]}</span></a>
  </div>
  <div class="encart mt-6" style="max-width:560px"><h2>Votre chirurgienne</h2>{mini_medecin("dr-fanelly-torres")}</div>
</div></section>''' + bandeau_rdv("Faire le point sur votre situation", "Le secrétariat vous oriente et vous indique, pour le ballon intragastrique, si vous êtes éligible.")
    return page(assets, "/obesite/", "Chirurgie de l'obésité à Nîmes — sleeve, bypass, ballon",
                "Chirurgie bariatrique à Nîmes : ballon intragastrique Allurion, sleeve gastrectomie, bypass, anneau. Calcul d'IMC, parcours pluridisciplinaire et suivi.",
                corps, fil=[FIL])


def page_tech(assets, t):
    url = f"/obesite/{t['slug']}/"
    chiffres = "".join(f'<div class="chiffre"><strong>{e(v)}</strong><span>{e(l)}</span></div>' for v, l in t["chiffres"])
    sommaire = "".join(f'<li><a href="#{ancre(s)}">{e(s)}</a></li>' for s, _ in t["sections"])
    blocs = "".join(f'<section class="bloc-section"><div class="bloc-section__tete"><span class="bloc-section__num">{i + 1:02d}</span><h2 id="{ancre(s)}">{e(s)}</h2></div>{riche(x)}</section>'
                    for i, (s, x) in enumerate(t["sections"]))
    if t["video"]:
        blocs += f'<section class="bloc-section"><h2>En vidéo</h2>{video(t["video"])}</section>'
    if t["liens"]:
        blocs += '<section class="bloc-section"><h2>Pour aller plus loin</h2><ul class="liste">' + "".join(
            f'<li><a href="{u}" target="_blank" rel="noopener">{e(l)}</a></li>' for l, u in t["liens"]) + "</ul></section>"
    autres = "".join(f'<li><a href="/obesite/{x["slug"]}/"><span>{e(x["titre"])}</span>{ICONES["fleche"]}</a></li>' for x in O.TECHNIQUES if x is not t)
    corps = tete_page(e(t["titre"]), e(t["resume"]), "Chirurgie de l'obésité", "var(--sable)", organe="estomac",
                      meta_html=f'<span class="pastille pastille--peche">{e(t["type"])}</span>') + f'''
<section class="section section--serree" style="padding-top:0"><div class="conteneur"><div class="chiffres" data-reveal>{chiffres}</div></div></section>
<section class="section section--serree" style="padding-top:24px"><div class="conteneur"><div class="article">
  <nav class="sommaire" aria-label="Sommaire" data-sommaire><p>Sur cette page</p><ol>{sommaire}</ol></nav>
  <div class="prose">{blocs}</div>
  <aside class="aside">
    <div class="encart encart--lagon"><h2>En parler en consultation</h2><p>Chaque situation est évaluée par l'équipe pluridisciplinaire.</p>
      <a class="btn btn--clair" href="/contact/">{ICONES["agenda"]}<span>Prendre rendez-vous</span><span class="btn__fleche" aria-hidden="true">{ICONES["fleche"]}</span></a></div>
    <div class="encart">{mini_medecin("dr-fanelly-torres")}</div>
    <div class="encart"><h2>Les autres techniques</h2><ul class="encart__liste">{autres}</ul></div>
  </aside>
</div></div></section>''' + bandeau_rdv()
    schema = {"@context": "https://schema.org", "@type": "MedicalWebPage", "name": t["titre"], "url": f"{config.SITE_URL}{url}",
              "inLanguage": "fr-FR", "about": {"@type": "MedicalProcedure", "name": t["titre"]}, "publisher": {"@id": f"{config.SITE_URL}/#cabinet"}}
    return page(assets, url, f"{t['titre']} à Nîmes — chirurgie de l'obésité", t["desc"], corps,
                fil=[FIL, (url, t["court"])], schemas=[schema])


def page_parcours(assets):
    pros = "".join(f'<li class="etape" data-reveal style="--d:{i % 3}" data-etape><h3>{e(t)}</h3><p>{e(d)}</p></li>' for i, (t, d) in enumerate(O.PREPARATION))
    decision = "".join(f"<li>{e(d)}</li>" for d in O.DECISION)
    corps = tete_page("Le parcours <em>avant l'opération</em>",
                      "Cette phase de préparation est indispensable et nécessite un véritable engagement de votre part : au minimum six mois, pendant lesquels vous rencontrez les professionnels de l'équipe pluridisciplinaire.",
                      "Chirurgie de l'obésité", "var(--sable)") + f'''
<section class="section section--serree"><div class="conteneur conteneur--etroit">
  <h2>Les professionnels rencontrés</h2>
  <ol class="parcours" style="grid-template-columns:1fr">{pros}</ol>
  <div class="encart encart--menthe mt-6"><p class="mb-0">{e(O.ESTIM)}</p></div>
  <h2 class="mt-7">La décision</h2>
  <ul class="liste">{decision}</ul>
  <p class="mt-6"><a class="lien-fleche" href="/obesite/suivi/">Le suivi après l'opération {ICONES["fleche"]}</a></p>
</div></section>''' + bandeau_rdv()
    return page(assets, "/obesite/parcours/", "Parcours avant une chirurgie de l'obésité — Nîmes",
                "Avant une chirurgie bariatrique à Nîmes : six mois de préparation, nutritionniste, diététicienne, psychologue, examens, puis décision collégiale de l'équipe.",
                corps, fil=[FIL, ("/obesite/parcours/", "Parcours avant l'opération")])


def page_suivi(assets):
    ali = "".join(f"<li>{e(x)}</li>" for x in O.SUIVI_ALIMENTATION)
    act = "".join(f"<li>{e(x)}</li>" for x in O.SUIVI_ACTIVITE)
    cons = "".join(f"<tr><td>{e(q)}</td><td style='font:inherit;white-space:normal'>{e(r)}</td></tr>" for q, r in O.SUIVI_CONSULTATIONS)
    corps = tete_page("Le suivi <em>après l'opération</em>",
                      "À la sortie, les modalités du suivi vous sont expliquées et les rendez-vous sont pris. Ces nouvelles habitudes sont parfois contraignantes, mais elles n'empêchent ni la vie sociale ni le plaisir de manger.",
                      "Chirurgie de l'obésité", "var(--sable)") + f'''
<section class="section section--serree"><div class="conteneur">
  <div class="grille grille--2" style="align-items:start">
    <div class="encart" data-reveal><span class="carte__ico">{ICONES["coeur"]}</span><h2>Sur le plan alimentaire</h2><p>L'alimentation à domicile (fractionnée, moulinée, et pour combien de temps) vous est précisée avant la sortie par la diététicienne de la clinique.</p><ul class="liste">{ali}</ul></div>
    <div class="encart" data-reveal style="--d:1"><span class="carte__ico">{ICONES["pulse"]}</span><h2>Sur le plan physique</h2><p>Une activité régulière et adaptée est indispensable.</p><ul class="liste">{act}</ul></div>
  </div>
  <h2 class="mt-7">Les consultations, à vie</h2>
  <table class="tableau"><thead><tr><th>Avec</th><th>Rythme</th></tr></thead><tbody>{cons}</tbody></table>
</div></section>''' + bandeau_rdv()
    return page(assets, "/obesite/suivi/", "Suivi après chirurgie de l'obésité — Nemaudig, Nîmes",
                "Après une sleeve ou un bypass à Nîmes : conseils alimentaires, reprise de l'activité physique et calendrier des consultations avec le chirurgien et la diététicienne.",
                corps, fil=[FIL, ("/obesite/suivi/", "Suivi après l'opération")])


def rendre(assets):
    pages = {"/obesite/": page_hub(assets), "/obesite/parcours/": page_parcours(assets), "/obesite/suivi/": page_suivi(assets)}
    for t in O.TECHNIQUES:
        pages[f"/obesite/{t['slug']}/"] = page_tech(assets, t)
    return pages
