"""Vidéo et GIF pour la comm conjointe J2 et J3.

Le site est lu en local (le J3 publié ne trouve pas ses fichiers donnees/j3/*.json) :

    cd _site && python -m http.server 8765
    uv run --with playwright --with pillow --with imageio --with imageio-ffmpeg --with numpy python output/comm/enregistrer_j2_j3.py
"""

import io, pathlib, sys
from PIL import Image
from playwright.sync_api import sync_playwright

SITE = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8765/"
L, H = 1280, 1000
ICI = pathlib.Path(__file__).resolve().parent
NOM = "j2-j3"

CURSEUR = """
window.__curseur = (x, y, clic) => {
  let c = document.getElementById('__curseur');
  if (!c) {
    c = document.createElement('div'); c.id = '__curseur';
    c.innerHTML = '<svg width="28" height="28" viewBox="0 0 24 24"><path d="M4 2 L4 20 L9 15 L12.5 22 L15.5 20.5 L12 13.8 L19 13.8 Z" fill="white" stroke="black" stroke-width="1.4" stroke-linejoin="round"/></svg>';
    c.style.cssText = 'position:fixed;z-index:999999;pointer-events:none;left:0;top:0';
    const r = document.createElement('div'); r.id = '__rond';
    r.style.cssText = 'position:fixed;z-index:999998;pointer-events:none;width:44px;height:44px;border-radius:50%;background:rgba(255,255,255,.35);display:none';
    document.body.append(r, c);
  }
  c.style.left = (x - 4) + 'px'; c.style.top = (y - 2) + 'px';
  const r = document.getElementById('__rond');
  r.style.display = clic ? 'block' : 'none';
  r.style.left = (x - 22) + 'px'; r.style.top = (y - 22) + 'px';
};
"""

images = []  # (image, durée en ms)


def capture(page, duree):
    images.append((Image.open(io.BytesIO(page.screenshot())).convert("RGB"), duree))


def deplacer(page, de, vers, n=14):
    # Le curseur dessiné et la vraie souris bougent ensemble : les bulles suivent.
    for i in range(1, n + 1):
        t = i / n
        t = t * t * (3 - 2 * t)
        x = de[0] + (vers[0] - de[0]) * t
        y = de[1] + (vers[1] - de[1]) * t
        page.mouse.move(x, y)
        page.evaluate(f"window.__curseur({x}, {y}, false)")
        capture(page, 40)
    return vers


def cliquer(page, de, vers, attente=1500):
    deplacer(page, de, vers)
    page.evaluate(f"window.__curseur({vers[0]}, {vers[1]}, true)")
    page.mouse.click(*vers)
    capture(page, 250)
    page.evaluate(f"window.__curseur({vers[0]}, {vers[1]}, false)")
    page.wait_for_timeout(attente)
    return vers


def centre(element):
    boite = element.bounding_box()
    return (boite["x"] + boite["width"] / 2, boite["y"] + boite["height"] / 2)


def defiler(page, de, vers, n=20):
    for i in range(1, n + 1):
        t = i / n
        t = t * t * (3 - 2 * t)
        page.evaluate(f"window.scrollTo(0, {de + (vers - de) * t})")
        capture(page, 40)


def masquer_semaines(page):
    # Le site local est rendu avec tous les jours : on cache les menus des semaines à venir.
    page.evaluate("""document.querySelectorAll('.navbar .nav-item').forEach((li) => {
      if (/Semaine [2-4]/.test(li.textContent)) li.remove()
    })""")


def haut(page, selecteur):
    return page.evaluate(f"document.querySelector('{selecteur}').getBoundingClientRect().top + window.scrollY")


