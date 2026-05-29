"""
==============================================
  FOYDALI TELEGRAM BOTLAR — 12 TA MODULE
  Python 3.10+ | python-telegram-bot 20.x
==============================================
O'rnatish:
  pip install python-telegram-bot apscheduler requests

Ishga tushurish:
  python bot.py

TOKEN olish:
  1. Telegram da @BotFather ga yozing
  2. /newbot buyrug'ini yuboring
  3. Bot nomi va username kiriting
  4. TOKEN nusxalab quyidagi BOT_TOKEN ga joylashtiring
"""

import logging
import asyncio
import json
import os
from datetime import datetime, time
from collections import defaultdict

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    CallbackQueryHandler, ContextTypes, filters
)

# ─────────────────────────────────────────────
#  TOKEN — shu yerga o'zingizning tokeningizni qo'ying
# ─────────────────────────────────────────────
BOT_TOKEN = "7875413809:AAGdZOTiGTT7Lph4nh0CwbTIqcQVjVdcPfA"

# Loglash
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Foydalanuvchi ma'lumotlari (xotirada saqlanadi)
user_data = defaultdict(dict)

# ══════════════════════════════════════════════════════════
#  ASOSIY MENYULAR
# ══════════════════════════════════════════════════════════

MAIN_MENU = [
    ["📖 O'quv Yordamchi", "💊 Dori Eslatma"],
    ["🧾 Hisob-Kitob",     "🌍 Til O'rgatuvchi"],
    ["🥗 Ovqat Retsepti",  "🧓 Keksalar Yordam"],
    ["🧠 Ruhiy Salomatlik","🏪 Do'kon Boshqaruv"],
    ["🚌 Transport",       "⚖️ Huquqiy Yordam"],
    ["💼 Ish Topish",      "🌾 Dehqon Yordamchi"],
]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bosh sahifa — barcha botlarni ko'rsatadi"""
    keyboard = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    await update.message.reply_text(
        "👋 *Xush kelibsiz!*\n\n"
        "Quyidagi xizmatlardan birini tanlang:\n\n"
        "Bot har kuni yanada yaxshilanib boradi 🚀",
        parse_mode="Markdown",
        reply_markup=keyboard
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ *Yordam*\n\n"
        "Har bir xizmat uchun pastdagi menyudan tanlang.\n"
        "Asosiy menyuga qaytish: /start\n\n"
        "Muammo bo'lsa: /start ni bosing.",
        parse_mode="Markdown"
    )


# ══════════════════════════════════════════════════════════
#  1. 📖 O'QUV YORDAMCHI BOT
# ══════════════════════════════════════════════════════════

QUIZ_QUESTIONS = {
    "matematika": [
        {"s": "2² + 3² = ?", "j": ["13", "12", "11", "10"], "t": "13"},
        {"s": "√144 = ?",    "j": ["12", "14", "11", "13"], "t": "12"},
        {"s": "5! = ?",      "j": ["120", "60", "24", "720"], "t": "120"},
    ],
    "fizika": [
        {"s": "Yorug'lik tezligi (km/s)?", "j": ["300000", "150000", "100000", "200000"], "t": "300000"},
        {"s": "F = m × ?",                 "j": ["a", "v", "t", "E"], "t": "a"},
    ],
    "inglizcha": [
        {"s": "'Apple' o'zbekcha?", "j": ["Olma", "Nok", "Uzum", "Shaftoli"], "t": "Olma"},
        {"s": "'Hello' rasmiy shakli?", "j": ["Good day", "Hi", "Hey", "Yo"], "t": "Good day"},
    ]
}

