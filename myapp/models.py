from django.db import models
from datetime import timedelta
from django.utils import timezone
class Verification(models.Model):
    phone_number = models.CharField(max_length=15, unique=True)
    verification_code = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    verification = models.OneToOneField(Verification, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    must_complete_by = models.DateTimeField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        if not self.must_complete_by:
            self.must_complete_by = self.created_at + timedelta(minutes=30)
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order #{self.pk} by {self.customer_name}"