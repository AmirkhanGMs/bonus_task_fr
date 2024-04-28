from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from .telegram_bot import send_telegram_message

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        message = f"New order received: Order #{instance.pk}, by {instance.customer_name}. Must call by {instance.must_complete_by}."
        send_telegram_message(message)
