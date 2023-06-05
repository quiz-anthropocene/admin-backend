from django.urls import include, path

from www.profile.views import (
    ProfileHistoryListView,
    ProfileHomeView,
    ProfileInfoView,
    ProfileQuestionListStatsView,
    ProfileQuestionListView,
    ProfileQuizListView,
    ProfileStatsQuizsListView,
)


app_name = "profile"

urlpatterns = [
    path("", ProfileHomeView.as_view(), name="home"),
    path("info/", ProfileInfoView.as_view(), name="info"),
    path(
        "questions/",
        include(
            [
                path("", ProfileQuestionListView.as_view(), name="questions"),
                path("stats/", ProfileQuestionListStatsView.as_view(), name="questions_stats"),
            ]
        ),
    ),
    path("quizs/", ProfileQuizListView.as_view(), name="quizs"),
    path("history/", ProfileHistoryListView.as_view(), name="history"),
    path("stats_quizs/", ProfileStatsQuizsListView.as_view(), name="stats_quizs"),
]
