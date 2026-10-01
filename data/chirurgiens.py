"""Les cinq chirurgiens — données recopiées des pages dr-* du site actuel.

Ne rien ajouter qui ne figure pas sur nemaudig.fr. Les « faits » sont tirés
des actualités du site (pages /actualites) et datés.
`portrait` : None tant que la photo officielle n'est pas fournie.
`pathologies` : liens de navigation vers les fiches en rapport avec les
spécialités déclarées (ce n'est pas une affirmation médicale).
"""

CHIRURGIENS = [
    {
        "slug": "dr-mathias-alline",
        "ancien_slug": "dr-mathias-alline",
        "prenom": "Mathias",
        "nom": "Alline",
        "genre": "m",
        "portrait": None,
        "these": "2011",
        "accroche": "Cancérologie digestive, proctologie et statique pelvienne.",
        "specialites": [
            ("Cancérologie digestive", None),
            ("Proctologie et statique pelvienne", None),
            ("Chirurgie générale", None),
            ("Chirurgie robotique", None),
        ],
        "formation": [
            "Ancien externe des Hôpitaux de Paris",
            "Ancien interne des Hôpitaux de Montpellier-Nîmes",
            "Ancien chef de clinique du CHU de Montpellier — services de chirurgie oncologique du Pr Rouanet, de chirurgie digestive du Pr Fabre et de chirurgie oncologique du Pr Saint-Aubert",
            "Ancien chef de clinique du CHU de Nîmes — service de chirurgie digestive du Pr Prudhomme",
        ],
        "diplomes": [
            ("Thèse de docteur en médecine", "2011"),
            ("Master 1 de sciences biologiques et médicales — physiologie et biologie des systèmes intégrés (Cochin-Port Royal)", "2002"),
            ("DES de chirurgie générale", None),
            ("DESC de chirurgie viscérale et digestive", None),
            ("DIU de chirurgie et d'anatomie cœlioscopique", "2009"),
            ("DIU de traumatologie viscérale", "2010"),
            ("DIU de statique pelvienne et urodynamique", "2015"),
        ],
        "societes": ["Membre de la FCVD (Fédération de chirurgie viscérale et digestive)"],
        "faits": [
            "Réalise avec le Dr Amielh des actes sous anesthésie locale le lundi matin aux soins externes de la Polyclinique Grand Sud (lipomes, naevus, kystes).",
            "Fait partie des chirurgiens qui ont fêté le 100e kyste pilonidal traité au laser aux Franciscaines, en moins d'un an (2025).",
        ],
        "videos": [],
        "pathologies": ["cancer-du-colon", "cancer-du-rectum", "hemorroides", "fissure-anale",
                        "abces-et-fistule-anale", "kyste-pilonidal", "kystes-et-lipomes"],
    },
    {
        "slug": "dr-david-amielh",
        "ancien_slug": "dr-david-amielh",
        "prenom": "David",
        "nom": "Amielh",
        "genre": "m",
        "portrait": None,
        "these": "2010",
        "accroche": "Cancérologie digestive, chirurgie de l'œsophage et chirurgie robotique.",
        "specialites": [
            ("Cancérologie digestive", None),
            ("Chirurgie œsophagienne", None),
            ("Chirurgie générale", None),
            ("Chirurgie robotique", None),
        ],
        "formation": [
            "Ancien externe des Hôpitaux de Lille",
            "Ancien interne des Hôpitaux de Lille",
            "Ancien chef de clinique-assistant du CHU de Lille — service de chirurgie digestive et cancérologie du Pr Triboulet",
        ],
        "diplomes": [
            ("Thèse de docteur en médecine", "2010"),
            ("DES de chirurgie générale", None),
            ("DESC de chirurgie viscérale et digestive", None),
            ("DIU de chirurgie œso-gastro-duodénale", None),
            ("DIU de traumatologie viscérale", None),
            ("Formation en chirurgie robotique — Intuitive Surgical", None),
            ("Formateur pour le laboratoire Bard de la technique mini-invasive TEP de chirurgie des hernies inguinales", None),
        ],
        "societes": ["Membre de la FCVD (Fédération de chirurgie viscérale et digestive)"],
        "faits": [
            "Consulte le lundi matin au Centre hospitalier d'Uzès depuis le 1er janvier 2025.",
            "Réalise avec le Dr Alline des actes sous anesthésie locale le lundi matin aux soins externes de la Polyclinique Grand Sud.",
            "Présent au congrès national de chirurgie viscérale et digestive, CNIT Forest, Paris, septembre 2025.",
        ],
        "videos": ["hernie-inguinale-tep", "cardia-robot", "hernie-hiatale-robot", "colectomie-angulaire-gauche"],
        "pathologies": ["cancer-de-l-oesophage", "cancer-de-l-estomac", "hernie-hiatale", "rgo",
                        "hernie-inguinale", "cancer-du-colon"],
    },
    {
        "slug": "dr-sylvain-laporte",
        "ancien_slug": "dr-sylvain-laporte",
        "prenom": "Sylvain",
        "nom": "Laporte",
        "genre": "m",
        "portrait": None,
        "these": None,
        "accroche": "Cancérologie digestive, chirurgie colorectale et endométriose pelvienne.",
        "specialites": [
            ("Cancérologie digestive", None),
            ("Chirurgie colorectale", None),
            ("Endométriose pelvienne", None),
            ("Chirurgie générale", None),
            ("Chirurgie robotique", None),
        ],
        "formation": [
            "Ancien externe des Hôpitaux de Paris",
            "Ancien interne des Hôpitaux de Montpellier-Nîmes",
            "Ancien chef de clinique-assistant des Hôpitaux de Montpellier-Nîmes — service de chirurgie digestive du Pr Prudhomme",
            "Ancien praticien hospitalier du CHU de Nîmes — service de chirurgie digestive du Pr Prudhomme",
        ],
        "diplomes": [
            ("Thèse de docteur en médecine", None),
            ("DES de chirurgie générale", None),
            ("DESC de chirurgie viscérale et digestive", None),
            ("DESC de cancérologie", None),
            ("DIU de traumatologie abdominale", "2000"),
            ("DU d'anatomie abdomino-pelvienne", "1998"),
        ],
        "societes": ["Membre de la FCVD (Fédération de chirurgie viscérale et digestive)"],
        "faits": [
            "Présente le robot chirurgical Da Vinci dans une vidéo du cabinet.",
            "Présent au congrès national de chirurgie viscérale et digestive, CNIT Forest, Paris, septembre 2025.",
        ],
        "videos": ["robot-da-vinci", "crohn-robot", "rectum-robot"],
        "pathologies": ["cancer-du-colon", "cancer-du-rectum", "diverticules-du-sigmoide", "mici",
                        "chirurgie-colique", "chirurgie-rectale"],
    },
    {
        "slug": "dr-emmanuel-prieur",
        "ancien_slug": "dr-emmanuel-prieur",
        "prenom": "Emmanuel",
        "nom": "Prieur",
        "genre": "m",
        "portrait": None,
        "these": "2004",
        "accroche": "Cancérologie digestive et chirurgie du foie.",
        "specialites": [
            ("Cancérologie digestive", None),
            ("Chirurgie hépatique", None),
            ("Chirurgie générale", None),
            ("Chirurgie robotique", None),
        ],
        "formation": [
            "Ancien externe des Hôpitaux de Paris",
            "Ancien interne des Hôpitaux de Lille",
            "Ancien chef de clinique des Hôpitaux de Lille — service de chirurgie digestive et transplantation du Pr Pruvot",
        ],
        "diplomes": [
            ("Thèse de docteur en médecine", "2004"),
            ("DES de chirurgie générale", None),
            ("DESC de chirurgie viscérale et digestive", None),
            ("DIU de chirurgie endocrinienne et métabolique", None),
            ("DU de sénologie", None),
        ],
        "societes": ["Membre de la FCVD (Fédération de chirurgie viscérale et digestive)"],
        "faits": [
            "Fait partie des chirurgiens qui ont fêté le 100e kyste pilonidal traité au laser aux Franciscaines, en moins d'un an (2025).",
        ],
        "videos": [],
        "pathologies": ["foie", "cancer-du-pancreas", "vesicule-biliaire", "cholecystectomie", "cancer-du-colon"],
    },
    {
        "slug": "dr-fanelly-torres",
        "ancien_slug": "dr-fanelly-torres",
        "prenom": "Fanelly",
        "nom": "Torres",
        "genre": "f",
        "portrait": None,
        "these": "2011",
        "accroche": "Chirurgie de l'obésité, chirurgie endocrinienne et chirurgie réparatrice.",
        "specialites": [
            ("Chirurgie de l'obésité", "anneau gastrique, sleeve gastrectomie, bypass gastrique, réinterventions complexes"),
            ("Chirurgie endocrinienne", "thyroïde et glandes surrénales"),
            ("Chirurgie réparatrice", "abdominoplastie après amaigrissement"),
            ("Chirurgie générale", "vésicule, paroi abdominale"),
            ("Chirurgie robotique", None),
        ],
        "formation": [
            "Ancienne externe des Hôpitaux de Montpellier-Nîmes",
            "Ancienne interne des Hôpitaux de Lille",
            "Ancienne cheffe de clinique des Hôpitaux de Lille — service de chirurgie endocrinienne, digestive et de l'obésité du Pr Pattou",
            "Ancienne praticienne hospitalière du CHU de Lille — même service",
        ],
        "diplomes": [
            ("Thèse de docteur en médecine", "2011"),
            ("Master 2 de sciences chirurgicales (Lille / Paris XI)", "2009"),
            ("Lauréate du prix du Chirurgien de l'Avenir (Fondation de l'Avenir, Paris)", "2009"),
            ("DES de chirurgie générale", None),
            ("DESC de chirurgie viscérale et digestive", None),
            ("DU d'anatomie abdomino-pelvienne", "2007"),
            ("DIU de chirurgie endocrinienne et métabolique", "2011"),
            ("DIU de chirurgie de l'obésité", "2013"),
            ("DIU d'endoscopie chirurgicale", "2015"),
            ("Formation en chirurgie robotique — Intuitive Surgical", None),
        ],
        "societes": [
            "Membre de la SOFFCO-MM (Société française et francophone de chirurgie de l'obésité et des maladies métaboliques)",
            "Membre de la FCVD (Fédération de chirurgie viscérale et digestive)",
        ],
        "faits": [
            "Opère un bypass gastrique avec la colonne cœlioscopique 3D des Franciscaines (mars 2025).",
            "Fait partie des chirurgiens qui ont fêté le 100e kyste pilonidal traité au laser aux Franciscaines, en moins d'un an (2025).",
        ],
        "videos": ["bypass-coelio"],
        "pathologies": ["sleeve-gastrectomie", "bypass-gastrique", "anneau-gastrique", "ballon-intragastrique",
                        "surrenales", "vesicule-biliaire", "hernie-ombilicale", "eventration"],
    },
]

PAR_SLUG = {c["slug"]: c for c in CHIRURGIENS}


def nom_complet(c):
    return f"Dr {c['prenom']} {c['nom']}"


def initiales(c):
    return c["prenom"][0] + c["nom"][0]
