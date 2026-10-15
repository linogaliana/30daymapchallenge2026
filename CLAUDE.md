# 30daymapchallenge2026

Site Quarto des 30 cartes du [#30DayMapChallenge](https://30daymapchallenge.com/) 2026 (1er au 30 novembre), avec des données de la statistique publique (Insee, Drees, IGN…), entièrement reproductible : chaque page montre le code qui va du fichier source à la carte.

## Ne pas committer

Ne jamais faire `git commit` ni `git push`, sauf demande explicite. Ne pas non plus modifier l'index (`git add`, `git restore --staged`) sans qu'on le demande.

## Structure

- `jours/NN-theme.qmd` : une page par jour (`01-points.qmd`…). Le numéro en tête du nom de fichier est le jour : l'accueil s'en sert.
- `index.qmd` + `_calendrier.ejs` : l'accueil, un listing Quarto des `jours/[0-9][0-9]-*.qmd` rendu en calendrier par semaine (J1 à J7, J8 à J14…). Les 30 thèmes officiels sont listés dans le gabarit. Un jour avec `image:` dans son en-tête s'affiche avec sa carte, un jour avec une page mais sans image est « en préparation », les autres sont « à venir ».
- `jours/vignettes/NN-theme.webp` : captures de la première carte de chaque page, faites par `scripts/vignettes.py` sur le site rendu (Playwright). Versionnées.
- `_quarto.yml` : la barre de navigation range les jours par semaine (« Semaine 1 · J1 à J7 ») ; ajouter un menu par semaine.
- Filtres Lua (`_quarto.yml`) : `en-cours.lua` (avertissement « en cours de rédaction » avant le jour J), `approche.lua` (encadré repliable « La démarche de ce site » en tête de chaque jour, texte dans `_approche.md`), `charte.lua` (charte de couleur d'une page et souligné coloré, voir plus bas).
- `theme.scss` (Open Sans, interlignes et marges, commun aux thèmes clair `cosmo` et sombre `darkly`) et `styles.css` (composants : lecteur, légendes, petits multiples, calendrier).
- `.github/workflows/publish.yml` : rendu et publication sur GitHub Pages à chaque push sur `main`, rendu seul sur les pull requests.

## Ce qui n'est pas versionné

`_site/`, `_freeze/` et les données produites au rendu (`jours/donnees/`, écrites par J3, J9, J10, J11 et J14) : tout se reconstruit à partir des `.qmd`. En CI, `_freeze/` est gardé dans le cache d'Actions. Ne rien écrire de généré ailleurs que dans ces dossiers.

## Une page de jour

- En-tête : `title: "JN · Thème. Sujet"` (le calendrier affiche le sujet en retirant `JN · Thème.`), `description:` d'une phrase, `image:` quand la vignette existe, `execute: echo: true`, `code-overflow: wrap`.
- Plan habituel : un paragraphe d'accroche (`p.lead` calculé en OJS), la carte interactive, puis `## Les données` (tableau des sources : source, producteur, ce qu'on en tire, format), `## Les traitements`, `## Les données de la carte` (tableau consultable, CSV téléchargeable), `## Précautions` si besoin, `## Pour aller plus loin`.
- Le traitement est en Python + DuckDB, montré au lecteur (`echo: true`) ; ce qui ne sert qu'à la mise en page est masqué (`#| echo: false`, `//| echo: false`). Les tables passent au JavaScript avec `ojs_define`.
- Les cartes sont en Observable Plot (ou MapLibre pour J1), dans des cellules `{ojs}`.
- Fonds de carte : le package Python [`cartiflette`](https://inseefrlab.github.io/cartiflette/), `carti_download(..., engine="duckdb", con=con)`, qui renvoie une relation DuckDB non évaluée, utilisable dans `con.sql` par son nom de variable (voir J1). Le filtre `where=` évite de tout lire.
- DuckDB : `LOAD spatial` puis `SET geometry_always_xy = true` (coordonnées en longitude, latitude).
- Les sources sont téléchargées au rendu depuis leur URL officielle : pas de fichier de données ajouté à la main dans le dépôt.
  Seule exception : `jours/sources/`, pour les fichiers que le rendu ne peut pas télécharger (le site de la Dares est derrière un pare-feu à captcha, lu par J10). Le code essaie toujours l'URL officielle d'abord.

## Style

- Charte d'une page, dans l'en-tête : `charte: {couleur: "#009099", sombre: "#3fc1c9"}` (variable CSS `--couleur-page` : boutons du lecteur et de téléchargement, souligné). Dans le texte, `[texte]{.underline}` souligne de la couleur de la page, `[texte]{.underline color="#ce614a"}` d'une autre. Reprendre les couleurs de la carte.
- Parties numérotées (`number-sections: true`), sauf `## Références {.unnumbered}`.
- Blocs de code montrés : un titre avec `#| filename: "…"`. Thème de code sombre (`arrow-dark`) en clair comme en sombre.

- Tout en français : texte, noms de variables, commentaires (`sombre`, `couleurOuverte`, `echelle`…). Typographie française (espace avant `:`, `;`, `%`, guillemets « »), nombres formatés avec `toLocaleString("fr-FR")`.
- Thème clair et thème sombre : les cellules OJS suivent `sombre` (classe `quarto-dark` du `body`) et adaptent fond et couleurs ; vérifier les deux.
- Pages lisibles sur mobile.

## Commandes

```bash
uv sync
uv run quarto preview                 # aperçu local
uv run quarto render                  # site dans _site/
uv run quarto render jours/01-points.qmd
uv run --with playwright --with pillow python scripts/vignettes.py   # vignettes, après un rendu complet
```

Pour les vignettes sur l'environnement de dev, Chromium est celui du cache Playwright : `CHROME=$(ls ~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome | head -1)`.
