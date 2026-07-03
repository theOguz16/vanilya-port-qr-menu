const MENU_STORAGE_KEY = "vanilya-port-products-v2";

const categoryLabels = {
  coldDrinks: "Soğuk İçecekler",
  hotDrinks: "Sıcak İçecekler",
  desserts: "Tatlılar",
  foods: "Yemekler",
};

const categoryOrder = ["coldDrinks", "hotDrinks", "foods", "desserts"];

const placeholderImage =
  "./assets/vanilya-port-logo.jpg";

const defaultProducts = [
  {
    "id": "espresso",
    "name": "Espresso",
    "price": "120 TL",
    "calories": "5 kcal",
    "category": "hotDrinks",
    "description": "Yoğun aromalı klasik espresso shot.",
    "image": "https://loremflickr.com/900/700/espresso,coffee?lock=1884",
    "isActive": true,
    "sortOrder": 10
  },
  {
    "id": "double-espresso",
    "name": "Double Espresso",
    "price": "150 TL",
    "calories": "10 kcal",
    "category": "hotDrinks",
    "description": "İki shot espresso ile daha yoğun kahve deneyimi.",
    "image": "https://loremflickr.com/900/700/double,espresso,coffee?lock=2564",
    "isActive": true,
    "sortOrder": 20
  },
  {
    "id": "affogato",
    "name": "Affogato",
    "price": "180 TL",
    "calories": "220 kcal",
    "category": "hotDrinks",
    "description": "Vanilyalı dondurma üzerine sıcak espresso dökülerek servis edilir.",
    "image": "https://loremflickr.com/900/700/affogato,coffee,dessert?lock=1839",
    "isActive": true,
    "sortOrder": 30
  },
  {
    "id": "cortado",
    "name": "Cortado",
    "price": "150 TL",
    "calories": "80 kcal",
    "category": "hotDrinks",
    "description": "Espresso ve sıcak sütün dengeli, yumuşak birleşimi.",
    "image": "https://loremflickr.com/900/700/cortado,coffee?lock=1748",
    "isActive": true,
    "sortOrder": 40
  },
  {
    "id": "americano",
    "name": "Americano",
    "price": "150 TL",
    "calories": "10 kcal",
    "category": "hotDrinks",
    "description": "Espresso üzerine sıcak suyla hazırlanan sade kahve.",
    "image": "https://loremflickr.com/900/700/americano,coffee?lock=1943",
    "isActive": true,
    "sortOrder": 50
  },
  {
    "id": "coffee-latte",
    "name": "Coffee Latte",
    "price": "150 TL",
    "calories": "170 kcal",
    "category": "hotDrinks",
    "description": "Espresso ve ipeksi süt dokusuyla yumuşak içimli latte.",
    "image": "https://loremflickr.com/900/700/hot,latte,coffee?lock=2199",
    "isActive": true,
    "sortOrder": 60
  },
  {
    "id": "coffee-mocha",
    "name": "Coffee Mocha",
    "price": "150 TL",
    "calories": "260 kcal",
    "category": "hotDrinks",
    "description": "Espresso, süt ve çikolata aromasıyla kremamsı sıcak kahve.",
    "image": "https://loremflickr.com/900/700/mocha,coffee,chocolate?lock=2181",
    "isActive": true,
    "sortOrder": 70
  },
  {
    "id": "cappuccino",
    "name": "Cappuccino",
    "price": "150 TL",
    "calories": "140 kcal",
    "category": "hotDrinks",
    "description": "Dengeli espresso, yoğun süt köpüğü ve kakao dokunuşu.",
    "image": "https://loremflickr.com/900/700/cappuccino,coffee?lock=2061",
    "isActive": true,
    "sortOrder": 80
  },
  {
    "id": "filtre-kahve",
    "name": "Filtre Kahve",
    "price": "150 TL",
    "calories": "5 kcal",
    "category": "hotDrinks",
    "description": "Günlük çekilmiş kahveyle hazırlanan sade filtre kahve.",
    "image": "https://loremflickr.com/900/700/filter,coffee?lock=2218",
    "isActive": true,
    "sortOrder": 90
  },
  {
    "id": "sicak-cikolata",
    "name": "Sıcak Çikolata",
    "price": "180 TL",
    "calories": "320 kcal",
    "category": "hotDrinks",
    "description": "Yoğun çikolata aromalı, sıcak ve kremamsı içecek.",
    "image": "https://loremflickr.com/900/700/hot,chocolate,drink?lock=2408",
    "isActive": true,
    "sortOrder": 100
  },
  {
    "id": "turk-kahvesi",
    "name": "Türk Kahvesi",
    "price": "120 TL",
    "calories": "25 kcal",
    "category": "hotDrinks",
    "description": "Geleneksel bakır cezvede hazırlanan bol köpüklü Türk kahvesi.",
    "image": "https://loremflickr.com/900/700/turkish,coffee?lock=2246",
    "isActive": true,
    "sortOrder": 110
  },
  {
    "id": "damla-sakizli-turk-kahvesi",
    "name": "Damla Sakızlı Türk Kahvesi",
    "price": "120 TL",
    "calories": "35 kcal",
    "category": "hotDrinks",
    "description": "Damla sakızı aromasıyla hazırlanan geleneksel Türk kahvesi.",
    "image": "https://loremflickr.com/900/700/turkish,coffee?lock=3606",
    "isActive": true,
    "sortOrder": 120
  },
  {
    "id": "dibek-kahvesi",
    "name": "Dibek Kahvesi",
    "price": "120 TL",
    "calories": "60 kcal",
    "category": "hotDrinks",
    "description": "Yumuşak içimli, aromatik geleneksel dibek kahvesi.",
    "image": "https://loremflickr.com/900/700/turkish,coffee?lock=2303",
    "isActive": true,
    "sortOrder": 130
  },
  {
    "id": "bitki-caylari",
    "name": "Bitki Çayları",
    "price": "150 TL",
    "calories": "5 kcal",
    "category": "hotDrinks",
    "description": "Sıcak servis edilen rahatlatıcı bitki çayı seçkisi.",
    "image": "https://loremflickr.com/900/700/herbal,tea?lock=2317",
    "isActive": true,
    "sortOrder": 140,
    "options": [
      "Ihlamur",
      "Papatya",
      "Ada Çayı",
      "Kış Çayı",
      "Yeşil Çay",
      "Kuşburnu Çayı"
    ]
  },
  {
    "id": "cay",
    "name": "Çay",
    "price": "50 TL",
    "calories": "3 kcal",
    "category": "hotDrinks",
    "description": "Taze demlenmiş klasik sıcak çay.",
    "image": "https://loremflickr.com/900/700/turkish,tea?lock=1317",
    "isActive": true,
    "sortOrder": 150
  },
  {
    "id": "chicken-burger",
    "name": "Chicken Burger",
    "price": "300 TL",
    "calories": "620 kcal",
    "category": "foods",
    "description": "Çıtır tavuk, taze yeşillik ve özel sosla hazırlanan doyurucu burger.",
    "image": "https://loremflickr.com/900/700/chicken,burger?lock=2417",
    "isActive": true,
    "sortOrder": 10
  },
  {
    "id": "hamburger",
    "name": "Hamburger",
    "price": "400 TL",
    "calories": "700 kcal",
    "category": "foods",
    "description": "Izgara köfte, taze yeşillik ve özel sosla hazırlanan klasik burger.",
    "image": "https://loremflickr.com/900/700/hamburger,burger?lock=1957",
    "isActive": true,
    "sortOrder": 20
  },
  {
    "id": "cheddar-burger",
    "name": "Cheddar Burger",
    "price": "430 TL",
    "calories": "780 kcal",
    "category": "foods",
    "description": "Cheddar peyniri, köfte ve özel sosla hazırlanan yoğun lezzetli burger.",
    "image": "https://loremflickr.com/900/700/cheeseburger,cheddar?lock=2407",
    "isActive": true,
    "sortOrder": 30
  },
  {
    "id": "gozleme",
    "name": "Gözleme",
    "price": "250 TL",
    "calories": "520 kcal",
    "category": "foods",
    "description": "Sıcak servis edilen ince hamurlu geleneksel gözleme.",
    "image": "https://loremflickr.com/900/700/flatbread,pastry?lock=1755",
    "isActive": true,
    "sortOrder": 40,
    "options": [
      "Patatesli",
      "Peynirli"
    ]
  },
  {
    "id": "combo-tabagi",
    "name": "Combo Tabağı",
    "price": "500 TL",
    "calories": "1100 kcal",
    "category": "foods",
    "description": "Paylaşımlık sıcak atıştırmalıkların doyurucu birleşimi.",
    "image": "https://loremflickr.com/900/700/snack,platter,fries?lock=2189",
    "isActive": true,
    "sortOrder": 50
  },
  {
    "id": "patates-kizartmasi",
    "name": "Patates Kızartması",
    "price": "200 TL",
    "calories": "430 kcal",
    "category": "foods",
    "description": "Altın renkli çıtır patates kızartması.",
    "image": "https://loremflickr.com/900/700/french,fries?lock=2886",
    "isActive": true,
    "sortOrder": 60
  },
  {
    "id": "elma-dilim-patates-kizartmasi",
    "name": "Elma Dilim Patates Kızartması",
    "price": "200 TL",
    "calories": "450 kcal",
    "category": "foods",
    "description": "Baharatlı elma dilim patates, sıcak ve çıtır servis edilir.",
    "image": "https://loremflickr.com/900/700/potato,wedges?lock=3918",
    "isActive": true,
    "sortOrder": 70
  },
  {
    "id": "sigara-boregi-tabagi",
    "name": "Sigara Böreği Tabağı",
    "price": "250 TL",
    "calories": "520 kcal",
    "category": "foods",
    "description": "Çıtır sigara börekleri, paylaşmalık tabak sunumuyla.",
    "image": "https://loremflickr.com/900/700/cheese,rolls,pastry?lock=2969",
    "isActive": true,
    "sortOrder": 80
  },
  {
    "id": "sogan-halkasi-tabagi",
    "name": "Soğan Halkası Tabağı",
    "price": "250 TL",
    "calories": "480 kcal",
    "category": "foods",
    "description": "Çıtır kaplamalı soğan halkaları, sıcak servis edilir.",
    "image": "https://loremflickr.com/900/700/onion,rings?lock=2975",
    "isActive": true,
    "sortOrder": 90
  },
  {
    "id": "nugget-tabagi",
    "name": "Nugget Tabağı",
    "price": "250 TL",
    "calories": "540 kcal",
    "category": "foods",
    "description": "Çıtır tavuk nugget parçaları, paylaşmalık tabak sunumuyla.",
    "image": "https://loremflickr.com/900/700/chicken,nuggets?lock=2311",
    "isActive": true,
    "sortOrder": 100
  },
  {
    "id": "citir-tavuk-sepeti",
    "name": "Çıtır Tavuk Sepeti",
    "price": "350 TL",
    "calories": "680 kcal",
    "category": "foods",
    "description": "Baharatlı çıtır tavuk parçaları, sepet sunumuyla.",
    "image": "https://loremflickr.com/900/700/crispy,chicken?lock=2834",
    "isActive": true,
    "sortOrder": 110
  },
  {
    "id": "ice-latte",
    "name": "Ice Latte",
    "price": "170 TL",
    "calories": "190 kcal",
    "category": "coldDrinks",
    "description": "Buz, espresso ve soğuk sütle hazırlanan ferah kahve.",
    "image": "https://loremflickr.com/900/700/iced,latte,coffee?lock=1888",
    "isActive": true,
    "sortOrder": 10,
    "options": [
      "Vanilya",
      "Karamel",
      "Tiramisu",
      "Cookie",
      "Fındık Cookie"
    ]
  },
  {
    "id": "ice-mocha",
    "name": "Ice Mocha",
    "price": "170 TL",
    "calories": "290 kcal",
    "category": "coldDrinks",
    "description": "Soğuk espresso, süt ve çikolata aromasıyla hazırlanır.",
    "image": "https://loremflickr.com/900/700/iced,mocha,coffee?lock=1870",
    "isActive": true,
    "sortOrder": 20
  },
  {
    "id": "ice-white-mocha",
    "name": "Ice White Mocha",
    "price": "170 TL",
    "calories": "320 kcal",
    "category": "coldDrinks",
    "description": "Beyaz çikolata aromalı soğuk kahve.",
    "image": "https://loremflickr.com/900/700/iced,white,mocha?lock=2460",
    "isActive": true,
    "sortOrder": 30
  },
  {
    "id": "ice-americano",
    "name": "Ice Americano",
    "price": "170 TL",
    "calories": "20 kcal",
    "category": "coldDrinks",
    "description": "Espresso, soğuk su ve buzla hazırlanan sade soğuk kahve.",
    "image": "https://loremflickr.com/900/700/iced,americano,coffee?lock=2293",
    "isActive": true,
    "sortOrder": 40
  },
  {
    "id": "cold-brew",
    "name": "Cold Brew",
    "price": "200 TL",
    "calories": "10 kcal",
    "category": "coldDrinks",
    "description": "Uzun demleme yöntemiyle hazırlanan yumuşak içimli soğuk kahve.",
    "image": "https://loremflickr.com/900/700/cold,brew,coffee?lock=1895",
    "isActive": true,
    "sortOrder": 50
  },
  {
    "id": "frappe",
    "name": "Frappe",
    "price": "200 TL",
    "calories": "360 kcal",
    "category": "coldDrinks",
    "description": "Buzla karıştırılmış kremamsı kahve içeceği.",
    "image": "https://loremflickr.com/900/700/coffee,frappe?lock=1638",
    "isActive": true,
    "sortOrder": 60,
    "options": [
      "Karamel",
      "Çikolata",
      "Vanilya",
      "Cookie"
    ]
  },
  {
    "id": "milkshake",
    "name": "Milkshake",
    "price": "200 TL",
    "calories": "420 kcal",
    "category": "coldDrinks",
    "description": "Yoğun ve kremamsı soğuk milkshake.",
    "image": "https://loremflickr.com/900/700/milkshake?lock=1953",
    "isActive": true,
    "sortOrder": 70,
    "options": [
      "Karamel",
      "Vanilya",
      "Çilek",
      "Çikolata",
      "Tiramisu"
    ]
  },
  {
    "id": "frozen",
    "name": "Frozen",
    "price": "200 TL",
    "calories": "260 kcal",
    "category": "coldDrinks",
    "description": "Buzlu meyve aromalarıyla hazırlanan ferah içecek.",
    "image": "https://loremflickr.com/900/700/frozen,fruit,drink?lock=1660",
    "isActive": true,
    "sortOrder": 80,
    "options": [
      "Mango",
      "Ananas",
      "Karadut",
      "Böğürtlen",
      "Çilek",
      "Yeşil Elma",
      "Orman Meyve"
    ]
  },
  {
    "id": "cool-lime",
    "name": "Cool Lime",
    "price": "180 TL",
    "calories": "160 kcal",
    "category": "coldDrinks",
    "description": "Lime ve nane ferahlığıyla hazırlanan buzlu içecek.",
    "image": "https://loremflickr.com/900/700/lime,drink?lock=1897",
    "isActive": true,
    "sortOrder": 90
  },
  {
    "id": "berry-hibiscus",
    "name": "Berry Hibiscus",
    "price": "180 TL",
    "calories": "150 kcal",
    "category": "coldDrinks",
    "description": "Hibiskus ve orman meyvesi aromalarıyla ferah içecek.",
    "image": "https://loremflickr.com/900/700/berry,hibiscus,drink?lock=2451",
    "isActive": true,
    "sortOrder": 100
  },
  {
    "id": "italyan-soda",
    "name": "İtalyan Soda",
    "price": "180 TL",
    "calories": "180 kcal",
    "category": "coldDrinks",
    "description": "Aromalı soda ve buzla hazırlanan renkli ferah içecek.",
    "image": "https://loremflickr.com/900/700/italian,soda,drink?lock=2222",
    "isActive": true,
    "sortOrder": 110
  },
  {
    "id": "mojito",
    "name": "Mojito",
    "price": "300 TL",
    "calories": "240 kcal",
    "category": "coldDrinks",
    "description": "Buzlu, naneli ve meyve aromalı özel içecek.",
    "image": "https://loremflickr.com/900/700/mojito,mocktail?lock=1658",
    "isActive": true,
    "sortOrder": 120,
    "options": [
      "Çilekli",
      "Nane",
      "Karadut",
      "Böğürtlen",
      "Yeşil Elma",
      "Orman Meyve"
    ]
  },
  {
    "id": "churchill",
    "name": "Churchill",
    "price": "150 TL",
    "calories": "80 kcal",
    "category": "coldDrinks",
    "description": "Soda, limon ve tuzla hazırlanan ferah klasik.",
    "image": "https://loremflickr.com/900/700/lemon,soda?lock=1958",
    "isActive": true,
    "sortOrder": 130
  },
  {
    "id": "berry-me",
    "name": "Berry Me",
    "price": "250 TL",
    "calories": "280 kcal",
    "category": "coldDrinks",
    "description": "Yoğun orman meyvesi aromalı özel soğuk içecek.",
    "image": "https://loremflickr.com/900/700/berry,smoothie?lock=1803",
    "isActive": true,
    "sortOrder": 140
  },
  {
    "id": "ev-yapimi-limonata",
    "name": "Ev Yapımı Limonata",
    "price": "120 TL",
    "calories": "140 kcal",
    "category": "coldDrinks",
    "description": "Taze limonla hazırlanan ev yapımı limonata.",
    "image": "https://loremflickr.com/900/700/lemonade?lock=2811",
    "isActive": true,
    "sortOrder": 150
  },
  {
    "id": "meyveli-limonata",
    "name": "Meyveli Limonata",
    "price": "180 TL",
    "calories": "210 kcal",
    "category": "coldDrinks",
    "description": "Meyve aromalarıyla hazırlanan taze limonata.",
    "image": "https://loremflickr.com/900/700/strawberry,lemonade?lock=2661",
    "isActive": true,
    "sortOrder": 160,
    "options": [
      "Çilek",
      "Nane",
      "Karadut",
      "Böğürtlen"
    ]
  },
  {
    "id": "cola",
    "name": "Cola",
    "price": "120 TL",
    "calories": "140 kcal",
    "category": "coldDrinks",
    "description": "Soğuk servis edilen gazlı içecek.",
    "image": "https://loremflickr.com/900/700/cola,drink?lock=1415",
    "isActive": true,
    "sortOrder": 170
  },
  {
    "id": "fanta",
    "name": "Fanta",
    "price": "120 TL",
    "calories": "140 kcal",
    "category": "coldDrinks",
    "description": "Soğuk servis edilen portakallı gazlı içecek.",
    "image": "https://loremflickr.com/900/700/orange,soda?lock=1522",
    "isActive": true,
    "sortOrder": 180
  },
  {
    "id": "gazoz",
    "name": "Gazoz",
    "price": "120 TL",
    "calories": "140 kcal",
    "category": "coldDrinks",
    "description": "Soğuk servis edilen klasik gazoz.",
    "image": "https://loremflickr.com/900/700/soda,drink?lock=1555",
    "isActive": true,
    "sortOrder": 190
  },
  {
    "id": "ice-tea",
    "name": "Ice Tea",
    "price": "120 TL",
    "calories": "120 kcal",
    "category": "coldDrinks",
    "description": "Soğuk servis edilen ferah ice tea.",
    "image": "https://loremflickr.com/900/700/iced,tea?lock=1664",
    "isActive": true,
    "sortOrder": 200
  },
  {
    "id": "soda",
    "name": "Soda",
    "price": "100 TL",
    "calories": "0 kcal",
    "category": "coldDrinks",
    "description": "Soğuk servis edilen sade maden suyu.",
    "image": "https://loremflickr.com/900/700/sparkling,water?lock=1423",
    "isActive": true,
    "sortOrder": 210
  },
  {
    "id": "ayran",
    "name": "Ayran",
    "price": "100 TL",
    "calories": "80 kcal",
    "category": "coldDrinks",
    "description": "Soğuk servis edilen geleneksel ayran.",
    "image": "https://loremflickr.com/900/700/yogurt,drink?lock=1539",
    "isActive": true,
    "sortOrder": 220
  },
  {
    "id": "su",
    "name": "Su",
    "price": "30 TL",
    "calories": "0 kcal",
    "category": "coldDrinks",
    "description": "Soğuk servis edilen şişe su.",
    "image": "https://loremflickr.com/900/700/water,bottle?lock=1232",
    "isActive": true,
    "sortOrder": 230
  },
  {
    "id": "extra-shot",
    "name": "Extra Shot",
    "price": "30 TL",
    "calories": "5 kcal",
    "category": "coldDrinks",
    "description": "Kahve içeceklerine ek espresso shot.",
    "image": "https://loremflickr.com/900/700/espresso,shot?lock=2039",
    "isActive": true,
    "sortOrder": 240
  },
  {
    "id": "sufle",
    "name": "Sufle",
    "price": "300 TL",
    "calories": "520 kcal",
    "category": "desserts",
    "description": "Akışkan çikolatalı sıcak sufle.",
    "image": "https://loremflickr.com/900/700/chocolate,souffle?lock=1543",
    "isActive": true,
    "sortOrder": 10
  },
  {
    "id": "magnolya",
    "name": "Magnolya",
    "price": "250 TL",
    "calories": "430 kcal",
    "category": "desserts",
    "description": "Kremalı magnolya tatlısı, seçilen meyveyle servis edilir.",
    "image": "https://loremflickr.com/900/700/dessert,cup,strawberry?lock=1856",
    "isActive": true,
    "sortOrder": 20,
    "options": [
      "Muz",
      "Çilek"
    ]
  },
  {
    "id": "cheesecake",
    "name": "Cheesecake",
    "price": "300 TL",
    "calories": "480 kcal",
    "category": "desserts",
    "description": "Kremamsı cheesecake, seçilen sosla servis edilir.",
    "image": "https://loremflickr.com/900/700/cheesecake,slice?lock=2025",
    "isActive": true,
    "sortOrder": 30,
    "options": [
      "Çilek",
      "Limon",
      "Frambuaz",
      "Çikolata"
    ]
  }
];

