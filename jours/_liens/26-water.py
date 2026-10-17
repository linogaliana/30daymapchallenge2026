# Les fichiers que lit la page J26 : leur copie sur le SSP Cloud, et en
# commentaire leur adresse officielle.
SOURCES = {
    # https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/impots-locaux-fichier-de-recensement-des-elements-dimposition-a-la-fiscalite-dir/attachments/rei_2025_fichier_notice_tracezip
    "rei": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/rei.zip",
    # https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/fiscalite-locale-des-particuliers/exports/csv?select=exercice%2Cinsee_com%2Cb52ggemapi%2Ce52ggemapi%2Ch52ggemapi&delimiter=%3B
    "historique": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/historique.csv",
}
