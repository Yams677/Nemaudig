# Nemaudig — maquette B « Exploration intérieure »

Proposition alternative de page d'accueil pour nemaudig.fr (chirurgiens digestifs et viscéraux, Nîmes) :
voyage en 3D à l'intérieur du tube digestif, arrêts par organe avec vues éclatées des vrais organes,
pathologies et chirurgien concerné, visionneuse d'organes, orientation par signes, prise de rendez-vous.

```bash
PYTHONIOENCODING=utf-8 python build.py      # → dist/index.html
python -m http.server 8780 --directory dist
```

- Contenus : repris de nemaudig.fr (`data/`), rien d'inventé. Maquette non indexée (`config.DEMO = True`).
- Attributions chirurgien ↔ pathologie (`data/voyage.py`, `ARRETS`) : proposées d'après les spécialités
  affichées sur le site, **à faire valider par l'équipe**.
- Rendez-vous en ligne : Maiia (plateforme citée sur le site actuel) ; liens directs par chirurgien à obtenir.
- Modèles 3D : [BodyParts3D](https://lifesciencedb.jp/bp3d/), © The Database Center for Life Science,
  licence CC BY 4.0 — simplifiés et lissés pour le web. three.js r160 (MIT) dans `src/assets/js/vendor/`.
