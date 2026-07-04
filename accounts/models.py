from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    role_choices = [
        ("customer", "Customer"),
        ("owner", "Owner"),
        ("admin", "Admin"),
    ]
    name = models.CharField(max_length=30)
    age = models.IntegerField()
    email = models.EmailField()
    address = models.TextField()
    role = models.CharField(choices=role_choices, default="customer")