with sync_playwright() as p:
    nav = p.chromium.launch(args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    page = nav.new_page(viewport={"width": L, "height": H}, color_scheme="dark")
    page.add_init_script(CURSEUR)

    # J2 : les navettes.
    page.goto(SITE + "jours/02-lines.html", wait_until="networkidle")
    page.wait_for_selector(".maplibregl-map canvas")
    page.wait_for_timeout(5000)
    masquer_semaines(page)
    curseur = (L / 2, H / 2)
    page.evaluate(f"window.__curseur({curseur[0]}, {curseur[1]}, false)")
    capture(page, 3000)
    y = haut(page, ".maplibregl-map") - 330
    defiler(page, 0, y, n=24)
    page.wait_for_timeout(1000)
    capture(page, 1500)
    # Paris : toutes ses navettes.
    curseur = cliquer(page, curseur, (575, 520), attente=2500)
    capture(page, 2500)
    defiler(page, y, y + 560, n=20)
    capture(page, 3000)
    curseur = cliquer(page, curseur, centre(page.get_by_role("button", name="Effacer la sélection")), attente=1000)
    # Lyon (les boutons sont sous la barre de navigation : on remonte un peu),
    # puis les navettes entre Lyon et Saint-Étienne.
    defiler(page, y + 560, y - 150, n=20)
    curseur = cliquer(page, curseur, centre(page.locator("form label", has_text="Lyon").first), attente=4000)
    defiler(page, y - 150, y, n=12)
    capture(page, 1800)
    curseur = cliquer(page, curseur, (560, 710), attente=2500)
    capture(page, 2200)
    curseur = cliquer(page, curseur, (305, 962), attente=2500)
    capture(page, 1500)
    page.evaluate(f"window.__curseur({L - 60}, {H / 2}, false)")
    defiler(page, y, y + 700, n=20)
    capture(page, 3000)

    # J3 : les parcelles.
    page.goto(SITE + "jours/03-polygons.html", wait_until="networkidle")
    page.wait_for_selector(".duo svg", timeout=60000)
    page.wait_for_timeout(2500)
    masquer_semaines(page)
    curseur = (L - 60, H / 2)
    page.evaluate(f"window.__curseur({curseur[0]}, {curseur[1]}, false)")
    capture(page, 3000)
    y = haut(page, ".duo") - 150
    defiler(page, 0, y, n=24)
    capture(page, 1500)
    # Une commune de l'ouest herbager, une des plaines de l'est.
    for cible in [(130, 560), (470, 690)]:
        curseur = cliquer(page, curseur, cible, attente=2500)
        capture(page, 2800)
    # Le recensement agricole, à la commune du siège.
    page.mouse.move(L - 60, H / 2)
    page.evaluate(f"window.__curseur({L - 60}, {H / 2}, false)")
    defiler(page, y, y + 600, n=24)
    capture(page, 4000)
    # Défilement rapide : le code qui produit les cartes.
    fin = page.evaluate("document.documentElement.scrollHeight") - H
    defiler(page, y + 600, fin, n=70)
    capture(page, 2000)
    nav.close()

LARGEUR = 960
reduites = [(im.resize((LARGEUR, round(im.height * LARGEUR / im.width)), Image.LANCZOS), d) for im, d in images]
LARGEUR_GIF = 720
pour_gif = [(im.resize((LARGEUR_GIF, round(im.height * LARGEUR_GIF / im.width)), Image.LANCZOS), d) for im, d in reduites]
durees = [max(20, round(d / 10) * 10) for _, d in pour_gif]
cadres = [im.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for im, _ in pour_gif]
cadres[0].save(ICI / f"{NOM}.gif", save_all=True, append_images=cadres[1:], duration=durees, loop=0, optimize=True, disposal=1)
import imageio.v3 as iio, numpy as np
video = []
for im, d in reduites:
    video += [np.asarray(im)] * max(1, round(d / 40))
iio.imwrite(ICI / f"{NOM}.mp4", np.stack(video), fps=25, codec="libx264", macro_block_size=8, ffmpeg_params=["-pix_fmt", "yuv420p", "-crf", "20"])
print(len(cadres), "images,", sum(durees) / 1000, "s")
