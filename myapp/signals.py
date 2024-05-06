from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .telegram_bot import send_telegram_message
from asgiref.sync import async_to_sync

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        async_to_sync(send_telegram_message)(instance)


def send_order_notification(sender, instance, created, **kwargs):
    if created:
        # Обернем асинхронную функцию в sync
        async_to_sync(send_telegram_message)(instance)