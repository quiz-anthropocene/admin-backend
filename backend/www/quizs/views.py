from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView

from api.quizs.serializers import QuizWithQuestionSerializer
from contributions.models import Contribution
from contributions.tables import ContributionTable
from core.mixins import ContributorUserRequiredMixin
from quizs.filters import QuizFilter
from quizs.forms import QuizCreateForm, QuizEditForm, QuizQuestionFormSet
from quizs.models import Quiz, QuizQuestion
from quizs.tables import QuizTable
from stats.models import QuizAggStat


class QuizListView(ContributorUserRequiredMixin, SingleTableMixin, FilterView):
    model = Quiz
    template_name = "quizs/list.html"
    context_object_name = "quizs"
    table_class = QuizTable
    filterset_class = QuizFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("author_link").prefetch_related("tags", "questions")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request_params = [value for (key, value) in self.request.GET.items() if ((key not in ["page"]) and value)]
        if len(request_params):
            context["active_filters"] = True
        return context


class QuizDetailView(ContributorUserRequiredMixin, DetailView):
    model = Quiz
    template_name = "quizs/detail_view.html"
    context_object_name = "quiz"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()
        # context["quiz_dict"] = model_to_dict(quiz, fields=[field.name for field in quiz._meta.fields])
        context["quiz_dict"] = QuizWithQuestionSerializer(quiz).data
        return context


class QuizDetailEditView(ContributorUserRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = QuizEditForm
    template_name = "quizs/detail_edit.html"
    success_message = "Le quiz a été mis à jour."
    # success_url = reverse_lazy("quizs:detail_view")

    def get_object(self):
        return get_object_or_404(Quiz, id=self.kwargs.get("pk"))

    def get_success_url(self):
        return reverse_lazy("quizs:detail_view", args=[self.kwargs.get("pk")])


class QuizDetailQuestionListView(ContributorUserRequiredMixin, ListView):
    model = QuizQuestion
    template_name = "quizs/detail_questions.html"
    context_object_name = "quiz_questions"

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("question")
        qs = qs.filter(quiz__id=self.kwargs.get("pk"))
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz"] = Quiz.objects.get(id=self.kwargs.get("pk"))
        context["quiz_question_formset"] = QuizQuestionFormSet(instance=context["quiz"])
        return context


class QuizDetailQuestionListEditView(ContributorUserRequiredMixin, UpdateView):
    form_class = QuizQuestionFormSet
    template_name = "quizs/detail_questions_edit_modal.html"
    success_message = "Les questions du quiz ont été mises à jour."
    # success_url = reverse_lazy("quizs:detail_questions")

    def get_object(self):
        return get_object_or_404(Quiz, id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["quiz_question_formset"] = QuizQuestionFormSet(self.request.POST, instance=self.object)
        else:
            context["quiz_question_formset"] = QuizQuestionFormSet(instance=self.object)
        return context

    def get_success_url(self):
        return reverse_lazy("quizs:detail_questions", args=[self.kwargs.get("pk")])


class QuizDetailContributionListView(ContributorUserRequiredMixin, SingleTableView):
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


class QuizDetailStatsView(ContributorUserRequiredMixin, DetailView):
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


class QuizCreateView(ContributorUserRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = QuizCreateForm
    template_name = "quizs/create.html"
    success_url = reverse_lazy("quizs:list")

    def get_success_url(self):
        success_url = super().get_success_url()
        next_url = self.request.GET.get("next", None)
        # sanitize next_url
        if next_url:
            # safe_url = get_safe_url(self.request, param_name="next")
            # if safe_url:
            #     return safe_url
            return next_url
        return success_url

    def get_success_message(self, cleaned_data):
        name_short = self.object.name if (len(self.object.name) < 20) else (self.object.name[:18] + "…")
        quiz_link = reverse_lazy("quizs:detail_view", args=[self.object.id])
        return mark_safe(f"Le quiz <a href='{quiz_link}'><strong>{name_short}</strong></a> a été crée avec succès.")

    def form_valid(self, form):
        """Set the author."""
        quiz = form.save(commit=False)
        quiz.author = self.request.user.full_name
        quiz.author_link = self.request.user
        quiz.save()
        return super().form_valid(form)
