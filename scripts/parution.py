"""Écrit le profil Quarto `parution` (_quarto-parution.yml) : le site tel qu'il est
publié à une date donnée, avec les seuls jours arrivés.

Le jour N paraît le N novembre 2026 : seules les pages jours/NN-*.qmd dont le
jour est passé sont rendues (project.render), et donc listées dans le calendrier
de l'accueil et dans la barre de navigation. Les jours suivants sont « à venir ».

    uv run python scripts/parution.py                     # date du jour
    uv run python scripts/parution.py --date 2026-11-05   # le site du 5 novembre
    uv run quarto render --profile parution

Le fichier produit n'est pas versionné : GitHub Actions le régénère à chaque
rendu (push et tous les jours à minuit, heure de Paris).

Le profil relance aussi ce script après le rendu (post-render) : le listing de
l'accueil copie dans le site les .qmd des jours non rendus, qui sont supprimés.
"""

import argparse
import datetime
import os
from pathlib import Path

import yaml

RACINE = Path(__file__).resolve().parent.parent
ANNEE, MOIS = 2026, 11


def jours_parus(date: datetime.date) -> int:
    """Nombre de jours du défi arrivés à `date` (0 avant le 1er novembre, 30 après)."""
    if (date.year, date.month) < (ANNEE, MOIS):
        return 0
    if (date.year, date.month) > (ANNEE, MOIS):
        return 30
    return min(date.day, 30)


def nettoyer(dossier: Path):
    """Après le rendu : retire du site les .qmd des jours pas encore parus."""
    for source in (dossier / "jours").glob("[0-9][0-9]-*.qmd"):
        source.unlink()


def main():
    # Lancé par Quarto après le rendu (post-render du profil).
    if "QUARTO_PROJECT_OUTPUT_DIR" in os.environ:
        nettoyer(Path(os.environ["QUARTO_PROJECT_OUTPUT_DIR"]))
        return

    analyseur = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    analyseur.add_argument(
        "--date",
        type=datetime.date.fromisoformat,
        default=datetime.date.today(),
        help="date de parution, AAAA-MM-JJ (par défaut : aujourd'hui)",
    )
    date = analyseur.parse_args().date
    dernier = jours_parus(date)

    # Les pages des jours parus, par numéro : jours/01-points.qmd est le jour 1.
    pages = {}
    for chemin in sorted((RACINE / "jours").glob("[0-9][0-9]-*.qmd")):
        numero = int(chemin.name[:2])
        if numero <= dernier:
            pages[numero] = f"jours/{chemin.name}"

    # Un menu par semaine qui a au moins un jour paru, comme _quarto-complet.yml.
    menus = []
    for semaine in range(5):
        premier = 7 * semaine + 1
        fin = min(premier + 6, 30)
        menu = [pages[n] for n in range(premier, fin + 1) if n in pages]
        if menu:
            menus.append({"text": f"Semaine {semaine + 1} · J{premier} à J{fin}", "menu": menu})

    profil = {
        # Lu par parution.lua : les liens vers les jours suivants sont retirés.
        "parution": dernier,
        "project": {
            "render": ["index.qmd", "about.qmd", *pages.values()],
            "post-render": "scripts/parution.py",
        },
        "website": {"navbar": {"left": [*menus, "about.qmd"]}},
    }
    entete = (
        f"# Généré par scripts/parution.py pour le {date.isoformat()} : ne pas modifier.\n"
        f"# Jours parus : {dernier} sur 30, dont {len(pages)} avec une page.\n"
    )
    sortie = RACINE / "_quarto-parution.yml"
    sortie.write_text(
        entete + yaml.safe_dump(profil, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"{sortie.name} : {len(pages)} page(s) de jour au {date.isoformat()}")


if __name__ == "__main__":
    main()
