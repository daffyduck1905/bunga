# flask_app.py


from flask import Flask
from slugify import slugify

app = Flask(__name__)

from flask import Flask, render_template, request, redirect, url_for
from slugify import slugify  # Install slugify if needed, but for PythonAnywhere, assume it's available or use manual slug

app = Flask(__name__)
@app.route("/test")
def test():
    return "CALISIYOR"


# Fake data for artworks inspired by İbrahim Balaban
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
    },
    {
        'id': 3,
        'title': 'Soyut Figürler',
        'year': 1959,
        'technique': 'Kağıt üzerine karışık teknik',
        'size': '15x20 cm',
        'image_url': 'https://via.placeholder.com/800x600?text=Soyut+Figurler',
        'description': 'Soyut figürlerle dolu erken dönem bir eser.',
        'slug': 'soyut-figurler-1959'
    },
    # Add more if needed
]

# Artist bio data
artist = {
    'name': 'İbrahim Balaban',
    'bio': 'İbrahim Balaban (1921-2019), Türk ressam ve yazar. Bursa’da doğdu, hapishane yıllarında Nazım Hikmet’in etkisiyle resim yapmaya başladı. Köy hayatı, folklor ve toplumsal gerçekçilik temaları işledi.',
    'exhibitions': ['İz Bırakanlar - II, Galeri Soyut, 2020', 'Diğer sergiler...'],
    'profile_photo': 'https://via.placeholder.com/300x300?text=Profile'
}
# artist sözlüğünü bu şekilde güncelle
artist = {
    'name': 'Fatih Bakır',
    'title': 'Siyaset Bilimci & Geleneksel El Sanatları Sanatçısı',
    'bio_long': """
    1983 yılında Almanya'nın Remscheid kentinde dünyaya gelen Fatih Bakır, çocukluk yıllarını Avrupa'nın kültürel atmosferinde geçirdikten sonra ana vatanı Elazığ'a, ata topraklarına dönüş yapmıştır. Hayatının bir döneminde hayvancılıkla da uğraşarak doğanın ve toprağın yalın diliyle bağ kuran Bakır, akademik eğitimini Siyaset Bilimi ve Kamu Yönetimi alanında tamamlamıştır.

    Eğitim aldığı alanda kendini akademik ve entelektüel olarak aşırı derecede geliştirmesine rağmen, içindeki sanat tutkusu onu bambaşka bir yola sevk etmiştir. Demirci bir babanın ocaktaki ateşle imtihanını ve yönetmen bir ağabeyin dünyayı yorumlama biçimini izleyerek büyüyen sanatçı, bu birikimi kendi zanaatıyla birleştirmiştir. Mimar Sinan Üniversitesi öğretim üyesi Dr. Cemal Arslan gibi kıymetli hocalardan aldığı eğitimlerle, el becerisini akademik bir disiplinle taçlandırmıştır.

    Son 15 yıldır Elazığ’daki bodrum katındaki atölyesinde, sadece ahşaba şekil vermekle kalmayıp ona altın varakla ruh üflemektedir. Atölyesinde sadık dostu papağanı 'Yakup' ile birlikte yürüttüğü çalışmalar, bugün sadece yerel bir başarı değil; Cumhurbaşkanlığı Külliyesi’nden Katar saraylarına, Rusya’dan Almanya ve Azerbaycan’a kadar uzanan küresel bir imzanın öyküsüdür. Siyaset biliminin analitik zekasını, el sanatlarının kadim sabrıyla birleştiren Fatih Bakır, bugün Türkiye’yi uluslararası arenada temsil eden nadide sanatçılardan biridir.
    """,
    'exhibitions': [
        'Cumhurbaşkanlığı Külliyesi Özel Proje Çalışmaları',
        'Uluslararası Altın Varak ve Restorasyon Koleksiyonu',
        'Katar & Körfez Ülkeleri Sanat İhracat Projeleri',
        'Almanya ve Rusya Özel Koleksiyon Seçkileri'
    ]
}

# Home page
@app.route('/')
def index():
    son_eklenen = eserler[-3:]  # Last 3 artworks
    return render_template('index.html', son_eklenen=son_eklenen, artist=artist)

# Gallery page
@app.route('/galeri')
def galeri():
    return render_template('galeri.html', eserler=eserler)

# Artwork detail page
@app.route('/eser/<slug>')
def eser_detay(slug):
    eser = next((e for e in eserler if e['slug'] == slug), None)
    if eser:
        return render_template('eser_detay.html', eser=eser)
    return 'Eser bulunamadı', 404

# About page
@app.route('/hakkinda')
def about():
    return render_template('about.html', artist=artist)

# Contact page
@app.route('/iletisim', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Simple form handling (no real sending, just redirect)
        return redirect(url_for('index'))
    return render_template('contact.html')

if __name__ == '__main__':
    app.run(debug=True)