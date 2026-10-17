# Les fichiers que lit la page J20, à leur adresse officielle.
import urllib.parse


def depp(jeu, **parametres):
    """L'export Parquet d'un jeu du portail de l'Éducation nationale, filtré (where) ou réduit à quelques colonnes (select)."""
    return (
        f"https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/{jeu}/exports/parquet?"
        + urllib.parse.urlencode(parametres)
    )


SOURCES = {
    "ips": depp("fr-en-ips-ecoles-ap2022", where="rentree_scolaire = '2024-2025'"),
    "effectifs": depp("fr-en-ecoles-effectifs-nb_classes", where="rentree_scolaire = date'2024-01-01'"),
    "annuaire": depp("fr-en-annuaire-education",
                     select="identifiant_de_l_etablissement, nom_commune, libelle_region, longitude, latitude",
                     where="type_etablissement = 'Ecole'"),
}
