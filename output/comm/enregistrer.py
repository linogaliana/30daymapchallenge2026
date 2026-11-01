import io, pathlib, time
from PIL import Image
from playwright.sync_api import sync_playwright

SITE = "https://linogaliana.github.io/30daymapchallenge2026/"
L, H = 1280, 1000
ACCELERATION = 4
ICI = pathlib.Path(__file__).resolve().parent

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

def pause(page, duree):
    capture(page, duree)

def deplacer(page, de, vers, n=12, clic=False):
    for i in range(1, n + 1):
        t = i / n
        t = t * t * (3 - 2 * t)
        x = de[0] + (vers[0] - de[0]) * t
        y = de[1] + (vers[1] - de[1]) * t
        page.evaluate(f"window.__curseur({x}, {y}, false)")
        capture(page, 40)
    if clic:
        page.evaluate(f"window.__curseur({vers[0]}, {vers[1]}, true)")
        capture(page, 250)

def continu(page, duree, acceleration=1):
    # Captures en continu pendant `duree` ms, rejouées `acceleration` fois plus vite.
    debut = precedent = time.monotonic()
    while (time.monotonic() - debut) * 1000 < duree:
        img = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
        maintenant = time.monotonic()
        images.append((img, max(20, (maintenant - precedent) * 1000 / acceleration)))
        precedent = maintenant

def cliquer(page, element, de):
    boite = element.bounding_box()
    cible = (boite["x"] + boite["width"] / 2, boite["y"] + boite["height"] / 2)
    deplacer(page, de, cible, n=14)
    page.evaluate(f"window.__curseur({cible[0]}, {cible[1]}, true)")
    element.click()
    capture(page, 200)
    page.evaluate(f"window.__curseur({cible[0]}, {cible[1]}, false)")
    return cible

def defiler(page, de, vers, n=20):
    for i in range(1, n + 1):
        t = i / n
        t = t * t * (3 - 2 * t)
        page.evaluate(f"window.scrollTo(0, {de + (vers - de) * t})")
        capture(page, 40)

with sync_playwright() as p:
    nav = p.chromium.launch(args=["--use-gl=angle", "--enable-webgl", "--ignore-gpu-blocklist"])
    page = nav.new_page(viewport={"width": L, "height": H}, color_scheme="dark")
    page.add_init_script(CURSEUR)
    page.goto(SITE, wait_until="networkidle")
    page.wait_for_timeout(1500)
    page.evaluate("window.__curseur(900, 450, false)")
    pause(page, 3500)
    defiler(page, 0, 600, n=40)
    pause(page, 1500)
    case = page.locator("a.case[data-jour='1']").bounding_box()
    cible = (case["x"] + case["width"] / 2, case["y"] + case["height"] / 2)
    deplacer(page, (900, 450), cible, n=28)
    page.locator("a.case[data-jour='1']").hover()
    page.evaluate(f"window.__curseur({cible[0]}, {cible[1]}, false)")
    page.wait_for_timeout(400)
    capture(page, 1000)
    page.evaluate(f"window.__curseur({cible[0]}, {cible[1]}, true)")
    capture(page, 250)

    page.locator("a.case[data-jour='1']").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_selector(".maplibregl-map canvas")
    page.wait_for_timeout(4000)
    page.evaluate(f"window.__curseur({L/2}, {H/2}, false)")
    pause(page, 1800)
    haut = page.evaluate("document.querySelector('form.lecteur').getBoundingClientRect().top + window.scrollY") - 12
    defiler(page, 0, haut, n=24)
    page.wait_for_timeout(1500)
    pause(page, 1000)
    bouton = page.locator("form.lecteur button").bounding_box()
    cb = (bouton["x"] + bouton["width"] / 2, bouton["y"] + bouton["height"] / 2)
    deplacer(page, (L / 2, H / 2), cb, n=14)
    page.evaluate(f"window.__curseur({cb[0]}, {cb[1]}, true)")
    page.locator("form.lecteur button").click()
    capture(page, 250)
    page.evaluate(f"window.__curseur({cb[0] + 380}, {cb[1] + 150}, false)")
    # Lecture : captures en continu, rejouées en accéléré.
    precedent = time.monotonic()
    while page.locator("form.lecteur button").inner_text().strip().startswith("⏸"):
        img = Image.open(io.BytesIO(page.screenshot())).convert("RGB")
        maintenant = time.monotonic()
        images.append((img, max(20, (maintenant - precedent) * 1000 / ACCELERATION)))
        precedent = maintenant
    page.wait_for_timeout(800)
    pause(page, 2000)
    # Changement de territoire : Martinique, puis Mayotte.
    curseur = (cb[0] + 380, cb[1] + 150)
    for nom in ["Martinique", "Mayotte"]:
        curseur = cliquer(page, page.locator("form label", has_text=nom).first, curseur)
        continu(page, 1200)
        # Le temps de charger le fond de carte, hors enregistrement.
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(9000)
        pause(page, 1800)
    # Défilement rapide de la page : le code qui produit la carte.
    page.evaluate(f"window.__curseur({L - 60}, {H / 2}, false)")
    depart = page.evaluate("window.scrollY")
    fin = page.evaluate("document.documentElement.scrollHeight") - H
    defiler(page, depart, fin, n=80)
    pause(page, 2000)
    nav.close()

LARGEUR = 960
reduites = [(im.resize((LARGEUR, round(im.height * LARGEUR / im.width)), Image.LANCZOS), d) for im, d in images]
# GIF plus petit que la vidéo, pour rester sous les limites de poids.
LARGEUR_GIF = 720
pour_gif = [(im.resize((LARGEUR_GIF, round(im.height * LARGEUR_GIF / im.width)), Image.LANCZOS), d) for im, d in reduites]
# Durées GIF : multiples de 10 ms.
durees = [max(20, round(d / 10) * 10) for _, d in pour_gif]
cadres = [im.quantize(colors=128, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE) for im, _ in pour_gif]
cadres[0].save(ICI / "30daymapchallenge2026.gif", save_all=True, append_images=cadres[1:], duration=durees, loop=0, optimize=True, disposal=1)
import imageio.v3 as iio, numpy as np
# MP4 à 25 images/s : chaque capture répétée selon sa durée.
video = []
for im, d in reduites:
    video += [np.asarray(im)] * max(1, round(d / 40))
iio.imwrite(ICI / "30daymapchallenge2026.mp4", np.stack(video), fps=25, codec="libx264", macro_block_size=8, ffmpeg_params=["-pix_fmt", "yuv420p", "-crf", "20"])
print(len(cadres), "images,", sum(durees) / 1000, "s")
