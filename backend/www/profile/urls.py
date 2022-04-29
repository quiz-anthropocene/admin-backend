from django.urls import path

from www.profile.views import ProfileHomeView, ProfileInfoView, ProfileQuestionsView, ProfileQuizsView


app_name = "profile"

urlpatterns = [
    path("", ProfileHomeView.as_view(), name="home"),
    path("info/", ProfileInfoView.as_view(), name="info"),
    path("questions/", ProfileQuestionsView.as_view(), name="questions"),
    path("quizs/", ProfileQuizsView.as_view(), name="quizs"),
]
