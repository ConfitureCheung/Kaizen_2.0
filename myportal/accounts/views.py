from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls import reverse


def custom_login(request):
    if request.user.is_authenticated:
        return redirect(_post_login_url(request.user))

    context = {}

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next") or request.POST.get("next")
            return redirect(next_url or _post_login_url(user))

        context["error"] = "Invalid username or password."

    return render(request, "accounts/login.html", context)


def custom_logout(request):
    logout(request)
    return redirect("login")


def _post_login_url(user):
    """
    Superuser/staff/provider -> dashboard, which will auto-pick first allowed client.
    Client user -> dashboard pre-scoped to their own client.
    """
    if getattr(user, "is_client_user", False) and not user.is_superuser and not user.is_staff:
        from core.models import BuildingUser

        building_user = (
            BuildingUser.objects
            .filter(auth_user=user, is_active=True)
            .select_related("client")
            .first()
        )
        if building_user and building_user.client_id:
            return f'{reverse("dashboard")}?client={building_user.client_id}'

    return reverse("dashboard")