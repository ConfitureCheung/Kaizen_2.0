import os
import json
import requests
import sqlite3

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.db.models.deletion import ProtectedError
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.exceptions import PermissionDenied

from .models import Client, Building, ClientGroup, BuildingUser, BuildingDatabase
from .models import COUNTRY_CHOICES, PARTNERSHIP_CHOICES, CURRENCY_CHOICES, TIMEZONE_CHOICES, BUILDING_TYPE_CHOICES, AREA_UNIT_CHOICES, WEATHER_UNIT_CHOICES
from accounts.forms import UserProfileForm
from accounts.models import UserProfile

# from .views import get_sidebar_context, get_allowed_client_ids, get_allowed_client_ids, get_sidebar_context
from .sidebar import get_allowed_client_ids, get_sidebar_context


WEATHER_API_KEY = "e9877c4893e043fd8f632826262003"
GOOGLE_MAPS_API_KEY = "AIzaSyCwvTyOK-c-n0aO80xVtGfVejLuZRtb5Q0"

PAGE_LIST = ["Dashboard", "Users", "Groups", "Buildings", "Clients", "Profile"]


@login_required
def dashboard_view(request):
    client_ids = get_allowed_client_ids(request.user)

    selected_client_id = request.GET.get("client")
    selected_client = None

    if selected_client_id:
        try:
            selected_client_id = int(selected_client_id)
        except (TypeError, ValueError):
            raise PermissionDenied

        if selected_client_id not in client_ids:
            raise PermissionDenied

        clients = Client.objects.filter(id=selected_client_id).prefetch_related("buildings")
        selected_client = clients.first()
    else:
        clients = Client.objects.filter(id__in=client_ids).prefetch_related("buildings")
        selected_client = clients.order_by("pk").first()

    # ── 1. Building Location: 1st building created per client ──────────────────
    first_buildings = []
    for client in clients:
        first_b = client.buildings.order_by("pk").first()
        if first_b:
            first_buildings.append(first_b)

    map_building = first_buildings[0] if first_buildings else None

    # ── 2. Data Collection Device Status ──────────────────────────────────────
    all_buildings = Building.objects.filter(
        client_id__in=clients.values_list("id", flat=True)
    ).select_related("building_database").order_by("pk")

    device_status_rows = []
    any_offline = False

    for building in all_buildings:
        db = building.building_database
        if not db:
            continue

        connected = False
        try:
            db_path = db.db_file.path
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                conn.cursor().execute("SELECT 1")
                conn.close()
                connected = True
        except Exception:
            connected = False

        if not connected:
            any_offline = True

        device_status_rows.append({
            "building": building,
            "db": db,
            "connected": connected,
        })

    # ── 3. Building Reports Count ──────────────────────────────────────────────
    building_report_counts = []
    for building in all_buildings:
        db = building.building_database
        if not db:
            continue

        count = 0
        try:
            conn = sqlite3.connect(db.db_file.path)
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM report")
            count = cur.fetchone()[0]
            conn.close()
        except Exception:
            count = 0

        if count > 0 or building.building_database:
            building_report_counts.append({
                "building": building,
                "count": count,
            })

    # ── 4. Latest 5 Reports ────────────────────────────────────────────────────
    latest_reports = []
    for building in all_buildings:
        db = building.building_database
        if not db:
            continue

        try:
            conn = sqlite3.connect(db.db_file.path)
            cur = conn.cursor()
            cur.execute("""
                SELECT name, datetime
                FROM report
                ORDER BY datetime DESC
                LIMIT 5
            """)
            for row in cur.fetchall():
                latest_reports.append({
                    "name": row[0],
                    "building": building,
                    "datetime": row[1],
                })
            conn.close()
        except Exception:
            pass

    latest_reports.sort(
        key=lambda r: r["datetime"] if r["datetime"] else "",
        reverse=True
    )
    latest_reports = latest_reports[:5]

    return render(request, "dashboard.html", {
        **get_sidebar_context(request.user),
        "clients": clients,
        "selected_client": selected_client,
        "map_building": map_building,
        "first_buildings": first_buildings,
        "google_maps_api_key": GOOGLE_MAPS_API_KEY,
        "device_status_rows": device_status_rows,
        "any_offline": any_offline,
        "building_report_counts": building_report_counts,
        "latest_reports": latest_reports,
    })


