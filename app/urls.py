from django.conf import settings
from django.urls import include, path

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
    path("glossary/", include("www.glossary.urls")),
    # admin
    path("admin/", admin_site.urls),
    # api
    path("api/", include("api.urls")),
    # stats
    path("stats/", include("stats.urls")),
]

if settings.DEBUG:  # and "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
