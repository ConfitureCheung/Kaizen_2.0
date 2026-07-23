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
    path("buildings/<int:pk>/edit/", views.building_detail_view, name="building_edit"),
    path("buildings/<int:pk>/", views.building_saved_view, name="building_saved"),
    path("buildings/<int:pk>/delete/", views.building_delete_view, name="building_delete"),
    path("buildings/<int:pk>/report/", views.building_report_view, name="building_report"),

    path("clients/", views.clients_view, name="clients"),
    path("clients/add/", views.client_detail_view, name="client_detail"),
    path("clients/<int:pk>/edit/", views.client_detail_view, name="client_edit"),
    path("clients/<int:pk>/delete/", views.client_delete_view, name="client_delete"),
    path("clients/<int:pk>/", views.client_saved_view, name="client_saved"),

    path("profile/", views.profile_view, name="profile"),
]

