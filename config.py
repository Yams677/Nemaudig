"""
Identité et coordonnées du cabinet — SEUL fichier à modifier pour les
informations NAP (Name / Address / Phone).

Toutes les valeurs ci-dessous proviennent du site actuel nemaudig.fr
(scraping Firecrawl, dossier ~/.firecrawl/nemaudig). Rien n'est inventé.

DEMO = True : maquette de démonstration — noindex partout, robots.txt fermé,
bandeau visible, liens tel: désactivés. Passer à False refuse la génération
tant qu'un élément marqué « À VALIDER » subsiste (voir build.py).
"""

DEMO = True

# Domaine actuel. Sert aux canonical, sitemap, Open Graph et redirections 301.
SITE_URL = "https://nemaudig.fr"

CABINET = {
    "nom": "Nemaudig",
    "nom_long": "Nemaudig — chirurgiens digestifs et viscéraux à Nîmes",
    "statut": "Association libérale de chirurgiens digestifs et viscéraux",
    "telephone_affiche": "04 66 05 24 63",
    "telephone_e164": "+33466052463",
    "email": "contact@nemaudig.fr",
    "adresse": {
        "rue": "480 avenue Saint-André de Codols",
        "complement": "Immeuble l'Odyssée, 2e étage",
        "code_postal": "30900",
        "ville": "Nîmes",
        "region": "Occitanie",
        "pays": "FR",
    },
    # Coordonnées approximatives du secteur Polyclinique Grand Sud — À VALIDER sur place.
    "geo": {"lat": 43.8160, "lng": 4.3420},
    "horaires": [(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "08:00", "18:30")],
    "horaires_affiches": "Du lundi au vendredi, 8 h – 18 h 30",
    "rdv_en_ligne": "https://www.maiia.com/",
    "rdv_en_ligne_libelle": "Maiia",
    "urgences_nom": "Urgences de la Polyclinique du Grand Sud",
    "urgences_tel": "04 66 04 31 46",
    "urgences_e164": "+33466043146",
}

MENTIONS = {
    "raison_sociale": "NEMAUDIG",
    "siren": "538 760 984",
    "directeur_publication": "Dr David Amielh",
    "hebergeur": "OVH SAS — 2 rue Kellermann, 59100 Roubaix — France",
}

# Communes citées pour le référencement local : uniquement des lieux où le
# cabinet est réellement présent (Nîmes : cabinet + 2 établissements ; Uzès :
# consultation du Dr Amielh au centre hospitalier).
ZONE = ["Nîmes", "Uzès", "Gard"]

# Chaque chirurgien doit avoir validé son portrait (ressemblance, droit à l'image)
# avant la mise en ligne : la production est refusée tant que False.
PORTRAITS_VALIDES = True

# Tout texte contenant l'un de ces motifs bloque la génération en production.
MARQUEURS_A_VALIDER = ["À VALIDER", "Portrait à venir", "maquette"]
