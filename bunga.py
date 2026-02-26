import os
from flask import Flask, render_template, request, redirect, url_for, abort
TEST_MARK = "RUNNING-FILE-20260226"

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Galeri klasörü: static/gallery/eserler/
GALLERY_DIR = os.path.join(BASE_DIR, "static", "gallery", "eserler")
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

artist = {
    "name": "Fatih Bakır",
    "title": "Geleneksel Ahşap Oyma ve Altın Varak Sanatçısı",
    "email": "fatihbakir23@outlook.com",
    "profile_photo": ""
}


def list_gallery_paths():
    """
    static/gallery/eserler içindeki görselleri,
    url_for('static', filename=...) ile kullanılacak relative path olarak döndürür.
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


def safe_filename(filename: str) -> str | None:
    """
    Sadece dosya adını kabul eder (001.jpg gibi).
    Path traversal engeller.
    """
    if not filename or "/" in filename or "\\" in filename:
        return None
    ext = os.path.splitext(filename.lower())[1]
    if ext not in ALLOWED_EXT:
        return None
    return filename


@app.route("/")
def index():
    image_paths = list_gallery_paths()
    featured_paths = image_paths[:6]  # ana sayfada 6 tane göster
    return render_template(
        "index.html",
        artist=artist,
        featured_paths=featured_paths
    )


@app.route("/galeri")
def galeri():
    image_paths = list_gallery_paths()
    return render_template(
        "galeri.html",
        artist=artist,
        image_paths=image_paths
    )


@app.route("/eser/<filename>")
def eser_detay(filename):
    filename = safe_filename(filename)
    if not filename:
        abort(404)

    full_path = os.path.join(GALLERY_DIR, filename)
    if not os.path.isfile(full_path):
        abort(404)

    image_url = url_for("static", filename=f"gallery/eserler/{filename}")
    return render_template(
        "eserdetay.html",
        artist=artist,
        filename=filename,
        image_url=image_url
    )


@app.route("/hakkinda")
def about():
    return render_template("about.html", artist=artist)


@app.route("/iletisim", methods=["GET", "POST"])
def contact():
    sent = request.args.get("sent") == "1"
    if request.method == "POST":
        # Formu gerçek mail göndermeye bağlamadıysan şimdilik sadece "gönderildi" sayfasına dön.
        return redirect(url_for("contact", sent="1"))

    return render_template("contact.html", artist=artist, sent=sent)


if __name__ == "__main__":
    app.run(debug=True)