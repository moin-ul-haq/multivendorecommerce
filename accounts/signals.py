from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from .tasks import send_signup_email


@receiver(post_save, sender=User)
def user_created(sender, instance, created, **kwargs):
    if created:
        send_signup_email.delay(instance.email, instance.name)
