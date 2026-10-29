-- En-tête des pages de jour (jours/NN-theme.qmd) : le titre « J1 · Points. Les
-- maternités » s'affiche en deux temps, un surtitre « Jour 1 · Points ·
-- dimanche 1er novembre » puis le sujet « Les maternités » en grand.
--
-- Le titre de l'en-tête YAML ne change pas (onglet du navigateur, recherche,
-- calendrier de l'accueil) : un script, placé juste après l'en-tête de la page,
-- réécrit le titre affiché avant qu'il ne soit visible.

local annee = 2026
local jours = {"dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"}

-- Texte inséré en HTML, dans une chaîne JavaScript entre apostrophes.
local function echapper(texte)
  return (texte:gsub("&", "&amp;"):gsub("<", "&lt;"):gsub(">", "&gt;"):gsub("'", "&#39;"))
end

-- Texte d'une chaîne JavaScript entre apostrophes, affecté à textContent.
local function chaine_js(texte)
  return (texte:gsub("\\", "\\\\"):gsub("'", "\\'"):gsub("<", "\\u003c"))
end

function Pandoc(doc)
  local fichier = (quarto.doc.input_file or ""):gsub("\\", "/")  -- chemins Windows
  local numero = fichier:match("jours/(%d%d)%-[^/]*%.qmd$")
  if not numero or not doc.meta.title then
    return doc
  end

  -- « J25 · Is this a map? Le monde vu des Douanes » : le thème s'arrête au
  -- premier point (retiré) ou point d'interrogation (gardé).
  local titre = pandoc.utils.stringify(doc.meta.title)
  local theme, fin, sujet = titre:match("^J%d+%s*·%s*(.-)([%.%?])%s+(.+)$")
  if not theme then
    return doc
  end
  if fin == "?" then
    theme = theme .. "?"
  end

  local jour = tonumber(numero)
  local date = os.time({year = annee, month = 11, day = jour, hour = 12})
  local quantieme = jour == 1 and "1<sup>er</sup>" or tostring(jour)
  local morceaux = {
    "Jour " .. jour,
    echapper(theme),
    jours[tonumber(os.date("%w", date)) + 1] .. " " .. quantieme .. " novembre",
  }
  local surtitre = ""
  for _, morceau in ipairs(morceaux) do
    surtitre = surtitre .. "<span>" .. morceau .. "</span>"
  end

  local script = string.format([[<script>
(function () {
  const titre = document.querySelector("#title-block-header h1.title");
  if (!titre) return;
  titre.insertAdjacentHTML("beforebegin", '<p class="surtitre">%s</p>');
  titre.textContent = '%s';
})();
</script>]], surtitre, chaine_js(sujet))

  doc.blocks:insert(1, pandoc.RawBlock("html", script))
  return doc
end
