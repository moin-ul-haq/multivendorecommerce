from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings


@shared_task
def send_signup_email(user_email, user_name):
    subject = 'Welcome'
    message = f'Hello {user_name}, your account has been created successfully.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)
    return True


@shared_task
def send_login_email(user_email, user_name):
    subject = 'Login Notification'
    message = f'Hello {user_name}, you have logged in to your account.'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email], fail_silently=False)
    return True
