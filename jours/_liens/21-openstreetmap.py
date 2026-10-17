# Les fichiers que lit la page J21, à leur adresse officielle.
import urllib.parse

SOURCES = {
    # Le recensement des équipements sportifs (RES), réduit aux colonnes utiles.
    "res": (
        "https://equipements.sports.gouv.fr/api/explore/v2.1/catalog/datasets/data-es/exports/parquet?"
        + urllib.parse.urlencode({"select": ",".join([
            "equip_numero", "inst_nom", "equip_nom", "equip_type_code", "equip_nature",
            "new_name", "dep_code_filled", "dens_lib", "equip_x", "equip_y", "inst_hs_bool",
        ])})
    ),
}
