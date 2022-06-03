from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.views.generic import CreateView, DetailView, FormView, UpdateView
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin, SingleTableView

from api.quizs.serializers import QuizWithQuestionFullStringSerializer
from contributions.models import Contribution
from contributions.tables import ContributionTable
from core.forms import form_filters_cleaned_dict, form_filters_to_list
from core.mixins import ContributorUserRequiredMixin
from core.utils.s3 import S3Upload
from history.utilities import get_diff_between_two_history_records
from quizs.filters import QuizFilter
from quizs.forms import QUIZ_FORM_FIELDS, QuizCreateForm, QuizEditForm, QuizQuestionFormSet
from quizs.models import Quiz
from quizs.tables import QuizTable
from stats.models import QuizAggStat
from users import constants as user_constants


class QuizListView(ContributorUserRequiredMixin, SingleTableMixin, FilterView):
    model = Quiz
    template_name = "quizs/list.html"
    context_object_name = "quizs"
    table_class = QuizTable
    filterset_class = QuizFilter

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.select_related("author").prefetch_related("tags", "questions")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if context["filter"].form.is_valid():
            search_dict = form_filters_cleaned_dict(context["filter"].form.cleaned_data)
            if search_dict:
                context["search_filters"] = form_filters_to_list(search_dict, with_delete_url=True)
        return context


class QuizDetailView(ContributorUserRequiredMixin, DetailView):
    model = Quiz
    template_name = "quizs/detail_view.html"
    context_object_name = "quiz"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()
        # context["quiz_dict"] = model_to_dict(quiz, fields=[field.name for field in quiz._meta.fields])
        context["quiz_dict"] = QuizWithQuestionFullStringSerializer(quiz).data
        return context


class QuizDetailEditView(ContributorUserRequiredMixin, SuccessMessageMixin, UpdateView):
    form_class = QuizEditForm
    template_name = "quizs/detail_edit.html"
    success_message = "Le quiz a été mis à jour."
    # success_url = reverse_lazy("quizs:detail_view")

    def get_object(self):
        return get_object_or_404(Quiz, id=self.kwargs.get("pk"))

    def get_form(self, *args, **kwargs):
        quiz = self.get_object()
        form = super().get_form(self.form_class)
        if not self.request.user.can_publish_quiz(quiz):
            form.fields["publish"].disabled = True
            form.fields["publish"].help_text = user_constants.ADMIN_REQUIRED_MESSAGE
            form.fields["spotlight"].disabled = True
            form.fields["spotlight"].help_text = user_constants.ADMIN_REQUIRED_MESSAGE
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = self.get_object()
        # S3 Upload form
        s3_upload = S3Upload(kind="quiz_image_background")
        context["s3_form_values"] = s3_upload.form_values
        context["s3_upload_config"] = s3_upload.config
        # User authorizations
        context["user_can_edit_quiz"] = self.request.user.can_edit_quiz(quiz)
        return context

    def get_success_url(self):
        return reverse_lazy("quizs:detail_view", args=[self.kwargs.get("pk")])


class QuizDetailQuestionListView(ContributorUserRequiredMixin, FormView):
    form_class = QuizQuestionFormSet
    template_name = "quizs/detail_questions.html"
    success_message = "Les questions du quiz ont été mises à jour."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz"] = Quiz.objects.get(id=self.kwargs.get("pk"))
        context["quiz_questions"] = context["quiz"].quizquestion_set.all()
        context["user_can_edit_quiz"] = self.request.user.can_edit_quiz(context["quiz"])
        if self.request.POST and context["user_can_edit_quiz"]:
            context["quiz_question_formset"] = QuizQuestionFormSet(self.request.POST, instance=context["quiz"])
        else:
            context["quiz_question_formset"] = QuizQuestionFormSet(instance=context["quiz"])
        return context

    def post(self, request, *args, **kwargs):
        quiz_question_formset = QuizQuestionFormSet(self.request.POST, instance=self.get_context_data()["quiz"])
        if quiz_question_formset.is_valid():
            return self.form_valid(quiz_question_formset)
        else:
            return self.form_invalid(quiz_question_formset)

    def form_valid(self, quiz_question_formset):
        quiz_question_formset.instance = self.get_context_data()["quiz"]
        quiz_question_formset.save()
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super().form_valid(quiz_question_formset)

    def form_invalid(self, quiz_question_formset):
        messages.add_message(
            self.request, messages.ERROR, "Erreur(s) dans le formulaire de modifications des questions"
        )
        return self.render_to_response(self.get_context_data())

    def get_success_url(self):
        return reverse_lazy("quizs:detail_view", args=[self.kwargs.get("pk")])


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


class QuizDetailHistoryView(ContributorUserRequiredMixin, DetailView):
    model = Quiz
    template_name = "quizs/detail_history.html"
    context_object_name = "quiz"

    def get_object(self):
        return get_object_or_404(Quiz, id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz_history"] = self.get_object().history.all()
        context["quiz_history_delta"] = list()
        for record in context["quiz_history"]:
            new_record = record
            if new_record.prev_record:
                delta_changes = get_diff_between_two_history_records(
                    new_record,
                    old_record=new_record.prev_record,
                    excluded_fields=Quiz.QUIZ_RELATION_FIELDS,
                    returns="changes",
                )
                context["quiz_history_delta"].append(delta_changes)
            else:
                delta_fields = QUIZ_FORM_FIELDS + Quiz.QUIZ_FLATTEN_FIELDS
                delta_new = [{"field": k, "new": v} for k, v in record.__dict__.items() if k in delta_fields if v]
                context["quiz_history_delta"].append(delta_new)
        return context


class QuizCreateView(ContributorUserRequiredMixin, SuccessMessageMixin, CreateView):
    form_class = QuizCreateForm
    template_name = "quizs/create.html"
    success_url = reverse_lazy("quizs:list")

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
        name_short = self.object.name if (len(self.object.name) < 20) else (self.object.name[:18] + "…")
        quiz_link = reverse_lazy("quizs:detail_view", args=[self.object.id])
        return mark_safe(f"Le quiz <a href='{quiz_link}'><strong>{name_short}</strong></a> a été crée avec succès.")
