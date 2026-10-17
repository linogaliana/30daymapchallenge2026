-- Ajoute en tête des pages de jour (jours/NN-theme.qmd) un avertissement
-- « travail en cours » tant que le jour NN de novembre n'est pas arrivé.
-- La date est celle du rendu : une page rendue avant son jour garde
-- l'avertissement jusqu'au rendu suivant.

local annee = 2026

function Pandoc(doc)
  local fichier = (quarto.doc.input_file or ""):gsub("\\", "/")  -- chemins Windows
  local numero = fichier:match("jours/(%d%d)%-[^/]*%.qmd$")
  if not numero then
    return doc
  end

  local jour = string.format("%d-11-%s", annee, numero)
  local aujourdhui = os.date("%Y-%m-%d")
  if aujourdhui >= jour then
    return doc
  end

  local avertissement = quarto.Callout({
    type = "warning",
    title = "Page en cours de rédaction",
    content = pandoc.read("Cette page est un *work in progress* et pourrait être mise à jour prochainement.", "markdown").blocks
  })

  doc.blocks:insert(1, avertissement)
  return doc
end
