from django.contrib import admin
from django.utils.html import format_html
from .models import Client, ClientMembership, ClientGroup, Building, BuildingUser, BuildingDatabase


@admin.register(BuildingDatabase)
class BuildingDatabaseAdmin(admin.ModelAdmin):
    list_display = ("name", "db_file_link", "uploaded_by", "uploaded_at", "description_short")
    search_fields = ("name", "description")
    readonly_fields = ("uploaded_at", "uploaded_by", "db_file_link")
    list_per_page = 20

    fieldsets = (
        (None, {
            "fields": ("name", "db_file", "description"),
            "description": "Upload a SQLite database file such as db.sqlite3 here.",
        }),
        ("Metadata (auto)", {
            "fields": ("uploaded_by", "uploaded_at"),
            "classes": ("collapse",),
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.uploaded_by_id:
            obj.uploaded_by = request.user
        super().save_model(request, obj, form, change)

    @admin.display(description="File")
    def db_file_link(self, obj):
        if obj.db_file:
            return format_html(
                '<a href="{}" target="_blank">{}</a>',
                obj.db_file.url,
                obj.db_file.name.split("/")[-1]
            )
        return "—"

    @admin.display(description="Description")
    def description_short(self, obj):
        return (obj.description[:60] + "…") if obj.description and len(obj.description) > 60 else (obj.description or "—")


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
    list_display = (
        "name", "client", "city", "country", "building_type",
        "gross_floor_area", "area_unit", "building_database", "is_active"
    )
    search_fields = ("name", "client__name", "city", "address")
    list_filter = ("client", "country", "building_type", "is_active")
    readonly_fields = ("created_at", "updated_at", "photo_preview")

    fieldsets = (
        ("Identity", {
            "fields": ("client", "name", "code", "is_active"),
        }),
        ("Location", {
            "fields": ("address", "city", "state", "postal", "country",
                       "currency", "timezone", "latitude", "longitude"),
        }),
        ("Building Attributes", {
            "fields": ("building_type", "gross_floor_area", "area_unit",
                       "occupancy", "dashboard_chart"),
        }),
        ("Energy & Weather", {
            "fields": ("energy_star_id", "weather_unit_group",
                       "base_temp_cooling", "base_temp_heating"),
        }),
        ("Building Database", {
            "fields": ("building_database",),
            "description": "Choose the uploaded SQLite database file for this building.",
        }),
        ("Photo", {
            "fields": ("photo", "photo_preview"),
        }),
        ("Technical Contact", {
            "fields": ("tech_contact_name", "tech_contact_email",
                       "tech_contact_phone", "building_phone", "building_fax"),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Current Photo")
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height:120px;border-radius:4px;" />',
                obj.photo.url,
            )
        return "No photo uploaded"


@admin.register(BuildingUser)
class BuildingUserAdmin(admin.ModelAdmin):
    list_display = ("full_name", "client", "email", "is_active")
    search_fields = ("full_name", "email", "client__name")
    list_filter = ("client", "is_active")
    filter_horizontal = ("groups", "buildings")

