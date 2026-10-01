"""« Voyage au cœur de l'appareil digestif » — section 3D de l'accueil.

RÈGLE : chaque phrase reprend une information présente sur nemaudig.fr
(fiches MICI, cancers, foie, vésicule, pancréas, chirurgie rectale, sleeve,
bypass, hernie hiatale). Aucun chiffre extérieur n'est ajouté.
`organes` : clés de lib/anatomie.py mises en lumière ; `camera` : décalage
de la caméra par rapport au centre des organes (x, y, z) ; `ecarter` : organes
poussés de côté pour dégager la vue.
"""

ETAPES = [
    {
        "cle": "intro", "organes": [], "camera": None, "nom": "L'appareil digestif",
        "titre": "Un voyage de la bouche à l'anus",
        "texte": "Lorsque l'on mange, les aliments descendent dans l'œsophage, arrivent dans l'estomac, puis traversent le duodénum, l'intestin grêle, le côlon et enfin le rectum. Tous ces organes sont pris en charge par l'équipe.",
        "faits": [], "liens": [],
    },
    {
        "cle": "oesophage", "organes": ["oesophage"], "camera": (1.3, 0.3, 4.4), "nom": "Œsophage",
        "titre": "Le passage entre deux mondes",
        "texte": "L'œsophage est le « tube » qui relie la bouche à l'estomac. Il traverse le thorax, puis franchit l'orifice hiatal pour rejoindre l'abdomen.",
        "faits": ["Une ablation de l'œsophage associe une cicatrice sur le thorax et de petites incisions sur l'abdomen",
                  "Contre le reflux, une valve façonnée avec le haut de l'estomac vient « cravater » l'œsophage"],
        "liens": [("Reflux (RGO)", "/pathologies/rgo/"), ("Hernie hiatale", "/pathologies/hernie-hiatale/"), ("Cancer de l'œsophage", "/pathologies/cancer-de-l-oesophage/")],
    },
    {
        "cle": "estomac", "organes": ["estomac"], "camera": (1.5, 0.4, 4.4), "nom": "Estomac",
        "titre": "La poche qui commande l'appétit",
        "texte": "L'estomac est la poche située entre l'œsophage et le duodénum. Une partie de sa paroi contient les cellules qui sécrètent la ghréline, l'hormone qui stimule l'appétit.",
        "faits": ["La sleeve retire environ les deux tiers de l'estomac, dont cette zone",
                  "Le bypass le réduit à une petite poche d'environ 15 à 75 cc"],
        "liens": [("Cancer de l'estomac", "/pathologies/cancer-de-l-estomac/"), ("Chirurgie de l'obésité", "/obesite/")],
    },
    {
        "cle": "foie", "organes": ["foie", "vesicule"], "camera": (-1.5, 0.5, 4.8), "nom": "Foie et vésicule",
        "titre": "Un organe indispensable à la vie",
        "texte": "Situé sous les côtes à droite, le foie nettoie et épure le sang, fabrique des protéines et stocke des molécules. Il fabrique aussi la bile, que la vésicule stocke pour l'évacuer en grande quantité au moment des repas.",
        "faits": ["Chaque moitié du foie est alimentée par une artère, une veine et un canal biliaire",
                  "Une éponge pleine de vaisseaux : le saignement est le principal risque de sa chirurgie",
                  "Il repousse après l'ablation d'une partie, en plusieurs semaines"],
        "liens": [("Chirurgie du foie", "/pathologies/foie/"), ("Calculs de la vésicule", "/pathologies/vesicule-biliaire/")],
    },
    {
        "cle": "pancreas", "organes": ["pancreas"], "camera": (0.7, -0.1, 4.2), "ecarter": ["estomac", "foie", "vesicule"], "nom": "Pancréas",
        "titre": "L'organe caché",
        "texte": "Profond, situé en arrière de l'estomac, le pancréas est encastré dans le duodénum ; le canal de la bile traverse sa tête. Il fabrique des enzymes de la digestion et l'insuline, qui régule le sucre dans le sang.",
        "faits": ["Après l'ablation de sa tête, trois coutures sont nécessaires : canal pancréatique, canal biliaire et tube digestif",
                  "Lors de ces opérations, le pronostic vital est engagé"],
        "liens": [("Cancer du pancréas", "/pathologies/cancer-du-pancreas/")],
    },
    {
        "cle": "intestin", "organes": ["intestin"], "camera": (0.4, -0.3, 4.6), "nom": "Intestin grêle",
        "titre": "Là où l'on absorbe",
        "texte": "Après le duodénum vient l'intestin grêle, le « petit intestin » : d'abord le jéjunum, puis l'iléon. C'est dans l'intestin que les nutriments sont réellement absorbés.",
        "faits": ["La maladie de Crohn peut toucher tout l'intestin grêle",
                  "Le bypass envoie les aliments directement dans sa partie moyenne"],
        "liens": [("MICI : Crohn, rectocolite", "/pathologies/mici/"), ("Bypass gastrique", "/obesite/bypass-gastrique/")],
    },
    {
        "cle": "colon", "organes": ["colon", "sigmoide"], "camera": (0.0, -0.1, 6.4), "nom": "Côlon",
        "titre": "Le cadre du gros intestin",
        "texte": "Le côlon fait suite à l'intestin grêle et encadre l'abdomen : côlon droit qui monte, côlon transverse qui traverse, côlon gauche qui redescend, puis le sigmoïde avant le rectum.",
        "faits": ["Les diverticules siègent le plus souvent dans le sigmoïde, et c'est là qu'ils se compliquent",
                  "Le plus souvent, on l'opère par cœlioscopie : 4 à 5 petites cicatrices"],
        "liens": [("Diverticulite", "/pathologies/diverticules-du-sigmoide/"), ("Cancer du côlon", "/pathologies/cancer-du-colon/"), ("Chirurgie colique", "/pathologies/chirurgie-colique/")],
    },
    {
        "cle": "rectum", "organes": ["rectum", "anus"], "camera": (1.1, -0.2, 4.0), "nom": "Rectum et anus",
        "titre": "Un carrefour de précision",
        "texte": "Le rectum, d'environ 15 cm, sert de réservoir. Il se termine par le canal anal, long de 2 à 3 cm, fermé par le sphincter qui assure la continence.",
        "faits": ["Il est au contact de la vessie, de la prostate ou de l'utérus, des uretères et des vaisseaux du bassin",
                  "Les nerfs sexuels cheminent autour : chaque geste compte"],
        "liens": [("Cancer du rectum", "/pathologies/cancer-du-rectum/"), ("Proctologie", "/pathologies/proctologie/")],
    },
    {
        "cle": "fin", "organes": [], "camera": None, "nom": "Notre équipe",
        "titre": "Cinq chirurgiens pour tout l'appareil digestif",
        "texte": "De l'œsophage à l'anus, chaque organe a ses spécificités. C'est pourquoi l'équipe discute ensemble les dossiers difficiles et opère à plusieurs les interventions lourdes.",
        "faits": [], "liens": [("Rencontrer les chirurgiens", "/chirurgiens/"), ("Prendre rendez-vous", "/contact/")],
    },
]
