from datetime import datetime

from telegram import Bot
from django.conf import settings

bot = Bot(token=settings.TELEGRAM_TOKEN)

async def send_telegram_message(order):
    chat_id = settings.TELEGRAM_CHAT_ID
    now = datetime.now().strftime("%H:%M:%S")
    message_text = (f"New order received: Order #{order.pk}, by {order.customer_name}. "
                    f"Created at: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')} "
                    f"Must call by: {order.must_complete_by.strftime('%Y-%m-%d %H:%M:%S')} "
                    f"Sent at {now}")
    await bot.send_message(chat_id=chat_id, text=message_text)