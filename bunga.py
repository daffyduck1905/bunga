import os
import smtplib
import traceback
from datetime import datetime
from email.mime.text import MIMEText
from email.utils import formataddr
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Galeri
GALLERY_DIR = os.path.join(BASE_DIR, "static", "gallery", "eserler")
ALLOWED_EXT = {".jpg", ".jpeg", ".png", ".webp"}

# Debug log dosyası (PythonAnywhere'de kesin çalışır)
MAIL_DEBUG_LOG = os.path.join(BASE_DIR, "mail_debug.log")

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


def _log_mail_debug(text: str) -> None:
    try:
        with open(MAIL_DEBUG_LOG, "a", encoding="utf-8") as f:
            f.write(text + "\n")
    except Exception:
        # Log yazamazsa bile site patlamasın
        pass


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
    WSGI içinde set edilen env'ler:
      SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS
    """
    smtp_host = os.environ.get("SMTP_HOST", "smtp-mail.outlook.com")
    smtp_port = int(os.environ.get("SMTP_PORT", "587"))
    smtp_user = os.environ.get("SMTP_USER")  # fatihbakir23@outlook.com
    smtp_pass = os.environ.get("SMTP_PASS")  # şifre / app password

    # Env kontrolünü logla (şifreyi yazmadan!)
    _log_mail_debug(
        f"[{datetime.now().isoformat()}] ENV CHECK | HOST={smtp_host} PORT={smtp_port} "
        f"USER={'SET' if smtp_user else 'MISSING'} PASS={'SET' if smtp_pass else 'MISSING'}"
    )

    if not smtp_user or not smtp_pass:
        raise RuntimeError("SMTP_USER / SMTP_PASS tanımlı değil (WSGI içinde set edilmemiş olabilir).")

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
    msg["Reply-To"] = email

    # STARTTLS (587)
    with smtplib.SMTP(smtp_host, smtp_port, timeout=25) as server:
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
            _log_mail_debug(f"[{datetime.now().isoformat()}] SEND OK | from_form={email}")
            return redirect(url_for("contact", sent="1"))
        except Exception as e:
            _log_mail_debug(f"[{datetime.now().isoformat()}] SEND FAIL | {repr(e)}")
            _log_mail_debug(traceback.format_exc())
            return redirect(url_for("contact", sent="0"))

    return render_template("contact.html")


if __name__ == "__main__":
    app.run(debug=True)
