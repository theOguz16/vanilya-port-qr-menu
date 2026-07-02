const store = window.VanilyaMenuStore || window.NovaMenuStore;
const categories = store.categoryOrder;
let pages = [];
const labels = store.categoryLabels;

let pageIndex = 0;
let touchStartX = 0;
let touchStartY = 0;
let isTurning = false;
let products = [];

const menuPage = document.querySelector("#menuPage");
const turnShadow = document.querySelector("#turnShadow");
const bookStage = document.querySelector("#bookStage");
const prevPage = document.querySelector("#prevPage");
const nextPage = document.querySelector("#nextPage");
const pageDots = document.querySelector("#pageDots");
const productSheet = document.querySelector("#productSheet");
const sheetImage = document.querySelector("#sheetImage");
const sheetTag = document.querySelector("#sheetTag");
const sheetTitle = document.querySelector("#sheetTitle");
const sheetDescription = document.querySelector("#sheetDescription");
const sheetPrice = document.querySelector("#sheetPrice");
const sheetCalories = document.querySelector("#sheetCalories");
const sheetOptions = document.querySelector("#sheetOptions");

function buildPages() {
  pages = [
    { type: "cover", label: "Hoş geldiniz" },
    ...categories.map((category) => ({ type: "category", category, label: labels[category] })),
    { type: "social", label: "Instagram" },
  ];
  if (pageIndex >= pages.length) {
    pageIndex = Math.max(0, pages.length - 1);
  }
}

function lockMenuViewportHeight() {
  const root = document.documentElement;
  let lockedWidth = window.innerWidth;

  function applyLock() {
    root.style.setProperty("--menu-locked-height", `${window.innerHeight}px`);
    lockedWidth = window.innerWidth;
  }

  applyLock();

  window.addEventListener("resize", () => {
    if (Math.abs(window.innerWidth - lockedWidth) > 24) {
      applyLock();
    }
  });

  window.addEventListener("orientationchange", () => {
    window.setTimeout(applyLock, 250);
  });
}

lockMenuViewportHeight();

function productsForCategory(category) {
  return products.filter((product) => product.category === category);
}

function sortProducts(productList) {
  const categoryRank = Object.fromEntries(categories.map((category, index) => [category, index]));

  return productList
    .filter((product) => product.isActive !== false)
    .sort(
      (a, b) =>
        (categoryRank[a.category] ?? 99) - (categoryRank[b.category] ?? 99) ||
        (a.sortOrder ?? 0) - (b.sortOrder ?? 0),
    );
}

function productImageSource(product) {
  return product.image || store.placeholderImage;
}

function applyImageFallback(image) {
  image.addEventListener(
    "error",
    () => {
      image.src = store.placeholderImage;
      image.classList.add("is-placeholder");
    },
    { once: true },
  );
}

async function initMenu() {
  try {
    products = sortProducts(await store.readProducts());
  } catch {
    products = sortProducts(store.defaultProducts || []);
  }

  buildPages();
  renderPage();
}

function renderDots() {
  pageDots.innerHTML = "";

  pages.forEach((page, index) => {
    const dot = document.createElement("button");
    dot.type = "button";
    dot.className = index === pageIndex ? "page-dot is-active" : "page-dot";
    dot.setAttribute("aria-label", `${page.label} sayfasına git`);
    dot.addEventListener("click", () => goToPage(index));
    pageDots.appendChild(dot);
  });
}

