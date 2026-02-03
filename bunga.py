from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# -----------------------------
# 1) ESKİ "eserler" (ister dursun)
# -----------------------------
eserler = [
    {
        'id': 1,
        'title': 'Fırın',
        'year': 1993,
        'technique': 'Ahşap oyma',
        'size': '80x110 cm',
        'image_url': 'https://via.placeholder.com/1200x800?text=Eser+1',
        'description': 'Bu eser, el işçiliği oyma detayları ve varak dokunuşlarıyla zamansız bir anlatı sunar.',
        'slug': 'firin-1993'
    },
    {
        'id': 2,
        'title': 'Anaların Bekleyişi',
        'year': 2017,
        'technique': 'Ahşap oyma + altın varak',
        'size': '70x100 cm',
        'image_url': 'https://via.placeholder.com/1200x800?text=Eser+2',
        'description': 'Geleneksel form, modern bir yorumla buluşur. Her çizgi sabırla işlenmiştir.',
        'slug': 'analarin-bekleyisi-2017'
    }
]

artist = {
    'name': 'Fatih Bakır',
    'title': 'Geleneksel El Sanatları Sanatçısı • Oyma & Altın Varak',
    'bio_long': 'Buraya sanatçının uzun biyografisi gelecek. (İstersen ben de yazayım: kısa + etkileyici)',
    'exhibitions': [],
    # about sayfası arkaplan için opsiyonel:
    'profile_photo': ''
}

# -----------------------------
# 2) FOTO KLASÖRÜNDEN OTOMATİK GALERİ
# static/gallery/eserler içine yüzlerce foto at -> otomatik görünsün
# -----------------------------
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

    files.sort()  # 001.jpg, 002.jpg gibi isimlendirme yaparsan çok iyi sıralanır
    # template’e static path olarak dönüyoruz
    return [f"gallery/eserler/{fn}" for fn in files]


# -----------------------------
# ROUTES
# -----------------------------
@app.route("/")
def index():
    # Ana sayfada öne çıkanlar: eserler listesi
    return render_template("index.html", eserler=eserler, artist=artist)


@app.route("/galeri")
def galeri():
    image_paths = list_gallery_images()
    return render_template("galeri.html", image_paths=image_paths, eserler=eserler)


@app.route("/eser/<slug>")
def eser_detay(slug):
    eser = next((e for e in eserler if e["slug"] == slug), None)
    if not eser:
        return "Eser bulunamadı", 404
    return render_template("eserdetay.html", eser=eser)


@app.route("/hakkinda")
def about():
    return render_template("about.html", artist=artist)


@app.route("/iletisim", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        # Buraya mail gönderme / DB kaydetme ekleyebiliriz
        return redirect(url_for("index"))
    return render_template("contact.html")
