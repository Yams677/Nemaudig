"""Techniques opératoires : hub + robotique, cœlioscopie, ambulatoire, réhabilitation améliorée."""

import config
from data.cabinet import TECHNIQUES
from lib.composants import bandeau_rdv, tete_page, video
from lib.html import ICONES, e, riche, surtitre
from lib.layout import page

REDIRECTIONS = {t["ancien"]: f"/techniques/{t['slug']}/" for t in TECHNIQUES}
ICONE = {"chirurgie-robotique": "robot", "coelioscopie": "camera", "chirurgie-ambulatoire": "maison", "rehabilitation-amelioree": "bouclier"}
FIL = ("/techniques/", "Techniques")


def page_hub(assets):
    cartes = "".join(f'''<a class="tuile" href="/techniques/{t["slug"]}/" data-reveal style="--d:{i}">
  <span class="tuile__ico">{ICONES[ICONE[t["slug"]]]}</span><h3>{e(t["titre"])}</h3><p>{e(t["accroche"])}</p>
  <span class="tuile__pied">Découvrir {ICONES["fleche"]}</span></a>''' for i, t in enumerate(TECHNIQUES))
    corps = f'''<section class="section section--nuit" style="padding-top:clamp(48px,6vw,80px)"><div class="conteneur">
  <div class="section__tete section__tete--2"><div>{surtitre("Techniques opératoires")}<h1 style="color:#fff">Opérer mieux, <em>récupérer plus vite.</em></h1></div>
  <p class="chapo" style="color:#AFC1CB">Cœlioscopie 3D, robot chirurgical, ambulatoire et réhabilitation améliorée : les techniques que l'équipe met au service de chaque intervention, quand elles sont adaptées à votre cas.</p></div>
  <div class="grille grille--2">{cartes}</div>
</div></section>''' + bandeau_rdv()
    return page(assets, "/techniques/", "Techniques chirurgicales — robot, cœlioscopie 3D, Nîmes",
                "Robot chirurgical Da Vinci, cœlioscopie 3D 4K, chirurgie ambulatoire et réhabilitation améliorée : les techniques de l'équipe Nemaudig à Nîmes.",
                corps, fil=[FIL])


def page_tech(assets, t):
    url = f"/techniques/{t['slug']}/"
    extra = ""
    if t.get("encart"):
        titre, txt = t["encart"]
        extra += f'<div class="encart encart--lagon mt-6"><h2>{e(titre)}</h2><p class="mb-0">{e(txt)}</p></div>'
    if t.get("conditions"):
        extra += '<h2 class="mt-7">Les conditions</h2><ul class="liste">' + "".join(f"<li>{e(c)}</li>" for c in t["conditions"]) + "</ul>"
        extra += '<p>Sont le plus souvent concernées : <a href="/pathologies/hernie-inguinale/">hernies</a>, <a href="/pathologies/vesicule-biliaire/">vésicule biliaire</a>, <a href="/pathologies/proctologie/">certaines opérations de la région anale</a> et <a href="/pathologies/kystes-et-lipomes/">opérations de la peau</a>.</p>'
    vids = "".join(f"<div>{video(v)}</div>" for v in t["videos"])
    bloc_v = (f'<section class="section section--blanc"><div class="conteneur"><div class="section__tete">{surtitre("En vidéo")}'
              f'<h2>{"Le robot et ses interventions" if t["slug"] == "chirurgie-robotique" else "Interventions filmées"}</h2></div>'
              f'<div class="grille grille--3">{vids}</div></div></section>') if vids else ""
    autres = "".join(f'<li><a href="/techniques/{x["slug"]}/"><span>{e(x["court"])}</span>{ICONES["fleche"]}</a></li>' for x in TECHNIQUES if x is not t)
    corps = tete_page(e(t["titre"]), e(t["accroche"]), "Techniques · Nîmes", "var(--ciel)") + f'''
<section class="section section--serree"><div class="conteneur"><div class="article" style="grid-template-columns:minmax(0,1fr) 300px">
  <div class="prose">{riche(t["texte"])}{extra}</div>
  <aside class="aside"><div class="encart"><h2>Autres techniques</h2><ul class="encart__liste">{autres}</ul></div>
  <div class="encart encart--menthe"><h2>Est-ce possible pour moi&nbsp;?</h2><p>Votre chirurgien vous indiquera en consultation la technique adaptée à votre cas.</p><a class="lien-fleche" href="/contact/">Prendre rendez-vous {ICONES["fleche"]}</a></div></aside>
</div></div></section>{bloc_v}''' + bandeau_rdv()
    return page(assets, url, f"{t['titre']} à Nîmes — Nemaudig", t["desc"], corps, fil=[FIL, (url, t["court"])])


def rendre(assets):
    pages = {"/techniques/": page_hub(assets)}
    for t in TECHNIQUES:
        pages[f"/techniques/{t['slug']}/"] = page_tech(assets, t)
    return pages