async def oquv_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔢 Matematika testi", callback_data="quiz_matematika")],
        [InlineKeyboardButton("⚡ Fizika testi",     callback_data="quiz_fizika")],
        [InlineKeyboardButton("🇬🇧 Inglizcha testi", callback_data="quiz_inglizcha")],
        [InlineKeyboardButton("❓ Savol ber",        callback_data="oquv_savol")],
    ])
    await update.message.reply_text(
        "📖 *O'quv Yordamchi*\n\nNimani xohlaysiz?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def quiz_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("quiz_"):
        fan = data.replace("quiz_", "")
        questions = QUIZ_QUESTIONS.get(fan, [])
        if not questions:
            await query.edit_message_text("Savol topilmadi.")
            return

        q = questions[0]
        uid = query.from_user.id
        user_data[uid]["quiz_fan"] = fan
        user_data[uid]["quiz_idx"] = 0
        user_data[uid]["quiz_ball"] = 0

        buttons = [[InlineKeyboardButton(j, callback_data=f"qans_{j}")] for j in q["j"]]
        await query.edit_message_text(
            f"📝 *{fan.upper()} TESTI*\n\n{q['s']}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data.startswith("qans_"):
        uid = query.from_user.id
        javob = data.replace("qans_", "")
        fan = user_data[uid].get("quiz_fan", "matematika")
        idx = user_data[uid].get("quiz_idx", 0)
        ball = user_data[uid].get("quiz_ball", 0)
        questions = QUIZ_QUESTIONS[fan]

        if javob == questions[idx]["t"]:
            ball += 1
            user_data[uid]["quiz_ball"] = ball
            natija = "✅ To'g'ri!"
        else:
            natija = f"❌ Noto'g'ri! To'g'ri javob: *{questions[idx]['t']}*"

        idx += 1
        user_data[uid]["quiz_idx"] = idx

        if idx >= len(questions):
            await query.edit_message_text(
                f"{natija}\n\n🏆 *Test yakunlandi!*\n"
                f"Ball: {ball}/{len(questions)}\n\n"
                f"{'⭐⭐⭐ Zo\'r!' if ball == len(questions) else '📚 Ko\'proq o\'qing!'}",
                parse_mode="Markdown"
            )
        else:
            q = questions[idx]
            buttons = [[InlineKeyboardButton(j, callback_data=f"qans_{j}")] for j in q["j"]]
            await query.edit_message_text(
                f"{natija}\n\n📝 Keyingi savol:\n{q['s']}",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    elif data == "oquv_savol":
        await query.edit_message_text(
            "❓ Savolingizni yozing, men javob beraman!\n\n"
            "Masalan: *Pifagor teoremasi nima?*",
            parse_mode="Markdown"
        )


# ══════════════════════════════════════════════════════════
#  2. 💊 DORI ESLATMA BOT
# ══════════════════════════════════════════════════════════

async def dori_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    dorlar = user_data[uid].get("dorlar", [])

    text = "💊 *Dori Eslatma Bot*\n\n"
    if dorlar:
        text += "📋 Dorilaring:\n"
        for i, d in enumerate(dorlar, 1):
            text += f"  {i}. {d['nom']} — {d['vaqt']} ({d['doza']})\n"
        text += "\n"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("➕ Dori qo'shish",    callback_data="dori_qosh")],
        [InlineKeyboardButton("🗑 Dori o'chirish",   callback_data="dori_ochir")],
        [InlineKeyboardButton("📋 Ro'yxat",          callback_data="dori_royxat")],
    ])
    await update.message.reply_text(text, parse_mode="Markdown", reply_markup=keyboard)

