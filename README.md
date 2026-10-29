# 30daymapchallenge2026

Les 30 cartes du [#30DayMapChallenge](https://30daymapchallenge.com/) 2026, avec des données de la statistique publique. Site Quarto : un `.qmd` par jour dans `jours/`. Les données sont traitées avec DuckDB (Python) au moment du rendu, et les cartes sont faites avec Observable Plot.

## Construire le site

Les dépendances, Quarto compris (paquet `quarto-cli`), sont gérées avec [uv](https://docs.astral.sh/uv/) :

```bash
uv sync
uv run quarto preview   # aperçu local
uv run quarto render    # site dans _site/
```

Les calculs sont mis en cache dans `_freeze/` (`freeze: auto`) : une page n'est recalculée que si son `.qmd` change. `_freeze/`, `_site/` et les données produites au rendu (`jours/donnees/`) ne sont pas versionnés : tout se reconstruit à partir des `.qmd`, en retéléchargeant les sources.

## Publication

À chaque push sur `main`, GitHub Actions (`.github/workflows/publish.yml`) rend le site et le publie sur GitHub Pages ; sur une pull request, il le rend seulement, pour vérifier qu'il se construit. Pour l'instant, le rendu utilise le profil `wip` (`_quarto-wip.yml`) : les jours de l'accueil sont tous « en préparation », sans lien, et la barre de navigation ne mène pas à leurs pages. Pour voir ce rendu en local : `uv run quarto preview --profile wip`. `_freeze/` est gardé d'une exécution à l'autre dans le cache d'Actions : seules les pages modifiées sont recalculées. Le premier rendu, ou un rendu après expiration du cache (7 jours sans usage), recalcule tout.

Dans les réglages du dépôt, *Settings > Pages > Build and deployment*, la source doit être *GitHub Actions*.

## Vignettes de l'accueil

L'accueil est un calendrier des 30 jours (`index.qmd`, gabarit `_calendrier.ejs`) : un jour dont la page a un champ `image:` s'affiche avec sa carte, un jour qui a une page sans image est « en préparation ». Les vignettes (`jours/vignettes/*.webp`) sont des captures de la première carte de chaque page, prises sur le site rendu :

```bash
uv run quarto render
uv run --with playwright --with pillow python scripts/vignettes.py
```

puis ajouter `image: vignettes/NN-theme.webp` dans l'en-tête de la page du jour.
