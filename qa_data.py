# Predefined Q&A for common Garuda Food product questions.
# Each entry has:
#   "keywords": list of words — if enough match the user's question, this entry is used
#   "answer": the response to return immediately (no API call)

QA_DATA = [
    {
        "keywords": ["product", "snack", "what", "have", "sell", "list", "brand", "jual", "apa saja"],
        "answer": (
            "Garuda Food has a wide range of snack products! Here are our key brands:\n\n"
            "🥜 Kacang Garuda – Roasted peanuts in original, spicy, and coated flavors\n"
            "🍫 Chocolatos – Chocolate wafer sticks, loved by kids and adults\n"
            "🍪 Gery – Biscuits, wafers, and cookies in many varieties\n"
            "🍮 Okky – Jelly snacks and drinks in fun fruity flavors\n"
            "🥔 Leo – Chips, crackers, and savory snacks\n"
            "🍫 Beng-Beng – Chocolate wafer bars with caramel filling\n"
            "🥛 Clevo – Milk-based snack products\n\n"
            "Would you like to know more about any specific product?"
        ),
    },
    {
        "keywords": ["kacang", "peanut", "garuda peanut", "kacang garuda"],
        "answer": (
            "🥜 Kacang Garuda is one of our most iconic products!\n\n"
            "Available flavors:\n"
            "• Original – Classic roasted peanuts, lightly salted\n"
            "• Spicy (Pedas) – For those who love a kick\n"
            "• Coated (Kulit) – Crispy shell-on peanuts\n"
            "• Rendang – Savory rendang-spiced peanuts\n\n"
            "Sizes: Small (100g), Medium (250g), Large (500g)\n"
            "High in protein and a great snack for any time of day!"
        ),
    },
    {
        "keywords": ["chocolatos", "chocolate wafer", "wafer stick", "coklat"],
        "answer": (
            "🍫 Chocolatos is our popular chocolate wafer stick snack!\n\n"
            "Variants:\n"
            "• Chocolatos Dark – Rich dark chocolate flavor\n"
            "• Chocolatos Milk – Creamy milk chocolate\n"
            "• Chocolatos White – Smooth white chocolate\n"
            "• Chocolatos Matcha – Green tea chocolate flavor\n\n"
            "Each pack contains crispy wafer sticks coated in delicious chocolate. "
            "Perfect as a snack or dessert topping. Available in single packs and multipacks."
        ),
    },
    {
        "keywords": ["gery", "biscuit", "biskuit", "cookie", "wafer"],
        "answer": (
            "🍪 Gery is our biscuit and wafer brand with many delicious options!\n\n"
            "Popular Gery products:\n"
            "• Gery Malkist – Crispy layered crackers\n"
            "• Gery Saluut – Chocolate-filled wafer rolls\n"
            "• Gery Pasta – Wafers with creamy filling\n"
            "• Gery Cheese – Savory cheese-flavored biscuits\n\n"
            "Gery products are great for snacking, lunchboxes, or teatime!"
        ),
    },
    {
        "keywords": ["okky", "jelly", "drink", "minuman", "agar"],
        "answer": (
            "🍮 Okky is our fun jelly snack and drink brand!\n\n"
            "Okky products:\n"
            "• Okky Jelly – Cup jellies in strawberry, grape, lychee, and orange\n"
            "• Okky Jelly Drink – Drinkable jelly in bottles\n"
            "• Okky Drink – Fruit-flavored drinks\n\n"
            "Okky is a favorite among kids and comes in colorful, fun packaging. "
            "Low calorie and refreshing!"
        ),
    },
    {
        "keywords": ["leo", "chip", "crisp", "keripik", "cracker", "savory"],
        "answer": (
            "🥔 Leo is our savory chips and crackers brand!\n\n"
            "Leo variants:\n"
            "• Leo Potato Chips – Classic crispy potato chips\n"
            "• Leo Cassava Chips – Crunchy cassava-based snacks\n"
            "• Leo Crackers – Light and crispy snack crackers\n\n"
            "Available in flavors: Original, BBQ, Spicy, Cheese, and Seaweed. "
            "Perfect for snacking and sharing!"
        ),
    },
    {
        "keywords": ["beng-beng", "beng beng", "caramel", "wafer bar", "chocolate bar"],
        "answer": (
            "🍫 Beng-Beng is our signature chocolate wafer bar!\n\n"
            "Features:\n"
            "• Crispy wafer layers\n"
            "• Smooth caramel filling\n"
            "• Coated in rich milk chocolate\n\n"
            "Variants:\n"
            "• Beng-Beng Original\n"
            "• Beng-Beng Maxx (bigger size)\n"
            "• Beng-Beng Share It (multipack)\n\n"
            "A satisfying sweet treat loved across Indonesia!"
        ),
    },
    {
        "keywords": ["clevo", "milk", "susu", "dairy"],
        "answer": (
            "🥛 Clevo is our milk-based snack product line!\n\n"
            "Clevo products include milk-flavored snacks and drinks designed "
            "for nutrition and taste. Great for kids as part of a balanced diet. "
            "Available in various flavors including plain, strawberry, and chocolate."
        ),
    },
    {
        "keywords": ["ingredient", "bahan", "contain", "made of", "terbuat", "komposisi"],
        "answer": (
            "Our products use quality ingredients. Here's a general overview:\n\n"
            "🥜 Kacang Garuda – Peanuts, salt, vegetable oil, seasoning\n"
            "🍫 Chocolatos – Wheat flour, cocoa, sugar, vegetable fat, milk powder\n"
            "🍪 Gery – Wheat flour, sugar, vegetable oil, flavorings\n"
            "🍮 Okky Jelly – Water, sugar, carrageenan, fruit flavoring\n"
            "🥔 Leo Chips – Potato/cassava, vegetable oil, seasoning\n"
            "🍫 Beng-Beng – Wheat flour, sugar, cocoa, caramel, milk\n\n"
            "For detailed ingredient lists and allergen info, please check the product packaging "
            "or visit the official Garuda Food website."
        ),
    },
    {
        "keywords": ["nutrition", "calorie", "kalori", "gizi", "healthy", "sehat", "protein", "fat", "lemak"],
        "answer": (
            "Here's a general nutritional overview of our popular snacks (per serving):\n\n"
            "🥜 Kacang Garuda (30g) – ~170 kcal, 7g protein, 14g fat\n"
            "🍫 Chocolatos (1 stick) – ~45 kcal, 0.5g protein, 2g fat\n"
            "🍪 Gery Malkist (4 pcs) – ~90 kcal, 1.5g protein, 3.5g fat\n"
            "🍮 Okky Jelly (1 cup) – ~80 kcal, 0g protein, 0g fat\n"
            "🥔 Leo Chips (25g) – ~130 kcal, 1g protein, 8g fat\n"
            "🍫 Beng-Beng (1 bar) – ~130 kcal, 1.5g protein, 6g fat\n\n"
            "For exact nutritional information, check the label on each product."
        ),
    },
    {
        "keywords": ["buy", "where", "beli", "toko", "store", "shop", "alfamart", "indomaret", "online", "shopee", "tokopedia"],
        "answer": (
            "🛒 You can find Garuda Food products at:\n\n"
            "Physical stores:\n"
            "• Indomaret and Alfamart (nationwide)\n"
            "• Hypermart, Transmart, Carrefour\n"
            "• Local warungs and minimarkets\n\n"
            "Online:\n"
            "• Tokopedia – search 'Garuda Food'\n"
            "• Shopee – search 'Garuda Food'\n"
            "• Lazada\n"
            "• Official Garuda Food online store\n\n"
            "Products are available across Indonesia and in select international markets."
        ),
    },
    {
        "keywords": ["sweet", "manis", "recommend", "rekomendasi", "suggestion", "saran", "favorite", "favorit", "best"],
        "answer": (
            "Looking for a sweet Garuda Food snack? Here are our top picks:\n\n"
            "🍫 Beng-Beng – Chocolate wafer bar with caramel, a classic!\n"
            "🍫 Chocolatos – Chocolate wafer sticks, great for munching\n"
            "🍪 Gery Saluut – Crispy wafer rolls with chocolate filling\n"
            "🍮 Okky Jelly – Light and fruity jelly cups\n\n"
            "All are available in most stores across Indonesia. Would you like more details on any of these?"
        ),
    },
    {
        "keywords": ["savory", "asin", "salty", "gurih", "spicy", "pedas"],
        "answer": (
            "Love savory snacks? Here are our best picks:\n\n"
            "🥜 Kacang Garuda Pedas – Spicy roasted peanuts\n"
            "🥔 Leo Chips – Potato chips in BBQ, Cheese, and Spicy flavors\n"
            "🍪 Gery Cheese Biscuits – Savory cheese-flavored crackers\n"
            "🥔 Leo Cassava Chips – Crunchy and lightly seasoned\n\n"
            "These are perfect for snacking, watching movies, or gatherings!"
        ),
    },
    {
        "keywords": ["price", "harga", "cost", "how much", "berapa"],
        "answer": (
            "Here's a rough price guide for Garuda Food products in Indonesia:\n\n"
            "🥜 Kacang Garuda – Rp 5,000 – Rp 35,000 (depending on size)\n"
            "🍫 Chocolatos – Rp 2,000 – Rp 5,000 per pack\n"
            "🍪 Gery – Rp 3,000 – Rp 15,000\n"
            "🍮 Okky Jelly – Rp 1,500 – Rp 5,000\n"
            "🥔 Leo Chips – Rp 5,000 – Rp 20,000\n"
            "🍫 Beng-Beng – Rp 3,000 – Rp 8,000\n\n"
            "Prices may vary by store and region. Check Tokopedia or Shopee for the latest prices."
        ),
    },
    {
        "keywords": ["halal", "certif", "sertifikat", "mui"],
        "answer": (
            "✅ Yes! Garuda Food products are Halal certified by MUI (Majelis Ulama Indonesia).\n\n"
            "All our snack products comply with halal standards in ingredients, "
            "processing, and packaging. You can find the MUI Halal logo on our product packaging."
        ),
    },
    {
        "keywords": ["hello", "hi", "halo", "hai", "hey", "good morning", "good afternoon", "selamat", "pagi", "siang", "sore"],
        "answer": (
            "Hello! 👋 Welcome to the Garuda Food Snack Assistant!\n\n"
            "I'm here to help you with anything about our delicious snack products — "
            "from ingredients and nutrition to where to buy them.\n\n"
            "What would you like to know about our snacks today? 🥜🍫🍪"
        ),
    },
    {
        "keywords": ["thank", "thanks", "terima kasih", "makasih", "thx"],
        "answer": (
            "You're welcome! 😊 Happy snacking with Garuda Food!\n\n"
            "Feel free to ask anytime if you have more questions about our products. 🥜🍫"
        ),
    },
]
