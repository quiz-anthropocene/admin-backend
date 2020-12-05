from django.urls import path, include

from app import views
from api.admin import admin_site


urlpatterns = [
    path("", views.app_home),
    path("admin/", admin_site.urls),
    path("api/", include("api.urls")),
    path("actions/aggregate-stats", views.action_aggregate_stats),
    path(
        "actions/import-questions-from-notion",
        views.action_import_questions_from_notion,
    ),
    path("actions/export-data-to-github", views.action_export_data_to_github),
]
