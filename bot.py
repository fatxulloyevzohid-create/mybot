import telebot
from telebot import types

BOT_TOKEN = "7875413809:AAGdZOTiGTT7Lph4nh0CwbTIqcQVjVdcPfA"
ADMIN_USERNAME = "SH_A_X_R_A_M"
ADMIN_NAME = "Shahrom Ramziev"
ADMIN_LINK = "https://t.me/SH_A_X_R_A_M"
CHANNEL_LINK = "https://t.me/LURSS_TM"
CHANNEL_NAME = "Lurss™"
CHANNEL_ID = "@LURSS_TM"

bot = telebot.TeleBot(BOT_TOKEN)

def is_subscribed(user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🛡 VPN", "🤖 Bot yasash")
    markup.add("📞 Murojaat", "ℹ️ Haqida")
    return markup

def sub_required(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton(
        "📢 " + CHANNEL_NAME + " ga obuna bo'lish",
        url=CHANNEL_LINK
    ))
    markup.add(types.InlineKeyboardButton(
        "✅ Obuna bo'ldim",
        callback_data="check_sub"
    ))
    bot.send_message(
        message.chat.id,
        "Botdan foydalanish uchun avval kanalga obuna bolan!\n\n"
        "Kanal: " + CHANNEL_NAME + "\n\n"
        "Obuna bolgandan keyin Obuna boldim tugmasini bosing!",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda c: c.data == "check_sub")
def check_sub(call):
    if is_subscribed(call.from_user.id):
        bot.answer_callback_query(call.id, "Rahmat! Endi botdan foydalanishingiz mumkin!")
        bot.delete_message(call.message.chat.id, call.message.message_id)
        name = call.from_user.first_name
        bot.send_message(
            call.message.chat.id,
            "Salom " + name + "!\n\n"
            "Xush kelibsiz!\n\n"
            "Bizning xizmatlar:\n\n"
            "VPN - 20,000 so'm\n"
            "VPN Pro - 50,000 so'm\n"
            "Bot yasash - 50,000 dan 200,000 so'mgacha\n\n"
            "Quyidagi tugmalardan birini tanlang:",
            reply_markup=main_menu()
        )
    else:
        bot.answer_callback_query(call.id, "Siz hali obuna bolmadingiz!", show_alert=True)

@bot.message_handler(commands=['start'])
def start(message):
    if not is_subscribed(message.from_user.id):
        sub_required(message)
        return
    name = message.from_user.first_name
    bot.send_message(
        message.chat.id,
        "Salom " + name + "!\n\n"
        "Xush kelibsiz!\n\n"
        "Bizning xizmatlar:\n\n"
        "VPN - 20,000 so'm\n"
        "VPN Pro - 50,000 so'm\n"
        "Bot yasash - 50,000 dan 200,000 so'mgacha\n\n"
        "Quyidagi tugmalardan birini tanlang:",
        reply_markup=main_menu()
    )

@bot.message_handler(func=lambda m: m.text == "🛡 VPN")
def vpn_menu(message):
    if not is_subscribed(message.from_user.id):
        sub_required(message)
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("VPN - 20,000 so'm")
    markup.add("VPN Pro - 50,000 so'm")
    markup.add("🔙 Orqaga")
    bot.send_message(
        message.chat.id,
        "VPN turlari:\n\n"
        "VPN - 20,000 so'm\n"
        "Tez ulanish, barcha qurilmalar\n\n"
        "VPN Pro - 50,000 so'm\n"
        "Eng tez, to'liq himoya, shaxsiy server\n\n"
        "Turni tanlang:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "VPN - 20,000 so'm")
def vpn_oddiy(message):
    if not is_subscribed(message.from_user.id):
        sub_required(message)
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 " + ADMIN_NAME + " ga yozish", url=ADMIN_LINK))
    markup.add(types.InlineKeyboardButton("📢 " + CHANNEL_NAME, url=CHANNEL_LINK))
    bot.send_message(
        message.chat.id,
        "VPN - 20,000 so'm\n\n"
        "Nimalar kiradi:\n"
        "Tez ulanish\n"
        "Barcha qurilmalar\n"
        "24/7 ishlaydi\n"
        "O'rnatish yordam\n\n"
        "Narx: 20,000 so'm\n\n"
        "Buyurtma berish uchun adminga yozing:\n\n"
        "Admin: " + ADMIN_NAME + "\n"
        "@" + ADMIN_USERNAME,
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "VPN Pro - 50,000 so'm")
def vpn_pro(message):
    if not is_subscribed(message.from_user.id):
        sub_required(message)
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 " + ADMIN_NAME + " ga yozish", url=ADMIN_LINK))
    markup.add(types.InlineKeyboardButton("📢 " + CHANNEL_NAME, url=CHANNEL_LINK))
    bot.send_message(
        message.chat.id,
        "VPN Pro - 50,000 so'm\n\n"
        "Nimalar kiradi:\n"
        "Eng tez ulanish\n"
        "To'liq himoya\n"
        "Barcha qurilmalar\n"
        "24/7 ishlaydi\n"
        "Shaxsiy server\n"
        "Ustunlik xizmat\n"
        "O'rnatish yordam\n\n"
        "Narx: 50,000 so'm\n\n"
        "Buyurtma berish uchun adminga yozing:\n\n"
        "Admin: " + ADMIN_NAME + "\n"
        "@" + ADMIN_USERNAME,
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "🤖 Bot yasash")
def bot_menu(message):
    if not is_subscribed(message.from_user.id):
        sub_required(message)
        return
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Oddiy bot - 50,000 so'm")
    markup.add("O'rta bot - 100,000 so'm")
    markup.add("Murakkab bot - 200,000 so'm")
    markup.add("🔙 Orqaga")
    bot.send_message(
        message.chat.id,
        "Bot yasash narxlari:\n\n"
        "Oddiy bot - 50,000 so'm\n"
        "Buyruqlar, tugmalar, javoblar\n\n"
        "O'rta bot - 100,000 so'm\n"
        "Obuna tizimi, admin panel\n\n"
        "Murakkab bot - 200,000 so'm\n"
        "To'liq avtomatik tizim\n\n"
        "Turni tanlang:",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: "bot -" in str(m.text))
def bot_order(message):
    if not is_subscribed(message.from_user.id):
        sub_required(message)
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📞 " + ADMIN_NAME + " ga yozish", url=ADMIN_LINK))
    bot.send_message(
        message.chat.id,
        "Siz tanladingiz:\n" + message.text + "\n\n"
        "Buyurtma berish uchun adminga yozing:\n\n"
        "Admin: " + ADMIN_NAME + "\n"
        "@" + ADMIN_USERNAME + "\n\n"
        "Bot haqida batafsil ayting!",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "📞 Murojaat")
def contact(message):
    if not is_subscribed(message.from_user.id):
        sub_required(message)
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💬 Yozish", url=ADMIN_LINK))
    markup.add(types.InlineKeyboardButton("📢 " + CHANNEL_NAME, url=CHANNEL_LINK))
    bot.send_message(
        message.chat.id,
        "Boglanish:\n\n"
        "Admin: " + ADMIN_NAME + "\n"
        "@" + ADMIN_USERNAME + "\n\n"
        "Kanal: " + CHANNEL_NAME + "\n\n"
        "Ish vaqti: 09:00 - 22:00",
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "ℹ️ Haqida")
def about(message):
    if not is_subscribed(message.from_user.id):
        sub_required(message)
        return
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📢 " + CHANNEL_NAME, url=CHANNEL_LINK))
    markup.add(types.InlineKeyboardButton("📞 Admin", url=ADMIN_LINK))
    bot.send_message(
        message.chat.id,
        "Biz haqimizda:\n\n"
        "VPN - 20,000 so'm\n"
        "VPN Pro - 50,000 so'm\n\n"
        "Bot yasash:\n"
        "Oddiy - 50,000 so'm\n"
        "O'rta - 100,000 so'm\n"
        "Murakkab - 200,000 so'm\n\n"
        "Kanal: " + CHANNEL_NAME + "\n"
        "Admin: @" + ADMIN_USERNAME,
        reply_markup=markup
    )

@bot.message_handler(func=lambda m: m.text == "🔙 Orqaga")
def back(message):
    start(message)

@bot.message_handler(content_types=['text'])
def other(message):
    if not is_subscribed(message.from_user.id):
        sub_required(message)
        return
    start(message)

print("Bot ishga tushdi!")
bot.polling(none_stop=True)
        
