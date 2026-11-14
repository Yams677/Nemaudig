"""Rapprochements entre données : familles, pathologies, chirurgiens, organes.

Ces rapprochements sont DÉDUITS des spécialités et des liens affichés sur nemaudig.fr :
ils orientent la navigation, ils ne constituent pas une affirmation médicale et restent
à confirmer par l'équipe.
"""
from data import obesite
from data.chirurgiens import CHIRURGIENS
from data.organes import ORGANE_DE_LA_PATHOLOGIE
from data.pathologies import FAMILLES, PATHOLOGIES

PATHOLOGIES_PAR_FAMILLE = {f["slug"]: [p for p in PATHOLOGIES if p["famille"] == f["slug"]] for f in FAMILLES}


def slugs_de_la_famille(famille):
    if famille == "obesite":
        return [t["slug"] for t in obesite.TECHNIQUES]
    return [p["slug"] for p in PATHOLOGIES_PAR_FAMILLE[famille]]


def chirurgiens_de_la_famille(famille):
    slugs = set(slugs_de_la_famille(famille))
    return [c for c in CHIRURGIENS if slugs & set(c["pathologies"])]


def chirurgiens_de_la_pathologie(slug):
    return [c for c in CHIRURGIENS if slug in c["pathologies"]]


def organe_de(pathologie):
    return ORGANE_DE_LA_PATHOLOGIE.get(pathologie["organe"])


def adresse_pathologie(slug):
    return f"/specialites/{slug}/"
