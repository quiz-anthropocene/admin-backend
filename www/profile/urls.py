from django.urls import include, path

from www.profile.views import (
    ProfileCommentListView,
    ProfileCommentNewListView,
    ProfileHistoryListView,
    ProfileHomeView,
    ProfileInfoView,
    ProfileQuestionListStatsView,
    ProfileQuestionListView,
    ProfileQuizListStatsView,
    ProfileQuizListView,
)


app_name = "profile"

urlpatterns = [
    path("", ProfileHomeView.as_view(), name="home"),
    path("info/", ProfileInfoView.as_view(), name="info"),
    path(
        "questions/",
        include(
            [
                path("", ProfileQuestionListView.as_view(), name="questions_view"),
                path("stats/", ProfileQuestionListStatsView.as_view(), name="questions_stats"),
            ]
        ),
    ),
    path(
        "quizs/",
        include(
            [
                path("", ProfileQuizListView.as_view(), name="quizs_view"),
                path("stats/", ProfileQuizListStatsView.as_view(), name="quizs_stats"),
            ]
        ),
    ),
    path(
        "comments/",
        include(
            [
                path("", ProfileCommentListView.as_view(), name="comments_view"),
                path("new/", ProfileCommentNewListView.as_view(), name="comments_new"),
            ]
        ),
    ),
    path("history/", ProfileHistoryListView.as_view(), name="history"),
]
