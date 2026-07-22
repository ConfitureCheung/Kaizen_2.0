from django.contrib import admin
from .models import Client, ClientMembership, ClientGroup, Building, BuildingUser


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "contact_person", "email", "is_active")
    search_fields = ("name", "code", "contact_person", "email")
    list_filter = ("is_active",)


@admin.register(ClientMembership)
class ClientMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "client", "role", "is_active")
    search_fields = ("user__username", "client__name")
    list_filter = ("role", "is_active")


@admin.register(ClientGroup)
class ClientGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "client")
    search_fields = ("name", "client__name")
    list_filter = ("client",)


@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ("name", "client", "city", "is_active")
    search_fields = ("name", "client__name", "city")
    list_filter = ("client", "is_active")


@admin.register(BuildingUser)
class BuildingUserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "client", "email", "is_active")
    search_fields = ("full_name", "email", "client__name")
    list_filter = ("client", "is_active")
    filter_horizontal = ("groups", "buildings")
