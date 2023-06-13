from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    home_address = models.CharField(max_length=400, blank=True, verbose_name='آدرس منزل')

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    
class EmailConfirmation(models.Model):
    token = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=11)
    username = models.CharField(max_length= 100)
    password = models.CharField(max_length=60, null=True)
    code = models.SmallIntegerField()
    expiration_date = models.DateTimeField(auto_now_add=True)