function renderPage() {
  const page = pages[pageIndex];
  menuPage.classList.remove("is-centered-page", "is-menu-page");

  if (page.type === "cover") {
    renderCoverPage();
    return;
  }

  if (page.type === "social") {
    renderSocialPage();
    return;
  }

  const category = page.category;
  const list = productsForCategory(category);
  menuPage.classList.add("is-menu-page");

  menuPage.innerHTML = `
    <div class="paper-accent-line"></div>
    <img class="page-vector page-vector-palm" src="./assets/palm-tree-icon.png" alt="" aria-hidden="true" />
    <img class="page-vector page-vector-umbrella" src="./assets/beach-umbrella-icon.png" alt="" aria-hidden="true" />
    <img class="page-vector page-vector-lounger" src="./assets/sunbed-icon.png" alt="" aria-hidden="true" />
    <img class="page-vector page-vector-waves" src="./assets/beach-icon.png" alt="" aria-hidden="true" />
    <div class="paper-topline">
      <span>Sayfa ${pageIndex + 1}/${pages.length}</span>
      <span>${list.length} ürün</span>
    </div>
    <div class="paper-title">
      <p class="hero-kicker">Menü</p>
      <h2>${labels[category]}</h2>
    </div>
    <div class="paper-items"></div>
  `;

  const itemWrap = menuPage.querySelector(".paper-items");
  if (list.length === 0) {
    itemWrap.innerHTML = `
      <div class="empty-menu-state">
        <strong>Bu sayfa hazırlanıyor</strong>
        <span>Yakında yeni Vanilya Port lezzetleri eklenecek.</span>
      </div>
    `;
  }

  list.forEach((product, index) => {
    const imageSrc = productImageSource(product);
    const imageClass = imageSrc === store.placeholderImage ? "product-thumb is-placeholder" : "product-thumb";
    const item = document.createElement("button");
    const photo = document.createElement("span");
    const image = document.createElement("img");
    const copy = document.createElement("span");
    const head = document.createElement("span");
    const name = document.createElement("strong");
    const price = document.createElement("b");
    const description = document.createElement("small");
    const calories = document.createElement("em");

    item.className = "paper-item";
    item.type = "button";
    item.style.animationDelay = `${index * 70}ms`;
    photo.className = "item-photo";
    image.className = imageClass;
    image.src = imageSrc;
    image.alt = product.name || "";
    image.loading = "lazy";
    applyImageFallback(image);

    copy.className = "item-copy";
    head.className = "item-head";
    name.textContent = product.name || "";
    price.textContent = product.price || "";
    description.textContent = product.description || "";
    calories.textContent = product.calories || "";

    photo.appendChild(image);
    head.append(name, price);
    copy.append(head, description, calories);
    item.append(photo, copy);
    item.addEventListener("click", () => openSheet(product));
    itemWrap.appendChild(item);
  });

  prevPage.disabled = pageIndex === 0;
  nextPage.disabled = pageIndex === pages.length - 1;
  renderDots();
}

function renderCoverPage() {
  menuPage.classList.add("is-centered-page");
  menuPage.innerHTML = `
    <div class="paper-accent-line"></div>
    <img class="page-vector page-vector-palm cover-vector" src="./assets/palm-tree-icon.png" alt="" aria-hidden="true" />
    <img class="page-vector page-vector-umbrella cover-vector" src="./assets/beach-umbrella-icon.png" alt="" aria-hidden="true" />
    <img class="page-vector page-vector-lounger cover-vector" src="./assets/sunbed-icon.png" alt="" aria-hidden="true" />
    <img class="page-vector page-vector-waves" src="./assets/beach-icon.png" alt="" aria-hidden="true" />
    <section class="cover-page">
      <div class="cover-ring">
        <img src="./assets/vanilya-port-logo.jpg" alt="Vanilya Port logosu" />
      </div>
      <div class="cover-meta">
        <span>Malkara</span>
        <span>Est. 2017</span>
      </div>
      <p class="hero-kicker">Food & Drink</p>
      <h2>VANİLYA PORT</h2>
      <span>Yazlık, sakin ve butik bir kafe deneyimi.</span>
      <small>Sayfayı sağa kaydırarak sahil esintili lezzetleri keşfedin.</small>
    </section>
  `;

  prevPage.disabled = true;
  nextPage.disabled = false;
  renderDots();
}

