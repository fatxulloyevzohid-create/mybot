import telebot
from telebot import types
import datetime
import random
import requests

BOT_TOKEN = "7875413809:AAGdZOTiGTT7Lph4nh0CwbTIqcQVjVdcPfA"
ADMIN_USERNAME = "SH_A_X_R_A_M"
ADMIN_NAME = "Shahrom Ramziev"

bot = telebot.TeleBot(BOT_TOKEN)

# Statistika
stats = {"users": set(), "messages": 0, "start_time": datetime.datetime.now()}

# Reaksiyalar
REACTIONS = ["👍", "❤️", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🎉",
             "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🐳", "❤️‍🔥", "💯"]

# Tarjimon kutish holati
user_states = {}

def is_admin(message):
    return message.from_user.username == ADMIN_USERNAME

# ---- /start ----
@bot.message_handler(commands=['start'])
def start(message):
    stats["users"].add(message.from_user.id)
    name = message.from_user.first_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🕐 Vaqt", "📅 Sana")
    markup.add("📊 Statistika", "ℹ️ Haqida")
    markup.add("👤 Admin", "🎲 Baxt sinab ko'r")
    markup.add("✂️ Tosh-Qaychi-Qog'oz", "🌐 Tarjimon")
    bot.send_message(
        message.chat.id,
        f"Salom *{name}*! 👋\n\n"
        "Men kuchli Telegram botman!\n\n"
        "✅ Har qanday xabarga reaksiya\n"
        "✅ O'yinlar va tarjimon\n"
        "✅ 24/7 ishlaydi",
        parse_mode="Markdown",
        reply_markup=markup
    )

# ---- /help ----
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "📋 *Barcha buyruqlar:*\n\n"
        "/start — Botni boshlash\n"
        "/help — Yordam\n"
        "/ping — Bot ishlayaptimi?\n\n"
        "🔘 *Admin buyruqlari:*\n"
        "/broadcast — Hammaga xabar\n\n"
        "🎯 *Tugmalar:*\n"
        "🕐 Vaqt | 📅 Sana\n"
        "📊 Statistika | ℹ️ Haqida\n"
        "👤 Admin | 🎲 Baxt sinab ko'r\n"
        "✂️ Tosh-Qaychi-Qog'oz\n"
        "🌐 Tarjimon",
        parse_mode="Markdown"
    )

# ---- /ping ----
@bot.message_handler(commands=['ping'])
def ping(message):
    bot.send_message(message.chat.id, "🟢 Bot ishlayapti! Pong! 🏓")

# ---- /broadcast ----
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if not is_admin(message):
        bot.send_message(message.chat.id, "❌ Faqat admin uchun!")
        return
    text = message.text.replace('/broadcast', '').strip()
    if not text:
        bot.send_message(message.chat.id, "📢 /broadcast Salom hammaga!")
        return
    count = 0
    for user_id in stats["users"]:
        try:
            bot.send_message(user_id, f"📢 *Admin xabari:*\n\n{text}", parse_mode="Markdown")
            count += 1
        except:
            pass
    bot.send_message(message.chat.id, f"✅ {count} ta foydalanuvchiga yuborildi!")

