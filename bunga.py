from flask import Flask, render_template, request, redirect, url_for
from slugify import slugify

app = Flask(__name__)

# Fake data for artworks
eserler = [
    {
        'id': 1,
        'title': 'Fırın',
        'year': 1993,
        'technique': 'Tuvale yağlı boya',
        'size': '80x110 cm',
        'image_url': 'https://via.placeholder.com/800x600?text=Firin',
        'description': 'Bu eser, sanatçının köy hayatı temalarını yansıtan bir çalışma.',
        'slug': 'firin-1993'
    },
    {
        'id': 2,
        'title': 'Anaların Bekleyişi',
        'year': 2017,
        'technique': 'Tuvale yağlı boya',
        'size': '70x100 cm',
        'image_url': 'https://via.placeholder.com/800x600?text=Analarin+Bekleyisi',
        'description': 'Annelerin bekleyişini konu alan duygusal bir tablo.',
        'slug': 'analarin-bekleyisi-2017'
    }
]

artist = {
    'name': 'Fatih Bakır',
    'title': 'Siyaset Bilimci & Geleneksel El Sanatları Sanatçısı',
    'bio_long': '...',
    'exhibitions': []
}

# HOME
@app.route("/")
def index():
    return render_template("index.html", eserler=eserler, artist=artist)

# GALERİ
@app.route("/galeri")
def galeri():
    return render_template("galeri.html", eserler=eserler)

# ESER DETAY
@app.route("/eser/<slug>")
def eser_detay(slug):
    eser = next((e for e in eserler if e["slug"] == slug), None)
    if not eser:
        return "Eser bulunamadı", 404
    return render_template("eserdetay.html", eser=eser)

# HAKKINDA
@app.route("/hakkinda")
def about():
    return render_template("about.html", artist=artist)

# İLETİŞİM
@app.route("/iletisim", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        return redirect(url_for("index"))
    return render_template("contact.html")
