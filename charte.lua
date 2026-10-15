-- Charte graphique d'une page.
--
-- Dans l'en-tête, la couleur principale de la page, et sa variante pour le
-- thème sombre :
--
--   charte:
--     couleur: "#009099"
--     sombre: "#3fc1c9"
--
-- Elle devient la variable CSS --couleur-page (souligné, bouton de
-- téléchargement…), qui bascule avec le thème.
--
-- Dans le texte, un souligné de couleur : [texte]{.underline} prend la couleur
-- de la page, [texte]{.underline color="#ce614a"} celle qu'on lui donne.

local function chaine(valeur)
  if valeur == nil then
    return nil
  end
  return pandoc.utils.stringify(valeur)
end

local function charte(meta)
  if not meta.charte then
    return nil
  end
  local couleur = chaine(meta.charte.couleur)
  local sombre = chaine(meta.charte.sombre) or couleur
  if couleur then
    quarto.doc.include_text("in-header", string.format([[<style>
:root { --couleur-page: %s; --couleur-page-contraste: #fff; }
body.quarto-dark { --couleur-page: %s; --couleur-page-contraste: #222; }
</style>]], couleur, sombre))
  end
  return nil
end

local function souligne(contenu, couleur)
  local attr = pandoc.Attr("", {"souligne"})
  if couleur then
    attr.attributes.style = "--souligne: " .. couleur
  end
  return pandoc.Span(contenu, attr)
end

-- Pandoc lit [texte]{.underline color="…"} comme un Underline dans un Span qui
-- porte la couleur.
local function span_colore(el)
  local couleur = el.attributes.color
  if couleur and #el.content == 1 and el.content[1].t == "Underline" then
    return souligne(el.content[1].content, couleur)
  end
end

return {
  {Meta = charte},
  {Span = span_colore},
  {Underline = function(el) return souligne(el.content) end}
}