# ---- Barcha xabarlar ----
@bot.message_handler(content_types=[
    'text', 'photo', 'video', 'audio', 'document',
    'sticker', 'voice', 'video_note', 'animation'
])
def handle_message(message):
    stats["users"].add(message.from_user.id)
    stats["messages"] += 1

    # Reaksiya
    try:
        reaction = random.choice(REACTIONS)
        bot.set_message_reaction(
            message.chat.id,
            message.message_id,
            [types.ReactionTypeEmoji(reaction)]
        )
    except Exception as e:
        print(f"Reaksiya xatosi: {e}")

    if message.chat.type != "private":
        return

    t = message.text if message.text else ""
    uid = message.from_user.id

    # ---- Tarjimon holati ----
    if user_states.get(uid) == "translate":
        if t == "🔙 Orqaga":
            user_states.pop(uid, None)
            start(message)
            return
        # MyMemory API orqali tarjima (bepul)
        try:
            url = f"https://api.mymemory.translated.net/get?q={requests.utils.quote(t)}&langpair=auto|uz"
            resp = requests.get(url, timeout=5)
            data = resp.json()
            translated = data["responseData"]["translatedText"]
            bot.send_message(
                message.chat.id,
                f"🌐 *Tarjima:*\n\n"
                f"📝 Asl: _{t}_\n"
                f"✅ Tarjima: *{translated}*",
                parse_mode="Markdown"
            )
        except:
            bot.send_message(message.chat.id, "❌ Tarjima xatosi. Qayta urinib ko'ring!")
        return

    # ---- Tosh-Qaychi-Qog'oz holati ----
    if user_states.get(uid) == "tqq":
        choices = {"🪨 Tosh": "tosh", "✂️ Qaychi": "qaychi", "📄 Qog'oz": "qogoz"}
        if t == "🔙 Orqaga":
            user_states.pop(uid, None)
            start(message)
            return
        if t in choices:
            user = choices[t]
            bot_choice = random.choice(["tosh", "qaychi", "qogoz"])
            bot_emoji = {"tosh": "🪨 Tosh", "qaychi": "✂️ Qaychi", "qogoz": "📄 Qog'oz"}
            
            if user == bot_choice:
                result = "🤝 Durrang!"
            elif (user == "tosh" and bot_choice == "qaychi") or \
                 (user == "qaychi" and bot_choice == "qogoz") or \
                 (user == "qogoz" and bot_choice == "tosh"):
                result = "🎉 Siz yutdingiz!"
            else:
                result = "😢 Bot yutdi!"
            
            bot.send_message(
                message.chat.id,
                f"Siz: *{t}*\n"
                f"Bot: *{bot_emoji[bot_choice]}*\n\n"
                f"{result}",
                parse_mode="Markdown"
            )
        return

    # ---- Asosiy tugmalar ----
    if t == "🕐 Vaqt":
        bot.send_message(
            message.chat.id,
            datetime.datetime.now().strftime("🕐 *%H:%M:%S*"),
            parse_mode="Markdown"
        )

    elif t == "📅 Sana":
        weekdays = ["Dushanba","Seshanba","Chorshanba","Payshanba","Juma","Shanba","Yakshanba"]
        day = weekdays[datetime.datetime.now().weekday()]
        date = datetime.datetime.now().strftime("%d.%m.%Y")
        bot.send_message(
            message.chat.id,
            f"📅 *{date}*\n📆 {day}",
            parse_mode="Markdown"
        )

    elif t == "📊 Statistika":
        uptime = datetime.datetime.now() - stats["start_time"]
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)
        bot.send_message(
            message.chat.id,
            f"📊 *Statistika:*\n\n"
            f"👥 Foydalanuvchilar: {len(stats['users'])}\n"
            f"💬 Xabarlar: {stats['messages']}\n"
            f"⏱ Ishlash vaqti: {hours}s {minutes}d",
            parse_mode="Markdown"
        )

    elif t == "👤 Admin":
        bot.send_message(
            message.chat.id,
            f"👤 *Admin:*\n\n"
            f"Ism: {ADMIN_NAME}\n"
            f"Username: @{ADMIN_USERNAME}\n\n"
            f"Muammo bo'lsa admin bilan bog'laning!",
            parse_mode="Markdown"
        )

    elif t == "🎲 Baxt sinab ko'r":
        lucky = random.randint(1, 100)
        if lucky >= 80:
            msg = f"🎉 Omadingiz {lucky}% — Bugun juda omadli kun!"
        elif lucky >= 50:
            msg = f"😊 Omadingiz {lucky}% — Yaxshi kun!"
        elif lucky >= 30:
            msg = f"😐 Omadingiz {lucky}% — O'rtacha kun."
        else:
            msg = f"😅 Omadingiz {lucky}% — Ehtiyot bo'ling!"
        bot.send_message(message.chat.id, msg)

    elif t == "✂️ Tosh-Qaychi-Qog'oz":
        user_states[uid] = "tqq"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🪨 Tosh", "✂️ Qaychi", "📄 Qog'oz")
        markup.add("🔙 Orqaga")
        bot.send_message(
            message.chat.id,
            "✂️ *Tosh-Qaychi-Qog'oz!*\n\nTanlang:",
            parse_mode="Markdown",
            reply_markup=markup
        )

    elif t == "🌐 Tarjimon":
        user_states[uid] = "translate"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🔙 Orqaga")
        bot.send_message(
            message.chat.id,
            "🌐 *Tarjimon*\n\n"
            "Istalgan tilda matn yozing — O'zbek tiliga tarjima qilaman!",
            parse_mode="Markdown",
            reply_markup=markup
        )

    elif t == "ℹ️ Haqida":
        bot.send_message(
            message.chat.id,
            "🤖 *Bot haqida:*\n\n"
            "• Har qanday xabarga reaksiya\n"
            "• Guruh va kanallarda ishlaydi\n"
            "• 24/7 Render serverda\n"
            "• Statistika tizimi\n"
            "• Admin panel\n"
            "• Tosh-Qaychi-Qog'oz o'yini\n"
            "• Tarjimon (har qanday til → O'zbek)\n"
            f"• Admin: @{ADMIN_USERNAME}",
            parse_mode="Markdown"
        )

    else:
        try:
            parts = t.split()
            if len(parts) == 3:
                a = float(parts[0])
                op = parts[1]
                b = float(parts[2])
                if op == '+': result = a + b
                elif op == '-': result = a - b
                elif op == '*': result = a * b
                elif op == '/':
                    if b == 0:
                        bot.send_message(message.chat.id, "❌ Nolga bo'lish mumkin emas!")
                        return
                    result = a / b
                else:
                    raise ValueError
                result_str = int(result) if result == int(result) else round(result, 4)
                bot.send_message(
                    message.chat.id,
                    f"🧮 {t} = *{result_str}*",
                    parse_mode="Markdown"
                )
            else:
                bot.send_message(message.chat.id, f"📩 _{t}_", parse_mode="Markdown")
        except:
            bot.send_message(message.chat.id, f"📩 _{t}_", parse_mode="Markdown")

print("✅ Bot ishga tushdi!")
bot.polling(none_stop=True)
