from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authpage.models import User
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ("title", "cost", "seller")
    # list_filter = ('available', 'created', 'updated')
    # search_fields = ('name', 'description')

admin.site.register(Product, ProductAdmin)
