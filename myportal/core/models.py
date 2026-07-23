from django.conf import settings
from django.db import models
from django.utils.text import slugify


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


class DatabaseConnection(models.Model):
    ENGINE_CHOICES = [
        ("sqlite", "SQLite"),
        ("postgres", "PostgreSQL"),
        ("mysql", "MySQL"),
        ("mssql", "MS SQL Server"),
    ]

    name = models.CharField(max_length=100, unique=True)
    engine = models.CharField(max_length=20, choices=ENGINE_CHOICES, default="postgres")
    host = models.CharField(max_length=200, blank=True)
    port = models.IntegerField(default=5432)
    database = models.CharField(max_length=200)
    username = models.CharField(max_length=200, blank=True)
    password = models.CharField(max_length=200, blank=True)
    options = models.JSONField(blank=True, default=dict)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


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


class Building(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="buildings")
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("client", "name")
        ordering = ["client__name", "name"]

    def __str__(self):
        return f"{self.client.name} / {self.name}"


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
