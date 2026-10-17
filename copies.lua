-- Ajoute aux pages de jour qui lisent des fichiers (celles qui ont un jours/_liens/NN-theme.py)
-- un encadré d'avertissement repliable, sous le titre « Making of » : les données sont lues sur
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
    title = "Pourquoi la lecture des données depuis le SSP Cloud ?",
    collapse = true,
    content = pandoc.read(texte, "markdown").blocks
  })
  -- Juste sous le titre « Making of », ou à défaut sous « Les données », qui ouvre la partie
  -- technique des pages sans ce titre.
  for _, titre in ipairs({"Making of", "Les données"}) do
    for i, bloc in ipairs(doc.blocks) do
      if bloc.t == "Header" and pandoc.utils.stringify(bloc) == titre then
        doc.blocks:insert(i + 1, encadre)
        return doc
      end
    end
  end
  return doc
end
