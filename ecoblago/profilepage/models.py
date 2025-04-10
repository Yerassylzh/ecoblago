from django.db import models
from django.core.validators import EmailValidator
from django.contrib.auth.models import AbstractUser

from authpage.validators import PhoneNumberValidator
from authpage.models import User


class Feedback(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="authored_feedbacks",
        related_query_name="authored_feedbacks",
    )
    
    reciever = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recieved_feedbacks",
        related_query_name="recieved_feedbacks",
    )
    
    content = models.TextField(
        verbose_name="Контент",
        name="content",
    )

    date = models.DateField(
        verbose_name="Дата",
        name="date",
        auto_now=True,
    )
