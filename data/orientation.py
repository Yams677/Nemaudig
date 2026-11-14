"""Entrée « Que ressentez-vous ? » — chaque signe reprend une description présente
sur nemaudig.fr (fiches pathologies). Ce n'est pas un outil de diagnostic : il oriente
vers les fiches et vers une consultation."""

SIGNES = [
    ("aine", "Une grosseur à l'aine, plus visible debout ou à l'effort", ["hernie-inguinale"]),
    ("nombril", "Un gonflement au nombril ou juste au-dessus", ["hernie-ombilicale"]),
    ("cicatrice", "Un gonflement sur une ancienne cicatrice", ["eventration"]),
    ("reflux", "Des remontées acides ou biliaires", ["rgo", "hernie-hiatale"]),
    ("colique", "Une douleur au niveau de l'estomac, parfois vers le dos ou l'épaule droite", ["vesicule-biliaire", "cholecystectomie"]),
    ("sang", "Du sang dans les selles", ["hemorroides", "cancer-du-colon", "cancer-du-rectum", "mici"]),
    ("selles", "Une douleur anale au passage des selles", ["fissure-anale"]),
    ("abces", "Une douleur intense et une grosseur près de l'anus", ["abces-et-fistule-anale"]),
    ("pilonidal", "Une inflammation ou un écoulement dans le sillon interfessier", ["kyste-pilonidal"]),
    ("peau", "Une boule sous la peau : kyste, lipome", ["kystes-et-lipomes"]),
    ("alimentation", "Des aliments qui passent de plus en plus mal", ["cancer-de-l-oesophage", "cancer-de-l-estomac"]),
]
