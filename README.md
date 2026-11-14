# Nemaudig — maquette C « Les visages d'abord »

Troisième proposition de site pour le cabinet Nemaudig (chirurgie digestive et viscérale, Nîmes).
Tons pastel (crème, pêche, sauge, lilas, encre prune du logo). L'accueil s'ouvre sur les cinq chirurgiens ;
les organes sont montrés un à la fois, par des images réalistes générées par IA (`src/assets/img/organes/`,
512 px, à faire valider). Plus aucune 3D depuis le 14/11/2026.
50 pages : accueil, chirurgiens, spécialités (24 fiches), explorateur anatomique,
parcours de soins, préparer, prévention, centres, rendez-vous, pages légales.

## Lancer

Double-cliquer sur `ouvrir-le-site.bat` (génération non incluse), ou :

```bash
PYTHONIOENCODING=utf-8 python build.py     # génère dist/
python serveur.py                          # http://localhost:8785
```

Python 3.12 suffit ; aucune dépendance à installer.

## Publier sur GitHub Pages

```bash
NEMAUDIG_BASE=/Nemaudig PYTHONIOENCODING=utf-8 python build.py
```

puis publier le contenu de `dist/` (branche `gh-pages`). `NEMAUDIG_BASE` est le nom du dépôt ;
le laisser vide pour un domaine propre. La maquette reste non indexée tant que `config.DEMO = True`.

## Organisation

| Dossier | Rôle |
|---|---|
| `config.py` | Coordonnées du cabinet, mode démonstration, préfixe d'adresse |
| `data/` | Contenus. Repris de nemaudig.fr : `cabinet`, `chirurgiens`, `pathologies`, `obesite`, `orientation`. Rédigés pour la maquette, à valider : `organes`, `examens`, `videos_ia` |
| `lib/` | Gabarit des pages, schémas animés SVG, galerie vidéo, rapprochements entre données |
| `pages/` | Un module par rubrique |
| `src/assets/` | CSS (assemblé en `site.css`), JavaScript sans dépendance, polices, images |
| `docs/` | `A-VALIDER.md` (contenus à faire relire) · `PROMPTS-VIDEO.md` (storyboards et prompts, généré) |

`build.py` refuse de générer si une page a un titre ou une description en double, plus d'un `<h1>`,
un lien interne ou une ancre cassés, un identifiant en double.

## Vérifier

- `?calme=1` : rendu « animations réduites » ; `?fige=1` : état final sans transition.
- `/?p=0.5` : fige l'ouverture de l'accueil à mi-parcours ; `/explorer/?vue=fixe` : explorateur sans transition.
- `python tools_capture.py "/?p=0.5" 1440 900 sortie.png` : capture Edge sans interface (largeur minimale 500 px).

## Choix assumés

- Nemaudig est un cabinet de **chirurgiens** : les examens endoscopiques sont présentés comme prescrits,
  réalisés par des gastro-entérologues (voir `docs/A-VALIDER.md`).
- Aucun cookie, aucun traceur, aucun formulaire ; polices et modèles hébergés sur le site ; carte chargée au clic.
- Tout élément provisoire est marqué ◇ ; le bouton « Maquette » de l'en-tête en donne la liste.
- Vidéos IA : emplacements seulement (images tirées du modèle 3D), jamais présentées comme existantes.

## Crédits

Images d'organes générées par IA (DaVinci, modèle Nano Banana 2). Polices Outfit, Geist, Geist Mono (SIL OFL).
