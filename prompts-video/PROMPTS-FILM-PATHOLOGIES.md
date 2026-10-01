# Film « Le parcours digestif » — prompts pour davinci.ai

Film immersif d'environ **90 secondes** : la caméra entre dans un corps de verre, distingue
chaque organe par sa couleur et **s'arrête sur chaque organe** pour montrer, de façon stylisée,
les pathologies que l'équipe Nemaudig opère. Chaque arrêt correspond à une fiche du site.

Les générateurs vidéo produisent des plans de 5 à 10 s : le film est donc découpé en **14 plans**,
à générer un par un puis à monter. Les prompts sont en anglais (meilleurs résultats) ; les textes
à l'écran sont en français et **seront ajoutés au montage**, jamais générés dans l'image.

---

## 1. Règles du film (à garder en tête à chaque génération)

**Ce que l'on montre** : une illustration médicale premium, stylisée, rassurante. Les maladies sont
évoquées par la lumière (une zone qui s'allume, une forme qui change), jamais de façon réaliste.

**Ce que l'on ne montre jamais** : sang, chair, plaie, tumeur réaliste, geste chirurgical réel,
personne, visage, logo de marque (y compris celui du robot), texte dans l'image.

**Code couleur des organes — identique au site** (c'est ce qui « différencie » les organes) :

| Organe | Couleur | Hex |
|---|---|---|
| Œsophage | rose poudré | `#E7B2BF` |
| Estomac | lavande | `#C5AEF0` |
| Foie | pêche | `#E7A090` |
| Vésicule biliaire | vert sauge | `#A9CF7C` |
| Pancréas | sable doré | `#F2CD8F` |
| Intestin grêle | rose tendre | `#F1AEBD` |
| Côlon, sigmoïde, rectum | menthe | `#8FD6C0` |
| Glandes surrénales | jaune pâle | `#F0D27A` |
| Corps de verre, lumières, balayage | lagon | `#2BB3A7` |
| Fond | nuit | `#07131C` |

**Lumière « pathologie »** : une teinte ambre douce `#FFB86B` sert à signaler la zone malade sur
tous les plans. Toujours la même, pour que le spectateur l'identifie sans texte.

---

## 2. Bloc de style (à coller à la fin de chaque prompt)

```
Cinematic premium medical 3D animation, stylized and elegant, never realistic surgery.
A translucent glass human torso with a soft teal rim light (#2BB3A7) floats in deep navy space
(#07131C) with drifting teal dust particles and soft out-of-focus bokeh in the foreground.
Faint glass ribs and spine in the background. Organs are smooth, glossy, slightly organic
clay-like volumes with clearcoat reflections and subtle surface texture, each with its own pastel
color: esophagus powder pink, stomach lavender, liver peach, gallbladder sage green, pancreas
golden sand, small intestine soft pink, colon mint green with visible soft haustral folds.
Shot on an anamorphic lens: shallow depth of field, gentle lens breathing, subtle film grain,
soft vignette, delicate bloom on highlights, volumetric light. Slow, smooth, weightless camera
motion. Calm, precise, reassuring mood. 4K, ultra detailed, 24 fps.
```

## 3. Prompt négatif (si l'outil en accepte un)

```
blood, gore, raw flesh, wound, realistic tumor, realistic surgery, scalpel, needle, gloves,
hands, person, doctor, face, skull, full skeleton, text, letters, numbers, subtitles, watermark,
logo, brand, cartoon, low poly, plastic toy look, harsh light, flicker, fast camera, shaky camera,
glitch, morphing artifacts, distorted anatomy, extra organs, oversaturated colors
```

## 4. Images de départ (image vers vidéo)

| Fichier | Usage |
|---|---|
| `ref-cinema-16x9.png` | Style du film (bandes cinéma, grain, côlon bosselé) : plans 1, 2, 14 |
| `ref-intro-16x9.png` | Vue d'ensemble nette : plans 2, 11, 13 |
| `ref-estomac-16x9.png` | Plans 3, 4 |
| `ref-colon-16x9.png` | Plans 8, 9, 10 |
| `ref-intro-9x16.png` | Toute la version verticale |

**Continuité** : pour chaque plan, utiliser la **dernière image du plan précédent** comme image de
départ. C'est la clé d'un film fluide. Garder le même « seed » d'un plan à l'autre si l'outil le permet.

---

## 5. Les 14 plans

### Plan 01 — Ouverture · 6 s
```
Total darkness. Tiny teal light particles slowly gather and draw the outline of a translucent
glass human torso floating in deep space, above three thin glowing concentric rings. A thin
horizontal teal scanning line sweeps slowly from top to bottom, revealing the torso.
Slow push-in.
[style block]
```
> Texte à l'écran : *Au cœur de l'appareil digestif*

### Plan 02 — Les organes s'allument un par un · 8 s
```
Inside the glass torso, the digestive organs appear one after another from top to bottom, each
lighting up in its own pastel color as the scanning line passes: esophagus, stomach, liver,
gallbladder, pancreas, small intestine, colon, rectum. The camera slowly orbits 25 degrees.
Each organ is clearly distinct and separated by soft shadows.
[style block]
```
> Texte : *De l'œsophage au rectum, tous ces organes sont pris en charge par l'équipe*

### Plan 03 — Arrêt « Œsophage » · 7 s → `/pathologies/oesophage-estomac/`
```
The camera glides up and stops on the powder-pink esophagus where it passes through a thin
glowing ring (the diaphragm opening) to join the lavender stomach. A soft amber light wave
gently rises from the stomach into the lower esophagus, then fades (acid reflux). Then the top of
the stomach slowly slides upward through the glowing ring into the chest area, highlighted in
amber (hiatal hernia). Slow, precise, educational.
[style block]
```
> Texte : *Reflux · Hernie hiatale · Cancer de l'œsophage*

### Plan 04 — Arrêt « Estomac » · 7 s → `/pathologies/cancer-de-l-estomac/`
```
Close, slow orbit around the glossy lavender stomach, its soft inner folds visible through a
slightly translucent wall. A small discreet zone on its wall softly glows amber, surrounded by a
thin teal circle, like a precise diagnostic highlight. Calm and reassuring, no realistic tumor.
[style block]
```
> Texte : *Cancer de l'estomac — chaque dossier discuté en réunion pluridisciplinaire*

### Plan 05 — Arrêt « Obésité » : sleeve et bypass · 8 s → `/obesite/`
```
The lavender stomach floats in the center. Left half of the frame: a translucent cut line
appears and about two thirds of the stomach dissolve into light particles, leaving a slim vertical
tube (sleeve gastrectomy). Right half: the stomach reduces to a small pouch connected by a glowing
path to a loop of soft pink small intestine shaped like a "Y" (gastric bypass). Clean,
diagrammatic, elegant, slow.
[style block]
```
> Texte : *Ballon intragastrique · Sleeve · Bypass · Anneau*

### Plan 06 — Arrêt « Foie » · 7 s → `/pathologies/foie/`
```
The camera turns toward the large peach liver. Three fine glowing vessels enter it from below
and branch into both halves: one coral (artery), one blue-violet (vein), one green (bile duct),
light pulses travelling along them. Then a thin section of the liver edge gently regrows with
soft particles (the liver regenerates). Slow and majestic.
[style block]
```
> Texte : *Un organe indispensable à la vie — il repousse en plusieurs semaines*

### Plan 07 — Arrêt « Vésicule biliaire » · 7 s → `/pathologies/vesicule-biliaire/`
```
Close-up under the liver on the sage-green gallbladder, slightly translucent: inside, a few small
pearl-like stones glow softly amber. Then four tiny glowing points of light appear on the surface
of the glass torso and four slender beams of light reach the gallbladder, which gently lifts away
and dissolves into light (minimally invasive laparoscopic removal, stylized).
[style block]
```
> Texte : *Calculs de la vésicule · Cholécystectomie par cœlioscopie, souvent en ambulatoire*

### Plan 08 — Arrêt « Pancréas » · 7 s → `/pathologies/cancer-du-pancreas/`
```
The lavender stomach and peach liver slowly float upward and aside, revealing the hidden golden
pancreas lying deep behind them, its head nested in the curve of the duodenum. A thin green duct
crosses its head with a light pulse. A small discreet zone glows amber in the head of the pancreas.
Mysterious, revealing, slow.
[style block]
```
> Texte : *L'organe caché — il fabrique l'insuline et des enzymes de la digestion*

### Plan 09 — Arrêt « Intestin grêle » · 7 s → `/pathologies/mici/`
```
The camera travels slowly along the soft pink coils of the small intestine floating in the
abdomen. A few separate segments glow with a warm amber inflammation light, with healthy pink
segments in between (Crohn's disease affects segments). Gentle, fluid tracking shot.
[style block]
```
> Texte : *Maladie de Crohn, rectocolite — les MICI*

### Plan 10 — Arrêt « Côlon » · 8 s → `/pathologies/colon-rectum/`
```
Smooth tracking shot along the mint-green colon with its soft haustral folds, rising on one side,
crossing the top, descending the other side. On the final S-shaped curve (sigmoid colon), several
tiny round pouches bulge outward from the wall and glow amber (diverticula). A teal light pulse
travels along the colon with the camera.
[style block]
```
> Texte : *Diverticulite · Cancer du côlon · Chirurgie colique par cœlioscopie ou robot*

### Plan 11 — Arrêt « Rectum et anus » · 6 s → `/pathologies/proctologie/`
```
The camera descends gently to the lower pelvis: the mint rectum, a short reservoir, ends in a
thin glowing teal muscular ring (the sphincter). The whole area is softly highlighted in amber,
discreet and respectful, seen from a slight distance. No detail of the skin.
[style block]
```
> Texte : *Cancer du rectum · Hémorroïdes · Fissure · Fistule · Kyste pilonidal*

### Plan 12 — Arrêt « Paroi abdominale » (hernies) · 7 s → `/pathologies/paroi-abdominale/`
```
The camera moves outside the glass torso to the lower abdomen. In the groin area, a soft bulge
pushes outward through a small weak opening in the glass wall, glowing amber (inguinal hernia).
Then a fine glowing teal mesh appears and gently settles over the opening, smoothing the wall
back (hernia repair with mesh). A second, smaller bulge near the navel softens the same way.
[style block]
```
> Texte : *Hernie inguinale · Hernie ombilicale · Éventration*

### Plan 13 — Les techniques : cœlioscopie, robot, 3D · 8 s → `/techniques/`
```
Wide shot of the glass torso. Four or five tiny luminous entry points appear on the abdomen, and
slender instruments made of pure light enter delicately (laparoscopy). Around the torso, the
elegant silhouettes of three robotic arms made of thin teal light lines move with precision
(robot-assisted surgery, no brand, no logo). Everything glows softly in 3D depth.
[style block]
```
> Texte : *Cœlioscopie 3D 4K · Robot chirurgical · Chirurgie ambulatoire*

### Plan 14 — Final · 6 s
```
The camera slowly pulls back. All organs glow together in their pastel colors, perfectly in place
inside the glass torso floating above the three glowing rings. The scanning line passes one last
time. The last two seconds are almost still, leaving calm empty space on the right of the frame.
[style block]
```
> Texte : *Cinq chirurgiens, une seule équipe · Nîmes · 04 66 05 24 63*

---

## 6. Version courte (30 s, accueil et réseaux sociaux)

Plans **01 → 02 → 05 → 07 → 10 → 12 → 14**, chacun raccourci à 4 s au montage.

## 7. Version verticale (9:16, mobile et réseaux)

Même liste, en ajoutant au début de chaque prompt :
`Vertical 9:16 framing, the subject centered in the upper two thirds of the frame.`
Image de départ : `ref-intro-9x16.png`.

---

## 8. Son (si la plateforme génère l'audio)

**Ambiance musicale** :
```
Minimal cinematic ambient score, soft warm synth pads, slow piano notes, gentle low pulse like a
calm heartbeat, airy and hopeful, no drums, no vocals, 90 seconds, fades out at the end.
```
**Effets** : légers « whoosh » de verre sur les mouvements de caméra, un « ping » cristallin discret à
chaque arrêt sur un organe. Le film doit rester compréhensible **sans le son** : sur le site, il sera muet par défaut.

**Voix off (facultative)** — texte uniquement issu du site actuel, à faire valider par les médecins :
> « De l'œsophage au rectum, chaque organe a son rôle… L'œsophage relie la bouche à l'estomac.
> L'estomac commande l'appétit. Le foie épure le sang, fabrique des protéines : il est indispensable
> à la vie. Caché derrière l'estomac, le pancréas fabrique l'insuline. C'est dans l'intestin que les
> aliments sont absorbés… Cinq chirurgiens, une seule équipe, à Nîmes. »

---

## 9. Ce que tu aurais pu oublier

1. **Les hernies et la paroi abdominale** (plan 12) : c'est l'une des opérations les plus fréquentes
   du cabinet, et elle n'apparaît pas dans le voyage 3D actuel.
2. **La chirurgie de l'obésité** (plan 5) et le **ballon Allurion** : c'est la dernière nouveauté du cabinet.
3. **Les techniques** (plan 13) : robot, cœlioscopie 3D 4K des Franciscaines, ambulatoire. Ce sont les
   arguments de modernité du site.
4. **Aucun texte généré dans l'image** : les IA écrivent mal le français. Les titres sont ajoutés au
   montage, et repris en HTML sur la page, pour Google et pour l'accessibilité.
5. **Les cancers montrés avec douceur** : une zone ambre cerclée, jamais une tumeur. Des patients
   inquiets regarderont ce film.
6. **La mention « Illustration animée — ne remplace pas une consultation »** sous la vidéo.
7. **La validation par les médecins** du film terminé (exactitude anatomique, ton) avant la mise en ligne.
8. **La continuité** : dernière image d'un plan = image de départ du suivant ; même seed.
9. **Une image d'affiche** (le plan 14) pour l'affichage avant lecture et pour le partage sur les réseaux.
10. **Le poids** : film complet < 8 Mo et version courte < 4 Mo en WebM/MP4. Je m'occupe de la compression.
11. **Les droits de la musique** : vérifier que la piste générée est utilisable commercialement.
12. **Une version sans texte** des plans, réutilisable pour Instagram, Facebook ou un écran en salle d'attente.

---

## 10. Intégration prévue sur le site

- Film en lecture automatique, muet, en boucle, en ouverture du voyage 3D. Bouton « Activer le son »,
  sous-titres en WebVTT et transcription pour l'accessibilité.
- **Chapitres cliquables** sous la vidéo, un par arrêt, chacun menant à la fiche correspondante
  (liens indiqués après chaque plan ci-dessus). Les timecodes seront fixés au montage.
- Option : la vidéo avance avec le défilement et marque une pause sur chaque organe, en restant
  synchronisée avec les cartes explicatives.
- Pas de lecture automatique si le visiteur a demandé moins d'animations ou active l'économie de
  données : l'image d'affiche et la 3D prennent le relais.

**Une fois les plans générés**, dépose-les dans `nemaudig/videos-source/`, nommés `plan-01.mp4` à
`plan-14.mp4` : je fais le montage, les titres, la compression et l'intégration.
