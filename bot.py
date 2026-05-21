import telebot
from telebot import types
import datetime

BOT_TOKEN = "7875413809:AAGdZOTiGTT7Lph4nh0CwbTIqcQVjVdcPfA"
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    name = message.from_user.first_name
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🕐 Vaqt", "📅 Sana")
    markup.add("ℹ️ Haqida")
    bot.send_message(message.chat.id, f"Salom {name}! 👋\nMen Telegram botman!", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle(message):
    t = message.text
    if t == "🕐 Vaqt":
        bot.send_message(message.chat.id, datetime.datetime.now().strftime("🕐 %H:%M:%S"))
    elif t == "📅 Sana":
        bot.send_message(message.chat.id, datetime.datetime.now().strftime("📅 %d.%m.%Y"))
    elif t == "ℹ️ Haqida":
        bot.send_message(message.chat.id, "🤖 Python Telegram Bot\nRender serverda ishlaydi!")
    else:
        bot.send_message(message.chat.id, f"Siz yozdingiz: {t}")

bot.polling(none_stop=True)
