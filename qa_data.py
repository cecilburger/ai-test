QA_DATA = [
    # Greetings
    {
        "keywords": ["halo", "hai", "hello", "hi", "hey"],
        "answer": "Halo kak 👋 Lagi cari snack apa hari ini? 😄 Manis atau gurih?",
    },
    {
        "keywords": ["selamat", "pagi", "siang", "sore", "malam"],
        "answer": "Halo kak 👋 Lagi cari snack apa hari ini? 😄 Manis atau gurih?",
    },
    # Thanks
    {
        "keywords": ["makasih", "terima kasih", "thank", "thanks", "thx"],
        "answer": "Sama-sama 😊 Selamat ngemil ya! 🍫🥜 Kalau butuh rekomendasi lagi, tinggal chat aja 👍",
    },
    # All products / what do you have
    {
        "keywords": ["produk", "product", "snack", "what", "have", "semua", "list", "apa saja", "brand", "jual", "sell"],
        "answer": (
            "Ini produk snack Garuda Food:\n\n"
            "🥜 Kacang Garuda – kacang panggang\n"
            "🍫 Chocolatos – wafer stick coklat\n"
            "🍪 Gery – biskuit & wafer\n"
            "🍮 Okky – jelly & minuman\n"
            "🥔 Leo – chips & crackers\n"
            "🍫 Beng-Beng – wafer bar coklat caramel\n"
            "🥛 Clevo – snack berbasis susu\n\n"
            "Mau tau lebih lanjut yang mana? 😄"
        ),
    },
    # Chocolatos flavors (must be before general chocolatos entry)
    {
        "keywords": ["chocolatos", "rasa", "varian", "flavor", "variant"],
        "answer": (
            "🍫 Chocolatos ada beberapa varian:\n\n"
            "• Milk – creamy & manis\n"
            "• Dark – rich coklat pekat\n"
            "• Matcha – green tea, unik & enak\n"
            "• White – lembut & manis\n\n"
            "Kamu suka yang mana? 😄"
        ),
    },
    # Chocolatos general
    {
        "keywords": ["chocolatos", "wafer stick", "coklat stick"],
        "answer": (
            "🍫 Chocolatos itu favorit banyak orang!\n\n"
            "Wafer stick coklat yang ringan & crunchy\n"
            "Ada varian: Milk, Dark, Matcha, White\n"
            "Harga sekitar Rp2.000–5.000 per pack\n\n"
            "Mau tau rasa yang mana dulu? 😄"
        ),
    },
    # Kacang Garuda flavors
    {
        "keywords": ["kacang", "rasa", "varian", "flavor"],
        "answer": (
            "🥜 Kacang Garuda ada beberapa varian:\n\n"
            "• Original – gurih ringan\n"
            "• Pedas – buat yang suka pedes 🌶️\n"
            "• Rendang – savory banget\n"
            "• Kulit – crispy shell-on\n\n"
            "Suka yang mana? 😄"
        ),
    },
    # Kacang Garuda general
    {
        "keywords": ["kacang", "peanut", "kacang garuda"],
        "answer": (
            "🥜 Kacang Garuda itu klasik banget!\n\n"
            "Varian: Original, Pedas, Rendang, Kulit\n"
            "Tinggi protein, cocok buat ngemil kapan aja 💪\n\n"
            "Lagi pengen yang gurih biasa atau pedas?"
        ),
    },
    # Sweet recommendation
    {
        "keywords": ["manis", "sweet", "recommend", "rekomen"],
        "answer": (
            "Kalau suka manis, coba ini kak:\n\n"
            "🍫 Beng-Beng – wafer + caramel + coklat, best seller!\n"
            "🍫 Chocolatos – wafer stick coklat, ringan & crunchy\n"
            "🍪 Gery Saluut – wafer roll coklat\n\n"
            "Mau yang lebih kenyang atau yang ringan aja?"
        ),
    },
    # Chocolate
    {
        "keywords": ["coklat", "chocolate"],
        "answer": (
            "Ada dong 😊 Pilihan coklat dari Garuda Food:\n\n"
            "🍫 Beng-Beng – wafer + caramel + coklat\n"
            "🍫 Chocolatos – wafer stick coklat\n\n"
            "Mau yang manis ringan atau yang lebih kenyang?"
        ),
    },
    # Light snack
    {
        "keywords": ["ringan", "light"],
        "answer": (
            "Kalau yang ringan aku saranin:\n\n"
            "🍫 Chocolatos – teksturnya ringan & crunchy\n"
            "🍮 Okky Jelly – seger & rendah kalori\n\n"
            "Kamu biasanya suka manis atau buah-buahan? 😄"
        ),
    },
    # Savory
    {
        "keywords": ["gurih", "asin", "savory", "salty"],
        "answer": (
            "Siap 👍 Rekomendasi gurih:\n\n"
            "🥜 Kacang Garuda – classic & protein tinggi\n"
            "🥔 Leo Chips – crispy, banyak rasa (BBQ, cheese, spicy)\n"
            "🍪 Gery Cheese – biskuit keju gurih\n\n"
            "Lagi pengen yang pedas atau biasa?"
        ),
    },
    # Spicy
    {
        "keywords": ["pedas", "spicy", "pedes"],
        "answer": (
            "🌶️ Yang pedas ada:\n\n"
            "🥜 Kacang Garuda Pedas – pedes gurih, nagih!\n"
            "🥔 Leo Chips Spicy – crispy & pedes\n\n"
            "Berani coba yang mana? 😄"
        ),
    },
    # Beng-Beng
    {
        "keywords": ["beng-beng", "beng beng", "bengbeng"],
        "answer": (
            "ENAK BANGET 😆🔥\n\n"
            "🍫 Beng-Beng:\n"
            "• Wafer crunchy berlapis\n"
            "• Caramel di tengah\n"
            "• Dibalut coklat susu\n\n"
            "Ada varian Original & Maxx (ukuran lebih besar)\n"
            "Best seller nih 👍"
        ),
    },
    # Leo chips
    {
        "keywords": ["leo", "chips", "keripik", "cracker"],
        "answer": (
            "🥔 Leo Chips itu crunchy & addictive!\n\n"
            "Rasa: BBQ, Cheese, Spicy, Original, Seaweed\n"
            "Ada juga Leo Cassava Chips dari singkong\n\n"
            "Suka yang rasa apa? 😄"
        ),
    },
    # Gery
    {
        "keywords": ["gery", "biskuit", "biscuit", "cookie"],
        "answer": (
            "🍪 Gery punya banyak pilihan!\n\n"
            "• Gery Malkist – crispy layered\n"
            "• Gery Saluut – wafer roll coklat\n"
            "• Gery Cheese – gurih keju\n"
            "• Gery Pasta – wafer krim\n\n"
            "Cocok buat cemilan atau bekal 😊"
        ),
    },
    # Okky
    {
        "keywords": ["okky", "jelly", "agar"],
        "answer": (
            "🍮 Okky Jelly itu seger & rendah kalori!\n\n"
            "Rasa: strawberry, grape, lychee, orange\n"
            "Ada juga Okky Jelly Drink yang bisa diminum langsung 🥤\n\n"
            "Cocok banget buat anak-anak 😄"
        ),
    },
    # Clevo
    {
        "keywords": ["clevo", "susu", "milk", "dairy"],
        "answer": (
            "🥛 Clevo itu snack berbasis susu dari Garuda Food!\n\n"
            "Rasa: plain, strawberry, coklat\n"
            "Bagus buat anak-anak sebagai camilan bergizi 😊"
        ),
    },
    # Price
    {
        "keywords": ["harga", "price", "berapa", "cost", "murah"],
        "answer": (
            "Harga produk Garuda Food:\n\n"
            "🥜 Kacang Garuda – Rp5.000–35.000\n"
            "🍫 Chocolatos – Rp2.000–5.000\n"
            "🍪 Gery – Rp3.000–15.000\n"
            "🍮 Okky Jelly – Rp1.500–5.000\n"
            "🥔 Leo Chips – Rp5.000–20.000\n"
            "🍫 Beng-Beng – Rp3.000–8.000\n\n"
            "Tergantung beli di mana ya 😊"
        ),
    },
    # Where to buy
    {
        "keywords": ["beli", "where", "toko", "store", "alfamart", "indomaret", "shopee", "tokopedia", "online"],
        "answer": (
            "🛒 Bisa beli di:\n\n"
            "Offline: Indomaret, Alfamart, Hypermart, warung terdekat\n"
            "Online: Tokopedia, Shopee, Lazada – cari 'Garuda Food'\n\n"
            "Tersedia di seluruh Indonesia 🇮🇩"
        ),
    },
    # Ingredients
    {
        "keywords": ["bahan", "ingredient", "contain", "terbuat", "komposisi"],
        "answer": (
            "Bahan utama produk kami:\n\n"
            "🥜 Kacang Garuda – kacang, garam, minyak nabati\n"
            "🍫 Chocolatos – tepung, kakao, gula, susu\n"
            "🍪 Gery – tepung, gula, minyak nabati\n"
            "🍮 Okky – air, gula, karagenan, perisa buah\n"
            "🥔 Leo – kentang/singkong, minyak, bumbu\n"
            "🍫 Beng-Beng – tepung, gula, kakao, karamel, susu\n\n"
            "Untuk info lengkap, cek kemasan produk ya 😊"
        ),
    },
    # Allergen
    {
        "keywords": ["alergi", "allergen", "susu", "gluten", "kacang alergi"],
        "answer": (
            "⚠️ Info alergen:\n\n"
            "• Chocolatos & Beng-Beng – mengandung susu & gluten\n"
            "• Kacang Garuda – mengandung kacang tanah\n"
            "• Gery – mengandung gluten\n"
            "• Okky Jelly – bebas gluten & susu\n\n"
            "Selalu cek label kemasan untuk info lengkap ya kak 😊"
        ),
    },
    # Halal
    {
        "keywords": ["halal", "mui", "sertifikat"],
        "answer": "✅ Semua produk Garuda Food sudah bersertifikat Halal MUI ya kak! Logo halal ada di setiap kemasan 😊",
    },
    # Nutrition
    {
        "keywords": ["kalori", "nutrition", "gizi", "sehat", "protein", "lemak"],
        "answer": (
            "Info gizi per sajian:\n\n"
            "🥜 Kacang Garuda (30g) – ~170 kkal, 7g protein\n"
            "🍫 Chocolatos (1 stick) – ~45 kkal\n"
            "🍮 Okky Jelly (1 cup) – ~80 kkal, 0g lemak\n"
            "🥔 Leo Chips (25g) – ~130 kkal\n"
            "🍫 Beng-Beng (1 bar) – ~130 kkal\n\n"
            "Untuk info lengkap cek label kemasan ya 😊"
        ),
    },
    # Vague
    {
        "keywords": ["enak", "bagus", "ada yang", "mau"],
        "answer": "Hehe banyak 😄 Kamu lagi pengen yang:\n👉 manis\n👉 gurih\n👉 atau ringan buat ngemil?",
    },
]

OUT_OF_SCOPE = (
    "Maaf ya kak 😊 Aku khusus bantu soal produk snack Garuda Food aja\n"
    "Kalau mau, aku bisa rekomendasiin snack yang cocok buat kamu 👌"
)
