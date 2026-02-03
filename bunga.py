import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ✅ Session için şart (rastgele bir şey yap)
app.secret_key = "COK_GIZLI_BIR_SEY_YAZ_123456"

# ✅ Admin şifresi (istersen değiştir)
ADMIN_PASSWORD = "1234"

# Mesajların kaydedileceği dosya
MESSAGES_FILE = os.path.join(BASE_DIR, "messages.json")

# Galeri klasörü
GALLERY_DIR = os.path.join(BASE_DIR, "static", "gallery", "eserler")
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

artist = {
    "name": "Fatih Bakır",
    "title": "Geleneksel El Sanatları Sanatçısı • Oyma & Altın Varak",
    "bio_long": "",
    "exhibitions": [],
    "profile_photo": ""
}


def list_gallery_images():
    if not os.path.isdir(GALLERY_DIR):
        return []
    files = []
    for f in os.listdir(GALLERY_DIR):
        if os.path.splitext(f.lower())[1] in ALLOWED_EXT:
            files.append(f)
    files.sort()
    return [f"gallery/eserler/{f}" for f in files]


def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    try:
        with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except Exception:
        return []


def save_message(msg: dict):
    messages = load_messages()
    messages.append(msg)
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    image_paths = list_gallery_images()
    featured_paths = image_paths[:6]
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
        full_name = (request.form.get("full_name") or "").strip()
        email = (request.form.get("email") or "").strip()
        phone = (request.form.get("phone") or "").strip()
        message = (request.form.get("message") or "").strip()

        save_message({
            "full_name": full_name,
            "email": email,
            "phone": phone,
            "message": message,
            "date": datetime.now().strftime("%d.%m.%Y %H:%M")
        })

        return redirect(url_for("contact", sent="1"))

    return render_template("contact.html")


# ==========================
# ✅ ADMIN (ŞİFRELİ) BÖLÜM
# ==========================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        password = request.form.get("password") or ""
        if password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_messages"))
        return render_template("admin_login.html", error="Şifre yanlış")

    return render_template("admin_login.html")


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("index"))


@app.route("/admin/mesajlar")
def admin_messages():
    # ✅ giriş yoksa login'e at
    if not session.get("admin"):
        return redirect(url_for("admin_login"))

    messages = load_messages()[::-1]  # en yeni üstte
    return render_template("admin_messages.html", messages=messages)


if __name__ == "__main__":
    app.run(debug=True)
