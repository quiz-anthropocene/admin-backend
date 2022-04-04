from django.urls import path

from www.quizs.views import QuizListView


app_name = "quizs"

urlpatterns = [
    path("", QuizListView.as_view(), name="list"),
]
