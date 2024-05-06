from datetime import datetime
import random
from telegram import Bot
from django.conf import settings

from myapp.models import Verification

bot = Bot(token=settings.TELEGRAM_TOKEN)


def generate_and_send_verification_code(phone_number):
    # Генерация 6-значного кода
    code = f"{random.randint(100000, 999999)}"

    # Сохраните или обновите запись в базе данных
    verification, created = Verification.objects.update_or_create(
        phone_number=phone_number,
        defaults={'verification_code': code, 'is_verified': False}
    )

    # Отправьте код клиенту
    bot.send_message(chat_id=phone_number, text=f"Ваш код подтверждения: {code}")


async def send_telegram_message(order):
    chat_id = settings.TELEGRAM_CHAT_ID
    now = datetime.now().strftime("%H:%M:%S")
    message_text = (f"New order received: Order #{order.pk}, by {order.customer_name}. "
                    f"Created at: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')} "
                    f"Must call by: {order.must_complete_by.strftime('%Y-%m-%d %H:%M:%S')} "
                    f"Sent at {now}")
    await bot.send_message(chat_id=chat_id, text=message_text)