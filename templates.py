import random
import re
from difflib import get_close_matches

# ---------------------------------------------------------------------------
# Typo correction — map common product names to canonical form
# ---------------------------------------------------------------------------

PRODUCT_VOCAB = [
    "chocolatos", "kacang", "beng-beng", "bengbeng", "leo", "gery",
    "okky", "pilus", "clevo", "garuda", "wafer", "biskuit", "chips",
]

def fix_typos(text: str) -> str:
    words = text.split()
    corrected = []
    for word in words:
        w = word.lower().strip("?!.,")
        matches = get_close_matches(w, PRODUCT_VOCAB, n=1, cutoff=0.75)
        corrected.append(matches[0] if matches else word)
    return " ".join(corrected)

# ---------------------------------------------------------------------------
# Intent detection — rule-based, no model needed
# Priority: rules are checked top-to-bottom, first match wins
# ---------------------------------------------------------------------------

RULES = [
    # Greeting
    ("greeting",            r"\b(halo|hai|hello|hi|hey|selamat pagi|selamat siang|selamat sore|selamat malam)\b"),
    # Thanks
    ("thanks",              r"\b(makasih|terima kasih|thanks|thank you|thx)\b"),
    # Checkout / buy intent
    ("checkout",            r"\b(checkout|beli|order|pesan|bayar|keranjang|mau beli)\b"),
    # Best seller
    ("best_seller",         r"\b(laris|best.?seller|hits|populer|terlaris|favorit|paling)\b"),
    # Spicy check
    ("spicy_check",         r"\b(pedas|pedes|spicy|nggak pedas|tidak pedas|ada pedas)\b"),
    # For kids
    ("for_kids",            r"\b(anak|kids|balita|bocah|cocok buat anak)\b"),
    # Expired
    ("expired",             r"\b(expired|kadaluarsa|tahan|exp|basi)\b"),
    # Availability
    ("availability",        r"\b(ready|stok|stock|masih ada|tersedia)\b"),
    # Shipping
    ("shipping",            r"\b(kirim|pengiriman|delivery|ongkir|ekspedisi|sampai)\b"),
    # Size
    ("size",                r"\b(isi|ukuran|size|kemasan|gram|besar|kecil|banyak)\b"),
    # Halal
    ("halal",               r"\b(halal|mui|sertifikat halal)\b"),
    # Nutrition
    ("nutrition",           r"\b(kalori|gizi|nutrisi|protein|lemak|sehat|karbohidrat)\b"),
    # Price
    ("price",               r"\b(harga|price|berapa|cost|murah|mahal)\b"),
    # Where to buy
    ("where_buy",           r"\b(beli dimana|indomaret|alfamart|shopee|tokopedia|lazada|online|toko)\b"),
    # Variant / flavor — must come BEFORE general product rules
    ("variant_chocolatos",  r"chocolatos.*(rasa|varian|flavor|apa aja|ada apa|macam)|(rasa|varian|flavor|apa aja).*(chocolatos)"),
    ("variant_kacang",      r"kacang.*(rasa|varian|flavor|apa aja|ada apa|macam)|(rasa|varian|flavor|apa aja).*(kacang)"),
    ("variant_leo",         r"leo.*(rasa|varian|flavor|apa aja|ada apa)|(rasa|varian|flavor|apa aja).*(leo)"),
    ("variant_pilus",       r"pilus.*(rasa|varian|flavor|apa aja|ada apa)|(rasa|varian|flavor|apa aja).*(pilus)"),
    # Product-specific
    ("product_chocolatos",  r"\b(chocolatos|wafer stick|coklat stick)\b"),
    ("product_kacang",      r"\b(kacang garuda|kacang atom|kacang kulit|kacang telur|kacang)\b"),
    ("product_bengbeng",    r"\b(beng.?beng)\b"),
    ("product_leo",         r"\b(leo chips|leo|keripik)\b"),
    ("product_gery",        r"\b(gery|biskuit|biscuit|cookie)\b"),
    ("product_okky",        r"\b(okky|jelly)\b"),
    ("product_pilus",       r"\b(pilus|jagung)\b"),
    # Sweet recommendation
    ("rec_sweet",           r"\b(manis|sweet|coklat|chocolate|recommend.*sweet|rekomendasi.*manis)\b"),
    # Savory recommendation
    ("rec_savory",          r"\b(gurih|asin|savory|salty)\b"),
    # Product list — broad, comes after specific products
    ("product_list",        r"\b(produk|snack|what.*have|ada apa|apa saja|jual apa|list|kategori|semua)\b"),
]


