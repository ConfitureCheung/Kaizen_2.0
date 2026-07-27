from .models import Client
from accounts.models import UserProfile


def get_allowed_client_ids(user):
    if user.is_superuser or user.is_staff or user.is_provider:
        return Client.objects.values_list("id", flat=True)
    return user.client_memberships.filter(is_active=True).values_list("client_id", flat=True)


def get_sidebar_context(user):
    client_ids = get_allowed_client_ids(user)
    clients = Client.objects.filter(id__in=client_ids).prefetch_related("buildings")
    return {
        "sidebar_clients": clients,
        "sidebar_profile": get_user_profile_safe(user),
    }


def get_user_profile_safe(user):
    if not user.is_authenticated:
        return None
    return UserProfile.objects.filter(user=user).first()