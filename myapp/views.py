# myapp/views.py
from django.shortcuts import render, redirect, HttpResponse
from django.conf import settings
from django.utils.timezone import now
from datetime import timedelta
from asgiref.sync import sync_to_async
from telegram import Bot
from .forms import OrderForm
from .models import Order
from .models import Verification

from myapp.utils import check_verification_code
# Настройка бота Telegram
bot = Bot(token=settings.TELEGRAM_TOKEN)
# views.py или telegram_bot.py
# myapp/views.py

from django.http import HttpResponse

def verify_code(request):
    entered_code = request.GET.get('entered_code')

    if not entered_code:
        return HttpResponse("Please provide a verification code.", status=400)

    # Убедитесь, что функция check_verification_code вызывается и работает правильно
    if check_verification_code(entered_code):
        return redirect('create_order')
    else:
        return HttpResponse("Invalid verification code.", status=400)


async def send_telegram_message(order):
    chat_id = settings.TELEGRAM_CHAT_ID
    current_time = now().strftime("%H:%M:%S")

    # Определите message_text перед использованием
    message_text = (
        f"New order received: Order #{order.pk}, by {order.customer_name}. "
        f"Created at: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')} "
        f"Must call by: {order.must_complete_by.strftime('%Y-%m-%d %H:%M:%S')} "
        f"Client's phone number {order.phone_number} "
        f"Sent at {current_time}"
    )

    try:
        # Логирование для отладки
        print(f"Sending message: {message_text} to chat ID: {chat_id}")

        # Отправка сообщения в Telegram
        await bot.send_message(chat_id=chat_id, text=message_text)
    except Exception as e:
        print(f"Failed to send message: {e}")


"""async def send_telegram_message(order):
    try:
        chat_id = settings.TELEGRAM_CHAT_ID
        current_time = now().strftime("%H:%M:%S")
        message_text = (
            f"New order received: Order #{order.pk}, by {order.customer_name}. "
            f"Created at: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')} "
            f"Must call by: {order.must_complete_by.strftime('%Y-%m-%d %H:%M:%S')} "
            f"Client's phone number {order.phone_number} "
            f"Sent at {current_time}"
        )
        await bot.send_message(chat_id=chat_id, text=message_text)
    except Exception as e:
        print(f"Error sending message to Telegram: {e}")"""




async def send_test_message(request):
    try:
        # Создание объекта Order в базе данных
        test_order = await sync_to_async(Order.objects.create)(
            customer_name="Daniyal",
            phone_number="+77017007003",
            created_at=now(),
            must_complete_by=now() + timedelta(minutes=30)
        )
        # Отправка сообщения в Telegram
        await send_telegram_message(test_order)
        return HttpResponse("Message sent")
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)

def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('success')
    else:
        form = OrderForm()
    return render(request, 'myapp/create_order.html', {'form': form})

def success_view(request):
    return render(request, 'myapp/success.html')
