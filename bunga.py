import os
import json
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MESSAGES_FILE = os.path.join(BASE_DIR, "messages.json")

# Galeri
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
    return [
        f"gallery/eserler/{f}"
        for f in sorted(os.listdir(GALLERY_DIR))
        if os.path.splitext(f.lower())[1] in ALLOWED_EXT
    ]


def load_messages():
    if not os.path.exists(MESSAGES_FILE):
        return []
    with open(MESSAGES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_message(data):
    messages = load_messages()
    messages.append(data)
    with open(MESSAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, ensure_ascii=False, indent=2)


@app.route("/")
def index():
    return render_template("index.html", artist=artist, featured_paths=list_gallery_images()[:6])


@app.route("/galeri")
def galeri():
    return render_template("galeri.html", image_paths=list_gallery_images())


@app.route("/hakkinda")
def about():
    return render_template("about.html", artist=artist)


@app.route("/iletisim", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = {
            "full_name": request.form.get("full_name"),
            "email": request.form.get("email"),
            "phone": request.form.get("phone"),
            "message": request.form.get("message"),
            "date": datetime.now().strftime("%d.%m.%Y %H:%M")
        }
        save_message(data)
        return redirect(url_for("contact", sent="1"))

    return render_template("contact.html")


# 🔒 GİZLİ SAYFA – SADECE SEN
@app.route
