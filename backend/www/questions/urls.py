from django.urls import include, path

from www.questions.views import QuestionDetailView, QuestionListView  # , QuestionDetailContributionsView


app_name = "questions"

urlpatterns = [
    path("", QuestionListView.as_view(), name="list"),
    # path("<int:pk>/", QuestionDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/",
        include(
            [
                path("", QuestionDetailView.as_view(), name="detail"),
                # path("", QuestionDetailContributionsView.as_view(), name="detail_contributions")
            ]
        ),
    ),
]
