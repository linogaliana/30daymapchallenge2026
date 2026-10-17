-- Ajoute aux pages de jour qui lisent des fichiers (celles qui ont un jours/_liens/NN-theme.py)
-- un encadré d'avertissement repliable, sous celui de la démarche : les données sont lues sur
-- leur copie du SSP Cloud, et non à leur adresse officielle. Son texte est dans _copies.md, à la
-- racine du projet.

function Pandoc(doc)
  local fichier = (quarto.doc.input_file or ""):gsub("\\", "/")  -- chemins Windows
  local page = fichier:match("jours/(%d%d%-[^/]*)%.qmd$")
  if not page then
    return doc
  end

  local liens = io.open(pandoc.path.join({quarto.project.directory, "jours", "_liens", page .. ".py"}), "r")
  if not liens then
    return doc
  end
  liens:close()

  local f = io.open(pandoc.path.join({quarto.project.directory, "_copies.md"}), "r")
  if not f then
    return doc
  end
  local texte = f:read("a")
  f:close()

  local encadre = quarto.Callout({
    type = "warning",
    title = "Les données lues sur le SSP Cloud",
    collapse = true,
    content = pandoc.read(texte, "markdown").blocks
  })
  -- Juste après l'encadré de la démarche, qu'approche.lua place en tête de page.
  doc.blocks:insert(math.min(2, #doc.blocks + 1), encadre)
  return doc
end
