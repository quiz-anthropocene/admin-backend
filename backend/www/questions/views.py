from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView

from api.questions.serializers import QuestionFullStringSerializer
from contributions.models import Contribution
from contributions.tables import ContributionTable
from questions.filters import QuestionFilter
from questions.forms import QuestionEditForm
from questions.models import Question
from questions.tables import QuestionTable
from quizs.models import QuizQuestion
from stats.models import QuestionAggStat


class QuestionListView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Question
    template_name = "questions/list.html"
    context_object_name = "questions"
    table_class = QuestionTable
    filterset_class = QuestionFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("category", "author_link", "validator_link").prefetch_related("tags")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_params = [value for (key, value) in self.request.GET.items() if ((key not in ["page"]) and value)]
        if len(request_params):
            context["active_filters"] = True
        return context


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = "questions/detail_view.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        # context["question_dict"] = model_to_dict(question, fields=[field.name for field in question._meta.fields])
        context["question_dict"] = QuestionFullStringSerializer(question).data
        return context


class QuestionDetailEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = QuestionEditForm
    template_name = "questions/detail_edit.html"
    success_message = "La question a été mise à jour."
    # success_url = reverse_lazy("questions:detail_view")

    def get_object(self):
        return get_object_or_404(Question, id=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy("questions:detail_view", args=[self.kwargs.get("pk")])


class QuestionDetailQuizsView(LoginRequiredMixin, ListView):
    model = QuizQuestion
    template_name = "questions/detail_quizs.html"
    context_object_name = "quiz_questions"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(question__id=self.kwargs.get("pk"))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = Question.objects.get(id=self.kwargs.get("pk"))
        return context


class QuestionDetailContributionsView(LoginRequiredMixin, SingleTableView):
    model = Contribution
    template_name = "questions/detail_contributions.html"
    context_object_name = "question_contributions"
    table_class = ContributionTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(question__id=self.kwargs.get("pk"))
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question"] = Question.objects.get(id=self.kwargs.get("pk"))
        return context


class QuestionDetailStatsView(LoginRequiredMixin, DetailView):
    model = QuestionAggStat
    template_name = "questions/detail_stats.html"
    context_object_name = "question_stats"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(question__id=self.kwargs.get("pk"))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question_agg_stat_dict"] = model_to_dict(self.get_object())
        del context["question_agg_stat_dict"]["question"]
        context["question"] = Question.objects.get(id=self.kwargs.get("pk"))
        return context
