import os
from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Galeri: static/gallery/eserler/
GALLERY_DIR = os.path.join(BASE_DIR, "static", "gallery", "eserler")
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

artist = {
    "name": "Fatih Bakır",
    "title": "Geleneksel El Sanatları Sanatçısı • Oyma & Altın Varak",
    "email": "fatihbakir23@outlook.com",  # burada mailini yazıyoruz
    "location": "Türkiye",
    "bio_long": (
        "Fatih Bakır, ahşap oyma ve altın varak uygulamalarını bir araya getirerek "
        "zamansız motifleri modern bir estetikle yorumlayan geleneksel el sanatları sanatçısıdır.\n\n"
        "Her eser; sabır, detay ve ustalık gerektiren katmanlı bir üretim sürecinin sonucudur. "
        "Doğal ahşabın karakteri, oyma işçiliğiyle şekillenir; altın varak ise esere tarihî bir ihtişam katar.\n\n"
        "EĞİTİM:\n"
        "• Eskişehir Üniversitesi — Kamu Yönetimi\n"
    ),
    "highlights": [
        "Ahşap Oyma (rölyef & derin oyma)",
        "Altın Varak Uygulama (klasik & modern yüzeyler)",
        "Kişiye özel tasarım (isim, arma, motif, tablo)"
    ]
}


def list_gallery_images():
    """Klasördeki görselleri dosya adı olarak döndürür."""
    if not os.path.isdir(GALLERY_DIR):
        return []
    files = []
    for filename in os.listdir(GALLERY_DIR):
        ext = os.path.splitext(filename.lower())[1]
        if ext in ALLOWED_EXT:
            files.append(filename)
    files.sort()
    return files


@app.route("/")
def index():
    images = list_gallery_images()
    featured = images[:8]
    return render_template("index.html", artist=artist, featured=featured)


@app.route("/galeri")
def galeri():
    images = list_gallery_images()
    return render_template("galeri.html", artist=artist, images=images)


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


@app.route("/iletisim", methods=["GET", "POST"])
def contact():
    # Formu saklamıyoruz / mail atmıyoruz. Sadece “gönderildi” feedback’i.
    if request.method == "POST":
        return redirect(url_for("contact", sent="1"))
    return render_template("contact.html", artist=artist)


if __name__ == "__main__":
    app.run(debug=True)
