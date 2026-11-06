
import csv
from collections import Counter


# Chemins des fichiers CSV
FICHIER_SITES = "data/sites.csv"
FICHIER_MATERIEL = "data/materiel.csv"
FICHIER_ASSOCIATIONS = "data/associations.csv"
FICHIER_RESERVATIONS = "data/reservations.csv"


# Fonction pour lire les fichiers CSV
def lire_csv(chemin):
    with open(chemin, encoding="utf-8", newline="") as fichier:
        return list(csv.DictReader(fichier))


# Fonction pour compter les valeurs
def compter_par(lignes, colonne):
    return dict(Counter(ligne[colonne] for ligne in lignes))


# Fonction pour calculer les quantités par site
def total_par(lignes, colonne_groupe, colonne_valeur):
    totaux = {}

    for ligne in lignes:
        groupe = ligne[colonne_groupe]
        valeur = int(ligne[colonne_valeur])
        totaux[groupe] = totaux.get(groupe, 0) + valeur

    return totaux


# Classe Site
class Site:
    def __init__(self, code_site, nom, commune, annee_ouverture, surface_m2):
        self.code_site = code_site
        self.nom = nom
        self.commune = commune
        self.annee_ouverture = int(annee_ouverture)
        self.surface_m2 = int(surface_m2)

    def anciennete(self, annee_reference):
        return annee_reference - self.annee_ouverture

    def __str__(self):
        return f"{self.code_site} - {self.nom} ({self.commune}), {self.surface_m2} m2"


# Fonction pour identifier les réservations en cours
def reservations_en_cours(reservations):
    return [
        ligne for ligne in reservations
        if not ligne["date_retour_reelle"].strip()
    ]


# Fonction principale
def main():
    sites = lire_csv(FICHIER_SITES)
    materiels = lire_csv(FICHIER_MATERIEL)
    associations = lire_csv(FICHIER_ASSOCIATIONS)
    reservations = lire_csv(FICHIER_RESERVATIONS)

    print("=== NOMBRE DE LIGNES ===")
    print(f"Sites : {len(sites)}")
    print(f"Matériels : {len(materiels)}")
    print(f"Associations : {len(associations)}")
    print(f"Réservations : {len(reservations)}")

    print("\n=== SITES ET ANCIENNETÉ ===")
    for ligne in sites:
        site = Site(
            ligne["code_site"],
            ligne["nom"],
            ligne["commune"],
            ligne["annee_ouverture"],
            ligne["surface_m2"]
        )
        print(f"{site} - Ancienneté : {site.anciennete(2026)} ans")

    print("\n=== RÉSERVATIONS PAR SITE ===")
    nombres = compter_par(reservations, "code_site")
    for code, nombre in sorted(nombres.items(), key=lambda x: x[1], reverse=True):
        print(f"{code} : {nombre}")

    print("\n=== QUANTITÉS RÉSERVÉES PAR SITE ===")
    quantites = total_par(reservations, "code_site", "quantite")
    for code, quantite in sorted(quantites.items(), key=lambda x: x[1], reverse=True):
        print(f"{code} : {quantite}")

    print("\n=== MATÉRIELS PAR ÉTAT ===")
    etats = compter_par(materiels, "etat")
    for etat, nombre in etats.items():
        print(f"{etat} : {nombre}")

    print("\n=== CATÉGORIES DISTINCTES ===")
    categories = compter_par(materiels, "categorie")
    print(f"Nombre de catégories : {len(categories)}")

    print("\n=== RÉSERVATIONS EN COURS ===")
    en_cours = reservations_en_cours(reservations)
    print(f"Nombre de réservations en cours : {len(en_cours)}")


if __name__ == "__main__":
    main()
