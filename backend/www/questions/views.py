from django.contrib.auth.mixins import LoginRequiredMixin
from django_tables2 import SingleTableView

from questions.models import Question
from questions.tables import QuestionTable


class QuestionListView(LoginRequiredMixin, SingleTableView):
    model = Question
    template_name = "questions/list.html"
    context_object_name = "questions"
    table_class = QuestionTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("category").prefetch_related("tags")
        return qs
