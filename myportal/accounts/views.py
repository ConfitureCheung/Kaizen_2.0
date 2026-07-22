from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


def custom_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    context = {}

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get("next") or request.POST.get("next")
            return redirect(next_url or "dashboard")

        context["error"] = "Invalid username or password."

    return render(request, "accounts/login.html", context)


def custom_logout(request):
    logout(request)
    return redirect("login")
