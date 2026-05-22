import telebot
from telebot import types
import datetime
import random
import requests

BOT_TOKEN = "7875413809:AAGdZOTiGTT7Lph4nh0CwbTIqcQVjVdcPfA"
ADMIN_USERNAME = "SH_A_X_R_A_M"
ADMIN_NAME = "Shahrom Ramziev"

bot = telebot.TeleBot(BOT_TOKEN)

stats = {"users": set(), "messages": 0, "start_time": datetime.datetime.now()}
REACTIONS = ["👍", "❤️", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🎉",
             "🙏", "👌", "😍", "💯", "🎊", "😎", "🤩", "💪", "🌟", "✨"]
user_states = {}
word_game = {}  # uid: {"last_word": "...", "used": set()}

def is_admin(message):
    return message.from_user.username == ADMIN_USERNAME

def send(chat_id, text):
    bot.send_message(chat_id, text)

# So'zlar bazasi
WORDS = [
    "alma", "anor", "asal", "arpa", "aziz", "asil",
    "bola", "bahor", "bog", "bosh", "baliq", "bozor",
    "choy", "chaman", "chiroq", "chayon", "chol",
    "daraxt", "dala", "davr", "daryo", "don",
    "er", "eshik", "echki",
    "fasl", "farzand", "fil", "ferma",
    "gul", "gilam", "guruch", "gap",
    "havo", "hayot", "hovuz", "holva",
    "ilm", "inson", "it", "ip",
    "joy", "javob", "jarlik",
    "kema", "ko'l", "kun", "kitob", "kuch",
    "lola", "limon", "lahza",
    "meva", "mehr", "muzey", "mavj",
    "non", "nur", "nok", "narx",
    "olma", "ot", "oydin", "obod",
    "paxta", "palak", "pichan",
    "qoʻy", "qalam", "qayiq", "qor",
    "rang", "rasm", "rahmat",
    "sabzi", "suv", "sog", "sariq",
    "tog", "tosh", "tulki", "tuproq",
    "urug", "uy", "umid",
    "vatan", "vaqt",
    "xurmo", "xabar", "xona",
    "yulduz", "yol", "yoz", "yigit",
    "zamin", "zavq", "ziyrak"
]

def get_bot_word(last_letter, used_words):
    candidates = [w for w in WORDS if w[0] == last_letter and w not in used_words]
    if candidates:
        return random.choice(candidates)
    return None

@bot.message_handler(commands=['start'])
def start(message):
    stats["users"].add(message.from_user.id)
    name = message.from_user.first_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🕐 Vaqt", "📅 Sana")
    markup.add("📊 Statistika", "ℹ️ Haqida")
    markup.add("👤 Admin", "🎲 Baxt sinab kor")
    markup.add("✂️ Tosh-Qaychi-Qogoz", "🌐 Tarjimon")
    markup.add("🐍 Soz oyini")
    bot.send_message(message.chat.id, "Salom " + name + "! Botga xush kelibsiz!", reply_markup=markup)

@bot.message_handler(commands=['ping'])
def ping(message):
    send(message.chat.id, "Bot ishlayapti! Pong!")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if not is_admin(message):
        send(message.chat.id, "Bu buyruq faqat admin uchun!")
        return
    text = message.text.replace('/broadcast', '').strip()
    if not text:
        send(message.chat.id, "Xabar yozing: /broadcast Salom!")
        return
    count = 0
    for user_id in stats["users"]:
        try:
            bot.send_message(user_id, "Admin xabari:\n\n" + text)
            count += 1
        except:
            pass
    send(message.chat.id, str(count) + " ta foydalanuvchiga yuborildi!")

