const showcaseStore = window.VanilyaMenuStore || window.NovaMenuStore;
const showcaseCategories = showcaseStore.categoryOrder;
const showcaseLabels = showcaseStore.categoryLabels;
const categoryView = document.querySelector("#categoryView");
const menuView = document.querySelector("#menuView");
const categoryGrid = document.querySelector("#categoryGrid");
const categoryRail = document.querySelector("#categoryRail");
const productSections = document.querySelector("#productSections");
const backToCategories = document.querySelector("#backToCategories");
const seeAllButton = document.querySelector("#seeAllButton");
const productSheetAlt = document.querySelector("#productSheetAlt");
const closeSheetAlt = document.querySelector("#closeSheetAlt");
const closeSheetButtons = document.querySelectorAll("[data-close-sheet]");
const altSheetImage = document.querySelector("#altSheetImage");
const altSheetCategory = document.querySelector("#altSheetCategory");
const altSheetTitle = document.querySelector("#altSheetTitle");
const altSheetDescription = document.querySelector("#altSheetDescription");
const altSheetOptions = document.querySelector("#altSheetOptions");
const altSheetPrice = document.querySelector("#altSheetPrice");
const altSheetCalories = document.querySelector("#altSheetCalories");

let showcaseProducts = [];
let sectionObserver = null;
let categoryScrollLock = null;
let categoryScrollLockTimer = null;

function setPageMode(mode) {
  document.body.classList.toggle("is-landing-locked", mode === "categories");
  document.body.classList.toggle("is-menu-scroll", mode === "menu");
  document.querySelector(".showcase-app").dataset.view = mode;
}

function normalizePrice(price) {
  return String(price || "").replace("TL", "₺").trim();
}

function activeProducts() {
  const categoryRank = Object.fromEntries(showcaseCategories.map((category, index) => [category, index]));

  return showcaseProducts
    .filter((product) => product.isActive !== false)
    .sort(
      (a, b) =>
        (categoryRank[a.category] ?? 99) - (categoryRank[b.category] ?? 99) ||
        (a.sortOrder ?? 0) - (b.sortOrder ?? 0),
    );
}

function productsFor(category) {
  return activeProducts().filter((product) => product.category === category);
}

function categoryHeroImage(category) {
  return productsFor(category).find((product) => product.image)?.image || showcaseStore.placeholderImage;
}

function createImage(src, alt = "") {
  const image = document.createElement("img");
  image.src = src || showcaseStore.placeholderImage;
  image.alt = alt;

  image.addEventListener(
    "error",
    () => {
      image.src = showcaseStore.placeholderImage;
      image.classList.add("is-placeholder");
    },
    { once: true },
  );

  if (image.src.includes("vanilya-port-logo")) {
    image.classList.add("is-placeholder");
  }

  return image;
}

function renderCategoryGrid() {
  categoryGrid.textContent = "";

  showcaseCategories.forEach((category) => {
    const button = document.createElement("button");
    button.className = "category-card";
    button.type = "button";

    const imageWrap = document.createElement("span");
    imageWrap.className = "category-card-image";
    const image = createImage(categoryHeroImage(category), showcaseLabels[category]);
    if (image.classList.contains("is-placeholder")) {
      imageWrap.classList.add("is-placeholder");
    }
    imageWrap.append(image);

    const label = document.createElement("strong");
    label.textContent = showcaseLabels[category];

    button.append(imageWrap, label);
    button.addEventListener("click", () => showMenu(category));
    categoryGrid.append(button);
  });
}

function renderCategoryRail() {
  categoryRail.textContent = "";

  showcaseCategories.forEach((category) => {
    const button = document.createElement("button");
    button.className = "rail-button";
    button.type = "button";
    button.dataset.category = category;

    const image = createImage(categoryHeroImage(category), "");
    const label = document.createElement("span");
    label.textContent = showcaseLabels[category];

    button.append(image, label);
    button.addEventListener("click", () => scrollToCategory(category));
    categoryRail.append(button);
  });
}

function renderProductSections() {
  productSections.textContent = "";

  showcaseCategories.forEach((category) => {
    const products = productsFor(category);
    const section = document.createElement("section");
    section.className = "product-section";
    section.id = `showcase-${category}`;
    section.dataset.category = category;

    const cover = document.createElement("div");
    cover.className = "section-cover";
    cover.append(createImage(categoryHeroImage(category), showcaseLabels[category]));

    const title = document.createElement("div");
    title.className = "section-title";
    const heading = document.createElement("h2");
    heading.textContent = showcaseLabels[category];
    const count = document.createElement("span");
    count.textContent = `${products.length} ürün`;
    title.append(heading, count);

    const list = document.createElement("div");
    list.className = "product-list";

    products.forEach((product) => {
      const card = document.createElement("button");
      card.className = "product-card";
      card.type = "button";

      const image = createImage(product.image, product.name);
      const copy = document.createElement("span");
      copy.className = "product-copy";
      const name = document.createElement("strong");
      name.textContent = product.name;
      const description = document.createElement("small");
      description.textContent = product.description || showcaseLabels[product.category] || "";
      copy.append(name, description);

      const price = document.createElement("span");
      price.className = "product-price";
      price.textContent = normalizePrice(product.price);

      card.append(image, copy, price);
      card.addEventListener("click", () => openProductSheet(product));
      list.append(card);
    });

    section.append(cover, title, list);
    productSections.append(section);
  });
}

