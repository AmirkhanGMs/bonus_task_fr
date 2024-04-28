from django.db import models

class Order(models.Model):
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    must_complete_by = models.DateTimeField()

    def __str__(self):
        return f"Order #{self.pk} by {self.customer_name}"