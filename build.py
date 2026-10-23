"""
Site B « Exploration intérieure » — maquette de la page d'accueil (proposition alternative au site A).

    PYTHONIOENCODING=utf-8 python build.py      # → dist/index.html

Données copiées du site A (data/), elles-mêmes issues de nemaudig.fr. Rien d'inventé.
Modèles 3D : BodyParts3D, © The Database Center for Life Science, CC BY 4.0.
"""

import json
import shutil
from html import escape
from pathlib import Path

import config
from data.cabinet import ACTUALITES, ETABLISSEMENTS, PARCOURS, UZES
from data.chirurgiens import CHIRURGIENS, nom_complet
from data.orientation import SIGNES
from data.pathologies import PAR_SLUG
from data.voyage import ARRETS, MODELES, SPECIALITE_ARRET, STATIONS

RACINE = Path(__file__).parent
DIST = RACINE / "dist"
C = config.CABINET


def e(t):
    return escape(str(t), quote=True)


def carte_chirurgien(slug):
    if slug is None:
        visages = "".join(f'<img src="/img/{c["slug"]}-400.webp" width="40" height="50" alt="">' for c in CHIRURGIENS)
        return f'''<div class="medecin medecin--equipe"><span class="medecin__visages">{visages}</span>
        <span><strong>L'équipe</strong><small>Vous êtes orienté vers le chirurgien le plus à même de vous prendre en charge</small></span>
        <a class="medecin__rdv" href="#contact" data-rdv="equipe">Rendez-vous</a></div>'''
    c = next(c for c in CHIRURGIENS if c["slug"] == slug)
    return f'''<div class="medecin"><img src="/img/{slug}-400.webp" width="72" height="90" alt="">
        <span><strong>{e(nom_complet(c))}</strong><small>{e(SPECIALITE_ARRET[slug])}</small></span>
        <a class="medecin__rdv" href="#contact" data-rdv="{slug}">Rendez-vous</a></div>'''


def puces_pathologies(st):
    noms = [PAR_SLUG[s]["titre"] for s in st["pathologies"]] + [t for t, _ in st.get("extra", [])]
    return "".join(f"<li>{e(n)}</li>" for n in noms)


# ── Ouverture + voyage (une seule scène épinglée) ─────────────────────────────
def voyage():
    stations = []
    for st in STATIONS:
        arret = ARRETS[st["cle"]]
        n = len(arret["pathos"])
        pathos = "".join(f'''<li class="patho" data-i="{i}">
      <p class="patho__compte">{i + 1:02d} / {n:02d}</p>
      <h4>{e(pa.get("titre") or PAR_SLUG[pa["slug"]]["titre"])}</h4>
      <p>{e(pa["texte"])}</p>
      {carte_chirurgien(pa["chirurgien"])}
    </li>''' for i, pa in enumerate(arret["pathos"]))
        schema = '<p class="station__schema">Représentation schématique</p>' if arret["riche"] else ""
        stations.append(f'''<article class="station{" station--riche" if arret["riche"] else ""}" data-station="{st["cle"]}" aria-labelledby="st-{st["cle"]}">
  <h3 class="station__nom" id="st-{st["cle"]}">{e(st["nom"])}</h3>
  <div class="station__fiche">
    <p class="station__titre">{e(st["titre"])}</p>
    <p>{e(st["texte"])}</p>
    <a class="lien-3d" href="#organes" data-voir="{st["modeles"][0]}"><span class="lien-3d__cube" aria-hidden="true"></span>Voir l'organe en 3D</a>
  </div>
  <ol class="station__pathos" aria-label="Pathologies prises en charge">{pathos}</ol>
  {schema}
</article>''')
    jalons = "".join(f'<li style="--u:{st["u"]}"><span>{e(st["nom"])}</span></li>' for st in STATIONS)
    titre = "Nous connaissons le chemin."
    mots = []
    k = 0
    for m in titre.split(" "):
        lettres = []
        for c in m:
            lettres.append(f'<span style="--i:{k}">{e(c)}</span>')
            k += 1
        mots.append(f'<span class="mot">{"".join(lettres)}</span>')
    return f'''<section class="voyage" id="voyage" aria-label="Voyage à l'intérieur de l'appareil digestif">
  <div class="voyage__scene">
    <canvas class="voyage__canvas" aria-hidden="true"></canvas>
    <div class="voile" aria-hidden="true"></div>
    <div class="ouverture" id="haut">
      <h1 class="ouverture__titre" aria-label="{e(titre)}"><span aria-hidden="true">{" ".join(mots)}</span></h1>
      <div class="ouverture__bas">
        <p class="ouverture__chapo">Cinq chirurgiens digestifs et viscéraux à Nîmes. De l'œsophage au rectum, chaque organe a ses spécificités&nbsp;: entrez, nous vous guidons.</p>
        <div class="ouverture__actions">
          <a class="bouton bouton--lampe" href="#voyage-depart">Commencer le voyage</a>
          <a class="bouton" href="#contact">Prendre rendez-vous</a>
        </div>
      </div>
    </div>
    <div class="stations">{"".join(stations)}</div>
    <div class="rail" aria-hidden="true"><ol>{jalons}</ol><span class="rail__curseur"><span class="rail__pct">000</span></span></div>
  </div>
  <span id="voyage-depart" class="ancre-depart"></span>
</section>'''


