from django.urls import include, path
from django.views.generic.base import RedirectView

from django.views.generic import TemplateView

from www.questions.views import (
    QuestionAutocomplete,
    QuestionCreateView,
    QuestionDetailCommentListView,
    QuestionDetailEditView,
    QuestionDetailHistoryView,
    QuestionDetailQuizListView,
    QuestionDetailStatsView,
    QuestionDetailView,
    QuestionImportODSView,
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
                path("edit/", QuestionDetailEditView.as_view(), name="detail_edit"),
                path("quizs/", QuestionDetailQuizListView.as_view(), name="detail_quizs"),
                path("comments/", QuestionDetailCommentListView.as_view(), name="detail_comments"),
                path("stats/", QuestionDetailStatsView.as_view(), name="detail_stats"),
                path("history/", QuestionDetailHistoryView.as_view(), name="detail_history"),
            ]
        ),
    ),
    path("create/", QuestionCreateView.as_view(), name="create"),
    path("import-ods/", QuestionImportODSView.as_view(), name="import_ods"),
    path("import-ods/format/", TemplateView.as_view(template_name="questions/import_ods_doc.html"), name="import_ods_doc"),
    path("search/", QuestionAutocomplete.as_view(), name="search"),
]
