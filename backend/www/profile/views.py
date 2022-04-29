from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView

from questions.filters import QuestionFilter
from questions.models import Question
from questions.tables import QuestionTable
from quizs.models import Quiz
from quizs.tables import QuizTable
from users.models import User
from users.tables import ContributorTable


class ProfileHomeView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile/home.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contributor_count"] = User.objects.filter(roles__contains=[User.USER_ROLE_CONTRIBUTOR]).count()
        return context


class ProfileInfoView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "profile/info.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user


class ProfileQuestionsView(LoginRequiredMixin, SingleTableMixin, FilterView):
    model = Question
    template_name = "profile/questions.html"
    context_object_name = "user_questions"
    table_class = QuestionTable
    filterset_class = QuestionFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("category", "author_link", "validator_link").prefetch_related("tags")
        qs = qs.filter(author_link=self.request.user)
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        request_params = [value for (key, value) in self.request.GET.items() if ((key not in ["page"]) and value)]
        if len(request_params):
            context["active_filters"] = True
        return context


class ProfileQuizsView(LoginRequiredMixin, SingleTableView):
    model = Quiz
    template_name = "profile/quizs.html"
    context_object_name = "user_quizs"
    table_class = QuizTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("author_link").prefetch_related("tags")
        qs = qs.filter(author_link=self.request.user)
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context


class ProfileAdminContributorListView(LoginRequiredMixin, SingleTableView):
    model = User
    template_name = "profile/admin_contributors.html"
    context_object_name = "contributors"
    table_class = ContributorTable

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("questions", "quizs")
        qs = qs.filter(roles__contains=[User.USER_ROLE_CONTRIBUTOR])
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context
