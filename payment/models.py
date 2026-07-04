from django.db import models
from order.models import Order


class Payment(models.Model):
    status_choices = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("shipped", "Shipped"),
        ("delivered", "Delivered"),
    ]
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="payments")
    status = models.CharField(choices=status_choices, default="pending")
    total_amount = models.DecimalField(
        max_digits=12, decimal_places=2, null=True, blank=True
    )

    def save(self, *args, **kwargs):
        self.total_amount = self.order.total_amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order of {self.order.user.name} of price {self.total_amount}"
