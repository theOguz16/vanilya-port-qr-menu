#!/usr/bin/env python3
import argparse
import base64
import json
import mimetypes
import secrets
import sqlite3
import time
from datetime import datetime, timezone
from http import HTTPStatus
from http.cookies import SimpleCookie
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import unquote, urlparse


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = BASE_DIR / "uploads"
DB_PATH = DATA_DIR / "vanilya_port.sqlite3"
MAX_BODY_BYTES = 12 * 1024 * 1024
SESSION_COOKIE = "vp_session"
ADMIN_USERNAME = "VanilyaPort"
ADMIN_PASSWORD = "Vanilya2017Port"

DEFAULT_CATEGORY_LABELS = {
    "coldDrinks": "Soğuk İçecekler",
    "hotDrinks": "Sıcak İçecekler",
    "desserts": "Tatlılar",
    "snacks": "Atıştırmalıklar",
}
DEFAULT_CATEGORY_ORDER = ["coldDrinks", "hotDrinks", "desserts", "snacks"]
PLACEHOLDER_IMAGE = "./assets/vanilya-port-logo.jpg"
DEFAULT_PRODUCT_OPTIONS = {
    "ice-latte": ["Klasik", "Vanilyalı", "Karamelli"],
    "milkshake": ["Çilekli", "Vanilyalı", "Karamelli"],
    "limonata": ["Klasik", "Naneli", "Çilekli"],
    "brownie": ["Sade", "Dondurmalı"],
    "citir-tavuk": ["Acısız", "Acılı"],
    "tost": ["Kaşarlı", "Sucuklu", "Karışık"],
}

