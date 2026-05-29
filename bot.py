import telebot
from telebot import types
import datetime
import random

BOT_TOKEN = "7875413809:AAGdZOTiGTT7Lph4nh0CwbTIqcQVjVdcPfA"
bot = telebot.TeleBot(BOT_TOKEN)

# Barcha reaksiyalar ro'yxati
REACTIONS = ["👍", "❤️", "🔥", "🥰", "👏", "😁", "🤔", "🤯", "😱", "🎉", 
             "🙏", "👌", "🕊", "🤡", "🥱", "🥴", "😍", "🐳", "❤️‍🔥", "💯"]

# ---- /start buyrug'i ----
@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🕐 Vaqt", "📅 Sana")
    markup.add("ℹ️ Haqida")
    bot.send_message(
        message.chat.id,
        f"Salom *{name}*! 👋\n\nMen Telegram botman!\nHar qanday xabarga reaksiya bosaman! 😊",
        parse_mode="Markdown",
        reply_markup=markup
    )

# ---- /help buyrug'i ----
@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "📋 *Buyruqlar:*\n\n"
        "/start — Botni boshlash\n"
        "/help — Yordam\n\n"
        "🔘 *Tugmalar:*\n"
        "🕐 Vaqt — Hozirgi vaqt\n"
        "📅 Sana — Bugungi sana\n"
        "ℹ️ Haqida — Bot haqida\n\n"
        "💬 Har qanday xabarga reaksiya bosaman!",
        parse_mode="Markdown"
    )

# ---- Barcha xabarlarga reaksiya bosish ----
@bot.message_handler(content_types=[
    'text', 'photo', 'video', 'audio', 'document', 
    'sticker', 'voice', 'video_note', 'animation'
])
def handle_message(message):
    # Tasodifiy reaksiya tanlash
    reaction = random.choice(REACTIONS)
    
    try:
        # Reaksiya bosish
        bot.set_message_reaction(
            message.chat.id,
            message.message_id,
            [types.ReactionTypeEmoji(reaction)]
        )
    except Exception as e:
        print(f"Reaksiya xatosi: {e}")

    # Shaxsiy chatda tugmalar ham ishlaydi
    if message.chat.type == "private":
        t = message.text if message.text else ""
        
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
        elif t == "ℹ️ Haqida":
            bot.send_message(
                message.chat.id,
                "🤖 *Bot haqida:*\n\n"
                "• Har qanday xabarga reaksiya bosadi\n"
                "• Guruh va kanallarda ishlaydi\n"
                "• 24/7 Render serverda ishlaydi\n"
                "• Python bilan yozilgan",
                parse_mode="Markdown"
            )
        else:
            # Kalkulyator
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
                    bot.send_message(
                        message.chat.id,
                        f"📩 Siz yozdingiz:\n_{t}_",
                        parse_mode="Markdown"
                    )
            except:
                bot.send_message(
                    message.chat.id,
                    f"📩 Siz yozdingiz:\n_{t}_",
                    parse_mode="Markdown"
                )

print("✅ Bot ishga tushdi!")
bot.polling(none_stop=True)
                      
