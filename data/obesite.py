"""Chirurgie de l'obésité — pages chirurgie-bariatrique-obesite, techniques,
sleeve, by-pass, anneau, ballon, parcours pré-opératoire, suivi, points importants.

Les chiffres (durées, pertes de poids, taux) sont ceux du site actuel. Les
statistiques épidémiologiques de « Points importants » (OMS, 2014) sont
anciennes : on ne les reprend pas sur la nouvelle page (À VALIDER avec le
cabinet s'il souhaite des chiffres actualisés et sourcés).
"""

TECHNIQUES = [
    {
        "slug": "ballon-intragastrique", "ancien": "le-ballon-intragastrique",
        "titre": "Ballon intragastrique Allurion", "court": "Ballon Allurion",
        "type": "Sans chirurgie ni anesthésie",
        "resume": "Une capsule avalée en consultation, qui se transforme en ballon dans l'estomac pendant environ 4 mois.",
        "desc": "Ballon intragastrique Allurion à Nîmes : sans chirurgie ni anesthésie, 10 à 15 % du poids perdu en moyenne, 6 mois de suivi diététique. Dès un IMC de 30.",
        "chiffres": [("≈ 4 mois", "en place, puis éliminé naturellement"), ("10–15 %", "du poids corporel perdu en moyenne"), ("6 mois", "de suivi par une diététicienne"), ("IMC ≥ 30", "indication")],
        "sections": [
            ("Le principe", "La capsule souple est avalée avec un verre d'eau, sous contrôle médical. Dans l'estomac, elle est remplie d'un liquide stérile et prend la forme d'un ballon, qui occupe une partie de l'estomac : la faim diminue et la satiété arrive plus vite.\n\nLe ballon reste en place environ 4 mois, puis se vide spontanément et est éliminé naturellement, sans chirurgie ni endoscopie."),
            ("Les avantages", "- Sans chirurgie ni anesthésie : une pose simple et rapide (20 minutes), réalisée en radiologie\n- Une méthode temporaire et réversible\n- Un accompagnement renforcé : suivi personnalisé par une diététicienne pendant 6 mois\n- Au-delà de la perte de poids, l'objectif est d'installer durablement de nouveaux comportements"),
            ("La perte de poids attendue", "Les études montrent une perte moyenne de 10 à 15 % du poids corporel pendant les 4 mois où le ballon est en place. Les résultats varient selon l'implication de chacun : alimentation, activité physique, suivi diététique."),
            ("Pour qui ?", "- IMC supérieur ou égal à 30 kg/m²\n- Souhait de perdre du poids sans relever nécessairement d'une chirurgie bariatrique\n- Motivation à suivre un accompagnement nutritionnel et à changer ses habitudes de vie\n\nCe n'est pas une solution « miracle », mais un outil médical qui, associé à un suivi professionnel et à la motivation du patient, permet d'obtenir des résultats durables."),
        ],
        "liens": [("Vidéo explicative (YouTube)", "https://youtu.be/YKc7sAluiWo"), ("Site Allurion", "https://www.allurion.com/")],
        "video": None,
    },
    {
        "slug": "sleeve-gastrectomie", "ancien": "sleeve-gastrectomie",
        "titre": "Sleeve gastrectomie", "court": "Sleeve",
        "type": "Restrictive · irréversible",
        "resume": "Retirer environ les deux tiers de l'estomac, qui devient un tube vertical.",
        "desc": "Sleeve gastrectomie à Nîmes : principe, durée de l'opération et de l'hospitalisation, perte de poids attendue, suivi à vie et complications possibles.",
        "chiffres": [("60–120 min", "d'intervention en moyenne"), ("3 à 8 jours", "d'hospitalisation"), ("45–65 %", "de l'excès de poids perdu à 2 ans"), ("10 ans", "de recul sur ces résultats")],
        "sections": [
            ("Le principe", "Technique restrictive et irréversible : elle retire environ les deux tiers de l'estomac, dont la partie contenant les cellules qui sécrètent l'hormone stimulant l'appétit (ghréline).\n\nL'estomac est réduit à un tube vertical, les aliments passent rapidement dans l'intestin et l'appétit diminue. La digestion des aliments n'est pas perturbée."),
            ("Résultats", "De l'ordre de 45 à 65 % de l'excès de poids après 2 ans, soit environ 25 à 35 kg. Le recul sur ces résultats est de 10 ans.\n\nLa morbi-mortalité (complications) est estimée à 0,2 %."),
            ("Suivi", "- Avec le chirurgien : tous les 3 mois la première année, puis 1 à 2 fois par an, à vie\n- Avec le nutritionniste et la diététicienne : tous les 3 mois la première année, puis au minimum 2 fois par an, à vie"),
            ("Complications", "- À court terme : ulcère, fuite ou rétrécissement de l'estomac restant, hémorragie précoce, complications pulmonaires ou thrombo-emboliques\n- À long terme : carences nutritionnelles possibles, reflux gastro-œsophagien et inflammation de l'œsophage, dilatation de l'estomac"),
        ],
        "liens": [], "video": None,
    },
    {
        "slug": "bypass-gastrique", "ancien": "by-pass-gastrique",
        "titre": "Bypass gastrique", "court": "Bypass",
        "type": "Restrictive et malabsorptive · irréversible",
        "resume": "Une petite poche gastrique et un court-circuit de l'intestin : moins d'aliments, et moins absorbés.",
        "desc": "Bypass gastrique à Nîmes par le Dr Fanelly Torres : principe du court-circuit en Y, durée, perte de poids attendue, suivi et complications. Vidéo.",
        "chiffres": [("1 h 30–3 h", "d'intervention"), ("3 à 8 jours", "d'hospitalisation"), ("60–75 %", "de l'excès de poids perdu"), ("à vie", "vitamines et suivi")],
        "sections": [
            ("Le principe", "Technique restrictive et malabsorptive irréversible : elle diminue à la fois la quantité d'aliments ingérés et leur absorption, car ils sont envoyés directement dans la partie moyenne de l'intestin grêle.\n\nL'estomac est réduit à une petite poche d'environ 15 à 75 cc. L'intestin grêle est sectionné à 1 m de son origine et sa partie d'aval est suturée à l'estomac (anse alimentaire). La partie qui recueille la bile et les sécrétions pancréatiques est raccordée en « Y » environ 150 cm plus bas. Aucun organe n'est enlevé."),
            ("Résultats", "De l'ordre de 60 à 75 % de l'excès de poids, soit environ 35 à 40 kg, entre 6 et 48 mois après l'intervention.\n\nSa morbidité est estimée à 5 % et sa mortalité à 0,5 %."),
            ("Suivi", "Avec votre chirurgien : tous les 3 mois la première année, puis 1 à 2 fois par an, à vie."),
            ("Complications", "- À court terme : saignement, abcès ou péritonite secondaires à une fistule, embolie pulmonaire, infections urinaires et pulmonaires\n- À long terme : carences nutritionnelles — la prise de vitamines (B12, acide folique, B1) et d'oligoéléments (calcium, zinc, fer) est le plus souvent nécessaire à vie\n- Troubles fonctionnels : hypoglycémie après le repas, dumping syndrome, constipation\n- À distance : dilatation de la poche (reprise de poids), rétrécissement de l'anastomose, occlusion intestinale par hernie interne (moins de 2 %), pouvant nécessiter une chirurgie"),
        ],
        "liens": [], "video": "bypass-coelio",
    },
    {
        "slug": "anneau-gastrique", "ancien": "anneau-peri-gastrique-ajustable",
        "titre": "Anneau gastrique ajustable", "court": "Anneau",
        "type": "Restrictive · réversible",
        "resume": "Un anneau gonflable placé autour du haut de l'estomac, réglable à travers la peau.",
        "desc": "Anneau gastrique ajustable : principe du sablier, durée, résultats à 2 et 5 ans, réglages et complications mécaniques possibles. Chirurgie de l'obésité, Nîmes.",
        "chiffres": [("40–60 min", "d'intervention"), ("12 à 48 h", "d'hospitalisation"), ("40–60 %", "de l'excès de poids perdu à 2 ans"), ("20 ans", "de recul")],
        "sections": [
            ("Le principe", "Technique restrictive et réversible : un anneau en silicone gonflable est placé autour de la partie haute de l'estomac. Il délimite une petite poche, vite remplie : la satiété apparaît rapidement et les aliments s'écoulent lentement, selon le principe du sablier. La digestion n'est pas perturbée.\n\nL'anneau est relié par un petit tube à un boîtier placé sous la peau ; on le serre ou le desserre en injectant du liquide dans ce boîtier. Il peut être retiré lors d'une nouvelle intervention (complication, inefficacité ou demande du patient)."),
            ("Résultats", "De l'ordre de 40 à 60 % de l'excès de poids à 2 ans, soit environ 20 à 30 kg. L'efficacité dépend directement du serrage, débuté 1 à 2 mois après la pose : il faut trouver l'équilibre entre perte de poids et confort alimentaire. En cas de retrait, une reprise de poids est habituelle.\n\nLe risque de décès est très faible (0,1 %). Le taux d'échec (moins de 25 % de perte d'excès de poids) est de près de 40 % à 5 ans, avec un taux de retrait de l'anneau de 20 %."),
            ("Suivi", "- Contrôle radiologique à chaque serrage ou desserrage, ou au moins une fois par an\n- Certains aliments peuvent être mal tolérés (viande rouge non hachée, pain, légumes ou fruits à peau)"),
            ("Complications", "Des complications mécaniques peuvent survenir, même après plusieurs années :\n\n- problèmes de boîtier : infection, déplacement, douleurs, rupture du tube\n- glissement de l'anneau et dilatation de la poche, avec vomissements importants\n- troubles de l'œsophage (reflux, œsophagite, troubles moteurs)\n- lésions de l'estomac (érosion, migration de l'anneau)\n\nUne nouvelle intervention peut être nécessaire pour retirer l'anneau ou réaliser une autre technique."),
        ],
        "liens": [], "video": None,
    },
]

