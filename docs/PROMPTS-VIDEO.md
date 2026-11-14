# Vidéos IA — storyboards et prompts de génération

Cinq séquences à produire (Veo, Kling, Runway…). Aucune n'existe encore : le site affiche des
emplacements « Séquence en préparation ». Fichier généré par `build.py` depuis `data/videos_ia.py`.

## Règles communes

- **Image** : 16:9, 1920 × 1080, 24 images/s (prévoir un recadrage 9:16 pour le mobile)
- **Fichiers** : WebM (VP9 ou AV1) + MP4 (H.264) en secours, sans piste audio, image d'attente WebP
- **Poids** : Version courte ≤ 2,5 Mo, version détaillée ≤ 8 Mo ; chargement au clic uniquement
- **Sous-titres** : WebVTT en français, affichés par défaut ; transcription texte sous la vidéo (fichiers prêts dans `dist/videos/`)
- **Deux versions** : la courte suit le storyboard ; la détaillée reprend chaque plan en le ralentissant (×3 environ) et ajoute un texte d'accompagnement validé par l'équipe.
- **Méthode conseillée** : générer d'abord une image de référence par plan (capture de l'explorateur 3D du site), puis animer cette image (image-to-video) : l'anatomie reste celle du modèle réel.
- **Avant publication** : chaque séquence est relue par un chirurgien de l'équipe.

### Style commun (à placer à la fin de chaque prompt)

```
Scientific medical visualization, photoreal 3D render of translucent glass anatomy on a deep midnight-blue background (#050B1A), soft cyan and turquoise rim light, subtle silver reflections, thin precise light lines, shallow depth of field, slow and steady camera move, calm premium mood, anatomically accurate proportions, clean and clinical. No blood, no gore, no surgery, no people, no faces, no text, no captions, no logos, no cartoon style, no flicker, no fast cuts.
```

### Prompt négatif

```
text, letters, watermark, logo, cartoon, toy-like, glitter, neon overload, blood, wounds, surgical instruments cutting tissue, human face, extra organs, wrong anatomy, mirrored anatomy, flicker, strobing, shaky camera, fast zoom, lens flare overload
```

## 01 — Voyage dans le système digestif

Une traversée continue de la bouche au côlon, pour situer chaque organe.

Durée : 24 s (courte) · 75 s (détaillée) — sous-titres : `videos/voyage.fr.vtt`

| Temps | À l'image | Sous-titre |
|---|---|---|
| 00–04 s | Silhouette de verre du tronc ; les organes digestifs s'allument un à un, de haut en bas. | Le système digestif mesure plusieurs mètres. |
| 04–09 s | La caméra descend le long de l'œsophage, tube fin et vertical. | L'œsophage conduit les aliments jusqu'à l'estomac. |
| 09–14 s | Arrivée dans l'estomac : la poche se contracte doucement. | L'estomac les brasse et commence la digestion. |
| 14–19 s | Passage près du foie et du pancréas, reliés au duodénum par de fins canaux. | Le foie et le pancréas apportent bile et enzymes. |
| 19–24 s | Travelling arrière : les anses de l'intestin grêle, puis le cadre du côlon. | L'intestin absorbe ; le côlon termine le travail. |

**Prompt**

```
Continuous slow descending camera travel through a translucent glass model of the human digestive tract: starting on the whole torso silhouette as the organs light up one after another from top to bottom, gliding down along the thin vertical esophagus, arriving at the J-shaped stomach which contracts gently, passing the large wedge-shaped liver on the viewer's left with the small gallbladder beneath it and the elongated pancreas behind the stomach, then pulling back to reveal the coiled small intestine framed by the large intestine. Scientific medical visualization, photoreal 3D render of translucent glass anatomy on a deep midnight-blue background (#050B1A), soft cyan and turquoise rim light, subtle silver reflections, thin precise light lines, shallow depth of field, slow and steady camera move, calm premium mood, anatomically accurate proportions, clean and clinical. No blood, no gore, no surgery, no people, no faces, no text, no captions, no logos, no cartoon style, no flicker, no fast cuts.
```

**À vérifier avant publication**

