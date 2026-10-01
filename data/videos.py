"""Vidéos YouTube publiées par le cabinet (pages /videos, /robotique et fiches).

`robot` : True seulement quand TOUTES les pages du site actuel le disent.
Deux vidéos sont présentées « robot » sur /robotique mais pas sur /videos
(hernie hiatale, colectomie angulaire gauche) : titre neutre en attendant
confirmation du cabinet.
"""

VIDEOS = {
    "robot-da-vinci": {"yt": "A9EcMqbDS6k", "titre": "Présentation du robot Da Vinci", "chirurgien": "dr-sylvain-laporte", "robot": True},
    "hernie-inguinale-tep": {"yt": "Y90RrXsyw7k", "titre": "Hernie inguinale par cœlioscopie (technique TEP)", "chirurgien": "dr-david-amielh", "robot": False},
    "crohn-robot": {"yt": "47wRXu6Y5tI", "titre": "Résection iléo-cæcale pour maladie de Crohn", "chirurgien": "dr-sylvain-laporte", "robot": True},
    "cardia-robot": {"yt": "X4SdnpcvcVU", "titre": "Résection d'une tumeur sous-muqueuse du cardia", "chirurgien": "dr-david-amielh", "robot": True},
    "hernie-hiatale-robot": {"yt": "IbW_o420v2o", "titre": "Cure de hernie hiatale", "chirurgien": "dr-david-amielh", "robot": False},
    "colectomie-angulaire-gauche": {"yt": "qrKsdT1hHIg", "titre": "Colectomie angulaire gauche", "chirurgien": "dr-david-amielh", "robot": False},
    "colectomie-droite-robot": {"yt": "n5tDFoFJnKg", "titre": "Colectomie droite", "chirurgien": None, "robot": True},
    "bypass-coelio": {"yt": "gmeHhoP8t6c", "titre": "Bypass gastrique par cœlioscopie", "chirurgien": "dr-fanelly-torres", "robot": False},
    "rectum-robot": {"yt": "nyDscTjMfB4", "titre": "Résection d'un cancer du rectum", "chirurgien": "dr-sylvain-laporte", "robot": True},
    "surrenalectomie-robot": {"yt": "kE_Z-rM9sAE", "titre": "Surrénalectomie droite", "chirurgien": None, "robot": True},
}

# Ordre d'affichage de la vidéothèque (celui de la page /videos, puis les vidéos
# présentes seulement sur les fiches).
ORDRE = ["robot-da-vinci", "hernie-inguinale-tep", "crohn-robot", "cardia-robot", "hernie-hiatale-robot",
         "colectomie-angulaire-gauche", "bypass-coelio", "rectum-robot", "colectomie-droite-robot",
         "surrenalectomie-robot"]
