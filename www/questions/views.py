from dal import autocomplete
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView

from api.questions.serializers import QuestionFullStringSerializer
from contributions.models import Contribution
from contributions.tables import ContributionTable
from core.forms import form_filters_cleaned_dict, form_filters_to_list
from core.mixins import ContributorUserRequiredMixin
from history.utilities import get_diff_between_two_history_records
from questions.filters import QuestionFilter
from questions.forms import QUESTION_FORM_FIELDS, QuestionCreateForm, QuestionEditForm
from questions.models import Question
from questions.tables import QuestionTable
from quizs.models import QuizQuestion
from stats.models import QuestionAggStat
from users import constants as user_constants


class QuestionListView(ContributorUserRequiredMixin, SingleTableMixin, FilterView):
    model = Question
    template_name = "questions/list.html"
    context_object_name = "questions"
    table_class = QuestionTable
    filterset_class = QuestionFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("category", "author", "validator").prefetch_related("tags")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_dict = form_filters_cleaned_dict(context["filter"].form.cleaned_data)
        if search_dict:
            context["search_filters"] = form_filters_to_list(search_dict)
        return context


class QuestionDetailView(ContributorUserRequiredMixin, DetailView):
    model = Question
    template_name = "questions/detail_view.html"
    context_object_name = "question"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        # context["question_dict"] = model_to_dict(question, fields=[field.name for field in question._meta.fields])
        context["question_dict"] = QuestionFullStringSerializer(question).data
        return context


class QuestionDetailEditView(ContributorUserRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = QuestionEditForm
    template_name = "questions/detail_edit.html"
    success_message = "La question a été mise à jour."
    # success_url = reverse_lazy("questions:detail_view")

    def get_object(self):
        return get_object_or_404(Question, id=self.kwargs.get("pk"))

    def get_form(self, *args, **kwargs):
        question = self.get_object()
        form = super().get_form(self.form_class)
        if not self.request.user.can_validate_question(question):
            form.fields["validation_status"].disabled = True
            form.fields["validation_status"].help_text = user_constants.ADMIN_REQUIRED_MESSAGE
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = self.get_object()
        context["user_can_edit_question"] = self.request.user.can_edit_question(question)
        return context

    def get_success_url(self):
        return reverse_lazy("questions:detail_view", args=[self.kwargs.get("pk")])


class QuestionDetailQuizListView(ContributorUserRequiredMixin, ListView):
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


class QuestionDetailContributionListView(ContributorUserRequiredMixin, SingleTableView):
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


class QuestionDetailStatsView(ContributorUserRequiredMixin, DetailView):
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


class QuestionDetailHistoryView(ContributorUserRequiredMixin, DetailView):
    model = Question
    template_name = "questions/detail_history.html"
    context_object_name = "question"

    def get_object(self):
        return get_object_or_404(Question, id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["question_history"] = self.get_object().history.all()
        context["question_history_delta"] = list()
        for record in context["question_history"]:
            new_record = record
            if new_record.prev_record:
                delta_changes = get_diff_between_two_history_records(
                    new_record,
                    old_record=new_record.prev_record,
                    excluded_fields=Question.QUESTION_RELATION_FIELDS,
                    returns="changes",
                )
                context["question_history_delta"].append(delta_changes)
            else:
                # probably a create action
                # we create the diff ourselves because there isn't any previous record
                delta_fields = QUESTION_FORM_FIELDS + Question.QUESTION_FLATTEN_FIELDS
                delta_new = [{"field": k, "new": v} for k, v in record.__dict__.items() if k in delta_fields if v]
                context["question_history_delta"].append(delta_new)
        return context


class QuestionCreateView(ContributorUserRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = QuestionCreateForm
    template_name = "questions/create.html"
    success_url = reverse_lazy("questions:list")

    def get_initial(self):
        return {"author": self.request.user}

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
        text_short = self.object.text if (len(self.object.text) < 20) else (self.object.text[:18] + "…")
        question_link = reverse_lazy("questions:detail_view", args=[self.object.id])
        return mark_safe(
            f"La question <a href='{question_link}'><strong>{text_short}</strong></a> a été crée avec succès."
        )


class QuestionAutocomplete(ContributorUserRequiredMixin, autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Question.objects.all()

        if self.q:
            qs = qs.filter(Q(id=self.q) | Q(text__icontains=self.q))

        return qs
