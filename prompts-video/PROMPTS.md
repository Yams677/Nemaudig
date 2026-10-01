# Vidéo « Voyage au cœur de l'appareil digestif » — prompts pour davinci.ai

**Usage sur le site** : ouverture de la section Voyage, en fond, muette, en boucle, sous le
titre « Au cœur de l'appareil digestif ». La 3D interactive prend ensuite le relais au défilement.
La vidéo doit donc **avoir exactement le même style que la 3D** (fond nuit, corps en verre turquoise,
organes pastel brillants) : sinon la transition se verra.

**Règles à respecter dans tous les plans**
- Illustration stylisée, **jamais réaliste-chirurgicale** : pas de sang, pas de chair, pas d'endoscopie réelle.
- Aucune personne, aucun visage, aucun texte ni logo dans l'image (les textes restent en HTML, pour le SEO et l'accessibilité).
- Le site affichera la mention « Illustration animée » — elle ne doit pas passer pour de l'imagerie médicale.

**Réglages conseillés** : 16:9 en 1920×1080 (+ une version 9:16 pour le mobile), 24 ou 30 i/s,
mouvement de caméra lent, 5 à 10 s par plan. Si l'outil propose « image vers vidéo », partir des
images de référence de ce dossier : c'est le meilleur moyen de garder la cohérence avec le site.

| Fichier de référence | Pour |
|---|---|
| `ref-intro-16x9.png` | Plans 1 et 5 (vue d'ensemble), ordinateur |
| `ref-intro-9x16.png` | Toutes les versions mobile |
| `ref-estomac-16x9.png` | Plan 2 |
| `ref-colon-16x9.png` | Plans 3 et 4 |

---

## Bloc de style (à coller à la fin de chaque prompt)

```
Style: premium medical 3D illustration, stylized and elegant, not realistic surgery.
Translucent glass human torso with a soft teal rim light (#2BB3A7), floating in a deep navy night
space (#07131C) with tiny teal dust particles. Organs are smooth, rounded, glossy clay-like volumes
with clearcoat reflections in soft pastel colors: liver peach (#E7A090), stomach lavender (#C5AEF0),
gallbladder sage green (#A9CF7C), pancreas pale sand (#F2CD8F), small intestine soft pink (#F1AEBD),
colon mint (#8FD6C0). Subtle bloom, cinematic depth of field, volumetric soft light, calm and
reassuring mood, ultra clean, 4K, high detail, smooth slow camera motion.
```

## Prompt négatif (si l'outil en accepte un)

```
blood, gore, raw flesh, realistic surgery, scalpel, wounds, veins close-up, skeleton, skull,
human face, person, doctor, hands, text, letters, watermark, logo, cartoon, low poly, flickering,
fast camera, shaky camera, glitch, distorted anatomy, extra organs, oversaturated colors
```

---

## Plan 1 — Apparition (6–8 s) · image de départ : `ref-intro-16x9.png`

```
Slow cinematic reveal in darkness: a translucent glass human torso slowly materializes from
teal light particles, floating above three thin glowing concentric rings. Inside, the digestive
organs fade in one after another, from top to bottom: esophagus, liver and stomach, pancreas,
small intestine, colon. A thin horizontal teal scanning line sweeps slowly from the top to the
bottom of the torso. The camera slowly orbits 20 degrees to the right.
[bloc de style]
```

## Plan 2 — Plongée vers l'estomac et le foie (6–8 s) · `ref-estomac-16x9.png`

```
The camera glides slowly forward through the glass surface of the torso and approaches the
lavender stomach and the peach liver. The other organs soften out of focus. The stomach gently
glows from within with a soft teal light, its glossy surface catching reflections. Slow push-in,
shallow depth of field, peaceful and precise.
[bloc de style]
```

## Plan 3 — Le long du cadre du côlon (6–8 s) · `ref-colon-16x9.png`

```
Smooth tracking shot following the mint colon as it frames the abdomen: the camera travels
along the tube, rising on the right side, crossing the top, descending on the left side, while the
soft pink coils of the small intestine float in the center. A gentle teal light pulse travels
along the colon in the same direction as the camera. Elegant, calm, continuous motion.
[bloc de style]
```

## Plan 4 — Vue éclatée (6–8 s) · `ref-colon-16x9.png` ou `ref-intro-16x9.png`

```
Exploded-view animation: the digestive organs slowly separate from each other and float apart
inside and around the glass torso, revealing the hidden pancreas behind the stomach, each organ
softly rotating on itself with glossy reflections. Then they smoothly glide back into their
original place. Slow, graceful, weightless motion, like a precise medical diagram coming alive.
[bloc de style]
```

## Plan 5 — Retour à la vue d'ensemble, image finale fixe (5–6 s) · `ref-intro-16x9.png`

```
The camera slowly pulls back to a full view of the glass torso with all organs in place, glowing
softly, floating above the three glowing rings. The scanning line passes one last time. The final
two seconds are almost still, so the video can loop or hand over to an interactive 3D scene.
[bloc de style]
```

---

## Version mobile (9:16) — un seul plan de 8–10 s · `ref-intro-9x16.png`

```
Vertical framing. A translucent glass human torso floats in deep navy space above glowing teal
rings. The camera starts close on the esophagus at the top and slowly travels down along the
digestive tract — stomach and liver, small intestine, colon — while each organ softly lights up
as the camera passes, then pulls back to reveal the whole torso. Slow, smooth, continuous.
[bloc de style]
```

## Option « boucle d'accueil » claire (8 s) — si on veut aussi une vidéo dans le premier écran

```
Seamless loop. A translucent frosted-glass human torso on a warm ivory background (#F6F4EE),
with a faint teal grid fading into the background. Glossy pastel digestive organs inside gently
breathe and float a few millimeters, a soft teal scanning line moves slowly from top to bottom.
Very slow 10-degree camera sway left and right. First and last frame identical. No text.
Style: premium medical 3D illustration, soft studio light, pastel, clean, reassuring, 4K.
```

---

## Ce que je ferai une fois les vidéos générées

1. Les déposer dans `nemaudig/videos-source/` (MP4, la meilleure qualité disponible).
2. Je les monte en un seul plan (enchaînement 1 → 5), je les compresse (WebM + MP4, objectif < 4 Mo),
   j'extrais une image d'affiche, et je les intègre en lecture automatique muette, en boucle.
3. Garde-fous : pas de lecture si l'utilisateur a demandé moins d'animations, ni en mode
   économie de données ; la 3D interactive reste la référence.

**Conseil** : générer 2 ou 3 variantes du plan 1 avant le reste, choisir la plus fidèle au site,
puis réutiliser sa dernière image comme image de départ du plan suivant pour garder la continuité.