PAR_SLUG = {t["slug"]: t for t in TECHNIQUES}

# Classes d'IMC telles que présentées sur « Points importants ».
IMC = [
    (18, 25, "Poids normal"),
    (25, 30, "Surpoids"),
    (30, 35, "Obésité modérée"),
    (35, 40, "Obésité sévère"),
    (40, 60, "Obésité massive ou morbide"),
]

CANDIDAT = ("La chirurgie bariatrique est principalement destinée aux patients souffrant d'obésité morbide "
            "(IMC > 40 kg/m²) ou sévère (IMC > 35 kg/m²) avec une maladie associée qui complique l'obésité. "
            "L'évaluation pluridisciplinaire de chaque cas permet de choisir la technique la plus adaptée.")

DEFINITION = ("Selon l'Organisation mondiale de la santé, l'obésité est une maladie chronique, grave et complexe : "
              "une accumulation anormale ou excessive de graisse, nocive pour la santé, liée à un déséquilibre "
              "entre les calories ingérées et dépensées.")

CAUSES = [
    ("Héréditaires", []),
    ("Sociales et environnementales", ["sédentarité", "manque d'exercice", "alimentation déséquilibrée", "suralimentation", "repas sans horaires", "grignotage"]),
    ("Psychologiques", ["dépression", "anxiété", "stress", "troubles du comportement alimentaire"]),
    ("Médicales", ["hypothyroïdie", "diabète non contrôlé", "problèmes endocriniens", "certains médicaments"]),
]

