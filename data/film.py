"""Scénario du film « Le parcours digestif » — partagé par tools_film.py (tournage)
et pages/accueil.py (chapitres du lecteur). Textes repris de data/voyage.py."""

from data.voyage import ETAPES

PAROI = {"cle": "paroi", "organes": ["aine", "ombilic"], "camera": (0.9, -0.45, 4.6), "nom": "Paroi abdominale",
         "titre": "Hernies et éventrations", "liens": [("Hernie inguinale", ""), ("Hernie ombilicale", ""), ("Éventration", "")]}

# Page du site vers laquelle renvoie chaque chapitre.
FICHES = {"oesophage": "/pathologies/oesophage-estomac/", "estomac": "/pathologies/oesophage-estomac/",
          "foie": "/pathologies/foie-vesicule-pancreas/", "pancreas": "/pathologies/cancer-du-pancreas/",
          "intestin": "/pathologies/mici/", "colon": "/pathologies/colon-rectum/", "rectum": "/pathologies/proctologie/",
          "paroi": "/pathologies/paroi-abdominale/"}

ARRETS_COURTS = ("estomac", "foie", "colon", "paroi")


def etapes_film(court=False):
    corps = [e for e in ETAPES if e["organes"]] + [PAROI]
    if court:
        corps = [e for e in corps if e["cle"] in ARRETS_COURTS]
    intro = {"cle": "intro", "organes": [], "camera": None, "nom": "Ouverture", "surtitre": "Nemaudig · Nîmes",
             "titre": "Au cœur de l'appareil digestif", "sous": "Chirurgie digestive et viscérale"}
    fin = {"cle": "fin", "organes": [], "camera": None, "nom": "L'équipe", "surtitre": "Nemaudig",
           "titre": "Cinq chirurgiens, une seule équipe.", "sous": "Chirurgie digestive et viscérale à Nîmes · 04 66 05 24 63"}
    liste = [intro]
    for i, e in enumerate(corps, 1):
        liste.append({"cle": e["cle"], "organes": e["organes"], "camera": e["camera"], "ecarter": e.get("ecarter", []),
                      "nom": e["nom"], "surtitre": f"{i:02d} — {e['nom']}", "titre": e["titre"],
                      "sous": " · ".join(l for l, _ in e["liens"])})
    return liste + [fin]


def calendrier(nb, court=False):
    """Segments (début, fin, f_départ, f_arrivée, index_titre) : transitions puis arrêts. Renvoie aussi la durée."""
    intro, trans, arret, final = (4.0, 1.8, 3.4, 5.0) if court else (5.0, 2.2, 4.3, 6.0)
    segs, t = [(0, intro, 0, 0, 0)], intro
    for i in range(1, nb):
        segs.append((t, t + trans, i - 1, i, None))
        t += trans
        duree = final if i == nb - 1 else arret
        segs.append((t, t + duree, i, i, i))
        t += duree
    return segs, t


def chapitres(court=False):
    """[(seconde de début, libellé, lien vers la fiche)] pour les arrêts sur organe."""
    etapes = etapes_film(court)
    segs, _ = calendrier(len(etapes), court)
    return [(round(a, 1), etapes[i]["nom"], FICHES.get(etapes[i]["cle"]))
            for a, b, f0, f1, i in segs if i is not None and FICHES.get(etapes[i]["cle"])]
