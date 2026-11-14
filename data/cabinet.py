"""Cabinet, équipe paramédicale, engagements, établissements, techniques,
parcours, honoraires, actualités — tout provient du site actuel."""

PRESENTATION = [
    "Nemaudig est une association libérale de chirurgiens digestifs et viscéraux.",
    "Nous sommes cinq chirurgiens expérimentés, de la même génération, spécialisés dans l'ensemble des maladies de l'appareil digestif. Nous nous connaissons depuis notre internat, période pendant laquelle nous avons été formés dans des centres hospitaliers universitaires.",
    "Cela nous permet de vous proposer une expertise dans chaque domaine de la chirurgie digestive et d'assurer la permanence et la continuité des soins. Vous serez orienté vers celui d'entre nous le plus à même de vous prendre en charge, en respectant toujours vos souhaits et les recommandations du médecin qui vous adresse.",
]

VALEURS = [
    ("Le travail en équipe", "Discussion des dossiers difficiles, consultation commune pour les cas complexes, interventions lourdes réalisées à plusieurs chirurgiens."),
    ("La continuité des soins", "Suivi commun des patients hospitalisés après une intervention : une présence assurée 365 jours et nuits par an."),
    ("La concertation", "Recours systématique à une concertation pluridisciplinaire en cancérologie, avec les radiologues, les gastro-entérologues et les cancérologues de l'Institut de cancérologie du Gard."),
    ("Une information claire et loyale", "Remise de fiches d'information spécifiques pour la plupart des pathologies."),
    ("La proximité", "Disponibilité vis-à-vis des attentes du patient et de sa famille."),
]

LOCAUX = [
    "Le cabinet est situé à proximité immédiate de la Polyclinique du Grand Sud, dans de vastes locaux récents (2014 et 2019), lumineux, sur deux étages, avec parking, ascenseurs et accessibles aux personnes handicapées.",
    "Au 2e étage : une banque d'accueil où vous recevront nos secrétaires, deux salles d'attente et trois bureaux de consultation.",
    "Au 1er étage : un espace spécialement conçu et adapté pour accueillir les patients en situation d'obésité, avec deux bureaux de consultation, une banque d'accueil et une salle d'attente confortable.",
]

EQUIPE_PARAMEDICALE = [
    {
        "titre": "Secrétariat", "chiffre": "3", "unite": "secrétaires",
        "texte": "Accueil des patients, programmation des consultations, des examens complémentaires, des interventions et du suivi : elles raccourcissent les délais et coordonnent les étapes de votre parcours et de votre hospitalisation. Au cabinet du lundi au vendredi, de 8 h à 18 h 30.",
    },
    {
        "titre": "Aides opératoires", "chiffre": "4", "unite": "infirmières",
        "texte": "Elles accueillent les patients au bloc opératoire, préparent les interventions et assistent les chirurgiens. Disponibles comme eux 365 jours par an, elles participent à la continuité des soins.",
    },
    {
        "titre": "Stomathérapie", "chiffre": "1", "unite": "infirmière spécialisée",
        "texte": "Avant l'opération, elle explique la stomie au patient et à sa famille et repère avec eux son emplacement. Après, elle apprend à faire sa toilette, à changer la poche et à choisir l'appareillage le plus adapté. Elle reste joignable après la sortie (lésion cutanée, appareillage, vie sociale, familiale, intime). Elle intervient aussi au cabinet pour les pansements complexes.",
    },
]

ETABLISSEMENTS = [
    {
        "slug": "polyclinique-grand-sud",
        "nom": "Polyclinique du Grand Sud",
        "ville": "Nîmes",
        "role": "Interventions · urgences · soins externes",
        "detail": "Établissement privé où opère l'équipe, à deux pas du cabinet. Les Drs Amielh et Alline y réalisent le lundi matin des actes sous anesthésie locale aux soins externes.",
        "urgences": "04 66 04 31 46",
        "site": "https://www.elsan.care/fr/polyclinique-grand-sud",
        "anesthesie": {
            "nom": "Cabinet des anesthésistes de la Polyclinique du Grand Sud",
            "adresse": "Immeuble Le Méridien (3e étage), 480 avenue Saint-André de Codols — juste à côté de la Polyclinique",
            "tel": ["04 66 04 97 70", "04 66 04 07 78"],
        },
    },
    {
        "slug": "hopital-prive-franciscaines",
        "nom": "Hôpital privé des Franciscaines",
        "ville": "Nîmes",
        "role": "Interventions · cœlioscopie 3D · laser",
        "detail": "Établissement privé où opère l'équipe. Il s'est doté en mars 2025 d'une colonne de cœlioscopie 3D haute définition 4K ; c'est aussi là qu'est réalisée la chirurgie du kyste pilonidal au laser.",
        "urgences": None,
        "site": "https://www.elsan.care/fr/hopital-prive-les-franciscaines",
        "anesthesie": {
            "nom": "Cabinet des anesthésistes de l'Hôpital privé des Franciscaines",
            "adresse": "9 impasse Jean Bouin — juste à côté des Franciscaines",
            "tel": ["04 66 26 64 40"],
        },
    },
]

