from django.db import models
from django.core.validators import EmailValidator
from authpage.validators import PhoneNumberValidator

class User(models.Model):
    name = models.CharField(
        verbose_name="имя пользователя",
        name="name",
        max_length=255,
    )

    surname = models.CharField(
        verbose_name="фамилия пользователя",
        name="surname",
        max_length=255,
    )

    username = models.CharField(
        verbose_name="хэндл пользователя",
        name="username",
        max_length=255,
        unique=True,
    )

    phone_number = models.CharField(
        verbose_name="Номер телефона",
        name="phone_number",
        validators=[
            PhoneNumberValidator(),
        ],
        max_length=255,
    )

    email = models.CharField(
        verbose_name="Почта",
        name="email",
        validators=[
            EmailValidator("Введите валидную почту"),
        ],
        max_length=255,
    )

    password = models.CharField(
        verbose_name="пароль",
        name="password",
        max_length=255,
    )

    about = models.TextField(
        verbose_name="О себе",
        name="about",
        default="",
        null=True,
    )

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.username
