"""Cinq séquences vidéo à produire par IA (Veo, Kling, Runway…) — storyboards et prompts.

Aucune de ces vidéos n'existe encore : le site affiche des emplacements marqués
« Séquence en préparation ». build.py en tire docs/PROMPTS-VIDEO.md et les sous-titres
WebVTT de la version courte (dist/videos/<id>.fr.vtt).

Chaque plan : (durée en secondes, ce que l'on voit, sous-titre affiché).
Les prompts sont rédigés en anglais (langue la mieux comprise par les générateurs).
Toute séquence générée doit être RELUE PAR UN MÉDECIN avant publication : ces outils
représentent parfois mal l'anatomie ou les gestes (voir `verifier`).
"""

STYLE = (
    "Scientific medical visualization, photoreal 3D render of translucent glass anatomy on a deep midnight-blue "
    "background (#050B1A), soft cyan and turquoise rim light, subtle silver reflections, thin precise light lines, "
    "shallow depth of field, slow and steady camera move, calm premium mood, anatomically accurate proportions, "
    "clean and clinical. No blood, no gore, no surgery, no people, no faces, no text, no captions, no logos, "
    "no cartoon style, no flicker, no fast cuts."
)

NEGATIF = (
    "text, letters, watermark, logo, cartoon, toy-like, glitter, neon overload, blood, wounds, surgical instruments "
    "cutting tissue, human face, extra organs, wrong anatomy, mirrored anatomy, flicker, strobing, shaky camera, "
    "fast zoom, lens flare overload"
)

FORMAT = {
    "image": "16:9, 1920 × 1080, 24 images/s (prévoir un recadrage 9:16 pour le mobile)",
    "fichiers": "WebM (VP9 ou AV1) + MP4 (H.264) en secours, sans piste audio, image d'attente WebP",
    "poids": "Version courte ≤ 2,5 Mo, version détaillée ≤ 8 Mo ; chargement au clic uniquement",
    "sous_titres": "WebVTT en français, affichés par défaut ; transcription texte sous la vidéo",
}

