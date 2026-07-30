from django.urls import path
from . import views

urlpatterns = [
    # ── Users ──
    path("users/", views.users_view, name="users"),
    path("users/add/", views.user_detail_view, name="user_detail"),
    path("users/<int:pk>/", views.user_view_view, name="user_view"),
    path("users/<int:pk>/edit/", views.user_detail_view, name="user_edit"),
    path("users/<int:pk>/delete/", views.user_delete_view, name="user_delete"),

    # ── Groups ──
    path("groups/", views.groups_view, name="groups"),
    path("groups/add/", views.group_detail_view, name="group_detail"),
    path("groups/<int:pk>/", views.group_saved_view, name="group_saved"),
    path("groups/<int:pk>/members/", views.group_members_view, name="group_members"),
    path("groups/<int:pk>/delete/", views.group_delete_view, name="group_delete"),

    # ── Buildings ──
    path("buildings/", views.buildings_view, name="buildings"),
    path("buildings/add/", views.building_detail_view, name="building_detail"),
    path("buildings/<int:pk>/edit/", views.building_detail_view, name="building_edit"),
    path("buildings/<int:pk>/", views.building_saved_view, name="building_saved"),
    path("buildings/<int:pk>/delete/", views.building_delete_view, name="building_delete"),
    path("buildings/<int:pk>/report/", views.building_report_view, name="building_report"),

    # ── Clients ──
    path("clients/", views.clients_view, name="clients"),
    path("clients/add/", views.client_detail_view, name="client_detail"),
    path("clients/<int:pk>/edit/", views.client_detail_view, name="client_edit"),
    path("clients/<int:pk>/delete/", views.client_delete_view, name="client_delete"),
    path("clients/<int:pk>/", views.client_saved_view, name="client_saved"),

    # ── Profile ──
    path("profile/", views.profile_view, name="profile"),

    path("", views.dashboard_view, name="dashboard"),
    path("dashboard/", views.dashboard_view, name="dashboard"),

    # ── Vault ──
    path("buildings/<int:building_id>/dashboard/", views.building_dashboard, name="building_dashboard"),
    path('buildings/<int:pk>/vault/trend-logs/', views.vault_trend_logs, name='vault_trend_logs'),
    path('buildings/<int:pk>/vault/objects/', views.vault_objects, name='vault_objects'),

    # ── Insights ──
    path('buildings/<int:pk>/insights/management/', views.insight_management, name='insight_management'),
    path('buildings/<int:pk>/insights/create-report/', views.create_insight_report, name='create_insight_report'),
    path('buildings/<int:pk>/insights/manage-rules/', views.manage_rules, name='manage_rules'),
    path('buildings/<int:pk>/insights/golden-standard/', views.golden_standard_configuration,
         name='golden_standard_configuration'),
    path('buildings/<int:pk>/insights/subscription/', views.insight_subscription, name='insight_subscription'),
]


