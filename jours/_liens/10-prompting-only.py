# Les fichiers que lit la page J10, à leur adresse officielle.
import urllib.parse


def export_ods(domaine, jeu, **parametres):
    """L'export CSV d'un jeu d'un portail Opendatasoft, filtré (where) ou réduit à quelques colonnes (select)."""
    requete = urllib.parse.urlencode({"delimiter": ";", **parametres})
    return f"https://{domaine}/api/explore/v2.1/catalog/datasets/{jeu}/exports/csv?{requete}"


SOURCES = {
    "epci": "https://www.insee.fr/fr/statistiques/fichier/2510634/epci_au_01-01-2026.zip",
    "ssmsi": (
        "https://static.data.gouv.fr/resources/bases-statistiques-communale-departementale-et-regionale-"
        "de-la-delinquance-enregistree-par-la-police-et-la-gendarmerie-nationales/20260709-120017/"
        "donnee-comm-data.gouv-parquet-2025-geographie2026-produit-le2026-06-25.parquet"
    ),
    "apl": (
        "https://data.drees.solidarites-sante.gouv.fr/api/v2/catalog/datasets/"
        "530_l-accessibilite-potentielle-localisee-apl/attachments/indicateur_d_apl_aux_medecins_generalistes_xlsx"
    ),
    "colleges": export_ods("data.education.gouv.fr", "fr-en-indice_eloignement_college_ap2022",
                           where='rentree_scolaire="2025"'),
    "annuaire_education": export_ods("data.education.gouv.fr", "fr-en-annuaire-education",
                                     select="identifiant_de_l_etablissement,nom_commune,latitude,longitude"),
    "etudiants": export_ods("data.enseignementsup-recherche.gouv.fr", "fr-esr-atlas_regional-effectifs-d-etudiants-inscrits",
                            where="niveau_geographique='Unité urbaine' AND regroupement='TOTAL' AND rentree IN ('2015', '2025')"),
    "rga": "https://data.statistiques.developpement-durable.gouv.fr/dido/api/v1/datafiles/1a9ad5c2-0929-4687-8455-78aac6530a76/csv",
    "agreste": (
        "https://agreste.agriculture.gouv.fr/agreste-web/download/publication/publie/"
        "RA2020_1013/RA2020_1013_SAU_Communes.zip"
    ),
    "foncier": export_ods("data.economie.gouv.fr", "fiscalite-locale-des-particuliers",
                          select="insee_com,taux_global_tfb", where='exercice="2025"'),
    "douane": "https://www.douane.gouv.fr/sites/default/files/2026-10/07/202608-Regional-2023-export.zip",
    "basilic": (
        "https://static.data.gouv.fr/resources/base-des-lieux-et-equipements-culturels-basilic/"
        "20260218-084338/base-des-lieux-et-des-equipements-culturels.csv"
    ),
    "clubs": (
        "https://static.data.gouv.fr/resources/donnees-geocodees-issues-du-recensement-des-licences-et-"
        "clubs-aupres-des-federations-sportives-agreees-par-le-ministere-charge-des-sports/"
        "20251229-163249/clubs-data-2023.csv"
    ),
    "dares": (
        "https://dares.travail-emploi.gouv.fr/sites/default/files/a4ef7ed6cced6fba8b492fec3933678c/"
        "R%C3%A9partition%20territoriale%20-%20part%20du%20m%C3%A9tier%20dans%20l%27emploi%20d%C3%A9partemental"
        "%20et%20r%C3%A9partition%20par%20d%C3%A9partement%20de%20l%27emploi%20du%20m%C3%A9tier.xlsx"
    ),
    "detenus": (
        "https://static.data.gouv.fr/resources/statistique-mensuelle-de-la-population-ecrouee-et-detenue-en-france/"
        "20261013-162028/statistique-etablissements-01092026.xlsx"
    ),
    # Les établissements pénitentiaires de l'annuaire de l'administration (service-public.fr).
    "annuaire": (
        "https://api-lannuaire.service-public.fr/api/explore/v2.1/catalog/datasets/api-lannuaire-administration/exports/json?"
        + urllib.parse.urlencode({
            "select": "nom,pivot,adresse",
            "where": " OR ".join(f'search("{t}")' for t in
                                 ["centre_penitentiaire", "maison_arret", "centre_detention", "maison_centrale"]),
        })
    ),
    "dgf": "http://www.dotations-dgcl.interieur.gouv.fr/consultation/criteres_repartition_csv.php?annee=2026&ct=com",
    "dgafp": "https://www.fonction-publique.gouv.fr/files/files/publications/vue-rapport-annuel/ra_2025-caracteristiques_postes.zip",
    "dsed": (
        "https://static.data.gouv.fr/resources/stock-et-flux-des-titres-de-sejour-en-france-sur-lannee-2024/"
        "20260821-131354/2024-sejour-flux-region-monde-nationalites.csv"
    ),
    "monde": "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/v5.1.2/geojson/ne_110m_admin_0_countries.geojson",
    "ecodef": "https://static.data.gouv.fr/resources/ecodef-statistiques-ndeg-255/20241212-133351/donnes-ecodef-255.xlsx",
}
