"""Stations du voyage intérieur et fiches « organe en 3D ».

RÈGLE : chaque phrase reprend une information présente sur nemaudig.fr (même
source que nemaudig/data/voyage.py du site A). Aucun chiffre extérieur ajouté.

`u` : position de la station le long du tube (0 = haut de l'œsophage, 1 = anus).
`modeles` : fichiers GLB (BodyParts3D) montrés dans la visionneuse.
`pathologies` : slugs de data/pathologies.py.
`riche` : arrêt complet (organe réel en vue éclatée + animation par pathologie) ;
sinon arrêt simple (fiche + pathologies + chirurgien).
`arrets` : pathologies présentées pendant l'arrêt. `texte` = phrases des fiches du site ;
`chirurgien` = slug déduit des spécialités affichées sur le site (None = toute l'équipe) —
attributions PROPOSÉES, à faire valider par l'équipe ; `anim` = animation schématique.
"""

STATIONS = [
    {
        "cle": "oesophage", "u": 0.06, "nom": "Œsophage", "modeles": ["oesophage"],
        "titre": "Le passage entre deux mondes",
        "texte": "L'œsophage est le « tube » qui relie la bouche à l'estomac. Il traverse le thorax, puis franchit l'orifice hiatal pour rejoindre l'abdomen.",
        "faits": ["Contre le reflux, une valve façonnée avec le haut de l'estomac vient « cravater » l'œsophage",
                  "Une ablation de l'œsophage associe une cicatrice sur le thorax et de petites incisions sur l'abdomen"],
        "pathologies": ["rgo", "hernie-hiatale", "cancer-de-l-oesophage"],
    },
    {
        "cle": "estomac", "u": 0.21, "nom": "Estomac", "modeles": ["estomac"],
        "titre": "La poche qui commande l'appétit",
        "texte": "L'estomac est la poche située entre l'œsophage et le duodénum. Une partie de sa paroi contient les cellules qui sécrètent la ghréline, l'hormone qui stimule l'appétit.",
        "faits": ["La sleeve retire environ les deux tiers de l'estomac, dont cette zone",
                  "Le bypass le réduit à une petite poche d'environ 15 à 75 cc"],
        "pathologies": ["cancer-de-l-estomac"],
        "extra": [("Chirurgie de l'obésité", "obesite")],
    },
    {
        "cle": "foie", "u": 0.355, "nom": "Foie & vésicule", "modeles": ["foie", "vesicule"],
        "titre": "Un organe indispensable à la vie",
        "texte": "Situé sous les côtes à droite, le foie nettoie et épure le sang, fabrique des protéines et stocke des molécules. Il fabrique aussi la bile, que la vésicule stocke pour l'évacuer en grande quantité au moment des repas.",
        "faits": ["Chaque moitié du foie est alimentée par une artère, une veine et un canal biliaire",
                  "Il repousse après l'ablation d'une partie, en plusieurs semaines"],
        "pathologies": ["foie", "vesicule-biliaire", "cholecystectomie"],
    },
    {
        "cle": "pancreas", "u": 0.425, "nom": "Pancréas", "modeles": ["pancreas", "duodenum"],
        "titre": "L'organe caché",
        "texte": "Profond, situé en arrière de l'estomac, le pancréas est encastré dans le duodénum ; le canal de la bile traverse sa tête. Il fabrique des enzymes de la digestion et l'insuline, qui régule le sucre dans le sang.",
        "faits": ["Après l'ablation de sa tête, trois coutures sont nécessaires : canal pancréatique, canal biliaire et tube digestif"],
        "pathologies": ["cancer-du-pancreas"],
    },
    {
        "cle": "intestin", "u": 0.55, "nom": "Intestin grêle", "modeles": ["intestin"],
        "titre": "Là où l'on absorbe",
        "texte": "Après le duodénum vient l'intestin grêle, le « petit intestin » : d'abord le jéjunum, puis l'iléon. C'est dans l'intestin que les nutriments sont réellement absorbés.",
        "faits": ["La maladie de Crohn peut toucher tout l'intestin grêle",
                  "Le bypass envoie les aliments directement dans sa partie moyenne"],
        "pathologies": ["mici"],
    },
    {
        "cle": "colon", "u": 0.74, "nom": "Côlon", "modeles": ["colon"],
        "titre": "Le cadre du gros intestin",
        "texte": "Le côlon fait suite à l'intestin grêle et encadre l'abdomen : côlon droit qui monte, côlon transverse qui traverse, côlon gauche qui redescend, puis le sigmoïde avant le rectum.",
        "faits": ["Les diverticules siègent le plus souvent dans le sigmoïde, et c'est là qu'ils se compliquent",
                  "Le plus souvent, on l'opère par cœlioscopie : 4 à 5 petites cicatrices"],
        "pathologies": ["diverticules-du-sigmoide", "cancer-du-colon", "chirurgie-colique"],
    },
    {
        "cle": "rectum", "u": 0.92, "nom": "Rectum", "modeles": ["rectum"],
        "titre": "Un carrefour de précision",
        "texte": "Le rectum, d'environ 15 cm, sert de réservoir. Il se termine par le canal anal, long de 2 à 3 cm, fermé par le sphincter qui assure la continence.",
        "faits": ["Il est au contact de la vessie, de la prostate ou de l'utérus, des uretères et des vaisseaux du bassin",
                  "Les nerfs sexuels cheminent autour : chaque geste compte"],
        "pathologies": ["cancer-du-rectum", "chirurgie-rectale", "hemorroides"],
    },
]

