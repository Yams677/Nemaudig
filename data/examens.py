"""« Comprendre votre parcours de soins » — examens prescrits avant une intervention.

IMPORTANT : Nemaudig est un cabinet de chirurgiens. Ces examens endoscopiques sont
réalisés par des gastro-entérologues ; ils sont expliqués ici parce que les patients
du cabinet y sont souvent confrontés avant ou après une opération.

Textes de vulgarisation rédigés pour la maquette d'après les fiches d'information
publiques (SFED, SNFGE, Assurance Maladie, INCa). Chaque fiche est PROVISOIRE :
durées, modalités d'anesthésie et consignes doivent être validées par l'équipe et
par les gastro-entérologues correspondants avant publication.

Rubriques (ordre imposé par le gabarit) : pourquoi, deroulement, preparation, duree,
anesthesie, risques, suites, resultats. `None` = à compléter avec l'équipe.
"""

RUBRIQUES = [
    ("pourquoi", "Pourquoi cet examen ?"),
    ("deroulement", "Comment se déroule-t-il ?"),
    ("preparation", "Comment s'y préparer ?"),
    ("duree", "Combien de temps dure-t-il ?"),
    ("anesthesie", "Sédation ou anesthésie ?"),
    ("risques", "Précautions et risques"),
    ("suites", "Après l'examen"),
    ("resultats", "Comment obtenir les résultats ?"),
]

REALISE_PAR = "Réalisé par un gastro-entérologue, sur prescription."

