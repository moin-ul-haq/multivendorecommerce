from .models import Order
from payment.models import Payment
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=Order)
def create_payment(sender, instance, created, **kwargs):
    print("Yes")
    if created:
        Payment.objects.create(order=instance)