def organes():
    boutons = "".join(f'<button type="button" class="organe-choix" data-modele="{k}" aria-pressed="{"true" if k == "foie" else "false"}">{e(nom)}</button>'
                      for k, (nom, _) in MODELES.items())
    fiches = []
    for k, (nom, _) in MODELES.items():
        st = next(s for s in STATIONS if k in s["modeles"])
        fiches.append(f'''<div class="fiche-organe" data-fiche="{k}"{"" if k == "foie" else " hidden"}>
  <h3>{e(nom)}</h3><p>{e(st["texte"])}</p>
  <ul class="pastilles" aria-label="Pathologies prises en charge">{puces_pathologies(st)}</ul>
</div>''')
    return f'''<section class="organes" id="organes" aria-labelledby="organes-t">
  <div class="organes__tete">
    <h2 id="organes-t">Chaque organe,<br><span class="fin">en vrai.</span></h2>
    <p>Des modèles anatomiques reconstruits à partir de l'imagerie d'un corps humain. Faites-les tourner, approchez-vous&nbsp;: la forme que connaît le chirurgien, sans le sang.</p>
  </div>
  <div class="visionneuse">
    <div class="visionneuse__vue">
      <canvas class="visionneuse__canvas" role="img" aria-label="Modèle 3D de l'organe sélectionné. Glissez pour le faire tourner."></canvas>
      <p class="visionneuse__etat" aria-live="polite">Chargement du modèle…</p>
      <p class="visionneuse__geste" aria-hidden="true">Glisser pour tourner</p>
    </div>
    <div class="visionneuse__panneau">
      <div class="choix" role="group" aria-label="Choisir un organe">{boutons}</div>
      {"".join(fiches)}
    </div>
  </div>
</section>'''


def orientation():
    puces = "".join(f'<button type="button" class="signe" data-signe="{k}" aria-pressed="false">{e(t)}</button>' for k, t, _ in SIGNES)
    lectures = []
    for k, t, slugs in SIGNES:
        items = "".join(f'<li><strong>{e(PAR_SLUG[s]["titre"])}</strong><span>{e(PAR_SLUG[s]["resume"])}</span></li>' for s in slugs)
        lectures.append(f'<div class="lecture" data-lecture="{k}" hidden><p class="lecture__signe">{e(t)}</p><ul>{items}</ul></div>')
    return f'''<section class="orientation" id="orientation" aria-labelledby="orientation-t">
  <h2 id="orientation-t">Que ressentez&#8209;vous&nbsp;?</h2>
  <div class="orientation__grille">
    <div class="signes" role="group" aria-label="Signes">{puces}</div>
    <div class="releve" aria-live="polite">
      <div class="lecture lecture--vide" data-lecture="vide"><p>Choisissez ce qui vous ressemble&nbsp;: nous vous indiquons les pathologies prises en charge par l'équipe qui s'en rapprochent.</p></div>
      {"".join(lectures)}
      <p class="avertissement">Ceci n'est pas un diagnostic. Seule une consultation permet de l'établir. En cas d'urgence vitale, composez le 15.</p>
    </div>
  </div>
</section>'''


def equipe():
    cartes = "".join(f'''<figure class="portrait">
  <img src="/img/{c["slug"]}-800.webp" width="800" height="1000" alt="Portrait du {e(nom_complet(c))}" loading="lazy">
  <figcaption><strong>{e(nom_complet(c))}</strong><span>{e(" · ".join(specialites_affichees(c)))}</span>
    <a class="portrait__rdv" href="#contact" data-rdv="{c["slug"]}">Prendre rendez-vous</a></figcaption>
</figure>''' for c in CHIRURGIENS)
    return f'''<section class="equipe" id="equipe" aria-labelledby="equipe-t">
  <div class="equipe__tete">
    <h2 id="equipe-t">Cinq chirurgiens,<br><span class="fin">un seul chemin.</span></h2>
    <p>Formés dans des centres hospitaliers universitaires, ils se connaissent depuis l'internat. Ils discutent ensemble les dossiers difficiles, opèrent à plusieurs les interventions lourdes et assurent la continuité des soins 365 jours et nuits par an.</p>
  </div>
  <div class="portraits">{cartes}</div>
</section>'''


