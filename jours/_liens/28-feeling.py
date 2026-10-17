# Les fichiers que lit la page J28, à leur adresse officielle.
import urllib.parse

SOURCES = {
    # Le classeur des données complémentaires de chaque publication sur les passoires thermiques.
    "passoires_2024": "https://www.statistiques.developpement-durable.gouv.fr/media/7941/download?inline",
    "passoires_2025": "https://www.statistiques.developpement-durable.gouv.fr/media/8810/download?inline",
    # Le nombre de DPE par département et par zone climatique.
    "zones_climatiques": (
        "https://data.ademe.fr/data-fair/api/v1/datasets/dpe03existant/values_agg?"
        + urllib.parse.urlencode({"field": "code_departement_ban;zone_climatique", "agg_size": "120;3", "size": 0})
    ),
}
