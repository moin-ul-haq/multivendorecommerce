from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_order_status_email(user_email, order_id, status):
    subject = "Order Update"
    message = f"Order #{order_id} status is {status}"
    send_mail(
        subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False
    )
    return True


@shared_task
def send_order_confirmation_email(user_email, order_id):
    subject = "Order Confirmed"
    message = f"Your order #{order_id} has been confirmed."
    send_mail(
        subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False
    )
    return True
