import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Galeri
GALLERY_DIR = os.path.join(BASE_DIR, "static", "gallery", "eserler")
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

# Sanatçı
artist = {
    "name": "Fatih Bakır",
    "title": "Geleneksel El Sanatları Sanatçısı • Oyma & Altın Varak",
    "bio_long": "Buraya sanatçının uzun biyografisi gelecek.",
    "exhibitions": [],
    "profile_photo": ""
}

# Mail hedefi
DEST_EMAIL = "fatihbakir23@outlook.com"


def list_gallery_images():
    if not os.path.isdir(GALLERY_DIR):
        return []
    files = []
    for filename in os.listdir(GALLERY_DIR):
        ext = os.path.splitext(filename.lower())[1]
        if ext in ALLOWED_EXT:
            files.append(filename)
    files.sort()
    return [f"gallery/eserler/{f}" for f in files]


def send_contact_email(full_name: str, email: str, phone: str, message: str) -> None:
    """
    Outlook SMTP ile mail gönderir.
    Gerekli env değişkenleri:
      SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS
    """
    smtp_host = os.environ.get("SMTP_HOST", "smtp-mail.outlook.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")  # ör: fatihbakir23@outlook.com
    smtp_pass = os.environ.get("SMTP_PASS")  # şifre / app password

    if not smtp_user or not smtp_pass:
        raise RuntimeError("SMTP_USER / SMTP_PASS tanımlı değil.")

    subject = f"Yeni İletişim Formu: {full_name}"
    body = (
        "Siteden yeni bir iletişim formu geldi.\n\n"
        f"Ad Soyad : {full_name}\n"
        f"E-mail  : {email}\n"
        f"Telefon : {phone}\n\n"
        "Mesaj:\n"
        f"{message}\n"
    )

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = formataddr(("Fatih Bakır Sitesi", smtp_user))
    msg["To"] = DEST_EMAIL
    msg["Reply-To"] = email  # Yanıtla'ya basınca kullanıcı maili gelsin

    # STARTTLS (587) ile gönder
    with smtplib.SMTP(smtp_host, smtp_port, timeout=20) as server:
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(smtp_user, smtp_pass)
        server.sendmail(smtp_user, [DEST_EMAIL], msg.as_string())


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

        try:
            send_contact_email(full_name, email, phone, message)
            return redirect(url_for("contact", sent="1"))
        except Exception:
            # Prod'da hata detayını kullanıcıya basmayalım
            return redirect(url_for("contact", sent="0"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