# Cabinet d'anesthésie listé sur la page /uzes du site actuel, sans autre
# précision (la page /les-cliniques ne cite que deux établissements). À VALIDER.
ANESTHESIE_KENNEDY = {
    "nom": "Cabinet des anesthésistes de la Clinique Kennedy",
    "adresse": "Dans la clinique Kennedy",
    "tel": ["04 66 64 06 04"],
    "site": "https://www.elsan.care/fr/polyclinique-kenval-kennedy",
}

UZES = {
    "nom": "Centre hospitalier d'Uzès",
    "chirurgien": "dr-david-amielh",
    "depuis": "1er janvier 2025",
    "creneau": "Le lundi matin",
    "tel": ["04 66 63 71 09", "04 66 63 70 00"],
    "horaires_tel": "Du lundi au vendredi, 8 h 15 – 17 h",
}

TECHNIQUES = [
    {
        "slug": "chirurgie-robotique", "ancien": "robotique", "titre": "Chirurgie robotique", "court": "Robot Da Vinci",
        "accroche": "Un robot chirurgical Da Vinci, piloté par votre chirurgien.",
        "desc": "Chirurgie robot-assistée Da Vinci à Nîmes : une technique maîtrisée par les cinq chirurgiens de Nemaudig. Présentation du robot et vidéos d'interventions.",
        "texte": "L'aide d'un robot chirurgical Da Vinci (Intuitive Surgical), piloté par votre chirurgien, peut vous être proposée pour certaines opérations : une chirurgie cœlioscopique robot-assistée.\n\nCette technique est maîtrisée par l'ensemble de l'équipe Nemaudig ; les cinq chirurgiens déclarent la chirurgie robotique parmi leurs spécialités.",
        "videos": ["robot-da-vinci", "crohn-robot", "cardia-robot", "rectum-robot", "colectomie-droite-robot", "surrenalectomie-robot"],
    },
    {
        "slug": "coelioscopie", "ancien": "coelioscopie", "titre": "Cœlioscopie et cœlioscopie 3D", "court": "Cœlioscopie 3D 4K",
        "accroche": "Opérer par de petites incisions, sous contrôle vidéo haute résolution.",
        "desc": "Cœlioscopie à Nîmes : petites cicatrices, moins de douleurs, récupération plus rapide. Colonne 3D 4K Storz aux Franciscaines depuis mars 2025.",
        "texte": "La cœlioscopie consiste à opérer avec des instruments de petite taille et une caméra de haute technologie, introduits par de petites incisions, sous contrôle vidéo sur un écran haute résolution.\n\nTout en réalisant l'intervention au moins aussi bien que par voie ouverte, elle limite les cicatrices, diminue les douleurs postopératoires et permet une mobilisation et une récupération plus précoces.\n\nUn grand nombre d'interventions peut être réalisé ainsi. Nous vous indiquerons si c'est possible dans votre cas : il existe des contre-indications, et des interventions pour lesquelles la cœlioscopie a peu d'intérêt ou relève de centres hyperspécialisés.",
        "encart": ("Mars 2025 — la 3D arrive aux Franciscaines", "L'Hôpital privé des Franciscaines a acquis pour l'équipe une colonne cœlioscopique 3D Storz, en haute définition 4K. Avec des lunettes 3D, le chirurgien voit les organes comme à l'œil nu : profondeur de champ, dissection anatomique et précision du geste. Le cabinet en attend un temps opératoire réduit, une moindre agression chirurgicale et des suites allégées."),
        "videos": ["hernie-inguinale-tep", "bypass-coelio"],
    },
    {
        "slug": "chirurgie-ambulatoire", "ancien": "ambulatoire", "titre": "Chirurgie ambulatoire", "court": "Ambulatoire",
        "accroche": "Moins de douze heures à la clinique : vous dormez chez vous.",
        "desc": "Chirurgie ambulatoire à Nîmes : hernie, vésicule, proctologie, kystes et lipomes. Conditions : moins d'une heure de route et un adulte présent la première nuit.",
        "texte": "L'ambulatoire est un mode de prise en charge où l'hospitalisation dure moins de douze heures : vous ne dormez pas à la clinique.\n\nToutes les opérations ne s'y prêtent pas. Aujourd'hui, la plupart des opérations de hernie et d'ablation de la vésicule biliaire sont réalisées ainsi, tout comme certaines opérations de la région anale et presque toutes les opérations de la peau (kystes, lésions, lipomes).",
        "conditions": ["Habiter à moins d'une heure de route", "La présence d'un adulte à domicile la première nuit", "L'absence de maladie associée imposant une surveillance plus longue"],
        "videos": [],
    },
    {
        "slug": "rehabilitation-amelioree", "ancien": "rehabilitation-amelioree", "titre": "Réhabilitation améliorée après chirurgie", "court": "Réhabilitation améliorée",
        "accroche": "Des mesures validées scientifiquement pour récupérer plus vite.",
        "desc": "Réhabilitation améliorée après chirurgie (RAAC) à Nîmes : moins de complications, récupération accélérée. Pratique reconnue par le groupe GRACE.",
        "texte": "Il s'agit d'un ensemble de mesures, toutes validées scientifiquement, qui bousculent les vieux dogmes chirurgicaux. Prises avant, pendant et après l'intervention, elles permettent de :\n\n- diminuer les effets secondaires des soins\n- diminuer le risque de complication\n- améliorer la récupération et accélérer le retour à une vie normale\n- diminuer la durée d'hospitalisation\n\nCette approche est bien validée pour la chirurgie du côlon, et l'équipe a été habilitée et reconnue pour cette pratique par le Groupe francophone de réhabilitation améliorée après chirurgie (GRACE). L'extension à d'autres chirurgies, comme celles du foie et du pancréas, est en cours.",
        "videos": [],
    },
]

