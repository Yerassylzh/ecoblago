from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser

from authpage.validators import PhoneNumberValidator


class User(AbstractUser):
    phone_number = models.CharField(
        verbose_name="Номер телефона",
        name="phone_number",
        validators=[
            PhoneNumberValidator(),
        ],
        max_length=255,
    )

    about = models.TextField(
        verbose_name="О себе",
        name="about",
        default="",
    )

    image = models.ImageField(
        verbose_name="изображение",
        name="image",
        upload_to="uploads/",
        null=True,
    )

    def __str__(self):
        return self.username
