from telegram import Bot
from django.conf import settings

bot = Bot(token=settings.TELEGRAM_TOKEN)

def send_telegram_message(text):
    chat_id = "YOUR_CHAT_ID_HERE"  # Замените на ваш Chat ID
    bot.send_message(chat_id=chat_id, text=text)
