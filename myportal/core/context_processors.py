from .models import Client, Building


def sidebar_navigation(request):
    if not request.user.is_authenticated:
        return {
            "sidebar_clients": [],
            "sidebar_profile": None,
        }

    profile = getattr(request.user, "profile", None)

    clients_qs = Client.objects.prefetch_related("buildings").order_by("name")

    if getattr(request.user, "is_superuser", False) or getattr(request.user, "is_staff", False):
        sidebar_clients = clients_qs
    else:
        role = getattr(profile, "role", None) if profile else None
        user_type = getattr(profile, "user_type", None) if profile else None
        account_type = getattr(profile, "account_type", None) if profile else None
        side = getattr(profile, "side", None) if profile else None

        is_profile_user = (
            role in ["Profile", "profile", "admin", "internal"] or
            user_type in ["Profile", "profile", "admin", "internal"] or
            account_type in ["Profile", "profile", "admin", "internal"] or
            side in ["Profile", "profile", "admin", "internal"]
        )

        if is_profile_user:
            sidebar_clients = clients_qs
        else:
            client = getattr(profile, "client", None) if profile else None
            if client:
                sidebar_clients = clients_qs.filter(pk=client.pk)
            elif getattr(profile, "client_id", None):
                sidebar_clients = clients_qs.filter(pk=profile.client_id)
            else:
                sidebar_clients = Client.objects.none()

    return {
        "sidebar_clients": sidebar_clients,
        "sidebar_profile": profile,
    }