def parcours():
    etapes = "".join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in PARCOURS)
    actus = "".join(f'<article><p class="journal__date">{e(a["date_txt"])}</p><h3>{e(a["titre"])}</h3><p>{e(a["texte"][:150].rsplit(" ", 1)[0])}…</p></article>'
                    for a in ACTUALITES[:3])
    return f'''<section class="parcours" id="parcours" aria-labelledby="parcours-t">
  <h2 id="parcours-t">Le parcours</h2>
  <ol class="etapes">{etapes}</ol>
  <div class="journal">
    <h2>Au cabinet, en ce moment</h2>
    <div class="journal__liste">{actus}</div>
  </div>
</section>'''


def specialites_affichees(c):
    return [x for x, _ in c["specialites"] if x not in ("Chirurgie générale", "Chirurgie robotique")]


def contact():
    """Module de rendez-vous : choisir un chirurgien, puis un canal. Aucune donnée saisie ni
    envoyée : il mène vers Maiia (plateforme citée sur nemaudig.fr), le téléphone ou Uzès."""
    a = C["adresse"]
    pgs, hpf = ETABLISSEMENTS
    choix = "".join(f'''<label class="choix-medecin"><input type="radio" name="rdv-medecin" value="{c["slug"]}" data-nom="{e(nom_complet(c))}">
      <img src="/img/{c["slug"]}-400.webp" width="64" height="80" alt="" loading="lazy">
      <span><strong>{e(nom_complet(c))}</strong><small>{e(" · ".join(specialites_affichees(c)[:2]))}</small></span></label>''' for c in CHIRURGIENS)
    choix += '''<label class="choix-medecin choix-medecin--equipe"><input type="radio" name="rdv-medecin" value="equipe" data-nom="Nemaudig">
      <span class="choix-medecin__signe" aria-hidden="true">?</span>
      <span><strong>Je ne sais pas encore</strong><small>Le secrétariat vous oriente vers le bon chirurgien</small></span></label>'''
    uzes = " ou ".join(UZES["tel"])
    return f'''<section class="contact" id="contact" aria-labelledby="contact-t">
  <h2 id="contact-t">Prendre rendez&#8209;vous</h2>
  <div class="rdv" data-etape="1">
    <ol class="rdv__fil" aria-hidden="true"><li data-n="1">Chirurgien</li><li data-n="2">Canal</li><li data-n="3">Confirmation</li></ol>
    <fieldset class="rdv__etape" data-pour="1">
      <legend>Avec qui souhaitez-vous consulter&nbsp;?</legend>
      <div class="rdv__medecins">{choix}</div>
    </fieldset>
    <fieldset class="rdv__etape" data-pour="2">
      <legend>Comment prendre rendez-vous&nbsp;?</legend>
      <div class="rdv__canaux">
        <label class="canal"><input type="radio" name="rdv-canal" value="maiia"><strong>En ligne</strong><span>Sur {e(C["rdv_en_ligne_libelle"])}, la plateforme de rendez-vous du cabinet</span></label>
        <label class="canal"><input type="radio" name="rdv-canal" value="tel"><strong>Par téléphone</strong><span>{e(C["horaires_affiches"])}</span></label>
        <label class="canal" data-seulement="dr-david-amielh"><input type="radio" name="rdv-canal" value="uzes"><strong>À Uzès</strong><span>Dr Amielh au {e(UZES["nom"])}, {e(UZES["creneau"].lower())}</span></label>
      </div>
      <button type="button" class="rdv__retour" data-aller="1">← Changer de chirurgien</button>
    </fieldset>
    <div class="rdv__etape rdv__fin" data-pour="3" aria-live="polite">
      <div data-canal="maiia">
        <p class="rdv__titre">Sur Maiia, recherchez&nbsp;:</p>
        <p class="rdv__recherche"><span data-recherche>Nemaudig</span><button type="button" class="rdv__copier">Copier</button></p>
        <a class="bouton bouton--sombre" href="{e(C["rdv_en_ligne"])}" target="_blank" rel="noopener">Ouvrir Maiia ↗</a>
      </div>
      <div data-canal="tel">
        <p class="rdv__titre">Appelez le secrétariat&nbsp;:</p>
        <p class="contact__tel">{C["telephone_affiche"]}</p>
        <p>{e(C["horaires_affiches"])}. Précisez <span data-recherche>Nemaudig</span>.</p>
      </div>
      <div data-canal="uzes">
        <p class="rdv__titre">{e(UZES["nom"])} · {e(UZES["creneau"].lower())}</p>
        <p class="contact__tel contact__tel--moyen">{e(UZES["tel"][0])}</p>
        <p>ou {e(UZES["tel"][1])} · {e(UZES["horaires_tel"])}</p>
      </div>
      <button type="button" class="rdv__retour" data-aller="2">← Changer de canal</button>
    </div>
  </div>
  <dl class="contact__fiche">
    <div><dt>Cabinet</dt><dd>{e(a["rue"])}<br>{e(a["complement"])}<br>{a["code_postal"]} {e(a["ville"])}</dd></div>
    <div><dt>On y opère</dt><dd>{e(pgs["nom"])}<br>{e(hpf["nom"])}</dd></div>
    <div><dt>Uzès</dt><dd>Dr Amielh, {e(UZES["creneau"].lower())}<br>{uzes}</dd></div>
    <div><dt>Urgences</dt><dd>{e(C["urgences_nom"])}<br>{C["urgences_tel"]}</dd></div>
  </dl>
</section>
<footer class="pied">
  <img src="/assets/img/logo-nemaudig-160.webp" width="56" height="56" alt="">
  <p>Nemaudig — association de chirurgiens digestifs et viscéraux · Nîmes</p>
  <p class="pied__credit">Modèles 3D&nbsp;: <a href="https://lifesciencedb.jp/bp3d/" rel="noopener">BodyParts3D</a>, © The Database Center for Life Science, licence <a href="https://creativecommons.org/licenses/by/4.0/deed.fr" rel="noopener">CC BY 4.0</a> — simplifiés et lissés pour le web.</p>
  <p>Maquette B · non indexée</p>
</footer>'''


