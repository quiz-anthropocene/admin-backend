from django.urls import path

from www.questions.views import QuestionListView


app_name = "questions"

urlpatterns = [
    path("", QuestionListView.as_view(), name="list"),
]
