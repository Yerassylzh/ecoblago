from django.forms import CharField, TextInput, CheckboxInput, BooleanField, ImageField
from django.core.validators import EmailValidator
from django.forms import ModelForm, FileInput, TextInput, Textarea, ValidationError, ClearableFileInput, Form
from django import forms
from django.forms import inlineformset_factory
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from catalog.models import Product, GalleryImage, Category, Region, City
from authpage.validators import PhoneNumberValidator

class ProductForm(ModelForm):
    category_name = forms.CharField(max_length=255, label=_("Категория"))
    region_name = forms.CharField(max_length=255, label=_("Регион"))
    city_name = forms.CharField(max_length=255, label=_("Город")) 

    def clean_category_name(self):
        category_name = self.cleaned_data["category_name"]
        if not (category := Category.objects.filter(name=category_name).first()):
            return ValidationError("Выбранная категория не существует")

        self.category = category
        return category_name

    def clean_region_name(self):
        region_name = self.cleaned_data["region_name"]
        region = Region.objects.prefetch_related("cities").filter(name=region_name)
        if not (region := region.first()):
            raise ValidationError("Выберите регион")
        
        self.region = region
        return region_name

    def clean_city_name(self):
        city_name = self.cleaned_data["city_name"]
        if city_name not in {city.name for city in self.region.cities.all()}:
            raise ValidationError("Город не пренадлежит выбранному региону")

        self.city = self.region.cities.get(name=city_name)
        return city_name

    def save(self, commit=True) -> Product:
        product = super().save(commit=False)
        product.category = self.category
        product.region = self.region
        product.city = self.city
        if commit:
            product.save()
        return product

    class Meta:
        model = Product
        fields = [
            "title",
            "phone_number",
            "cost",
            "description",
            "email",
        ]

# GalleryImageFormSet = inlineformset_factory(
#     Product,
#     GalleryImage,
#     fields=["image"],
# )