function normalizeProduct(product, index = 0) {
  return {
    isActive: true,
    sortOrder: index * 10,
    image: placeholderImage,
    options: [],
    ...product,
    category: product.category === "appetizers" ? "snacks" : product.category,
    options: Array.isArray(product.options)
      ? product.options.map((option) => String(option).trim()).filter(Boolean)
      : [],
  };
}

function applyMenuMeta(data = {}) {
  if (data.categoryLabels && typeof data.categoryLabels === "object") {
    Object.keys(categoryLabels).forEach((key) => delete categoryLabels[key]);
    Object.entries(data.categoryLabels).forEach(([key, value]) => {
      categoryLabels[key] = String(value);
    });
  }

  if (Array.isArray(data.categoryOrder) && data.categoryOrder.length > 0) {
    categoryOrder.splice(0, categoryOrder.length, ...data.categoryOrder.map(String));
  }
}

function readLocalProducts() {
  const saved = localStorage.getItem(MENU_STORAGE_KEY);

  if (!saved) {
    return defaultProducts.map(normalizeProduct);
  }

  try {
    const parsed = JSON.parse(saved);
    return Array.isArray(parsed) && parsed.length > 0
      ? parsed.map(normalizeProduct)
      : defaultProducts.map(normalizeProduct);
  } catch {
    return defaultProducts.map(normalizeProduct);
  }
}

