from django.urls import include, path
from django.views.generic.base import RedirectView

from www.tags.views import (
    TagCreateView,
    TagDetailEditView,
    TagDetailQuestionListView,
    TagDetailQuizListView,
    TagDetailView,
    TagListView,
)


app_name = "tags"

urlpatterns = [
    path("", TagListView.as_view(), name="list"),
    # path("<int:pk>/", TagDetailView.as_view(), name="detail"),
    path(
        "<int:pk>/",
        include(
            [
                # path("", TagDetailView.as_view(), name="detail"),
                path(
                    "",
                    RedirectView.as_view(pattern_name="tags:detail_view", permanent=False),
                    name="detail",
                ),
                path("view/", TagDetailView.as_view(), name="detail_view"),
                path("edit/", TagDetailEditView.as_view(), name="detail_edit"),
                path("questions/", TagDetailQuestionListView.as_view(), name="detail_questions"),
                path("quizs/", TagDetailQuizListView.as_view(), name="detail_quizs"),
            ]
        ),
    ),
    path("create/", TagCreateView.as_view(), name="create"),
]
