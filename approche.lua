-- Ajoute en tête des pages de jour (jours/NN-theme.qmd) un encadré repliable
-- qui présente la démarche du site. Son texte est dans _approche.md, à la
-- racine du projet. Contrairement à l'avertissement d'en-cours.lua, il reste
-- quelle que soit la date.

-- Les shortcodes ne sont pas interprétés dans un texte lu par un filtre :
-- {{< fa groupe icone >}} est remplacé par la balise de Font Awesome.
local function icones(texte)
  return texte:gsub("{{<%s*fa%s+(%S+)%s+(%S+)%s*>}}", function(groupe, icone)
    return string.format('<i class="fa-%s fa-%s" aria-label="%s"></i>', groupe, icone, icone)
  end)
end

function Pandoc(doc)
  local fichier = (quarto.doc.input_file or ""):gsub("\\", "/")  -- chemins Windows
  if not fichier:match("jours/%d%d%-[^/]*%.qmd$") then
    return doc
  end

  local chemin = pandoc.path.join({quarto.project.directory, "_approche.md"})
  local f = io.open(chemin, "r")
  if not f then
    return doc
  end
  local texte = icones(f:read("a"))
  f:close()

  -- La feuille de style de l'extension fontawesome, même nom et même version :
  -- elle n'est copiée qu'une fois si la page utilise aussi le shortcode.
  quarto.doc.add_html_dependency({
    name = "fontawesome6",
    version = "6.7.2",
    stylesheets = {
      "_extensions/quarto-ext/fontawesome/assets/css/all.min.css",
      "_extensions/quarto-ext/fontawesome/assets/css/latex-fontsize.css"
    }
  })

  local encadre = quarto.Callout({
    type = "note",
    title = "La démarche de ce site",
    collapse = true,
    content = pandoc.read(texte, "markdown").blocks
  })
  doc.blocks:insert(1, encadre)
  return doc
end
