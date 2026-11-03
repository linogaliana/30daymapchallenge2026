# Les fichiers que lit la page J14 : leur copie sur le SSP Cloud, et en
# commentaire leur adresse officielle.
SOURCES = {
    # https://www.insee.fr/fr/statistiques/fichier/8217525/BPE25.parquet
    "bpe": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/BPE25.parquet",
    # https://static.data.gouv.fr/resources/base-des-lieux-et-equipements-culturels-basilic/20260218-084338/base-des-lieux-et-des-equipements-culturels.csv
    "basilic": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/base-des-lieux-et-des-equipements-culturels.csv",
    # https://www.data.gouv.fr/fr/datasets/r/29406189-15e9-4f2f-9e9d-d18649762198
    "musees": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/liste",
    # https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/gares-de-voyageurs/exports/parquet
    "gares-de-voyageurs": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/gares-de-voyageurs.parquet",
    # https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-annuaire-education/exports/parquet?select=identifiant_de_l_etablissement%2C+nom_commune%2C+libelle_region%2C+longitude%2C+latitude&where=type_etablissement+%3D+%27Ecole%27
    "annuaire": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/annuaire.parquet",
    # https://equipements.sports.gouv.fr/api/explore/v2.1/catalog/datasets/data-es/exports/parquet
    "data_es": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/data_es.parquet",
}
