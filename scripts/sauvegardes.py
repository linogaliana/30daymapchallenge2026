"""Liste les fichiers sources de toutes les pages et leur adresse de sauvegarde sur le S3 du SSP Cloud.

Lit les dicts SOURCES de jours/_liens/*.py, regroupe les URL identiques (un même fichier lu par
plusieurs pages) et écrit jours/_liens/sauvegardes.yml : pour chaque fichier, son URL officielle
(source) et celle de sa copie (substitution).

    uv run python scripts/sauvegardes.py
"""

import pathlib
import posixpath
import re
import runpy
import unicodedata
import urllib.parse
from collections import defaultdict

import yaml

S3 = "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/"
LIENS = pathlib.Path(__file__).resolve().parent.parent / "jours" / "_liens"
EXTENSIONS = (".csv", ".zip", ".parquet", ".xlsx", ".json", ".gz", ".geojson", ".txt")
# Fins d'URL sans point qui disent pourtant le format : exports d'API, pièces jointes Opendatasoft.
FORMATS = {"csv": ".csv", "parquet": ".parquet", "json": ".json", "values_agg": ".json",
           "_xlsx": ".xlsx", "xlsx": ".xlsx", "tracezip": ".zip"}


def ascii(nom):
    """Un nom de fichier sans accents ni espaces, utilisable comme clé S3."""
    nom = unicodedata.normalize("NFKD", nom).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9._-]+", "-", nom).strip("-")


def nom_de_fichier(url, cle):
    adresse = urllib.parse.urlsplit(url)
    dernier = urllib.parse.unquote(posixpath.basename(adresse.path))
    if not adresse.query and dernier.lower().endswith(EXTENSIONS):
        return ascii(dernier)
    extension = next((e for fin, e in FORMATS.items() if dernier.endswith(fin)), "")
    return ascii(cle) + extension


# Chaque URL, avec les pages et les clés qui la lisent, dans l'ordre des pages.
usages = defaultdict(list)
for fichier in sorted(LIENS.glob("*.py")):
    for cle, url in runpy.run_path(str(fichier))["SOURCES"].items():
        usages[url].append((fichier.stem, cle))

# Un nom pris par deux URL différentes est préfixé, pour chacune, du nom de sa page.
candidats = {url: nom_de_fichier(url, pages[0][1]) for url, pages in usages.items()}
compte = defaultdict(int)
for nom in candidats.values():
    compte[nom] += 1
noms = {url: nom if compte[nom] == 1 else f"{usages[url][0][0]}-{nom}" for url, nom in candidats.items()}
assert len(set(noms.values())) == len(noms), "deux sauvegardes porteraient le même nom"

sauvegardes = [{"source": url, "substitution": S3 + nom} for url, nom in noms.items()]
sortie = LIENS / "sauvegardes.yml"
with open(sortie, "w", encoding="utf-8") as f:
    f.write("# Écrit par scripts/sauvegardes.py à partir de jours/_liens/*.py : ne pas modifier à la main.\n")
    yaml.safe_dump(sauvegardes, f, sort_keys=False, allow_unicode=True, width=1000)
print(f"{len(sauvegardes)} fichiers ({sum(map(len, usages.values()))} liens) : {sortie}")