def entete():
    return '''<header class="entete">
  <a class="marque" href="#haut" aria-label="Nemaudig — haut de page">
    <img src="/assets/img/logo-nemaudig-320.webp" width="88" height="87" alt="Logo Nemaudig">
    <span class="marque__nom">Nemaudig<small>Chirurgie digestive &amp; viscérale · Nîmes</small></span>
  </a>
  <nav class="menu" aria-label="Sections">
    <a href="#voyage-depart">Le voyage</a><a href="#organes">Les organes</a><a href="#orientation">Orientation</a><a href="#equipe">L'équipe</a>
  </nav>
  <a class="bouton bouton--lampe bouton--petit" href="#contact">Rendez-vous</a>
</header>'''


def page():
    donnees = json.dumps({"stations": [{"cle": s["cle"], "u": s["u"], "riche": ARRETS[s["cle"]]["riche"],
                                        "anims": [pa.get("anim") for pa in ARRETS[s["cle"]]["pathos"]]} for s in STATIONS],
                          "modeles": list(MODELES)}, ensure_ascii=False)
    return f'''<!doctype html>
<html lang="fr" class="no-js">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nemaudig — Exploration intérieure (maquette B)</title>
<meta name="description" content="Maquette B du site Nemaudig, chirurgiens digestifs et viscéraux à Nîmes : un voyage en 3D à l'intérieur de l'appareil digestif.">
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#160f26">
<link rel="icon" href="/favicon-32.png" type="image/png">
<link rel="preload" href="/assets/fonts/unbounded-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/sora-var.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="/assets/css/exploration.css">
<script>document.documentElement.classList.replace("no-js","js")</script>
<script type="application/json" id="donnees">{donnees}</script>
<script type="module" src="/assets/js/exploration.js"></script>
</head>
<body>
<!-- Direction « Exploration intérieure » : dans le corps il n'y a pas de lumière, sauf celle qu'on apporte.
     Monde violet profond (logo #413B5D) éclairé par une lampe orange (#F38D38). Unbounded / Sora / JetBrains Mono (mesures).
     Image stable : aucun grain, aucun scintillement, aucun flash ; seul le scroll déplace la caméra. -->
<p class="demo">Maquette B — proposition alternative · contenus repris du site nemaudig.fr</p>
{entete()}
<main>
{voyage()}{organes()}{orientation()}{equipe()}{parcours()}{contact()}
</main>
</body>
</html>'''


def main():
    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(RACINE / "src", DIST)
    (DIST / "index.html").write_text(page(), encoding="utf-8")
    print("✓ dist/index.html — maquette B « Exploration intérieure »")


if __name__ == "__main__":
    main()
