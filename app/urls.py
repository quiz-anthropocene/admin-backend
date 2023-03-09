from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path

from core.admin import admin_site


contribution_patterns = i18n_patterns(
    path("", include("www.pages.urls")),
    path("accounts/", include("www.auth.urls")),
    path("profile/", include("www.profile.urls")),
    path("questions/", include("www.questions.urls")),
    path("quizs/", include("www.quizs.urls")),
    path("categories/", include("www.categories.urls")),
    path("tags/", include("www.tags.urls")),
    path("contributions/", include("www.contributions.urls")),
    path("glossary/", include("www.glossary.urls")),
    path("activity/", include("www.activity.urls")),
    path("admin/", include("www.admin.urls")),
)

urlpatterns = contribution_patterns + [
    # set_language
    path("i18n/", include("django.conf.urls.i18n")),
    # admin
    path("django/", admin_site.urls),
    # api
    path("api/", include("api.urls")),
    # stats
    path("stats/", include("stats.urls")),
]

if settings.DEBUG:  # and "debug_toolbar" in settings.INSTALLED_APPS:
    urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
