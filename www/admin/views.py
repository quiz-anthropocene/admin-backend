from itertools import chain

from django.contrib import messages
from django.db.models import Value
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView, TemplateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from activity.utilities import create_event
from core.forms import form_filters_cleaned_dict, form_filters_to_list
from core.mixins import AdministratorUserRequiredMixin
from glossary.models import GlossaryItem
from history.tables import HistoryTable
from questions.models import Question
from quizs.models import Quiz
from users.filters import ContributorFilter
from users.forms import ContributorCreateForm
from users.models import User
from users.tables import ContributorTable


class AdminHomeView(AdministratorUserRequiredMixin, DetailView):
    model = User
    template_name = "admin/home.html"
    context_object_name = "user"

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["contributor_count"] = User.objects.all_contributors().count()
        return context


class AdminContributorListView(AdministratorUserRequiredMixin, SingleTableMixin, FilterView):
    model = User
    template_name = "admin/contributors.html"
    context_object_name = "contributors"
    table_class = ContributorTable
    filterset_class = ContributorFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.prefetch_related("questions", "quizs")
        qs = qs.all_contributors()
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


class AdminContributorCreateView(AdministratorUserRequiredMixin, CreateView):
    form_class = ContributorCreateForm
    template_name = "admin/contributors_create.html"
    success_url = reverse_lazy("admin:contributors")

    def form_valid(self, form):
        # create user
        contributor = form.save(commit=False)
        password = User.objects.make_random_password()
        contributor.set_password(password)
        contributor.save()

        # add user to mailing list
        # done in users/models.py (post_save)

        # create event
        create_event(user=self.request.user, event_verb="CREATED", event_object=contributor)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            self.get_success_message(form.cleaned_data),
        )
        return HttpResponseRedirect(self.success_url)

    def get_success_message(self, cleaned_data):
        return mark_safe(
            f"Le contributeur <strong>{cleaned_data['first_name']} {cleaned_data['last_name']}</strong> a été crée avec succès."  # noqa
        )


class AdminHistoryListView(AdministratorUserRequiredMixin, TemplateView):
    template_name = "admin/history.html"

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