# Modèles BodyParts3D (identifiants FMA, arbre « part-of ») → fichiers de src/models/.
MODELES = {
    "oesophage": ("Œsophage", "FMA7131"),
    "estomac": ("Estomac", "FMA7148"),
    "foie": ("Foie", "FMA7197"),
    "vesicule": ("Vésicule biliaire", "FMA7202"),
    "pancreas": ("Pancréas", "FMA7198"),
    "duodenum": ("Duodénum", "FMA7206"),
    "intestin": ("Intestin grêle", "FMA7200"),
    "colon": ("Côlon", "FMA14545+FMA14546+FMA14547+SIGMOIDE"),
    "rectum": ("Rectum", "FMA14544"),
}


# Spécialité affichée sur le site qui justifie l'attribution proposée.
SPECIALITE_ARRET = {
    "dr-david-amielh": "Chirurgie œsophagienne",
    "dr-emmanuel-prieur": "Chirurgie hépatique",
    "dr-sylvain-laporte": "Chirurgie colorectale",
    "dr-mathias-alline": "Proctologie",
    "dr-fanelly-torres": "Chirurgie de l'obésité",
}

ARRETS = {
    "oesophage": {"riche": True, "pathos": [
        {"slug": "rgo", "anim": "reflux", "chirurgien": "dr-david-amielh",
         "texte": "Des remontées acides ou biliaires de l'estomac vers l'œsophage. Elles exposent au risque d'une brûlure progressive de l'œsophage (œsophagite)."},
        {"slug": "hernie-hiatale", "anim": "hernie", "chirurgien": "dr-david-amielh",
         "texte": "La partie haute de l'estomac remonte dans le thorax. Le chirurgien la réintègre dans l'abdomen et referme l'orifice entre l'abdomen et le thorax."},
        {"slug": "cancer-de-l-oesophage", "anim": "zone-oeso", "chirurgien": "dr-david-amielh",
         "texte": "Une tumeur qui se crée dans la paroi de l'œsophage et grossit progressivement jusqu'à empêcher l'alimentation."},
    ]},
    "estomac": {"riche": False, "pathos": [
        {"slug": "cancer-de-l-estomac", "chirurgien": None,
         "texte": "Une tumeur qui se crée dans la paroi de l'estomac et grossit progressivement jusqu'à empêcher l'alimentation."},
        {"titre": "Chirurgie de l'obésité", "chirurgien": "dr-fanelly-torres",
         "texte": "La sleeve gastrectomie retire environ les deux tiers de l'estomac, qui devient un tube vertical."},
    ]},
    "foie": {"riche": True, "pathos": [
        {"slug": "foie", "anim": "hepatectomie", "chirurgien": "dr-emmanuel-prieur",
         "texte": "Le plus souvent pour retirer des cancers, primitifs du foie ou métastases d'autres cancers. Le foie repousse après l'ablation d'une partie, en plusieurs semaines."},
        {"slug": "vesicule-biliaire", "anim": "calculs", "chirurgien": None,
         "texte": "La bile peut sédimenter dans la vésicule et former des calculs, qui peuvent occasionner des complications."},
        {"slug": "cholecystectomie", "anim": "ablation-vesicule", "chirurgien": None,
         "texte": "L'ablation de la vésicule, seul traitement des calculs compliqués. La plupart du temps sous cœlioscopie, sans grande cicatrice."},
    ]},
    "pancreas": {"riche": False, "pathos": [
        {"slug": "cancer-du-pancreas", "chirurgien": None,
         "texte": "Située dans la tête du pancréas, la tumeur peut comprimer le canal de la bile et provoquer une jaunisse (ictère)."},
    ]},
    "intestin": {"riche": False, "pathos": [
        {"slug": "mici", "chirurgien": None,
         "texte": "La maladie de Crohn peut toucher tout l'intestin grêle, le côlon et le rectum, jusqu'à l'anus."},
        {"titre": "Bypass gastrique", "chirurgien": "dr-fanelly-torres",
         "texte": "Une petite poche gastrique et un court-circuit de l'intestin : moins d'aliments, et moins absorbés."},
    ]},
    "colon": {"riche": True, "pathos": [
        {"slug": "diverticules-du-sigmoide", "anim": "diverticules", "chirurgien": "dr-sylvain-laporte",
         "texte": "De fragiles petites poches à l'extérieur du côlon, le plus souvent sur sa partie terminale, le sigmoïde. Elles peuvent s'enflammer : c'est la diverticulite."},
        {"slug": "cancer-du-colon", "anim": "zone-colon", "chirurgien": "dr-sylvain-laporte",
         "texte": "Une tumeur qui se développe dans la paroi du gros intestin. La chirurgie retire le segment atteint et les ganglions voisins, puis raccorde les deux extrémités."},
        {"slug": "chirurgie-colique", "anim": "colectomie", "chirurgien": "dr-sylvain-laporte",
         "texte": "Retirer la zone malade, plus ou moins étendue, puis rétablir le circuit intestinal par une couture entre les deux extrémités : l'anastomose."},
    ]},
    "rectum": {"riche": False, "pathos": [
        {"slug": "cancer-du-rectum", "chirurgien": "dr-sylvain-laporte",
         "texte": "Une tumeur de la partie terminale du tube digestif, entre le côlon et l'anus."},
        {"slug": "hemorroides", "chirurgien": "dr-mathias-alline",
         "texte": "Des vaisseaux présents chez tous, qui participent à la continence ; ils deviennent une maladie lorsqu'ils sont gênants."},
    ]},
}
