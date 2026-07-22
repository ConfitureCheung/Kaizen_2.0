from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Client, Building, ClientGroup, BuildingUser


def get_allowed_client_ids(user):
    if user.is_superuser or user.is_staff or user.is_provider:
        return Client.objects.values_list("id", flat=True)
    return user.client_memberships.filter(is_active=True).values_list("client_id", flat=True)


@login_required
def dashboard_view(request):
    client_ids = get_allowed_client_ids(request.user)
    buildings = Building.objects.filter(client_id__in=client_ids)
    clients = Client.objects.filter(id__in=client_ids)
    return render(request, "dashboard.html", {
        "buildings": buildings,
        "clients": clients,
    })


@login_required
def users_view(request):
    client_ids = get_allowed_client_ids(request.user)
    users = BuildingUser.objects.filter(client_id__in=client_ids)
    return render(request, "core/users.html", {"users": users})


@login_required
def user_detail_view(request):
    return render(request, "core/user_detail.html")


@login_required
def groups_view(request):
    client_ids = get_allowed_client_ids(request.user)
    groups = ClientGroup.objects.filter(client_id__in=client_ids)
    return render(request, "core/groups.html", {"groups": groups})


''' Sample Building is required to show building_report.html '''
@login_required
def buildings_view(request):
    sample_buildings = []
    sample_saved_buildings = [
        {
            "name": "Sunshine Building",
            "city": "",
            "country": "HK",
            "client": "-",
        }
    ]
    return render(request, "core/buildings.html", {
        "buildings": sample_buildings,
        "sample_saved_buildings": sample_saved_buildings,
    })


@login_required
def building_detail_view(request):
    return render(request, "core/building_detail.html")


''' fake sample data, to use db in next step '''
@login_required
def building_report_view(request):
    monthly_labels = [
        "2025-01", "2025-02", "2025-03", "2025-04", "2025-05", "2025-06",
        "2025-07", "2025-08", "2025-09", "2025-10", "2025-11", "2025-12",
    ]
    last_year_recent = [220, 230, 248, 240, 255, 268, 275, 281, 276, 270, 262, 258]
    baseline_year_before = [210, 215, 225, 228, 233, 240, 246, 249, 251, 248, 242, 238]

    donut_labels = ["Room Temp Logs", "Total KWH Logs"]
    donut_values = [45, 55]

    return render(request, "core/building_report.html", {
        "building_name": "Sunshine Building",
        "building_country": "HK",
        "monthly_labels": monthly_labels,
        "last_year_recent": last_year_recent,
        "baseline_year_before": baseline_year_before,
        "donut_labels": donut_labels,
        "donut_values": donut_values,
        "insight_count": 2,
    })


@login_required
def clients_view(request):
    if request.user.is_superuser or request.user.is_staff or request.user.is_provider:
        clients = Client.objects.all()
    else:
        clients = Client.objects.filter(memberships__user=request.user).distinct()
    return render(request, "core/clients.html", {"clients": clients})


@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")


@login_required
def client_detail_view(request):
    return render(request, "core/client_detail.html")


@login_required
def client_saved_view(request):
    return render(request, "core/client_saved.html")