TECH = {t["slug"]: t for t in TECHNIQUES}

PARCOURS = [
    ("Consultation", "Prise de rendez-vous au cabinet, en ligne ou à Uzès. Vous êtes orienté vers le chirurgien le plus à même de vous prendre en charge."),
    ("Consultation d'anesthésie", "Obligatoire avant toute anesthésie générale ou loco-régionale, auprès du cabinet d'anesthésie de l'établissement choisi. Une consultation de cardiologie peut être nécessaire avant."),
    ("Démarches", "Consentement éclairé signé et rapporté au cabinet, dépassement d'honoraires réglé au cabinet, préadmission dans l'établissement."),
    ("Intervention", "Dans l'un des deux établissements privés de Nîmes, en ambulatoire quand c'est possible, avec la réhabilitation améliorée."),
    ("Suivi", "Une ou plusieurs consultations après l'opération ; en cancérologie, un suivi régulier selon les recommandations de la Haute Autorité de santé."),
]

DEMARCHES_MEDICALES = [
    "Avant toute opération sous anesthésie générale ou loco-régionale, vous devez avoir une consultation avec un médecin anesthésiste.",
    "Prenez rendez-vous avec le cabinet d'anesthésie rattaché à l'établissement où vous serez opéré.",
    "Selon votre âge, vos habitudes de vie (tabac notamment) et vos antécédents, une consultation avec un cardiologue peut être nécessaire avant de voir l'anesthésiste.",
    "Dans tous les cas, munissez-vous de la liste de vos traitements et de votre dossier médical.",
]

DEMARCHES_ADMIN = [
    "Signer le consentement éclairé et le rapporter au cabinet avant l'opération.",
    "Régler au cabinet le dépassement d'honoraires avant l'intervention.",
    "Effectuer les formalités de préadmission dans l'établissement choisi — vous pourrez alors demander une chambre seule.",
    "Avant la fin du séjour, effectuer les formalités de sortie auprès de l'établissement.",
    "La clinique vous fera parvenir une facture à transmettre à votre mutuelle.",
]

SUIVI = [
    "Toute opération est suivie d'une ou de plusieurs consultations, pour s'assurer que l'évolution est normale et détecter toute anomalie.",
    "Pour les maladies chroniques, cancérologie comprise, le suivi est régulier et rigoureux, selon les recommandations de la Haute Autorité de santé.",
    "Les examens complémentaires sont prescrits par l'équipe.",
]

# Tarifs affichés sur le site actuel — date de mise à jour inconnue : À VALIDER.
HONORAIRES = {
    "secteur": "Les cinq chirurgiens sont conventionnés en secteur 2 : ils pratiquent des dépassements d'honoraires.",
    "lignes": [
        ("Première consultation (à la demande du médecin traitant)", "70 €", "base de remboursement 50 €"),
        ("Consultation postopératoire", "50 €", "base de remboursement 30 €"),
        ("Consultations multiples et rapprochées", "30 €", "base de remboursement 30 €"),
    ],
    "intervention": "Pour une intervention, le montant du dépassement vous est indiqué en consultation, avec un devis remis selon l'intervention prévue. Il est encaissé au cabinet et une facture vous est remise.",
    "mutuelle": "Votre complémentaire santé peut rembourser tout ou partie du dépassement, selon votre niveau de garantie, exprimé en pourcentage du tarif de la Sécurité sociale.",
    "exemple": "Exemple donné par le cabinet : pour une hernie de l'aine, le tarif Sécurité sociale s'élève à 215 €. Avec une complémentaire remboursant 200 % ou plus, un dépassement inférieur ou égal à 215 € est entièrement remboursé ; au-delà, la différence reste à votre charge.",
}

