# Les fichiers que lit la page J20 : leur copie sur le SSP Cloud, et en
# commentaire leur adresse officielle.
SOURCES = {
    # https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-ips-ecoles-ap2022/exports/parquet?where=rentree_scolaire+%3D+%272024-2025%27
    "ips": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/ips.parquet",
    # https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-ecoles-effectifs-nb_classes/exports/parquet?where=rentree_scolaire+%3D+date%272024-01-01%27
    "effectifs": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/effectifs.parquet",
    # https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-annuaire-education/exports/parquet?select=identifiant_de_l_etablissement%2C+nom_commune%2C+libelle_region%2C+longitude%2C+latitude&where=type_etablissement+%3D+%27Ecole%27
    "annuaire": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/annuaire.parquet",
}
