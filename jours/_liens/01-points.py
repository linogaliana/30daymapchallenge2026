# Les fichiers que lit la page J1 : leur copie sur le SSP Cloud, et en
# commentaire leur adresse officielle.
SOURCES = {
    # https://data.drees.solidarites-sante.gouv.fr/api/explore/v2.1/catalog/datasets/fichier_maternites_112021/attachments/fichier_maternites_122025_mad_xlsx
    "maternites": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/maternites.xlsx",
    # https://static.data.gouv.fr/resources/finess-extraction-du-fichier-des-etablissements/20260512-091152/etalab-cs1100507-stock-20260512-0339.csv
    "finess": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/etalab-cs1100507-stock-20260512-0339.csv",
    # https://static.data.gouv.fr/resources/finess-structures-1/20261001-021940/finess-structures-mensuel-202609.json.gz
    "finess_ans": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/finess-structures-mensuel-202609.json.gz",
}
