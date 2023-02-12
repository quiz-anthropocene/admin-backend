from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path, re_path

from core.admin import admin_site


urlpatterns = i18n_patterns(
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
    path("admin/", include("www.admin.urls")),
    # admin
    path("django/", admin_site.urls),
    # api
    path("api/", include("api.urls")),
    # stats
    path("stats/", include("stats.urls")),
    path("i18n/", include("django.conf.urls.i18n")),
)

if "rosetta" in settings.INSTALLED_APPS:
    urlpatterns += [re_path(r"^rosetta/", include("rosetta.urls"))]

if settings.DEBUG:  # and "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
