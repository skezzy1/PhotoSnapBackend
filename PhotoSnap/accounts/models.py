from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length = 50)
    username = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.username
