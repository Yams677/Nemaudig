# Nemaudig — refonte du site (maquette)

Site statique généré par Python, destiné à remplacer nemaudig.fr. Source factuelle :
le scraping Firecrawl `~/.firecrawl/nemaudig` (78 pages lues). Aucune donnée médicale,
qualification ou coordonnée n'a été ajoutée.

```
PYTHONIOENCODING=utf-8 python build.py      # → dist/ (64 pages, 77 redirections 301)
```

Aperçu local : serveur « nemaudig » (port 8770) dans `Skill/.claude/launch.json`.
Captures pleine page : `MSYS_NO_PATHCONV=1 python tools_capture.py /chemin/ 1440 900 4000 sortie.png`.

## Organisation

| Dossier | Rôle |
|---|---|
| `config.py` | Coordonnées (seul fichier NAP), `DEMO = True` → noindex, robots fermé, bandeau, liens tel: neutralisés |
| `data/` | Contenus : chirurgiens, pathologies (24 fiches), obésité, cabinet/parcours/actualités, vidéos |
| `lib/anatomie.py` | Planche anatomique SVG dessinée à la main, réutilisée partout (organe actif en surbrillance) |
| `lib/layout.py` | En-tête, méga-menu, pied de page, JSON-LD (MedicalClinic, Physician, MedicalWebPage, FAQPage, BreadcrumbList) |
| `pages/` | Un module par rubrique ; chaque module déclare ses `REDIRECTIONS` depuis les anciennes URL |
| `src/assets/` | `style.css` (design system complet), `main.js` (interactions sans dépendance), polices auto-hébergées |

`build.py` refuse la génération si : titre/description dupliqués, ≠ 1 `<h1>`, lien interne
ou ancre cassés, id dupliqué, redirection vers une page absente — et, en production,
s'il reste un marqueur « À VALIDER ».

## Anatomie 3D (accueil)

`src/assets/js/anatomie3d.js` + three.js r160 auto-hébergé (`assets/js/vendor/`, ~170 Ko gzip, chargé
sur l'accueil seulement). Organes modélisés à partir des tracés SVG de `lib/anatomie.py` (`donnees_3d()`).
- Hero et planche « Explorer » : les organes s'écartent à l'approche de la souris, l'organe survolé avance,
  s'illumine et porte son nom ; lumière qui suit le curseur ; rotation au glisser ; clic → fiche.
- Section « Voyage au cœur de l'appareil digestif » (`data/voyage.py`) : caméra pilotée par le défilement,
  9 étapes, halo lumineux (bloom). Textes = uniquement des faits du site actuel.
  Rendu « cinéma » (`assets/js/anatomie3d-cinema.js`) : bosselures du côlon, surface organique,
  côtes et colonne en filigrane, pédicule du foie (artère / veine / canal biliaire) aux étapes foie et pancréas,
  profondeur de champ (désactivée sous 700 px), grain + vignettage, poussières floues, caméra « à l'épaule »,
  bandes cinéma, pulsation lumineuse à chaque changement d'étape.
- Prompts pour une vidéo d'ouverture générée par IA : `prompts-video/PROMPTS.md` (+ images de référence).
- Sans WebGL : planche SVG d'origine. Animations réduites si l'utilisateur le demande.
- Contrôle visuel : `tools_capture3d.py` (Edge + SwiftShader ; peu d'images calculées, les transitions
  n'y sont pas toujours terminées — vérifier aussi dans un vrai navigateur).

## Nouvelle architecture

Accueil · Pathologies (5 familles par région du corps + 24 fiches) · Cancérologie ·
Chirurgiens (équipe + 5 fiches) · Obésité (hub avec calcul d'IMC, 4 techniques, parcours, suivi) ·
Techniques (robot, cœlioscopie 3D, ambulatoire, réhabilitation améliorée) · Votre parcours ·
Honoraires · Établissements · Consultation à Uzès · Rendez-vous · Actualités · Vidéos · FAQ ·
Cabinet · pages légales · `/charte/` (design system, noindex).

## À valider avec le cabinet avant mise en ligne

1. **Portraits** : intégrés le 01/10/2026 depuis `photos/chirurgiens/<slug>.png` (recadrage 4:5, WebP+JPG via `lib/portraits.py`). Validés par les chirurgiens le 01/10/2026 (`config.PORTRAITS_VALIDES = True`). Photos des locaux : toujours à fournir.
2. **Honoraires** (70 € / 50 € / 30 €) : date de mise à jour inconnue sur l'ancien site.
3. **Clinique Kennedy** : cabinet d'anesthésie listé sur l'ancienne page « Uzès » alors que
   « Les cliniques » ne cite que 2 établissements. La miniature de la vidéo hernie TEP cite
   aussi la Clinique Kennedy → rôle à confirmer.
4. **Robot ou non** : hernie hiatale et colectomie angulaire gauche sont « ROBOT » sur
   /robotique mais pas sur /videos (et « cœlio » sur la fiche hernie hiatale) → titres neutres.
5. **« 6 médecins associés »** sur l'ancienne page Engagements alors que l'équipe compte 5
   chirurgiens → non repris.
6. **Lien Maiia direct** du cabinet (lien générique pour l'instant).
7. **Surrénales** : l'ancienne page ne contient qu'une vidéo → fiche à rédiger par l'équipe.
8. Statistiques OMS 2014 (page « Points importants ») : non reprises, trop anciennes.
9. Mentions légales : n° RPPS des chirurgiens, concepteur du site.
10. Coordonnées GPS du cabinet (`config.CABINET["geo"]`) : approximatives.

## Choix assumés

- Pas de formulaire de contact : aucune donnée de santé ne transite par le site (RDV par
  téléphone ou Maiia). Aucun cookie ; vidéos YouTube chargées au clic (youtube-nocookie).
- Les fiches PDF patient pointent encore vers nemaudig.fr (© FCVD) : à recopier dans `src/` au déploiement.
- `.htaccess` (Apache/OVH) généré avec les 301 de toutes les anciennes URL.
