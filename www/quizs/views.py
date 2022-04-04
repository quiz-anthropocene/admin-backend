from django.contrib.auth.mixins import LoginRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from quizs.filters import QuizFilter
from quizs.models import Quiz
from quizs.tables import QuizTable


class QuizListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Quiz
    template_name = "quizs/list.html"
    context_object_name = "quizs"
    table_class = QuizTable
    filterset_class = QuizFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("tags")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_params = [value for (key, value) in self.request.GET.items() if ((key not in ["page"]) and value)]
        if len(request_params):
            context["active_filters"] = True
        return context
