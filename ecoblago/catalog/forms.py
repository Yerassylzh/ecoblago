from django.forms import CharField, TextInput, CheckboxInput, BooleanField, ImageField
from django.core.validators import EmailValidator
from django.forms import ModelForm, FileInput, TextInput, Textarea

from catalog.models import Product
from authpage.validators import PhoneNumberValidator

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            "image",
            "title",
            "region",
            "city",
            "phone_number",
            "location",
            "cost",
            "description",
        ]
        widgets = {
            "image": FileInput(
                attrs={
                    "type": "file",
                    "id": "image",
                }
            ),
            "title": TextInput(
                attrs={
                    "placeholder": "Название",
                    "type": "text",
                    "id": "title",
                }
            ),
            "region": TextInput(),  # has special implementation
            "city": TextInput(),  # has special implementation
            "phone_number": TextInput(
                attrs={
                    "placeholder": "Номер телефона",
                    "type": "text",
                    "id": "phone-number",
                }
            ),
            "location": TextInput(
                attrs={
                    "placeholder": "Местоположение",
                    "type": "text",
                    "id": "location",
                }
            ),
            "cost": TextInput(
                attrs={
                    "placeholder": "Цена",
                    "type": "text",
                    "id": "cost",
                }
            ),
            "description": Textarea(
                attrs={
                    "placeholder": "Описание",
                    "class": "textarea-field",
                    "id": "description",
                }
            ),
        }