function saveProducts(products) {
  localStorage.setItem(MENU_STORAGE_KEY, JSON.stringify(products));
}

async function apiRequest(path, options = {}) {
  const response = await fetch(path, {
    credentials: "same-origin",
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
    ...options,
  });

  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const error = new Error(data.error || "İşlem tamamlanamadı.");
    error.status = response.status;
    throw error;
  }

  return data;
}

async function readProducts(options = {}) {
  const endpoint = options.includeInactive ? "/api/admin/products" : "/api/products";

  try {
    const data = await apiRequest(endpoint);
    applyMenuMeta(data);
    return Array.isArray(data.products)
      ? data.products.map(normalizeProduct)
      : defaultProducts.map(normalizeProduct);
  } catch (error) {
    if (options.includeInactive || options.requireApi) {
      throw error;
    }

    return readLocalProducts();
  }
}

async function addProduct(product) {
  const data = await apiRequest("/api/admin/products", {
    method: "POST",
    body: JSON.stringify(normalizeProduct(product)),
  });
  return normalizeProduct(data.product);
}

async function updateProduct(productId, product) {
  const data = await apiRequest(`/api/admin/products/${encodeURIComponent(productId)}`, {
    method: "PUT",
    body: JSON.stringify(normalizeProduct({ ...product, id: productId })),
  });
  return normalizeProduct(data.product);
}

