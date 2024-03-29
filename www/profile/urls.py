from django.urls import include, path

from www.profile.views import (
    ProfileCommentListView,
    ProfileCommentNewListView,
    ProfileHistoryListView,
    ProfileHomeView,
    ProfileInfoCardCreateView,
    ProfileInfoCardEditView,
    ProfileInfoCardView,
    ProfileInfoView,
    ProfileQuestionListStatsView,
    ProfileQuestionListView,
    ProfileQuizListStatsView,
    ProfileQuizListView,
)


app_name = "profile"

urlpatterns = [
    path("", ProfileHomeView.as_view(), name="home"),
    path(
        "info/",
        include(
            [
                path("", ProfileInfoView.as_view(), name="info_view"),
                path("card/", ProfileInfoCardView.as_view(), name="info_card_view"),
            ]
        ),
    ),
    path("info/card/create", ProfileInfoCardCreateView.as_view(), name="info_card_create"),
    path("info/card/edit", ProfileInfoCardEditView.as_view(), name="info_card_edit"),
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
