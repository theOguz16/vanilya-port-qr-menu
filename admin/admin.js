const loginForm = document.querySelector("#loginForm");
const loginStatus = document.querySelector("#loginStatus");
const adminLogin = document.querySelector("#adminLogin");
const adminDashboard = document.querySelector("#adminDashboard");
const logoutButton = document.querySelector("#logoutButton");
const form = document.querySelector("#productForm");
const imageInput = document.querySelector("#imageInput");
const imagePreview = document.querySelector("#imagePreview");
const formStatus = document.querySelector("#formStatus");
const adminProducts = document.querySelector("#adminProducts");
const adminCount = document.querySelector("#adminCount");
const adminCategoryTabs = document.querySelector("#adminCategoryTabs");
const saveButton = document.querySelector("#saveButton");
const cancelEdit = document.querySelector("#cancelEdit");
const store = window.VanilyaMenuStore || window.NovaMenuStore;

let uploadedImage = "";
let editingProductId = "";
let selectedCategory = store.categoryOrder[0];
let productsCache = [];

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function fileToDataUrl(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.addEventListener("load", () => resolve(reader.result));
    reader.addEventListener("error", () => reject(new Error("Fotoğraf okunamadı.")));
    reader.readAsDataURL(file);
  });
}

function showLogin(message = "") {
  adminLogin.hidden = false;
  adminDashboard.hidden = true;
  loginStatus.textContent = message;
}

function showDashboard() {
  adminLogin.hidden = true;
  adminDashboard.hidden = false;
}

function sortedProducts() {
  const categoryRank = Object.fromEntries(store.categoryOrder.map((category, index) => [category, index]));

  return [...productsCache].sort(
    (a, b) =>
      (categoryRank[a.category] ?? 99) - (categoryRank[b.category] ?? 99) ||
      (a.sortOrder ?? 0) - (b.sortOrder ?? 0),
  );
}

async function loadProducts() {
  productsCache = await store.readProducts({ includeInactive: true, requireApi: true });
}

function resetFormState(message = "") {
  form.reset();
  uploadedImage = "";
  editingProductId = "";
  imagePreview.removeAttribute("src");
  imagePreview.classList.remove("is-visible");
  saveButton.textContent = "Ürünü ekle";
  cancelEdit.hidden = true;
  formStatus.textContent = message;
}

function renderCategoryTabs() {
  const products = sortedProducts();
  adminCategoryTabs.innerHTML = "";

  store.categoryOrder.forEach((category) => {
    const count = products.filter((product) => product.category === category).length;
    const button = document.createElement("button");
    button.type = "button";
    button.className = category === selectedCategory ? "admin-category-tab is-active" : "admin-category-tab";
    button.dataset.category = category;
    button.innerHTML = `
      <span>${escapeHtml(store.categoryLabels[category])}</span>
      <strong>${count}</strong>
    `;
    adminCategoryTabs.appendChild(button);
  });
}

function renderAdminProducts() {
  const products = sortedProducts();
  const filteredProducts = products.filter((product) => product.category === selectedCategory);

  adminCount.textContent = `${filteredProducts.length}/${products.length} ürün`;
  adminProducts.innerHTML = "";
  renderCategoryTabs();

  if (filteredProducts.length === 0) {
    adminProducts.innerHTML = `
      <div class="admin-empty-state">
        <strong>${escapeHtml(store.categoryLabels[selectedCategory])}</strong>
        <span>Bu kategoriye henüz ürün eklenmedi.</span>
      </div>
    `;
    return;
  }

  filteredProducts.forEach((product) => {
    const row = document.createElement("article");
    row.className = product.isActive === false ? "admin-product-row is-passive" : "admin-product-row";
    row.innerHTML = `
      <img src="${escapeHtml(product.image || store.placeholderImage)}" alt="${escapeHtml(product.name)}" />
      <span class="admin-product-copy">
        <strong>${escapeHtml(product.name)}</strong>
        <small>${escapeHtml(product.calories)} · Sıra ${escapeHtml(product.sortOrder ?? 0)}</small>
      </span>
      <b>${escapeHtml(product.price)}</b>
      <em>${product.isActive === false ? "Pasif" : "Aktif"}</em>
      <div class="admin-row-actions">
        <button type="button" data-action="edit" data-id="${escapeHtml(product.id)}">Düzenle</button>
        <button type="button" data-action="delete" data-id="${escapeHtml(product.id)}">Sil</button>
      </div>
    `;
    adminProducts.appendChild(row);
  });
}

