"""Pathologies et interventions — contenu médical repris du site actuel.

RÈGLE : le texte vient de nemaudig.fr (orthographe corrigée, phrases parfois
reformulées pour la lisibilité) ; aucune donnée médicale n'est ajoutée.
Mini-balisage des sections : paragraphes séparés par une ligne vide,
lignes « - » = puces.

`organe`   : zone surlignée sur la planche anatomique (lib/anatomie.py).
`ancien`   : slug de l'ancienne URL, pour les redirections 301.
`desc`     : meta description (unique, 70–170 caractères).
"""

FAMILLES = [
    {"slug": "oesophage-estomac", "titre": "Œsophage et estomac", "organe": "estomac",
     "intro": "Reflux, hernie hiatale et cancers de l'œsophage et de l'estomac : la partie haute du tube digestif."},
    {"slug": "foie-vesicule-pancreas", "titre": "Foie, vésicule et pancréas", "organe": "foie",
     "intro": "Calculs de la vésicule biliaire, chirurgie du foie et du pancréas."},
    {"slug": "colon-rectum", "titre": "Côlon et rectum", "organe": "colon",
     "intro": "Diverticules, maladies inflammatoires de l'intestin, cancers et chirurgie colorectale."},
    {"slug": "proctologie", "titre": "Proctologie", "organe": "anus",
     "intro": "Hémorroïdes, fissure, abcès et fistule anale, kyste pilonidal."},
    {"slug": "paroi-abdominale", "titre": "Paroi abdominale", "organe": "paroi",
     "intro": "Hernies de l'aine et du nombril, éventrations."},
    {"slug": "obesite", "titre": "Obésité", "organe": "estomac",
     "intro": "Ballon intragastrique, sleeve, bypass et anneau : un parcours pluridisciplinaire."},
    {"slug": "endocrinien", "titre": "Glandes surrénales", "organe": "surrenales",
     "intro": "Chirurgie endocrinienne des glandes surrénales."},
    {"slug": "pathologie-generale", "titre": "Peau et dispositifs", "organe": "peau",
     "intro": "Kystes, lipomes et pose de chambre implantable (port-à-cath)."},
]

FAM = {f["slug"]: f for f in FAMILLES}