CONSEQUENCES = ["Diabète", "Hypertension", "Complications cardiovasculaires", "Complications articulaires",
                "Apnée du sommeil", "Reflux gastro-œsophagien", "Risque de certains cancers (sein, endomètre, côlon)",
                "Dépression", "Troubles menstruels et de la fertilité", "Incontinence urinaire"]

# Parcours pré-opératoire : professionnels rencontrés (au minimum 6 mois).
PREPARATION = [
    ("Nutritionniste et/ou endocrinologue", "Examen clinique et bilan biologique complet : dépistage et traitement des maladies associées (diabète, thyroïde, surrénales, foie), recherche et correction des carences."),
    ("Diététicienne", "Très tôt, avant même l'intervention : décoder et corriger le mode alimentaire, instaurer de bonnes habitudes."),
    ("Psychologue et/ou psychiatre", "Évaluer l'anxiété, la dépression, les troubles du comportement alimentaire et l'isolement ; démarrer si besoin une prise en charge."),
    ("Médecin de l'activité physique", "Bilan de l'activité et des habitudes pour reprendre une activité adaptée à votre état, vos goûts et vos possibilités."),
    ("Gynécologue", "Pour les femmes en âge d'avoir des enfants : contraception (au moins 24 mois après l'intervention), mammographie de dépistage après 50 ans."),
    ("Gastro-entérologue", "Endoscopie œso-gastro-duodénale (hernie hiatale, ulcère, Helicobacter pylori) et coloscopie en cas d'antécédents familiaux de cancer colorectal."),
    ("Pneumologue", "Évaluation respiratoire, dépistage d'un syndrome d'apnées du sommeil."),
    ("Cardiologue", "Évaluation de la fonction cardiaque et recherche d'une maladie coronarienne ou artérielle."),
    ("Examens", "Prises de sang, test de grossesse, radiographie pulmonaire, transit gastro-duodénal, évaluation bucco-dentaire."),
]

