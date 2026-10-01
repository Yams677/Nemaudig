"""Blocs réutilisables entre pages."""

import config
from data.chirurgiens import CHIRURGIENS, PAR_SLUG as CHIRS, initiales, nom_complet
from data.videos import VIDEOS
from lib import portraits
from lib.anatomie import planche
from lib.html import C, ICONES, bouton, e, surtitre, tel_href

# Une teinte pastel par chirurgien, en attendant les portraits.
TEINTES = {
    "dr-mathias-alline": "var(--ciel)",
    "dr-david-amielh": "var(--menthe)",
    "dr-sylvain-laporte": "var(--lilas)",
    "dr-emmanuel-prieur": "var(--sable)",
    "dr-fanelly-torres": "var(--peche)",
}


def specialites_courtes(c):
    return " · ".join(s for s, _ in c["specialites"] if s not in ("Chirurgie générale", "Chirurgie robotique"))


def portrait(c, sizes, classe="", charge="lazy"):
    """<picture> WebP + JPG si une photo existe, sinon le monogramme."""
    if not portraits.source(c["slug"]):
        note = '<span class="medecin__note">Portrait à venir</span>' if config.DEMO else ""
        return f'<span class="medecin__monogramme" aria-hidden="true">{initiales(c)}</span>{note}'
    s = c["slug"]
    srcset = lambda ext: ", ".join(f"{portraits.url(s, l, ext)} {l}w" for l in portraits.LARGEURS)
    return (f'<picture class="{classe}"><source type="image/webp" srcset="{srcset("webp")}" sizes="{sizes}">'
            f'<img src="{portraits.url(s, 800, "jpg")}" srcset="{srcset("jpg")}" sizes="{sizes}" width="800" height="1000" '
            f'alt="Portrait du {e(nom_complet(c))}" loading="{charge}" decoding="async"></picture>')


def carte_medecin(c, i=0):
    return f'''<a class="medecin" href="/chirurgiens/{c["slug"]}/" style="--teinte:{TEINTES[c["slug"]]};--d:{i}" data-reveal>
  <div class="medecin__portrait">{portrait(c, "(min-width: 1000px) 230px, (min-width: 640px) 45vw, 90vw")}</div>
  <div class="medecin__corps">
    <h3 class="medecin__nom">{e(nom_complet(c))}</h3>
    <p class="medecin__specs">{e(specialites_courtes(c))}</p>
    <span class="medecin__voir">Parcours et spécialités {ICONES["fleche"]}</span>
  </div>
</a>'''


def mini_medecin(slug):
    c = CHIRS[slug]
    return f'''<a class="mini-medecin" href="/chirurgiens/{slug}/" style="--teinte:{TEINTES[slug]}">
  <span class="mini-medecin__mono" aria-hidden="true">{f'<img src="{portraits.url(slug, 400, "webp")}" alt="" width="44" height="55" loading="lazy" decoding="async">' if portraits.source(slug) else initiales(c)}</span>
  <span><strong>{e(nom_complet(c))}</strong><span>{e(c["accroche"])}</span></span>
</a>'''


def video(cle, titre_h="h3"):
    v = VIDEOS[cle]
    chir = CHIRS.get(v["chirurgien"]) if v["chirurgien"] else None
    auteur = f"par le {nom_complet(chir)}" if chir else "équipe Nemaudig"
    robot = f'<span class="tag-robot">{ICONES["robot"]} Robot</span>' if v["robot"] else ""
    return f'''<div class="video" data-video="{v["yt"]}" data-titre="{e(v["titre"])}">
  <div class="video__media">
    <img src="https://i.ytimg.com/vi/{v["yt"]}/hqdefault.jpg" alt="" loading="lazy" decoding="async" width="480" height="360">
    <span class="video__play" aria-hidden="true"><svg viewBox="0 0 24 24"><path d="M7 4.5v15l12-7.5Z" fill="currentColor"/></svg></span>
    <button type="button" aria-label="Lire la vidéo : {e(v["titre"])}, {e(auteur)} (chargement depuis YouTube)"></button>
  </div>
  <div class="video__texte"><span class="video__titre">{e(v["titre"])}</span><span class="video__meta">{e(auteur)} {robot}</span></div>
</div>'''


def faq(questions, ident="faq"):
    if not questions:
        return ""
    items = "".join(f'''<details{' open' if i == 0 else ''}><summary>{e(q)}</summary><div class="faq__rep"><p>{e(r)}</p></div></details>'''
                    for i, (q, r) in enumerate(questions))
    return f'<div class="faq" id="{ident}">{items}</div>'


def schema_faq(questions):
    if not questions:
        return None
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in questions]}


def tete_page(titre_html, chapo, surt=None, teinte="var(--menthe)", organe=None, meta_html=""):
    planche_html = (f'<div class="tete-page__planche" aria-hidden="true">{planche(actif=organe, ident="planche-tete", classe="a-un-actif")}</div>'
                    if organe else "")
    return f'''<header class="tete-page{' tete-page--organe' if organe else ''}" style="--teinte:{teinte}">
  <div class="conteneur">
    <div>
      {surtitre(surt) if surt else ""}
      <h1>{titre_html}</h1>
      {f'<p class="chapo">{chapo}</p>' if chapo else ""}
      {f'<div class="tete-page__meta">{meta_html}</div>' if meta_html else ""}
    </div>
    {planche_html}
  </div>
</header>'''


def bandeau_rdv(titre="Prendre rendez-vous avec un chirurgien", texte=None):
    texte = texte or ("Vous serez orienté vers celui d'entre nous le plus à même de vous prendre en charge, "
                      "en respectant vos souhaits et les recommandations du médecin qui vous adresse.")
    return f'''<section class="section section--serree" aria-labelledby="rdv-titre">
  <div class="conteneur">
    <div class="rdv" data-reveal>
      <div>
        {surtitre("Rendez-vous")}
        <h2 id="rdv-titre">{titre}</h2>
        <p>{texte}</p>
      </div>
      <div class="rdv__canaux">
        <a class="canal" href="{tel_href()}"><span class="canal__ico">{ICONES["tel"]}</span><span><strong>{C["telephone_affiche"]}</strong><span>Secrétariat · {e(C["horaires_affiches"].lower())}</span></span></a>
        <a class="canal" href="/contact/#en-ligne"><span class="canal__ico">{ICONES["agenda"]}</span><span><strong>En ligne sur {C["rdv_en_ligne_libelle"]}</strong><span>Recherchez « Nemaudig » ou le nom du chirurgien</span></span></a>
        <a class="canal" href="/consultation-uzes/"><span class="canal__ico">{ICONES["lieu"]}</span><span><strong>Consultation à Uzès</strong><span>Dr Amielh · le lundi matin</span></span></a>
      </div>
    </div>
  </div>
</section>'''


def carte_patho(p, avec_planche=True):
    pl = f'<div class="patho__planche" aria-hidden="true">{planche(actif=p["organe"], ident="pp-" + p["slug"], classe="a-un-actif planche--vignette")}</div>' if avec_planche else ""
    cancer = '<span class="pastille pastille--lilas">Cancérologie</span>' if p.get("cancer") else ""
    return f'''<a class="patho" href="/pathologies/{p["slug"]}/" data-reveal>
  {pl}
  <div><h3>{e(p["court"] if len(p["titre"]) > 34 else p["titre"])}</h3><p>{e(p["resume"])}</p>{cancer}</div>
  {ICONES["fleche"]}
</a>'''
