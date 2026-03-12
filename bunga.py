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


def list_gallery_images():

    if not GALLERY_DIR.exists():
        return []

    files = []

    for p in GALLERY_DIR.iterdir():

        if p.is_file() and p.suffix.lower() in ALLOWED_EXTS:
            files.append(p.name)

    files.sort(key=lambda x: x.lower())

    return files


def build_featured_paths(images, limit=6):

    featured = images[:limit]

    return [f"gallery/eserler/{name}" for name in featured]


def create_app():

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

        featured_paths = build_featured_paths(images)

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
    def eser_detay(filename):

        safe = secure_filename(filename)

        if not safe:
            abort(404)

        full = GALLERY_DIR / safe

        if not full.exists():
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

    # SITEMAP

    @app.route("/sitemap.xml")
    def sitemap():

        pages = []

        base = "https://fatihbakir.pythonanywhere.com"

        pages.append(base + "/")
        pages.append(base + "/galeri")
        pages.append(base + "/referanslar")
        pages.append(base + "/hakkinda")
        pages.append(base + "/iletisim")

        images = list_gallery_images()

        for img in images:
            pages.append(base + "/eser/" + img)

        xml = '<?xml version="1.0" encoding="UTF-8"?>'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'

        for page in pages:
            xml += "<url>"
            xml += f"<loc>{page}</loc>"
            xml += "</url>"

        xml += "</urlset>"

        return xml, 200, {"Content-Type": "application/xml"}

    # IMAGE SITEMAP

    @app.route("/image-sitemap.xml")
    def image_sitemap():

        base = "https://fatihbakir.pythonanywhere.com"

        images = list_gallery_images()

        xml = '<?xml version="1.0" encoding="UTF-8"?>'
        xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
        xml += 'xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'

        for img in images:

            xml += "<url>"
            xml += f"<loc>{base}/eser/{img}</loc>"
            xml += "<image:image>"
            xml += f"<image:loc>{base}/static/gallery/eserler/{img}</image:loc>"
            xml += "<image:title>Fatih Bakır Ahşap Oyma Sanat Eseri</image:title>"
            xml += "</image:image>"
            xml += "</url>"

        xml += "</urlset>"

        return xml, 200, {"Content-Type": "application/xml"}

    # ROBOTS

    @app.route("/robots.txt")
    def robots():

        robots = f"""
User-agent: *
Allow: /

Sitemap: https://fatihbakir.pythonanywhere.com/sitemap.xml
Sitemap: https://fatihbakir.pythonanywhere.com/image-sitemap.xml
"""

        return robots, 200, {"Content-Type": "text/plain"}

    # GOOGLE VERIFY

    @app.route("/google3TMT0Wq-GzRmG9wOobyB4lPHrsudjP1v6-QiLX_3A.html")
    def google_verify():
        return "google-site-verification: google3TMT0Wq-GzRmG9wOobyB4lPHrsudjP1v6-QiLX_3A.html"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)