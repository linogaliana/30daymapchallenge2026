# Les fichiers que lit la page J10 : leur copie sur le SSP Cloud, et en
# commentaire leur adresse officielle.
SOURCES = {
    # https://www.insee.fr/fr/statistiques/fichier/2510634/epci_au_01-01-2026.zip
    "epci": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/epci_au_01-01-2026.zip",
    # https://static.data.gouv.fr/resources/bases-statistiques-communale-departementale-et-regionale-de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/20260709-120017/donnee-comm-data.gouv-parquet-2025-geographie2026-produit-le2026-06-25.parquet
    "ssmsi": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/donnee-comm-data.gouv-parquet-2025-geographie2026-produit-le2026-06-25.parquet",
    # https://data.drees.solidarites-sante.gouv.fr/api/v2/catalog/datasets/530_l-accessibilite-potentielle-localisee-apl/attachments/indicateur_d_apl_aux_medecins_generalistes_xlsx
    "apl": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/apl.xlsx",
    # https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-indice_eloignement_college_ap2022/exports/csv?delimiter=%3B&where=rentree_scolaire%3D%222025%22
    "colleges": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/colleges.csv",
    # https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-annuaire-education/exports/csv?delimiter=%3B&select=identifiant_de_l_etablissement%2Cnom_commune%2Clatitude%2Clongitude
    "annuaire_education": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/annuaire_education.csv",
    # https://data.enseignementsup-recherche.gouv.fr/api/explore/v2.1/catalog/datasets/fr-esr-atlas_regional-effectifs-d-etudiants-inscrits/exports/csv?delimiter=%3B&where=niveau_geographique%3D%27Unit%C3%A9+urbaine%27+AND+regroupement%3D%27TOTAL%27+AND+rentree+IN+%28%272015%27%2C+%272025%27%29
    "etudiants": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/etudiants.csv",
    # https://data.statistiques.developpement-durable.gouv.fr/dido/api/v1/datafiles/1a9ad5c2-0929-4687-8455-78aac6530a76/csv
    "rga": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/rga.csv",
    # https://agreste.agriculture.gouv.fr/agreste-web/download/publication/publie/RA2020_1013/RA2020_1013_SAU_Communes.zip
    "agreste": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/RA2020_1013_SAU_Communes.zip",
    # https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/fiscalite-locale-des-particuliers/exports/csv?delimiter=%3B&select=insee_com%2Ctaux_global_tfb&where=exercice%3D%222025%22
    "foncier": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/foncier.csv",
    # https://www.douane.gouv.fr/sites/default/files/2026-10/07/202608-Regional-2023-export.zip
    "douane": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/202608-Regional-2023-export.zip",
    # https://static.data.gouv.fr/resources/base-des-lieux-et-equipements-culturels-basilic/20260218-084338/base-des-lieux-et-des-equipements-culturels.csv
    "basilic": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/base-des-lieux-et-des-equipements-culturels.csv",
    # https://static.data.gouv.fr/resources/donnees-geocodees-issues-du-recensement-des-licences-et-clubs-aupres-des-federations-sportives-agreees-par-le-ministere-charge-des-sports/20251229-163249/clubs-data-2023.csv
    "clubs": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/clubs-data-2023.csv",
    # https://dares.travail-emploi.gouv.fr/sites/default/files/a4ef7ed6cced6fba8b492fec3933678c/R%C3%A9partition%20territoriale%20-%20part%20du%20m%C3%A9tier%20dans%20l%27emploi%20d%C3%A9partemental%20et%20r%C3%A9partition%20par%20d%C3%A9partement%20de%20l%27emploi%20du%20m%C3%A9tier.xlsx
    "dares": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/Repartition-territoriale---part-du-metier-dans-l-emploi-departemental-et-repartition-par-departement-de-l-emploi-du-metier.xlsx",
    # https://static.data.gouv.fr/resources/statistique-mensuelle-de-la-population-ecrouee-et-detenue-en-france/20261013-162028/statistique-etablissements-01092026.xlsx
    "detenus": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/statistique-etablissements-01092026.xlsx",
    # https://api-lannuaire.service-public.fr/api/explore/v2.1/catalog/datasets/api-lannuaire-administration/exports/json?select=nom%2Cpivot%2Cadresse&where=search%28%22centre_penitentiaire%22%29+OR+search%28%22maison_arret%22%29+OR+search%28%22centre_detention%22%29+OR+search%28%22maison_centrale%22%29
    "annuaire": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/annuaire.json",
    # http://www.dotations-dgcl.interieur.gouv.fr/consultation/criteres_repartition_csv.php?annee=2026&ct=com
    "dgf": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/dgf",
    # https://www.fonction-publique.gouv.fr/files/files/publications/vue-rapport-annuel/ra_2025-caracteristiques_postes.zip
    "dgafp": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/ra_2025-caracteristiques_postes.zip",
    # https://static.data.gouv.fr/resources/stock-et-flux-des-titres-de-sejour-en-france-sur-lannee-2024/20260821-131354/2024-sejour-flux-region-monde-nationalites.csv
    "dsed": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/2024-sejour-flux-region-monde-nationalites.csv",
    # https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/ne_110m_admin_0_countries.geojson
    "monde": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/ne_110m_admin_0_countries.geojson",
    # https://static.data.gouv.fr/resources/ecodef-statistiques-ndeg-255/20241212-133351/donnes-ecodef-255.xlsx
    "ecodef": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/donnes-ecodef-255.xlsx",
}
