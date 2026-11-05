# Les fichiers que lit la page J21 : leur copie sur le SSP Cloud, et en
# commentaire leur adresse officielle.
SOURCES = {
    # https://ministere-culture.s3.sbg.io.cloud.ovh.net/POP/merimee.csv
    "merimee": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/merimee.csv",
    # https://qlever.cs.uni-freiburg.de/api/osm-planet?query=PREFIX%20geo%3A%20%3Chttp%3A%2F%2Fwww.opengis.net%2Font%2Fgeosparql%23%3E%20PREFIX%20geof%3A%20%3Chttp%3A%2F%2Fwww.opengis.net%2Fdef%2Ffunction%2Fgeosparql%2F%3E%20PREFIX%20osmkey%3A%20%3Chttps%3A%2F%2Fwww.openstreetmap.org%2Fwiki%2FKey%3A%3E%20PREFIX%20osmmeta%3A%20%3Chttps%3A%2F%2Fwww.openstreetmap.org%2Fmeta%2F%3E%20SELECT%20%3Fosm%20%3Fref%20%3Fnom%20%3Fmodification%20%28geof%3Acentroid%28%3Fgeom%29%20AS%20%3Fcentre%29%20WHERE%20%7B%20%3Fosm%20osmkey%3Aref%3Amhs%20%3Fref%20.%20OPTIONAL%20%7B%20%3Fosm%20osmkey%3Aname%20%3Fnom%20%7D%20%3Fosm%20osmmeta%3Atimestamp%20%3Fmodification%20.%20%3Fosm%20geo%3AhasGeometry%2Fgeo%3AasWKT%20%3Fgeom%20.%20%7D&action=csv_export
    "osm": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/osm_mhs.csv",
}