DECISION = [
    "Une fois toutes les évaluations réalisées, votre dossier est discuté collégialement par les chirurgiens, nutritionnistes, endocrinologues, psychiatres, psychologues et diététiciennes.",
    "Un dossier peut être mis en attente si la préparation nutritionnelle n'est pas suffisante ou en cas de difficulté psychiatrique mal stabilisée.",
    "Si la chirurgie est retenue, le type d'intervention est choisi selon l'âge, les maladies et antécédents, l'IMC, le mode de vie et le désir de grossesse ; une demande d'entente préalable est adressée à l'Assurance maladie.",
    "Si la chirurgie n'est pas envisageable, l'équipe vous en explique les raisons et vous propose une autre prise en charge, non chirurgicale.",
]

ESTIM = ("Pendant la préparation, il est utile de rencontrer des patients déjà opérés et de participer aux groupes "
         "de parole, ateliers et réunions d'information organisés au sein du centre ESTIM.")

SUIVI_ALIMENTATION = [
    "Manger de petites quantités et mastiquer lentement ; fractionner les repas (collations à 10 h et 16 h si nécessaire)",
    "Prendre ses repas assis, au calme",
    "Ne pas boire en mangeant, mais suffisamment entre les repas",
    "Manger équilibré et varié pour éviter les carences",
    "Conserver un apport suffisant en protéines (viandes, poissons, œufs, produits laitiers)",
    "Éviter boissons gazeuses ou sucrées, sauces, fritures, sucreries et aliments gras",
]

SUIVI_ACTIVITE = [
    "Le premier mois, reprendre progressivement : marche, escaliers",
    "Pendant l'arrêt de travail, 30 à 45 minutes de marche matin et soir si possible",
    "Un effort plus soutenu est possible après une dizaine de jours",
    "Piscine possible à partir de 21 jours après l'intervention",
    "Kinésithérapie possible dès la deuxième semaine ; rééducation abdominale après disparition des douleurs",
    "Au-delà de 30 minutes d'effort, les graisses sont mobilisées : chaque minute supplémentaire compte",
]

SUIVI_CONSULTATIONS = [
    ("Chirurgien", "Dans le mois qui suit, puis tous les 3 mois la première année ; ensuite au minimum tous les 6 mois, à vie"),
    ("Diététicienne", "Dans le mois qui suit, puis tous les 3 mois la première année ; ensuite au minimum tous les 6 mois, à vie"),
    ("Médecin nutritionniste", "Au plus tard 3 mois après l'intervention avec un bilan biologique, puis tous les 6 mois, à vie"),
]