# ─────────────────────────────────────────────
# USERS
# ─────────────────────────────────────────────

# ─── REPLACE users_view ───────────────────────────────────────────────────────
@login_required
def users_view(request):
    client_ids = get_allowed_client_ids(request.user)
    users = BuildingUser.objects.filter(client_id__in=client_ids).select_related("auth_user").prefetch_related("groups")
    deleted_name = request.session.pop("user_deleted_name", None)
    return render(request, "core/users.html", {
        **get_sidebar_context(request.user),
        "users": users,
        "deleted_name": deleted_name,
    })


# ─── ADD user_view_view (eye icon – read-only) ────────────────────────────────
@login_required
def user_view_view(request, pk):
    user_obj = get_object_or_404(BuildingUser, pk=pk)
    client_ids = get_allowed_client_ids(request.user)
    groups = ClientGroup.objects.filter(client_id__in=client_ids)
    selected_group = user_obj.groups.first()

    return render(request, "core/user_detail.html", {
        **get_sidebar_context(request.user),
        "user_obj": user_obj,
        "groups": groups,
        "selected_group_id": selected_group.pk if selected_group else None,
        "timezone_choices": TIMEZONE_CHOICES,
        "readonly": True,
        "errors": {},
    })


# ─── REPLACE user_detail_view (handles Add + Edit) ───────────────────────────
@login_required
def user_detail_view(request, pk=None):
    User = get_user_model()
    user_obj = get_object_or_404(BuildingUser, pk=pk) if pk else None

    client_ids = get_allowed_client_ids(request.user)
    client = Client.objects.filter(id__in=client_ids).first()
    groups = ClientGroup.objects.filter(client_id__in=client_ids)
    selected_group = user_obj.groups.first() if user_obj else None

    if request.method == "POST":
        errors = {}

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip()

        if not user_obj and not username:
            errors["username"] = "Username is required."
        if not user_obj and not password:
            errors["password"] = "Password is required."
        if not email:
            errors["email"] = "Email is required."

        if not user_obj and username and User.objects.filter(username=username).exists():
            errors["username"] = "This username is already taken."

        if not first_name and username:
            first_name = username

        if errors:
            return render(request, "core/user_detail.html", {
                **get_sidebar_context(request.user),
                "user_obj": user_obj,
                "groups": groups,
                "selected_group_id": int(request.POST.get("group")) if request.POST.get("group") else None,
                "timezone_choices": TIMEZONE_CHOICES,
                "readonly": False,
                "errors": errors,
            })

        if not user_obj:
            auth_user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                is_client_user=True,
            )
            user_obj = BuildingUser(
                client=client,
                auth_user=auth_user,
                full_name=f"{first_name} {last_name}".strip() or username,
                email=email,
            )
        else:
            auth_user = user_obj.auth_user
            auth_user.first_name = first_name
            auth_user.last_name = last_name
            auth_user.email = email
            auth_user.save()

        user_obj.full_name = f"{first_name} {last_name}".strip() or username or auth_user.username
        user_obj.email = email
        user_obj.work_phone = request.POST.get("work_phone", "").strip()
        user_obj.cell_phone = request.POST.get("cell_phone", "").strip()
        user_obj.position = request.POST.get("position", "").strip()
        user_obj.title = request.POST.get("title", "").strip()
        user_obj.timezone = request.POST.get("timezone", "Asia/Hong_Kong")
        user_obj.view_all = bool(request.POST.get("view_all"))
        user_obj.daily_summary = bool(request.POST.get("daily_summary"))
        user_obj.single_report = bool(request.POST.get("single_report"))
        user_obj.receive_assigned = bool(request.POST.get("receive_assigned"))
        user_obj.daily_delivery = request.POST.get("daily_delivery", "morning")
        user_obj.is_active = True

        if request.FILES.get("photo"):
            user_obj.photo = request.FILES["photo"]

        user_obj.save()

        group_pk = request.POST.get("group")
        if group_pk:
            group = ClientGroup.objects.filter(pk=group_pk, client_id__in=client_ids).first()
            if group:
                user_obj.groups.set([group])
        else:
            user_obj.groups.clear()

        return redirect("users")

    return render(request, "core/user_detail.html", {
        **get_sidebar_context(request.user),
        "user_obj": user_obj,
        "groups": groups,
        "selected_group_id": selected_group.pk if selected_group else None,
        "timezone_choices": TIMEZONE_CHOICES,
        "readonly": False,
        "errors": {},
    })


