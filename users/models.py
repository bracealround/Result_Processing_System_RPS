from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from .manager import CustomUserManager


# Create your models here.
class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    is_teacher = models.BooleanField("teacher status", default=False)
    is_student = models.BooleanField("student status", default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = [
        "is_teacher",
    ]

    objects = CustomUserManager()

    def __str__(self):
        return self.email
