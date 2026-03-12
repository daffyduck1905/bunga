# bunga.py

from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, abort, request
from werkzeug.utils import secure_filename


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TEMPLATES_DIR = BASE_DIR / "templates"

GALLERY_DIR = STATIC_DIR / "gallery" / "eserler"
REFERANS_DIR = STATIC_DIR / "referanslar"

ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def list_gallery_images() -> list[str]:

    if not GALLERY_DIR.exists():
        return []

    files: list[str] = []

    for p in GALLERY_DIR.iterdir():

        if p.is_file() and p.suffix.lower() in ALLOWED_EXTS:

            files.append(p.name)

    files.sort(key=lambda x: x.lower())

    return files


def build_featured_paths(images: list[str], limit: int = 6) -> list[str]:

    featured = images[:limit]

    return [f"gallery/eserler/{name}" for name in featured]


def create_app() -> Flask:

    app = Flask(
        __name__,
        template_folder=str(TEMPLATES_DIR),
        static_folder=str(STATIC_DIR),
    )

    ARTIST = {
        "name": "Fatih Bakır",
        "title": "Ahşap Oyma & Altın Varak",
        "email": "fatihbakir23@outlook.com",
        "instagram": "fhtbkr",
        "phone": "",
        "location": "",
    }

    @app.context_processor
    def inject_globals():

        lang = request.args.get("lang", "tr")

        return {
            "artist": ARTIST,
            "asset_version": datetime.utcnow().strftime("%Y%m%d%H%M%S"),
            "lang": lang
        }

    @app.get("/")
    def index():

        images = list_gallery_images()

        featured_paths = build_featured_paths(images, limit=6)

        return render_template(
            "index.html",
            featured_paths=featured_paths
        )

    @app.get("/galeri")
    def galeri():

        images = list_gallery_images()

       
        images = [img for img in images if img != "104.png"]

        return render_template(
            "galeri.html",
            images=images
        )
    @app.get("/eser/<path:filename>")
    def eser_detay(filename: str):

        safe = secure_filename(filename)

        if not safe:
            abort(404)

        full = GALLERY_DIR / safe

        if not full.exists() or not full.is_file():
            abort(404)

        images = list_gallery_images()

        return render_template(
            "eserdetay.html",
            filename=safe,
            images=images
        )


    @app.get("/referanslar")
    def referanslar():

        return render_template("referanslar.html")

    @app.get("/hakkinda")
    def about():

        return render_template("about.html")

    @app.get("/iletisim")
    def contact():

        return render_template("contact.html")

    @app.errorhandler(404)
    def page_not_found(e):

        return (
            """
            <!doctype html>
            <html lang="tr">
            <head>
              <meta charset="utf-8"/>
              <meta name="viewport" content="width=device-width,initial-scale=1"/>
              <title>404</title>
              <style>
                body{background:#0b0b0d;color:#fff;font-family:Arial;display:flex;min-height:100vh;align-items:center;justify-content:center}
                a{color:#D4AF37;text-decoration:none}
              </style>
            </head>
            <body>
              <div style="text-align:center;max-width:520px;padding:24px">
                <h1 style="margin:0 0 12px">404</h1>
                <div style="opacity:.8;line-height:1.6;margin-bottom:14px">
                  Aradığınız sayfa bulunamadı.
                </div>
                <a href="/">Ana sayfaya dön</a>
              </div>
            </body>
            </html>
            """,
            404,
        )

    return app


app = create_app()

if __name__ == "__main__":

    app.run(debug=True)