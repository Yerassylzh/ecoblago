from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authpage.models import User


class CustomUserAdmin(UserAdmin):
    model = User
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ("phone_number", "about")}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {"fields": ("phone_number", "about")}),
    )


admin.site.register(User, UserAdmin)