EXAMENS = [
    {
        "slug": "gastroscopie", "titre": "Gastroscopie", "organes": ["oesophage", "estomac"],
        "autre_nom": "Endoscopie œso-gastro-duodénale",
        "resume": "Un endoscope souple, introduit par la bouche, explore l'œsophage, l'estomac et le duodénum.",
        "pourquoi": [
            "Rechercher la cause de brûlures persistantes, d'une difficulté à avaler, de douleurs, d'une anémie ou d'un saignement.",
            "Réaliser des prélèvements (biopsies), indolores, pour les analyser au microscope.",
            "Compléter le bilan avant certaines interventions, par exemple une chirurgie du reflux ou de l'obésité.",
        ],
        "deroulement": [
            "Vous êtes installé sur le côté gauche. Un embout protège vos dents.",
            "L'endoscope, fin et souple, est glissé par la bouche. Un peu d'air est insufflé pour déplisser les parois.",
            "Le médecin examine la muqueuse sur un écran et réalise, si besoin, des prélèvements.",
        ],
        "preparation": [
            "Être à jeun : ne pas manger, ne pas boire et ne pas fumer pendant les heures qui précèdent, selon la consigne remise.",
            "Signaler vos traitements, en particulier ceux qui fluidifient le sang, et vos allergies.",
            "Ne modifiez jamais un traitement sans l'avis du médecin qui vous suit.",
        ],
        "duree": ["L'examen lui-même est court : quelques minutes le plus souvent."],
        "anesthesie": [
            "Il peut être réalisé avec une simple anesthésie locale de la gorge.",
            "Il peut aussi être réalisé sous sédation ou anesthésie générale courte : une consultation d'anesthésie est alors obligatoire plusieurs jours avant.",
        ],
        "risques": [
            "Les complications sont rares : perforation, saignement, troubles respiratoires ou cardiaques, infection.",
            "Une gêne dans la gorge et des ballonnements passagers sont fréquents et sans gravité.",
            "Douleur, fièvre, vomissements de sang ou selles noires dans les jours qui suivent : contactez immédiatement le médecin ou le 15.",
        ],
        "suites": [
            "Après une anesthésie locale, attendez la disparition de l'engourdissement de la gorge avant de boire ou de manger.",
            "Après une anesthésie générale : sortie accompagnée, pas de conduite le jour même.",
        ],
        "resultats": [
            "Les premières constatations vous sont expliquées après l'examen et un compte rendu est remis.",
            "Le résultat des prélèvements demande quelques jours ; il est transmis au médecin prescripteur.",
        ],
        "faq": [
            ("Est-ce douloureux ?", "L'examen est désagréable plutôt que douloureux. Respirer calmement aide beaucoup ; une sédation peut être proposée."),
            ("Puis-je prendre mes médicaments habituels ?", "Posez la question au moment de la prescription : certains traitements doivent être adaptés avant l'examen."),
        ],
    },
    {
        "slug": "coloscopie", "titre": "Coloscopie", "organes": ["colon", "rectum"],
        "autre_nom": "Endoscopie digestive basse",
        "resume": "Un endoscope souple explore l'ensemble du côlon et permet de retirer les polypes dans le même temps.",
        "pourquoi": [
            "Après un test de dépistage positif, ou en cas de sang dans les selles, de transit modifié ou de douleurs inexpliquées.",
            "En cas d'antécédent personnel ou familial de polype ou de cancer colorectal.",
            "Pour surveiller une maladie inflammatoire de l'intestin, ou compléter le bilan avant une chirurgie du côlon.",
        ],
        "deroulement": [
            "L'endoscope est introduit par l'anus et progresse jusqu'au début du côlon.",
            "De l'air ou du gaz est insufflé pour déplisser les parois ; la muqueuse est examinée en retirant l'appareil.",
            "Les polypes repérés sont retirés et des prélèvements peuvent être réalisés.",
        ],
        "preparation": [
            "Un régime pauvre en fibres (« sans résidus ») les jours qui précèdent.",
            "Une préparation à boire, selon l'horaire prescrit, qui nettoie l'intestin : un côlon propre conditionne la qualité de l'examen.",
            "Signaler vos traitements, en particulier ceux qui fluidifient le sang. Suivez les consignes personnelles qui vous sont remises.",
        ],
        "duree": ["Environ une demi-heure pour l'examen ; comptez quelques heures sur place avec la surveillance."],
        "anesthesie": [
            "Le plus souvent sous anesthésie générale courte ou sédation profonde.",
            "Une consultation d'anesthésie est obligatoire plusieurs jours avant l'examen.",
        ],
        "risques": [
            "Les complications sont rares : perforation, saignement — parfois retardé de quelques jours après l'ablation d'un polype —, complications liées à l'anesthésie.",
            "Des ballonnements passagers sont fréquents.",
            "Douleurs abdominales, sang rouge dans les selles, fièvre ou frissons dans les jours qui suivent : contactez immédiatement le médecin ou le 15.",
        ],
        "suites": [
            "L'examen est le plus souvent réalisé en ambulatoire, avec un passage en salle de réveil.",
            "Sortie accompagnée ; pas de conduite ni de décision importante le jour même.",
        ],
        "resultats": [
            "Un compte rendu vous est remis à la sortie.",
            "L'analyse des polypes et des prélèvements demande quelques jours ; elle fixe la date du prochain contrôle.",
        ],
        "faq": [
            ("La préparation est-elle vraiment indispensable ?", "Oui. Si le côlon n'est pas propre, de petites lésions peuvent passer inaperçues et l'examen peut être à refaire."),
            ("Les polypes sont-ils retirés le jour même ?", "Le plus souvent, oui : ils sont retirés pendant l'examen, puis analysés."),
            ("Et si l'on découvre une lésion à opérer ?", "Votre gastro-entérologue vous adresse alors à un chirurgien ; en cancérologie, le dossier est discuté en concertation pluridisciplinaire."),
        ],
    },
    {
        "slug": "echo-endoscopie", "titre": "Écho-endoscopie", "organes": ["pancreas", "vesicule", "rectum"],
        "autre_nom": "Échographie par voie endoscopique",
        "resume": "Un endoscope muni d'une sonde d'échographie étudie la paroi du tube digestif et les organes voisins, comme le pancréas et les voies biliaires.",
        "pourquoi": [
            "Préciser une lésion de la paroi de l'œsophage, de l'estomac ou du rectum.",
            "Étudier le pancréas et les voies biliaires, par exemple à la recherche d'un calcul.",
            "Réaliser, si nécessaire, un prélèvement guidé par l'échographie.",
        ],
        "deroulement": None,
        "preparation": ["Être à jeun, selon la consigne remise. Signaler vos traitements et vos allergies."],
        "duree": None,
        "anesthesie": ["Le plus souvent sous anesthésie générale : une consultation d'anesthésie préalable est obligatoire."],
        "risques": None,
        "suites": None,
        "resultats": None,
        "faq": [],
    },
]

PAR_SLUG = {x["slug"]: x for x in EXAMENS}

# Documents à apporter en consultation — reprend « Dans tous les cas, munissez-vous de la
# liste de vos traitements et de votre dossier médical » (site) ; les autres lignes sont
# des usages courants, À VALIDER par le secrétariat.
DOCUMENTS = [
    ("La lettre de votre médecin", "Le courrier du médecin qui vous adresse.", True),
    ("La liste de vos traitements", "Vos ordonnances en cours, y compris les médicaments qui fluidifient le sang.", False),
    ("Votre dossier médical", "Comptes rendus d'examens, d'opérations et d'hospitalisations.", False),
    ("Vos examens d'imagerie", "Échographies, scanners, IRM : comptes rendus et images.", True),
    ("Vos résultats de prises de sang", "Les bilans les plus récents.", True),
    ("Carte Vitale et carte de mutuelle", "Pour les formalités administratives.", True),
]
