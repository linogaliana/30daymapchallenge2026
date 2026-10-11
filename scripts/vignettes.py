"""Vignettes de la page d'accueil : une capture de la carte de chaque jour.

Lit le site déjà rendu (`_site/`, après `quarto render`), le sert en local, et
capture la première carte de chaque page (MapLibre ou Observable Plot), écrite
en WebP dans `jours/vignettes/`. Les pages sans carte sont ignorées.

    uv run --with playwright --with pillow python scripts/vignettes.py

Chromium : celui de Playwright (`uv run --with playwright playwright install
chromium`), ou un autre binaire désigné par la variable `CHROME`.
"""

import functools
import http.server
import io
import os
import pathlib
import threading

from PIL import Image
from playwright.sync_api import sync_playwright

RACINE = pathlib.Path(__file__).resolve().parent.parent
SITE = RACINE / "_site"
SORTIE = RACINE / "jours" / "vignettes"
LARGEUR = 800
CARTES = ".maplibregl-map, svg[class^='plot']"
# Rang de la carte à capturer quand ce n'est pas la première de la page.
RANG = {}


class Silencieux(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


def serveur(dossier):
    gestion = functools.partial(Silencieux, directory=dossier)
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), gestion)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def capturer(navigateur, url):
    page = navigateur.new_page(
        viewport={"width": 1400, "height": 1000}, device_scale_factor=2, color_scheme="light"
    )
    page.goto(url, wait_until="networkidle", timeout=180_000)
    page.add_style_tag(content=".maplibregl-ctrl-top-right { display: none }")
    page.wait_for_timeout(5000)
    cartes = [
        e
        for e in page.query_selector_all(CARTES)
        if (b := e.bounding_box()) and b["width"] > 300 and b["height"] > 250
    ]
    image = None
    if cartes:
        carte = cartes[min(RANG.get(url.rsplit("/", 1)[-1], 0), len(cartes) - 1)]
        carte.scroll_into_view_if_needed()
        page.wait_for_timeout(1500)
        image = carte.screenshot()
    page.close()
    return image


def main():
    SORTIE.mkdir(exist_ok=True)
    srv = serveur(SITE)
    base = f"http://127.0.0.1:{srv.server_address[1]}/jours"
    options = {"executable_path": os.environ["CHROME"]} if "CHROME" in os.environ else {}
    with sync_playwright() as p:
        navigateur = p.chromium.launch(
            args=["--use-gl=swiftshader", "--enable-unsafe-swiftshader"], **options
        )
        for html in sorted((SITE / "jours").glob("[0-9][0-9]-*.html")):
            png = capturer(navigateur, f"{base}/{html.name}")
            if png is None:
                continue
            image = Image.open(io.BytesIO(png)).convert("RGB")
            image.thumbnail((LARGEUR, LARGEUR))
            image.save(SORTIE / f"{html.stem}.webp", quality=82)
        navigateur.close()
    srv.shutdown()


if __name__ == "__main__":
    main()
