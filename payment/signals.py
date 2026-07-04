from django.db.models.signals import post_save
from .models import Payment
from django.dispatch import receiver
from order.models import Order
from order.tasks import send_order_confirmation_email


@receiver(post_save, sender=Payment)
def change_order_status(instance, sender, **kwargs):
    order = instance.order
    if instance.status == "confirmed":
        order.status = "confirmed"
        order.save()
        send_order_confirmation_email.delay(order.user.email, order.id)