SEED_PRODUCTS = [
    {
        "id": "ice-latte",
        "name": "Ice Latte",
        "price": "155 TL",
        "calories": "165 kcal",
        "category": "coldDrinks",
        "description": "Buz, espresso ve soğuk sütle ferah yaz klasiği.",
        "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=80",
        "options": DEFAULT_PRODUCT_OPTIONS["ice-latte"],
        "isActive": True,
        "sortOrder": 10,
    },
    {
        "id": "limonata",
        "name": "Limonata",
        "price": "125 TL",
        "calories": "120 kcal",
        "category": "coldDrinks",
        "description": "Taze limon, nane ve hafif şeker dengesiyle hazırlanır.",
        "image": "https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&w=900&q=80",
        "options": DEFAULT_PRODUCT_OPTIONS["limonata"],
        "isActive": True,
        "sortOrder": 20,
    },
    {
        "id": "milkshake",
        "name": "Milkshake",
        "price": "180 TL",
        "calories": "390 kcal",
        "category": "coldDrinks",
        "description": "Vanilya aromalı kremamsı milkshake, soğuk servis.",
        "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=900&q=80",
        "options": DEFAULT_PRODUCT_OPTIONS["milkshake"],
        "isActive": True,
        "sortOrder": 30,
    },
    {
        "id": "soguk-cay",
        "name": "Soğuk Çay",
        "price": "115 TL",
        "calories": "90 kcal",
        "category": "coldDrinks",
        "description": "Siyah çay, limon ve buzla hazırlanan hafif içecek.",
        "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=80",
        "isActive": True,
        "sortOrder": 40,
    },
    {
        "id": "turk-kahvesi",
        "name": "Türk Kahvesi",
        "price": "95 TL",
        "calories": "25 kcal",
        "category": "hotDrinks",
        "description": "Geleneksel bakır cezvede hazırlanan bol köpüklü Türk kahvesi.",
        "image": "https://images.unsplash.com/photo-1559496417-e7f25cb247f3?auto=format&fit=crop&w=900&q=80",
        "isActive": True,
        "sortOrder": 10,
    },
    {
        "id": "latte",
        "name": "Latte",
        "price": "140 TL",
        "calories": "150 kcal",
        "category": "hotDrinks",
        "description": "Yumuşak espresso, ipeksi süt dokusu ve zarif latte art.",
        "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=80",
        "isActive": True,
        "sortOrder": 20,
    },
    {
        "id": "cappuccino",
        "name": "Cappuccino",
        "price": "140 TL",
        "calories": "130 kcal",
        "category": "hotDrinks",
        "description": "Dengeli espresso, yoğun süt köpüğü ve kakao dokunuşu.",
        "image": "https://images.unsplash.com/photo-1534778101976-62847782c213?auto=format&fit=crop&w=900&q=80",
        "isActive": True,
        "sortOrder": 30,
    },
    {
        "id": "cay",
        "name": "Çay",
        "price": "55 TL",
        "calories": "5 kcal",
        "category": "hotDrinks",
        "description": "İnce belli bardakta taze demlenmiş klasik çay.",
        "image": PLACEHOLDER_IMAGE,
        "isActive": True,
        "sortOrder": 40,
    },
    {
        "id": "san-sebastian",
        "name": "San Sebastian Cheesecake",
        "price": "245 TL",
        "calories": "520 kcal",
        "category": "desserts",
        "description": "Kremamsı doku, karamelize üst ve isteğe bağlı çikolata sos.",
        "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=900&q=80",
        "isActive": True,
        "sortOrder": 10,
    },
    {
        "id": "brownie",
        "name": "Brownie",
        "price": "190 TL",
        "calories": "460 kcal",
        "category": "desserts",
        "description": "Yoğun çikolata, nemli doku ve vanilyalı dondurma eşliği.",
        "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=900&q=80",
        "options": DEFAULT_PRODUCT_OPTIONS["brownie"],
        "isActive": True,
        "sortOrder": 20,
    },
    {
        "id": "waffle",
        "name": "Waffle",
        "price": "260 TL",
        "calories": "640 kcal",
        "category": "desserts",
        "description": "Mevsim meyveleri, çikolata ve çıtır waffle tabanı.",
        "image": "https://images.unsplash.com/photo-1562376552-0d160a2f238d?auto=format&fit=crop&w=900&q=80",
        "isActive": True,
        "sortOrder": 30,
    },
    {
        "id": "patates-kizartmasi",
        "name": "Patates Kızartması",
        "price": "160 TL",
        "calories": "420 kcal",
        "category": "snacks",
        "description": "Altın renkli çıtır patates, özel Vanilya Port sosuyla.",
        "image": "https://images.unsplash.com/photo-1576107232684-1279f390859f?auto=format&fit=crop&w=900&q=80",
        "isActive": True,
        "sortOrder": 10,
    },
    {
        "id": "mozzarella-sticks",
        "name": "Mozzarella Sticks",
        "price": "210 TL",
        "calories": "510 kcal",
        "category": "snacks",
        "description": "Çıtır kaplama mozzarella, domates salsa ile servis edilir.",
        "image": "https://images.unsplash.com/photo-1639024471283-03518883512d?auto=format&fit=crop&w=900&q=80",
        "isActive": True,
        "sortOrder": 20,
    },
    {
        "id": "citir-tavuk",
        "name": "Çıtır Tavuk",
        "price": "240 TL",
        "calories": "560 kcal",
        "category": "snacks",
        "description": "Baharatlı çıtır tavuk parçacıkları, ballı hardal sos ile.",
        "image": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=900&q=80",
        "options": DEFAULT_PRODUCT_OPTIONS["citir-tavuk"],
        "isActive": True,
        "sortOrder": 30,
    },
    {
        "id": "kruvasan",
        "name": "Kruvasan",
        "price": "135 TL",
        "calories": "310 kcal",
        "category": "snacks",
        "description": "Tereyağlı kat kat kruvasan, sıcak servis edilir.",
        "image": "https://images.unsplash.com/photo-1555507036-ab1f4038808a?auto=format&fit=crop&w=900&q=80",
        "isActive": True,
        "sortOrder": 40,
    },
    {
        "id": "tost",
        "name": "Tost",
        "price": "165 TL",
        "calories": "430 kcal",
        "category": "snacks",
        "description": "Kaşarlı ve sucuklu klasik tost, domates ve yeşillik ile.",
        "image": PLACEHOLDER_IMAGE,
        "options": DEFAULT_PRODUCT_OPTIONS["tost"],
        "isActive": True,
        "sortOrder": 50,
    },
    {
        "id": "sandvic",
        "name": "Sandviç",
        "price": "195 TL",
        "calories": "480 kcal",
        "category": "snacks",
        "description": "Taze ekmek, peynir, hindi füme, domates ve roka.",
        "image": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?auto=format&fit=crop&w=900&q=80",
        "isActive": True,
        "sortOrder": 60,
    },
]


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def db_connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def column_exists(conn, table, column):
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(row["name"] == column for row in rows)


