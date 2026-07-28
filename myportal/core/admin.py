# myportal/core/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Client, ClientGroup,
    Building, BuildingUser, BuildingDatabase,
    TIMEZONE_CHOICES,
)


# ─────────────────────────────────────────────
# BUILDING DATABASE  (admin-only upload — not exposed on frontend)
# ─────────────────────────────────────────────

@admin.register(BuildingDatabase)
class BuildingDatabaseAdmin(admin.ModelAdmin):
    list_display    = ("name", "db_file_link", "uploaded_by", "uploaded_at", "description_short")
    search_fields   = ("name", "description")
    readonly_fields = ("uploaded_at", "uploaded_by", "db_file_link")
    list_per_page   = 20

    fieldsets = (
        (None, {
            "fields": ("name", "db_file", "description"),
            "description": (
                "⚠️ Upload a SQLite (.sqlite3) database file here. "
                "Once uploaded, link it to a Building via the Building admin or the frontend Building form."
            ),
        }),
        ("Metadata (auto-filled)", {
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
                obj.db_file.name.split("/")[-1],
            )
        return "—"

    @admin.display(description="Description")
    def description_short(self, obj):
        if obj.description and len(obj.description) > 60:
            return obj.description[:60] + "…"
        return obj.description or "—"


# ─────────────────────────────────────────────
# CLIENT
# ─────────────────────────────────────────────

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display  = ("name", "code", "country", "partnership", "phone", "contact_person", "email", "is_active")
    search_fields = ("name", "code", "contact_person", "email", "city")
    list_filter   = ("is_active", "country", "partnership")
    readonly_fields = ("code", "created_at", "logo_preview")
    list_per_page = 25

    fieldsets = (
        ("Identity", {
            "fields": ("name", "code", "partnership", "is_active"),
            "description": "Client slug (code) is auto-generated from the name.",
        }),
        ("Address", {
            "fields": ("address", "city", "state", "postal", "country"),
        }),
        ("Contact", {
            "fields": ("contact_person", "email", "phone", "fax"),
        }),
        ("Logo", {
            "fields": ("logo", "logo_preview"),
        }),
        ("Timestamps", {
            "fields": ("created_at",),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Logo Preview")
    def logo_preview(self, obj):
        if obj.logo:
            return format_html(
                '<img src="{}" style="max-height:80px; border-radius:4px;" />',
                obj.logo.url,
            )
        return "No logo uploaded"


# ─────────────────────────────────────────────
# CLIENT GROUP  (mirrors frontend group permissions grid)
# ─────────────────────────────────────────────

@admin.register(ClientGroup)
class ClientGroupAdmin(admin.ModelAdmin):
    list_display  = ("name", "client", "can_read", "can_write")
    search_fields = ("name", "client__name")
    list_filter   = ("client",)
    list_select_related = ("client",)

    fieldsets = (
        ("Group Identity", {
            "fields": ("client", "name", "description"),
        }),
        ("Global Permissions", {
            "fields": ("can_read", "can_write"),
            "description": "Master read/write toggles that override per-page settings.",
        }),
        ("Per-Page Read Access", {
            "fields": (
                "read_dashboard",
                "read_users",
                "read_groups",
                "read_buildings",
                "read_clients",
                "read_profile",
            ),
            "classes": ("wide",),
        }),
        ("Per-Page Write Access", {
            "fields": (
                "write_dashboard",
                "write_users",
                "write_groups",
                "write_buildings",
                "write_clients",
                "write_profile",
            ),
            "classes": ("wide",),
        }),
    )


# ─────────────────────────────────────────────
# BUILDING  (database upload is admin-only; all other fields mirror frontend)
# ─────────────────────────────────────────────

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = (
        "name", "client", "city", "country",
        "building_type", "gross_floor_area", "area_unit",
        "building_database", "is_active",
    )
    search_fields       = ("name", "client__name", "city", "address", "code")
    list_filter         = ("client", "country", "building_type", "is_active", "area_unit")
    list_select_related = ("client", "building_database")
    readonly_fields     = ("created_at", "updated_at", "photo_preview")
    autocomplete_fields = ("client",)
    list_per_page       = 25

    fieldsets = (
        # Mirrors frontend "Basic Info" section
        ("Identity", {
            "fields": ("client", "name", "code", "is_active"),
        }),
        # Mirrors frontend "Location" tab
        ("Location", {
            "fields": (
                "address", "city", "state", "postal",
                "country", "currency", "timezone",
                "latitude", "longitude",
            ),
        }),
        # Mirrors frontend "Building Details" section
        ("Building Attributes", {
            "fields": (
                "building_type", "gross_floor_area", "area_unit",
                "occupancy", "dashboard_chart",
            ),
        }),
        # Mirrors frontend "Energy & Weather" section
        ("Energy & Weather", {
            "fields": (
                "energy_star_id", "weather_unit_group",
                "base_temp_cooling", "base_temp_heating",
            ),
        }),
        # Admin-only: database file linking (upload is done via BuildingDatabase admin)
        ("Building Database (Admin Only)", {
            "fields": ("building_database",),
            "description": (
                "🔒 Select an uploaded SQLite database to link to this building. "
                "To upload a new database file, go to Building Databases in the sidebar first."
            ),
        }),
        # Mirrors frontend photo upload
        ("Photo", {
            "fields": ("photo", "photo_preview"),
        }),
        # Mirrors frontend "Technical Contact" section
        ("Technical Contact", {
            "fields": (
                "tech_contact_name", "tech_contact_email",
                "tech_contact_phone", "building_phone", "building_fax",
            ),
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",),
        }),
    )

    @admin.display(description="Photo Preview")
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height:120px; border-radius:4px;" />',
                obj.photo.url,
            )
        return "No photo uploaded"


# ─────────────────────────────────────────────
# BUILDING USER  (mirrors frontend user_detail.html form)
# ─────────────────────────────────────────────

@admin.register(BuildingUser)
class BuildingUserAdmin(admin.ModelAdmin):
    list_display = (
        "full_name", "client", "email",
        "position", "timezone", "is_active",
    )
    search_fields       = ("full_name", "email", "client__name", "position", "employee_id")
    list_filter         = ("client", "is_active", "timezone", "view_all")
    list_select_related = ("client", "auth_user")
    filter_horizontal   = ("groups", "buildings")
    readonly_fields     = ("photo_preview",)
    list_per_page       = 25

    fieldsets = (
        # Mirrors frontend "Basic Info" section
        ("Identity", {
            "fields": ("client", "auth_user", "full_name", "email", "employee_id", "is_active"),
        }),
        # Mirrors frontend "Personal Details" section
        ("Personal Details", {
            "fields": (
                "title", "position",
                "work_phone", "cell_phone",
                "timezone",
            ),
        }),
        # Mirrors frontend photo upload
        ("Photo", {
            "fields": ("photo", "photo_preview"),
        }),
        # Mirrors frontend notification/preference checkboxes
        ("Preferences & Notifications", {
            "fields": (
                "view_all",
                "daily_summary",
                "single_report",
                "receive_assigned",
                "daily_delivery",
            ),
            "description": "These settings mirror the notification toggles on the frontend user form.",
        }),
        # Access control — matches frontend group assignment
        ("Access Control", {
            "fields": ("groups", "buildings"),
            "description": "Assign the user to a client group and specific buildings.",
        }),
    )

    @admin.display(description="Photo Preview")
    def photo_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" style="max-height:100px; border-radius:50%;" />',
                obj.photo.url,
            )
        return "No photo uploaded"