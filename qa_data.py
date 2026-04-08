QA_DATA = [
    # Greetings
    {
        "keywords": ["halo", "hai", "hello", "hi", "hey", "selamat", "pagi", "siang", "sore", "malam"],
        "answer": "Halo kak 👋 Lagi cari snack apa hari ini? 😄 Manis atau gurih?",
    },
    # Thanks / closing
    {
        "keywords": ["makasih", "terima kasih", "thank", "thanks", "thx"],
        "answer": "Sama-sama 😊 Selamat ngemil ya! 🍫🥜 Kalau butuh rekomendasi lagi, tinggal chat aja 👍",
    },
    # Vague / unclear
    {
        "keywords": ["enak", "rekomen", "suggest", "saran", "bagus", "ada yang"],
        "answer": "Hehe banyak 😄 Kamu lagi pengen yang:\n👉 manis\n👉 gurih\n👉 atau ringan buat ngemil?",
    },
    # Sweet recommendation
    {
        "keywords": ["manis", "sweet", "coklat", "chocolate"],
        "answer": (
            "Ada dong 😊 Kalau suka coklat, kamu bisa coba:\n"
            "🍫 Beng-Beng – wafer + caramel + coklat\n"
            "🍫 Chocolatos – wafer stick coklat, enak banget buat ngemil\n\n"
            "Mau yang manis ringan atau yang lebih kenyang?"
        ),
    },
    # Light snack
    {
        "keywords": ["ringan", "light", "tipis", "kecil"],
        "answer": (
            "Oke 👍 Kalau yang ringan aku saranin:\n"
            "🍫 Chocolatos – teksturnya ringan & crunchy\n\n"
            "Ada varian:\n• Milk\n• Dark\n• Matcha\n\n"
            "Kamu biasanya suka rasa apa? 😄"
        ),
    },
    # Savory
    {
        "keywords": ["gurih", "asin", "savory", "salty", "pedas", "spicy", "crispy"],
        "answer": (
            "Siap 👍 Ini rekomendasi gurih:\n"
            "🥜 Kacang Garuda – classic & protein tinggi\n"
            "🥔 Leo Chips – crispy, banyak rasa (BBQ, cheese, spicy)\n\n"
            "Lagi pengen yang pedas atau biasa?"
        ),
    },
    # Beng-Beng
    {
        "keywords": ["beng-beng", "beng beng", "bengbeng"],
        "answer": (
            "ENAK BANGET 😆🔥\n"
            "🍫 Beng-Beng:\n• ada caramel\n• crunchy wafer\n• coklatnya tebel\n\n"
            "Best seller sih ini 👍"
        ),
    },
    # Chocolatos
    {
        "keywords": ["chocolatos", "wafer stick"],
        "answer": (
            "🍫 Chocolatos itu favorit banyak orang!\n\n"
            "Varian:\n• Milk – creamy\n• Dark – rich coklat\n• Matcha – unik & enak\n\n"
            "Harga sekitar Rp2.000–5.000 per pack. Mau yang rasa apa? 😄"
        ),
    },
    # Kacang Garuda
    {
        "keywords": ["kacang", "peanut", "kacang garuda"],
        "answer": (
            "🥜 Kacang Garuda itu klasik banget!\n\n"
            "Varian:\n• Original – gurih ringan\n• Pedas – buat yang suka pedes\n• Rendang – savory banget\n\n"
            "Tinggi protein, cocok buat ngemil kapan aja 💪"
        ),
    },
    # Leo chips
    {
        "keywords": ["leo", "chips", "keripik", "cracker"],
        "answer": (
            "🥔 Leo Chips itu crunchy & addictive!\n\n"
            "Rasa:\n• BBQ\n• Cheese\n• Spicy\n• Original\n\n"
            "Cocok buat nonton atau santai 😄 Suka yang rasa apa?"
        ),
    },
    # Gery
    {
        "keywords": ["gery", "biskuit", "biscuit", "cookie", "wafer"],
        "answer": (
            "🍪 Gery punya banyak pilihan!\n\n"
            "• Gery Malkist – crispy layered\n"
            "• Gery Saluut – wafer roll coklat\n"
            "• Gery Cheese – gurih keju\n\n"
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
            "Tergantung beli di mana ya (Indomaret, Alfamart, atau online) 😊"
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
        "keywords": ["bahan", "ingredient", "contain", "terbuat", "komposisi", "alergi", "allergen"],
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
    # Halal
    {
        "keywords": ["halal", "mui", "sertifikat", "certif"],
        "answer": "✅ Semua produk Garuda Food sudah bersertifikat Halal MUI ya kak! Logo halal ada di setiap kemasan 😊",
    },
    # Nutrition
    {
        "keywords": ["kalori", "nutrition", "gizi", "sehat", "protein", "lemak", "fat", "healthy"],
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
    # All products
    {
        "keywords": ["produk", "product", "semua", "list", "apa saja", "brand", "jual"],
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
]

# Out-of-scope fallback
OUT_OF_SCOPE = "Maaf ya kak 😊 Untuk saat ini kami hanya menyediakan produk snack dari Garuda Food\nKalau mau, aku bisa rekomendasiin snack yang cocok buat kamu 👌"
