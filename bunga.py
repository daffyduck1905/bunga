import os
from flask import Flask, render_template, abort

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Galeri klasörü: static/gallery/eserler/
GALLERY_DIR = os.path.join(BASE_DIR, "static", "gallery", "eserler")
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

artist = {
    "name": "Fatih Bakır",
    "title": "Geleneksel Ahşap Oyma ve Altın Varak Sanatçısı",
    "email": "fatihbakir23@outlook.com",
}


def list_gallery_files():
    """Sadece dosya adlarını döndürür: 001.jpg gibi"""
    if not os.path.isdir(GALLERY_DIR):
        return []

    files = []
    for fn in os.listdir(GALLERY_DIR):
        ext = os.path.splitext(fn.lower())[1]
        if ext in ALLOWED_EXT:
            files.append(fn)

    files.sort()
    return files


def files_to_paths(files):
    """Dosya adlarını template'de url_for('static', filename=...) için path'e çevirir."""
    return [f"gallery/eserler/{f}" for f in files]


@app.route("/")
def index():
    files = list_gallery_files()
    featured_paths = files_to_paths(files)[:6]   # index.html bunu bekliyor
    return render_template("index.html", artist=artist, featured_paths=featured_paths)


@app.route("/galeri")
def galeri():
    files = list_gallery_files()
    # galeri.html senin sürümünde "images" listesi istiyor (dosya adı listesi)
    return render_template("galeri.html", artist=artist, images=files)


@app.route("/eser/<filename>")
def eser_detay(filename):
    ext = os.path.splitext(filename.lower())[1]
    if ext not in ALLOWED_EXT:
        abort(404)

    full_path = os.path.join(GALLERY_DIR, filename)
    if not os.path.isfile(full_path):
        abort(404)

    return render_template("eserdetay.html", artist=artist, filename=filename)


@app.route("/hakkinda")
def about():
    return render_template("about.html", artist=artist)


if __name__ == "__main__":
    app.run(debug=True)
