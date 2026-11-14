"""
Identité et coordonnées du cabinet — SEUL fichier à modifier pour les
informations NAP (Name / Address / Phone).

Toutes les valeurs proviennent du site actuel nemaudig.fr (mêmes données que
les maquettes A et B). Rien n'est inventé.

DEMO = True : maquette de démonstration — noindex partout, robots.txt fermé,
étiquette « Maquette » visible, liens tel: neutralisés (un message s'affiche).

BASE : préfixe des adresses. "" en local ou sur un domaine ; "/Nemaudig" pour
une publication GitHub Pages dans un sous-dossier (voir README).
"""
import os

DEMO = True
BASE = os.environ.get("NEMAUDIG_BASE", "").rstrip("/")

SITE_URL = "https://nemaudig.fr"

CABINET = {
    "nom": "Nemaudig",
    "nom_long": "Nemaudig — chirurgie digestive et viscérale à Nîmes",
    "statut": "Association libérale de chirurgiens digestifs et viscéraux",
    "telephone_affiche": "04 66 05 24 63",
    "telephone_e164": "+33466052463",
    "email": "contact@nemaudig.fr",
    "adresse": {
        "rue": "480 avenue Saint-André de Codols",
        "complement": "Immeuble l'Odyssée, 2e étage",
        "code_postal": "30900",
        "ville": "Nîmes",
    },
    # Coordonnées approximatives du secteur Polyclinique Grand Sud — À VALIDER sur place.
    "geo": {"lat": 43.8160, "lng": 4.3420},
    "horaires_affiches": "Du lundi au vendredi, 8 h – 18 h 30",
    # Lien générique : les liens directs par chirurgien sont à obtenir du cabinet.
    "rdv_en_ligne": "https://www.maiia.com/",
    "rdv_en_ligne_libelle": "Maiia",
    "urgences_nom": "Urgences de la Polyclinique du Grand Sud",
    "urgences_tel": "04 66 04 31 46",
}

MENTIONS = {
    "raison_sociale": "NEMAUDIG",
    "siren": "538 760 984",
    "directeur_publication": "Dr David Amielh",
    "hebergeur": "À préciser au moment de la mise en ligne",
}

# Attribution obligatoire des modèles 3D (licence CC BY 4.0).
CREDIT_IMAGES = "Images d'organes : illustrations générées par intelligence artificielle, à valider par l'équipe"
