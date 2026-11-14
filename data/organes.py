"""Fiches de l'explorateur anatomique — un organe = une fiche.

DEUX NIVEAUX DE FIABILITÉ, à ne pas mélanger :
- `pathologies`, `chirurgiens` et les phrases marquées (site) reprennent nemaudig.fr ;
- le reste (fonctionnement, signes, examens, traitements) est une information
  générale de vulgarisation, rédigée pour la maquette d'après les repères publics
  (HAS, INCa, Assurance Maladie, SNFGE). Elle doit être RELUE ET VALIDÉE PAR L'ÉQUIPE
  avant toute publication (voir docs/A-VALIDER.md).

`chirurgiens` : (slug, spécialité affichée sur le site). Attributions PROPOSÉES
d'après les spécialités déclarées, à confirmer. Liste vide = toute l'équipe.
`teinte` : couleur pastel du fond (variable CSS). `article` : nom avec son article.
Image : src/assets/img/organes/<cle>.webp, générée par IA — à faire valider (anatomie).
`schema` : animation de lib/schemas.py.
"""

ORGANES = [
    {
        "cle": "oesophage", "teinte": "org-oesophage", "article": "l'œsophage", "nom": "Œsophage", "latin": "Oesophagus", "fma": "FMA 7131",
        "modeles": ["oesophage"],
        "accroche": "Le passage entre la gorge et l'estomac.",
        "role": "L'œsophage est le conduit musculaire qui relie la gorge à l'estomac. Il traverse le thorax, puis franchit le diaphragme par l'orifice hiatal pour rejoindre l'abdomen.",
        "fonctionnement": [
            "À chaque déglutition, des contractions successives — le péristaltisme — poussent les aliments vers l'estomac, même allongé.",
            "À sa partie basse, un muscle en anneau se referme après le passage des aliments : il empêche le contenu acide de l'estomac de remonter.",
        ],
        "signes": [
            "Brûlures ou remontées acides qui persistent malgré le traitement",
            "Aliments qui passent de plus en plus mal",
            "Douleur en avalant",
            "Amaigrissement inexpliqué",
        ],
        "pathologies": ["rgo", "hernie-hiatale", "cancer-de-l-oesophage"],
        "examens": [
            ("Gastroscopie", "Elle montre la paroi de l'œsophage et permet des prélèvements.", "gastroscopie"),
            ("pH-métrie et manométrie", "Elles mesurent le reflux acide et la force des contractions.", None),
            ("Scanner", "Il précise l'étendue d'une lésion et ses rapports avec les organes voisins.", None),
        ],
        "traitements": [
            "Pour le reflux : règles d'hygiène de vie et médicaments réduisant l'acidité, en première intention.",
            "Chirurgie anti-reflux : une valve façonnée avec le haut de l'estomac vient « cravater » l'œsophage et empêche les remontées.",
            "En cancérologie : la stratégie est décidée en réunion de concertation pluridisciplinaire ; la chirurgie peut être associée à d'autres traitements.",
        ],
        "chirurgiens": [("dr-david-amielh", "Chirurgie œsophagienne")],
        "schema": None,
    },
    {
        "cle": "estomac", "teinte": "org-estomac", "article": "l'estomac", "nom": "Estomac", "latin": "Gaster", "fma": "FMA 7148",
        "modeles": ["estomac"],
        "accroche": "Une poche musculaire qui brasse et prépare les aliments.",
        "role": "Situé entre l'œsophage et le duodénum, l'estomac reçoit les aliments, les brasse et commence leur digestion avant de les transmettre à l'intestin.",
        "fonctionnement": [
            "Sa paroi musculaire malaxe les aliments et les mélange au suc gastrique, très acide.",
            "Le contenu est ensuite libéré par petites quantités vers le duodénum, à travers le pylore.",
            "Une partie de sa paroi sécrète la ghréline, l'hormone qui stimule l'appétit.",
        ],
        "signes": [
            "Douleur ou brûlure au creux de l'estomac",
            "Nausées ou vomissements répétés",
            "Sensation d'être très vite rassasié",
            "Vomissements de sang ou selles noires : appelez le 15",
        ],
        "pathologies": ["cancer-de-l-estomac", "hernie-hiatale"],
        "familles": ["obesite"],
        "examens": [
            ("Gastroscopie", "Elle explore l'intérieur de l'estomac et permet des prélèvements.", "gastroscopie"),
            ("Scanner abdominal", "Il complète le bilan lorsqu'une lésion est découverte.", None),
            ("Bilan sanguin", "Il recherche notamment une anémie.", None),
        ],
        "traitements": [
            "Traitement médical, prescrit par votre médecin traitant ou votre gastro-entérologue, dans la plupart des maladies bénignes.",
            "Chirurgie de l'estomac en cancérologie, après concertation pluridisciplinaire.",
            "Chirurgie de l'obésité (sleeve, bypass), dans le cadre d'un parcours pluridisciplinaire.",
        ],
        "chirurgiens": [("dr-fanelly-torres", "Chirurgie de l'obésité")],
        "schema": "estomac",
    },
    {
        "cle": "foie", "teinte": "org-foie", "article": "le foie", "nom": "Foie", "latin": "Hepar", "fma": "FMA 7197",
        "modeles": ["foie"],
        "accroche": "Un organe indispensable à la vie, qui épure, fabrique et stocke.",
        "role": "Situé sous les côtes à droite, le foie nettoie et épure le sang, fabrique des protéines et stocke des molécules. Il fabrique aussi la bile, nécessaire à la digestion des graisses.",
        "fonctionnement": [
            "Il reçoit par la veine porte le sang venu de l'intestin, chargé des nutriments absorbés.",
            "Il transforme, stocke et épure : sucres, graisses, médicaments, alcool.",
            "Il repousse après l'ablation d'une partie, en plusieurs semaines.",
        ],
        "maladies": [
            ("Stéatose", "Une accumulation de graisse dans les cellules du foie, liée notamment au surpoids, au diabète ou à l'alcool."),
            ("Hépatites", "Des inflammations du foie, d'origine virale, toxique, médicamenteuse ou auto-immune."),
            ("Fibrose et cirrhose", "La cicatrisation progressive d'un foie agressé au long cours ; la cirrhose en est le stade avancé."),
            ("Tumeurs", "Bénignes ou malignes ; il peut s'agir d'un cancer né dans le foie ou de métastases d'un autre cancer."),
        ],
        "maladies_note": "Le suivi des maladies chroniques du foie relève de votre médecin traitant et de l'hépato-gastro-entérologue. L'équipe Nemaudig intervient lorsqu'une chirurgie est indiquée.",
        "signes": [
            "Très souvent aucun signe pendant longtemps",
            "Fatigue inhabituelle et durable",
            "Jaunisse (ictère)",
            "Anomalie découverte sur une prise de sang ou une échographie",
        ],
        "pathologies": ["foie"],
        "examens": [
            ("Bilan sanguin hépatique", "Il mesure les enzymes du foie et sa capacité de fabrication.", None),
            ("Échographie abdominale", "Premier examen d'imagerie, sans rayons ni piqûre.", None),
            ("Élastographie", "Elle mesure la dureté du foie, reflet de la fibrose, sans prélèvement.", None),
            ("Scanner et IRM", "Ils caractérisent une lésion et préparent une éventuelle intervention.", None),
        ],
        "traitements": [
            "Correction des causes : alcool, surpoids, traitement d'une hépatite.",
            "Surveillance régulière par des prises de sang et de l'imagerie.",
            "Chirurgie du foie (hépatectomie), le plus souvent pour retirer une tumeur, primitive ou métastase.",
        ],
        "chirurgiens": [("dr-emmanuel-prieur", "Chirurgie hépatique")],
        "schema": "foie",
    },
    {
        "cle": "vesicule", "teinte": "org-vesicule", "article": "la vésicule biliaire", "nom": "Vésicule biliaire", "latin": "Vesica biliaris", "fma": "FMA 7202",
        "modeles": ["vesicule"],
        "accroche": "Le réservoir de la bile, sous le foie.",
        "role": "La vésicule biliaire stocke la bile fabriquée par le foie pour l'évacuer en grande quantité au moment des repas.",
        "fonctionnement": [
            "Entre les repas, la bile s'y accumule et s'y concentre.",
            "Lorsque vous mangez, la vésicule se contracte et libère la bile dans le duodénum, où elle aide à digérer les graisses.",
            "La bile peut y sédimenter et former des calculs.",
        ],
        "signes": [
            "Douleur au creux de l'estomac ou sous les côtes à droite, parfois vers le dos ou l'épaule droite",
            "Douleur survenant après un repas",
            "Fièvre ou jaunisse associées : consultez sans attendre",
        ],
        "pathologies": ["vesicule-biliaire", "cholecystectomie"],
        "examens": [
            ("Échographie abdominale", "L'examen de référence pour voir les calculs de la vésicule.", None),
            ("Bilan sanguin", "Il recherche une inflammation ou un retentissement sur le foie et le pancréas.", None),
            ("IRM des voies biliaires ou écho-endoscopie", "Lorsqu'un calcul a pu migrer dans le canal de la bile.", "echo-endoscopie"),
        ],
        "traitements": [
            "Calculs sans aucun symptôme : le plus souvent, une simple surveillance.",
            "Calculs compliqués : ablation de la vésicule (cholécystectomie), la plupart du temps sous cœlioscopie.",
            "Aujourd'hui, la plupart des ablations de la vésicule sont réalisées en ambulatoire.",
        ],
        "chirurgiens": [],
        "schema": None,
    },
    {
        "cle": "pancreas", "teinte": "org-pancreas", "article": "le pancréas", "nom": "Pancréas", "latin": "Pancreas", "fma": "FMA 7198",
        "modeles": ["pancreas", "duodenum"],
        "accroche": "L'organe caché, derrière l'estomac.",
        "role": "Profond, situé en arrière de l'estomac, le pancréas est encastré dans le duodénum. Il fabrique des enzymes de la digestion et l'insuline, qui régule le sucre dans le sang.",
        "fonctionnement": [
            "Fonction digestive : le suc pancréatique rejoint le duodénum et y décompose graisses, protéines et sucres.",
            "Fonction hormonale : l'insuline et le glucagon règlent en permanence le taux de sucre dans le sang.",
            "Le canal de la bile traverse sa tête : une lésion à cet endroit peut bloquer l'écoulement de la bile.",
        ],
        "signes": [
            "Jaunisse (ictère)",
            "Douleur du haut du ventre irradiant dans le dos",
            "Amaigrissement, perte d'appétit",
            "Diabète d'apparition récente",
        ],
        "pathologies": ["cancer-du-pancreas"],
        "examens": [
            ("Scanner", "L'examen clé pour étudier le pancréas et les vaisseaux qui l'entourent.", None),
            ("IRM", "Elle précise les canaux et la nature d'une lésion.", None),
            ("Écho-endoscopie", "Elle approche le pancréas au plus près et permet un prélèvement.", "echo-endoscopie"),
        ],
        "traitements": [
            "Chaque dossier est discuté en réunion de concertation pluridisciplinaire.",
            "Chirurgie du pancréas lorsque la lésion peut être retirée ; après l'ablation de la tête, trois coutures sont nécessaires : canal pancréatique, canal biliaire et tube digestif.",
            "D'autres traitements peuvent être associés, avant ou après l'opération.",
        ],
        "chirurgiens": [],
        "schema": None,
    },
    {
        "cle": "intestin", "teinte": "org-intestin", "article": "l'intestin grêle", "nom": "Intestin grêle", "latin": "Intestinum tenue", "fma": "FMA 7200",
        "modeles": ["intestin"],
        "accroche": "Là où l'organisme absorbe ce dont il a besoin.",
        "role": "Après le duodénum vient l'intestin grêle : d'abord le jéjunum, puis l'iléon. C'est dans l'intestin que les nutriments sont réellement absorbés.",
        "fonctionnement": [
            "Long de plusieurs mètres, il est tapissé de replis et de villosités qui multiplient sa surface d'absorption.",
            "Les nutriments passent dans le sang et rejoignent le foie par la veine porte.",
            "Ses contractions font progresser le contenu jusqu'au côlon.",
        ],
        "signes": [
            "Douleurs abdominales et diarrhée qui durent",
            "Amaigrissement, fatigue",
            "Ventre gonflé, arrêt des gaz et des selles avec vomissements : urgence",
        ],
        "pathologies": ["mici"],
        "examens": [
            ("Entéro-IRM ou scanner", "Ils étudient la paroi de l'intestin sur toute sa longueur.", None),
            ("Coloscopie", "Elle peut explorer la toute fin de l'intestin grêle.", "coloscopie"),
            ("Bilan sanguin", "Il recherche une inflammation et des carences.", None),
        ],
        "traitements": [
            "Maladies inflammatoires : le traitement médical est conduit par votre gastro-entérologue.",
            "Une chirurgie peut être proposée en cas de complication ou lorsque le traitement médical ne suffit plus.",
        ],
        "chirurgiens": [],
        "schema": None,
    },
    {
        "cle": "colon", "teinte": "org-colon", "article": "le côlon", "nom": "Côlon", "latin": "Colon", "fma": "FMA 14543",
        "modeles": ["colon"],
        "accroche": "Le cadre du gros intestin, où se termine la digestion.",
        "role": "Le côlon fait suite à l'intestin grêle et encadre l'abdomen : côlon droit qui monte, côlon transverse qui traverse, côlon gauche qui redescend, puis le sigmoïde avant le rectum.",
        "fonctionnement": [
            "Il réabsorbe l'eau et les sels minéraux : le contenu devient progressivement solide.",
            "Des milliards de bactéries — le microbiote — y achèvent la digestion des fibres.",
            "Le transit : des contractions font avancer les selles jusqu'au rectum.",
        ],
        "encarts": [
            ("Les polypes", "De petites excroissances de la paroi du côlon. La plupart sont bénins, mais certains peuvent, en plusieurs années, se transformer en cancer. Les retirer pendant une coloscopie prévient cette évolution."),
            ("Le dépistage", "Entre 50 et 74 ans, sans symptôme ni risque particulier, un test de recherche de sang dans les selles est proposé tous les deux ans. S'il est positif, une coloscopie est nécessaire."),
            ("La coloscopie", "Elle explore tout le côlon avec un endoscope souple, le plus souvent sous anesthésie. Elle demande une préparation : un régime pauvre en fibres, puis une boisson qui nettoie l'intestin. La qualité de l'examen en dépend."),
            ("Prévention et suivi", "Activité physique régulière, alimentation riche en fibres, moins d'alcool, de viande rouge et de charcuterie, pas de tabac. Après l'ablation d'un polype ou une opération, un calendrier de surveillance est fixé."),
        ],
        "signes": [
            "Sang dans les selles",
            "Transit modifié de façon récente et durable",
            "Douleurs abdominales inhabituelles",
            "Fatigue, anémie, amaigrissement",
        ],
        "pathologies": ["diverticules-du-sigmoide", "cancer-du-colon", "chirurgie-colique", "mici"],
        "examens": [
            ("Test de dépistage", "Un test immunologique à faire chez soi, tous les deux ans entre 50 et 74 ans.", None),
            ("Coloscopie", "Elle visualise toute la paroi et permet de retirer les polypes.", "coloscopie"),
            ("Scanner", "Il confirme une diverticulite ou complète un bilan.", None),
        ],
        "traitements": [
            "Ablation des polypes pendant la coloscopie, par le gastro-entérologue.",
            "Chirurgie du côlon : retirer le segment atteint, puis rétablir le circuit par une couture entre les deux extrémités. Le plus souvent par cœlioscopie.",
            "Réhabilitation améliorée après chirurgie : des mesures validées pour récupérer plus vite.",
        ],
        "chirurgiens": [("dr-sylvain-laporte", "Chirurgie colorectale")],
        "schema": "colon",
    },
    {
        "cle": "rectum", "teinte": "org-rectum", "article": "le rectum", "nom": "Rectum", "latin": "Rectum", "fma": "FMA 14544",
        "modeles": ["rectum"],
        "accroche": "Le dernier segment, un carrefour de précision.",
        "role": "Le rectum, d'environ 15 cm, sert de réservoir. Il se termine par le canal anal, long de 2 à 3 cm, fermé par le sphincter qui assure la continence.",
        "fonctionnement": [
            "Lorsqu'il se remplit, il déclenche le besoin d'aller à la selle.",
            "Le sphincter anal, en partie volontaire, permet de se retenir.",
            "Il est au contact de la vessie, de la prostate ou de l'utérus, et des nerfs du bassin : chaque geste y demande de la précision.",
        ],
        "signes": [
            "Sang rouge dans les selles ou sur le papier",
            "Douleur anale au passage des selles",
            "Envies pressantes ou faux besoins",
            "Grosseur ou écoulement près de l'anus",
        ],
        "pathologies": ["cancer-du-rectum", "chirurgie-rectale", "hemorroides", "fissure-anale", "abces-et-fistule-anale"],
        "examens": [
            ("Examen proctologique", "Réalisé en consultation, il suffit souvent au diagnostic.", None),
            ("Coloscopie", "Elle vérifie l'ensemble du côlon et du rectum.", "coloscopie"),
            ("IRM du bassin", "Elle précise l'étendue d'une tumeur avant de choisir le traitement.", None),
        ],
        "traitements": [
            "Proctologie : traitements médicaux, instrumentaux ou chirurgicaux, selon la gêne ressentie.",
            "Cancer du rectum : la stratégie est décidée en concertation pluridisciplinaire.",
            "Chirurgie du rectum, conservant le sphincter chaque fois que c'est possible.",
        ],
        "chirurgiens": [("dr-sylvain-laporte", "Chirurgie colorectale"), ("dr-mathias-alline", "Proctologie et statique pelvienne")],
        "schema": None,
    },
]

PAR_CLE = {o["cle"]: o for o in ORGANES}

# Ordre d'apparition dans la scène 3D (du haut vers le bas du tube digestif).
ORDRE_MODELES = ["oesophage", "estomac", "foie", "vesicule", "pancreas", "duodenum", "intestin", "colon", "rectum"]

# Modèle 3D → organe de l'explorateur (le duodénum est présenté avec le pancréas).
ORGANE_DU_MODELE = {m: o["cle"] for o in ORGANES for m in o["modeles"]}

# Organe de data/pathologies.py → organe de l'explorateur (None : hors du modèle 3D).
ORGANE_DE_LA_PATHOLOGIE = {
    "oesophage": "oesophage", "estomac": "estomac", "foie": "foie", "vesicule": "vesicule",
    "pancreas": "pancreas", "intestin": "intestin", "colon": "colon", "sigmoide": "colon",
    "rectum": "rectum", "anus": "rectum",
}
