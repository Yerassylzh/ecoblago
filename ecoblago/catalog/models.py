from django.db import models
from django.core.validators import EmailValidator
from authpage.models import User


class Feedback(models.Model):
    text = models.TextField(
        verbose_name="текст",
        name="text",
    )

    rating = models.PositiveSmallIntegerField(
        verbose_name="оценка",
        name="rating",
    )

    date = models.DateField(
        verbose_name="дата",
        auto_now=True,
    )

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="my_feedbacks",
        related_query_name="my_feedbacks",
    )

    seller_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="feedbacks",
        related_query_name="feedbacks",
    )