def init_db():
    DATA_DIR.mkdir(exist_ok=True)
    UPLOAD_DIR.mkdir(exist_ok=True)
    with db_connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS products (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                price TEXT NOT NULL,
                calories TEXT NOT NULL,
                category TEXT NOT NULL,
                description TEXT NOT NULL,
                image TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 1,
                sort_order INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        if not column_exists(conn, "products", "options_json"):
            conn.execute("ALTER TABLE products ADD COLUMN options_json TEXT NOT NULL DEFAULT '[]'")
        for product_id, options in DEFAULT_PRODUCT_OPTIONS.items():
            conn.execute(
                """
                UPDATE products
                SET options_json = ?
                WHERE id = ? AND (options_json IS NULL OR options_json = '' OR options_json = '[]')
                """,
                (json.dumps(options, ensure_ascii=False), product_id),
            )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS categories (
                id TEXT PRIMARY KEY,
                label TEXT NOT NULL,
                sort_order INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS sessions (
                token TEXT PRIMARY KEY,
                created_at TEXT NOT NULL
            )
            """
        )
        category_count = conn.execute("SELECT COUNT(*) AS count FROM categories").fetchone()["count"]
        if category_count == 0:
            now = utc_now()
            conn.executemany(
                """
                INSERT INTO categories (id, label, sort_order, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                [
                    (category, DEFAULT_CATEGORY_LABELS[category], index * 10, now, now)
                    for index, category in enumerate(DEFAULT_CATEGORY_ORDER)
                ],
            )
        count = conn.execute("SELECT COUNT(*) AS count FROM products").fetchone()["count"]
        if count == 0:
            now = utc_now()
            conn.executemany(
                """
                INSERT INTO products (
                    id, name, price, calories, category, description, image,
                    is_active, sort_order, options_json, created_at, updated_at
                )
                VALUES (
                    :id, :name, :price, :calories, :category, :description, :image,
                    :is_active, :sort_order, :options_json, :created_at, :updated_at
                )
                """,
                [
                    {
                        **product,
                        "is_active": 1 if product["isActive"] else 0,
                        "sort_order": product["sortOrder"],
                        "options_json": json.dumps(product.get("options", []), ensure_ascii=False),
                        "created_at": now,
                        "updated_at": now,
                    }
                    for product in SEED_PRODUCTS
                ],
            )


def product_from_row(row):
    try:
        options = json.loads(row["options_json"] or "[]")
    except (TypeError, json.JSONDecodeError):
        options = []

    return {
        "id": row["id"],
        "name": row["name"],
        "price": row["price"],
        "calories": row["calories"],
        "category": row["category"],
        "description": row["description"],
        "image": row["image"],
        "options": [str(option).strip() for option in options if str(option).strip()],
        "isActive": bool(row["is_active"]),
        "sortOrder": row["sort_order"],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
    }


def category_from_row(row):
    return {
        "id": row["id"],
        "label": row["label"],
        "sortOrder": row["sort_order"],
        "createdAt": row["created_at"],
        "updatedAt": row["updated_at"],
    }


def category_meta(conn):
    rows = conn.execute("SELECT * FROM categories ORDER BY sort_order, label").fetchall()
    categories = [category_from_row(row) for row in rows]
    if not categories:
        categories = [
            {"id": category, "label": DEFAULT_CATEGORY_LABELS[category], "sortOrder": index * 10}
            for index, category in enumerate(DEFAULT_CATEGORY_ORDER)
        ]
    return {
        "categories": categories,
        "categoryLabels": {category["id"]: category["label"] for category in categories},
        "categoryOrder": [category["id"] for category in categories],
    }


def products_payload(products, meta):
    return {
        "products": products,
        "categories": meta["categories"],
        "categoryLabels": meta["categoryLabels"],
        "categoryOrder": meta["categoryOrder"],
        "placeholderImage": PLACEHOLDER_IMAGE,
    }


def normalize_options(value):
    if isinstance(value, list):
        source = value
    elif isinstance(value, str):
        source = value.splitlines()
    else:
        source = []
    return [str(option).strip() for option in source if str(option).strip()]


def normalize_payload(payload, category_labels):
    category = payload.get("category") or "coldDrinks"
    if category == "appetizers":
        category = "snacks"
    if category not in category_labels:
        category = next(iter(category_labels), "coldDrinks")

    return {
        "id": str(payload.get("id") or f"urun-{int(time.time() * 1000)}-{secrets.token_hex(3)}"),
        "name": str(payload.get("name") or "").strip(),
        "price": str(payload.get("price") or "").strip(),
        "calories": str(payload.get("calories") or "").strip(),
        "category": category,
        "description": str(payload.get("description") or "").strip(),
        "image": str(payload.get("image") or PLACEHOLDER_IMAGE).strip(),
        "options_json": json.dumps(normalize_options(payload.get("options")), ensure_ascii=False),
        "is_active": 1 if payload.get("isActive", True) is not False else 0,
        "sort_order": int(payload.get("sortOrder") or 0),
    }


def category_id_from_label(label):
    value = str(label or "").strip().lower()
    replacements = str.maketrans("çğıöşüı", "cgiosui")
    value = value.translate(replacements)
    slug = []
    previous_dash = False
    for char in value:
        if char.isalnum():
            slug.append(char)
            previous_dash = False
        elif not previous_dash:
            slug.append("-")
            previous_dash = True
    result = "".join(slug).strip("-")
    return result or f"kategori-{int(time.time() * 1000)}"


def normalize_category_payload(payload, existing_id=""):
    label = str(payload.get("label") or "").strip()
    category_id = str(payload.get("id") or existing_id or category_id_from_label(label)).strip()
    return {
        "id": category_id,
        "label": label,
        "sort_order": int(payload.get("sortOrder") or 0),
    }


def save_data_url(value):
    if not value.startswith("data:image/") or ";base64," not in value:
        return value or PLACEHOLDER_IMAGE

    header, encoded = value.split(",", 1)
    mime = header[5:].split(";", 1)[0]
    ext = {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/webp": "webp",
        "image/gif": "gif",
    }.get(mime)
    if not ext:
        raise ValueError("Desteklenmeyen görsel formatı.")

    raw = base64.b64decode(encoded, validate=True)
    filename = f"product-{int(time.time() * 1000)}-{secrets.token_hex(5)}.{ext}"
    (UPLOAD_DIR / filename).write_bytes(raw)
    return f"/uploads/{filename}"


def is_safe_child(path, parent):
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def delete_upload_if_local(image_path):
    if not image_path.startswith("/uploads/"):
        return

    target = (BASE_DIR / image_path.lstrip("/")).resolve()
    if is_safe_child(target, UPLOAD_DIR) and target.exists():
        target.unlink()


class VanilyaPortHandler(BaseHTTPRequestHandler):
    server_version = "VanilyaPortQR/1.0"

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/products":
            return self.handle_products(active_only=True)
        if path == "/api/admin/products":
            return self.with_auth(lambda: self.handle_products(active_only=False))
        if path == "/api/admin/categories":
            return self.with_auth(self.handle_categories)
        if path == "/api/admin/session":
            return self.write_json({"ok": self.is_authenticated()})
        return self.serve_static(path)

    def do_POST(self):
        path = urlparse(self.path).path
        if path == "/api/admin/login":
            return self.handle_login()
        if path == "/api/admin/logout":
            return self.handle_logout()
        if path == "/api/admin/products":
            return self.with_auth(self.create_product)
        if path == "/api/admin/categories":
            return self.with_auth(self.create_category)
        return self.write_json({"error": "Bulunamadı."}, HTTPStatus.NOT_FOUND)

    def do_PUT(self):
        path = urlparse(self.path).path
        if path.startswith("/api/admin/products/"):
            product_id = unquote(path.rsplit("/", 1)[-1])
            return self.with_auth(lambda: self.update_product(product_id))
        if path.startswith("/api/admin/categories/"):
            category_id = unquote(path.rsplit("/", 1)[-1])
            return self.with_auth(lambda: self.update_category(category_id))
        return self.write_json({"error": "Bulunamadı."}, HTTPStatus.NOT_FOUND)

    def do_DELETE(self):
        path = urlparse(self.path).path
        if path.startswith("/api/admin/products/"):
            product_id = unquote(path.rsplit("/", 1)[-1])
            return self.with_auth(lambda: self.delete_product(product_id))
        if path.startswith("/api/admin/categories/"):
            category_id = unquote(path.rsplit("/", 1)[-1])
            return self.with_auth(lambda: self.delete_category(category_id))
        return self.write_json({"error": "Bulunamadı."}, HTTPStatus.NOT_FOUND)

    def handle_products(self, active_only):
        where = "WHERE is_active = 1" if active_only else ""
        with db_connect() as conn:
            meta = category_meta(conn)
            rank_case = " ".join(
                f"WHEN '{category}' THEN {index}" for index, category in enumerate(meta["categoryOrder"])
            )
            rows = conn.execute(
                f"""
                SELECT * FROM products
                {where}
                ORDER BY CASE category {rank_case} ELSE 99 END, sort_order, name
                """
            ).fetchall()
        return self.write_json(products_payload([product_from_row(row) for row in rows], meta))

    def handle_categories(self):
        with db_connect() as conn:
            meta = category_meta(conn)
        return self.write_json({"categories": meta["categories"], "categoryLabels": meta["categoryLabels"], "categoryOrder": meta["categoryOrder"]})

    def create_category(self):
        payload = normalize_category_payload(self.read_json())
        if not payload["label"]:
            return self.write_json({"error": "Kategori adı zorunlu."}, HTTPStatus.BAD_REQUEST)

        now = utc_now()
        with db_connect() as conn:
            existing = conn.execute("SELECT id FROM categories WHERE id = ?", (payload["id"],)).fetchone()
            if existing:
                payload["id"] = f"{payload['id']}-{secrets.token_hex(2)}"
            conn.execute(
                """
                INSERT INTO categories (id, label, sort_order, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (payload["id"], payload["label"], payload["sort_order"], now, now),
            )
            row = conn.execute("SELECT * FROM categories WHERE id = ?", (payload["id"],)).fetchone()
            meta = category_meta(conn)
        return self.write_json({"category": category_from_row(row), **meta}, HTTPStatus.CREATED)

    def update_category(self, category_id):
        payload = normalize_category_payload(self.read_json(), existing_id=category_id)
        if not payload["label"]:
            return self.write_json({"error": "Kategori adı zorunlu."}, HTTPStatus.BAD_REQUEST)

        now = utc_now()
        with db_connect() as conn:
            existing = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
            if not existing:
                return self.write_json({"error": "Kategori bulunamadı."}, HTTPStatus.NOT_FOUND)
            conn.execute(
                """
                UPDATE categories
                SET label = ?, sort_order = ?, updated_at = ?
                WHERE id = ?
                """,
                (payload["label"], payload["sort_order"], now, category_id),
            )
            row = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
            meta = category_meta(conn)
        return self.write_json({"category": category_from_row(row), **meta})

    def delete_category(self, category_id):
        with db_connect() as conn:
            existing = conn.execute("SELECT * FROM categories WHERE id = ?", (category_id,)).fetchone()
            if not existing:
                return self.write_json({"error": "Kategori bulunamadı."}, HTTPStatus.NOT_FOUND)
            category_count = conn.execute("SELECT COUNT(*) AS count FROM categories").fetchone()["count"]
            if category_count <= 1:
                return self.write_json({"error": "Son kategori silinemez."}, HTTPStatus.BAD_REQUEST)
            product_count = conn.execute(
                "SELECT COUNT(*) AS count FROM products WHERE category = ?",
                (category_id,),
            ).fetchone()["count"]
            if product_count:
                return self.write_json(
                    {"error": "Bu kategoride ürün var. Önce ürünleri başka kategoriye taşı veya sil."},
                    HTTPStatus.BAD_REQUEST,
                )
            conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
            meta = category_meta(conn)
        return self.write_json({"ok": True, "deleted": category_id, **meta})

    def handle_login(self):
        payload = self.read_json()
        username = str(payload.get("username") or "")
        password = str(payload.get("password") or "")

        if not (
            secrets.compare_digest(username, ADMIN_USERNAME)
            and secrets.compare_digest(password, ADMIN_PASSWORD)
        ):
            return self.write_json({"ok": False, "error": "Kullanıcı adı veya şifre hatalı."}, HTTPStatus.UNAUTHORIZED)

        token = secrets.token_urlsafe(32)
        with db_connect() as conn:
            conn.execute("INSERT INTO sessions (token, created_at) VALUES (?, ?)", (token, utc_now()))
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header(
            "Set-Cookie",
            f"{SESSION_COOKIE}={token}; HttpOnly; SameSite=Lax; Path=/; Max-Age=604800",
        )
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))

    def handle_logout(self):
        token = self.session_token()
        if token:
            with db_connect() as conn:
                conn.execute("DELETE FROM sessions WHERE token = ?", (token,))
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Set-Cookie", f"{SESSION_COOKIE}=; HttpOnly; SameSite=Lax; Path=/; Max-Age=0")
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True}).encode("utf-8"))

    def create_product(self):
        with db_connect() as conn:
            meta = category_meta(conn)
        payload = normalize_payload(self.read_json(), meta["categoryLabels"])
        if not all([payload["name"], payload["price"], payload["calories"], payload["description"]]):
            return self.write_json({"error": "Ürün adı, fiyat, kalori ve açıklama zorunlu."}, HTTPStatus.BAD_REQUEST)
        try:
            payload["image"] = save_data_url(payload["image"])
        except ValueError as exc:
            return self.write_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

        now = utc_now()
        with db_connect() as conn:
            conn.execute(
                """
                INSERT INTO products (
                    id, name, price, calories, category, description, image,
                    is_active, sort_order, options_json, created_at, updated_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    payload["id"],
                    payload["name"],
                    payload["price"],
                    payload["calories"],
                    payload["category"],
                    payload["description"],
                    payload["image"],
                    payload["is_active"],
                    payload["sort_order"],
                    payload["options_json"],
                    now,
                    now,
                ),
            )
            row = conn.execute("SELECT * FROM products WHERE id = ?", (payload["id"],)).fetchone()
        return self.write_json({"product": product_from_row(row)}, HTTPStatus.CREATED)

    def update_product(self, product_id):
        with db_connect() as conn:
            meta = category_meta(conn)
        payload = normalize_payload({**self.read_json(), "id": product_id}, meta["categoryLabels"])
        try:
            payload["image"] = save_data_url(payload["image"])
        except ValueError as exc:
            return self.write_json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)

        now = utc_now()
        with db_connect() as conn:
            existing = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            if not existing:
                return self.write_json({"error": "Ürün bulunamadı."}, HTTPStatus.NOT_FOUND)
            conn.execute(
                """
                UPDATE products
                SET name = ?, price = ?, calories = ?, category = ?, description = ?,
                    image = ?, is_active = ?, sort_order = ?, options_json = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    payload["name"],
                    payload["price"],
                    payload["calories"],
                    payload["category"],
                    payload["description"],
                    payload["image"],
                    payload["is_active"],
                    payload["sort_order"],
                    payload["options_json"],
                    now,
                    product_id,
                ),
            )
            row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
        if existing["image"] != row["image"]:
            delete_upload_if_local(existing["image"])
        return self.write_json({"product": product_from_row(row)})

    def delete_product(self, product_id):
        with db_connect() as conn:
            row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
            if not row:
                return self.write_json({"error": "Ürün bulunamadı."}, HTTPStatus.NOT_FOUND)
            conn.execute("DELETE FROM products WHERE id = ?", (product_id,))
        delete_upload_if_local(row["image"])
        return self.write_json({"ok": True, "deleted": product_id})

    def read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY_BYTES:
            raise ValueError("İstek boyutu çok büyük.")
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def session_token(self):
        cookie = SimpleCookie(self.headers.get("Cookie"))
        morsel = cookie.get(SESSION_COOKIE)
        return morsel.value if morsel else ""

    def is_authenticated(self):
        token = self.session_token()
        if not token:
            return False
        with db_connect() as conn:
            row = conn.execute("SELECT token FROM sessions WHERE token = ?", (token,)).fetchone()
        return bool(row)

    def with_auth(self, callback):
        if not self.is_authenticated():
            return self.write_json({"error": "Giriş gerekli."}, HTTPStatus.UNAUTHORIZED)
        return callback()

    def write_json(self, payload, status=HTTPStatus.OK):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_static(self, request_path):
        path = unquote(request_path)
        if path == "/":
            path = "/index.html"
        if path.endswith("/"):
            path = f"{path}index.html"

        target = (BASE_DIR / path.lstrip("/")).resolve()
        if not is_safe_child(target, BASE_DIR) or not target.exists() or target.is_dir():
            return self.write_json({"error": "Bulunamadı."}, HTTPStatus.NOT_FOUND)

        body = target.read_bytes()
        content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
        if target.suffix in {".html", ".css", ".js"}:
            content_type = f"{content_type}; charset=utf-8"

        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):
        return


def main():
    parser = argparse.ArgumentParser(description="Vanilya Port QR menu backend")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=4948)
    args = parser.parse_args()

    init_db()
    server = ThreadingHTTPServer((args.host, args.port), VanilyaPortHandler)
    print(f"Vanilya Port QR backend: http://{args.host}:{args.port}")
    server.serve_forever()


if __name__ == "__main__":
    main()