function productFromForm(existingProduct) {
  const formData = new FormData(form);

  return {
    ...(existingProduct || {}),
    name: formData.get("name").trim(),
    price: formData.get("price").trim(),
    category: formData.get("category"),
    calories: formData.get("calories").trim(),
    description: formData.get("description").trim(),
    image: uploadedImage || existingProduct?.image || store.placeholderImage,
    isActive: formData.get("isActive") === "true",
    sortOrder: Number(formData.get("sortOrder")) || 0,
  };
}

function startEdit(productId) {
  const product = productsCache.find((item) => item.id === productId);

  if (!product) {
    return;
  }

  editingProductId = product.id;
  uploadedImage = "";
  form.elements.name.value = product.name;
  form.elements.price.value = product.price;
  form.elements.category.value = product.category;
  form.elements.calories.value = product.calories || "";
  form.elements.sortOrder.value = product.sortOrder ?? 0;
  form.elements.isActive.value = product.isActive === false ? "false" : "true";
  form.elements.description.value = product.description || "";
  imagePreview.src = product.image || store.placeholderImage;
  imagePreview.classList.add("is-visible");
  saveButton.textContent = "Ürünü güncelle";
  cancelEdit.hidden = false;
  formStatus.textContent = `${product.name} düzenleniyor.`;
  form.scrollIntoView({ behavior: "smooth", block: "start" });
}

async function deleteProduct(productId) {
  const product = productsCache.find((item) => item.id === productId);

  if (!product || !window.confirm(`${product.name} silinsin mi?`)) {
    return;
  }

  await store.deleteProduct(productId);

  if (editingProductId === productId) {
    resetFormState();
  }

  await loadProducts();
  formStatus.textContent = `${product.name} silindi.`;
  renderAdminProducts();
}

async function refreshDashboard() {
  await loadProducts();
  showDashboard();
  renderAdminProducts();
}

imageInput.addEventListener("change", async () => {
  const file = imageInput.files?.[0];

  if (!file) {
    uploadedImage = "";
    imagePreview.removeAttribute("src");
    imagePreview.classList.remove("is-visible");
    return;
  }

  uploadedImage = await fileToDataUrl(file);
  imagePreview.src = uploadedImage;
  imagePreview.classList.add("is-visible");
});

loginForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const formData = new FormData(loginForm);
  loginStatus.textContent = "Giriş kontrol ediliyor...";

  try {
    await store.login(formData.get("username").trim(), formData.get("password"));
    loginForm.reset();
    await refreshDashboard();
  } catch (error) {
    showLogin(error.message || "Giriş yapılamadı.");
  }
});

logoutButton.addEventListener("click", async () => {
  await store.logout();
  resetFormState();
  productsCache = [];
  showLogin("Oturum kapatıldı.");
});

adminCategoryTabs.addEventListener("click", (event) => {
  const button = event.target.closest("[data-category]");

  if (!button) {
    return;
  }

  selectedCategory = button.dataset.category;
  renderAdminProducts();
});

adminProducts.addEventListener("click", (event) => {
  const button = event.target.closest("[data-action]");

  if (!button) {
    return;
  }

  if (button.dataset.action === "edit") {
    startEdit(button.dataset.id);
  }

  if (button.dataset.action === "delete") {
    deleteProduct(button.dataset.id).catch((error) => {
      formStatus.textContent = error.message || "Ürün silinemedi.";
    });
  }
});

cancelEdit.addEventListener("click", () => {
  resetFormState("Düzenleme iptal edildi.");
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const file = imageInput.files?.[0];
  const existingProduct = productsCache.find((item) => item.id === editingProductId);

  saveButton.disabled = true;
  formStatus.textContent = "Kaydediliyor...";

  try {
    if (!uploadedImage && file) {
      uploadedImage = await fileToDataUrl(file);
    }

    if (editingProductId && existingProduct) {
      const updatedProduct = await store.updateProduct(editingProductId, productFromForm(existingProduct));
      selectedCategory = updatedProduct.category;
      resetFormState(`${updatedProduct.name} güncellendi.`);
    } else {
      const product = await store.addProduct(productFromForm());
      selectedCategory = product.category;
      resetFormState(`${product.name} menüye eklendi.`);
    }

    await loadProducts();
    renderAdminProducts();
  } catch (error) {
    formStatus.textContent = error.message || "Ürün kaydedilemedi.";
  } finally {
    saveButton.disabled = false;
  }
});

async function initAdmin() {
  const hasSession = await store.checkSession();

  if (!hasSession) {
    showLogin();
    return;
  }

  try {
    await refreshDashboard();
  } catch {
    showLogin("Oturum süresi doldu. Lütfen tekrar giriş yapın.");
  }
}

initAdmin();
