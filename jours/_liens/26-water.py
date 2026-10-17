# Les fichiers que lit la page J26, à leur adresse officielle.
import urllib.parse

SOURCES = {
    "rei": (
        "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
        "impots-locaux-fichier-de-recensement-des-elements-dimposition-a-la-fiscalite-dir/"
        "attachments/rei_2025_fichier_notice_tracezip"
    ),
    # L'historique de la fiscalité locale, réduit aux colonnes Gemapi.
    "historique": (
        "https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
        "fiscalite-locale-des-particuliers/exports/csv?"
        + urllib.parse.urlencode({"select": "exercice,insee_com,b52ggemapi,e52ggemapi,h52ggemapi", "delimiter": ";"})
    ),
}
