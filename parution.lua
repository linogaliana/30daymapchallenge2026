-- Profil parution (scripts/parution.py) : `parution: N` dans les métadonnées, seuls
-- les jours 1 à N sont rendus. Les liens vers les pages des jours suivants
-- (jours/NN-theme.qmd) mèneraient nulle part : une ligne de tableau qui commence
-- par un tel lien est retirée (les sources jour par jour de l'accueil), les autres
-- liens sont remplacés par leur texte. Sans `parution` (profils complet et wip),
-- rien ne change.

local parution = nil

-- Numéro du jour d'un lien vers une page de jour, ou nil.
local function jour_du_lien(cible)
  local numero = cible:match("^[%./]*jours/(%d%d)%-[^/]*%.qmd") or cible:match("^(%d%d)%-[^/]*%.qmd")
  return numero and tonumber(numero)
end

local function a_venir(lien)
  local jour = jour_du_lien(lien.target)
  return jour ~= nil and jour > parution
end

local function premiere_cellule_a_venir(ligne)
  local cellule = ligne.cells[1]
  if not cellule then
    return false
  end
  local trouve = false
  pandoc.walk_block(pandoc.Div(cellule.contents), {
    Link = function(lien)
      if a_venir(lien) then
        trouve = true
      end
    end,
  })
  return trouve
end

return {
  {
    Meta = function(meta)
      if meta.parution ~= nil then
        parution = tonumber(pandoc.utils.stringify(meta.parution))
      end
    end,
  },
  {
    Table = function(tableau)
      if not parution then
        return nil
      end
      for _, corps in ipairs(tableau.bodies) do
        local gardees = pandoc.List()
        for _, ligne in ipairs(corps.body) do
          if not premiere_cellule_a_venir(ligne) then
            gardees:insert(ligne)
          end
        end
        corps.body = gardees
      end
      return tableau
    end,
    Link = function(lien)
      if parution and a_venir(lien) then
        return lien.content
      end
    end,
  },
}
