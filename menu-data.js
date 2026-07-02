const MENU_STORAGE_KEY = "vanilya-port-products-v2";

const categoryLabels = {
  coldDrinks: "Soğuk İçecekler",
  hotDrinks: "Sıcak İçecekler",
  desserts: "Tatlılar",
  snacks: "Atıştırmalıklar",
};

const categoryOrder = ["coldDrinks", "hotDrinks", "desserts", "snacks"];

const placeholderImage =
  "./assets/vanilya-port-logo.jpg";

const defaultProducts = [
  {
    id: "patates-kizartmasi",
    name: "Patates Kızartması",
    price: "160 TL",
    calories: "420 kcal",
    category: "snacks",
    description: "Altın renkli çıtır patates, özel Vanilya Port sosuyla.",
    image:
      "https://images.unsplash.com/photo-1576107232684-1279f390859f?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 10,
  },
  {
    id: "mozzarella-sticks",
    name: "Mozzarella Sticks",
    price: "210 TL",
    calories: "510 kcal",
    category: "snacks",
    description: "Çıtır kaplama mozzarella, domates salsa ile servis edilir.",
    image:
      "https://images.unsplash.com/photo-1639024471283-03518883512d?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 20,
  },
  {
    id: "citir-tavuk",
    name: "Çıtır Tavuk",
    price: "240 TL",
    calories: "560 kcal",
    category: "snacks",
    description: "Baharatlı çıtır tavuk parçacıkları, ballı hardal sos ile.",
    image:
      "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 30,
  },
  {
    id: "turk-kahvesi",
    name: "Türk Kahvesi",
    price: "95 TL",
    calories: "25 kcal",
    category: "hotDrinks",
    description: "Geleneksel bakır cezvede hazırlanan bol köpüklü Türk kahvesi.",
    image:
      "https://images.unsplash.com/photo-1559496417-e7f25cb247f3?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 10,
  },
  {
    id: "latte",
    name: "Latte",
    price: "140 TL",
    calories: "150 kcal",
    category: "hotDrinks",
    description: "Yumuşak espresso, ipeksi süt dokusu ve zarif latte art.",
    image:
      "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 20,
  },
  {
    id: "cappuccino",
    name: "Cappuccino",
    price: "140 TL",
    calories: "130 kcal",
    category: "hotDrinks",
    description: "Dengeli espresso, yoğun süt köpüğü ve kakao dokunuşu.",
    image:
      "https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 30,
  },
  {
    id: "cay",
    name: "Çay",
    price: "55 TL",
    calories: "5 kcal",
    category: "hotDrinks",
    description: "İnce belli bardakta taze demlenmiş klasik çay.",
    image: placeholderImage,
    isActive: true,
    sortOrder: 40,
  },
  {
    id: "ice-latte",
    name: "Ice Latte",
    price: "155 TL",
    calories: "165 kcal",
    category: "coldDrinks",
    description: "Buz, espresso ve soğuk sütle ferah yaz klasiği.",
    image:
      "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 10,
  },
  {
    id: "limonata",
    name: "Limonata",
    price: "125 TL",
    calories: "120 kcal",
    category: "coldDrinks",
    description: "Taze limon, nane ve hafif şeker dengesiyle hazırlanır.",
    image:
      "https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 20,
  },
  {
    id: "milkshake",
    name: "Milkshake",
    price: "180 TL",
    calories: "390 kcal",
    category: "coldDrinks",
    description: "Vanilya aromalı kremamsı milkshake, soğuk servis.",
    image:
      "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 30,
  },
  {
    id: "soguk-cay",
    name: "Soğuk Çay",
    price: "115 TL",
    calories: "90 kcal",
    category: "coldDrinks",
    description: "Siyah çay, limon ve buzla hazırlanan hafif içecek.",
    image:
      "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 40,
  },
  {
    id: "san-sebastian",
    name: "San Sebastian Cheesecake",
    price: "245 TL",
    calories: "520 kcal",
    category: "desserts",
    description: "Kremamsı doku, karamelize üst ve isteğe bağlı çikolata sos.",
    image:
      "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 10,
  },
  {
    id: "brownie",
    name: "Brownie",
    price: "190 TL",
    calories: "460 kcal",
    category: "desserts",
    description: "Yoğun çikolata, nemli doku ve vanilyalı dondurma eşliği.",
    image:
      "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 20,
  },
  {
    id: "waffle",
    name: "Waffle",
    price: "260 TL",
    calories: "640 kcal",
    category: "desserts",
    description: "Mevsim meyveleri, çikolata ve çıtır waffle tabanı.",
    image:
      "https://images.unsplash.com/photo-1562376552-0d160a2f238d?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 30,
  },
  {
    id: "kruvasan",
    name: "Kruvasan",
    price: "135 TL",
    calories: "310 kcal",
    category: "snacks",
    description: "Tereyağlı kat kat kruvasan, sıcak servis edilir.",
    image:
      "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 40,
  },
  {
    id: "tost",
    name: "Tost",
    price: "165 TL",
    calories: "430 kcal",
    category: "snacks",
    description: "Kaşarlı ve sucuklu klasik tost, domates ve yeşillik ile.",
    image: placeholderImage,
    isActive: true,
    sortOrder: 50,
  },
  {
    id: "sandvic",
    name: "Sandviç",
    price: "195 TL",
    calories: "480 kcal",
    category: "snacks",
    description: "Taze ekmek, peynir, hindi füme, domates ve roka.",
    image:
      "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=900&q=80",
    isActive: true,
    sortOrder: 60,
  },
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
