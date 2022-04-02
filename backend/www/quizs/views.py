from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView

from quizs.models import Quiz
from quizs.tables import QuizTable


class QuizListView(LoginRequiredMixin, SingleTableView):
    model = Quiz
    template_name = "quizs/list.html"
    context_object_name = "quizs"
    table_class = QuizTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("tags")
        return qs
