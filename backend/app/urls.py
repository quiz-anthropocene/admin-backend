from django.conf import settings
from django.urls import include, path

from app import views
from core.admin import admin_site


urlpatterns = [
    path("", include("www.pages.urls")),
    path("accounts/", include("www.auth.urls")),
    path("questions/", include("www.questions.urls")),
    path("quizs/", include("www.quizs.urls")),
    path("admin/", admin_site.urls),
    path("api/", include("api.urls")),
    path("stats/", include("stats.urls")),
    path("actions/aggregate-stats", views.action_aggregate_stats),
    path(
        "actions/import-questions-from-notion",
        views.action_import_questions_from_notion,
    ),
    path("actions/export-data-to-github", views.action_export_data_to_github),
    path("actions/export-stats-to-github", views.action_export_stats_to_github),
    path(
        "actions/export-contributions-to-notion",
        views.action_export_contributions_to_notion,
    ),
]

if settings.DEBUG:  # and "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
