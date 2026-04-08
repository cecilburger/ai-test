import random

TEMPLATES = {
    "greeting": [
        "Halo kak 👋 Lagi cari snack apa nih? Manis atau gurih? 😄",
        "Hai kak 😊 Mau yang manis atau gurih?",
        "Halo! Ada yang bisa dibantu? 👋",
    ],
    
    "product_list": [
        (
            "GarudaFood punya banyak pilihan kak! 😄\n\n"
            "🥜 Kacang – kacang atom, kacang kulit, kacang telur\n"
            "🌽 Pilus – snack jagung bulat, ada yang pedas!\n"
            "🍫 Chocolatos – wafer stick & drink coklat\n"
            "🍪 Gery – biskuit & wafer aneka rasa\n"
            "🥔 Leo – chips kentang & singkong\n"
            "🍫 Beng-Beng – wafer bar coklat caramel\n"
            "🍮 Okky – jelly & minuman buah\n\n"
            "Mau yang mana kak? 😊"
        ),
    ],
    
    "product_ask": {
        "chocolatos": (
            "🍫 Chocolatos itu snack wafer stick coklat yang ringan & crunchy!\n\n"
            "Ada varian wafer stick & drink\n"
            "Harga mulai Rp2.000 aja kak\n\n"
            "Mau tau varian rasanya? 😄"
        ),
        "kacang": (
            "🥜 Kacang GarudaFood itu klasik & enak banget!\n\n"
            "Ada kacang atom, kacang kulit, sama kacang telur\n"
            "Tinggi protein, cocok ngemil kapan aja 💪\n\n"
            "Mau yang gurih biasa atau pedas kak?"
        ),
        "beng": (
            "🍫 Beng-Beng ENAK BANGET kak 😆🔥\n\n"
            "• Wafer crunchy berlapis\n"
            "• Caramel di tengah\n"
            "• Dibalut coklat susu\n\n"
            "Ada Original & Maxx (ukuran lebih besar)\n"
            "Best seller nih, langsung checkout aja kak 👍"
        ),
        "pilus": (
            "🌽 Pilus itu snack jagung bulat yang nagih banget!\n\n"
            "Varian: original, pedas, mie goreng\n"
            "Yang pilus mie goreng lagi hits banget sekarang 🔥\n\n"
            "Mau coba kak?"
        ),
        "leo": (
            "🥔 Leo Chips itu crunchy & addictive kak!\n\n"
            "Rasa: BBQ, Cheese, Spicy, Original, Seaweed\n"
            "Ada juga dari singkong, lebih kriuk!\n\n"
            "Suka yang rasa apa? 😄"
        ),
        "gery": (
            "🍪 Gery punya banyak pilihan kak!\n\n"
            "• Gery Malkist – crispy berlapis\n"
            "• Gery Saluut – wafer roll coklat\n"
            "• Gery Cheese – gurih keju\n\n"
            "Cocok buat cemilan atau bekal anak 😊"
        ),
        "okky": (
            "🍮 Okky Jelly seger & rendah kalori kak!\n\n"
            "Rasa: strawberry, grape, lychee, orange\n"
            "Ada juga Okky Jelly Drink yang bisa langsung diminum 🥤\n\n"
            "Favorit anak-anak nih 😄"
        ),
        "default": (
            "Ada kak! Produk GarudaFood lengkap 😊\n"
            "Mau tau lebih detail tentang produk yang mana?"
        ),
    },
    
    "product_variant": {
        "chocolatos": (
            "Chocolatos ada 2 jenis kak:\n\n"
            "🍫 Wafer Stick: coklat, cappuccino\n"
            "🥤 Drink: coklat original, dark chocolate\n\n"
            "Semua enak, tapi yang wafer stick paling hits! 😄 Mau yang mana?"
        ),
        "kacang": (
            "Kacang GarudaFood ada beberapa varian kak:\n\n"
            "🥜 Kacang Atom – original, pedas\n"
            "🥜 Kacang Kulit – original, rendang\n"
            "🥜 Kacang Telur – gurih, pedas\n\n"
            "Yang paling laris itu kacang atom pedas 🔥 Mau coba?"
        ),
        "default": (
            "Ada beberapa varian kak 😊\n"
            "Produk yang mana yang mau ditanyain?"
        ),
    },
    
    "recommendation_sweet": [
        (
            "Kalau suka manis, coba ini kak 😊\n\n"
            "🍫 Beng-Beng – wafer + caramel + coklat, best seller!\n"
            "🍫 Chocolatos – wafer stick coklat, ringan & crunchy\n"
            "🍪 Gery Saluut – wafer roll coklat\n\n"
            "Mau yang lebih kenyang atau yang ringan aja?"
        ),
    ],
    
    "recommendation_savory": [
        (
            "Kalau gurih nih rekomendasinya kak 👍\n\n"
            "🥜 Kacang Garuda – classic & protein tinggi\n"
            "🥔 Leo Chips – crispy, banyak rasa\n"
            "🌽 Pilus – snack jagung yang nagih\n\n"
            "Lagi pengen yang pedas atau biasa?"
        ),
    ],
    
    "recommendation_spicy": [
        (
            "🌶️ Yang pedas ada:\n\n"
            "🥜 Kacang Atom Pedas – pedes gurih, nagih!\n"
            "🌽 Pilus Pedas – jagung bulat pedes\n"
            "🥔 Leo Chips Spicy – crispy & pedes\n\n"
            "Berani coba yang mana? 😄"
        ),
    ],
    
    "best_seller": [
        (
            "Best seller GarudaFood nih kak 🔥\n\n"
            "1. 🥜 Kacang Atom – klasik, semua orang suka\n"
            "2. 🍫 Chocolatos – favorit anak muda\n"
            "3. 🌽 Pilus Mie Goreng – lagi hits banget!\n\n"
            "Stok terbatas, langsung checkout aja kak 👍"
        ),
    ],
    
    "price": [
        (
            "Harga produk GarudaFood:\n\n"
            "🥜 Kacang – Rp5.000–35.000\n"
            "🍫 Chocolatos – Rp2.000–5.000\n"
            "🍪 Gery – Rp3.000–15.000\n"
            "🍮 Okky Jelly – Rp1.500–5.000\n"
            "🥔 Leo Chips – Rp5.000–20.000\n"
            "🍫 Beng-Beng – Rp3.000–8.000\n\n"
            "Terjangkau semua kak! Langsung checkout aja 🛒"
        ),
    ],
    
    "where_buy": [
        (
            "🛒 Bisa beli di:\n\n"
            "Offline: Indomaret, Alfamart, Hypermart, warung terdekat\n"
            "Online: Tokopedia, Shopee, Lazada – cari 'Garuda Food'\n\n"
            "Tersedia di seluruh Indonesia 🇮🇩"
        ),
    ],
    
    "availability": [
        "Ready kak 👍 Stok masih ada, langsung aja checkout di keranjang kuning sebelum habis! 🛒",
        "Ada kak! Langsung checkout sekarang ya 😊",
    ],
    
    "shipping": [
        (
            "Pengiriman cepat kak! 🚀\n\n"
            "Diproses sesuai antrian order hari ini\n"
            "Bisa pilih ekspedisi sesuai kebutuhan\n\n"
            "Langsung checkout sekarang biar cepet nyampe 😊"
        ),
    ],
    
    "size": [
        (
            "Tergantung kemasannya kak 😊\n\n"
            "📦 Kemasan kecil – buat ngemil harian\n"
            "📦 Kemasan besar – buat sharing atau keluarga\n\n"
            "Mau yang buat sendiri atau buat rame-rame?"
        ),
    ],
    
    "for_kids": [
        (
            "Cocok buat anak-anak kak 👍\n\n"
            "Rekomendasi:\n"
            "🍫 Chocolatos – ringan & manis\n"
            "🍮 Okky Jelly – seger & fun\n"
            "🍪 Gery – biskuit yang lembut\n\n"
            "Hindari yang terlalu pedas ya buat anak kecil 😊"
        ),
    ],
    
    "spicy_check": [
        (
            "Ada yang pedas & nggak pedas kak 😊\n\n"
            "🌶️ Yang pedas: kacang atom pedas, pilus pedas, Leo spicy\n"
            "😌 Yang nggak pedas: kacang kulit original, Chocolatos, Beng-Beng\n\n"
            "Suka yang pedas atau yang aman? 😄"
        ),
    ],
    
    "halal": [
        "✅ Semua produk GarudaFood udah bersertifikat Halal MUI kak! Logo halal ada di setiap kemasan 😊",
    ],
    
    "nutrition": [
        (
            "Info gizi per sajian:\n\n"
            "🥜 Kacang (30g) – ~170 kkal, 7g protein\n"
            "🍫 Chocolatos (1 stick) – ~45 kkal\n"
            "🍮 Okky Jelly (1 cup) – ~80 kkal, 0g lemak\n"
            "🥔 Leo Chips (25g) – ~130 kkal\n"
            "🍫 Beng-Beng (1 bar) – ~130 kkal\n\n"
            "Cek label kemasan untuk info lengkap ya kak 😊"
        ),
    ],
    
    "expired": [
        (
            "Snack GarudaFood umumnya tahan lama kak 😊\n\n"
            "Cek tanggal kadaluarsa di kemasan ya\n"
            "Simpan di tempat kering & sejuk biar tetap kriuk! 👍"
        ),
    ],
    
    "checkout": [
        "Yuk kak langsung checkout sekarang! 🛒🔥 Lagi ada promo & stok terbatas!",
        "Siap kak! Langsung klik keranjang kuning ya 😊",
    ],
    
    "thanks": [
        "Sama-sama kak 😊 Selamat ngemil! 🍫🥜",
        "Sama-sama! Kalau butuh apa-apa tinggal tanya ya 👍",
    ],
    
    "out_of_scope": [
        (
            "Maaf kak 😊 Aku khusus bantu soal produk snack GarudaFood aja nih\n"
            "Kalau mau rekomendasi snack enak, aku siap bantu! 👌"
        ),
    ],
}


def generate_response(intent, context=None):
    """Generate response based on intent and optional context"""
    if intent not in TEMPLATES:
        return "Maaf kak, bisa dijelaskan lebih detail? 😊"
    
    template = TEMPLATES[intent]
    
    # Handle dict templates (product_ask, product_variant)
    if isinstance(template, dict):
        if context:
            for key in template.keys():
                if key in context.lower():
                    return template[key]
        return template.get("default", "Maaf kak, bisa dijelaskan lebih detail? 😊")
    
    # Handle list templates
    if isinstance(template, list):
        return random.choice(template)
    
    return template
