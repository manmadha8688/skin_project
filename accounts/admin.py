from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Accounts

class CustomUserAdmin(UserAdmin):
    list_display = ("email", "username", "role", "is_active", "is_staff")
    search_fields = ("email", "username")
    readonly_fields = ("date_joined", "last_login")

    fieldsets = (
        (None, {"fields": ("email", "username")}),
        ("Personal Info", {"fields": ("name", "address")}),
        ("Permissions", {"fields": ("role", "is_active", "is_staff", "is_superuser")}),
        ("Important Dates", {"fields": ("date_joined", "last_login")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "name",'role', "password1", "password2"),
        }),
    )

    ordering = ("email",)

admin.site.register(Accounts, CustomUserAdmin)