PATHOLOGIES = [
    # ───────────────────────── Œsophage et estomac ─────────────────────────
    {
        "slug": "rgo", "ancien": "rgo", "famille": "oesophage-estomac", "organe": "oesophage",
        "titre": "Reflux gastro-œsophagien (RGO)", "court": "Reflux (RGO)",
        "resume": "Remontées acides ou biliaires de l'estomac vers l'œsophage.",
        "desc": "Reflux gastro-œsophagien résistant au traitement : principe de la valve anti-reflux par cœlioscopie, risques et suites. Chirurgiens digestifs à Nîmes.",
        "sections": [
            ("La maladie", "Les remontées deviennent progressivement plus nombreuses et peuvent résister au traitement par inhibiteurs de la pompe à protons (IPP).\n\nElles exposent au risque d'une brûlure progressive de l'œsophage (œsophagite) pouvant dégénérer en cancer."),
            ("L'intervention", "Elle est réalisée par cœlioscopie (mini-incisions sur l'abdomen) ou par une cicatrice au-dessus de l'ombilic.\n\nLe chirurgien confectionne une valve avec le haut de l'estomac, qui vient « cravater » l'œsophage et empêche les remontées."),
            ("Les risques", "- Plaie avec perforation de l'œsophage ou de l'estomac pendant l'opération, nécessitant une reprise chirurgicale\n- Rétrécissement initial lié à la valve, entraînant des troubles de la déglutition"),
            ("Après l'opération", "- Impossibilité d'éructer, donc davantage de gaz et de flatulences\n- La stabilisation du poids est primordiale"),
        ],
        "faq": [], "videos": [], "pdf": None,
    },
    {
        "slug": "hernie-hiatale", "ancien": "hernie-hiatale", "famille": "oesophage-estomac", "organe": "estomac",
        "titre": "Hernie hiatale", "court": "Hernie hiatale",
        "resume": "Ascension de la partie haute de l'estomac dans le thorax.",
        "desc": "Hernie hiatale : quand opérer, comment se déroule la cure par cœlioscopie, risques et alimentation après l'intervention. Nemaudig, Nîmes.",
        "sections": [
            ("La maladie", "La hernie augmente progressivement de volume, avec un risque de troubles de la digestion, de reflux gastrique et de troubles respiratoires."),
            ("L'intervention", "Par cœlioscopie (mini-incisions sur l'abdomen) ou par une cicatrice au-dessus de l'ombilic, le chirurgien :\n\n- réintègre l'estomac dans l'abdomen\n- confectionne une valve avec le haut de l'estomac qui cravate l'œsophage\n- referme l'orifice entre l'abdomen et le thorax (orifice hiatal)"),
            ("Les risques", "- Plaie avec perforation de l'œsophage ou de l'estomac pendant l'opération, nécessitant une reprise chirurgicale\n- Rétrécissement initial lié à la valve, entraînant des blocages alimentaires (dysphagie)"),
            ("Après l'opération", "- Alimentation mixée le premier mois\n- Impossibilité d'éructer, donc davantage de gaz et de flatulences\n- La stabilisation du poids est primordiale"),
        ],
        "faq": [], "videos": ["hernie-hiatale-robot"], "pdf": None,
    },
    {
        "slug": "cancer-de-l-oesophage", "ancien": "cancer-de-l-oesophage", "famille": "oesophage-estomac", "organe": "oesophage",
        "cancer": True,
        "titre": "Cancer de l'œsophage", "court": "Cancer de l'œsophage",
        "resume": "L'œsophage est le « tube » entre la bouche et l'estomac.",
        "desc": "Cancer de l'œsophage : déroulement de l'œsophagectomie, principaux risques et vie après l'opération. Chirurgie digestive et cancérologie à Nîmes.",
        "sections": [
            ("La maladie", "Le cancer de l'œsophage est une tumeur qui se crée dans la paroi de l'œsophage et grossit progressivement jusqu'à empêcher l'alimentation."),
            ("L'intervention", "Par une cicatrice sur le thorax et de petites incisions sur l'abdomen au-dessus de l'ombilic, le chirurgien retire la quasi-totalité de l'œsophage et l'ensemble des ganglions qui l'entourent.\n\nUn raccord est ensuite réalisé entre l'œsophage restant et l'estomac, transformé en tube pour permettre l'alimentation."),
            ("Les risques", "- Le principal : la fuite au niveau de la couture entre l'œsophage et l'estomac\n- Risques de saignement et d'infection respiratoire liés à l'ouverture du thorax"),
            ("Après l'opération", "- Nécessité de fractionner les repas\n- Perte de poids d'environ 20 %, qui ne sera jamais récupérée\n- Surveillance régulière pour dépister une récidive"),
        ],
        "faq": [], "videos": [], "pdf": None,
    },
    {
        "slug": "cancer-de-l-estomac", "ancien": "cancer-de-l-estomac", "famille": "oesophage-estomac", "organe": "estomac",
        "cancer": True,
        "titre": "Cancer de l'estomac", "court": "Cancer de l'estomac",
        "resume": "L'estomac est la poche située entre l'œsophage et le duodénum.",
        "desc": "Cancer de l'estomac : principe de la gastrectomie, risques, alimentation et suivi après l'opération. Chirurgiens digestifs Nemaudig à Nîmes.",
        "sections": [
            ("La maladie", "Le cancer de l'estomac est une tumeur qui se crée dans la paroi de l'estomac et grossit progressivement jusqu'à empêcher l'alimentation."),
            ("L'intervention", "Par une cicatrice au-dessus de l'ombilic, le chirurgien retire complètement l'estomac et l'ensemble des ganglions qui l'entourent.\n\nUn raccord est alors réalisé entre l'œsophage et l'intestin grêle pour permettre l'alimentation."),
            ("Les risques", "Le principal est la fuite au niveau de la couture entre l'œsophage et l'intestin."),
            ("Après l'opération", "- Nécessité de fractionner les repas\n- Perte de poids d'environ 20 %, qui ne sera jamais récupérée\n- Surveillance régulière pour dépister une récidive"),
        ],
        "faq": [], "videos": ["cardia-robot"], "pdf": None,
    },
    # ───────────────────────── Foie, vésicule, pancréas ─────────────────────────
    {
        "slug": "vesicule-biliaire", "ancien": "vesicule-biliaire", "famille": "foie-vesicule-pancreas", "organe": "vesicule",
        "titre": "Calculs de la vésicule biliaire", "court": "Vésicule biliaire",
        "resume": "La vésicule biliaire stocke la bile pour l'évacuer en grande quantité lorsque l'on mange.",
        "desc": "Calculs de la vésicule biliaire à Nîmes : pourquoi retirer la vésicule, opération par cœlioscopie en ambulatoire, et réponses aux questions fréquentes.",
        "sections": [
            ("Le rôle de la vésicule", "La bile sert à la digestion des aliments. Elle est fabriquée par le foie, qui l'évacue vers l'intestin par un petit canal : le canal cholédoque.\n\nLa vésicule biliaire stocke la bile pour l'évacuer en grande quantité lorsque l'on mange."),
            ("La maladie", "La vésicule peut fabriquer des calculs, qui peuvent occasionner des complications.\n\nLorsque c'est le cas, il n'y a qu'une solution : l'ablation de la vésicule, ou cholécystectomie."),
            ("L'intervention", "L'opération se déroule la plupart du temps sous cœlioscopie : une caméra introduite dans le ventre et trois ou quatre pinces permettent de retirer la vésicule sans grande cicatrice.\n\nEn l'absence de contre-indication, elle se déroule en ambulatoire, c'est-à-dire sur une journée d'hospitalisation."),
            ("Les risques", "Comme toute intervention, elle peut se compliquer, notamment d'une fuite de bile pouvant nécessiter d'autres interventions dans un second temps."),
            ("Après l'opération", "Il n'y a pas de conséquence à l'ablation de la vésicule, hormis la disparition des signes liés aux calculs. L'organisme s'adapte très bien et rapidement à son absence : aucune conséquence sur la digestion, aucun régime spécifique."),
        ],
        "faq": [
            ("Existe-t-il un autre moyen de retirer les calculs sans opération ?", "Non. Aucun médicament ne dissout les calculs. Retirer simplement les calculs sans retirer la vésicule exposerait à la récidive, car ce sont les calculs que fabrique la vésicule."),
            ("Y a-t-il un régime ou des problèmes de digestion après l'ablation de la vésicule ?", "Il n'y a aucun régime spécifique à mettre en place après l'opération, ni aucune conséquence sur la digestion."),
            ("Peut-on retirer les calculs de la vésicule par laser ?", "Non. Le laser est parfois utilisé pour fragmenter les calculs du rein, facilement éliminés ensuite dans les urines. Fragmenter les calculs de la vésicule exposerait à leur migration dans le cholédoque et pourrait déclencher une pancréatite aiguë, la complication la plus grave des calculs de la vésicule."),
            ("Faut-il un régime après l'ablation de la vésicule biliaire ?", "La vésicule n'est pas indispensable à la digestion : aucun régime n'est à suivre à long terme, on peut manger de tout en quantité raisonnable. Pendant la semaine qui suit l'intervention, privilégiez une alimentation légère, pauvre en graisses, le temps que le système digestif s'ajuste."),
        ],
        "videos": [], "pdf": "https://nemaudig.fr/_objects/tao_medias/file/fiche-cholecystectomie-19.pdf",
    },
    {
        "slug": "cholecystectomie", "ancien": "la-cholecystectomie", "famille": "foie-vesicule-pancreas", "organe": "vesicule",
        "titre": "La cholécystectomie", "court": "Cholécystectomie",
        "resume": "L'ablation chirurgicale de la vésicule biliaire, seul traitement des calculs compliqués.",
        "desc": "Cholécystectomie (ablation de la vésicule biliaire) : indications, déroulement, durée, complications possibles et signes d'alerte. Nemaudig, Nîmes.",
        "sections": [
            ("Pourquoi opérer ?", "La bile, fabriquée par le foie, est déversée dans l'intestin par le canal cholédoque. Au bord de ce canal se trouve une « aire de repos » : la vésicule biliaire. La bile peut y sédimenter et former des calculs.\n\nLorsque ces calculs donnent des complications, il n'existe qu'un seul traitement : l'ablation de la vésicule. S'ils ne donnent aucun trouble (découverte fortuite par exemple), il est inutile de les traiter ou même de les surveiller."),
            ("Les complications des calculs", "- La douleur (colique hépatique) : au niveau de l'estomac, au moins une demi-heure, parfois vers le dos ou l'épaule droite, avec nausées ou vomissements\n- La fièvre, en général avec des douleurs, témoin d'une inflammation de la vésicule : c'est une urgence\n- La pancréatite, rare mais parfois gravissime, pouvant nécessiter un séjour en réanimation\n- La jaunisse (ictère), liée au passage de calculs dans le cholédoque\n- La jaunisse avec fièvre (angiocholite), infection très grave nécessitant une hospitalisation en urgence\n\nLe diagnostic repose sur l'échographie. Même sans trouble au moment de l'examen, il faut opérer sans attendre la deuxième crise, afin d'éviter une complication plus grave."),
            ("Avant l'opération", "Le chirurgien recherche des signes de calculs associés dans le canal cholédoque (jusqu'à 15 % des cas, davantage avec l'âge). S'il en existe, il peut les confirmer par une radio pendant l'opération (cholangiographie) et les retirer, ou les faire retirer avant l'opération par voie endoscopique."),
            ("Le déroulement", "La cholécystectomie est souvent réalisée par cœlioscopie, sous anesthésie générale, avec une à quatre incisions de 5 à 20 mm. Une ouverture plus large (laparotomie) peut être prévue ou décidée pendant l'opération en cas de difficulté.\n\n- Entrée la veille ou le jour de l'opération\n- Durée de l'opération : entre 45 minutes et 2 heures\n- Sortie le jour même ou dans les jours qui suivent\n- La vésicule est analysée au microscope ; la remise des calculs au patient n'est pas autorisée\n- Un arrêt de travail de quelques jours est prescrit"),
            ("Les complications possibles", "Comme toute opération, il existe un risque de saignement justifiant une surveillance étroite et parfois une réintervention.\n\nLa principale complication est la blessure des voies biliaires, dans moins de 1 % des cas ; elle peut nécessiter une ou plusieurs réinterventions et éventuellement un transfert en centre spécialisé.\n\nIl existe enfin des complications très exceptionnelles liées à la cœlioscopie (blessure de l'intestin ou d'un gros vaisseau, embolie pulmonaire). Chez les patients à risque de phlébite, un traitement préventif est entrepris."),
            ("Signes d'alerte après le retour à domicile", "Contactez votre chirurgien sans attendre la consultation postopératoire en cas de :\n\n- essoufflement\n- douleurs abdominales aiguës ou intenses\n- fièvre\n- douleurs des épaules, en particulier à droite"),
        ],
        "faq": [], "videos": [], "pdf": "https://nemaudig.fr/_objects/tao_medias/file/fiche-cholecystectomie-19.pdf",
    },
    {
        "slug": "foie", "ancien": "le-foie", "famille": "foie-vesicule-pancreas", "organe": "foie",
        "titre": "Chirurgie du foie (hépatectomie)", "court": "Foie",
        "resume": "Le foie nettoie et épure le sang, fabrique des protéines et stocke des molécules.",
        "desc": "Chirurgie du foie à Nîmes : pourquoi une hépatectomie, comment limiter le saignement, le foie repousse-t-il ? Explications des chirurgiens de Nemaudig.",
        "sections": [
            ("L'organe", "Le foie est situé sous les côtes, à droite. Il nettoie et épure le sang, fabrique des protéines et stocke des molécules : c'est un organe indispensable à la vie.\n\nEn chirurgie, on le décompose en deux parties, le foie droit et le foie gauche, chacune alimentée par une artère, une veine et un canal biliaire."),
            ("Pourquoi opérer ?", "Les opérations du foie, ou hépatectomies, sont le plus souvent décidées pour retirer des cancers — primitifs du foie ou métastases d'autres cancers — et plus rarement des tumeurs bénignes pouvant dégénérer."),
            ("Les risques", "Le risque principal pendant l'opération est le saignement : le foie est une éponge pleine de petits et gros vaisseaux. Diverses techniques, notamment de clampage des vaisseaux, permettent de réduire ce risque.\n\nIl faut aussi laisser suffisamment de foie pour une vie normale : des techniques permettent d'estimer le volume restant, voire de faire grossir avant l'opération la partie qui sera conservée.\n\nAprès l'opération, des fuites de bile peuvent survenir sur la tranche de section, nécessitant parfois un drainage et une hospitalisation prolongés."),
        ],
        "faq": [
            ("Le foie repousse-t-il ?", "Oui, le foie grossit après l'ablation d'une partie. Cela prend cependant plusieurs semaines, et il faut être sûr qu'il en reste suffisamment juste après l'opération."),
        ],
        "videos": [], "pdf": None,
    },
    {
        "slug": "cancer-du-pancreas", "ancien": "cancer-du-pancreas", "famille": "foie-vesicule-pancreas", "organe": "pancreas",
        "cancer": True,
        "titre": "Cancer du pancréas", "court": "Cancer du pancréas",
        "resume": "Le pancréas est un organe profond, situé en arrière de l'estomac.",
        "desc": "Cancer du pancréas : duodéno-pancréatectomie céphalique et spléno-pancréatectomie caudale, risques et conséquences. Chirurgie digestive à Nîmes.",
        "sections": [
            ("L'organe", "De forme grossièrement triangulaire, le pancréas est encastré par sa tête dans le duodénum ; sa queue se termine au niveau de la rate. Le cholédoque (canal de la bile) traverse sa tête.\n\nIl fabrique des enzymes qui participent à la digestion, et l'insuline, qui régule le taux de sucre dans le sang."),
            ("La maladie", "Située dans la tête du pancréas, la tumeur peut comprimer le canal de la bile et provoquer une jaunisse (ictère). Elle peut aussi se développer sans symptôme. En dehors de l'ictère, elle se manifeste le plus souvent par des douleurs abdominales."),
            ("Les interventions", "Selon la localisation de la tumeur :\n\n- La duodéno-pancréatectomie céphalique (tumeurs de la tête) : ablation de la tête du pancréas, du duodénum, de la partie terminale du cholédoque et de la vésicule, puis trois coutures pour rétablir la continuité (canal pancréatique, canal biliaire, tube digestif). Elle nécessite une large ouverture de l'abdomen.\n- La spléno-pancréatectomie caudale (tumeurs de la queue) : ablation de la queue du pancréas et de la rate, par une grande ouverture ou par cœlioscopie."),
            ("Les risques", "Le risque principal est la fuite de liquide pancréatique dans le ventre, pouvant provoquer une infection intra-abdominale ou une hémorragie potentiellement très grave. Le pronostic vital est engagé lors de ces opérations."),
            ("Après l'opération", "- Diabète (perte d'une partie de la fabrication d'insuline)\n- Diarrhées (perte d'une partie de la fonction digestive)\n- En cas d'ablation de la rate : antibiotiques pendant 3 ans et plusieurs vaccins"),
        ],
        "faq": [], "videos": [], "pdf": None,
    },
    # ───────────────────────── Côlon et rectum ─────────────────────────
    {
        "slug": "diverticules-du-sigmoide", "ancien": "diverticules-du-colon-sigmoide", "famille": "colon-rectum", "organe": "sigmoide",
        "titre": "Diverticules du côlon sigmoïde", "court": "Diverticulite",
        "resume": "De petites poches fragiles qui se forment sur la paroi du côlon et peuvent s'enflammer.",
        "desc": "Diverticulite du côlon sigmoïde : quand opérer, sigmoïdectomie par cœlioscopie, risques et réhabilitation améliorée. Chirurgiens digestifs à Nîmes.",
        "sections": [
            ("Anatomie", "Les diverticules sont de petites hernies de la muqueuse (revêtement interne du côlon) à travers la musculeuse (couche externe), formant de fragiles petites poches à l'extérieur du côlon.\n\nIls siègent le plus souvent dans la partie terminale du côlon, le côlon sigmoïde — c'est aussi là qu'ils se compliquent le plus souvent."),
            ("La maladie", "Les diverticules peuvent s'enflammer : c'est la diverticulite. Une perforation peut alors survenir, avec un abcès localisé ou une péritonite.\n\nLa répétition des poussées peut conduire à un rétrécissement du côlon (sténose), voire à une communication anormale avec la vessie ou le vagin (fistule)."),
            ("Quand opérer ?", "- En urgence, lors d'une poussée compliquée (abcès, perforation) — un anus artificiel est alors parfois nécessaire\n- En raison de la répétition des poussées inflammatoires\n- En raison des séquelles des poussées répétées (sténose ou fistule)"),
            ("L'intervention", "Elle consiste à retirer le segment de côlon porteur des diverticules responsables — presque toujours le sigmoïde — puis à recoudre les deux extrémités : c'est l'anastomose.\n\nElle est réalisée le plus souvent par cœlioscopie : moins douloureuse, elle abîme moins la paroi et permet une récupération plus rapide. Une ouverture classique (laparotomie) est parfois nécessaire."),
            ("Les risques", "Pendant l'intervention :\n\n- blessure de l'intestin grêle ou de l'uretère\n- hémorragie pouvant nécessiter une transfusion\n- compressions nerveuses des membres, risques liés au bistouri électrique\n\nDans les jours qui suivent :\n\n- fuite sur la couture (fistule anastomotique), dans environ 5 à 8 % des cas : complication grave qui nécessite presque toujours une réintervention, souvent avec une stomie temporaire\n- saignement, infection (abdominale, urinaire, pulmonaire, sur cathéter)\n- phlébite, embolie pulmonaire"),
            ("Les suites", "Le plus souvent simples, avec une reprise du transit en deux à trois jours. Grâce à la réhabilitation améliorée, la sortie est possible entre le 2e et le 5e jour en l'absence de complication. Un rendez-vous de contrôle a lieu dans les 10 jours."),
        ],
        "faq": [], "videos": [], "pdf": None,
    },
    {
        "slug": "mici", "ancien": "mici-maladies-inflammatoires-chroniques-de-l-intestin", "famille": "colon-rectum", "organe": "intestin",
        "titre": "MICI : maladie de Crohn et rectocolite hémorragique", "court": "MICI (Crohn, RCH)",
        "resume": "Des maladies qui provoquent une inflammation d'une partie plus ou moins étendue de l'intestin.",
        "desc": "Maladie de Crohn et rectocolite ulcéro-hémorragique : place de la chirurgie, interventions possibles et conséquences. Chirurgiens digestifs Nemaudig, Nîmes.",
        "sections": [
            ("Définition", "Il en existe deux principales :\n\n- la maladie de Crohn, qui peut toucher tout l'intestin grêle, le côlon et le rectum, jusqu'à l'anus\n- la rectocolite ulcéro-hémorragique (RCUH), qui peut atteindre le côlon et le rectum, mais jamais l'intestin grêle"),
            ("Le trajet digestif", "Les aliments passent par l'œsophage, l'estomac, le duodénum, puis l'intestin grêle (jéjunum puis iléon). Vient ensuite le côlon — droit, transverse, gauche puis sigmoïde — et enfin le rectum, réservoir d'environ 15 cm, qui se termine par l'anus."),
            ("Diagnostic", "Il repose principalement sur l'endoscopie (caméra introduite par la bouche ou par l'anus), parfois complétée par une prise de sang ou de l'imagerie (échographie, scanner, IRM)."),
            ("Conséquences de la maladie", "- douleurs, diarrhées, saignements dans les selles\n- perforation, avec risque d'abcès ou de péritonite\n- fistule vers un autre segment digestif ou un autre organe (vessie, vagin)\n- rétrécissement (sténose), pouvant aller jusqu'à l'occlusion\n- dénutrition\n- risque de cancérisation"),
            ("Les traitements", "Les traitements médicaux sont prescrits et surveillés par les gastro-entérologues (salicylés, corticoïdes, immunosuppresseurs, biothérapies…).\n\nLa chirurgie intervient pour traiter une complication, compléter un traitement médical insuffisant, ou en cas d'évolution vers le cancer.\n\n- Maladie de Crohn : on retire le segment malade en étant le plus économe possible. La chirurgie ne guérit pas définitivement la maladie. Le risque de fuite sur la couture est plus élevé, du fait de la maladie elle-même.\n- Rectocolite : la chirurgie peut aussi viser à éradiquer la maladie, en retirant le côlon et le rectum puis en confectionnant un réservoir avec l'intestin grêle, raccordé à l'anus. Elle se déroule en 2 ou 3 étapes, avec une stomie temporaire."),
            ("Conséquences de la chirurgie", "Selon le geste réalisé : altération de la continence, conséquences nutritionnelles ou sexuelles. Un anus artificiel est parfois nécessaire, de façon transitoire ou définitive. Les risques sont ceux de la chirurgie colique ou rectale."),
        ],
        "faq": [], "videos": ["crohn-robot"], "pdf": None,
    },
    {
        "slug": "chirurgie-colique", "ancien": "chirurgie-colique", "famille": "colon-rectum", "organe": "colon",
        "titre": "Chirurgie du côlon (colectomie)", "court": "Chirurgie colique",
        "resume": "Retirer la zone malade du côlon puis rétablir le circuit intestinal.",
        "desc": "Colectomie : indications, anastomose, cœlioscopie ou laparotomie, risques pendant et après l'intervention. Chirurgie colorectale à Nîmes avec Nemaudig.",
        "sections": [
            ("Anatomie", "Le côlon, ou gros intestin, fait suite à l'intestin grêle et se termine par le rectum. Il comprend le côlon droit (ascendant), le côlon transverse, puis le côlon gauche, dont la partie terminale est le côlon sigmoïde."),
            ("Indications", "- certains polypes\n- les diverticules\n- les maladies inflammatoires (maladie de Crohn, rectocolite ulcéro-hémorragique)\n- les cancers\n\nL'indication peut être posée par le gastro-entérologue, le chirurgien digestif, le cancérologue, ou par une concertation entre les trois (réunion pluridisciplinaire)."),
            ("La technique", "L'intervention retire la zone malade, plus ou moins étendue, puis rétablit le circuit intestinal par une couture entre les deux extrémités : l'anastomose, faite à la main ou à l'agrafeuse. En cas de cancer, les ganglions de drainage sont également retirés.\n\nUne stomie (anus artificiel) peut parfois être nécessaire, temporaire ou définitive.\n\nL'intervention se fait par cœlioscopie ou par ouverture du ventre (laparotomie), selon le type de maladie, les antécédents de chirurgie abdominale et les autres maladies."),
            ("Les risques", "Pendant l'intervention :\n\n- blessure de l'intestin grêle ou de l'uretère\n- hémorragie pouvant nécessiter une transfusion\n- compressions nerveuses des membres, risques liés au bistouri électrique\n\nDans les jours qui suivent :\n\n- fuite sur la couture (fistule anastomotique), dans environ 5 à 8 % des cas : complication grave nécessitant presque toujours une réintervention, souvent avec une stomie temporaire\n- saignement, infection (abdominale, urinaire, pulmonaire, sur cathéter)\n- phlébite, embolie pulmonaire"),
        ],
        "faq": [
            ("Vais-je devoir boire une purge ?", "Sauf exception, aucune purge n'est nécessaire avant une intervention sur le côlon."),
            ("Aurai-je un régime ?", "Une opération du côlon ne nécessite aucun régime durable. La réalimentation normale en 24 à 48 heures est la règle, en l'absence de nausées ou de vomissements."),
            ("Quand pourrai-je me lever ?", "Le plus souvent le jour même de l'opération ; la marche est normalisée en deux à trois jours."),
            ("Vais-je avoir mal ?", "Toute opération engendre des douleurs, mais les moyens actuels permettent d'en atténuer considérablement l'intensité."),
            ("Vais-je dormir pendant l'opération ?", "Oui, obligatoirement. Dans certains cas, une péridurale peut être proposée en complément de l'anesthésie générale, pour calmer les douleurs pendant 2 à 4 jours après l'opération."),
            ("Vais-je aller en soins intensifs ?", "Pas systématiquement, mais c'est possible en cas de certains problèmes de santé."),
            ("Aurai-je mal en allant à la selle ?", "Normalement non."),
            ("Peut-on mourir des suites de cette opération ?", "Oui, mais le risque est aujourd'hui bien inférieur à 1 %."),
        ],
        "videos": ["colectomie-angulaire-gauche", "colectomie-droite-robot"],
        "pdf": "https://nemaudig.fr/_objects/tao_medias/file/fiche-chirurgie-colique-1-17.pdf",
    },
    {
        "slug": "cancer-du-colon", "ancien": "cancer-du-colon", "famille": "colon-rectum", "organe": "colon",
        "cancer": True,
        "titre": "Cancer du côlon", "court": "Cancer du côlon",
        "resume": "Une tumeur qui se développe dans la paroi du gros intestin.",
        "desc": "Cancer du côlon : colectomie le plus souvent par cœlioscopie, principaux risques, vie après l'opération et surveillance. Nemaudig, chirurgie digestive à Nîmes.",
        "sections": [
            ("Anatomie", "Le côlon (« gros intestin ») est la portion du tube digestif située entre l'intestin grêle et le rectum. On le divise en côlon droit, transverse, gauche et sigmoïde."),
            ("La maladie", "La tumeur peut grossir jusqu'à boucher complètement l'intestin (occlusion), saigner (sang dans les selles, ou rectorragies), ou envoyer des cellules cancéreuses dans d'autres organes comme le foie (métastases)."),
            ("L'intervention", "La chirurgie retire le segment de côlon atteint et les ganglions voisins, puis raccorde les deux extrémités.\n\nLe plus souvent, elle est réalisée par cœlioscopie : 4 à 5 petites cicatrices et une incision de 5 à 10 cm pour extraire la partie retirée."),
            ("Les risques", "Le risque principal est la fistule, c'est-à-dire une fuite au niveau de la couture. Elle nécessite souvent une nouvelle opération, voire une stomie (anus artificiel) temporaire, en raison du risque d'abcès ou de péritonite. Comme toute chirurgie, il existe un risque de saignement."),
            ("Après l'opération", "- Diarrhées ou selles plus fréquentes pendant quelques semaines\n- Pas de restriction alimentaire, même si certains aliments sont parfois moins bien tolérés\n- Surveillance régulière (examen clinique et scanner) pour dépister une éventuelle récidive"),
        ],
        "faq": [], "videos": ["colectomie-angulaire-gauche", "colectomie-droite-robot"], "pdf": None,
    },
    {
        "slug": "cancer-du-rectum", "ancien": "cancer-du-rectum", "famille": "colon-rectum", "organe": "rectum",
        "cancer": True,
        "titre": "Cancer du rectum", "court": "Cancer du rectum",
        "resume": "Une tumeur de la partie terminale du tube digestif, entre le côlon et l'anus.",
        "desc": "Cancer du rectum : déroulement de la proctectomie par cœlioscopie ou robot, stomie temporaire, risques et séquelles possibles. Chirurgiens digestifs à Nîmes.",
        "sections": [
            ("Anatomie", "Le rectum est la partie terminale du tube digestif, entre le côlon et l'anus. Il joue un rôle de réservoir pour les selles."),
            ("La maladie", "La tumeur peut boucher le tube digestif (occlusion), saigner (rectorragies) ou envoyer des cellules cancéreuses vers d'autres organes comme le foie et les poumons (métastases)."),
            ("L'intervention", "Elle retire la partie malade du rectum, la graisse qui l'entoure (avec ses ganglions) et la partie terminale du côlon, puis raccorde le côlon au rectum restant — ou à l'anus si tout le rectum a été retiré.\n\nElle est le plus souvent réalisée par cœlioscopie (4 à 5 petites cicatrices et une incision de 5 à 10 cm au-dessus du pubis), voire avec l'aide du robot chirurgical.\n\nUne stomie temporaire est fréquente pour protéger la cicatrisation de la couture ; elle est supprimée lors d'une deuxième opération, 6 à 8 semaines plus tard. L'opération est souvent précédée d'une radiothérapie associée à une chimiothérapie."),
            ("Les risques", "Le principal risque est la fistule, c'est-à-dire une fuite au niveau de la couture entre le côlon et le rectum, qui peut nécessiter une nouvelle opération (risque d'abcès ou de péritonite). Comme toute chirurgie, il existe un risque de saignement."),
            ("Après l'opération", "L'ablation du rectum est une chirurgie lourde qui peut laisser des séquelles plus ou moins invalidantes :\n\n- troubles du transit : selles plus fréquentes, sensation de vidange incomplète, faux besoins\n- si la tumeur est proche du sphincter : risque d'incontinence partielle aux gaz, voire aux selles\n- les nerfs sexuels cheminent autour du rectum : chez l'homme, éjaculation rétrograde ou troubles de l'érection ; chez la femme, troubles de la lubrification ou douleurs pendant les rapports"),
        ],
        "faq": [], "videos": ["rectum-robot"], "pdf": None,
    },
    {
        "slug": "chirurgie-rectale", "ancien": "chirurgie-rectale", "famille": "colon-rectum", "organe": "rectum",
        "titre": "Chirurgie du rectum", "court": "Chirurgie rectale",
        "resume": "Interventions conservatrices ou non sur le segment terminal de l'intestin.",
        "desc": "Chirurgie rectale : affections bénignes et malignes, interventions conservatrices, cœlioscopie ou laparotomie, risques et durée d'hospitalisation. Nîmes.",
        "sections": [
            ("Anatomie", "Le rectum fait suite au côlon sigmoïde et se termine par l'anus. On distingue le rectum pelvien (ampoule rectale), qui sert de réservoir, et le canal anal (2 à 3 cm), fermé par le sphincter, qui assure la continence.\n\nIl est en contact étroit avec l'utérus et le vagin chez la femme, avec la vessie, les vésicules séminales et la prostate chez l'homme ; en arrière avec le sacrum, latéralement avec les uretères et les vaisseaux du bassin."),
            ("Le but de la chirurgie", "Elle s'adresse à des affections bénignes (polypes, tumeur villeuse, prolapsus, hémorroïdes, maladies inflammatoires) ou malignes (cancer).\n\n- Les interventions conservatrices préservent le canal anal et le sphincter, et donc une continence normale\n- Les interventions non conservatrices les suppriment et se terminent par un anus artificiel définitif (colostomie)"),
            ("Le déroulement", "Par cœlioscopie ou par laparotomie (incision verticale), parfois associée à un abord périnéal.\n\nLa cœlioscopie limite les cicatrices et les douleurs et permet une récupération plus rapide. Le ventre est gonflé avec du gaz carbonique, et les instruments passent par des trocarts sous contrôle d'une caméra. Le principe de l'opération reste le même qu'à ventre ouvert ; en cas de difficulté, le chirurgien peut devoir convertir en ouverture classique."),
            ("Les risques", "Aucune intervention n'est dénuée de risques ; ils sont rares et en général bien maîtrisés.\n\nPendant l'intervention : blessure d'un organe proche, hémorragie, compression nerveuse, traumatisme urétéral.\n\nAprès l'intervention : fistule anastomotique, saignement, infection, occlusion intestinale ; complications des stomies, périnéales ou urinaires ; phlébite, voire embolie pulmonaire, extrêmement rares grâce à la prévention systématique."),
            ("Les suites", "Le transit reprend tôt, en 2 à 3 jours, ce qui permet de se réalimenter. La durée d'hospitalisation est de 6 à 8 jours."),
        ],
        "faq": [], "videos": ["rectum-robot"],
        "pdf": "https://nemaudig.fr/_objects/tao_medias/file/fiche-chirurgie-rectale-1-18.pdf",
    },
    # ───────────────────────── Proctologie ─────────────────────────
    {
        "slug": "hemorroides", "ancien": "hemorroides", "famille": "proctologie", "organe": "anus",
        "titre": "Hémorroïdes", "court": "Hémorroïdes",
        "resume": "Des vaisseaux présents chez tous, qui deviennent une maladie lorsqu'ils sont gênants.",
        "desc": "Maladie hémorroïdaire : traitements médicaux et instrumentaux, opérations de Milligan-Morgan et de Longo, complications. Proctologie chirurgicale à Nîmes.",
        "sections": [
            ("Comprendre", "Les hémorroïdes sont des vaisseaux sanguins présents chez tous les individus, à l'intérieur de l'anus (hémorroïdes internes) ou sous la peau de l'anus (externes). Elles participent à la continence.\n\nOn parle de maladie hémorroïdaire lorsqu'elles deviennent gênantes : douleurs, saignements, suintements, démangeaisons."),
            ("Les traitements", "Le traitement est souvent médical (suppositoires, crèmes) ou instrumental (injection, ligature élastique).\n\nEn cas d'échec ou de complications répétées, une opération peut être envisagée :\n\n- retirer les paquets hémorroïdaires : technique de Milligan et Morgan\n- agrafer les hémorroïdes à l'intérieur de l'anus : technique de Longo notamment"),
            ("Les complications", "Elles sont rares : saignement postopératoire, douleurs prolongées, surinfection des plaies, troubles urinaires précoces."),
        ],
        "faq": [("Vais-je avoir mal après l'opération ?", "Les douleurs postopératoires varient d'un patient à l'autre. Les médicaments prescrits sont souvent très efficaces pour les soulager.")],
        "videos": [], "pdf": None,
    },
    {
        "slug": "fissure-anale", "ancien": "fissure-anale", "famille": "proctologie", "organe": "anus",
        "titre": "Fissure anale", "court": "Fissure anale",
        "resume": "Une déchirure de la peau du canal anal, douloureuse surtout au passage des selles.",
        "desc": "Fissure anale : traitement médical d'abord, chirurgie en cas d'échec, durée de cicatrisation et précautions après l'opération. Proctologie à Nîmes.",
        "sections": [
            ("Comprendre", "La fissure anale est une déchirure de la peau du canal anal, responsable d'une douleur surtout lors du passage des selles."),
            ("Le traitement", "Il est le plus souvent médical. En cas d'échec, la chirurgie est une alternative : elle consiste à retirer la fissure pour laisser en place des tissus sains, capables de cicatriser.\n\nLa cicatrisation est cependant longue : entre 6 semaines et 4 mois."),
        ],
        "faq": [("Quelles précautions après une chirurgie de la fissure anale ?", "Il faut veiller à ne pas être constipé, pour éviter le passage de selles trop dures sur la cicatrice.")],
        "videos": [], "pdf": None,
    },
    {
        "slug": "abces-et-fistule-anale", "ancien": "abces-de-l-anus-et-fistule-anale", "famille": "proctologie", "organe": "anus",
        "titre": "Abcès de l'anus et fistule anale", "court": "Abcès et fistule",
        "resume": "Douleur intense et grosseur autour de l'anus, liées à une fistule.",
        "desc": "Abcès de la marge anale et fistule anale : symptômes, drainage chirurgical et traitement de la fistule en préservant la continence. Proctologie à Nîmes.",
        "sections": [
            ("L'abcès", "Il se manifeste par des douleurs intenses autour de l'anus et une grosseur qui apparaît progressivement. Il peut se drainer spontanément — l'écoulement de pus soulage alors instantanément — ou nécessiter un drainage par le chirurgien au bloc opératoire."),
            ("La fistule", "C'est une communication anormale entre l'intérieur de l'anus et la peau qui l'entoure. Elle est à l'origine des abcès dans les formes aiguës, ou d'un trajet chronique : un petit orifice près de l'anus, avec un écoulement permanent qui ne cicatrise jamais."),
            ("Les traitements", "- Abcès : évacuer le pus lors d'une opération\n- Fistule : supprimer le trajet anormal en préservant la continence anale"),
        ],
        "faq": [("L'abcès anal est-il lié à une mauvaise hygiène ?", "Pas du tout. Il est lié à la surinfection d'une glande à l'intérieur de l'anus ; il n'y a pas de rapport direct avec l'hygiène.")],
        "videos": [], "pdf": None,
    },
    {
        "slug": "kyste-pilonidal", "ancien": "kyste-saccro-coccygien-ou-kyste-pilonidal", "famille": "proctologie", "organe": "sacrum",
        "titre": "Kyste pilonidal (sacro-coccygien)", "court": "Kyste pilonidal",
        "resume": "Une inflammation du sillon interfessier liée à la pénétration de poils sous la peau.",
        "desc": "Kyste pilonidal à Nîmes : traitement chirurgical, cicatrisation, et chirurgie au laser — 100e kyste traité au laser aux Franciscaines par l'équipe Nemaudig.",
        "sections": [
            ("Comprendre", "Le kyste sacro-coccygien, ou kyste pilonidal, se manifeste par une inflammation au niveau du sillon interfessier, secondaire à la pénétration de poils sous la peau. Il entraîne des abcès ou des écoulements intermittents."),
            ("Le traitement", "Il s'agit d'abord de supprimer l'abcès s'il existe, en incisant la peau. Secondairement, il faut retirer la totalité du kyste ; la plaie est laissée ouverte et couverte d'un pansement cicatrisant.\n\nUne hémorragie peut parfois survenir pendant la cicatrisation et nécessiter une reprise chirurgicale. Le kyste peut aussi récidiver malgré une excision importante."),
            ("La chirurgie au laser", "Précurseurs de la chirurgie du kyste pilonidal au laser à Nîmes, les Drs Amielh, Prieur, Alline et Torres ont fêté en 2025 leur centième kyste pilonidal traité au laser aux Franciscaines, en moins d'un an.\n\nLe cabinet met en avant un taux de guérison élevé et une convalescence courte. La prise en charge se fait sur devis."),
        ],
        "faq": [("La cicatrisation après chirurgie du kyste pilonidal est-elle longue ?", "Oui. Elle est généralement obtenue entre 6 semaines et 6 mois.")],
        "videos": [], "pdf": None,
    },
    # ───────────────────────── Paroi abdominale ─────────────────────────
    {
        "slug": "hernie-inguinale", "ancien": "hernie-inguinale", "famille": "paroi-abdominale", "organe": "aine",
        "titre": "Hernie inguinale (hernie de l'aine)", "court": "Hernie inguinale",
        "resume": "Un gonflement de l'aine, accentué debout et à l'effort.",
        "desc": "Hernie inguinale à Nîmes : opération par incision ou cœlioscopie (technique TEP), risques, reprise du sport et arrêt de travail. Chirurgiens Nemaudig.",
        "sections": [
            ("La maladie", "Le gonflement correspond à un relâchement de l'orifice inguinal, à travers lequel passe une partie du contenu de l'abdomen.\n\nIl augmente progressivement de volume, avec un risque d'incarcération de l'intestin dans la hernie : c'est l'urgence de l'étranglement herniaire."),
            ("L'intervention", "La paroi est renforcée par une couture ou par un voile de tissu synthétique (plaque, prothèse, filet).\n\nElle est réalisée par une incision unique à l'aine, ou par cœlioscopie (mini-incision proche du nombril). Le Dr Amielh présente en vidéo sa technique par cœlioscopie extrapéritonéale, qui limite les douleurs postopératoires."),
            ("Les risques", "- Sérome : bosse de liquide clair à la place de la hernie\n- Ecchymose : placard bleu, pouvant diffuser chez l'homme dans la verge et les bourses (insensibilité, augmentation de volume des bourses)\n- Infection de la prothèse"),
            ("Après l'opération", "- Pas d'effort important pendant quatre semaines (port de charges de plus de 5 kg)\n- Ni sport ni charges de plus de 15 kg pendant un mois\n- Pas de conduite pendant une semaine ; ni bain ni piscine pendant 15 jours\n- Arrêt de travail de 10 à 40 jours selon la pénibilité du métier\n- Marcher tous les jours, même en cas de gêne"),
        ],
        "faq": [("Quelles précautions après une cure de hernie inguinale ?", "Pas de sport ni de charges de plus de 15 kg pendant un mois, pas de conduite pendant une semaine, ni bain ni piscine pendant 15 jours. L'arrêt de travail va de 10 à 40 jours selon la pénibilité du métier. Il faut se forcer à marcher tous les jours, même en cas de gêne.")],
        "videos": ["hernie-inguinale-tep"],
        "pdf": "https://nemaudig.fr/_objects/tao_medias/file/fiche-hernie-20.pdf",
    },
    {
        "slug": "hernie-ombilicale", "ancien": "hernie-ombilicale", "famille": "paroi-abdominale", "organe": "ombilic",
        "titre": "Hernie ombilicale", "court": "Hernie ombilicale",
        "resume": "Un gonflement du nombril ou juste au-dessus, accentué debout et à l'effort.",
        "desc": "Hernie ombilicale : risque d'étranglement, réparation par couture ou prothèse, par incision ou cœlioscopie, et consignes après l'opération. Nîmes.",
        "sections": [
            ("La maladie", "Le gonflement correspond à un relâchement de l'orifice ombilical, à travers lequel passe une partie du contenu de l'abdomen. Il augmente progressivement, avec un risque d'incarcération de l'intestin : l'urgence de l'étranglement herniaire."),
            ("L'intervention", "Renforcement de la paroi par couture ou par un voile synthétique (plaque, prothèse, filet), par une incision unique près de l'ombilic ou par cœlioscopie (mini-incision sur le côté de l'abdomen)."),
            ("Les risques", "- Sérome : bosse de liquide clair à la place de la hernie\n- Ecchymose : placard bleu diffusant dans les tissus de l'abdomen\n- Infection de la prothèse"),
            ("Après l'opération", "Pas d'effort physique important pendant quatre semaines (port de charges de plus de 5 kg)."),
        ],
        "faq": [], "videos": [], "pdf": None,
    },
    {
        "slug": "eventration", "ancien": "eventration", "famille": "paroi-abdominale", "organe": "paroi",
        "titre": "Éventration", "court": "Éventration",
        "resume": "Un gonflement au niveau d'une ancienne cicatrice, accentué debout et à l'effort.",
        "desc": "Éventration sur cicatrice : réparation de la paroi abdominale par incision, cœlioscopie ou technique mixte, risques et récidive. Chirurgiens digestifs à Nîmes.",
        "sections": [
            ("La maladie", "Il s'agit d'un relâchement de la suture musculaire d'une ancienne cicatrice, à travers lequel passe une partie du contenu de l'abdomen. Le volume augmente progressivement, avec un risque d'incarcération de l'intestin : l'urgence de l'étranglement."),
            ("L'intervention", "Renforcement de la paroi par couture ou par un voile synthétique (plaque, prothèse, filet), par une incision reprenant l'ancienne cicatrice, par cœlioscopie (mini-incision sur le côté de l'abdomen), ou par une technique mixant les deux abords."),
            ("Les risques", "- Sérome : bosse de liquide clair à la place de l'éventration\n- Ecchymose diffusant dans les tissus de l'abdomen\n- Douleurs chroniques, surtout latérales\n- Infection de la prothèse"),
            ("Après l'opération", "- Pas d'effort physique important pendant six semaines (port de charges de plus de 5 kg), sous peine d'un fort risque de récidive\n- La stabilisation du poids est primordiale"),
        ],
        "faq": [], "videos": [], "pdf": None,
    },
    # ───────────────────────── Glandes surrénales ─────────────────────────
    {
        "slug": "surrenales", "ancien": "pathologies-surrenaliennes", "famille": "endocrinien", "organe": "surrenales",
        "titre": "Chirurgie des glandes surrénales", "court": "Surrénales",
        "resume": "La chirurgie endocrinienne fait partie des spécialités du Dr Fanelly Torres.",
        "desc": "Chirurgie des glandes surrénales à Nîmes : surrénalectomie assistée par robot, chirurgie endocrinienne au sein de l'équipe Nemaudig. Vidéo d'intervention.",
        "sections": [
            ("Au cabinet", "La chirurgie endocrinienne — thyroïde et glandes surrénales — fait partie des spécialités déclarées du Dr Fanelly Torres, titulaire d'un DIU de chirurgie endocrinienne et métabolique, comme le Dr Emmanuel Prieur.\n\nLe cabinet a publié la vidéo d'une surrénalectomie droite réalisée avec l'aide du robot chirurgical."),
        ],
        "faq": [], "videos": ["surrenalectomie-robot"], "pdf": None, "a_completer": True,
    },
    # ───────────────────────── Peau et dispositifs ─────────────────────────
    {
        "slug": "kystes-et-lipomes", "ancien": "kystes-lipomes", "famille": "pathologie-generale", "organe": "peau",
        "titre": "Kystes et lipomes", "court": "Kystes, lipomes",
        "resume": "Des tumeurs bénignes de la peau très fréquentes, retirées le plus souvent sous anesthésie locale.",
        "desc": "Ablation de kyste sébacé et de lipome à Nîmes, le plus souvent sous anesthésie locale, le lundi matin à la Polyclinique Grand Sud, même sans courrier.",
        "sections": [
            ("Comprendre", "Il existe de nombreuses tumeurs bénignes de la peau ; le kyste sébacé et le lipome sont très fréquents. Le kyste peut s'infecter et devenir douloureux, le lipome peut grossir."),
            ("L'intervention", "Elle retire la totalité de la lésion pour éviter la récidive. La cicatrisation peut être longue et nécessiter des soins locaux. Les lésions sont systématiquement analysées pour confirmer leur nature bénigne.\n\nLa chirurgie est, dans la majorité des cas, possible sous anesthésie locale."),
            ("Soins sous anesthésie locale", "Les Drs Amielh et Alline réalisent tous les lundis matin des actes sous anesthésie locale aux soins externes de la Polyclinique Grand Sud : ablation de lipome, de naevus, de kyste…\n\nMême sans adressage par un dermatologue, avec une prise en charge sur devis. Rendez-vous au 04 66 05 24 63."),
        ],
        "faq": [("Faut-il systématiquement retirer un kyste ?", "Non. Le retrait est proposé si la lésion est symptomatique (douleurs, infection) ou en cas de doute sur sa nature.")],
        "videos": [], "pdf": None,
    },
    {
        "slug": "port-a-cath", "ancien": "port-a-cath", "famille": "pathologie-generale", "organe": "thorax",
        "titre": "Pose de chambre implantable (port-à-cath)", "court": "Port-à-cath",
        "resume": "Un boîtier placé sous la peau, relié à un cathéter introduit dans une grosse veine.",
        "desc": "Pose de port-à-cath (chambre implantable) au bloc opératoire à Nîmes : utilité, complications possibles et vie quotidienne avec le dispositif.",
        "sections": [
            ("Le dispositif", "La chambre implantable est un boîtier placé sous la peau, relié à un cathéter introduit dans une grosse veine. Elle permet d'administrer facilement des produits par voie intraveineuse et de faire des prises de sang.\n\nElle est mise en place lors d'une opération, au bloc opératoire."),
            ("Les complications possibles", "- Hématome postopératoire, surtout chez les patients sous anticoagulants\n- Infection du boîtier, qui nécessite son retrait"),
        ],
        "faq": [("Puis-je me doucher avec le port-à-cath ?", "Oui, l'ensemble du dispositif est sous la peau.")],
        "videos": [], "pdf": None,
    },
]

PAR_SLUG = {p["slug"]: p for p in PATHOLOGIES}


def par_famille(slug):
    return [p for p in PATHOLOGIES if p["famille"] == slug]
