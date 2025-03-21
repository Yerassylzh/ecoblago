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
        unique=True,
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

    liked_products = models.ManyToManyField(
        "catalog.Product",
        verbose_name="Понравившиеся товары",
        name="liked_products",
        related_name="liked_by",
        related_query_name="liked_by",
    )

    def __str__(self):
        return self.username
