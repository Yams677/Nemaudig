"""Galerie des séquences vidéo — emplacements de démonstration, clairement signalés."""
from data.videos_ia import FORMAT, VIDEOS
from lib.gabarit import e, sur_titre, u


def _plans(v):
    lignes, t = [], 0
    for duree, visuel, sous_titre in v["plans"]:
        lignes.append(f'<tr><td class="repere">{t:02d}–{t + duree:02d} s</td><td>{e(visuel)}</td><td>« {e(sous_titre)} »</td></tr>')
        t += duree
    return "".join(lignes)


def _modale(v):
    return f'''<dialog class="modale" id="video-{v["id"]}" aria-labelledby="video-{v["id"]}-titre">
  <div class="modale__tete"><p class="sur-titre">Séquence {v["numero"]} · en préparation</p>
    <button class="tiroir__fermer" type="button" data-ferme aria-label="Fermer">×</button></div>
  <h2 class="titre-m" id="video-{v["id"]}-titre">{e(v["titre"])}</h2>
  <p>{e(v["objet"])}</p>
  <p class="provisoire"><span aria-hidden="true">◇</span> Cette vidéo n'est pas encore produite. Voici son découpage ; le prompt de génération est prêt (docs/PROMPTS-VIDEO.md).</p>
  <div class="tableau-defile"><table class="tableau">
    <thead><tr><th scope="col">Temps</th><th scope="col">À l'image</th><th scope="col">Sous-titre</th></tr></thead>
    <tbody>{_plans(v)}</tbody></table></div>
  <dl class="fiche-technique">
    <div><dt>Durées</dt><dd>Version courte {v["courte"]} s · version détaillée {v["detaillee"]} s</dd></div>
    <div><dt>Format</dt><dd>{e(FORMAT["image"])}</dd></div>
    <div><dt>Accessibilité</dt><dd>{e(FORMAT["sous_titres"])}</dd></div>
    <div><dt>Avant publication</dt><dd>Relecture de la séquence par un chirurgien de l'équipe</dd></div>
  </dl>
</dialog>'''


def galerie(titre="Comprendre en images", niveau=2):
    cartes = "".join(f'''<li><button class="video" type="button" data-ouvre="video-{v["id"]}" aria-haspopup="dialog">
    <span class="video__ecran" aria-hidden="true"><img src="{u("/assets/img/organes/" + v["organe"] + ".webp")}" width="640" height="640" alt="" loading="lazy" decoding="async"><span class="video__lecture"></span>
      <span class="video__etat">Séquence en préparation</span></span>
    <span class="repere">{v["numero"]} · {v["courte"]} s / {v["detaillee"]} s</span>
    <span class="video__titre">{e(v["titre"])}</span>
    <span class="video__objet">{e(v["objet"])}</span>
  </button></li>''' for v in VIDEOS)
    modales = "".join(_modale(v) for v in VIDEOS)
    return f'''<section class="plan plan--nuit bloc" id="videos" aria-labelledby="videos-titre">
  <div class="contenu">
    <div class="bloc__tete">{sur_titre("Vidéothèque")}
      <h{niveau} class="titre-l" id="videos-titre">{e(titre)}</h{niveau}>
      <p class="chapo">Cinq séquences courtes, sous-titrées, pour expliquer un organe ou un examen sans jargon. Elles seront générées par intelligence artificielle, puis vérifiées par l'équipe avant publication.</p>
    </div>
    <ul class="videos">{cartes}</ul>
  </div>
  {modales}
</section>'''
