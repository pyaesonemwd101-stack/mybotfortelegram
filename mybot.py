import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import time
import os

# --- SECURE TOKEN LOADING ---
# On GitHub/Cloud, it looks for an environment variable named 'BOT_TOKEN'
# On your local PC, it will use the fallback if you haven't set the variable.
BOT_TOKEN = os.getenv("BOT_TOKEN")

# IMPORTANT: If you want to test locally, put the token here temporarily.
# But BEFORE you 'commit' and 'push' to GitHub, make sure it is empty or os.getenv only.
if not BOT_TOKEN:
    BOT_TOKEN = "" # DO NOT LEAVE YOUR TOKEN HERE ON GITHUB

bot = telebot.TeleBot(BOT_TOKEN)

# Admin Telegram link
ADMIN_LINK = "https://t.me/drsaipleasurebotadmin"

# --- CONFIGURATION ---
CHANNELS = [
    {"name": "ညစာ", "link": "https://t.me/+kU-EYauYFGIzNGVl", "emoji": "🍜"},
    {"name": "Book Pleasure", "link": "https://t.me/+_f_nIWLphJxmOGM1", "emoji": "📚"},
    {"name": "Japan Pleasure", "link": "https://t.me/+0-WFrrBK7H84ZjI1", "emoji": "🇯🇵"},
    {"name": "Eng Pleasure", "link": "https://t.me/+paNDwIR5VVc0NWY1", "emoji": "💯"}
]

DESTINATION_CHANNELS = ["-1003872737032", "-1003806042648", "-1003891024687", "-1003740090519"]

# --- HANDLERS ---
@bot.message_handler(content_types=['new_chat_members', 'left_chat_member'])
def handle_service_messages(message):
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"❌ Error: {e}")

@bot.message_handler(commands=['channels'])
def show_channels(message):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for channel in CHANNELS:
        button = InlineKeyboardButton(text=f"{channel['emoji']} {channel['name']}", url=channel['link'])
        keyboard.add(button)
    admin_button = InlineKeyboardButton(text="👤 Contact Admin", url=ADMIN_LINK)
    keyboard.add(admin_button)
    bot.send_message(message.chat.id, "📋 **Dr Sai's Channels**\n\nClick to join:", reply_markup=keyboard, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(KeyboardButton("📋 View Channels"), KeyboardButton("📩 Contact Admin"), KeyboardButton("ℹ️ Help"))
    welcome_text = f"👋 **Welcome to Dr Sai's Manager!**\n\nManaging {len(CHANNELS)} channels."
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "📋 View Channels":
        show_channels(message)
    elif message.text == "📩 Contact Admin":
        bot.send_message(message.chat.id, f"👤 **Admin:** {ADMIN_LINK}", parse_mode="Markdown")
    elif message.text == "ℹ️ Help":
        bot.reply_to(message, "Commands: /channels, /start")

if __name__ == "__main__":
    print("✅ Bot engine active...")
    bot.infinity_polling()
