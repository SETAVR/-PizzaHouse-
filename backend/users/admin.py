from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Profile", {"fields": ("phone", "address", "avatar", "bio")}),
    )
    list_display = ("username", "email", "phone", "is_staff", "is_active")