# ─── ADD user_delete_view ─────────────────────────────────────────────────────
@login_required
@require_POST
def user_delete_view(request, pk):
    user_obj = get_object_or_404(BuildingUser, pk=pk)
    deleted_name = user_obj.full_name or user_obj.auth_user.username
    if user_obj.auth_user:
        user_obj.auth_user.delete()
    else:
        user_obj.delete()
    request.session["user_deleted_name"] = deleted_name
    return redirect("users")


@login_required
def groups_view(request):
    client_ids = get_allowed_client_ids(request.user)
    groups = ClientGroup.objects.filter(client_id__in=client_ids)
    deleted_name = request.session.pop("group_deleted_name", None)
    return render(request, "core/groups.html", {
        **get_sidebar_context(request.user),
        "groups": groups,
        "deleted_name": deleted_name,
    })


@login_required
def group_detail_view(request):
    pk = request.GET.get("pk") or request.POST.get("pk")
    group = get_object_or_404(ClientGroup, pk=pk) if pk else None

    client_ids = get_allowed_client_ids(request.user)
    client = Client.objects.filter(id__in=client_ids).first()

    if client is None:
        return render(request, "core/group_detail.html", {
            **get_sidebar_context(request.user),
            "group": group,
            "page_list": PAGE_LIST,
            "no_client_error": True,
        })

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        if not name:
            return render(request, "core/group_detail.html", {
                **get_sidebar_context(request.user),
                "group": group,
                "page_list": PAGE_LIST,
                "name_error": True,
            })

        perm_fields = {}
        for page in PAGE_LIST:
            key = page.lower()
            perm_fields[f"read_{key}"]  = bool(request.POST.get(f"read_{key}"))
            perm_fields[f"write_{key}"] = bool(request.POST.get(f"write_{key}"))
        perm_fields["can_read"]  = bool(request.POST.get("can_read_all"))
        perm_fields["can_write"] = bool(request.POST.get("can_write_all"))

        if not group:
            group = ClientGroup.objects.create(client=client, name=name, **perm_fields)
            return redirect(reverse("group_saved", args=[group.pk]) + "?created=1")
        else:
            group.name = name
            for k, v in perm_fields.items():
                setattr(group, k, v)
            group.save()
            return redirect("group_saved", pk=group.pk)

    return render(request, "core/group_detail.html", {
        **get_sidebar_context(request.user),
        "group": group,
        "page_list": PAGE_LIST,
    })


@login_required
def group_saved_view(request, pk):
    group = get_object_or_404(ClientGroup, pk=pk)
    members = group.users.select_related("auth_user").all()
    created = request.GET.get("created")
    return render(request, "core/group_saved.html", {
        **get_sidebar_context(request.user),
        "group": group,
        "members": members,
        "page_permissions": group.get_page_permissions(),
        "created": created,
    })


@login_required
def group_members_view(request, pk):
    group = get_object_or_404(ClientGroup, pk=pk)
    client_ids = get_allowed_client_ids(request.user)

    # IDs of users already assigned to a DIFFERENT group
    other_group_user_ids = set(
        BuildingUser.objects
        .filter(client_id__in=client_ids)
        .exclude(groups__isnull=True)
        .exclude(groups=group)
        .values_list("pk", flat=True)
    )

    all_users = BuildingUser.objects.filter(client_id__in=client_ids).prefetch_related("groups")
    current_member_ids = set(group.users.values_list("pk", flat=True))

    users_with_flags = []
    for u in all_users:
        users_with_flags.append({
            "user":             u,
            "is_current_member": u.pk in current_member_ids,
            "taken_by_other":   u.pk in other_group_user_ids,
        })

    if request.method == "POST":
        selected_ids = request.POST.getlist("members")
        group.users.set(BuildingUser.objects.filter(pk__in=selected_ids))
        return redirect("groups")

    return render(request, "core/group_members.html", {
        **get_sidebar_context(request.user),
        "group": group,
        "users_with_flags": users_with_flags,
    })


@login_required
@require_POST
def group_delete_view(request, pk):
    group = get_object_or_404(ClientGroup, pk=pk)
    request.session["group_deleted_name"] = group.name
    group.delete()
    return redirect("groups")