def detect_intent(text: str) -> str:
    t = fix_typos(text).lower()
    for intent, pattern in RULES:
        if re.search(pattern, t):
            return intent
    return "out_of_scope"


# ---------------------------------------------------------------------------
# Response templates
# ---------------------------------------------------------------------------

TEMPLATES = {
    "greeting": [
        "Halo kak 👋 Lagi cari snack apa nih? Manis atau gurih? 😄",
        "Hai kak 😊 Mau yang manis atau gurih?",
    ],
    "thanks": [
        "Sama-sama kak 😊 Selamat ngemil! 🍫🥜",
        "Sama-sama! Kalau butuh apa-apa tinggal tanya ya 👍",
    ],
    "checkout": [
        "Yuk kak langsung checkout sekarang! 🛒🔥 Lagi ada promo & stok terbatas!",
        "Siap kak! Langsung klik keranjang kuning ya 😊",
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
    "spicy_check": [
        (
            "Ada yang pedas & nggak pedas kak 😊\n\n"
            "🌶️ Yang pedas: kacang atom pedas, pilus pedas, Leo spicy\n"
            "😌 Yang nggak pedas: kacang kulit original, Chocolatos, Beng-Beng\n\n"
            "Suka yang pedas atau yang aman? 😄"
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
    "expired": [
        (
            "Snack GarudaFood umumnya tahan lama kak 😊\n\n"
            "Cek tanggal kadaluarsa di kemasan ya\n"
            "Simpan di tempat kering & sejuk biar tetap kriuk! 👍"
        ),
    ],
    "availability": [
        "Ready kak 👍 Stok masih ada, langsung checkout di keranjang kuning sebelum habis! 🛒",
        "Ada kak! Langsung checkout sekarang ya 😊",
    ],
    "shipping": [
        (
            "Pengiriman cepat kak! 🚀\n\n"
            "Diproses sesuai antrian order hari ini\n"
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
    "variant_chocolatos": [
        (
            "Chocolatos ada 2 jenis kak:\n\n"
            "🍫 Wafer Stick: coklat, cappuccino\n"
            "🥤 Drink: coklat original, dark chocolate\n\n"
            "Yang wafer stick paling hits! 😄 Mau yang mana?"
        ),
    ],
    "variant_kacang": [
        (
            "Kacang GarudaFood ada beberapa varian kak:\n\n"
            "🥜 Kacang Atom – original, pedas\n"
            "🥜 Kacang Kulit – original, rendang\n"
            "🥜 Kacang Telur – gurih, pedas\n\n"
            "Yang paling laris kacang atom pedas 🔥 Mau coba?"
        ),
    ],
    "variant_leo": [
        (
            "Leo Chips ada banyak rasa kak:\n\n"
            "🥔 BBQ, Cheese, Spicy, Original, Seaweed\n"
            "Ada juga varian singkong yang lebih kriuk!\n\n"
            "Suka yang rasa apa? 😄"
        ),
    ],
    "variant_pilus": [
        (
            "Pilus ada beberapa varian kak:\n\n"
            "🌽 Original, Pedas, Mie Goreng\n\n"
            "Yang mie goreng lagi hits banget sekarang 🔥 Mau coba?"
        ),
    ],
    "product_chocolatos": [
        (
            "🍫 Chocolatos itu snack wafer stick coklat yang ringan & crunchy!\n\n"
            "Ada varian wafer stick & drink\n"
            "Harga mulai Rp2.000 aja kak\n\n"
            "Mau tau varian rasanya? 😄"
        ),
    ],
    "product_kacang": [
        (
            "🥜 Kacang GarudaFood itu klasik & enak banget!\n\n"
            "Ada kacang atom, kacang kulit, sama kacang telur\n"
            "Tinggi protein, cocok ngemil kapan aja 💪\n\n"
            "Mau yang gurih biasa atau pedas kak?"
        ),
    ],
    "product_bengbeng": [
        (
            "🍫 Beng-Beng ENAK BANGET kak 😆🔥\n\n"
            "• Wafer crunchy berlapis\n"
            "• Caramel di tengah\n"
            "• Dibalut coklat susu\n\n"
            "Ada Original & Maxx (ukuran lebih besar)\n"
            "Best seller nih, langsung checkout aja kak 👍"
        ),
    ],
    "product_leo": [
        (
            "🥔 Leo Chips itu crunchy & addictive kak!\n\n"
            "Rasa: BBQ, Cheese, Spicy, Original, Seaweed\n"
            "Ada juga dari singkong, lebih kriuk!\n\n"
            "Suka yang rasa apa? 😄"
        ),
    ],
    "product_gery": [
        (
            "🍪 Gery punya banyak pilihan kak!\n\n"
            "• Gery Malkist – crispy berlapis\n"
            "• Gery Saluut – wafer roll coklat\n"
            "• Gery Cheese – gurih keju\n\n"
            "Cocok buat cemilan atau bekal anak 😊"
        ),
    ],
    "product_okky": [
        (
            "🍮 Okky Jelly seger & rendah kalori kak!\n\n"
            "Rasa: strawberry, grape, lychee, orange\n"
            "Ada juga Okky Jelly Drink yang bisa langsung diminum 🥤\n\n"
            "Favorit anak-anak nih 😄"
        ),
    ],
    "product_pilus": [
        (
            "🌽 Pilus itu snack jagung bulat yang nagih banget!\n\n"
            "Varian: original, pedas, mie goreng\n"
            "Yang pilus mie goreng lagi hits banget sekarang 🔥\n\n"
            "Mau coba kak?"
        ),
    ],
    "rec_sweet": [
        (
            "Kalau suka manis, coba ini kak 😊\n\n"
            "🍫 Beng-Beng – wafer + caramel + coklat, best seller!\n"
            "🍫 Chocolatos – wafer stick coklat, ringan & crunchy\n"
            "🍪 Gery Saluut – wafer roll coklat\n\n"
            "Mau yang lebih kenyang atau yang ringan aja?"
        ),
    ],
    "rec_savory": [
        (
            "Kalau gurih nih rekomendasinya kak 👍\n\n"
            "🥜 Kacang Garuda – classic & protein tinggi\n"
            "🥔 Leo Chips – crispy, banyak rasa\n"
            "🌽 Pilus – snack jagung yang nagih\n\n"
            "Lagi pengen yang pedas atau biasa?"
        ),
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
    "out_of_scope": [
        "Maaf kak 😊 Itu bukan produk GarudaFood nih\nKalau mau rekomendasi snack enak dari kami, aku siap bantu! 👌",
        "Wah itu bukan produk kami kak 😄 GarudaFood fokus ke snack ya\nMau aku rekomendasiin yang enak?",
        "Kayaknya itu bukan dari GarudaFood deh kak 😊\nTapi kalau mau snack enak, aku bisa bantu rekomendasiin lho!",
        "Hmm itu di luar produk kami kak 🙏\nGarudaFood punya banyak snack enak kok, mau coba yang mana?",
    ],
}


def generate_response(intent: str, context: str = "") -> str:
    options = TEMPLATES.get(intent, TEMPLATES["out_of_scope"])
    return random.choice(options)
