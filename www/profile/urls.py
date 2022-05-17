from django.urls import include, path
from django.views.generic.base import RedirectView

from www.profile.views import (
    ProfileAdminContributorListView,
    ProfileAdminHistoryListView,
    ProfileHomeView,
    ProfileInfoView,
    ProfileQuestionListView,
    ProfileQuizListView,
)


app_name = "profile"

urlpatterns = [
    path("", ProfileHomeView.as_view(), name="home"),
    path("info/", ProfileInfoView.as_view(), name="info"),
    path("questions/", ProfileQuestionListView.as_view(), name="questions"),
    path("quizs/", ProfileQuizListView.as_view(), name="quizs"),
    path(
        "admin/",
        include(
            [
                path(
                    "",
                    RedirectView.as_view(pattern_name="profile:home", permanent=False),
                    name="admin_home",
                ),
                path("contributors/", ProfileAdminContributorListView.as_view(), name="admin_contributors"),
                path("history/", ProfileAdminHistoryListView.as_view(), name="admin_history"),
            ]
        ),
    ),
]