def _building_form_context(user, building=None, errors=None):
    clients = Client.objects.filter(id__in=get_allowed_client_ids(user))
    return {
        **get_sidebar_context(user),
        "building": building,
        "errors": errors or {},
        "clients": clients,
        "uploaded_databases": BuildingDatabase.objects.all(),
        "country_choices": COUNTRY_CHOICES,
        "currency_choices": CURRENCY_CHOICES,
        "timezone_choices": TIMEZONE_CHOICES,
        "building_type_choices": BUILDING_TYPE_CHOICES,
        "area_unit_choices": AREA_UNIT_CHOICES,
        "weather_unit_choices": WEATHER_UNIT_CHOICES,
        "google_maps_api_key": GOOGLE_MAPS_API_KEY,
    }


@login_required
def buildings_view(request):
    buildings = Building.objects.filter(
        client_id__in=get_allowed_client_ids(request.user)
    ).select_related("client")
    deleted_name = request.session.pop("building_deleted_name", None)
    return render(request, "core/buildings.html", {
        **get_sidebar_context(request.user),
        "buildings": buildings,
        "deleted_name": deleted_name,
    })


@login_required
def building_detail_view(request, pk=None):
    building = get_object_or_404(Building, pk=pk) if pk else None

    if request.method == "POST":
        errors = {}
        name = request.POST.get("name", "").strip()
        address = request.POST.get("address", "").strip()
        gfa_raw = request.POST.get("gross_floor_area", "").strip()

        if not name:
            errors["name"] = "Building name is required."
        if not address:
            errors["address"] = "Address is required."

        try:
            gfa = float(gfa_raw) if gfa_raw else None
            if gfa is None:
                errors["gross_floor_area"] = "Gross floor area is required."
        except ValueError:
            errors["gross_floor_area"] = "Enter a valid number."
            gfa = None

        client_id = request.POST.get("client_id")
        client = Client.objects.filter(pk=client_id).first() if client_id else None
        if not client:
            errors["client"] = "Please select a client."

        if errors:
            class _Stub:
                pass
            b = building or _Stub()
            for k, v in request.POST.items():
                setattr(b, k, v)
            ctx = _building_form_context(request.user, building=b, errors=errors)
            return render(request, "core/building_detail.html", ctx)

        def _float(key, default=None):
            v = request.POST.get(key, "").strip()
            try:
                return float(v) if v else default
            except ValueError:
                return default

        uploaded_db = BuildingDatabase.objects.filter(
            pk=request.POST.get("building_database") or 0
        ).first()

        fields = dict(
            client=client,
            name=name,
            code=request.POST.get("code", "").strip(),
            address=address,
            city=request.POST.get("city", "").strip(),
            state=request.POST.get("state", "").strip(),
            postal=request.POST.get("postal", "").strip(),
            country=request.POST.get("country", "HK"),
            currency=request.POST.get("currency", "HKD"),
            timezone=request.POST.get("timezone", "Asia/Hong_Kong"),
            latitude=_float("latitude"),
            longitude=_float("longitude"),
            building_type=request.POST.get("building_type", ""),
            gross_floor_area=gfa,
            area_unit=request.POST.get("area_unit", "ft2"),
            occupancy=int(request.POST.get("occupancy", 0) or 0),
            dashboard_chart=request.POST.get("dashboard_chart", "").strip(),
            energy_star_id=request.POST.get("energy_star_id", "").strip(),
            weather_unit_group=request.POST.get("weather_unit_group", "metric"),
            base_temp_cooling=_float("base_temp_cooling"),
            base_temp_heating=_float("base_temp_heating"),
            building_database=uploaded_db,
            tech_contact_name=request.POST.get("tech_contact_name", "").strip(),
            tech_contact_email=request.POST.get("tech_contact_email", "").strip(),
            tech_contact_phone=request.POST.get("tech_contact_phone", "").strip(),
            building_phone=request.POST.get("building_phone", "").strip(),
            building_fax=request.POST.get("building_fax", "").strip(),
        )

        if building:
            for k, v in fields.items():
                setattr(building, k, v)
            if request.FILES.get("photo"):
                building.photo = request.FILES["photo"]
            building.save()
        else:
            building = Building(**fields)
            if request.FILES.get("photo"):
                building.photo = request.FILES["photo"]
            building.save()

        return redirect(reverse("building_saved", args=[building.pk]) + "?created=1")

    return render(
        request,
        "core/building_detail.html",
        _building_form_context(request.user, building=building)
    )