VIDEOS = [
    {
        "id": "voyage", "numero": "01", "titre": "Voyage dans le système digestif",
        "objet": "Une traversée continue de la bouche au côlon, pour situer chaque organe.",
        "courte": 24, "detaillee": 75, "organe": "estomac",
        "plans": [
            (4, "Silhouette de verre du tronc ; les organes digestifs s'allument un à un, de haut en bas.", "Le système digestif mesure plusieurs mètres."),
            (5, "La caméra descend le long de l'œsophage, tube fin et vertical.", "L'œsophage conduit les aliments jusqu'à l'estomac."),
            (5, "Arrivée dans l'estomac : la poche se contracte doucement.", "L'estomac les brasse et commence la digestion."),
            (5, "Passage près du foie et du pancréas, reliés au duodénum par de fins canaux.", "Le foie et le pancréas apportent bile et enzymes."),
            (5, "Travelling arrière : les anses de l'intestin grêle, puis le cadre du côlon.", "L'intestin absorbe ; le côlon termine le travail."),
        ],
        "prompt": "Continuous slow descending camera travel through a translucent glass model of the human digestive tract: starting on the whole torso silhouette as the organs light up one after another from top to bottom, gliding down along the thin vertical esophagus, arriving at the J-shaped stomach which contracts gently, passing the large wedge-shaped liver on the viewer's left with the small gallbladder beneath it and the elongated pancreas behind the stomach, then pulling back to reveal the coiled small intestine framed by the large intestine.",
        "verifier": [
            "Foie à droite du patient (à gauche de l'image), estomac à gauche du patient",
            "Ordre des organes : œsophage, estomac, duodénum, grêle, côlon, rectum",
            "Le côlon encadre bien l'intestin grêle ; pas d'organe en double",
        ],
    },
    {
        "id": "gastroscopie", "numero": "02", "titre": "Comprendre la gastroscopie",
        "objet": "Le principe de l'examen, ce qu'il permet de voir et ses grandes étapes.",
        "courte": 22, "detaillee": 80, "organe": "oesophage",
        "plans": [
            (4, "Coupe de profil stylisée : bouche, œsophage, estomac, en verre translucide.", "La gastroscopie explore l'œsophage, l'estomac et le duodénum."),
            (5, "Un endoscope souple et fin, à l'extrémité lumineuse, descend dans l'œsophage.", "Un endoscope souple est introduit par la bouche."),
            (5, "L'extrémité éclaire l'intérieur de l'estomac ; le faisceau balaie lentement la paroi.", "Sa caméra examine la paroi, millimètre par millimètre."),
            (4, "Gros plan : un point de la paroi est repéré par un fin cercle lumineux.", "Si besoin, un prélèvement indolore est réalisé."),
            (4, "L'endoscope se retire ; la coupe complète réapparaît, apaisée.", "L'examen dure quelques minutes."),
        ],
        "prompt": "Side cutaway view of a translucent glass human upper digestive tract (mouth, esophagus, stomach, duodenum). A thin flexible endoscope with a small glowing tip slowly descends through the esophagus into the stomach, its soft light gently sweeping the inner wall; a thin luminous ring marks one small spot on the wall; then the endoscope withdraws smoothly.",
        "verifier": [
            "Endoscope fin et souple, introduit par la bouche (pas par le nez)",
            "Aucun geste tranchant, aucune représentation de sang",
            "Durée et modalités d'anesthésie : texte validé par l'équipe",
        ],
    },
    {
        "id": "coloscopie", "numero": "03", "titre": "Comprendre la coloscopie",
        "objet": "Le côlon, la progression de l'endoscope et la détection d'un polype.",
        "courte": 24, "detaillee": 85, "organe": "colon",
        "plans": [
            (4, "Le cadre du côlon en verre, vu de face : droit, transverse, gauche, sigmoïde, rectum.", "Le côlon encadre l'abdomen sur plus d'un mètre."),
            (6, "Un endoscope souple progresse du rectum vers le côlon droit ; un trait lumineux suit son trajet.", "L'endoscope parcourt tout le côlon."),
            (5, "Vue intérieure : paroi lisse à plis réguliers ; une petite excroissance arrondie apparaît.", "Un polype est une petite excroissance de la paroi."),
            (5, "Un fin anneau lumineux entoure le polype, qui s'efface en douceur.", "Il est retiré pendant l'examen, puis analysé."),
            (4, "Retour à la vue d'ensemble ; le trait lumineux se retire.", "Retirer les polypes prévient le cancer colorectal."),
        ],
        "prompt": "Front view of a translucent glass human large intestine framing the abdomen. A thin flexible endoscope with a glowing tip advances slowly from the rectum through the sigmoid, descending, transverse and ascending colon, leaving a soft line of light. Cut to an interior view of a clean smooth colon wall with regular folds where a small rounded polyp appears; a thin ring of light encircles it and it gently fades away.",
        "verifier": [
            "Progression du rectum vers le cæcum (et non l'inverse)",
            "Polype petit, arrondi, sans aspect inquiétant ni sang",
            "Ne pas suggérer que tout polype est un cancer",
        ],
    },
    {
        "id": "foie", "numero": "04", "titre": "Le foie et ses fonctions",
        "objet": "Épurer le sang, fabriquer, stocker, produire la bile : quatre fonctions en images.",
        "courte": 22, "detaillee": 70, "organe": "foie",
        "plans": [
            (4, "Le foie en verre tourne lentement, la vésicule visible en dessous.", "Le foie est le plus gros organe de l'abdomen."),
            (5, "Un flux de particules bleutées arrive de l'intestin par une large veine.", "Il reçoit le sang venu de l'intestin."),
            (5, "Les particules traversent le foie et ressortent plus claires vers le haut.", "Il l'épure, transforme et stocke les nutriments."),
            (4, "Un fin canal turquoise s'illumine du foie vers la vésicule, puis vers l'intestin.", "Il fabrique la bile, qui aide à digérer les graisses."),
            (4, "Le foie entier pulse d'une lumière douce et régulière.", "Il peut se régénérer après une opération."),
        ],
        "prompt": "A translucent glass human liver slowly rotating, with the small gallbladder beneath it. A stream of soft blue light particles flows into the liver through a wide vein coming from below, spreads through the organ and exits upward looking clearer and brighter; then a thin turquoise duct lights up from the liver to the gallbladder and onward toward the intestine; the liver glows with a calm steady light.",
        "verifier": [
            "Veine porte : arrivée par le bas ; veines hépatiques : sortie vers le haut",
            "Bile : du foie vers la vésicule et le duodénum",
            "Forme du foie : lobe droit plus volumineux, à gauche de l'image",
        ],
    },
    {
        "id": "depistage", "numero": "05", "titre": "Prévention et dépistage",
        "objet": "L'intérêt du dépistage organisé du cancer colorectal, de 50 à 74 ans.",
        "courte": 26, "detaillee": 80, "organe": "colon",
        "plans": [
            (5, "Le côlon en verre ; un minuscule point apparaît sur sa paroi et grandit très lentement.", "Un cancer colorectal se développe lentement, souvent sans signe."),
            (5, "Une frise sobre de 50 à 74 se dessine, avec un repère tous les deux ans.", "De 50 à 74 ans, un test est proposé tous les deux ans."),
            (5, "Un kit de test stylisé, posé sur une surface claire, s'illumine.", "Le test se fait chez soi, en quelques minutes."),
            (5, "Deux chemins : l'un continue la frise, l'autre mène vers le côlon et un endoscope.", "S'il est positif, une coloscopie est nécessaire."),
            (6, "Le point sur la paroi s'efface ; le côlon retrouve une lumière uniforme.", "Détecté tôt, ce cancer se guérit dans 9 cas sur 10."),
        ],
        "prompt": "A translucent glass human large intestine on a deep midnight-blue background; a tiny point of warm light appears on its wall and grows very slowly. A minimal thin timeline draws itself with evenly spaced markers. A simple stylized home test kit rests on a clean pale surface and softly lights up. The point of light on the colon wall fades away and the organ returns to an even calm glow.",
        "verifier": [
            "Chiffres et tranche d'âge conformes aux recommandations en vigueur (INCa, Assurance Maladie)",
            "Aucun texte généré par l'IA à l'image : les chiffres sont ajoutés au montage",
            "« 9 cas sur 10 » : formulation et source à valider par l'équipe",
        ],
    },
]

PAR_ID = {v["id"]: v for v in VIDEOS}
