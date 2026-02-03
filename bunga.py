import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ======================================================
# TEMEL DİZİN (PythonAnywhere uyumlu)
# ======================================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ======================================================
# GALERİ AYARLARI
# ======================================================
GALLERY_DIR = os.path.join(BASE_DIR, "static", "gallery", "eserler")
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

# ======================================================
# SANATÇI BİLGİLERİ
# ======================================================
artist = {
    "name": "Fatih Bakır",
    "title": "Geleneksel El Sanatları Sanatçısı • Oyma & Altın Varak",
    "bio_long": "Buraya sanatçının uzun biyografisi gelecek.",
    "exhibitions": [],
    "profile_photo": ""
}

# ======================================================
# GALERİDEN FOTO OKUMA FONKSİYONU
# ======================================================
def list_gallery_images():
    if not os.path.isdir(GALLERY_DIR):
        return []

    files = []
    for filename in os.listdir(GALLERY_DIR):
        ext = os.path.splitext(filename.lower())[1]
        if ext in ALLOWED_EXT:
            files.append(filename)

    files.sort()  # 001.jpg, 002.jpg, 003.jpg sıralı gelir
    return [f"gallery/eserler/{f}" for f in files]

# ======================================================
# ROUTES
# ======================================================

@app.route("/")
def index():
    image_paths = list_gallery_images()
    featured_paths = image_paths[:6]  # ana sayfada ilk 6 foto
    return render_template(
        "index.html",
        artist=artist,
        featured_paths=featured_paths
    )


@app.route("/galeri")
def galeri():
    image_paths = list_gallery_images()
    return render_template(
        "galeri.html",
        image_paths=image_paths
    )


@app.route("/hakkinda")
def about():
    return render_template(
        "about.html",
        artist=artist
    )


@app.route("/iletisim", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # form işlemi ileride eklenebilir
        return redirect(url_for("index"))

    return render_template("contact.html")


# ======================================================
# UYGULAMA BAŞLATMA (LOCAL İÇİN)
# PythonAnywhere bunu kullanmaz ama sorun da olmaz
# ======================================================
if __name__ == "__main__":
    app.run(debug=True)