@login_required
def building_saved_view(request, pk):
    building = get_object_or_404(Building, pk=pk)
    return render(request, "core/building_saved.html", {
        **get_sidebar_context(request.user),
        "building": building,
        "created": request.GET.get("created"),
    })


@login_required
@require_POST
def building_delete_view(request, pk):
    building = get_object_or_404(Building, pk=pk)
    request.session["building_deleted_name"] = building.name
    building.delete()
    return redirect("buildings")


@login_required
def building_report_view(request, pk):
    building = get_object_or_404(Building, pk=pk)

    weather_data = None
    weather_error = None

    query = (
        f"{building.latitude},{building.longitude}"
        if building.latitude and building.longitude
        else building.city or None
    )

    if query:
        try:
            r = requests.get(
                "https://api.weatherapi.com/v1/current.json",
                params={"key": WEATHER_API_KEY, "q": query, "aqi": "yes"},
                timeout=5,
            )
            weather_data = r.json() if r.status_code == 200 else None
            if not weather_data:
                weather_error = f"API error {r.status_code}"
        except Exception as e:
            weather_error = str(e)

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    this_yr = [0] * 12
    last_yr = [0] * 12
    d_labels = ["HVAC", "Lighting", "Other"]
    d_vals = [0, 0, 0]

    if building.building_database and building.building_database.db_file:
        try:
            db_path = building.building_database.db_file.path
            conn = sqlite3.connect(db_path)
            cur = conn.cursor()

            # current year
            cur.execute("""
                SELECT month, SUM(kwh)
                FROM energy_monthly
                WHERE building_name = ?
                  AND year = CAST(strftime('%Y', 'now') AS INTEGER)
                GROUP BY month
                ORDER BY month
            """, ("Sample Tower",))
            for m, v in cur.fetchall():
                if 1 <= m <= 12:
                    this_yr[m - 1] = float(v or 0)

            # previous year
            cur.execute("""
                SELECT month, SUM(kwh)
                FROM energy_monthly
                WHERE building_name = ?
                  AND year = CAST(strftime('%Y', 'now') AS INTEGER) - 1
                GROUP BY month
                ORDER BY month
            """, ("Sample Tower",))
            for m, v in cur.fetchall():
                if 1 <= m <= 12:
                    last_yr[m - 1] = float(v or 0)

            # breakdown
            cur.execute("""
                SELECT category, SUM(kwh)
                FROM energy_breakdown
                WHERE building_name = ?
                GROUP BY category
            """, ("Sample Tower",))
            cats = {row[0]: float(row[1] or 0) for row in cur.fetchall()}
            d_vals = [
                cats.get("HVAC", 0),
                cats.get("Lighting", 0),
                cats.get("Other", 0),
            ]

            cur.close()
            conn.close()
        except Exception:
            # swallow errors for now; you can log them later
            pass

    return render(request, "core/building_report.html", {
        **get_sidebar_context(request.user),
        "building": building,
        "weather_data": weather_data,
        "weather_error": weather_error,
        "monthly_labels": json.dumps(months),
        "last_year_recent": json.dumps(this_yr),
        "baseline_year_before": json.dumps(last_yr),
        "donut_labels": json.dumps(d_labels),
        "donut_values": json.dumps(d_vals),
    })


@login_required
def clients_view(request):
    if request.user.is_superuser or request.user.is_staff or request.user.is_provider:
        clients = Client.objects.all()
    else:
        clients = Client.objects.filter(memberships__user=request.user).distinct()
    deleted_name = request.session.pop("client_deleted_name", None)
    delete_error = request.session.pop("client_delete_error", None)
    return render(request, "core/clients.html", {
        **get_sidebar_context(request.user),
        "clients": clients,
        "deleted_name": deleted_name,
        "delete_error": delete_error,
    })


@login_required
@require_POST
def client_delete_view(request, pk):
    client = get_object_or_404(Client, pk=pk)

    try:
        client_name = client.name
        client.delete()
        request.session["client_deleted_name"] = client_name
        request.session["client_delete_error"] = None
    except ProtectedError:
        request.session["client_deleted_name"] = None
        request.session["client_delete_error"] = (
            f'Client "{client.name}" cannot be deleted because one or more buildings are linked to it.'
        )

    return redirect("clients")