async def dori_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "dori_qosh":
        uid = query.from_user.id
        user_data[uid]["dori_holat"] = "nom_kutish"
        await query.edit_message_text(
            "💊 Dori nomini yozing:\n_(Masalan: Paracetamol)_",
            parse_mode="Markdown"
        )
    elif query.data == "dori_royxat":
        uid = query.from_user.id
        dorlar = user_data[uid].get("dorlar", [])
        if dorlar:
            text = "📋 *Dorilar ro'yxati:*\n\n"
            for i, d in enumerate(dorlar, 1):
                text += f"{i}. 💊 *{d['nom']}*\n   ⏰ {d['vaqt']} | 📏 {d['doza']}\n\n"
        else:
            text = "📭 Hali dori qo'shilmagan.\n\nDori qo'shish uchun '➕ Dori qo'shish' tugmasini bosing."
        await query.edit_message_text(text, parse_mode="Markdown")
    elif query.data == "dori_ochir":
        uid = query.from_user.id
        dorlar = user_data[uid].get("dorlar", [])
        if not dorlar:
            await query.edit_message_text("📭 O'chirish uchun dori yo'q.")
            return
        buttons = [
            [InlineKeyboardButton(f"🗑 {d['nom']}", callback_data=f"ochir_{i}")]
            for i, d in enumerate(dorlar)
        ]
        await query.edit_message_text(
            "Qaysi dorini o'chirmoqchisiz?",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif query.data.startswith("ochir_"):
        uid = query.from_user.id
        idx = int(query.data.replace("ochir_", ""))
        dorlar = user_data[uid].get("dorlar", [])
        if 0 <= idx < len(dorlar):
            nom = dorlar[idx]["nom"]
            dorlar.pop(idx)
            user_data[uid]["dorlar"] = dorlar
            await query.edit_message_text(f"✅ *{nom}* o'chirildi.", parse_mode="Markdown")


# ══════════════════════════════════════════════════════════
#  3. 🧾 HISOB-KITOB BOT
# ══════════════════════════════════════════════════════════

async def hisob_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    trxn = user_data[uid].get("trxn", [])
    daromad = sum(t["summa"] for t in trxn if t["tur"] == "daromad")
    xarajat = sum(t["summa"] for t in trxn if t["tur"] == "xarajat")

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💰 Daromad qo'sh", callback_data="hisob_daromad"),
         InlineKeyboardButton("💸 Xarajat qo'sh", callback_data="hisob_xarajat")],
        [InlineKeyboardButton("📊 Hisobot", callback_data="hisob_hisobot")],
        [InlineKeyboardButton("🗑 Tozalash", callback_data="hisob_tozala")],
    ])
    await update.message.reply_text(
        f"🧾 *Hisob-Kitob Bot*\n\n"
        f"💰 Daromad: *{daromad:,} so'm*\n"
        f"💸 Xarajat: *{xarajat:,} so'm*\n"
        f"{'✅' if daromad >= xarajat else '⚠️'} Balans: *{daromad - xarajat:,} so'm*",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def hisob_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    if query.data == "hisob_daromad":
        user_data[uid]["hisob_holat"] = "daromad"
        await query.edit_message_text("💰 Daromad miqdorini yozing (so'mda):\n_(Masalan: 500000)_", parse_mode="Markdown")

    elif query.data == "hisob_xarajat":
        user_data[uid]["hisob_holat"] = "xarajat"
        await query.edit_message_text("💸 Xarajat miqdorini yozing (so'mda):\n_(Masalan: 150000)_", parse_mode="Markdown")

    elif query.data == "hisob_hisobot":
        trxn = user_data[uid].get("trxn", [])
        if not trxn:
            await query.edit_message_text("📭 Hali hech narsa kiritilmagan.")
            return
        text = "📊 *Hisobot:*\n\n"
        for t in trxn[-10:]:
            icon = "💰" if t["tur"] == "daromad" else "💸"
            text += f"{icon} {t['izoh']}: *{t['summa']:,}* so'm\n"
        daromad = sum(t["summa"] for t in trxn if t["tur"] == "daromad")
        xarajat = sum(t["summa"] for t in trxn if t["tur"] == "xarajat")
        text += f"\n✅ Jami daromad: *{daromad:,}*\n❌ Jami xarajat: *{xarajat:,}*\n💵 Balans: *{daromad-xarajat:,}*"
        await query.edit_message_text(text, parse_mode="Markdown")

    elif query.data == "hisob_tozala":
        user_data[uid]["trxn"] = []
        await query.edit_message_text("✅ Barcha ma'lumotlar tozalandi.")


# ══════════════════════════════════════════════════════════
#  4. 🌍 TIL O'RGATUVCHI BOT
# ══════════════════════════════════════════════════════════

DAILY_WORDS = [
    {"uz": "Olma",     "en": "Apple",     "ru": "Яблоко",   "mis": "I eat an apple every day."},
    {"uz": "Kitob",    "en": "Book",      "ru": "Книга",    "mis": "This is a good book."},
    {"uz": "Maktab",   "en": "School",    "ru": "Школа",    "mis": "I go to school."},
    {"uz": "Do'st",    "en": "Friend",    "ru": "Друг",     "mis": "He is my best friend."},
    {"uz": "Suv",      "en": "Water",     "ru": "Вода",     "mis": "Water is important."},
    {"uz": "Uy",       "en": "House",     "ru": "Дом",      "mis": "My house is big."},
    {"uz": "Kun",      "en": "Day",       "ru": "День",     "mis": "It's a beautiful day."},
]

PHRASES = [
    {"uz": "Rahmat",         "en": "Thank you",    "ru": "Спасибо"},
    {"uz": "Salom",          "en": "Hello",         "ru": "Привет"},
    {"uz": "Xayr",           "en": "Goodbye",       "ru": "До свидания"},
    {"uz": "Kechirasiz",     "en": "Excuse me",     "ru": "Извините"},
    {"uz": "Qanday qilsam?", "en": "How do I?",     "ru": "Как мне?"},
]

async def til_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("📅 Bugungi so'z",    callback_data="til_soz")],
        [InlineKeyboardButton("💬 Foydali iboralar", callback_data="til_ibora")],
        [InlineKeyboardButton("🧪 So'z testi",       callback_data="til_test")],
    ])
    await update.message.reply_text(
        "🌍 *Til O'rgatuvchi Bot*\n\nHar kuni yangi so'z o'rganing!",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def til_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "til_soz":
        import random
        w = random.choice(DAILY_WORDS)
        await query.edit_message_text(
            f"📅 *Bugungi so'z*\n\n"
            f"🇺🇿 *{w['uz']}*\n"
            f"🇬🇧 {w['en']}\n"
            f"🇷🇺 {w['ru']}\n\n"
            f"📝 Misol: _{w['mis']}_",
            parse_mode="Markdown"
        )
    elif query.data == "til_ibora":
        text = "💬 *Foydali iboralar:*\n\n"
        for p in PHRASES:
            text += f"🇺🇿 *{p['uz']}* → 🇬🇧 {p['en']} | 🇷🇺 {p['ru']}\n"
        await query.edit_message_text(text, parse_mode="Markdown")

    elif query.data == "til_test":
        import random
        w = random.choice(DAILY_WORDS)
        options = [w["en"]]
        while len(options) < 4:
            r = random.choice(DAILY_WORDS)["en"]
            if r not in options:
                options.append(r)
        random.shuffle(options)
        uid = query.from_user.id
        user_data[uid]["til_test_javob"] = w["en"]
        buttons = [[InlineKeyboardButton(o, callback_data=f"tilans_{o}")] for o in options]
        await query.edit_message_text(
            f"🧪 *So'z testi*\n\n'{w['uz']}' inglizcha nima?",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
    elif query.data.startswith("tilans_"):
        uid = query.from_user.id
        javob = query.data.replace("tilans_", "")
        togri = user_data[uid].get("til_test_javob", "")
        if javob == togri:
            await query.edit_message_text("✅ *To'g'ri!* Zo'r bilasiz! 🎉", parse_mode="Markdown")
        else:
            await query.edit_message_text(f"❌ Noto'g'ri!\nTo'g'ri javob: *{togri}*", parse_mode="Markdown")


# ══════════════════════════════════════════════════════════
#  5. 🥗 OVQAT RETSEPTI BOT
# ══════════════════════════════════════════════════════════

RETSEPTLAR = {
    "palov": {
        "nomi": "O'zbekcha Palov",
        "vaqt": "60 daqiqa",
        "materiallar": ["Guruch 500g", "Sabzi 3 dona", "Piyoz 2 dona", "Go'sht 500g",
                        "O'simlik yog'i 150ml", "Tuz, zira, don zira"],
        "qadamlar": [
            "Yog'ni qiziting, piyozni qo'shib qovuring",
            "Go'shtni qo'shib, oltin rang bo'lguncha qovuring",
            "Sabzini qo'shib, 10 daqiqa qovuring",
            "Suv qo'shib, 20 daqiqa qaynatib oling",
            "Yuvib tayyorlangan guruchni soling",
            "Suv bug'lanib ketguncha dam ostida pishiring"
        ]
    },
    "somsa": {
        "nomi": "O'zbekcha Somsa",
        "vaqt": "45 daqiqa",
        "materiallar": ["Un 500g", "Qo'y go'shtli farsh 400g", "Piyoz 3 dona",
                        "Tuz, qora murch", "Sariyog' 100g"],
        "qadamlar": [
            "Xmir yoğrib, 30 daqiqa qoldiring",
            "Go'sht, piyoz va ziravorlarni aralashtirib to'ldirishni tayyorlang",
            "Xamirni yupqa yoying va to'rtburchak kesimlarga bo'ling",
            "Har biriga to'ldirish qo'ying va uchburchak shakl bering",
            "Tandirga yoki pechga 200°C da 25-30 daqiqa pishiring"
        ]
    },
    "mastava": {
        "nomi": "Mastava",
        "vaqt": "50 daqiqa",
        "materiallar": ["Go'sht 400g", "Guruch 100g", "Sabzi 2 dona", "Pomidor 3 dona",
                        "Kartoshka 3 dona", "Piyoz 2 dona", "Tuz, zira"],
        "qadamlar": [
            "Go'shtni qovurib suvga soling",
            "Piyoz va sabzini qo'shib 20 daqiqa qaynating",
            "Pomidor va kartoshkani qo'shing",
            "Yuvib tayyorlangan guruchni qo'shing",
            "Pishib tayyor bo'lguncha qaynating"
        ]
    }
}

async def ovqat_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🍚 Palov retsepti",   callback_data="ret_palov")],
        [InlineKeyboardButton("🥟 Somsa retsepti",   callback_data="ret_somsa")],
        [InlineKeyboardButton("🍲 Mastava retsepti", callback_data="ret_mastava")],
        [InlineKeyboardButton("🔍 Mahsulot kiriting", callback_data="ovqat_qidir")],
    ])
    await update.message.reply_text(
        "🥗 *Ovqat Retsepti Bot*\n\nQaysi taomni pishirmoqchisiz?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def ovqat_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("ret_"):
        nom = query.data.replace("ret_", "")
        r = RETSEPTLAR.get(nom)
        if r:
            text = (f"🍽 *{r['nomi']}*\n⏱ Vaqt: {r['vaqt']}\n\n"
                    f"📦 *Materiallar:*\n" +
                    "\n".join(f"  • {m}" for m in r["materiallar"]) +
                    f"\n\n👨‍🍳 *Tayyorlash:*\n" +
                    "\n".join(f"  {i+1}. {q}" for i, q in enumerate(r["qadamlar"])))
            await query.edit_message_text(text, parse_mode="Markdown")

    elif query.data == "ovqat_qidir":
        uid = query.from_user.id
        user_data[uid]["ovqat_holat"] = "qidirish"
        await query.edit_message_text(
            "🔍 Uyingizda qanday mahsulotlar bor?\n_(Masalan: kartoshka, piyoz, tuxum)_",
            parse_mode="Markdown"
        )


# ══════════════════════════════════════════════════════════
#  6. 🧓 KEKSALAR YORDAMCHI BOT
# ══════════════════════════════════════════════════════════

async def keksa_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("💡 Kommunal to'lov",  callback_data="keksa_kommunal")],
        [InlineKeyboardButton("🏥 Shifokor topish",  callback_data="keksa_shifokor")],
        [InlineKeyboardButton("📞 Yaqinlarga xabar", callback_data="keksa_xabar")],
        [InlineKeyboardButton("💊 Dori eslatma →",   callback_data="keksa_dori")],
        [InlineKeyboardButton("☎️ Muhim raqamlar",   callback_data="keksa_raqamlar")],
    ])
    await update.message.reply_text(
        "🧓 *Keksalar Yordamchi*\n\n👋 Xush kelibsiz!\nNimaga yordam kerak?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )

async def keksa_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    responses = {
        "keksa_kommunal": (
            "💡 *Kommunal To'lovlar*\n\n"
            "Toshkent shahri uchun:\n\n"
            "• 🔵 *Gaz:* 1 m³ = 650 so'm\n"
            "• 💡 *Elektr:* 1 kVt/soat = 300 so'm\n"
            "• 💧 *Suv:* 1 m³ = 1200 so'm\n\n"
            "To'
