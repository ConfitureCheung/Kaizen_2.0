from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProviderProfile


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Roles", {"fields": ("is_provider", "is_client_user")}),
    )
    list_display = ("username", "email", "is_staff", "is_superuser", "is_provider", "is_client_user")
    list_filter = ("is_staff", "is_superuser", "is_provider", "is_client_user")


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    list_display = ("company_name", "user", "contact_email", "phone")
    search_fields = ("company_name", "user__username", "contact_email")
