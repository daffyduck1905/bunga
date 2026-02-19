import os
import time
from flask import Flask, render_template, abort, send_from_directory, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Galeri klasörü
GALLERY_DIR = os.path.join(BASE_DIR, "static", "gallery", "eserler")
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}


# ----------------------------
# GLOBAL: Asset version (cache kırma)
# ----------------------------
# Web Reload yaptığında otomatik değişir -> tarayıcı eski resmi tutamaz
app.config["ASSET_VERSION"] = str(int(time.time()))


@app.context_processor
def inject_globals():
    return {
        "asset_version": app.config["ASSET_VERSION"]
    }


# ----------------------------
# Sanatçı bilgileri
# ----------------------------
artist = {
    "name": "Fatih Bakır",
    "title": "Geleneksel Ahşap Oyma & Altın Varak Sanatçısı",
    "university": "Eskişehir Üniversitesi",
    "department": "Kamu Yönetimi",
    "bio_long": (
        "Fatih Bakır, geleneksel ahşap oyma sanatını çağdaş bir estetik anlayışla "
        "yorumlayan, eserlerinde sabır, emek ve ustalığı merkeze alan bir sanatçıdır.\n\n"
        "Ahşabı yalnızca bir malzeme olarak değil, geçmişle bugün arasında kurulan yaşayan bir bağ olarak ele alır. "
        "Zaman içerisinde ahşap oyma sanatını derinlemesine öğrenmiş, bu kadim zanaatı altın varak tekniğiyle birleştirerek "
        "kendine özgü bir ifade dili geliştirmiştir.\n\n"
        "Çalışmalarının tamamı el işçiliğiyle üretilir. Seri üretim anlayışından uzak duran sanatçı, "
        "her parçayı tek ve özgün bir eser olarak ele alır. Altın varak uygulamaları ise eserlere zamansız bir asalet kazandırır."
    ),
}

CONTACT = {
    "email": "fatihbakir23@outlook.com",
    "instagram_handle": "fhtbkr",
    "instagram_url": "https://www.instagram.com/fhtbkr/",
}


def list_gallery_images():
    """
    static/gallery/eserler içindeki görselleri listeler.
    ZIP veya başka dosyaları asla almaz.
    """
    if not os.path.isdir(GALLERY_DIR):
        return []

    files = []
    for filename in os.listdir(GALLERY_DIR):
        # gizli dosyaları alma
        if filename.startswith("."):
            continue

        ext = os.path.splitext(filename.lower())[1]
        if ext in ALLOWED_EXT:
            files.append(filename)

    # alfabetik sırala (001.png, 002.png gibi)
    files.sort()

    # template'lere relative path döndür (url_for ile kullanılacak)
    return [f"gallery/eserler/{f}" for f in files]


def safe_filename_from_gallery(rel_path: str) -> str:
    """
    /eser/<filename> için güvenlik:
    sadece gallery/eserler içinde bulunan gerçek dosyalar kabul.
    """
    # rel_path "gallery/eserler/XXX.png" gibi gelir
    if not rel_path.startswith("gallery/eserler/"):
        return ""

    filename = rel_path.replace("gallery/eserler/", "", 1)
    if not filename:
        return ""

    # sadece izinli uzantılar
    ext = os.path.splitext(filename.lower())[1]
    if ext not in ALLOWED_EXT:
        return ""

    abs_path = os.path.join(GALLERY_DIR, filename)
    if not os.path.isfile(abs_path):
        return ""

    return filename


# ----------------------------
# ROUTES
# ----------------------------

@app.route("/")
def index():
    image_paths = list_gallery_images()
    featured_paths = image_paths[:6]  # ana sayfada 6 tane
    return render_template(
        "index.html",
        artist=artist,
        featured_paths=featured_paths
    )


@app.route("/galeri")
def galeri():
    image_paths = list_gallery_images()
    return render_template("galeri.html", image_paths=image_paths, artist=artist)


@app.route("/eser/<path:rel_path>")
def eser_detay(rel_path):
    filename = safe_filename_from_gallery(rel_path)
    if not filename:
        abort(404)

    image_paths = list_gallery_images()
    current_rel = f"gallery/eserler/{filename}"

    # prev/next için index bul
    try:
        idx = image_paths.index(current_rel)
    except ValueError:
        abort(404)

    prev_path = image_paths[idx - 1] if idx > 0 else None
    next_path = image_paths[idx + 1] if idx < len(image_paths) - 1 else None

    return render_template(
        "eserdetay.html",
        image_path=current_rel,
        prev_path=prev_path,
        next_path=next_path,
        artist=artist
    )


@app.route("/hakkinda")
def about():
    return render_template("about.html", artist=artist)

@app.route("/iletisim")
def contact():
    return render_template("contact.html", artist=artist, contact=CONTACT)



# (Opsiyonel) logo/fav dosyaları için ayrıca route gerek yok; static zaten serve ediyor.

if __name__ == "__main__":
    app.run(debug=True)
