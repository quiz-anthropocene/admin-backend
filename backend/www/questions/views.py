from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.views.generic import DetailView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from questions.filters import QuestionFilter
from questions.models import Question
from questions.tables import QuestionTable


class QuestionListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Question
    template_name = "questions/list.html"
    context_object_name = "questions"
    table_class = QuestionTable
    filterset_class = QuestionFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("category").prefetch_related("tags")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_params = [value for (key, value) in self.request.GET.items() if ((key not in ["page"]) and value)]
        if len(request_params):
            context["active_filters"] = True
        return context


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = "questions/detail.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question_dict"] = model_to_dict(self.get_object())
        # print(context["question_dict"])
        return context
