# Contenus à valider avant mise en ligne

Sur le site, tout élément provisoire porte le symbole ◇. Cette liste les regroupe.

## 1. Point de départ à confirmer

- **Nemaudig est un cabinet de chirurgiens digestifs et viscéraux**, pas de gastro-entérologues (source : nemaudig.fr).
  Le site parle donc de chirurgie ; la gastroscopie, la coloscopie et l'écho-endoscopie sont présentées comme des
  examens *prescrits*, réalisés par des gastro-entérologues. Si l'équipe réalise elle-même certains de ces actes,
  il suffit de modifier `REALISE_PAR` dans `data/examens.py`.

## 2. Relecture médicale (textes rédigés pour la maquette)

| Contenu | Fichier | Sources utilisées |
|---|---|---|
| Fiches des 8 organes : fonctionnement, signes, examens, traitements | `data/organes.py` | Repères publics HAS, Assurance Maladie, SNFGE |
| Foie : stéatose, hépatites, fibrose, cirrhose | `data/organes.py` (`maladies`) | idem |
| Côlon : polypes, dépistage, préparation, prévention | `data/organes.py` (`encarts`) | INCa, Assurance Maladie |
| Gastroscopie, coloscopie, écho-endoscopie | `data/examens.py` | Fiches d'information SFED, Assurance Maladie |
| Durées d'examen, modalités d'anesthésie, consignes de jeûne | `data/examens.py` | à valider avec les gastro-entérologues et anesthésistes |
| Écho-endoscopie : 5 rubriques laissées vides | `data/examens.py` | à compléter |
| Dépistage du cancer colorectal (50-74 ans, tous les 2 ans) | `pages/pratique.py` | INCa, Assurance Maladie |
| « Détecté tôt, ce cancer se guérit dans 9 cas sur 10 » (storyboard vidéo 5) | `data/videos_ia.py` | INCa — formulation à valider |
| Six conseils de prévention | `pages/pratique.py` | INCa |
| Trois schémas animés (estomac, foie, coloscopie) | `lib/schemas.py` | schémas de principe |

## 3. Attributions proposées (déduites des spécialités affichées sur nemaudig.fr)

- Chirurgien référent par organe dans l'explorateur (`data/organes.py`, `chirurgiens`).
- « Dans l'équipe » sur chaque fiche de pathologie et « Domaines en lien avec son activité » sur chaque fiche de chirurgien.
- Chirurgiens proposés par domaine dans l'orientation du rendez-vous.

## 4. Informations à fournir par le cabinet

- Liens de prise de rendez-vous en ligne **par chirurgien** (aujourd'hui : lien général Maiia).
- Liste des documents à apporter en consultation (`data/examens.py`, `DOCUMENTS`).
- Honoraires : date de mise à jour (70 € / 50 € / 30 € repris du site actuel).
- Numéros RPPS, hébergeur, adresse de contact pour les droits RGPD.
- Photographies des locaux et de l'équipe paramédicale.
- Position exacte du cabinet sur la carte (coordonnées approximatives).
- Rôle de la Clinique Kennedy (citée sur l'ancien site, non reprise ici).

## 5. Vidéos

Aucune vidéo n'est produite. Les cinq emplacements affichent « Séquence en préparation » avec une image d'organe générée par IA.
Storyboards, prompts, sous-titres et points de contrôle médical : `docs/PROMPTS-VIDEO.md`.

## 6. Déjà vérifié (repris du site actuel, comme pour les maquettes A et B)

Identité et parcours des cinq chirurgiens, 24 fiches de pathologies, parcours obésité, techniques opératoires,
établissements, coordonnées, horaires, démarches, actualités, questions fréquentes des fiches.
