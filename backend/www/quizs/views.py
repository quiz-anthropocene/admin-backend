from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms.models import model_to_dict
from django.views.generic import DetailView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView

from api.quizs.serializers import QuizSerializer
from contributions.models import Contribution
from contributions.tables import ContributionTable
from quizs.filters import QuizFilter
from quizs.models import Quiz
from quizs.tables import QuizTable
from stats.models import QuizAggStat


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


class QuizDetailView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = "quizs/detail_view.html"
    context_object_name = "quiz"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()
        # context["quiz_dict"] = model_to_dict(quiz, fields=[field.name for field in quiz._meta.fields])
        context["quiz_dict"] = QuizSerializer(quiz).data
        return context


class QuizDetailContributionsView(LoginRequiredMixin, SingleTableView):
    model = Contribution
    template_name = "quizs/detail_contributions.html"
    context_object_name = "quiz_contributions"
    table_class = ContributionTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(quiz__id=self.kwargs.get("pk"))
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz"] = Quiz.objects.get(id=self.kwargs.get("pk"))
        return context


class QuizDetailStatsView(LoginRequiredMixin, DetailView):
    model = QuizAggStat
    template_name = "quizs/detail_stats.html"
    context_object_name = "quiz_stats"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(quiz__id=self.kwargs.get("pk"))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz_agg_stat_dict"] = model_to_dict(self.get_object())
        del context["quiz_agg_stat_dict"]["quiz"]
        context["quiz"] = Quiz.objects.get(id=self.kwargs.get("pk"))
        return context
