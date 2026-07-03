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
    "foods": "Yemekler",
}
DEFAULT_CATEGORY_ORDER = ["hotDrinks", "foods", "coldDrinks", "desserts"]
PLACEHOLDER_IMAGE = "./assets/vanilya-port-logo.jpg"
DEFAULT_PRODUCT_OPTIONS = {
    "ice-latte": ["Klasik", "Vanilyalı", "Karamelli"],
    "milkshake": ["Çilekli", "Vanilyalı", "Karamelli"],
    "limonata": ["Klasik", "Naneli", "Çilekli"],
    "brownie": ["Sade", "Dondurmalı"],
    "citir-tavuk": ["Acısız", "Acılı"],
    "tost": ["Kaşarlı", "Sucuklu", "Karışık"],
}

SEED_PRODUCTS = [{"id": "espresso",
  "name": "Espresso",
  "price": "120 TL",
  "calories": "5 kcal",
  "category": "hotDrinks",
  "description": "Yoğun aromalı klasik espresso shot.",
  "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 10},
 {"id": "double-espresso",
  "name": "Double Espresso",
  "price": "150 TL",
  "calories": "10 kcal",
  "category": "hotDrinks",
  "description": "İki shot espresso ile daha yoğun kahve deneyimi.",
  "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 20},
 {"id": "affogato",
  "name": "Affogato",
  "price": "180 TL",
  "calories": "220 kcal",
  "category": "hotDrinks",
  "description": "Vanilyalı dondurma üzerine sıcak espresso dökülerek servis edilir.",
  "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 30},
 {"id": "cortado",
  "name": "Cortado",
  "price": "150 TL",
  "calories": "80 kcal",
  "category": "hotDrinks",
  "description": "Espresso ve sıcak sütün dengeli, yumuşak birleşimi.",
  "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 40},
 {"id": "americano",
  "name": "Americano",
  "price": "150 TL",
  "calories": "10 kcal",
  "category": "hotDrinks",
  "description": "Espresso üzerine sıcak suyla hazırlanan sade kahve.",
  "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 50},
 {"id": "coffee-latte",
  "name": "Coffee Latte",
  "price": "150 TL",
  "calories": "170 kcal",
  "category": "hotDrinks",
  "description": "Espresso ve ipeksi süt dokusuyla yumuşak içimli latte.",
  "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 60},
 {"id": "coffee-mocha",
  "name": "Coffee Mocha",
  "price": "150 TL",
  "calories": "260 kcal",
  "category": "hotDrinks",
  "description": "Espresso, süt ve çikolata aromasıyla kremamsı sıcak kahve.",
  "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 70},
 {"id": "cappuccino",
  "name": "Cappuccino",
  "price": "150 TL",
  "calories": "140 kcal",
  "category": "hotDrinks",
  "description": "Dengeli espresso, yoğun süt köpüğü ve kakao dokunuşu.",
  "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 80},
 {"id": "filtre-kahve",
  "name": "Filtre Kahve",
  "price": "150 TL",
  "calories": "5 kcal",
  "category": "hotDrinks",
  "description": "Günlük çekilmiş kahveyle hazırlanan sade filtre kahve.",
  "image": "https://images.unsplash.com/photo-1517701604599-bb29b565090c?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 90},
 {"id": "sicak-cikolata",
  "name": "Sıcak Çikolata",
  "price": "180 TL",
  "calories": "320 kcal",
  "category": "hotDrinks",
  "description": "Yoğun çikolata aromalı, sıcak ve kremamsı içecek.",
  "image": "https://images.unsplash.com/photo-1542990253-0d0f5be5f0ed?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 100},
 {"id": "turk-kahvesi",
  "name": "Türk Kahvesi",
  "price": "120 TL",
  "calories": "25 kcal",
  "category": "hotDrinks",
  "description": "Geleneksel bakır cezvede hazırlanan bol köpüklü Türk kahvesi.",
  "image": "https://images.unsplash.com/photo-1559496417-e7f25cb247f3?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 110},
 {"id": "damla-sakizli-turk-kahvesi",
  "name": "Damla Sakızlı Türk Kahvesi",
  "price": "120 TL",
  "calories": "35 kcal",
  "category": "hotDrinks",
  "description": "Damla sakızı aromasıyla hazırlanan geleneksel Türk kahvesi.",
  "image": "https://images.unsplash.com/photo-1559496417-e7f25cb247f3?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 120},
 {"id": "dibek-kahvesi",
  "name": "Dibek Kahvesi",
  "price": "120 TL",
  "calories": "60 kcal",
  "category": "hotDrinks",
  "description": "Yumuşak içimli, aromatik geleneksel dibek kahvesi.",
  "image": "https://images.unsplash.com/photo-1559496417-e7f25cb247f3?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 130},
 {"id": "bitki-caylari",
  "name": "Bitki Çayları",
  "price": "150 TL",
  "calories": "5 kcal",
  "category": "hotDrinks",
  "description": "Sıcak servis edilen rahatlatıcı bitki çayı seçkisi.",
  "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 140,
  "options": ["Ihlamur", "Papatya", "Ada Çayı", "Kış Çayı", "Yeşil Çay", "Kuşburnu Çayı"]},
 {"id": "cay",
  "name": "Çay",
  "price": "50 TL",
  "calories": "3 kcal",
  "category": "hotDrinks",
  "description": "Taze demlenmiş klasik sıcak çay.",
  "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 150},
 {"id": "chicken-burger",
  "name": "Chicken Burger",
  "price": "300 TL",
  "calories": "620 kcal",
  "category": "foods",
  "description": "Çıtır tavuk, taze yeşillik ve özel sosla hazırlanan doyurucu burger.",
  "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 10},
 {"id": "hamburger",
  "name": "Hamburger",
  "price": "400 TL",
  "calories": "700 kcal",
  "category": "foods",
  "description": "Izgara köfte, taze yeşillik ve özel sosla hazırlanan klasik burger.",
  "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 20},
 {"id": "cheddar-burger",
  "name": "Cheddar Burger",
  "price": "430 TL",
  "calories": "780 kcal",
  "category": "foods",
  "description": "Cheddar peyniri, köfte ve özel sosla hazırlanan yoğun lezzetli burger.",
  "image": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 30},
 {"id": "gozleme",
  "name": "Gözleme",
  "price": "250 TL",
  "calories": "520 kcal",
  "category": "foods",
  "description": "Sıcak servis edilen ince hamurlu geleneksel gözleme.",
  "image": "https://images.unsplash.com/photo-1529006557810-274b9b2fc783?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 40,
  "options": ["Patatesli", "Peynirli"]},
 {"id": "combo-tabagi",
  "name": "Combo Tabağı",
  "price": "500 TL",
  "calories": "1100 kcal",
  "category": "foods",
  "description": "Paylaşımlık sıcak atıştırmalıkların doyurucu birleşimi.",
  "image": "https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 50},
 {"id": "patates-kizartmasi",
  "name": "Patates Kızartması",
  "price": "200 TL",
  "calories": "430 kcal",
  "category": "foods",
  "description": "Altın renkli çıtır patates kızartması.",
  "image": "https://images.unsplash.com/photo-1576107232684-1279f390859f?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 60},
 {"id": "elma-dilim-patates-kizartmasi",
  "name": "Elma Dilim Patates Kızartması",
  "price": "200 TL",
  "calories": "450 kcal",
  "category": "foods",
  "description": "Baharatlı elma dilim patates, sıcak ve çıtır servis edilir.",
  "image": "https://images.unsplash.com/photo-1576107232684-1279f390859f?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 70},
 {"id": "sigara-boregi-tabagi",
  "name": "Sigara Böreği Tabağı",
  "price": "250 TL",
  "calories": "520 kcal",
  "category": "foods",
  "description": "Çıtır sigara börekleri, paylaşmalık tabak sunumuyla.",
  "image": "https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 80},
 {"id": "sogan-halkasi-tabagi",
  "name": "Soğan Halkası Tabağı",
  "price": "250 TL",
  "calories": "480 kcal",
  "category": "foods",
  "description": "Çıtır kaplamalı soğan halkaları, sıcak servis edilir.",
  "image": "https://images.unsplash.com/photo-1541592106381-b31e9677c0e5?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 90},
 {"id": "nugget-tabagi",
  "name": "Nugget Tabağı",
  "price": "250 TL",
  "calories": "540 kcal",
  "category": "foods",
  "description": "Çıtır tavuk nugget parçaları, paylaşmalık tabak sunumuyla.",
  "image": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 100},
 {"id": "citir-tavuk-sepeti",
  "name": "Çıtır Tavuk Sepeti",
  "price": "350 TL",
  "calories": "680 kcal",
  "category": "foods",
  "description": "Baharatlı çıtır tavuk parçaları, sepet sunumuyla.",
  "image": "https://images.unsplash.com/photo-1626082927389-6cd097cdc6ec?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 110},
 {"id": "ice-latte",
  "name": "Ice Latte",
  "price": "170 TL",
  "calories": "190 kcal",
  "category": "coldDrinks",
  "description": "Buz, espresso ve soğuk sütle hazırlanan ferah kahve.",
  "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 10,
  "options": ["Vanilya", "Karamel", "Tiramisu", "Cookie", "Fındık Cookie"]},
 {"id": "ice-mocha",
  "name": "Ice Mocha",
  "price": "170 TL",
  "calories": "290 kcal",
  "category": "coldDrinks",
  "description": "Soğuk espresso, süt ve çikolata aromasıyla hazırlanır.",
  "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 20},
 {"id": "ice-white-mocha",
  "name": "Ice White Mocha",
  "price": "170 TL",
  "calories": "320 kcal",
  "category": "coldDrinks",
  "description": "Beyaz çikolata aromalı soğuk kahve.",
  "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 30},
 {"id": "ice-americano",
  "name": "Ice Americano",
  "price": "170 TL",
  "calories": "20 kcal",
  "category": "coldDrinks",
  "description": "Espresso, soğuk su ve buzla hazırlanan sade soğuk kahve.",
  "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 40},
 {"id": "cold-brew",
  "name": "Cold Brew",
  "price": "200 TL",
  "calories": "10 kcal",
  "category": "coldDrinks",
  "description": "Uzun demleme yöntemiyle hazırlanan yumuşak içimli soğuk kahve.",
  "image": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 50},
 {"id": "frappe",
  "name": "Frappe",
  "price": "200 TL",
  "calories": "360 kcal",
  "category": "coldDrinks",
  "description": "Buzla karıştırılmış kremamsı kahve içeceği.",
  "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 60,
  "options": ["Karamel", "Çikolata", "Vanilya", "Cookie"]},
 {"id": "milkshake",
  "name": "Milkshake",
  "price": "200 TL",
  "calories": "420 kcal",
  "category": "coldDrinks",
  "description": "Yoğun ve kremamsı soğuk milkshake.",
  "image": "https://images.unsplash.com/photo-1572490122747-3968b75cc699?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 70,
  "options": ["Karamel", "Vanilya", "Çilek", "Çikolata", "Tiramisu"]},
 {"id": "frozen",
  "name": "Frozen",
  "price": "200 TL",
  "calories": "260 kcal",
  "category": "coldDrinks",
  "description": "Buzlu meyve aromalarıyla hazırlanan ferah içecek.",
  "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 80,
  "options": ["Mango", "Ananas", "Karadut", "Böğürtlen", "Çilek", "Yeşil Elma", "Orman Meyve"]},
 {"id": "cool-lime",
  "name": "Cool Lime",
  "price": "180 TL",
  "calories": "160 kcal",
  "category": "coldDrinks",
  "description": "Lime ve nane ferahlığıyla hazırlanan buzlu içecek.",
  "image": "https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 90},
 {"id": "berry-hibiscus",
  "name": "Berry Hibiscus",
  "price": "180 TL",
  "calories": "150 kcal",
  "category": "coldDrinks",
  "description": "Hibiskus ve orman meyvesi aromalarıyla ferah içecek.",
  "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 100},
 {"id": "italyan-soda",
  "name": "İtalyan Soda",
  "price": "180 TL",
  "calories": "180 kcal",
  "category": "coldDrinks",
  "description": "Aromalı soda ve buzla hazırlanan renkli ferah içecek.",
  "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 110},
 {"id": "mojito",
  "name": "Mojito",
  "price": "300 TL",
  "calories": "240 kcal",
  "category": "coldDrinks",
  "description": "Buzlu, naneli ve meyve aromalı özel içecek.",
  "image": "https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 120,
  "options": ["Çilekli", "Nane", "Karadut", "Böğürtlen", "Yeşil Elma", "Orman Meyve"]},
 {"id": "churchill",
  "name": "Churchill",
  "price": "150 TL",
  "calories": "80 kcal",
  "category": "coldDrinks",
  "description": "Soda, limon ve tuzla hazırlanan ferah klasik.",
  "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 130},
 {"id": "berry-me",
  "name": "Berry Me",
  "price": "250 TL",
  "calories": "280 kcal",
  "category": "coldDrinks",
  "description": "Yoğun orman meyvesi aromalı özel soğuk içecek.",
  "image": "https://images.unsplash.com/photo-1544145945-f90425340c7e?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 140},
 {"id": "ev-yapimi-limonata",
  "name": "Ev Yapımı Limonata",
  "price": "120 TL",
  "calories": "140 kcal",
  "category": "coldDrinks",
  "description": "Taze limonla hazırlanan ev yapımı limonata.",
  "image": "https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 150},
 {"id": "meyveli-limonata",
  "name": "Meyveli Limonata",
  "price": "180 TL",
  "calories": "210 kcal",
  "category": "coldDrinks",
  "description": "Meyve aromalarıyla hazırlanan taze limonata.",
  "image": "https://images.unsplash.com/photo-1621263764928-df1444c5e859?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 160,
  "options": ["Çilek", "Nane", "Karadut", "Böğürtlen"]},
 {"id": "cola",
  "name": "Cola",
  "price": "120 TL",
  "calories": "140 kcal",
  "category": "coldDrinks",
  "description": "Soğuk servis edilen gazlı içecek.",
  "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 170},
 {"id": "fanta",
  "name": "Fanta",
  "price": "120 TL",
  "calories": "140 kcal",
  "category": "coldDrinks",
  "description": "Soğuk servis edilen portakallı gazlı içecek.",
  "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 180},
 {"id": "gazoz",
  "name": "Gazoz",
  "price": "120 TL",
  "calories": "140 kcal",
  "category": "coldDrinks",
  "description": "Soğuk servis edilen klasik gazoz.",
  "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 190},
 {"id": "ice-tea",
  "name": "Ice Tea",
  "price": "120 TL",
  "calories": "120 kcal",
  "category": "coldDrinks",
  "description": "Soğuk servis edilen ferah ice tea.",
  "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 200},
 {"id": "soda",
  "name": "Soda",
  "price": "100 TL",
  "calories": "0 kcal",
  "category": "coldDrinks",
  "description": "Soğuk servis edilen sade maden suyu.",
  "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 210},
 {"id": "ayran",
  "name": "Ayran",
  "price": "100 TL",
  "calories": "80 kcal",
  "category": "coldDrinks",
  "description": "Soğuk servis edilen geleneksel ayran.",
  "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 220},
 {"id": "su",
  "name": "Su",
  "price": "30 TL",
  "calories": "0 kcal",
  "category": "coldDrinks",
  "description": "Soğuk servis edilen şişe su.",
  "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 230},
 {"id": "extra-shot",
  "name": "Extra Shot",
  "price": "30 TL",
  "calories": "5 kcal",
  "category": "coldDrinks",
  "description": "Kahve içeceklerine ek espresso shot.",
  "image": "https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 240},
 {"id": "sufle",
  "name": "Sufle",
  "price": "300 TL",
  "calories": "520 kcal",
  "category": "desserts",
  "description": "Akışkan çikolatalı sıcak sufle.",
  "image": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 10},
 {"id": "magnolya",
  "name": "Magnolya",
  "price": "250 TL",
  "calories": "430 kcal",
  "category": "desserts",
  "description": "Kremalı magnolya tatlısı, seçilen meyveyle servis edilir.",
  "image": "https://images.unsplash.com/photo-1488477181946-6428a0291777?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 20,
  "options": ["Muz", "Çilek"]},
 {"id": "cheesecake",
  "name": "Cheesecake",
  "price": "300 TL",
  "calories": "480 kcal",
  "category": "desserts",
  "description": "Kremamsı cheesecake, seçilen sosla servis edilir.",
  "image": "https://images.unsplash.com/photo-1533134242443-d4fd215305ad?auto=format&fit=crop&w=900&q=82",
  "isActive": True,
  "sortOrder": 30,
  "options": ["Çilek", "Limon", "Frambuaz", "Çikolata"]}]

def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def db_connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def column_exists(conn, table, column):
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    return any(row["name"] == column for row in rows)


def resolve_food_category_id(conn):
    row = conn.execute(
        """
        SELECT id
        FROM categories
        WHERE id IN ('yemek', 'foods') OR lower(label) LIKE '%yemek%'
        ORDER BY CASE WHEN id = 'yemek' THEN 0 WHEN id = 'foods' THEN 1 ELSE 2 END
        LIMIT 1
        """
    ).fetchone()
    if row:
        return row["id"]

    now = utc_now()
    conn.execute(
        """
        INSERT OR IGNORE INTO categories (id, label, sort_order, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        ("foods", DEFAULT_CATEGORY_LABELS["foods"], 40, now, now),
    )
    return "foods"


def apply_requested_menu_products_migration(conn):
    migration_id = "20260703-full-vanilya-menu"
    applied = conn.execute("SELECT id FROM migrations WHERE id = ?", (migration_id,)).fetchone()
    if applied:
        return

    now = utc_now()
    food_category_id = resolve_food_category_id(conn)
    category_rows = [
        ("hotDrinks", DEFAULT_CATEGORY_LABELS["hotDrinks"], 0, now, now),
        (food_category_id, DEFAULT_CATEGORY_LABELS["foods"], 10, now, now),
        ("coldDrinks", DEFAULT_CATEGORY_LABELS["coldDrinks"], 20, now, now),
        ("desserts", DEFAULT_CATEGORY_LABELS["desserts"], 30, now, now),
    ]
    conn.executemany(
        """
        INSERT INTO categories (id, label, sort_order, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            label = excluded.label,
            sort_order = excluded.sort_order,
            updated_at = excluded.updated_at
        """,
        category_rows,
    )
    conn.execute(
        "DELETE FROM categories WHERE id NOT IN (?, ?, ?, ?)",
        ("hotDrinks", food_category_id, "coldDrinks", "desserts"),
    )
    conn.execute("UPDATE products SET is_active = 0, updated_at = ?", (now,))

    for product in SEED_PRODUCTS:
        category = food_category_id if product["category"] == "foods" else product["category"]
        conn.execute(
            """
            INSERT INTO products (
                id, name, price, calories, category, description, image,
                is_active, sort_order, options_json, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                name = excluded.name,
                price = excluded.price,
                calories = excluded.calories,
                category = excluded.category,
                description = excluded.description,
                image = excluded.image,
                is_active = excluded.is_active,
                sort_order = excluded.sort_order,
                options_json = excluded.options_json,
                updated_at = excluded.updated_at
            """,
            (
                product["id"],
                product["name"],
                product["price"],
                product["calories"],
                category,
                product["description"],
                product["image"],
                1 if product["isActive"] else 0,
                product["sortOrder"],
                json.dumps(product.get("options", []), ensure_ascii=False),
                now,
                now,
            ),
        )

    conn.execute("INSERT INTO migrations (id, applied_at) VALUES (?, ?)", (migration_id, now))

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
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS migrations (
                id TEXT PRIMARY KEY,
                applied_at TEXT NOT NULL
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
        apply_requested_menu_products_migration(conn)


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
    raw_sort_order = payload.get("sortOrder")
    sort_order = None
    if raw_sort_order not in (None, ""):
        sort_order = int(raw_sort_order)
    return {
        "id": category_id,
        "label": label,
        "sort_order": sort_order,
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
            if payload["sort_order"] is None:
                max_sort_order = conn.execute(
                    "SELECT COALESCE(MAX(sort_order), -10) AS max_sort_order FROM categories"
                ).fetchone()["max_sort_order"]
                payload["sort_order"] = int(max_sort_order) + 10
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
            sort_order = existing["sort_order"] if payload["sort_order"] is None else payload["sort_order"]
            conn.execute(
                """
                UPDATE categories
                SET label = ?, sort_order = ?, updated_at = ?
                WHERE id = ?
                """,
                (payload["label"], sort_order, now, category_id),
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
        if path in {"/", "/index.html"}:
            path = "/showcase.html"
        if path == "/admin":
            path = "/admin/index.html"
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
