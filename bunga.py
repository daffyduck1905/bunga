import os
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Galeri klasörü: static/gallery/eserler/
GALLERY_DIR = os.path.join(BASE_DIR, "static", "gallery", "eserler")
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

artist = {
    "name": "Fatih Bakır",
    "title": "Geleneksel Ahşap Oyma ve Altın Varak Sanatçısı",
    "email": "fatihbakir23@outlook.com",
    "profile_photo": ""  # istersen sonra kullanırsın
}


def list_gallery_paths():
    """
    static/gallery/eserler içindeki görselleri
    template'lerde url_for('static', filename=path) ile kullanılacak şekilde döndürür.
    Örn: 'gallery/eserler/001.jpg'
    """
    if not os.path.isdir(GALLERY_DIR):
        return []

    files = []
    for fn in os.listdir(GALLERY_DIR):
        ext = os.path.splitext(fn.lower())[1]
        if ext in ALLOWED_EXT:
            files.append(fn)

    files.sort()
    return [f"gallery/eserler/{f}" for f in files]


@app.route("/")
def index():
    image_paths = list_gallery_paths()
    featured_paths = image_paths[:6]  # index.html'deki blok bunu bekliyor
    return render_template("index.html", artist=artist, featured_paths=featured_paths)


@app.route("/galeri")
def galeri():
    image_paths = list_gallery_paths()
    # galeri.html'i de buna göre yazacağız: featured değil image_paths
    return render_template("galeri.html", artist=artist, image_paths=image_paths)


@app.route("/eser/<filename>")
def eser_detay(filename):
    # filename sadece dosya adı olmalı: 001.jpg gibi
    ext = os.path.splitext(filename.lower())[1]
    if ext not in ALLOWED_EXT:
        abort(404)

    full_path = os.path.join(GALLERY_DIR, filename)
    if not os.path.isfile(full_path):
        abort(404)

    # template içinde url_for('static', filename='gallery/eserler/' ~ filename) yapacağız
    return render_template("eserdetay.html", artist=artist, filename=filename)


@app.route("/hakkinda")
def about():
    return render_template("about.html", artist=artist)


@app.route("/iletisim", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return redirect(url_for("contact", sent="1"))
    return render_template("contact.html", artist=artist)


if __name__ == "__main__":
    app.run(debug=True)
