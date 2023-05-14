from itertools import chain

from django.db.models import Value
from django.views.generic import DetailView, TemplateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView

from core.forms import form_filters_cleaned_dict, form_filters_to_list
from core.mixins import ContributorUserRequiredMixin
from glossary.models import GlossaryItem
from history.tables import HistoryTable
from questions.filters import QuestionFilter
from questions.models import Question
from questions.tables import QuestionTable
from quizs.models import Quiz
from quizs.tables import QuizTable
from stats.models import QuestionAggStat, QuizAggStat
from stats.tables import QuestionsStatsTable, QuizsStatsTable

# from stats.models import QuestionAggStat, QuizAggStat
from users.models import User


class ProfileHomeView(ContributorUserRequiredMixin, DetailView):
    model = User
    template_name = "profile/home.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user


class ProfileInfoView(ContributorUserRequiredMixin, DetailView):
    model = User
    template_name = "profile/info.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user


class ProfileQuestionListView(ContributorUserRequiredMixin, SingleTableMixin, FilterView):
    model = Question
    template_name = "profile/questions.html"
    context_object_name = "user_questions"
    table_class = QuestionTable
    filterset_class = QuestionFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("category", "author", "validator").prefetch_related("tags")
        qs = qs.for_author(self.request.user)
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        if context["filter"].form.is_valid():
            search_dict = form_filters_cleaned_dict(context["filter"].form.cleaned_data)
            if search_dict:
                context["search_filters"] = form_filters_to_list(search_dict, with_delete_url=True)
        return context


class ProfileQuizListView(ContributorUserRequiredMixin, SingleTableView):
    model = Quiz
    template_name = "profile/quizs.html"
    context_object_name = "user_quizs"
    table_class = QuizTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("tags", "authors")
        qs = qs.for_author(self.request.user)
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ProfileHistoryListView(ContributorUserRequiredMixin, TemplateView):
    template_name = "profile/history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_quiz_history = list(
            chain(
                Question.history.annotate(object_model=Value("Question")).filter(history_user=self.request.user),
                Quiz.history.annotate(object_model=Value("Quiz")).filter(history_user=self.request.user),
                GlossaryItem.history.annotate(object_model=Value("GlossaryItem")).filter(
                    history_user=self.request.user
                ),
            )
        )
        question_quiz_history.sort(key=lambda x: x.history_date, reverse=True)
        context["table"] = HistoryTable(question_quiz_history[:50])  # TODO: pagination ?
        return context


class ProfileStatsQuestionsListView(ContributorUserRequiredMixin, SingleTableView):
    model = QuestionAggStat
    template_name = "profile/stats_questions.html"
    context_object_name = "user_questions_stats"
    table_class = QuestionsStatsTable
    # filterset_class = QuestionFilter

    def get_queryset(self):
        qs = super().get_queryset()
        questions = Question.objects.for_author(self.request.user)
        qs = QuestionAggStat.objects.filter(question__in=questions)
        qs = qs.order_by("-question__created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        """
        if context["filter"].form.is_valid():
            search_dict = form_filters_cleaned_dict(context["filter"].form.cleaned_data)
            if search_dict:
                context["search_filters"] = form_filters_to_list(search_dict, with_delete_url=True)
                """
        return context


class ProfileStatsQuizsListView(ContributorUserRequiredMixin, SingleTableView):
    model = QuizAggStat
    template_name = "profile/stats_quizs.html"
    context_object_name = "user_quizs_stats"
    table_class = QuizsStatsTable
    # filterset_class = QuizFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = QuizAggStat.objects.filter(quiz__in=self.request.user.quizs.all())
        qs = qs.order_by("-quiz__created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        """
        if context["filter"].form.is_valid():
            search_dict = form_filters_cleaned_dict(context["filter"].form.cleaned_data)
            if search_dict:
                context["search_filters"] = form_filters_to_list(search_dict, with_delete_url=True)
                """
        return context
