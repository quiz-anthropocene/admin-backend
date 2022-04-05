from django.urls import path

from www.questions.views import QuestionDetailView, QuestionListView


app_name = "questions"

urlpatterns = [
    path("", QuestionListView.as_view(), name="list"),
    path("<int:pk>/", QuestionDetailView.as_view(), name="detail"),
]
