from itertools import chain

from django.db.models import Value
from django.views.generic import DetailView, TemplateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView

from core.forms import form_filters_cleaned_dict, form_filters_to_list
from core.mixins import AdministratorUserRequiredMixin, ContributorUserRequiredMixin
from glossary.models import GlossaryItem
from history.tables import HistoryTable
from questions.filters import QuestionFilter
from questions.models import Question
from questions.tables import QuestionTable
from quizs.models import Quiz
from quizs.tables import QuizTable
from users.models import User
from users.tables import ContributorTable


class ProfileHomeView(ContributorUserRequiredMixin, DetailView):
    model = User
    template_name = "profile/home.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contributor_count"] = User.objects.all_contributors().count()
        return context


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
        qs = qs.filter(author=self.request.user)
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        if context["filter"].form.is_valid():
            search_dict = form_filters_cleaned_dict(context["filter"].form.cleaned_data)
            if search_dict:
                context["search_filters"] = form_filters_to_list(search_dict)
        return context


class ProfileQuizListView(ContributorUserRequiredMixin, SingleTableView):
    model = Quiz
    template_name = "profile/quizs.html"
    context_object_name = "user_quizs"
    table_class = QuizTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("author").prefetch_related("tags")
        qs = qs.filter(author=self.request.user)
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
                GlossaryItem.history.annotate(object_model=Value("Glossaire")).filter(history_user=self.request.user),
            )
        )
        question_quiz_history.sort(key=lambda x: x.history_date, reverse=True)
        context["table"] = HistoryTable(question_quiz_history[:50])  # TODO: pagination ?
        return context


class ProfileAdminContributorListView(AdministratorUserRequiredMixin, SingleTableView):
    model = User
    template_name = "profile/admin_contributors.html"
    context_object_name = "contributors"
    table_class = ContributorTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("questions", "quizs")
        qs = qs.all_contributors()
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ProfileAdminHistoryListView(AdministratorUserRequiredMixin, TemplateView):
    template_name = "profile/admin_history.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question_quiz_history = list(
            chain(
                Question.history.annotate(object_model=Value("Question")).all(),
                Quiz.history.annotate(object_model=Value("Quiz")).all(),
                GlossaryItem.history.annotate(object_model=Value("Glossaire")).all(),
            )
        )
        question_quiz_history.sort(key=lambda x: x.history_date, reverse=True)
        context["table"] = HistoryTable(question_quiz_history[:50])  # TODO: pagination ?
        return context