@bot.message_handler(content_types=[
    'text', 'photo', 'video', 'audio', 'document',
    'sticker', 'voice', 'video_note', 'animation'
])
def handle_message(message):
    stats["users"].add(message.from_user.id)
    stats["messages"] += 1

    try:
        reaction = random.choice(REACTIONS)
        bot.set_message_reaction(
            message.chat.id,
            message.message_id,
            [types.ReactionTypeEmoji(reaction)]
        )
    except Exception as e:
        print("Reaksiya xatosi: " + str(e))

    if message.chat.type != "private":
        return

    t = message.text if message.text else ""
    uid = message.from_user.id

    # ---- SOZ OYINI ----
    if user_states.get(uid) == "word_game":
        if t == "🔙 Orqaga":
            user_states.pop(uid, None)
            word_game.pop(uid, None)
            start(message)
            return

        word = t.lower().strip()

        if uid not in word_game:
            # Birinchi so'z
            if len(word) < 2:
                send(message.chat.id, "Kamida 2 harfli soz yozing!")
                return
            word_game[uid] = {"last_word": word, "used": {word}, "score": 0}
            last_letter = word[-1]
            bot_word = get_bot_word(last_letter, word_game[uid]["used"])
            if bot_word:
                word_game[uid]["used"].add(bot_word)
                word_game[uid]["last_word"] = bot_word
                send(message.chat.id,
                    "Siz: " + word + "\n"
                    "Bot: " + bot_word + "\n\n"
                    "Navbat sizda! " + bot_word[-1].upper() + " harfidan boshlang!"
                )
            else:
                send(message.chat.id, "Bot soz topolmadi! Siz yutdingiz!")
                word_game.pop(uid, None)
            return

        game = word_game[uid]
        last_word = game["last_word"]
        expected_letter = last_word[-1]

        if len(word) < 2:
            send(message.chat.id, "Kamida 2 harfli soz yozing!")
            return

        if word[0] != expected_letter:
            send(message.chat.id,
                "Notogri! Soz '" + expected_letter.upper() + "' harfidan boshlanishi kerak!\n"
                "Qayta urinib koring."
            )
            return

        if word in game["used"]:
            send(message.chat.id, "Bu soz allaqachon ishlatilgan! Boshqa soz yozing.")
            return

        game["used"].add(word)
        game["score"] += 1
        last_letter = word[-1]
        bot_word = get_bot_word(last_letter, game["used"])

        if bot_word:
            game["used"].add(bot_word)
            game["last_word"] = bot_word
            send(message.chat.id,
                "Siz: " + word + "\n"
                "Bot: " + bot_word + "\n\n"
                "Hisob: " + str(game["score"]) + " ta soz\n"
                "Navbat sizda! '" + bot_word[-1].upper() + "' harfidan boshlang!"
            )
        else:
            send(message.chat.id,
                "Siz: " + word + "\n\n"
                "Bot soz topolmadi!\n"
                "Siz yutdingiz! Hisob: " + str(game["score"]) + " ta soz"
            )
            word_game.pop(uid, None)
            user_states.pop(uid, None)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add("🔄 Qayta oynash", "🔙 Orqaga")
            bot.send_message(message.chat.id, "Tabriklaymiz!", reply_markup=markup)
        return

    # ---- TARJIMON ----
    if user_states.get(uid) == "translate":
        if t == "🔙 Orqaga":
            user_states.pop(uid, None)
            start(message)
            return
        try:
            url = "https://api.mymemory.translated.net/get?q=" + requests.utils.quote(t) + "&langpair=auto|uz"
            resp = requests.get(url, timeout=5)
            data = resp.json()
            translated = data["responseData"]["translatedText"]
            send(message.chat.id, "Asl: " + t + "\n\nTarjima: " + translated)
        except:
            send(message.chat.id, "Tarjima xatosi. Qayta urinib koring!")
        return

    # ---- TOSH-QAYCHI-QOGOZ ----
    if user_states.get(uid) == "tqq":
        if t == "🔙 Orqaga":
            user_states.pop(uid, None)
            start(message)
            return
        choices_map = {"Tosh": "tosh", "Qaychi": "qaychi", "Qogoz": "qogoz"}
        user_choice = None
        for key in choices_map:
            if key in t:
                user_choice = choices_map[key]
                break
        if user_choice:
            bot_choice = random.choice(["tosh", "qaychi", "qogoz"])
            bot_emoji = {"tosh": "Tosh", "qaychi": "Qaychi", "qogoz": "Qogoz"}
            if user_choice == bot_choice:
                result = "Durrang!"
            elif (user_choice == "tosh" and bot_choice == "qaychi") or \
                 (user_choice == "qaychi" and bot_choice == "qogoz") or \
                 (user_choice == "qogoz" and bot_choice == "tosh"):
                result = "Siz yutdingiz!"
            else:
                result = "Bot yutdi!"
            send(message.chat.id,
                "Siz: " + t + "\nBot: " + bot_emoji[bot_choice] + "\n\n" + result)
        return

    # ---- ASOSIY MENYУ ----
    if t == "🔄 Qayta oynash":
        user_states[uid] = "word_game"
        word_game.pop(uid, None)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🔙 Orqaga")
        bot.send_message(message.chat.id,
            "Soz oyini boshlandi!\n\n"
            "Qoidalar:\n"
            "- Har bir soz oldingi sozning oxirgi harfidan boshlansin\n"
            "- Bir soz ikki marta ishlatilmaydi\n"
            "- Kamida 2 harfli sozlar\n\n"
            "Birinchi sozni yozing!",
            reply_markup=markup)

    elif t == "🐍 Soz oyini":
        user_states[uid] = "word_game"
        word_game.pop(uid, None)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🔙 Orqaga")
        bot.send_message(message.chat.id,
            "Soz oyini boshlandi!\n\n"
            "Qoidalar:\n"
            "- Har bir soz oldingi sozning oxirgi harfidan boshlansin\n"
            "- Bir soz ikki marta ishlatilmaydi\n"
            "- Kamida 2 harfli sozlar\n\n"
            "Birinchi sozni yozing!",
            reply_markup=markup)

    elif t == "🕐 Vaqt":
        send(message.chat.id, "Hozirgi vaqt: " + datetime.datetime.now().strftime("%H:%M:%S"))

    elif t == "📅 Sana":
        weekdays = ["Dushanba","Seshanba","Chorshanba","Payshanba","Juma","Shanba","Yakshanba"]
        day = weekdays[datetime.datetime.now().weekday()]
        date = datetime.datetime.now().strftime("%d.%m.%Y")
        send(message.chat.id, "Bugun: " + date + "\nKun: " + day)

    elif t == "📊 Statistika":
        uptime = datetime.datetime.now() - stats["start_time"]
        hours = int(uptime.total_seconds() // 3600)
        minutes = int((uptime.total_seconds() % 3600) // 60)
        send(message.chat.id,
            "Statistika:\n\n"
            "Foydalanuvchilar: " + str(len(stats["users"])) + "\n"
            "Xabarlar: " + str(stats["messages"]) + "\n"
            "Ishlash vaqti: " + str(hours) + "s " + str(minutes) + "d"
        )

    elif t == "👤 Admin":
        send(message.chat.id,
            "Admin:\n\nIsm: " + ADMIN_NAME + "\nUsername: @" + ADMIN_USERNAME)

    elif t == "🎲 Baxt sinab kor":
        lucky = random.randint(1, 100)
        if lucky >= 80:
            msg = "Omadingiz " + str(lucky) + "% - Bugun juda omadli kun!"
        elif lucky >= 50:
            msg = "Omadingiz " + str(lucky) + "% - Yaxshi kun!"
        elif lucky >= 30:
            msg = "Omadingiz " + str(lucky) + "% - Ortacha kun."
        else:
            msg = "Omadingiz " + str(lucky) + "% - Ehtiyot boling!"
        send(message.chat.id, msg)

    elif t == "✂️ Tosh-Qaychi-Qogoz":
        user_states[uid] = "tqq"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("Tosh", "Qaychi", "Qogoz")
        markup.add("🔙 Orqaga")
        bot.send_message(message.chat.id, "Tosh-Qaychi-Qogoz! Tanlang:", reply_markup=markup)

    elif t == "🌐 Tarjimon":
        user_states[uid] = "translate"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("🔙 Orqaga")
        bot.send_message(message.chat.id,
            "Tarjimon - Istalgan tilda yozing, Uzbek tiliga tarjima qilaman!",
            reply_markup=markup)

    elif t == "ℹ️ Haqida":
        send(message.chat.id,
            "Bot haqida:\n\n"
            "- Har qanday xabarga reaksiya\n"
            "- Guruh va kanallarda ishlaydi\n"
            "- 24/7 Render serverda\n"
            "- Statistika tizimi\n"
            "- Admin panel\n"
            "- Tosh-Qaychi-Qogoz oyini\n"
            "- Soz oyini\n"
            "- Tarjimon\n"
            "- Admin: @" + ADMIN_USERNAME
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
                        send(message.chat.id, "Nolga bolish mumkin emas!")
                        return
                    result = a / b
                else:
                    raise ValueError
                result_str = int(result) if result == int(result) else round(result, 4)
                send(message.chat.id, t + " = " + str(result_str))
            else:
                send(message.chat.id, "Siz yozdingiz: " + t)
        except:
            send(message.chat.id, "Siz yozdingiz: " + t)

print("Bot ishga tushdi!")
bot.polling(none_stop=True)