async function deleteProduct(productId) {
  return apiRequest(`/api/admin/products/${encodeURIComponent(productId)}`, {
    method: "DELETE",
  });
}

async function readCategories() {
  const data = await apiRequest("/api/admin/categories");
  applyMenuMeta(data);
  return Array.isArray(data.categories) ? data.categories : [];
}

async function addCategory(category) {
  const data = await apiRequest("/api/admin/categories", {
    method: "POST",
    body: JSON.stringify(category),
  });
  applyMenuMeta(data);
  return data.category;
}

async function updateCategory(categoryId, category) {
  const data = await apiRequest(`/api/admin/categories/${encodeURIComponent(categoryId)}`, {
    method: "PUT",
    body: JSON.stringify(category),
  });
  applyMenuMeta(data);
  return data.category;
}

async function deleteCategory(categoryId) {
  const data = await apiRequest(`/api/admin/categories/${encodeURIComponent(categoryId)}`, {
    method: "DELETE",
  });
  applyMenuMeta(data);
  return data;
}

async function login(username, password) {
  return apiRequest("/api/admin/login", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
}

async function logout() {
  return apiRequest("/api/admin/logout", {
    method: "POST",
    body: JSON.stringify({}),
  });
}

async function checkSession() {
  try {
    const data = await apiRequest("/api/admin/session");
    return Boolean(data.ok);
  } catch {
    return false;
  }
}

window.VanilyaMenuStore = {
  addProduct,
  addCategory,
  categoryLabels,
  categoryOrder,
  checkSession,
  deleteCategory,
  deleteProduct,
  defaultProducts,
  login,
  logout,
  placeholderImage,
  readCategories,
  readProducts,
  readLocalProducts,
  saveProducts,
  updateCategory,
  updateProduct,
};

window.NovaMenuStore = window.VanilyaMenuStore;