ACTUALITES = [
    {
        "slug": "ballon-intragastrique-allurion", "date": "2025-11-15", "date_txt": "Novembre 2025", "categorie": "Nouveau au cabinet",
        "titre": "Le ballon intragastrique Allurion arrive au cabinet",
        "texte": "Perdre du poids sans chirurgie : le ballon Allurion est une capsule avalée en consultation, qui se transforme en ballon dans l'estomac. Il réduit la faim et favorise la satiété pendant 4 mois avant de disparaître naturellement. Sans chirurgie ni anesthésie, perte moyenne de 10 à 15 % du poids corporel, 6 mois de suivi par une diététicienne, à partir d'un IMC de 30.",
        "lien": "/obesite/ballon-intragastrique/",
    },
    {
        "slug": "enquete-ffcv", "date": "2025-10-01", "date_txt": "Octobre 2025", "categorie": "Qualité",
        "titre": "Participation à une enquête nationale de la FFCV",
        "texte": "Les chirurgiens de l'équipe invitent leurs patients à répondre à un questionnaire national et anonyme sur la relation chirurgien-patient, édité par la Fédération française de chirurgie viscérale. Il est remis lors de la consultation postopératoire, dans le but d'améliorer sans cesse la relation avec le patient.",
        "lien": None,
    },
    {
        "slug": "congres-national-2025", "date": "2025-09-19", "date_txt": "Septembre 2025", "categorie": "Formation",
        "titre": "L'équipe au congrès national de chirurgie digestive",
        "texte": "Du 16 au 19 septembre 2025, les chirurgiens viscéraux et digestifs francophones se sont réunis au CNIT Forest, à Paris. La réunion de 9 sociétés savantes a permis une mise à niveau des dernières recommandations et la présentation de techniques innovantes. Les Drs Laporte et Amielh y étaient, avec leur aide opératoire dédiée au cabinet.",
        "lien": None,
    },
    {
        "slug": "coelioscopie-3d", "date": "2025-03-01", "date_txt": "Mars 2025", "categorie": "Technologie",
        "titre": "La cœlioscopie 3D arrive aux Franciscaines",
        "texte": "L'Hôpital privé des Franciscaines a acquis pour l'équipe une colonne cœlioscopique 3D Storz en haute définition 4K. Lunettes 3D sur le nez, le chirurgien voit les organes comme à l'œil nu, avec un gain de profondeur de champ et de précision. Le Dr Torres a notamment opéré un bypass avec cette technologie.",
        "lien": "/techniques/coelioscopie/",
    },
    {
        "slug": "100e-kyste-pilonidal-laser", "date": "2025-02-12", "date_txt": "2025", "categorie": "Étape",
        "titre": "Centième kyste pilonidal opéré au laser",
        "texte": "Précurseurs de cette technique à Nîmes, les Drs Amielh, Prieur, Alline et Torres ont fêté leur centième kyste pilonidal traité au laser aux Franciscaines, en moins d'un an : un taux de guérison élevé, une convalescence courte, une prise en charge sur devis.",
        "lien": "/pathologies/kyste-pilonidal/",
    },
    {
        "slug": "soins-anesthesie-locale", "date": "2025-02-11", "date_txt": "2025", "categorie": "Consultation",
        "titre": "Soins sous anesthésie locale le lundi matin",
        "texte": "Les Drs Amielh et Alline réalisent tous les lundis matin des actes sous anesthésie locale aux soins externes de la Polyclinique Grand Sud : ablation de lipome, de naevus, de kyste… Même sans adressage par un dermatologue, sur devis.",
        "lien": "/pathologies/kystes-et-lipomes/",
    },
    {
        "slug": "consultation-uzes", "date": "2025-01-01", "date_txt": "Janvier 2025", "categorie": "Nouveau lieu",
        "titre": "Le Dr Amielh consulte à Uzès",
        "texte": "Depuis le 1er janvier 2025, le Dr Amielh consulte le lundi matin au Centre hospitalier d'Uzès. Rendez-vous au 04 66 63 71 09 ou au 04 66 63 70 00, du lundi au vendredi de 8 h 15 à 17 h.",
        "lien": "/consultation-uzes/",
    },
]

SITES_UTILES = [
    ("Fédération de chirurgie viscérale et digestive (FCVD)", "http://www.chirurgie-viscerale.org/"),
    ("Groupe francophone de réhabilitation améliorée (GRACE)", "http://www.grace-asso.fr/"),
    ("Assurance maladie — ameli.fr", "https://www.ameli.fr/"),
]
