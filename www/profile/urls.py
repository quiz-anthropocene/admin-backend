from django.urls import path

from www.profile.views import (
    ProfileHistoryListView,
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
    path("history/", ProfileHistoryListView.as_view(), name="history"),
]
