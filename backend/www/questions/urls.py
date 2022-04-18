from django.urls import include, path
from django.views.generic.base import RedirectView

from www.questions.views import (
    QuestionDetailContributionsView,
    QuestionDetailQuizsView,
    QuestionDetailStatsView,
    QuestionDetailView,
    QuestionListView,
)


app_name = "questions"

urlpatterns = [
    path("", QuestionListView.as_view(), name="list"),
    # path("<int:pk>/", QuestionDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/",
        include(
            [
                # path("", QuestionDetailView.as_view(), name="detail"),
                path(
                    "",
                    RedirectView.as_view(pattern_name="questions:detail_view", permanent=False),
                    name="detail",
                ),
                path("view/", QuestionDetailView.as_view(), name="detail_view"),
                path("quizs/", QuestionDetailQuizsView.as_view(), name="detail_quizs"),
                path("comments/", QuestionDetailContributionsView.as_view(), name="detail_contributions"),
                path("stats/", QuestionDetailStatsView.as_view(), name="detail_stats"),
            ]
        ),
    ),
]
