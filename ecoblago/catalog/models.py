from django.db import models
from django.core.validators import EmailValidator

from PIL import Image

from authpage.models import User
from authpage.validators import PhoneNumberValidator

class Category(models.Model):
    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    name = models.CharField(
        verbose_name="название",
        name="name",
        max_length=255,
    )

    def __str__(self):
        return self.name


class Region(models.Model):
    class Meta:
        verbose_name = "регион"
        verbose_name_plural = "регионы"

    name = models.CharField(
        verbose_name="название",
        name="name",
        max_length=255,
    )

    def __str__(self):
        return self.name


class City(models.Model):
    class Meta:
        verbose_name = "город"
        verbose_name_plural = "города"

    name = models.CharField(
        verbose_name="название",
        name="name",
        max_length=255,
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="cities",
        related_query_name="cities",
    )   

    def __str__(self):
        return self.name


class Product(models.Model):
    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"

    title = models.CharField(
        verbose_name="название",
        name="title",
        max_length=255,
    )

    phone_number = models.CharField(
        verbose_name="номер телефона",
        name="phone_number",
        validators=[
            PhoneNumberValidator(),
        ],
        max_length=255,
    )

    email = models.EmailField(
        verbose_name="email",
        name="email",
        validators=[
            EmailValidator(),
        ],
        max_length=255,
    )

    cost = models.PositiveIntegerField(
        verbose_name="цена",
        name="cost",
    )

    description = models.TextField(
        verbose_name="описание",
        name="description",
    )

    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="products",
        related_query_name="products",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        related_query_name="products",
    )

    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="products",
        related_query_name="products",
    )

    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="products",
        related_query_name="products",
    )


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


class GalleryImage(models.Model):
    image = models.ImageField(
        verbose_name="фото",
        upload_to="uploads/"
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="gallery_images",
        related_query_name="gallery_images",
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)
            original_width, original_height = img.size

            target_aspect_ratio = 460 / 300

            original_aspect_ratio = original_width / original_height

            if original_aspect_ratio > target_aspect_ratio:
                new_width = int(original_height * target_aspect_ratio)
                offset = (original_width - new_width) // 2
                crop_box = (offset, 0, original_width - offset, original_height)
            else:
                new_height = int(original_width / target_aspect_ratio)
                offset = (original_height - new_height) // 2
                crop_box = (0, offset, original_width, original_height - offset)

            cropped_img = img.crop(crop_box)

            cropped_img.save(self.image.path)
