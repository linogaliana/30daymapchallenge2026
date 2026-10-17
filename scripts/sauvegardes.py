"""Liste les fichiers à copier sur le S3 du SSP Cloud.

Dans jours/_liens/*.py, chaque entrée de SOURCES est l'URL de la copie sur le SSP Cloud,
précédée en commentaire de l'adresse officielle du fichier :

    # https://www.insee.fr/fr/statistiques/fichier/9004795/RP2023_mobpro.parquet
    "mobpro": "https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/RP2023_mobpro.parquet",

Le script écrit jours/_liens/sauvegardes.yml : pour chaque fichier, une fois même s'il sert à
plusieurs pages, son adresse officielle (source) et celle de sa copie (substitution).

    uv run python scripts/sauvegardes.py
"""

import pathlib
import re

import yaml

LIENS = pathlib.Path(__file__).resolve().parent.parent / "jours" / "_liens"
ENTREE = re.compile(r'^\s*# (https?://\S+)\n\s*"[^"]+": "(https?://[^"]+)",', re.M)

sauvegardes = {}
for fichier in sorted(LIENS.glob("*.py")):
    for source, copie in ENTREE.findall(fichier.read_text(encoding="utf-8")):
        assert sauvegardes.get(source, copie) == copie, f"deux copies pour {source}"
        sauvegardes[source] = copie

sortie = LIENS / "sauvegardes.yml"
with open(sortie, "w", encoding="utf-8") as f:
    f.write("# Écrit par scripts/sauvegardes.py à partir de jours/_liens/*.py : ne pas modifier à la main.\n")
    yaml.safe_dump([{"source": s, "substitution": c} for s, c in sauvegardes.items()], f,
                   sort_keys=False, allow_unicode=True, width=1000)
print(f"{len(sauvegardes)} fichiers : {sortie}")
