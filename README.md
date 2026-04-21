# 🎉 Konkurs Bot

Professional Telegram bot for running contests with mandatory channel subscriptions, multi-language support, and automatic winner selection.

## ✨ Xususiyatlar (Features)

- ✅ **3 tilli interfeys**: O'zbekcha, Ruscha, Inglizcha
- ✅ **Admin panel** — konkurslarni yaratish va boshqarish
- ✅ **Majburiy kanallarga obuna** tekshirish
- ✅ **Sana asosida** avtomatik boshlash/tugatish
- ✅ **Maksimal ishtirokchilar** chegarasi
- ✅ **Random g'oliblarni** aniqlash (xohlagan miqdorda)
- ✅ **Sovrinlar** ro'yxati
- ✅ **G'oliblarga avtomatik xabar** yuborish
- ✅ **Statistika** admin uchun
- ✅ **PostgreSQL** bazasi

## 📋 Talablar

- Python 3.10+
- PostgreSQL 12+
- Telegram Bot Token ([@BotFather](https://t.me/BotFather) dan)

## 🚀 O'rnatish

### 1. Loyihani yuklang

```bash
# zip ichidagi fayllarni o'qing
cd konkurs_bot
```

### 2. Virtual muhit yarating

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\Scripts\activate  # Windows
```

### 3. Kutubxonalarni o'rnating

```bash
pip install -r requirements.txt
```

### 4. PostgreSQL bazasini yarating

```bash
# PostgreSQL ichida:
CREATE DATABASE konkurs_bot;
```

### 5. .env faylini sozlang

`.env.example` faylini `.env` ga nusxalab, to'ldiring:

```bash
cp .env.example .env
```

`.env` fayl ichini to'ldiring:
```env
BOT_TOKEN=sizning_bot_tokeningiz
ADMIN_IDS=123456789,987654321
DB_HOST=localhost
DB_PORT=5432
DB_NAME=konkurs_bot
DB_USER=postgres
DB_PASSWORD=yourpassword
```

Telegram ID ni bilish uchun [@userinfobot](https://t.me/userinfobot) ga yozing.

### 6. Botni ishga tushiring

```bash
python main.py
```

## 📖 Foydalanish

### Foydalanuvchilar uchun
1. `/start` buyrug'ini yuboring
2. Tilni tanlang
3. "🎉 Aktiv konkurslar" tugmasini bosing
4. Qatnashish uchun kanallarga obuna bo'ling

### Adminlar uchun

**Konkurs yaratish:**
1. `/admin` yoki "👑 Admin panel" tugmasini bosing
2. "➕ Konkurs yaratish"
3. Quyidagilarni ketma-ket kiriting:
   - Nomi
   - Tavsifi
   - Sovrinlar
   - G'oliblar soni
   - Maksimal ishtirokchilar (ixtiyoriy)
   - Boshlanish sanasi (`YYYY-MM-DD HH:MM`)
   - Tugash sanasi
   - Majburiy kanallar
4. `/done` bilan yakunlang

**Muhim:** Bot kanalda **admin** bo'lishi kerak!

**Buyruqlar:**
- `/admin` — Admin panel
- `/winner <id>` — G'oliblarni aniqlash (masalan: `/winner 1`)
- `/help` — Yordam

## 📂 Loyiha tuzilishi

```
konkurs_bot/
├── main.py                  # Asosiy kirish nuqtasi
├── config.py                # Sozlamalar
├── requirements.txt         # Kutubxonalar
├── .env.example             # .env namuna
├── database/
│   └── db.py                # PostgreSQL modellari
├── handlers/
│   ├── user.py              # Foydalanuvchi handlerlari
│   └── admin.py             # Admin handlerlari
├── keyboards/
│   └── keyboards.py         # Klaviaturalar
├── locales/
│   ├── uz.py                # O'zbek tili
│   ├── ru.py                # Rus tili
│   └── en.py                # Ingliz tili
├── states/
│   └── contest.py           # FSM holatlar
└── utils/
    ├── helpers.py           # Yordamchi funksiyalar
    └── subscription.py      # Obunani tekshirish
```

## 🔧 Sozlash maslahatlari

**Kanal qo'shishda xato bo'lsa:**
- Bot kanalda admin ekanligini tekshiring
- Kanalning `@username` bor bo'lishi kerak (private kanallar uchun invite link)
- Bot kanal kontentini ko'ra oladigan huquqqa ega bo'lishi kerak

**Avtomatik g'oliblar aniqlash:**
- Agar `max_participants` belgilangan bo'lsa va yetsa, adminlarga xabar yuboriladi
- Tugash sanasi kelganda avtomatik g'oliblar tanlanadi

## 📝 Litsenziya

MIT License — erkin foydalaning!