function setActiveCategory(category) {
  document.querySelectorAll(".rail-button").forEach((button) => {
    button.classList.toggle("is-active", button.dataset.category === category);
  });

  const active = document.querySelector(`.rail-button[data-category="${category}"]`);
  if (active) {
    const targetLeft = active.offsetLeft - categoryRail.clientWidth / 2 + active.clientWidth / 2;
    categoryRail.scrollTo({ left: Math.max(0, targetLeft), behavior: "smooth" });
  }
}

function stickyOffset() {
  const topbar = document.querySelector(".menu-topbar")?.getBoundingClientRect().height || 0;
  const filter = document.querySelector(".menu-filter-shell")?.getBoundingClientRect().height || 0;
  return topbar + filter + 14;
}

function observeSections() {
  sectionObserver?.disconnect();

  sectionObserver = new IntersectionObserver(
    (entries) => {
      if (categoryScrollLock) {
        return;
      }

      const visible = entries
        .filter((entry) => entry.isIntersecting)
        .sort((a, b) => b.intersectionRatio - a.intersectionRatio)[0];

      if (visible?.target?.dataset.category) {
        setActiveCategory(visible.target.dataset.category);
      }
    },
    { rootMargin: "-34% 0px -56% 0px", threshold: [0.08, 0.2, 0.42] },
  );

  document.querySelectorAll(".product-section").forEach((section) => sectionObserver.observe(section));
}

function scrollToCategory(category) {
  const section = document.querySelector(`#showcase-${category}`);
  if (!section) {
    return;
  }

  categoryScrollLock = category;
  window.clearTimeout(categoryScrollLockTimer);
  setActiveCategory(category);

  const targetTop = window.scrollY + section.getBoundingClientRect().top - stickyOffset();
  window.scrollTo({ top: Math.max(0, targetTop), behavior: "smooth" });

  categoryScrollLockTimer = window.setTimeout(() => {
    categoryScrollLock = null;
    setActiveCategory(category);
  }, 760);
}

function showMenu(category = showcaseCategories[0]) {
  categoryScrollLock = null;
  window.clearTimeout(categoryScrollLockTimer);
  window.scrollTo({ top: 0, behavior: "auto" });
  categoryView.hidden = true;
  menuView.hidden = false;
  setPageMode("menu");
  window.scrollTo({ top: 0, behavior: "auto" });
  renderCategoryRail();
  renderProductSections();
  observeSections();
  setActiveCategory(category);

  if (category !== showcaseCategories[0]) {
    window.setTimeout(() => scrollToCategory(category), 140);
  }
}

function showCategories() {
  window.scrollTo({ top: 0, behavior: "auto" });
  menuView.hidden = true;
  categoryView.hidden = false;
  setPageMode("categories");
  sectionObserver?.disconnect();
  window.scrollTo({ top: 0, behavior: "auto" });
}

function openProductSheet(product) {
  altSheetImage.src = product.image || showcaseStore.placeholderImage;
  altSheetImage.alt = product.name;
  altSheetCategory.textContent = showcaseLabels[product.category] || "Menü";
  altSheetTitle.textContent = product.name;
  altSheetDescription.textContent = product.description || "Vanilya Port seçkisinden özel lezzet.";
  altSheetOptions.innerHTML = "";
  const options = Array.isArray(product.options) ? product.options : [];
  altSheetOptions.hidden = options.length === 0;
  options.forEach((option) => {
    const chip = document.createElement("span");
    chip.textContent = option;
    altSheetOptions.append(chip);
  });
  altSheetPrice.textContent = normalizePrice(product.price);
  altSheetCalories.textContent = product.calories || "";
  productSheetAlt.classList.add("is-open");
  productSheetAlt.setAttribute("aria-hidden", "false");
}

function closeProductSheet() {
  productSheetAlt.classList.remove("is-open");
  productSheetAlt.setAttribute("aria-hidden", "true");
}

async function initShowcase() {
  setPageMode("categories");

  try {
    showcaseProducts = await showcaseStore.readProducts();
  } catch {
    showcaseProducts = showcaseStore.defaultProducts || [];
  }

  renderCategoryGrid();
}

backToCategories.addEventListener("click", showCategories);
seeAllButton.addEventListener("click", showCategories);
closeSheetAlt.addEventListener("click", closeProductSheet);
closeSheetButtons.forEach((button) => button.addEventListener("click", closeProductSheet));
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape") {
    closeProductSheet();
  }
});

document.addEventListener(
  "touchmove",
  (event) => {
    if (document.body.classList.contains("is-landing-locked")) {
      event.preventDefault();
    }
  },
  { passive: false },
);

initShowcase();
