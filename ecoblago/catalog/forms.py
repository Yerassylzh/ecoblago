from django.forms import CharField, TextInput, CheckboxInput, BooleanField, ImageField
from django.core.validators import EmailValidator
from django.forms import ModelForm, FileInput, TextInput, Textarea, ValidationError, ClearableFileInput

from catalog.models import Product
from authpage.validators import PhoneNumberValidator

from django import forms
from django.core.exceptions import ValidationError

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "phone_number",
            "cost",
            "description",
        ]
        widgets = {
            "title": TextInput(
                attrs={
                    "placeholder": "Название",
                    "type": "text",
                    "id": "title",
                }
            ),
            "phone_number": TextInput(
                attrs={
                    "placeholder": "Номер телефона",
                    "type": "text",
                    "id": "phone-number",
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