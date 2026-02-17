import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import datetime
import time
import os

# --- CLOUD SECURITY ---
# This pulls the token from the hosting service's environment variables (Secrets)
# On your local PC, it will use the fallback if the environment variable isn't set.
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    # Fallback for local testing only. 
    # REMOVE THIS LINE before making your GitHub repo 'Public' if you want max security.
    BOT_TOKEN = "8516246567:AAE7fmvW4xmBkgWRsQ5WVPGHJJdEBNJPycM"

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
    """Deletes 'User joined' or 'User left' messages automatically to keep chat clean"""
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except Exception as e:
        print(f"❌ Error deleting service message: {e}")

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
    welcome_text = f"👋 **Welcome to Dr Sai's Manager!**\n\nManaging {len(CHANNELS)} channels 24/7."
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):
    if message.text == "📋 View Channels":
        show_channels(message)
    elif message.text == "📩 Contact Admin":
        bot.send_message(message.chat.id, f"👤 **Admin:** {ADMIN_LINK}", parse_mode="Markdown")
    elif message.text == "ℹ️ Help":
        bot.reply_to(message, "Available Commands:\n/start - Restart Bot\n/channels - Show Links")

# --- START THE BOT ---
if __name__ == "__main__":
    # logger to help you see the bot status in your cloud logs
    print("✅ Bot engine initialized.")
    print("🚀 Connection established. Bot is now active 24/7.")
    # infinity_polling is the 'Golden Rule' for cloud bots to prevent freezing
    bot.infinity_polling(timeout=10, long_polling_timeout=5)