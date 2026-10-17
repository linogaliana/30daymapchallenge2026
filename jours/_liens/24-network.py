# Les fichiers que lit la page J24 : leur copie sur le SSP Cloud, et en
# commentaire leur adresse officielle.
SOURCES = {
    # https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/lignes-par-statut/exports/parquet
    "lignes-par-statut": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/lignes-par-statut.parquet",
    # https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/frequentation-gares/exports/parquet
    "frequentation-gares": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/frequentation-gares.parquet",
    # https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/gares-de-voyageurs/exports/parquet
    "gares-de-voyageurs": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/gares-de-voyageurs.parquet",
    # https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/liste-des-gares/exports/parquet
    "liste-des-gares": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/liste-des-gares.parquet",
}
