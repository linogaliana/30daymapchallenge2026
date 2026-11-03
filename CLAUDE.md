# 30daymapchallenge2026

Site Quarto des 30 cartes du [#30DayMapChallenge](https://30daymapchallenge.com/) 2026 (1er au 30 novembre), avec des données de la statistique publique (Insee, Drees, IGN…), entièrement reproductible : chaque page montre le code qui va du fichier source à la carte.

## Ne pas committer

Ne jamais faire `git commit` ni `git push`, sauf demande explicite. Ne pas non plus modifier l'index (`git add`, `git restore --staged`) sans qu'on le demande.

Quand un commit est demandé, ne pas le signer : pas de ligne `Co-Authored-By: Claude…` ni de mention « Generated with Claude Code » dans le message. Le message ne contient que la description du changement.

## Branches : `dev`, pas `main`

`main` est le site publié : tout push sur `main` déclenche la publication sur GitHub Pages (`publish.yml`). Ne jamais fusionner dans `main` sans demande explicite de mise en ligne. Le travail se fait dans des branches ; quand une ligne de travail est finie (et qu'on a demandé de committer), sa branche est fusionnée dans `dev`. Créer `dev` à partir de `main` si elle n'existe pas encore.

## Travailler dans un worktree git

Ne jamais modifier le code dans le dépôt principal (`C:\Users\linog\Documents\PROJECTS\30daymapchallenge2026`). Toute modification se fait dans un worktree git sur sa propre branche, créé par `git worktree add .claude/worktrees/<nom> -b <branche>` (`.claude/` est ignoré par git) ou par l'isolation en worktree de l'agent. Cela vaut pour les sous-agents : chacun a son worktree, pour que des travaux en parallèle ne se marchent pas dessus. Jamais de `git stash` pour déplacer du travail : passer par un worktree ou par `git diff` / `git apply`.

Comme on ne committe pas sans demande, le travail d'un sous-agent se récupère par `git diff` dans son worktree, appliqué (`git apply`) dans le worktree d'intégration de l'agent principal.

Un worktree ne contient que les fichiers versionnés : ni `_freeze/`, ni `jours/donnees/`, ni `.venv`, ni les fichiers non suivis (un `jours/_liens/NN-theme.py` pas encore ajouté, par exemple). Y lancer `uv sync` avant tout rendu, et s'attendre à ce que le premier rendu réexécute tout et retélécharge les sources.

## Orchestrer, pas implémenter

L'agent principal planifie, délègue, relit et vérifie. Il n'écrit pas le premier jet du code.

- Découper. Diviser la tâche en morceaux indépendants aux frontières de fichiers nettes (une page `jours/NN-theme.qmd`, son `_liens/NN-theme.py`, un filtre Lua, `styles.css`…), avec pour chacun un brief précis : quoi changer, où, et à quoi on reconnaît que c'est fini.
- Implémenter avec des sous-agents économiques en parallèle. Confier chaque morceau à un sous-agent sur le modèle le moins cher capable de le faire (Haiku sous Claude, le plus petit modèle mini sous Codex). Lancer les morceaux indépendants en même temps, chacun dans son worktree.
- Relire au centre. Quand les sous-agents ont fini, l'agent principal lit lui-même chaque diff : justesse, cohérence entre les morceaux, accord avec le code voisin et avec les règles de ce fichier (français, typographie, `requests`, `SOURCES[...]`, thèmes clair et sombre…). Il ne réunit les morceaux qu'après cette relecture.
- Vérifier au centre. Seulement après la relecture, l'agent principal lance les vérifications, une fois, sur le résultat réuni : `uv run quarto render jours/NN-theme.qmd` pour les pages touchées (ou `uv run quarto render` si le changement est commun), `scripts/sauvegardes.py` après un ajout de source, et un coup d'œil aux pages en clair et en sombre.
- Déléguer les corrections. Les problèmes trouvés à la relecture ou aux vérifications repartent à des sous-agents économiques avec un brief précis, en parallèle quand c'est possible. Puis relire et vérifier de nouveau.
- Corriger soi-même seulement à la toute fin. L'agent principal ne modifie le code directement que pour les dernières petites retouches, quand la délégation ne vaut plus la peine.

## Les sous-agents ne vérifient rien

Les sous-agents ne lancent ni rendu Quarto (`quarto render`, `quarto preview`), ni scripts (`scripts/*.py`), ni tests, linters, vérificateurs de types, ni formateurs qui réécrivent d'autres fichiers, ni aucune autre commande de vérification. Ils écrivent le code et rendent compte de ce qu'ils ont changé. Le dire explicitement dans chaque brief de sous-agent. Toute vérification revient à l'agent principal, après relecture.

## Cas limites et sur-ingénierie

Avant d'ajouter de la complexité pour un cas limite hypothétique ou très improbable (concurrence, sécurité, source qui change de format…), expliquer à l'utilisateur le scénario d'échec concret, sa probabilité et le coût en complexité, et obtenir son accord. Ne pas élargir le périmètre en silence au nom d'une robustesse théorique.

## Structure

- `jours/NN-theme.qmd` : une page par jour (`01-points.qmd`…). Le numéro en tête du nom de fichier est le jour : l'accueil s'en sert.
- `index.qmd` + `_calendrier.ejs` : l'accueil, un listing Quarto des `jours/[0-9][0-9]-*.qmd` rendu en calendrier par semaine (J1 à J7, J8 à J14…). Les 30 thèmes officiels sont listés dans le gabarit. Un jour avec `image:` dans son en-tête s'affiche avec sa carte, un jour avec une page mais sans image est « en préparation », les autres sont « à venir ».
- `jours/_liens/NN-theme.py` : le dict `SOURCES` d'une page : pour chaque fichier lu, une clé et l'URL de sa copie sur le S3 du SSP Cloud (`https://minio.lab.sspcloud.fr/lgaliana/30daymapchallenge2026/<nom>`), précédée en commentaire de son adresse officielle (`# https://…`). Inclus dans la page par une cellule « Les sources » placée après la connexion DuckDB : `{{< include _liens/NN-theme.py >}}`. `scripts/sauvegardes.py` relève les paires adresse officielle → copie dans `jours/_liens/sauvegardes.yml`, la liste des fichiers à copier : le relancer après tout ajout de source, puis copier le nouveau fichier sur le S3. Le `_` empêche Quarto d'en faire des pages.
- `jours/vignettes/NN-theme.webp` : captures de la première carte de chaque page, faites par `scripts/vignettes.py` sur le site rendu (Playwright). Versionnées.
- Profils Quarto : `complet` par défaut (`_quarto-complet.yml` : la barre de navigation range les jours par semaine, « Semaine 1 · J1 à J7 » ; ajouter un menu par semaine), `wip` (`_quarto-wip.yml`, `quarto render --profile wip` : `wip: true` met tous les jours de l'accueil « en préparation », sans lien, et la barre ne mène pas aux jours) et `parution`, utilisé par GitHub Actions : `_quarto-parution.yml`, non versionné, est écrit par `scripts/parution.py [--date AAAA-MM-JJ]` selon la date (le jour N paraît le N novembre) ; il ne rend que les jours arrivés (`project.render`), les range dans la barre par semaine et passe `parution: N` à `parution.lua`. Les jours suivants sont « à venir » sur l'accueil. `_quarto.yml` garde ce qui est commun ; Quarto ajoute les listes `navbar.left` des profils à la sienne.
- Filtres Lua (`_quarto.yml`) : `en-cours.lua` (avertissement « en cours de rédaction » avant le jour J), `approche.lua` (encadré repliable « La démarche de ce site » en tête de chaque jour, texte dans `_approche.md`), `copies.lua` (encadré d'avertissement repliable « Les données lues sur le SSP Cloud » sous le titre « Making of », ou à défaut « Les données », des pages qui ont un `_liens/NN-theme.py`, texte dans `_copies.md`), `charte.lua` (charte de couleur d'une page et souligné coloré, voir plus bas), `parution.lua` (profil parution : retire les lignes de tableau, et dé-lie les liens, vers les jours pas encore parus), `entete.lua` (en-tête des jours : le titre « J1 · Points. Les maternités » s'affiche en surtitre « Jour 1 · Points · dimanche 1er novembre » et sujet, par un script ; le titre YAML ne change pas).
- `theme.scss` (polices : Open Sans pour le texte, Fraunces pour les titres, JetBrains Mono pour le code ; interlignes, marges, en-têtes, navigation ; commun aux thèmes clair `cosmo` et sombre `darkly`), `theme-clair.scss` et `theme-sombre.scss` (fond, texte et liens de chaque thème) et `styles.css` (composants : lecteur, légendes, petits multiples, calendrier).
- `.github/workflows/publish.yml` : rendu (profil `parution`, fuseau `Europe/Paris`) et publication sur GitHub Pages à chaque push sur `main` et tous les jours à 0 h 05 (heure de Paris) en novembre, rendu seul sur les pull requests.

## Ce qui n'est pas versionné

`_site/`, `_freeze/` et les données produites au rendu (`jours/donnees/`, écrites par J3, J4, J7, J9, J10, J11 et J14) : tout se reconstruit à partir des `.qmd`. En CI, `_freeze/` est gardé dans le cache d'Actions. Ne rien écrire de généré ailleurs que dans ces dossiers.

## Une page de jour

- En-tête : `title: "JN · Thème. Sujet"` (le calendrier affiche le sujet en retirant `JN · Thème.`), `description:` d'une phrase, `image:` quand la vignette existe, `execute: echo: true`, `code-overflow: wrap`.
- Plan habituel : un paragraphe d'accroche (`p.lead` calculé en OJS), la carte interactive, puis `## Les données` (tableau des sources : source, producteur, ce qu'on en tire, format), `## Les traitements`, `## Les données de la carte` (tableau consultable, CSV téléchargeable), `## Précautions` si besoin, `## Pour aller plus loin`.
- Le traitement est en Python + DuckDB, montré au lecteur (`echo: true`) ; ce qui ne sert qu'à la mise en page est masqué (`#| echo: false`, `//| echo: false`). Les tables passent au JavaScript avec `ojs_define`.
- Les cartes sont en Observable Plot (ou MapLibre pour J1), dans des cellules `{ojs}`.
- Fonds de carte : le package Python [`cartiflette`](https://inseefrlab.github.io/cartiflette/), `carti_download(..., engine="duckdb", con=con)`, qui renvoie une relation DuckDB non évaluée, utilisable dans `con.sql` par son nom de variable (voir J1). Le filtre `where=` évite de tout lire.
- DuckDB : `LOAD spatial` puis `SET geometry_always_xy = true` (coordonnées en longitude, latitude).
- Les sources sont téléchargées au rendu depuis leur URL officielle : pas de fichier de données ajouté à la main dans le dépôt.
  Les URL ne sont pas écrites dans la page mais dans `jours/_liens/NN-theme.py`, une entrée par fichier (gabarits déroulés, adresse officielle complète avec les filtres d'export), et le code les lit par `SOURCES["cle"]`, sans rien d'autre à changer. Restent dans la page les API interrogées élément par élément (géocodage, isochrones, pages WFS, Overpass) et les fonds cartiflette, déjà sur le S3 du SSP Cloud.
  Récupération des données en Python : toujours `requests` (`requests.get`, `params=`, `raise_for_status`, `.content`/`.json()`, `stream=True` pour les gros fichiers), jamais `urllib.request` (`urlopen`, `urlretrieve`, `Request`, contextes SSL…). `requests` vérifie les certificats avec `certifi`, ce qui évite les erreurs de certificat du magasin Windows (Agreste, Douanes). Si DuckDB lit lui-même une URL et bute sur un certificat sous Windows : `SET ca_cert_file = '{certifi.where()}'` (voir J25).
  Seule exception : `jours/sources/`, pour les fichiers que le rendu ne peut pas télécharger (le site de la Dares est derrière un pare-feu à captcha, lu par J10), en secours de la copie du SSP Cloud.

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
