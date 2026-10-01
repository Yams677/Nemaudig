# Film 30 s « réaliste » — prompts pour davinci.ai

**Objectif** : 30 secondes, de **vrais organes** (rendu anatomique photoréaliste, type
visualisation médicale de musée), en lien direct avec le site : les spécialités du cabinet,
les techniques modernes, et la signature Nemaudig à Nîmes.

**Format** : 5 plans de 6 s, en 16:9 (1920×1080, 24 i/s). Une variante verticale est en bas de page.
**Économie de crédits** : générer d'abord **l'image clé** (étape 0) en image fixe, la valider, puis
animer chaque plan en « image vers vidéo » à partir d'elle. Faire un seul essai du plan 1 avant le reste.

---

## Règles

- **Réaliste, mais jamais chirurgical** : organes entiers, propres, comme un modèle anatomique
  d'exception. Pas de sang, pas d'incision, pas de geste opératoire réel, pas de personne.
- **Aucun texte dans l'image** : les titres sont ajoutés au montage (les IA écrivent mal le français).
- **Couleurs** : organes dans leurs couleurs naturelles ; décor nuit `#07131C` ; lumières
  turquoise `#2BB3A7` (couleur du site) ; plan final sur le violet du logo `#413B5D`, touche orange `#F38D38`.
- **Validation médicale** : faire valider le film par les chirurgiens (exactitude anatomique)
  avant toute diffusion, et l'afficher avec la mention « Illustration animée ».

---

## Bloc de style (à coller à la fin de chaque prompt)

```
Photorealistic medical 3D visualization, anatomically accurate human digestive organs with
natural tissue colors: liver deep red-brown, stomach soft pink, small intestine salmon pink,
colon pale pink with visible haustral folds, gallbladder dark green, pancreas pale yellow-beige.
Clean, intact organs like a museum-grade anatomical model, subtle moist sheen, subsurface
scattering, fine visible blood vessels on the surface. Organs float in a deep navy void (#07131C)
with soft teal rim light (#2BB3A7) and delicate floating particles. Cinematic anamorphic lens,
shallow depth of field, soft volumetric light, subtle film grain, slow elegant camera motion.
Calm, precise, reassuring, premium. 4K, ultra detailed, 24 fps.
```

## Prompt négatif

```
blood, gore, wound, incision, open surgery, scalpel, gloves, hands, person, face, skeleton,
skull, disease lesions, tumor, pus, text, letters, logo, watermark, cartoon, plastic toy look,
low detail, distorted anatomy, extra organs, oversaturated, harsh light, fast camera, shaky camera
```

---

## Étape 0 — Image clé (image fixe, pas de vidéo)

```
Full human digestive system floating upright in a deep navy void: esophagus, stomach, liver with
gallbladder, pancreas, small intestine coils framed by the colon, rectum. Anatomically correct
positions, front view, slightly turned three-quarters. A faint translucent outline of a human
torso made of teal light surrounds the organs.
[bloc de style]
```
→ Une fois validée, c'est l'image de départ de tous les plans.

---

## Plan 1 — Ouverture · 0–6 s
```
Starting from darkness, a thin horizontal teal scanning light sweeps down slowly and reveals,
organ by organ, the complete realistic human digestive system floating inside a faint glass-like
torso outline. Slow push-in toward the organs.
[bloc de style]
```
> Titre au montage : **Au cœur de l'appareil digestif** — *Nemaudig · Nîmes*

## Plan 2 — Œsophage et estomac · 6–12 s
```
The camera glides down along the realistic esophagus, its muscular wall gently contracting in a
slow peristaltic wave, until it reaches the soft pink stomach. Slow orbit around the stomach,
fine vessels visible on its surface, teal rim light outlining its curve.
[bloc de style]
```
> Titre : **Reflux · Hernie hiatale · Chirurgie de l'obésité**

## Plan 3 — Foie et vésicule · 12–18 s
```
Majestic close-up of the realistic deep red-brown liver with the small dark green gallbladder
beneath it. Thin luminous lines trace the vessels entering the liver — one artery, one vein,
one bile duct — with a soft pulse of light travelling along them. Slow lateral dolly.
[bloc de style]
```
> Titre : **Foie · Vésicule biliaire · Pancréas**

## Plan 4 — Côlon et précision chirurgicale · 18–24 s
```
Smooth tracking shot along the realistic colon with its soft haustral folds framing the abdomen.
Then three slender instruments made of pure teal light glide in with extreme precision toward
the colon, without touching it, suggesting minimally invasive laparoscopic surgery. Elegant,
controlled, technological.
[bloc de style]
```
> Titre : **Côlon · Rectum · Cœlioscopie 3D et robot chirurgical**

## Plan 5 — Signature · 24–30 s
```
The camera pulls back to reveal the whole realistic digestive system, which gently separates into
a floating exploded view, each organ slowly rotating, then smoothly reassembles. The background
fades from deep navy to a rich muted violet (#413B5D), with a small warm orange light accent
(#F38D38) in the lower right. The last two seconds are almost still, leaving clean empty space
in the center for a logo.
[bloc de style]
```
> Au montage : **logo Nemaudig** au centre, puis *Chirurgie digestive et viscérale · Nîmes · 04 66 05 24 63*

---

## Variante verticale (9:16, mobile et réseaux)

Même plans, en ajoutant au début de chaque prompt :
`Vertical 9:16 framing, organs centered in the upper two thirds, empty space at the bottom for titles.`

## Son (si la plateforme le propose)

```
Minimal cinematic ambient score, warm deep synth pad, slow piano notes, soft heartbeat-like low
pulse, hopeful and calm, no vocals, 30 seconds, gentle fade out.
```
Le film doit rester compréhensible sans le son.

---

## Ensuite

Dépose les 5 plans dans `nemaudig/videos-source/` (`plan-1.mp4` à `plan-5.mp4`) : je fais le
montage, les titres aux polices du site, le logo final, la compression web, et je te propose
une intégration discrète sur le site — uniquement si le résultat te plaît.
