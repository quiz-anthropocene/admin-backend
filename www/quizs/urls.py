from django.urls import include, path
from django.views.generic.base import RedirectView

from www.quizs.views import QuizDetailContributionsView, QuizDetailStatsView, QuizDetailView, QuizListView


app_name = "quizs"

urlpatterns = [
    path("", QuizListView.as_view(), name="list"),
    # path("<int:pk>/", QuizDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/",
        include(
            [
                # path("", QuizDetailView.as_view(), name="detail"),
                path(
                    "",
                    RedirectView.as_view(pattern_name="quizs:detail_view", permanent=False),
                    name="detail",
                ),
                path("view/", QuizDetailView.as_view(), name="detail_view"),
                path("comments/", QuizDetailContributionsView.as_view(), name="detail_contributions"),
                path("stats/", QuizDetailStatsView.as_view(), name="detail_stats"),
            ]
        ),
    ),
]
