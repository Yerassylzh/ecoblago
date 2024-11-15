from django.db import models


class User(models.Model):
    first_name = models.CharField(
        name="first_name",
        null=False,
        max_length=255,
    )

    last_name = models.CharField(
        name="last_name",
        null=False,
        max_length=255,
    )

    # format: 77088221205
    phone = models.CharField(
        name="phone",
        null=False,
        max_length=255,
        unique=True,
    )

    email = models.EmailField(
        name="email",
        null=False,
        unique=True,
    )

    password = models.CharField(
        name="password",
        null=False,
        max_length=255,
        default="secret",
    )
