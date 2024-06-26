from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, DetailView, FormView, ListView, UpdateView
from django.views.generic.edit import FormMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin

from activity.utilities import create_event
from api.quizs.serializers import QuizWithQuestionFullStringSerializer
from contributions.forms import CommentCreateForm
from contributions.models import Comment
from contributions.tables import CommentTable
from core import constants
from core.forms import form_filters_cleaned_dict, form_filters_to_list
from core.mixins import ContributorUserRequiredMixin
from core.utils.s3 import S3Upload
from history.utilities import get_diff_between_two_history_records
from quizs.filters import QuizFilter
from quizs.forms import QUIZ_FORM_FIELDS, QuizCreateForm, QuizEditForm, QuizQuestionFormSet
from quizs.models import Quiz
from quizs.tables import QuizQuestionTable, QuizTable
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
        qs = qs.prefetch_related("tags", "questions", "authors")
        qs = qs.order_by("-created")
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
    success_message = _("The quiz was updated.")
    # success_url = reverse_lazy("quizs:detail_view")

    def get_object(self):
        return get_object_or_404(Quiz, id=self.kwargs.get("pk"))

    def get_form(self, *args, **kwargs):
        """
        - some fields are only editable by administrators (or quiz author if private)
        """
        quiz = self.get_object()
        form = super().get_form(self.form_class)
        if not self.request.user.can_publish_quiz(quiz):
            form.fields["validation_status"].disabled = True
            form.fields["validation_status"].help_text = user_constants.ADMIN_REQUIRED_EDIT_FIELD_MESSAGE_FULL
            form.fields["publish"].disabled = True
            form.fields["publish"].help_text = user_constants.ADMIN_REQUIRED_EDIT_FIELD_MESSAGE_FULL
            form.fields["spotlight"].disabled = True
            form.fields["spotlight"].help_text = user_constants.ADMIN_REQUIRED_EDIT_FIELD_MESSAGE_FULL
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # S3 Upload form
        s3_upload = S3Upload(kind="quiz_image_background")
        context["s3_form_values"] = s3_upload.form_values
        context["s3_upload_config"] = s3_upload.config
        return context

    def form_valid(self, form):
        quiz_before = self.get_object()
        quiz = form.save(commit=False)
        # Change detected on the validation_status field
        if quiz_before.validation_status != quiz.validation_status:
            # Quiz validated! set the validator data + create event
            if quiz.is_validated:
                quiz.validator = self.request.user
                quiz.validation_date = timezone.now()
                if not quiz.is_private:
                    create_event(user=self.request.user, event_verb="VALIDATED", event_object=quiz)
            # Quiz not validated anymore... reset the validator data
            elif quiz_before.is_validated:
                quiz.validator = None
                quiz.validation_date = None
        # Change detected on the publish field
        if quiz_before.publish != quiz.publish:
            # Quiz validated! set the validator data + create event
            if quiz.publish:
                quiz.publish_date = timezone.now()
                if not quiz.is_private:
                    create_event(user=self.request.user, event_verb="PUBLISHED", event_object=quiz)
            # Quiz not published anymore... reset the extra data
            elif quiz_before.publish:
                quiz.publish_date = None
        quiz.save()

        messages.add_message(
            self.request,
            messages.SUCCESS,
            self.get_success_message(form.cleaned_data),
        )
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy("quizs:detail_view", args=[self.kwargs.get("pk")])


class QuizDetailQuestionListView(ContributorUserRequiredMixin, SingleTableMixin, FormView):
    template_name = "quizs/detail_questions.html"
    success_message = _("The quiz questions were updated.")
    table_class = QuizQuestionTable
    form_class = QuizQuestionFormSet

    def get(self, request, *args, **kwargs):
        self.quiz = Quiz.objects.get(id=self.kwargs.get("pk"))
        return super().get(request, *args, **kwargs)

    def get_table_data(self):
        return self.quiz.quizquestion_set.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz"] = self.quiz
        context["user_can_edit"] = self.request.user.can_edit_quiz(self.quiz)
        if self.request.POST and context["user_can_edit"]:
            context["quiz_question_formset"] = QuizQuestionFormSet(self.request.POST, instance=self.quiz)
        else:
            context["quiz_question_formset"] = QuizQuestionFormSet(instance=self.quiz)
        return context

    def post(self, request, *args, **kwargs):
        self.quiz = Quiz.objects.get(id=self.kwargs.get("pk"))
        quiz_question_formset = QuizQuestionFormSet(self.request.POST, instance=self.quiz)
        if quiz_question_formset.is_valid():
            return self.form_valid(quiz_question_formset)
        else:
            return self.form_invalid(quiz_question_formset)

    def form_valid(self, quiz_question_formset):
        quiz_question_formset.instance = self.quiz
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


class QuizDetailCommentListView(ContributorUserRequiredMixin, SingleTableMixin, FormMixin, ListView):
    model = Comment
    template_name = "quizs/detail_comments.html"
    context_object_name = "quiz_contributions"
    table_class = CommentTable
    form_class = CommentCreateForm

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.filter(quiz__id=self.kwargs.get("pk"))
        qs = qs.order_by("-created")
        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["quiz"] = Quiz.objects.get(id=self.kwargs.get("pk"))
        return context

    def get_initial(self):
        return {
            "type": constants.COMMENT_TYPE_COMMENT_CONTRIBUTOR,
            "quiz": self.kwargs.get("pk"),
            "status": constants.COMMENT_STATUS_PROCESSED,
            "author": self.request.user,
            "parent": None,
        }

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.save()
        # response
        messages.add_message(self.request, messages.SUCCESS, self.get_success_message(form.cleaned_data))
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data())

    def get_success_message(self, cleaned_data):
        return _("Your message was created.")

    def get_success_url(self):
        return reverse_lazy("quizs:detail_comments", args=[self.kwargs.get("pk")])


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
    # success_message = ""

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        self.object.authors.set([self.request.user])

        # create event
        if not self.object.is_private:
            create_event(user=self.request.user, event_verb="CREATED", event_object=self.object)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            self.get_success_message(form.cleaned_data),
        )
        return HttpResponseRedirect(self.get_success_url())

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
        quiz_name_short = self.object.name if (len(self.object.name) < 20) else (self.object.name[:18] + "…")
        quiz_url = reverse_lazy("quizs:detail_view", args=[self.object.id])
        quiz_link = f"<a href='{quiz_url}' title='{self.object.name}'><strong>{quiz_name_short}</strong></a>"
        return mark_safe(_("The quiz {quiz_link} was created.").format(quiz_link=quiz_link))