function renderSocialPage() {
  menuPage.classList.add("is-centered-page");
  menuPage.innerHTML = `
    <div class="paper-accent-line"></div>
    <img class="page-vector page-vector-palm cover-vector" src="./assets/palm-tree-icon.png" alt="" aria-hidden="true" />
    <img class="page-vector page-vector-umbrella cover-vector" src="./assets/beach-umbrella-icon.png" alt="" aria-hidden="true" />
    <img class="page-vector page-vector-lounger cover-vector" src="./assets/sunbed-icon.png" alt="" aria-hidden="true" />
    <img class="page-vector page-vector-waves" src="./assets/beach-icon.png" alt="" aria-hidden="true" />
    <section class="social-page">
      <img src="./assets/vanilya-port-logo.jpg" alt="Vanilya Port logosu" />
      <p class="hero-kicker">Vanilya Port</p>
      <h2>Instagram'da bizi etiketle</h2>
      <a href="https://www.instagram.com/vanilya_port" target="_blank" rel="noreferrer">@vanilya_port</a>
      <small>Masanızdan bir yaz anısı bırakın. Kahvenizi, tatlınızı veya gün batımı keyfinizi paylaşırken bizi etiketleyin.</small>
    </section>
  `;

  prevPage.disabled = false;
  nextPage.disabled = true;
  renderDots();
}

function animateTurn(direction) {
  const className = direction > 0 ? "is-turning-next" : "is-turning-prev";
  isTurning = true;
  turnShadow.className = `paper-page turn-shadow ${className}`;
  menuPage.classList.add(direction > 0 ? "page-leaves-left" : "page-leaves-right");

  window.setTimeout(() => {
    menuPage.classList.remove("page-leaves-left", "page-leaves-right");
    menuPage.classList.add(direction > 0 ? "page-enters-right" : "page-enters-left");
    renderPage();
  }, 330);

  window.setTimeout(() => {
    menuPage.classList.remove("page-enters-right", "page-enters-left");
    turnShadow.className = "paper-page turn-shadow";
    isTurning = false;
  }, 750);
}

function goToPage(nextIndex) {
  if (isTurning || nextIndex === pageIndex || nextIndex < 0 || nextIndex >= pages.length) {
    return;
  }

  const direction = nextIndex > pageIndex ? 1 : -1;
  pageIndex = nextIndex;
  animateTurn(direction);
}

function openSheet(product) {
  sheetImage.src = productImageSource(product);
  sheetImage.alt = product.name;
  applyImageFallback(sheetImage);
  sheetTag.textContent = labels[product.category] || product.category;
  sheetTitle.textContent = product.name;
  sheetDescription.textContent = product.description;
  sheetPrice.textContent = product.price;
  sheetCalories.textContent = product.calories || "";
  sheetOptions.innerHTML = "";
  const options = Array.isArray(product.options) ? product.options : [];
  sheetOptions.hidden = options.length === 0;
  options.forEach((option) => {
    const chip = document.createElement("span");
    chip.textContent = option;
    sheetOptions.append(chip);
  });
  productSheet.classList.add("is-open");
  productSheet.setAttribute("aria-hidden", "false");
}

function closeSheet() {
  productSheet.classList.remove("is-open");
  productSheet.setAttribute("aria-hidden", "true");
}

prevPage.addEventListener("click", () => goToPage(pageIndex - 1));
nextPage.addEventListener("click", () => goToPage(pageIndex + 1));

bookStage.addEventListener("touchstart", (event) => {
  touchStartX = event.touches[0].clientX;
  touchStartY = event.touches[0].clientY;
});

bookStage.addEventListener("touchend", (event) => {
  const touch = event.changedTouches[0];
  const deltaX = touch.clientX - touchStartX;
  const deltaY = touch.clientY - touchStartY;

  if (Math.abs(deltaX) < 48 || Math.abs(deltaX) < Math.abs(deltaY)) {
    return;
  }

  goToPage(deltaX < 0 ? pageIndex + 1 : pageIndex - 1);
});

bookStage.addEventListener("pointerup", (event) => {
  if (event.pointerType === "touch") {
    return;
  }

  if (event.target.closest(".paper-item")) {
    return;
  }

  const stageRect = bookStage.getBoundingClientRect();
  const clickX = event.clientX - stageRect.left;

  if (clickX > stageRect.width * 0.68) {
    goToPage(pageIndex + 1);
  }

  if (clickX < stageRect.width * 0.32) {
    goToPage(pageIndex - 1);
  }
});

document.querySelectorAll("[data-close-sheet]").forEach((button) => {
  button.addEventListener("click", closeSheet);
});

document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeSheet();
  }

  if (event.key === "ArrowRight") {
    goToPage(pageIndex + 1);
  }

  if (event.key === "ArrowLeft") {
    goToPage(pageIndex - 1);
  }
});

initMenu();
