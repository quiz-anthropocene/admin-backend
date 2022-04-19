from django.conf import settings
from django.urls import include, path

from app import views
from core.admin import admin_site


urlpatterns = [
    # www
    path("", include("www.pages.urls")),
    path("accounts/", include("www.auth.urls")),
    path("profile/", include("www.profile.urls")),
    path("questions/", include("www.questions.urls")),
    path("quizs/", include("www.quizs.urls")),
    path("categories/", include("www.categories.urls")),
    path("tags/", include("www.tags.urls")),
    path("contributions/", include("www.contributions.urls")),
    # admin
    path("admin/", admin_site.urls),
    # api
    path("api/", include("api.urls")),
    # stats
    path("stats/", include("stats.urls")),
    # actions
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