@login_required
def client_detail_view(request, pk=None):
    client = get_object_or_404(Client, pk=pk) if pk else None
    if request.method == "POST":
        name = request.POST.get("client_name", "").strip()
        if not name:
            return render(request, "core/client_detail.html", {
                **get_sidebar_context(request.user),
                "client": client, "country_choices": COUNTRY_CHOICES,
                "partnership_choices": PARTNERSHIP_CHOICES, "name_error": True,
            })
        data = {
            "name": name,
            "address":     request.POST.get("client_address", "").strip(),
            "city":        request.POST.get("client_city", "").strip(),
            "state":       request.POST.get("client_state", "").strip(),
            "postal":      request.POST.get("client_postal", "").strip(),
            "country":     request.POST.get("client_country", "HK"),
            "partnership": request.POST.get("client_partnership", "skyforce"),
            "phone":       request.POST.get("client_phone", "").strip(),
            "fax":         request.POST.get("client_fax", "").strip(),
        }
        if client:
            for k, v in data.items():
                setattr(client, k, v)
            if request.FILES.get("client_logo"):
                client.logo = request.FILES["client_logo"]
            client.save()
        else:
            client = Client(**data)
            if request.FILES.get("client_logo"):
                client.logo = request.FILES["client_logo"]
            client.save()
        return redirect(reverse("client_saved", args=[client.pk]) + "?created=1")

    return render(request, "core/client_detail.html", {
        **get_sidebar_context(request.user),
        "client": client,
        "country_choices": COUNTRY_CHOICES,
        "partnership_choices": PARTNERSHIP_CHOICES,
    })


@login_required
def client_saved_view(request, pk):
    client = get_object_or_404(Client, pk=pk)
    created = request.GET.get("created")
    return render(request, "core/client_saved.html", {
        **get_sidebar_context(request.user),
        "client": client,
        "created": created,
    })


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)

        if form.is_valid():
            profile = form.save(commit=False)

            if request.FILES.get("avatar"):
                profile.avatar = request.FILES["avatar"]

            profile.save()
            messages.success(request, "Profile has been saved successfully.")
            return redirect("profile")

        messages.error(request, "Please check the form and try again.")
    else:
        form = UserProfileForm(instance=profile)

    return render(request, "accounts/profile.html", {
        **get_sidebar_context(request.user),
        "form": form,
        "profile": profile,
    })


def _is_profile_side_user(user):
    if not user.is_authenticated:
        return False

    if getattr(user, "is_superuser", False) or getattr(user, "is_staff", False):
        return True

    profile = getattr(user, "profile", None)
    if not profile:
        return False

    role = getattr(profile, "role", None)
    user_type = getattr(profile, "user_type", None)
    account_type = getattr(profile, "account_type", None)
    side = getattr(profile, "side", None)

    return (
        role in ["Profile", "profile", "admin", "internal"] or
        user_type in ["Profile", "profile", "admin", "internal"] or
        account_type in ["Profile", "profile", "admin", "internal"] or
        side in ["Profile", "profile", "admin", "internal"]
    )


def _get_user_client(user):
    profile = getattr(user, "profile", None)
    if not profile:
        return None

    if hasattr(profile, "client") and profile.client:
        return profile.client

    if hasattr(profile, "client_id") and profile.client_id:
        return Client.objects.filter(pk=profile.client_id).first()

    return None


def _user_can_access_client(user, client):
    if _is_profile_side_user(user):
        return True

    user_client = _get_user_client(user)
    return bool(user_client and user_client.pk == client.pk)


def _user_can_access_building(user, building):
    client = getattr(building, "client", None)
    if not client:
        return False
    return _user_can_access_client(user, client)


@login_required
def building_dashboard(request, building_id):
    client_ids = get_allowed_client_ids(request.user)

    building = get_object_or_404(
        Building.objects.select_related("client"),
        pk=building_id
    )

    if building.client_id not in client_ids:
        raise PermissionDenied

    return render(request, "core/building_dashboard.html", {
        **get_sidebar_context(request.user),
        "selected_building": building,
        "selected_client": building.client,
        "building_tab": "dashboard",
    })