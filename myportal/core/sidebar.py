from .models import Client, BuildingUser
from accounts.models import UserProfile


def get_allowed_client_ids(user):
    """
    Clients the user is allowed to access.
    - superuser / staff / provider: all clients
    - client user: only the client linked via BuildingUser
    - fallback: ClientMembership
    """
    if user.is_superuser or user.is_staff or getattr(user, "is_provider", False):
        return Client.objects.values_list("id", flat=True)

    if getattr(user, "is_client_user", False):
        building_user = (
            BuildingUser.objects
            .filter(auth_user=user, is_active=True)
            .select_related("client")
            .first()
        )
        if building_user:
            return Client.objects.filter(pk=building_user.client_id).values_list("id", flat=True)

    return user.client_memberships.filter(is_active=True).values_list("client_id", flat=True)


def get_active_client(request):
    """
    Resolve the current working client for the request.

    Priority:
    1. explicit ?client=...
    2. session active_client_id
    3. first allowed client
    """
    user = request.user
    allowed_ids = list(get_allowed_client_ids(user))

    if not allowed_ids:
        return None

    query_client_id = request.GET.get("client")
    if query_client_id:
        try:
            query_client_id = int(query_client_id)
        except (TypeError, ValueError):
            query_client_id = None

        if query_client_id in allowed_ids:
            request.session["active_client_id"] = query_client_id
            return Client.objects.filter(pk=query_client_id).first()

    session_client_id = request.session.get("active_client_id")
    if session_client_id in allowed_ids:
        return Client.objects.filter(pk=session_client_id).first()

    first_client = Client.objects.filter(pk__in=allowed_ids).order_by("name", "pk").first()
    if first_client:
        request.session["active_client_id"] = first_client.pk
    return first_client


def get_sidebar_context(user, request=None):
    client_ids = get_allowed_client_ids(user)
    clients = Client.objects.filter(id__in=client_ids).prefetch_related("buildings").order_by("name", "pk")

    active_client = None
    if request is not None and user.is_authenticated:
        active_client = get_active_client(request)

    return {
        "sidebar_clients": clients,
        "sidebar_profile": get_user_profile_safe(user),
        "active_client": active_client,
    }


def get_user_profile_safe(user):
    if not user.is_authenticated:
        return None
    return UserProfile.objects.filter(user=user).first()