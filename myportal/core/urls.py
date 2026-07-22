from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.users_view, name="users"),
    path("users/add/", views.user_detail_view, name="user_detail"),
    path("groups/", views.groups_view, name="groups"),
    path("groups/add/", views.group_detail_view, name="group_detail"),
    path("groups/<int:pk>/", views.group_saved_view, name="group_saved"),
    path("groups/<int:pk>/members/", views.group_members_view, name="group_members"),
    path("buildings/", views.buildings_view, name="buildings"),
    path("buildings/add/", views.building_detail_view, name="building_detail"),
    path("buildings/report/", views.building_report_view, name="building_report"),
    path("clients/", views.clients_view, name="clients"),
    path("clients/add/", views.client_detail_view, name="client_detail"),
    path("clients/saved/", views.client_saved_view, name="client_saved"),
    path("profile/", views.profile_view, name="profile"),
]
