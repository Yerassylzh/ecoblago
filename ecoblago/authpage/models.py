from django.db import models
from django.core.validators import EmailValidator
from authpage.validators import PhoneNumberValidator

class User(models.Model):
    username = models.CharField(
        verbose_name="имя пользователя",
        name="username",
        max_length=255,
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

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self):
        return self.username
