import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# DEMO ESERLER KALDIRILDI ✅
# Artık galeri fotoğrafları klasörden otomatik okunuyor.
eserler = []

artist = {
    'name': 'Fatih Bakır',
    'title': 'Geleneksel El Sanatları Sanatçısı • Oyma & Altın Varak',
    'bio_long': 'Buraya sanatçının uzun biyografisi gelecek.',
    'exhibitions': [],
    'profile_photo': ''
}

# FOTOĞRAF KLASÖRÜ
# static/gallery/eserler içine yüzlerce foto at -> otomatik görünür
GALLERY_DIR = os.path.join("static", "gallery", "eserler")
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def list_gallery_images():
    if not os.path.isdir(GALLERY_DIR):
        return []
    files = []
    for name in os.listdir(GALLERY_DIR):
        ext = os.path.splitext(name.lower())[1]
        if ext in ALLOWED_EXT:
            files.append(name)
    files.sort()  # 001.jpg, 002.jpg gibi isimlerle düzgün sıralanır
    return [f"gallery/eserler/{fn}" for fn in files]


@app.route("/")
def index():
    image_paths = list_gallery_images()
    featured_paths = image_paths[:6]  # ana sayfada ilk 6 görsel
    return render_template("index.html", artist=artist, featured_paths=featured_paths)


@app.route("/galeri")
def galeri():
    image_paths = list_gallery_images()
    return render_template("galeri.html", image_paths=image_paths)


@app.route("/hakkinda")
def about():
    return render_template("about.html", artist=artist)


@app.route("/iletisim", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return redirect(url_for("index"))
    return render_template("contact.html")
