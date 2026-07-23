from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


PARTNERSHIP_CHOICES = [
    ("skyforce", "Skyforce"),
    ("others", "Others"),
]

COUNTRY_CHOICES = [
    ("HK", "Hong Kong"),
    ("CN", "China"),
    ("JP", "Japan"),
    ("KR", "South Korea"),
    ("SG", "Singapore"),
    ("TW", "Taiwan"),
    ("AU", "Australia"),
    ("GB", "United Kingdom"),
    ("US", "United States"),
    ("CA", "Canada"),
    ("DE", "Germany"),
    ("FR", "France"),
    ("NL", "Netherlands"),
    ("AE", "UAE"),
    ("IN", "India"),
]

CURRENCY_CHOICES = [
    ("HKD", "HKD – Hong Kong Dollar"),
    ("USD", "USD – US Dollar"),
    ("CNY", "CNY – Chinese Yuan"),
    ("GBP", "GBP – British Pound"),
    ("AUD", "AUD – Australian Dollar"),
    ("SGD", "SGD – Singapore Dollar"),
    ("JPY", "JPY – Japanese Yen"),
]

TIMEZONE_CHOICES = [
    ("Asia/Hong_Kong", "Asia/Hong Kong (UTC+8)"),
    ("Asia/Shanghai", "Asia/Shanghai (UTC+8)"),
    ("Asia/Singapore", "Asia/Singapore (UTC+8)"),
    ("Asia/Tokyo", "Asia/Tokyo (UTC+9)"),
    ("Europe/London", "Europe/London (UTC+0/+1)"),
    ("America/New_York", "America/New_York (UTC-5/-4)"),
    ("Australia/Sydney", "Australia/Sydney (UTC+10/+11)"),
]

BUILDING_TYPE_CHOICES = [
    ("office", "Office"),
    ("retail", "Retail"),
    ("hotel", "Hotel"),
    ("residential", "Residential"),
    ("industrial", "Industrial"),
    ("mixed", "Mixed Use"),
    ("data_centre", "Data Centre"),
    ("education", "Education"),
    ("healthcare", "Healthcare"),
    ("other", "Other"),
]

AREA_UNIT_CHOICES = [
    ("m2", "m²"),
    ("ft2", "ft²"),
]

WEATHER_UNIT_CHOICES = [
    ("metric", "Metric (°C)"),
    ("imperial", "Imperial (°F)"),
]

DB_ENGINE_CHOICES = [
    ("postgres", "PostgreSQL"),
    ("mysql", "MySQL"),
    ("mssql", "MS SQL Server"),
    ("sqlite", "SQLite"),
]


class Client(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=5, choices=COUNTRY_CHOICES, default="HK", blank=True)
    partnership = models.CharField(max_length=20, choices=PARTNERSHIP_CHOICES, default="skyforce", blank=True)
    phone = models.CharField(max_length=50, blank=True)
    fax = models.CharField(max_length=50, blank=True)
    logo = models.ImageField(upload_to="client_logos/", blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.code:
            base_slug = slugify(self.name) or "client"
            unique_slug = base_slug
            counter = 1
            while Client.objects.filter(code=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.code = unique_slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ClientMembership(models.Model):
    ROLE_CHOICES = [
        ("admin", "Client Admin"),
        ("editor", "Editor"),
        ("viewer", "Viewer"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="client_memberships")
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="viewer")
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("user", "client")

    def __str__(self):
        return f"{self.user.username} - {self.client.name} ({self.role})"


class ClientGroup(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="groups")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ("client", "name")
        ordering = ["client__name", "name"]

    def __str__(self):
        return f"{self.client.name} / {self.name}"


class BuildingDatabase(models.Model):
    name = models.CharField(max_length=120, verbose_name="Database name")
    db_file = models.FileField(upload_to="building_databases/", verbose_name="Database file")
    description = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Building Database (db_test)"
        verbose_name_plural = "Building Databases (db_test)"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.name


class Building(models.Model):
    client = models.ForeignKey("Client", on_delete=models.PROTECT, related_name="buildings")
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=40, blank=True)
    is_active = models.BooleanField(default=True)

    address = models.TextField()
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, default="HK")
    currency = models.CharField(max_length=5, choices=CURRENCY_CHOICES, default="HKD")
    timezone = models.CharField(max_length=50, choices=TIMEZONE_CHOICES, default="Asia/Hong_Kong")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    building_type = models.CharField(max_length=20, choices=BUILDING_TYPE_CHOICES, blank=True)
    gross_floor_area = models.FloatField(null=True, blank=True)
    area_unit = models.CharField(max_length=5, choices=AREA_UNIT_CHOICES, default="ft2")
    occupancy = models.PositiveIntegerField(default=0)
    dashboard_chart = models.CharField(max_length=120, blank=True)

    energy_star_id = models.CharField(max_length=60, blank=True)
    weather_unit_group = models.CharField(max_length=12, choices=WEATHER_UNIT_CHOICES, default="metric")
    base_temp_cooling = models.FloatField(null=True, blank=True)
    base_temp_heating = models.FloatField(null=True, blank=True)

    building_database = models.ForeignKey(
        BuildingDatabase,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="buildings",
        verbose_name="Uploaded DB (db_test)"
    )

    photo = models.ImageField(upload_to="buildings/photos/", null=True, blank=True)

    tech_contact_name = models.CharField(max_length=100, blank=True)
    tech_contact_email = models.EmailField(blank=True)
    tech_contact_phone = models.CharField(max_length=30, blank=True)
    building_phone = models.CharField(max_length=30, blank=True)
    building_fax = models.CharField(max_length=30, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Building"
        verbose_name_plural = "Buildings"
        ordering = ["name"]

    def __str__(self):
        return self.name


class BuildingUser(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="building_users")
    auth_user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="building_user_profile",
        null=True,
        blank=True,
    )
    full_name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    employee_id = models.CharField(max_length=100, blank=True)
    groups = models.ManyToManyField(ClientGroup, blank=True, related_name="users")
    buildings = models.ManyToManyField(Building, blank=True, related_name="users")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["client__name", "full_name"]

    def __str__(self):
        return f"{self.client.name} / {self.full_name}"