- [ ] Foie à droite du patient (à gauche de l'image), estomac à gauche du patient
- [ ] Ordre des organes : œsophage, estomac, duodénum, grêle, côlon, rectum
- [ ] Le côlon encadre bien l'intestin grêle ; pas d'organe en double

## 02 — Comprendre la gastroscopie

Le principe de l'examen, ce qu'il permet de voir et ses grandes étapes.

Durée : 22 s (courte) · 80 s (détaillée) — sous-titres : `videos/gastroscopie.fr.vtt`

| Temps | À l'image | Sous-titre |
|---|---|---|
| 00–04 s | Coupe de profil stylisée : bouche, œsophage, estomac, en verre translucide. | La gastroscopie explore l'œsophage, l'estomac et le duodénum. |
| 04–09 s | Un endoscope souple et fin, à l'extrémité lumineuse, descend dans l'œsophage. | Un endoscope souple est introduit par la bouche. |
| 09–14 s | L'extrémité éclaire l'intérieur de l'estomac ; le faisceau balaie lentement la paroi. | Sa caméra examine la paroi, millimètre par millimètre. |
| 14–18 s | Gros plan : un point de la paroi est repéré par un fin cercle lumineux. | Si besoin, un prélèvement indolore est réalisé. |
| 18–22 s | L'endoscope se retire ; la coupe complète réapparaît, apaisée. | L'examen dure quelques minutes. |

**Prompt**

```
Side cutaway view of a translucent glass human upper digestive tract (mouth, esophagus, stomach, duodenum). A thin flexible endoscope with a small glowing tip slowly descends through the esophagus into the stomach, its soft light gently sweeping the inner wall; a thin luminous ring marks one small spot on the wall; then the endoscope withdraws smoothly. Scientific medical visualization, photoreal 3D render of translucent glass anatomy on a deep midnight-blue background (#050B1A), soft cyan and turquoise rim light, subtle silver reflections, thin precise light lines, shallow depth of field, slow and steady camera move, calm premium mood, anatomically accurate proportions, clean and clinical. No blood, no gore, no surgery, no people, no faces, no text, no captions, no logos, no cartoon style, no flicker, no fast cuts.
```

**À vérifier avant publication**

- [ ] Endoscope fin et souple, introduit par la bouche (pas par le nez)
- [ ] Aucun geste tranchant, aucune représentation de sang
- [ ] Durée et modalités d'anesthésie : texte validé par l'équipe

## 03 — Comprendre la coloscopie

Le côlon, la progression de l'endoscope et la détection d'un polype.

Durée : 24 s (courte) · 85 s (détaillée) — sous-titres : `videos/coloscopie.fr.vtt`

| Temps | À l'image | Sous-titre |
|---|---|---|
| 00–04 s | Le cadre du côlon en verre, vu de face : droit, transverse, gauche, sigmoïde, rectum. | Le côlon encadre l'abdomen sur plus d'un mètre. |
| 04–10 s | Un endoscope souple progresse du rectum vers le côlon droit ; un trait lumineux suit son trajet. | L'endoscope parcourt tout le côlon. |
| 10–15 s | Vue intérieure : paroi lisse à plis réguliers ; une petite excroissance arrondie apparaît. | Un polype est une petite excroissance de la paroi. |
| 15–20 s | Un fin anneau lumineux entoure le polype, qui s'efface en douceur. | Il est retiré pendant l'examen, puis analysé. |
| 20–24 s | Retour à la vue d'ensemble ; le trait lumineux se retire. | Retirer les polypes prévient le cancer colorectal. |

**Prompt**

```
Front view of a translucent glass human large intestine framing the abdomen. A thin flexible endoscope with a glowing tip advances slowly from the rectum through the sigmoid, descending, transverse and ascending colon, leaving a soft line of light. Cut to an interior view of a clean smooth colon wall with regular folds where a small rounded polyp appears; a thin ring of light encircles it and it gently fades away. Scientific medical visualization, photoreal 3D render of translucent glass anatomy on a deep midnight-blue background (#050B1A), soft cyan and turquoise rim light, subtle silver reflections, thin precise light lines, shallow depth of field, slow and steady camera move, calm premium mood, anatomically accurate proportions, clean and clinical. No blood, no gore, no surgery, no people, no faces, no text, no captions, no logos, no cartoon style, no flicker, no fast cuts.
```

**À vérifier avant publication**

- [ ] Progression du rectum vers le cæcum (et non l'inverse)
- [ ] Polype petit, arrondi, sans aspect inquiétant ni sang
- [ ] Ne pas suggérer que tout polype est un cancer

## 04 — Le foie et ses fonctions

Épurer le sang, fabriquer, stocker, produire la bile : quatre fonctions en images.

Durée : 22 s (courte) · 70 s (détaillée) — sous-titres : `videos/foie.fr.vtt`

| Temps | À l'image | Sous-titre |
|---|---|---|
| 00–04 s | Le foie en verre tourne lentement, la vésicule visible en dessous. | Le foie est le plus gros organe de l'abdomen. |
| 04–09 s | Un flux de particules bleutées arrive de l'intestin par une large veine. | Il reçoit le sang venu de l'intestin. |
| 09–14 s | Les particules traversent le foie et ressortent plus claires vers le haut. | Il l'épure, transforme et stocke les nutriments. |
| 14–18 s | Un fin canal turquoise s'illumine du foie vers la vésicule, puis vers l'intestin. | Il fabrique la bile, qui aide à digérer les graisses. |
| 18–22 s | Le foie entier pulse d'une lumière douce et régulière. | Il peut se régénérer après une opération. |

**Prompt**

```
A translucent glass human liver slowly rotating, with the small gallbladder beneath it. A stream of soft blue light particles flows into the liver through a wide vein coming from below, spreads through the organ and exits upward looking clearer and brighter; then a thin turquoise duct lights up from the liver to the gallbladder and onward toward the intestine; the liver glows with a calm steady light. Scientific medical visualization, photoreal 3D render of translucent glass anatomy on a deep midnight-blue background (#050B1A), soft cyan and turquoise rim light, subtle silver reflections, thin precise light lines, shallow depth of field, slow and steady camera move, calm premium mood, anatomically accurate proportions, clean and clinical. No blood, no gore, no surgery, no people, no faces, no text, no captions, no logos, no cartoon style, no flicker, no fast cuts.
```

**À vérifier avant publication**

- [ ] Veine porte : arrivée par le bas ; veines hépatiques : sortie vers le haut
- [ ] Bile : du foie vers la vésicule et le duodénum
- [ ] Forme du foie : lobe droit plus volumineux, à gauche de l'image

## 05 — Prévention et dépistage

L'intérêt du dépistage organisé du cancer colorectal, de 50 à 74 ans.

Durée : 26 s (courte) · 80 s (détaillée) — sous-titres : `videos/depistage.fr.vtt`

| Temps | À l'image | Sous-titre |
|---|---|---|
| 00–05 s | Le côlon en verre ; un minuscule point apparaît sur sa paroi et grandit très lentement. | Un cancer colorectal se développe lentement, souvent sans signe. |
| 05–10 s | Une frise sobre de 50 à 74 se dessine, avec un repère tous les deux ans. | De 50 à 74 ans, un test est proposé tous les deux ans. |
| 10–15 s | Un kit de test stylisé, posé sur une surface claire, s'illumine. | Le test se fait chez soi, en quelques minutes. |
| 15–20 s | Deux chemins : l'un continue la frise, l'autre mène vers le côlon et un endoscope. | S'il est positif, une coloscopie est nécessaire. |
| 20–26 s | Le point sur la paroi s'efface ; le côlon retrouve une lumière uniforme. | Détecté tôt, ce cancer se guérit dans 9 cas sur 10. |

**Prompt**

```
A translucent glass human large intestine on a deep midnight-blue background; a tiny point of warm light appears on its wall and grows very slowly. A minimal thin timeline draws itself with evenly spaced markers. A simple stylized home test kit rests on a clean pale surface and softly lights up. The point of light on the colon wall fades away and the organ returns to an even calm glow. Scientific medical visualization, photoreal 3D render of translucent glass anatomy on a deep midnight-blue background (#050B1A), soft cyan and turquoise rim light, subtle silver reflections, thin precise light lines, shallow depth of field, slow and steady camera move, calm premium mood, anatomically accurate proportions, clean and clinical. No blood, no gore, no surgery, no people, no faces, no text, no captions, no logos, no cartoon style, no flicker, no fast cuts.
```

**À vérifier avant publication**

- [ ] Chiffres et tranche d'âge conformes aux recommandations en vigueur (INCa, Assurance Maladie)
- [ ] Aucun texte généré par l'IA à l'image : les chiffres sont ajoutés au montage
- [ ] « 9 cas sur 10 » : formulation et source à valider par l'équipe
