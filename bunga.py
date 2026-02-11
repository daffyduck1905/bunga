import os
import time
from flask import Flask, render_template, abort, request

app = Flask(__name__)
app.config["VERSION"] = "1.0.2"

# Flask static cache'i kapat (dev gibi davran)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

GALLERY_DIR = os.path.join(BASE_DIR, "static", "gallery", "eserler")
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

artist = {
    "name": "Fatih Bakır",
    "title": "Geleneksel Ahşap Oyma ve Altın Varak Sanatçısı",
    "email": "fatihbakir23@outlook.com",
    "instagram": "fhtbkr",
    "profile_photo": ""
}


def list_gallery_files():
    """Klasördeki dosyaları her request'te yeniden okur."""
    if not os.path.isdir(GALLERY_DIR):
        return []

    files = []
    for fn in os.listdir(GALLERY_DIR):
        ext = os.path.splitext(fn.lower())[1]
        if ext in ALLOWED_EXT:
            files.append(fn)

    files.sort()
    return files


def list_gallery_paths():
    files = list_gallery_files()
    return [f"gallery/eserler/{f}" for f in files]


def compute_cache_buster():
    """
    Cache'i öldürmek için:
    - klasörde dosya varsa en yeni dosyanın mtime'ını kullan
    - yoksa time.time() kullan
    """
    try:
        files = list_gallery_files()
        if not files:
            return int(time.time())

        latest = 0
        for fn in files:
            p = os.path.join(GALLERY_DIR, fn)
            latest = max(latest, int(os.path.getmtime(p)))
        return latest
    except Exception:
        return int(time.time())


@app.after_request
def add_no_cache_headers(resp):
    """
    HTML sayfaların cache'ini kapat (tarayıcı eski sayfayı göstermesin).
    """
    resp.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    resp.headers["Pragma"] = "no-cache"
    resp.headers["Expires"] = "0"
    return resp


@app.route("/")
def index():
    featured_paths = list_gallery_paths()[:6]
    cache_buster = compute_cache_buster()
    return render_template(
        "index.html",
        artist=artist,
        featured_paths=featured_paths,
        cache_buster=cache_buster
    )


@app.route("/galeri")
def galeri():
    images = list_gallery_files()
    cache_buster = compute_cache_buster()
    return render_template(
        "galeri.html",
        artist=artist,
        images=images,
        cache_buster=cache_buster
    )


@app.route("/eser/<filename>")
def eser_detay(filename):
    ext = os.path.splitext(filename.lower())[1]
    if ext not in ALLOWED_EXT:
        abort(404)

    full_path = os.path.join(GALLERY_DIR, filename)
    if not os.path.isfile(full_path):
        abort(404)

    cache_buster = compute_cache_buster()
    return render_template(
        "eserdetay.html",
        artist=artist,
        filename=filename,
        cache_buster=cache_buster
    )


@app.route("/hakkinda")
def about():
    cache_buster = compute_cache_buster()
    return render_template("about.html", artist=artist, cache_buster=cache_buster)


@app.route("/iletisim")
def contact():
    cache_buster = compute_cache_buster()
    return render_template("contact.html", artist=artist, cache_buster=cache_buster)


if __name__ == "__main__":
    app.run(debug=True)
